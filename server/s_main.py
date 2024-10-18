import socket
from ..shared.encoder import HOST, PORT, decode_message, encode_message

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()  # Listen for incoming connections
        print(f"Server is listening on {HOST}:{PORT}...")
        
        while True:
            conn, addr = server_socket.accept()  # Accept a connection
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    message = decode_message(data)
                    print(f"Received from client: {message}")
                    response = f"Server received: {message}"
                    conn.sendall(encode_message(response))  # Send response

def main():
    start_server()

if __name__ == "__main__":
    main()