import socket
from shared.encoder import HOST, PORT, decode_message, encode_message

class NMS_Agent:
    def __init__(self):
        self.ip = ""

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
    
    def send_message(self, message):
        self.client.send(encode_message(message))
        return decode_message(self.client.recv(1024))
    
    def close(self):
        self.client.close()
    
    def get_ip(self):
        return self.ip

def main():
    agent = NMS_Agent()
    agent.connect()
    print(agent.send_message("Hello, server!"))
    agent.close()