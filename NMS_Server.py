from protocols import MAX_BUFFER_SIZE, NetTask as NT, AlertFlow as AF

class NMS_Server:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.alert_flow = AF(host, port)
        #self.net_task = NT(host, port)

def main():
    server = NMS_Server()
    server.alert_flow.s_start()

if __name__ == "__main__":
    main()