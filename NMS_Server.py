from protocols import MAX_BUFFER_SIZE, AGENT_REGISTER_COMMAND, TASK_REQUEST_COMMAND, TASK_RESULT_COMMAND, AGENT_READY_COMMAND, NetTask as NT, AlertFlow as AF
from encoder import decode_message, encode_message
from colorama import Fore
from task import TaskManager
import socket
import threading
import sys

TASKS_FILENAME = "configure.json"

class NMS_Server:
    def __init__(self, host='127.0.0.1', port=8888):
        self.alert_flow = AF(host, port)
        self.net_task = NT(host, port)
        self.task_manager = TaskManager()
        self.ready_agents = [] # When a task (started and agent not ready, its ocuppied) ends the agent returns the result and send a ready message again and its added to this list again

    # Class methods (Server-side)
    def agent_ready(self, agent_id):
        self.ready_agents.append(agent_id)

    # AlertFlow methods (Server-side)
    # TODO: Implement the AlertFlow server-side protocol
    def start_alert_flow(self):
        alert_flow = self.alert_flow
        alert_flow.socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        alert_flow.socket_tcp.bind((alert_flow.host, alert_flow.port))
        alert_flow.socket_tcp.listen(5)
        print(Fore.GREEN + f"AlertFlow Server started at {alert_flow.host}:{alert_flow.port}" + Fore.RESET)

    # NetTask methods (Server-side)
    def start_net_task(self):
        net_task = self.net_task
        net_task.socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        net_task.socket_udp.bind((net_task.host, net_task.port))
        print(Fore.GREEN + f"NetTask Server started at {net_task.host}:{net_task.port}" + Fore.RESET)

        self.task_manager.parse_tasks(self.task_manager.read_tasks_from_file(TASKS_FILENAME))

        while True:
            data, addr = net_task.socket_udp.recvfrom(MAX_BUFFER_SIZE)
            message = decode_message(data)

            if message == AGENT_REGISTER_COMMAND:
                net_task.register_agent(addr)
                # TODO: check if the agent is already connected, if so, update the agent's address so it can reconnect if it goes offline and comes back online
                # This will only work in a emulated environment, in local host all agents will have the same address but different ports
                net_task.socket_udp.sendto(encode_message(str(net_task.agent_counter)), addr)
                print(Fore.YELLOW + f"Agent {net_task.agent_counter} connected at {addr}" + Fore.RESET)

            elif message == AGENT_READY_COMMAND:
                agent_id = net_task.get_agent_id(addr)
                self.agent_ready(agent_id)
                print(Fore.YELLOW + f"Agent {agent_id} is ready to receive tasks" + Fore.RESET)

            elif message.startswith(TASK_RESULT_COMMAND):
                agent_id = net_task.get_agent_id(addr)
                result = message[len(TASK_RESULT_COMMAND) + 1:].strip()
                print(Fore.YELLOW + f"Received task result from Agent {agent_id}: {result}" + Fore.RESET)

def main(args):
    server = NMS_Server()
    if len(args) >= 2:
        host = args[0]
        port = int(args[1])
        server = NMS_Server(host, port)
    # Create threads for each protocol
    alert_thread = threading.Thread(target=server.start_alert_flow)
    net_task_thread = threading.Thread(target=server.start_net_task)
    # Start both threads
    alert_thread.start()
    net_task_thread.start()
    # Join threads if you want the main program to wait for them to finish
    alert_thread.join()
    net_task_thread.join()

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)