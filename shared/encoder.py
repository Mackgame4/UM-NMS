HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def encode_message(message):
    """Encode a message to send over the network."""
    return message.encode('utf-8')

def decode_message(message):
    """Decode a message received from the network."""
    return message.decode('utf-8')
