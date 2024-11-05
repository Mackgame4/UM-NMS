all: dev

dev: 
	@echo "Running in development mode..."
	@python main.py

client: dev-client
dev-client:
	@echo "Running in development mode with client..."
	@python NMS_Agent.py

server: dev-server
dev-server:
	@echo "Running in development mode with server..."
	@python NMS_Server.py