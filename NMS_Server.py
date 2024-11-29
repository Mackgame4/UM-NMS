from protocols import MAX_BUFFER_SIZE, AGENT_REGISTER_COMMAND, AGENT_RECEIVED_COMMAND, TASK_REQUEST_COMMAND, TASK_REQUEST_CONFIRM_COMMAND, TASK_RESULT_COMMAND, AGENT_READY_COMMAND, NetTask as NT, AlertFlow as AF
from encoder import decode_message, encode_message
from notify import notify, notify_af
from task import TaskManager
import socket
import threading
import sys
import json

class NMS_Server:
    def __init__(self, host='127.0.0.1', port=8888, config_file="data/configure.json"):
        self.alert_flow = AF(host, port)
        self.net_task = NT(host, port)
        self.config_file = config_file
        self.task_manager = TaskManager()

    ### AlertFlow methods (Server-side) ###
    def start_alert_flow(self):
        alert_flow = self.alert_flow
        alert_flow.socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        alert_flow.socket_tcp.bind((alert_flow.host, alert_flow.port))
        alert_flow.socket_tcp.listen(alert_flow.max_connections)
        notify("info", f"AlertFlow Server started at {alert_flow.host}:{alert_flow.port}")

        while True:
            conn, addr = alert_flow.socket_tcp.accept()
            with conn:
                notify("info", f"AlertFlow Client connected at {addr}")
                buffer = ""
                while True:
                    data = conn.recv(MAX_BUFFER_SIZE)
                    if not data:
                        break
                    buffer += data.decode('utf-8')  # Accumulate incoming data
                    while '\n' in buffer:  # Process each complete message
                        raw_message, buffer = buffer.split('\n', 1)
                        try:
                            message = decode_message(raw_message.encode('utf-8'))
                            metric_name = message.command
                            metric_data = message.data
                            notify_af("warning", f"{metric_name} condition got exceeded: {metric_data}")
                        except json.JSONDecodeError as e:
                            notify("error", f"Failed to decode message: {e}")

    ### NetTask methods (Server-side) ###
    def start_net_task(self):
        # Start the NetTask server-side socket
        net_task = self.net_task
        task_manager = self.task_manager
        net_task.socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        net_task.socket_udp.bind((net_task.host, net_task.port))
        notify("info", f"NetTask Server started at {net_task.host}:{net_task.port}")

        task_manager.read_config_file(self.config_file)
        notify("debug", f"Loaded Tasks: {task_manager.tasks}")

        while True:
            data, c_addr = net_task.socket_udp.recvfrom(MAX_BUFFER_SIZE)
            message = decode_message(data)
            agent_id = net_task.get_agent_id(c_addr)
            
            # Server received agent register: Register agent and send agent_id
            if message.command == AGENT_REGISTER_COMMAND:
                if agent_id is None:
                    agent_id = net_task.register_agent(c_addr)
                net_task.socket_udp.sendto(encode_message(AGENT_RECEIVED_COMMAND, agent_id), c_addr)
                notify("success", f"Agent {agent_id} assigned at {c_addr}")
                notify("debug", f"Connected Agents: {net_task.get_connected_agents()}")

            # Server received agent ready to task: Check if there are tasks for it and send the task
            elif message.command == AGENT_READY_COMMAND:
                notify("warning", f"Agent {agent_id} is ready to receive tasks")
                # Check if there are tasks for the agent and send them to be ran
                for task in task_manager.tasks:
                    task_assigned = False  # Add a flag to track if a task has been assigned
                    for device in task['devices']:
                        if c_addr[0] == device['device_addr']:
                            net_task.socket_udp.sendto(encode_message(TASK_REQUEST_COMMAND, {"task_id": task['task_id'], "frequency": task['frequency'], "device": device}), c_addr)
                            notify("info", f"Sent task {task['task_id']} to Agent {agent_id}")
                            task_assigned = True  # Set the flag to True
                            break  # Break the inner loop
                    if task_assigned:  # If a task has been assigned, exit the outer loop
                        break # this brak is to avoid sendind two tasks to the same agent at the same time in (theres no colision avoidance control, im sorry ;-;)

            # Comment this part of code if we want to run the task more times than the frequency defined in the task
            elif message.command == TASK_REQUEST_CONFIRM_COMMAND:
                notify("info", f"Agent {agent_id} confirmed task request")
                # Remove the task from the list of tasks
                task_manager.remove_task(message.data)
                notify("debug", f"Remaining Tasks: {task_manager.tasks}")

            elif message.command == TASK_RESULT_COMMAND:
                result = message.data
                notify("success", f"Task result from Agent {agent_id}: {result}")

### Runnable Section ###
def main(args):
    server = NMS_Server()
    if len(args) >= 3:
        host = args[0]
        port = int(args[1])
        config_file = args[2]
        server = NMS_Server(host, port, config_file)
    elif len(args) >= 2:
        host = args[0]
        port = int(args[1])
        server = NMS_Server(host, port)
    elif len(args) >= 1:
        host = args[0]
        server = NMS_Server(host)
    alert_thread = threading.Thread(target=server.start_alert_flow)
    net_task_thread = threading.Thread(target=server.start_net_task)
    alert_thread.start()
    net_task_thread.start()
    alert_thread.join()
    net_task_thread.join()

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)