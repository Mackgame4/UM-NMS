import socket
from shared.encoder import decode_message, encode_message

class NMS_Server:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.socket_tcp = None
        self.socket_udp = None
        self.MaxConnected = 5
        self.connectedAgents = []
    
    def start(self):
        self.socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_tcp.bind((self.host, self.port))
        self.socket_tcp.listen(self.MaxConnected)
        print("Server started on", self.host, ":", self.port)
        self.accept_connections()

    def accept_connections(self):
        while True:
            conn, addr = self.socket_tcp.accept()
            print("Connected to", addr)
            self.connectedAgents.append(conn)
            self.handle_connection(conn)

    def handle_connection(self, conn):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = decode_message(data)
            print("Received:", message)
            response = "Received: " + message
            conn.send(encode_message(response))

    def close(self):
        self.socket_tcp.close()

def main():
    server = NMS_Server()
    server.start()