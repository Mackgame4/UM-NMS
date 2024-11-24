from protocols import MAX_BUFFER_SIZE, AGENT_REGISTER_COMMAND, AGENT_RECEIVED_COMMAND, TASK_REQUEST_COMMAND, TASK_RESULT_COMMAND, AGENT_READY_COMMAND, NetTask as NT, AlertFlow as AF
from encoder import decode_message, encode_message
from notify import notify
import socket
import threading
import subprocess
import sys
import queue
import psutil
import json

class NMS_Agent:
    def __init__(self, host='127.0.0.1', port=8888):
        self.alert_flow = AF(host, port)
        self.net_task = NT(host, port)

    ### Class methods (Client-side) ###
    def get_cpu_usage(self):
        try:
            cpu = psutil.cpu_percent(interval=1) # We could also use the psutil library to get the CPU usage for a determined process
            return cpu
        except Exception as e:
            notify("error", f"Error getting CPU Usage: {e}")
            return None

    def get_ram_usage(self):
        try:
            ram = psutil.virtual_memory()
            ram_usage = ram.percent
            return ram_usage
        except Exception as e:
            notify("error", f"Error getting RAM Usage: {e}")
            return None

    def get_interface_stats(self): # Get network interface stats
        try:
            eth_stats = psutil.net_io_counters(pernic=True)
            notify("debug", f"Available network interfaces: {list(eth_stats.keys())}") # List of available network interfaces
            return eth_stats
        except Exception as e:
            notify("error", f"Error getting network interface stats: {e}")
            return None

    def run_device_metrics(self, device, result_queue): # Run device metrics tests
        device_metrics_results = {}
        # Get cpu usage if device['device_metrics']['cpu'] is True
        if device['device_metrics']['cpu_usage']:
            cpu_usage = self.get_cpu_usage()
            if cpu_usage is not None:
                notify("info", f"CPU Usage: {cpu_usage}%")
                device_metrics_results['cpu_usage'] = cpu_usage
        # Get ram usage if device['device_metrics']['ram'] is True
        if device['device_metrics']['ram_usage']:
            ram_usage = self.get_ram_usage()
            if ram_usage is not None:
                notify("info", f"RAM Usage: {ram_usage}%")
                device_metrics_results['ram_usage'] = ram_usage
        # Get interface stats if device['device_metrics']['interface_stats'] is not empty
        for eth in device['device_metrics']['interface_stats']:
            eth_stats = self.get_interface_stats()
            if eth_stats is not None:
                if eth in eth_stats: # Check if the eth interface exists in available interfaces
                    eth_name = eth
                    eth_bytes_sent = eth_stats[eth].bytes_sent
                    eth_bytes_recv = eth_stats[eth].bytes_recv
                    notify("info", f"Interface {eth_name}: Bytes sent: {eth_bytes_sent}, Bytes received: {eth_bytes_recv}")
                    device_metrics_results[eth_name] = {"bytes_sent": eth_bytes_sent, "bytes_recv": eth_bytes_recv}
                else:
                    notify("warning", f"Interface {eth} not found in network interfaces.")
        result_queue.put(device_metrics_results)
        return device_metrics_results

    def run_link_metrics(self, device, result_queue): # Run network tests
        link_metric_results = {}
        for metric_name in device['link_metrics']:
            notify("info", f"Running {metric_name} metrics test")
            metric = device['link_metrics'][metric_name]
            metric_tool = metric['tool']
            if metric_tool == 'iperf':
                metric_role = metric.get('role', 'server') # Default role is server
                metric_server_address = metric.get('server_address', '0.0.0.0') # Default server address
                metric_duration = metric.get('duration', 10) # Default duration is 10 seconds
                metric_transport = '-u' if metric.get('transport', 'tcp') == 'udp' else '' # Default transport is TCP
                metric_frequency = metric.get('frequency', 1) # Default frequency is 1
                if metric_role == 'server':
                    command = f"iperf3 -s".strip()
                elif metric_role == 'client':
                    command = f"iperf3 -c {metric_server_address} -t {metric_duration} -J {metric_transport}".strip()
                for i in range(1, metric_frequency+1):
                    # Run the command and get the output
                    notify("debug", f"Running command: {command}; {i}/{metric_frequency} times")
                    result = self.run_process(command, metric_name)
                    if metric_name == 'jitter' and result:
                        try:
                            json_output = json.loads(result)
                            jitter = json_output['end']['sum']['jitter_ms']
                            notify("debug", f"Jitter: {jitter} ms")
                            link_metric_results[metric_name] = jitter
                        except Exception as e:
                            notify("error", f"Error parsing iperf3 output: {e}")
                    if metric_name == 'bandwidth' and result:
                        try:
                            json_output = json.loads(result)
                            bandwidth = json_output['end']['sum_sent']['bits_per_second']
                            notify("debug", f"Bandwidth: {bandwidth} bps")
                            link_metric_results[metric_name] = bandwidth
                        except Exception as e:
                            notify("error", f"Error parsing iperf3 output: {e}")
                    if metric_name == 'packet_loss' and result:
                        try:
                            json_output = json.loads(result)
                            packet_loss = json_output['end']['sum']['lost_percent']
                            notify("debug", f"Packet Loss: {packet_loss}%")
                            link_metric_results[metric_name] = packet_loss
                        except Exception as e:
                            notify("error", f"Error parsing iperf3 output: {e}")
            if metric_tool == 'ping':
                metric_destination_address = metric.get('destination', '127.0.0.1')
                metric_packet_count = metric.get('packet_count', 4)
                metric_frequency = metric.get('frequency', 1)
                command = f"ping {metric_destination_address} -c {metric_packet_count}".strip()
                for i in range(1, metric_frequency+1):
                    # Run the command and get the output
                    notify("debug", f"Running command: {command}; {i}/{metric_frequency} times")
                    result = self.run_process(command, metric_name)
                    if metric_name == 'latency' and result:
                        try:
                            latency = float(result.split('/')[-1].split()[0])
                            notify("debug", f"Latency: {latency} ms")
                            link_metric_results[metric_name] = latency
                        except Exception as e:
                            notify("error", f"Error parsing ping output for latency: {e}")
        result_queue.put(link_metric_results)
        return link_metric_results
    
    def run_process(self, command, name):
        stdout = None
        try:
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            stdout = stdout.strip().decode()
            stderr = stderr.strip().decode()
            if stdout:
                notify("debug", f"Link metrics test {name} results: {stdout}")
            if stderr:
                notify("error", f"Error running command: {stderr}")
        except Exception as e:
            notify("error", f"Error running command: {e}")
        return stdout

    def run_task(self, id, frequency, device): # Run the task
        task_results = {}
        result_queue = queue.Queue()
        for i in range(1, frequency+1):
            notify("debug", f"Running {i}/{frequency} from task {id}")
            device_metrics_thread = threading.Thread(target=self.run_device_metrics, args=(device, result_queue))
            link_metrics_thread = threading.Thread(target=self.run_link_metrics, args=(device, result_queue))
            device_metrics_thread.start()
            link_metrics_thread.start()
            device_metrics_thread.join()
            link_metrics_thread.join()
            while not result_queue.empty():
                result = result_queue.get()
                task_results.update(result)
        return task_results

    ### AlertFlow methods (Client-side) ###
    def start_alert_flow(self):
        alert_flow = self.alert_flow
        alert_flow.socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        notify("info", f"AlertFlow Client connected at {alert_flow.host}:{alert_flow.port}")
        alert_flow.socket_tcp.connect((alert_flow.host, alert_flow.port))

    ### NetTask methods (Client-side) ###
    def start_net_task(self):
        # Start the NetTask client-side socket
        net_task = self.net_task
        net_task.socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        notify("info", f"NetTask Client connected at {net_task.host}:{net_task.port}")
        s_addr = (net_task.host, net_task.port)

        # Send requests to the server to register the agent and receive the assigned agent_id (only visual, server is the one that keeps track of the agents)
        net_task.socket_udp.sendto(encode_message(AGENT_REGISTER_COMMAND), s_addr)
        data, _ = net_task.socket_udp.recvfrom(MAX_BUFFER_SIZE)
        message = decode_message(data)
        if message.command == AGENT_RECEIVED_COMMAND:
            agent_id = message.data
            notify("success", f"You were assigned Agent ID: {agent_id}")

        # Send requests to the server to notify that the agent is ready to receive tasks
        net_task.socket_udp.sendto(encode_message(AGENT_READY_COMMAND), s_addr)

        while True:
            data, _ = net_task.socket_udp.recvfrom(MAX_BUFFER_SIZE)
            message = decode_message(data)

            # Client received task request: Run it and send the result back to the server
            if message.command == TASK_REQUEST_COMMAND:
                task_id = message.data['task_id']
                task_frequency = message.data['frequency']
                task_device = message.data['device']
                notify("info", f"Received task: {task_id} with frequency {task_frequency}")
                # Run task and send the result back to the server
                result = self.run_task(task_id, task_frequency, task_device)
                net_task.socket_udp.sendto(encode_message(TASK_RESULT_COMMAND, result), s_addr)
                # Tell server that the task was completed and agent is ready for more tasks
                #net_task.socket_udp.sendto(encode_message(AGENT_READY_COMMAND), s_addr)

### Runnable Section ###
def main(args):
    agent = NMS_Agent()
    if len(args) >= 2:
        host = args[0]
        port = int(args[1])
        agent = NMS_Agent(host, port)
    elif len(args) >= 1:
        host = args[0]
        agent = NMS_Agent(host)
    alert_thread = threading.Thread(target=agent.start_alert_flow)
    net_task_thread = threading.Thread(target=agent.start_net_task)
    alert_thread.start()
    net_task_thread.start()
    alert_thread.join()
    net_task_thread.join()

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)