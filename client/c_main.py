import socket
from shared.encoder import HOST, PORT, decode_message, encode_message

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")

        while True:
            message = input("Enter message to send to server (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break

            client_socket.sendall(encode_message(message))
            data = client_socket.recv(1024)
            print(f"Received from server: {decode_message(data)}")

def main():
    start_client()

if __name__ == "__main__":
    main()