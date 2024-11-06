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
        self.agent_id = 0
        self.agent_tasks = {}

    # Server side protocol
    def s_start(self):
        self.socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_udp.bind((self.host, self.port))
        print(f"NetTask Server started at {self.host}:{self.port}")
        while True:
            data, addr = self.socket_udp.recvfrom(MAX_BUFFER_SIZE)
            message = decode_message(data)
            print(f"Received from {addr}: {message}")

    # Client side protocol
    def c_start(self):
        self.socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"NetTask Client started at {self.host}:{self.port}")
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