class Device:
    def __init__(self):
        self.device_id = 0
        self.device_metrics = {}
        self.link_metrics = {}

class Task:
    def __init__(self):
        self.task_id = 0
        self.frequency = 0
        self.devices = []
        self.alertflow_conditions = {}