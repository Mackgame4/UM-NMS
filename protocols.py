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

# AlertFlow (utilizando TCP) para notificação de alterações críticas no estado dos dispositivos de rede.
class AlertFlow:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.socket_tcp = None
        self.MaxConnected = 5
        self.connectedAgents = []
        self.agent_id = 0

    # Server side protocol
    def s_start(self):
        self.socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_tcp.bind((self.host, self.port))
        self.socket_tcp.listen(self.MaxConnected)
        print("Server started on", self.host, ":", self.port)
        self.s_accept_connections()

    def s_accept_connections(self):
        while True:
            conn, addr = self.socket_tcp.accept()
            self.agent_id += 1
            client_id = self.agent_id
            print(f"Client {client_id} connected from {addr}")
            self.connectedAgents.append((conn, client_id))
            conn.send(encode_message(f"Welcome, your client ID is {client_id}"))
            threading.Thread(target=self.s_handle_connection, args=(conn, client_id)).start()

    def s_handle_connection(self, conn, client_id):
        try:
            while True:
                data = conn.recv(MAX_BUFFER_SIZE)
                if not data:
                    print(f"Client {client_id} disconnected")
                    break
                message = decode_message(data)
                print(f"Received from Client {client_id}: {message}")
                response = f"Received by Server: {message}"
                conn.send(encode_message(response))
        except ConnectionResetError:
            print(f"Client {client_id} forcibly disconnected")
        finally:
            conn.close()
            self.connectedAgents = [(c, id) for c, id in self.connectedAgents if id != client_id]
            print(f"Client {client_id} disconnected")

    def s_close(self):
        self.socket_tcp.close()

    # Client side protocol
    def c_start(self):
        self.socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_tcp.connect((self.host, self.port))
        print("Connected to", self.host, ":", self.port)
        self.c_handle_connection()

    def c_handle_connection(self):
        try:
            while True:
                message = input("Enter message: ")
                self.socket_tcp.send(encode_message(message))
                data = self.socket_tcp.recv(MAX_BUFFER_SIZE)
                response = decode_message(data)
                print(response)
        except ConnectionResetError:
            print("Server forcibly disconnected")
        finally:
            self.socket_tcp.close()

    def c_close(self):
        self.socket_tcp.close()