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
        
    def get_tasks(self):
        return self.tasks
    
    def get_task(self, task_id):
        for task in self.tasks:
            if task['task_id'] == task_id:
                return task
        return None
    
    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task_id):
        for task in self.tasks:
            if task['task_id'] == task_id:
                self.tasks.remove(task)
                return True
        return False
    
    def update_task(self, task_id, task):
        for i, t in enumerate(self.tasks):
            if t['task_id'] == task_id:
                self.tasks[i] = task
                return True
        return False
    
    def get_task_devices(self, task_id):
        task = self.get_task(task_id)
        if task is not None:
            return task['devices']
        return None
    
    def add_task_device(self, task_id, device):
        task = self.get_task(task_id)
        if task is not None:
            task['devices'].append(device)
            return True
        return False
    
    def remove_task_device(self, task_id, device_addr):
        task = self.get_task(task_id)
        if task is not None:
            for device in task['devices']:
                if device['device_addr'] == device_addr:
                    task['devices'].remove(device)
                    return True
        return False