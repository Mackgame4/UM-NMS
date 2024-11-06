import socket
import threading
from encoder import decode_message, encode_message

# Export variables
MAX_BUFFER_SIZE = 2048
AGENT_REGISTER_COMMAND = "register_agent"
TASK_REQUEST_COMMAND = "request_task"
TASK_RESULT_COMMAND = "task_result"

# NetTask (utilizando UDP) para a comunicação de tarefas e a coleta contínua de métricas
class NetTask:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket_udp = socket.socket()
        self.connectedAgents = []
        self.agent_counter = 0

    def get_agent_id(self, addr):
        for agent in self.connectedAgents:
            if agent[0] == addr:
                return agent[1]
        return None

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