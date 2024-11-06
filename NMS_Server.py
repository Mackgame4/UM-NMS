from protocols import NetTask as NT, AlertFlow as AF
import json

class NMS_Server:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.alert_flow = AF(host, port)
        #self.net_task = NT(host, port)
        self.tasks = []

        # test zone
        self.read_tasks_from_file("configure-example.json")
        # end test zone

    # ler arquivo de tarefas (JSON)
    def read_tasks_from_file(self, filename):
        path = f"data/{filename}"
        with open(path, "r") as f:
            tasks = json.load(f)
            self.tasks = tasks["tasks"] # Get tasks from "tasks" key

    def send_task(self, task):
        print(f"Sending task: {task}")
        # Send via NetTask

def main():
    server = NMS_Server()
    server.alert_flow.s_start()

if __name__ == "__main__":
    main()