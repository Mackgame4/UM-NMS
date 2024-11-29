from protocols import MAX_BUFFER_SIZE, AGENT_REGISTER_COMMAND, AGENT_RECEIVED_COMMAND, TASK_REQUEST_COMMAND, TASK_REQUEST_CONFIRM_COMMAND, TASK_RESULT_COMMAND, AGENT_READY_COMMAND, NetTask as NT, AlertFlow as AF
from encoder import decode_message, encode_message
from notify import notify, notify_nt, notify_af
import socket
import threading
import subprocess
import sys
import queue
from metrics import run_device_metrics, run_link_metrics

class NMS_Agent:
    def __init__(self, host='127.0.0.1', port=8888):
        self.alert_flow = AF(host, port)
        self.net_task = NT(host, port)

    ### Class methods (Client-side) ###
    def run_task(self, id, frequency, device): # Run the task
        task_results = {}
        result_queue = queue.Queue()
        for i in range(1, frequency+1):
            notify_nt("debug", f"Running {i}/{frequency} from task {id}")
            device_metrics_thread = threading.Thread(target=run_device_metrics, args=(device, result_queue))
            link_metrics_thread = threading.Thread(target=run_link_metrics, args=(device, result_queue))
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
            notify_nt("success", f"You were assigned Agent ID: {agent_id}")

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
                notify_nt("info", f"Received task: {task_id} with frequency {task_frequency}")
                # Send task confirmation to the server
                #net_task.socket_udp.sendto(encode_message(TASK_REQUEST_CONFIRM_COMMAND, task_id), s_addr)
                # Run task and send the result back to the server
                result = self.run_task(task_id, task_frequency, task_device)
                net_task.socket_udp.sendto(encode_message(TASK_RESULT_COMMAND, result), s_addr)
                # After sending the result to server, check if theres any values out of the normal range and send an alert in alert_flow
                alert_flow = self.alert_flow
                for metric, value in result.items():
                    metric_threshold = task_device.get('alertflow_conditions', {}).get(metric, None)
                    #print("Debug: Checking", metric, value, metric_threshold)
                    # check if value is an int, is is a dict interface_stats, dont check
                    if metric_threshold is not None:
                        if not isinstance(value, dict):
                            if value >= metric_threshold and metric == 'cpu_usage':
                                alert_flow.socket_tcp.send(encode_message(metric, value) + b'\n')
                            elif value >= metric_threshold and metric == 'ram_usage':
                                alert_flow.socket_tcp.send(encode_message(metric, value) + b'\n')
                            elif value >= metric_threshold and metric == 'packet_loss':
                                alert_flow.socket_tcp.send(encode_message(metric, value) + b'\n')
                            elif value >= metric_threshold and metric == 'jitter':
                                alert_flow.socket_tcp.send(encode_message(metric, value) + b'\n')
                        else:
                            if metric == 'interface_stats':
                                for _, stats in value.items():
                                    eth_bytes_sent = stats['bytes_sent']
                                    eth_bytes_recv = stats['bytes_recv']
                                    if eth_bytes_sent >= metric_threshold:
                                        alert_flow.socket_tcp.send(encode_message(metric, str(int(eth_bytes_sent))) + b'\n')
                                    if eth_bytes_recv >= metric_threshold:
                                        alert_flow.socket_tcp.send(encode_message(metric, str(int(eth_bytes_recv))) + b'\n')
                # Instead of sending the confirmation when it receives the taks, send when its done, this way of the agent disconnects, the task will still be in the server and it will re send it once it reconnects
                net_task.socket_udp.sendto(encode_message(TASK_REQUEST_CONFIRM_COMMAND, task_id), s_addr)
                # Tell server that the task was completed and agent is ready for more tasks
                net_task.socket_udp.sendto(encode_message(AGENT_READY_COMMAND), s_addr)

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