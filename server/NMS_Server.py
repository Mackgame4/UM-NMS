import socket
from shared.encoder import HOST, PORT, decode_message, encode_message

class NMS_Server:
    def __init__(self):
        self.ip = ""
    
    def connect(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen(5)
        self.client, self.addr = self.server.accept()

    def receive_message(self):
        return decode_message(self.client.recv(1024))
    
    def send_message(self, message):
        self.client.send(encode_message(message))

    def close(self):
        self.client.close()
        self.server.close()

    def get_ip(self):
        return self.ip

def main():
    server = NMS_Server()
    server.connect()
    print(server.receive_message())
    server.send_message("Hello, client!")
    server.close()