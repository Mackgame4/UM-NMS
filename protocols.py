import socket

# Export variables
MAX_BUFFER_SIZE = 2048
AGENT_REGISTER_COMMAND = "register_agent"
AGENT_READY_COMMAND = "agent_ready"
TASK_REQUEST_COMMAND = "request_task"
TASK_RESULT_COMMAND = "task_result"

# NetTask (utilizando UDP) para a comunicação de tarefas e a coleta contínua de métricas
class NetTask:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket_udp = socket.socket()
        self.connectedAgents = []
        self.agent_counter = 0 # Only for used for Agent ID assignment in the server-side

    def register_agent(self, addr):
        self.agent_counter += 1
        self.connectedAgents.append((addr, self.agent_counter))
        return self.agent_counter

    def get_agent_id(self, addr):
        for agent in self.connectedAgents:
            if agent[0] == addr:
                return agent[1]
        return None
    
    def get_agent_addr(self, agent_id):
        for agent in self.connectedAgents:
            if agent[1] == agent_id:
                return agent[0]
        return None
    
    def get_connected_agents(self):
        return self.connectedAgents

# AlertFlow (utilizando TCP) para notificação de alterações críticas no estado dos dispositivos de rede.
class AlertFlow:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.socket_tcp = socket.socket()