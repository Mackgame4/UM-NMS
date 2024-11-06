from protocols import MAX_BUFFER_SIZE, NetTask as NT, AlertFlow as AF
import threading

class NMS_Agent:
    def __init__(self, host='127.0.0.1', port=8888):
        self.alert_flow = AF(host, port)
        self.net_task = NT(host, port)

    def run_alert_flow(self):
        self.alert_flow.c_start()

    def run_net_task(self):
        self.net_task.c_start()

def main():
    agent = NMS_Agent()

    # Create threads for each protocol
    alert_thread = threading.Thread(target=agent.run_alert_flow)
    net_task_thread = threading.Thread(target=agent.run_net_task)

    # Start both threads
    alert_thread.start()
    net_task_thread.start()

    # Optionally, join threads if you want the main program to wait for them to finish
    alert_thread.join()
    net_task_thread.join()

if __name__ == "__main__":
    main()