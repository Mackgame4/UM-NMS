from colorama import Fore
import json

class Device:
    def __init__(self):
        self.device_id = 0
        self.device_addr = ""
        self.device_port = 0
        self.device_metrics = {}
        self.link_metrics = {}
        self.alertflow_conditions = {}

class Task:
    def __init__(self):
        self.task_id = 0
        self.frequency = 0
        self.devices = [] # self.devices = [Device()]

class TaskManager:
    def __init__(self):
        self.tasks = [] # self.tasks = [Task()]

    def read_tasks_from_file(self, filename): # Read tasks from a JSON file
        path = f"data/{filename}"
        try:
            with open(path, "r") as f:
                tasks = json.load(f)
                return tasks["tasks"]
        except FileNotFoundError:
            print(Fore.RED + f"Configuration file {filename} not found" + Fore.RESET)
            return []

    def parse_tasks(self, tasks):
        new_task = Task()
        for task in tasks:
            new_task.task_id = task["task_id"]
            new_task.frequency = task["frequency"]
            new_task.devices = []
            task_devices = task["devices"]
            for device in task_devices:
                new_device = Device()
                new_device.device_id = device["device_id"]
                new_device.device_addr = device["device_addr"]
                new_device.device_metrics = device["device_metrics"]
                new_device.link_metrics = device["link_metrics"]
                new_device.alertflow_conditions = device["alertflow_conditions"]
                new_task.devices.append(new_device)
            self.tasks.append(new_task)