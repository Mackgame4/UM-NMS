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

relatorio: relatorio_build

relatorio_build:
	@echo "Compilando relatorio..."
	@typst compile relatorio/relatorio.typ

relatorio_watch:
	@echo "Assistindo alteracoes no relatorio..."
	@typst watch relatorio/relatorio.typ

relatorio_clean:
	@rm -rf relatorio/relatorio.pdf