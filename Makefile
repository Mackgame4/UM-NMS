# Detect the operating system
ifeq ($(OS), Windows_NT)
	OS_DETECTED := Windows
else
	OS_DETECTED := $(shell uname -s)
endif

MAIN = main.py
IP = 127.0.0.1
PORT = 8888
CONFIG = data/configure.json

all: dev

dev:
ifeq ($(OS_DETECTED), Linux)
	@echo "Detected OS: Linux"
	@python3 $(MAIN)
else ifeq ($(OS_DETECTED), Darwin)
	@echo "Detected OS: macOS"
	@python $(MAIN)
else ifeq ($(OS_DETECTED), Windows)
	@echo "Detected OS: Windows"
	@python $(MAIN)
else
	@echo "Unknown OS: $(OS_DETECTED)"
	@python3 $(MAIN)
endif

client:
ifeq ($(OS_DETECTED), Linux)
	@echo "Detected OS: Linux"
	@python3 $(MAIN) client $(IP) $(PORT) $(CONFIG)
else ifeq ($(OS_DETECTED), Darwin)
	@echo "Detected OS: macOS"
	@python $(MAIN) client $(IP) $(PORT) $(CONFIG)
else ifeq ($(OS_DETECTED), Windows)
	@echo "Detected OS: Windows"
	@python $(MAIN) client $(IP) $(PORT) $(CONFIG)
else
	@echo "Unknown OS: $(OS_DETECTED)"
	@python3 $(MAIN) client $(IP) $(PORT) $(CONFIG)
endif

server:
ifeq ($(OS_DETECTED), Linux)
	@echo "Detected OS: Linux"
	@python3 $(MAIN) server $(IP) $(PORT) $(CONFIG)
else ifeq ($(OS_DETECTED), Darwin)
	@echo "Detected OS: macOS"
	@python $(MAIN) server $(IP) $(PORT) $(CONFIG)
else ifeq ($(OS_DETECTED), Windows)
	@echo "Detected OS: Windows"
	@python $(MAIN) server $(IP) $(PORT) $(CONFIG)
else
	@echo "Unknown OS: $(OS_DETECTED)"
	@python3 $(MAIN) server $(IP) $(PORT) $(CONFIG)
endif

dev-client:
ifeq ($(OS_DETECTED), Linux)
	@echo "Detected OS: Linux"
	@python3 $(MAIN) dev-client $(IP) $(PORT) $(CONFIG)
else ifeq ($(OS_DETECTED), Darwin)
	@echo "Detected OS: macOS"
	@python $(MAIN) dev-client $(IP) $(PORT) $(CONFIG)
else ifeq ($(OS_DETECTED), Windows)
	@echo "Detected OS: Windows"
	@python $(MAIN) dev-client $(IP) $(PORT) $(CONFIG)
else
	@echo "Unknown OS: $(OS_DETECTED)"
	@python3 $(MAIN) dev-client $(IP) $(PORT) $(CONFIG)
endif

dev-server:
ifeq ($(OS_DETECTED), Linux)
	@echo "Detected OS: Linux"
	@python3 $(MAIN) dev-server $(IP) $(PORT) $(CONFIG)
else ifeq ($(OS_DETECTED), Darwin)
	@echo "Detected OS: macOS"
	@python $(MAIN) dev-server $(IP) $(PORT) $(CONFIG)
else ifeq ($(OS_DETECTED), Windows)
	@echo "Detected OS: Windows"
	@python $(MAIN) dev-server $(IP) $(PORT) $(CONFIG)
else
	@echo "Unknown OS: $(OS_DETECTED)"
	@python3 $(MAIN) dev-server $(IP) $(PORT) $(CONFIG)
endif

relatorio: relatorio_build

relatorio_build:
	@echo "Compilando relatorio..."
	@typst compile relatorio/relatorio.typ

relatorio_watch:
	@echo "Assistindo alteracoes no relatorio..."
	@typst watch relatorio/relatorio.typ

relatorio_clean:
	@rm -rf relatorio/relatorio.pdf