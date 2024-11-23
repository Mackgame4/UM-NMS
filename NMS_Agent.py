from protocols import MAX_BUFFER_SIZE, AGENT_REGISTER_COMMAND, AGENT_RECEIVED_COMMAND, TASK_REQUEST_COMMAND, TASK_RESULT_COMMAND, AGENT_READY_COMMAND, NetTask as NT, AlertFlow as AF
from encoder import decode_message, encode_message
from notify import notify
import socket
import threading
import subprocess
import sys
import time
import psutil

class NMS_Agent:
    def __init__(self, host='127.0.0.1', port=8888):
        self.alert_flow = AF(host, port)
        self.net_task = NT(host, port)

    ### Class methods (Client-side) ###
    # We could also use the psutil library to get the CPU usage for a determined process
    def get_cpu_usage(self):
        try:
            cpu = psutil.cpu_percent(interval=1)
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
            #notify("debug", f"Available network interfaces: {list(eth_stats.keys())}") # List of available network interfaces
            return eth_stats
        except Exception as e:
            notify("error", f"Error getting network interface stats: {e}")
            return None

    def run_task(self, id, frequency, device):
        #notify("debug", f"Running task: {id}")
        for i in range(frequency):
            # Run the task
            notify("debug", f"Running task {id} {i+1}/{frequency} times")
            # Get cpu usage if device['device_metrics']['cpu'] is True
            if device['device_metrics']['cpu_usage']:
                cpu_usage = self.get_cpu_usage()
                if cpu_usage is not None:
                    notify("info", f"CPU Usage: {cpu_usage}%")
            if device['device_metrics']['ram_usage']:
                ram_usage = self.get_ram_usage()
                if ram_usage is not None:
                    notify("info", f"RAM Usage: {ram_usage}%")
            for eth in device['device_metrics']['interface_stats']:
                eth_stats = self.get_interface_stats()
                if eth_stats is not None:
                    if eth in eth_stats: # Check if the eth interface exists in available interfaces
                        eth_name = eth
                        eth_bytes_sent = eth_stats[eth].bytes_sent
                        eth_bytes_recv = eth_stats[eth].bytes_recv
                        notify("info", f"Interface {eth_name}: Bytes sent: {eth_bytes_sent}, Bytes received: {eth_bytes_recv}")
                    else:
                        notify("warning", f"Interface {eth} not found in network interfaces.")

            # Sleep for 1 seconds
            time.sleep(1)

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
                #notify("debug", f"Received task: {task_id} with frequency {task_frequency} for device {task_device}")
                notify("info", f"Received task: {task_id}")
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
    alert_thread = threading.Thread(target=agent.start_alert_flow)
    net_task_thread = threading.Thread(target=agent.start_net_task)
    alert_thread.start()
    net_task_thread.start()
    #alert_thread.join()
    #net_task_thread.join()

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)