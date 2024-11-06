import socket
import threading
from encoder import decode_message, encode_message
from colorama import Fore

# Export variables
MAX_BUFFER_SIZE = 1024
AGENT_REGISTER_COMMAND = "register_agent"
TASK_REQUEST_COMMAND = "request_task"
TASK_RESULT_COMMAND = "task_result"

# TODO: NetTask class
# NetTask (utilizando UDP) para a comunicação de tarefas e a coleta contínua de métricas
class NetTask:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.socket_udp = None
        self.connectedAgents = []
        self.agent_counter = 0

    def get_agent_id(self, addr):
        for agent in self.connectedAgents:
            if agent[0] == addr:
                return agent[1]
        return None

    # Server side protocol
    def s_start(self):
        self.socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_udp.bind((self.host, self.port))
        print(Fore.GREEN + f"NetTask Server started at {self.host}:{self.port}" + Fore.RESET)

        while True:
            data, addr = self.socket_udp.recvfrom(MAX_BUFFER_SIZE)
            message = decode_message(data)

            if message == AGENT_REGISTER_COMMAND:
                self.agent_counter += 1
                self.connectedAgents.append((addr, self.agent_counter))
                self.socket_udp.sendto(encode_message(str(self.agent_counter)), addr)
                print(Fore.YELLOW + f"Agent {self.agent_counter} connected at {addr}" + Fore.RESET)
                # After agent connected and registed, send a task request to the agent
                task_request = "ping www.google.com" # TODO: Implement task queue
                self.socket_udp.sendto(encode_message(TASK_REQUEST_COMMAND + f": {task_request}"), addr)

            else:
                agent_id = self.get_agent_id(addr)
                result = message[len(TASK_RESULT_COMMAND) + 1:].strip()
                print(Fore.YELLOW + f"Received task result from Agent {agent_id}: {result}" + Fore.RESET)

    # Client side protocol
    def c_start(self):
        self.socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(Fore.GREEN + f"NetTask Client connected at {self.host}:{self.port}" + Fore.RESET)

        # Send requests to the server to register the agent and receive the assigned agent_id
        self.socket_udp.sendto(encode_message(AGENT_REGISTER_COMMAND), (self.host, self.port))
        data, _ = self.socket_udp.recvfrom(MAX_BUFFER_SIZE)
        agent_id = decode_message(data)
        print(Fore.YELLOW + f"Assigned Agent ID: {agent_id}" + Fore.RESET)

        while True:
            # Wait for task requests from the server
            data, _ = self.socket_udp.recvfrom(MAX_BUFFER_SIZE)
            message = decode_message(data)

            if message.startswith(TASK_REQUEST_COMMAND):
                task = message[len(TASK_REQUEST_COMMAND) + 1:].strip()
                print(Fore.YELLOW + f"Received task request from server: {task}" + Fore.RESET)
                
                # wait for result and send it back to the server
                result = self.run_task(task)
                self.socket_udp.sendto(encode_message(TASK_RESULT_COMMAND + f": {result}"), (self.host, self.port))

    def run_task(self, task):
        # Execute the task
        import subprocess
        result = subprocess.run(task.split(), capture_output=True)
        #print(Fore.CYAN + f"Task result: {result.stdout.decode()}" + Fore.RESET)
        return result.stdout.decode()

# AlertFlow (utilizando TCP) para notificação de alterações críticas no estado dos dispositivos de rede.
class AlertFlow:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.socket_tcp = None

    # Server side protocol
    def s_start(self):
        self.socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_tcp.bind((self.host, self.port))
        self.socket_tcp.listen(5)
        print(f"AlertFlow Server started at {self.host}:{self.port}")
        while True:
            conn, addr = self.socket_tcp.accept()
            print(f"Connected by {addr}")
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

    def handle_client(self, conn, addr):
        while True:
            data = conn.recv(MAX_BUFFER_SIZE)
            if not data:
                break
            message = decode_message(data)
            print(f"Received from {addr}: {message}")
            conn.send(encode_message(f"Echo: {message}"))
        conn.close()

    # Client side protocol
    def c_start(self):
        self.socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"AlertFlow Client started at {self.host}:{self.port}")
        self.socket_tcp.connect((self.host, self.port))
        while True:
            message = input("Enter message: ")
            self.socket_tcp.send(encode_message(message))
            data = self.socket_tcp.recv(MAX_BUFFER_SIZE)
            print(f"Received: {data}")