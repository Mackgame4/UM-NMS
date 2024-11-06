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

    def start_alert_flow(self):
        self.alert_flow.c_start()

    def start_net_task(self):
        self.net_task.socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(Fore.GREEN + f"NetTask Client connected at {self.net_task.host}:{self.net_task.port}" + Fore.RESET)

        # Send requests to the server to register the agent and receive the assigned agent_id
        self.net_task.socket_udp.sendto(encode_message(AGENT_REGISTER_COMMAND), (self.net_task.host, self.net_task.port))
        data, _ = self.net_task.socket_udp.recvfrom(MAX_BUFFER_SIZE)
        agent_id = decode_message(data)
        print(Fore.YELLOW + f"Assigned Agent ID: {agent_id}" + Fore.RESET)

        while True:
            # Wait for task requests from the server
            data, _ = self.net_task.socket_udp.recvfrom(MAX_BUFFER_SIZE)
            message = decode_message(data)

            if message.startswith(TASK_REQUEST_COMMAND):
                task = message[len(TASK_REQUEST_COMMAND) + 1:].strip()
                print(Fore.YELLOW + f"Received task request from server: {task}" + Fore.RESET)
                
                # wait for result and send it back to the server
                result = self.run_task(task)
                self.net_task.socket_udp.sendto(encode_message(TASK_RESULT_COMMAND + f": {result}"), (self.net_task.host, self.net_task.port))

    def run_task(self, task):
        # Execute the task
        result = subprocess.run(task.split(), capture_output=True)
        return result.stdout.decode()

def main():
    agent = NMS_Agent()

    # Create threads for each protocol
    #alert_thread = threading.Thread(target=agent.run_alert_flow)
    net_task_thread = threading.Thread(target=agent.start_net_task)

    # Start both threads
    #alert_thread.start()
    net_task_thread.start()

    # Optionally, join threads if you want the main program to wait for them to finish
    #alert_thread.join()
    net_task_thread.join()

if __name__ == "__main__":
    main()