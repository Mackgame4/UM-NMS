import socket
import threading
from encoder import decode_message, encode_message

# Export variables
MAX_BUFFER_SIZE = 1024

# TODO: NetTask class
# NetTask (utilizando UDP) para a comunicação de tarefas e a coleta contínua de métricas
class NetTask:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.socket_udp = None
        self.MaxConnected = 5
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
        print(f"NetTask Server started at {self.host}:{self.port}")
        while True:
            data, addr = self.socket_udp.recvfrom(MAX_BUFFER_SIZE)
            message = decode_message(data)
            print(f"Received from {addr}, {self.get_agent_id(addr)}: {message}")
            if message == "register_agent":
                self.agent_counter += 1
                self.connectedAgents.append((addr, self.agent_counter))
                self.socket_udp.sendto(encode_message(str(self.agent_counter)), addr)
            print(f"Connected agents: {self.connectedAgents}")

    # Client side protocol
    def c_start(self):
        self.socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"NetTask Client started at {self.host}:{self.port}")
        # Send requests to the server to register the agent and receive the assigned agent_id
        self.socket_udp.sendto(encode_message("register_agent"), (self.host, self.port))
        data, addr = self.socket_udp.recvfrom(MAX_BUFFER_SIZE)
        agent_id = decode_message(data)
        print(f"Agent ID: {agent_id}")
        while True:
            message = input("Enter message: ")
            self.socket_udp.sendto(encode_message(message), (self.host, self.port))

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