import json

class Message:
    def __init__(self, command, data):
        self.command = command
        self.data = data

    def __str__(self):
        return f"Command: {self.command}, Data: {self.data}"

    def __repr__(self):
        return f"Message({self.command}, {self.data})"

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_string):
        return Message(**json.loads(json_string))

    def encode(command, data):
        return Message(command, data).to_json().encode('utf-8')

    @staticmethod
    def decode(data):
        return Message.from_json(data.decode('utf-8'))

def encode_message(command="", data=None):
    return Message.encode(command, data)

def decode_message(data=None):
    return Message.decode(data)