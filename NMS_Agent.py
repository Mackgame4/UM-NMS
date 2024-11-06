from protocols import MAX_BUFFER_SIZE, NetTask as NT, AlertFlow as AF

class NMS_Agent:
    def __init__(self, host='127.0.0.1', port=8888):
        self.alert_flow = AF(host, port)
        #self.net_task = NT()
    
    def run_task(self, task):
        # Receive task via NetTask
        print(f"Running task: {task}")
        # Run task

def main():
    agent = NMS_Agent()
    agent.alert_flow.c_start()

if __name__ == "__main__":
    main()