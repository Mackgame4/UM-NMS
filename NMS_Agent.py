from protocols import MAX_BUFFER_SIZE, NetTask as NT, AlertFlow as AF

class NMS_Agent:
    def __init__(self, shost='127.0.0.1', sport=8888):
        self.shost = shost # Server host to connect to
        self.sport = sport # Server port to connect to
        self.alert_flow = AF(shost, sport)
        #self.net_task = NT()

def main():
    agent = NMS_Agent()
    agent.alert_flow.c_start()

if __name__ == "__main__":
    main()