from protocols import MAX_BUFFER_SIZE, AGENT_REGISTER_COMMAND, TASK_REQUEST_COMMAND, TASK_RESULT_COMMAND, AGENT_READY_COMMAND, NetTask as NT, AlertFlow as AF
from encoder import decode_message, encode_message
from notify import notify
import socket
import threading
import subprocess
import sys

class NMS_Agent:
    def __init__(self, host='127.0.0.1', port=8888):
        self.alert_flow = AF(host, port)
        self.net_task = NT(host, port)

    ### Class methods (Client-side) ###
    def run_task(self, task):
        result = subprocess.run(task.split(), capture_output=True)
        notify("debug", f"Task result: {result.stdout.decode()}")
        return result.stdout.decode()

    ### AlertFlow methods (Client-side) ###
    def start_alert_flow(self):
        alert_flow = self.alert_flow
        alert_flow.socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        notify("info", f"AlertFlow Client connected at {alert_flow.host}:{alert_flow.port}")
        alert_flow.socket_tcp.connect((alert_flow.host, alert_flow.port))

    ### NetTask methods (Client-side) ###
    def start_net_task(self):
        net_task = self.net_task
        net_task.socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        notify("info", f"NetTask Client connected at {net_task.host}:{net_task.port}")

        # Send requests to the server to register the agent and receive the assigned agent_id
        net_task.socket_udp.sendto(encode_message(AGENT_REGISTER_COMMAND), (net_task.host, net_task.port))
        data, _ = net_task.socket_udp.recvfrom(MAX_BUFFER_SIZE)
        agent_id = decode_message(data)
        notify("warning", f"Assigned Agent ID: {agent_id}")

        # Send a message to the server to indicate that the agent is ready to receive tasks
        net_task.socket_udp.sendto(encode_message(AGENT_READY_COMMAND), (net_task.host, net_task.port))

        while True:
            # Wait for task requests from the server
            data, _ = net_task.socket_udp.recvfrom(MAX_BUFFER_SIZE)
            message = decode_message(data)

            if message.startswith(TASK_REQUEST_COMMAND):
                task = message[len(TASK_REQUEST_COMMAND) + 1:].strip()
                notify("debug", f"Received task: {task}")
                
                # Wait for result and send it back to the server
                result = self.run_task(task)
                net_task.socket_udp.sendto(encode_message(TASK_RESULT_COMMAND + f": {result}"), (net_task.host, net_task.port))

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
    alert_thread.join()
    net_task_thread.join()

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)