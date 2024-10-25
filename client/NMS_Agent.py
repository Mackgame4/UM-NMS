### 
# Some python package imports path
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
###
import socket
from shared.encoder import MAX_BUFFER_SIZE, decode_message, encode_message

class NMS_Agent:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.socket_tcp = None

    def start(self):
        self.socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_tcp.connect((self.host, self.port))
        print("Connected to", self.host, ":", self.port)
        
        # Receive the welcome message with client ID
        data = self.socket_tcp.recv(MAX_BUFFER_SIZE)
        if data:
            welcome_message = decode_message(data)
            print(welcome_message)

        self.handle_connection()

    def handle_connection(self):
        while True:
            message = input("Message: ")
            if message.lower() == "exit":
                break
            self.socket_tcp.send(encode_message(message))
            data = self.socket_tcp.recv(MAX_BUFFER_SIZE)
            if not data:
                break
            response = decode_message(data)
            print("Server responded:", response)
            
    def close(self):
        self.socket_tcp.close()

def main():
    agent = NMS_Agent()
    agent.start()