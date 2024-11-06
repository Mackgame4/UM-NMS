from protocols import MAX_BUFFER_SIZE, AGENT_REGISTER_COMMAND, TASK_REQUEST_COMMAND, TASK_RESULT_COMMAND, NetTask as NT, AlertFlow as AF
from encoder import decode_message, encode_message
from colorama import Fore
import socket
import threading
import json

class NMS_Server:
    def __init__(self, host='127.0.0.1', port=8888):
        self.alert_flow = AF(host, port)
        self.net_task = NT(host, port)
        self.tasks_queue = []

    # Read tasks from a JSON file
    def read_tasks_from_file(self, filename):
        path = f"data/{filename}"
        with open(path, "r") as f:
            tasks = json.load(f)
            self.tasks_queue = tasks["tasks"]  # Get tasks from "tasks" key

    def start_alert_flow(self):
        self.alert_flow.s_start()

    def start_net_task(self):
        self.net_task.socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.net_task.socket_udp.bind((self.net_task.host, self.net_task.port))
        print(Fore.GREEN + f"NetTask Server started at {self.net_task.host}:{self.net_task.port}" + Fore.RESET)

        while True:
            data, addr = self.net_task.socket_udp.recvfrom(MAX_BUFFER_SIZE)
            message = decode_message(data)

            if message == AGENT_REGISTER_COMMAND:
                self.net_task.agent_counter += 1
                self.net_task.connectedAgents.append((addr, self.net_task.agent_counter))
                self.net_task.socket_udp.sendto(encode_message(str(self.net_task.agent_counter)), addr)
                print(Fore.YELLOW + f"Agent {self.net_task.agent_counter} connected at {addr}" + Fore.RESET)
                # After agent connected and registed, send a task request to the agent
                task_request = "ping www.google.com" # TODO: Implement task queue
                self.net_task.socket_udp.sendto(encode_message(TASK_REQUEST_COMMAND + f": {task_request}"), addr)

            else:
                agent_id = self.net_task.get_agent_id(addr)
                result = message[len(TASK_RESULT_COMMAND) + 1:].strip()
                print(Fore.YELLOW + f"Received task result from Agent {agent_id}: {result}" + Fore.RESET)

def main():
    server = NMS_Server()

    # Create threads for each protocol
    #alert_thread = threading.Thread(target=server.run_alert_flow)
    net_task_thread = threading.Thread(target=server.start_alert_flow)

    # Start both threads
    #alert_thread.start()
    net_task_thread.start()

    # Join threads if you want the main program to wait for them to finish
    #alert_thread.join()
    net_task_thread.join()

if __name__ == "__main__":
    main()