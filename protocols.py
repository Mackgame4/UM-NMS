import socket

# Export variables
MAX_BUFFER_SIZE = 2048
AGENT_REGISTER_COMMAND = "register_agent"
AGENT_RECEIVED_COMMAND = "agent_received"
AGENT_READY_COMMAND = "agent_ready"
TASK_REQUEST_COMMAND = "request_task"
TASK_REQUEST_CONFIRM_COMMAND = "task_request_confirm"
TASK_RESULT_COMMAND = "task_result"

# NetTask (utilizando UDP) para a comunicação de tarefas e a coleta contínua de métricas
class NetTask:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket_udp = socket.socket()
        self.connected_agents = []
        self.agent_counter = 0

    def register_agent(self, c_addr):
        ip = c_addr[0]
        # if ip already exists, update the port only, else add a new agent (incrementing the agent_counter)
        for agent in self.connected_agents:
            if agent[0][0] == ip:
                agent[0] = c_addr
                return agent[1]
        self.agent_counter += 1
        self.connected_agents.append([c_addr, self.agent_counter])
        return self.agent_counter

    def get_agent_id(self, c_addr):
        for agent in self.connected_agents:
            if agent[0] == c_addr:
                return agent[1]
        return None
    
    def get_agent_addr(self, agent_id):
        for agent in self.connected_agents:
            if agent[1] == agent_id:
                return agent[0]
        return None
    
    def get_connected_agents(self):
        return self.connected_agents

# AlertFlow (utilizando TCP) para notificação de alterações críticas no estado dos dispositivos de rede.
class AlertFlow:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket_tcp = socket.socket()
        self.max_connections = 5 # TODO: Implementar controlo de conexões