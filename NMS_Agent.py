from protocols import MAX_BUFFER_SIZE, AGENT_REGISTER_COMMAND, TASK_REQUEST_COMMAND, TASK_RESULT_COMMAND, NetTask as NT, AlertFlow as AF
from encoder import decode_message, encode_message
from colorama import Fore
import socket
import threading
import subprocess

class NMS_Agent:
    def __init__(self, host='127.0.0.1', port=8888):
        self.alert_flow = AF(host, port)
        self.net_task = NT(host, port)

    # Class methods (Client-side)
    def run_task(self, task):
        # Execute the task
        result = subprocess.run(task.split(), capture_output=True)
        print(Fore.CYAN + f"Task result: {result.stdout.decode()}" + Fore.RESET)
        return result.stdout.decode()

    # AlertFlow methods (Client-side)
    # TODO: Implement the AlertFlow client-side protocol
    def start_alert_flow(self):
        alert_flow = self.alert_flow
        alert_flow.socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(Fore.GREEN + f"AlertFlow Client connected at {alert_flow.host}:{alert_flow.port}" + Fore.RESET)
        alert_flow.socket_tcp.connect((alert_flow.host, alert_flow.port))

    # NetTask methods (Client-side)
    def start_net_task(self):
        net_task = self.net_task
        net_task.socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(Fore.GREEN + f"NetTask Client connected at {net_task.host}:{net_task.port}" + Fore.RESET)

        # Send requests to the server to register the agent and receive the assigned agent_id
        net_task.socket_udp.sendto(encode_message(AGENT_REGISTER_COMMAND), (net_task.host, net_task.port))
        data, _ = net_task.socket_udp.recvfrom(MAX_BUFFER_SIZE)
        agent_id = decode_message(data)
        print(Fore.YELLOW + f"Assigned Agent ID: {agent_id}" + Fore.RESET)

        while True:
            # Wait for task requests from the server
            data, _ = net_task.socket_udp.recvfrom(MAX_BUFFER_SIZE)
            message = decode_message(data)

            if message.startswith(TASK_REQUEST_COMMAND):
                task = message[len(TASK_REQUEST_COMMAND) + 1:].strip()
                print(Fore.YELLOW + f"Received task request from server: {task}" + Fore.RESET)
                
                # wait for result and send it back to the server
                result = self.run_task(task)
                net_task.socket_udp.sendto(encode_message(TASK_RESULT_COMMAND + f": {result}"), (net_task.host, net_task.port))

def main():
    agent = NMS_Agent()
    # Create threads for each protocol
    alert_thread = threading.Thread(target=agent.start_alert_flow)
    net_task_thread = threading.Thread(target=agent.start_net_task)
    # Start both threads
    alert_thread.start()
    net_task_thread.start()
    # Join threads if you want the main program to wait for them to finish
    #alert_thread.join()
    #net_task_thread.join()

if __name__ == "__main__":
    main()