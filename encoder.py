MAX_BUFFER_SIZE = 1024

def encode_message(message):
    """Encode a message to send over the network."""
    return message.encode('utf-8')

def decode_message(message):
    """Decode a message received from the network."""
    return message.decode('utf-8')
