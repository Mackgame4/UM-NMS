from protocols import NetTask as NT, AlertFlow as AF
import json
import threading

class NMS_Server:
    def __init__(self, host='127.0.0.1', port=8888):
        self.alert_flow = AF(host, port)
        self.net_task = NT(host, port)
        self.tasks_queue = []

    # Read tasks from a JSON file
    def read_tasks_from_file(self, filename):
        path = f"data/{filename}"
        with open(path, "r") as f:
            tasks = json.load(f)
            self.tasks_queue = tasks["tasks"]  # Get tasks from "tasks" key

    def run_alert_flow(self):
        self.alert_flow.s_start()

    def run_net_task(self):
        self.net_task.s_start()

def main():
    server = NMS_Server()

    # Create threads for each protocol
    #alert_thread = threading.Thread(target=server.run_alert_flow)
    net_task_thread = threading.Thread(target=server.run_net_task)

    # Start both threads
    #alert_thread.start()
    net_task_thread.start()

    # Join threads if you want the main program to wait for them to finish
    #alert_thread.join()
    net_task_thread.join()

if __name__ == "__main__":
    main()