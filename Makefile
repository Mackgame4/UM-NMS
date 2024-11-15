all: dev

dev: 
	@echo "Running in development mode..."
	@python main.py

dev-client:
	@echo "Running in development mode with client..."
	@python NMS_Agent.py

dev-server:
	@echo "Running in development mode with server..."
	@python NMS_Server.py

# Windows commands
win-client:
	@echo "Running in client mode..."
	@cmd /c start python NMS_Agent.py

win-server:
	@echo "Running in server mode..."
	@cmd /c start python NMS_Server.py

# Linux commands
linux-client:
	@echo "Running in development mode with client..."
	@python3 NMS_Agent.py

linux-server:
	@echo "Running in development mode with server..."
	@python3 NMS_Server.py

relatorio: relatorio_build

relatorio_build:
	@echo "Compilando relatorio..."
	@typst compile relatorio/relatorio.typ

relatorio_watch:
	@echo "Assistindo alteracoes no relatorio..."
	@typst watch relatorio/relatorio.typ

relatorio_clean:
	@rm -rf relatorio/relatorio.pdf