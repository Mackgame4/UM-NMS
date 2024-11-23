from notify import notify
import json

class TaskManager:
    def __init__(self):
        self.tasks = [] # self.tasks = [Task()]

    def read_config_file(self, path): # Read tasks from a JSON file
        try:
            with open(path, "r") as f:
                data = json.load(f)
                tasks = data["tasks"]
                for task in tasks:
                    self.tasks.append(task)
        except FileNotFoundError:
            notify("error", f"File not found: {path}")
            return []