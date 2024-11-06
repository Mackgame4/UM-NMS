import socket
import threading
from encoder import MAX_BUFFER_SIZE, decode_message, encode_message

class NMS_Server:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.socket_tcp = None
        self.MaxConnected = 5
        self.connectedAgents = []
        self.agent_id = 0  # Initialize ID counter

    def start(self):
        self.socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_tcp.bind((self.host, self.port))
        self.socket_tcp.listen(self.MaxConnected)
        print("Server started on", self.host, ":", self.port)
        self.accept_connections()

    def accept_connections(self):
        while True:
            conn, addr = self.socket_tcp.accept()
            self.agent_id += 1  # Increment the ID for each new client
            client_id = self.agent_id
            print(f"Client {client_id} connected from {addr}")
            self.connectedAgents.append((conn, client_id)) # Store the connection and ID as a tuple
            
            # Start a new thread for each client
            threading.Thread(target=self.handle_connection, args=(conn, client_id)).start()

    def handle_connection(self, conn, client_id):
        try:
            conn.send(encode_message(f"Welcome, your client ID is {client_id}"))
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
            # Ensure the connection is closed and notify of disconnection
            conn.close()
            self.connectedAgents = [(c, id) for c, id in self.connectedAgents if id != client_id]
            print(f"Client {client_id} disconnected")

    def close(self):
        self.socket_tcp.close()

def main():
    server = NMS_Server()
    server.start()

if __name__ == "__main__":
    main()