from protocols import MAX_BUFFER_SIZE, AGENT_REGISTER_COMMAND, AGENT_RECEIVED_COMMAND, TASK_REQUEST_COMMAND, TASK_RESULT_COMMAND, AGENT_READY_COMMAND, NetTask as NT, AlertFlow as AF
from encoder import decode_message, encode_message
from notify import notify
from task import TaskManager
import socket
import threading
import sys

class NMS_Server:
    def __init__(self, host='127.0.0.1', port=8888, config_file="data/configure.json"):
        self.alert_flow = AF(host, port)
        self.net_task = NT(host, port)
        self.config_file = config_file
        self.task_manager = TaskManager()

    ### Class methods (Server-side) ###

    ### AlertFlow methods (Server-side) ###
    def start_alert_flow(self):
        alert_flow = self.alert_flow
        alert_flow.socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        alert_flow.socket_tcp.bind((alert_flow.host, alert_flow.port))
        alert_flow.socket_tcp.listen(alert_flow.max_connections)
        notify("info", f"AlertFlow Server started at {alert_flow.host}:{alert_flow.port}")

    ### NetTask methods (Server-side) ###
    def start_net_task(self):
        # Start the NetTask server-side socket
        net_task = self.net_task
        task_manager = self.task_manager
        net_task.socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        net_task.socket_udp.bind((net_task.host, net_task.port))
        notify("info", f"NetTask Server started at {net_task.host}:{net_task.port}")

        task_manager.read_config_file(self.config_file)
        #notify("debug", f"Tasks: {task_manager.tasks}")

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
                #notify("debug", f"Agents: {net_task.get_connected_agents()}")

            # Server received agent ready to task: Check if there are tasks for it and send the task
            elif message.command == AGENT_READY_COMMAND:
                notify("warning", f"Agent {agent_id} is ready to receive tasks")
                # Check if there are tasks for the agent and send them to be ran
                for task in task_manager.tasks:
                    for device in task['devices']:
                        if c_addr[0] == device['device_addr']:
                            net_task.socket_udp.sendto(encode_message(TASK_REQUEST_COMMAND, {"task_id": task['task_id'], "frequency": task['frequency'], "device": device}), c_addr)
                            notify("info", f"Sent task {task['task_id']} to Agent {agent_id}")

            elif message.command == TASK_RESULT_COMMAND:
                result = message.data
                notify("debug", f"Task result from Agent {agent_id}: {result}")

### Runnable Section ###
def main(args):
    server = NMS_Server()
    if len(args) >= 3:
        host = args[0]
        port = int(args[1])
        config_file = args[2]
        server = NMS_Server(host, port, config_file)
    alert_thread = threading.Thread(target=server.start_alert_flow)
    net_task_thread = threading.Thread(target=server.start_net_task)
    alert_thread.start()
    net_task_thread.start()
    alert_thread.join()
    net_task_thread.join()

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)