# Detect the operating system
ifeq ($(OS), Windows_NT)
	OS_DETECTED := Windows
else
	OS_DETECTED := $(shell uname -s)
endif

MAIN = main.py

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
	@python3 $(MAIN) client
else ifeq ($(OS_DETECTED), Darwin)
	@echo "Detected OS: macOS"
	@python $(MAIN) client
else ifeq ($(OS_DETECTED), Windows)
	@echo "Detected OS: Windows"
	@python $(MAIN) client
else
	@echo "Unknown OS: $(OS_DETECTED)"
	@python3 $(MAIN) client
endif

server:
ifeq ($(OS_DETECTED), Linux)
	@echo "Detected OS: Linux"
	@python3 $(MAIN) server
else ifeq ($(OS_DETECTED), Darwin)
	@echo "Detected OS: macOS"
	@python $(MAIN) server
else ifeq ($(OS_DETECTED), Windows)
	@echo "Detected OS: Windows"
	@python $(MAIN) server
else
	@echo "Unknown OS: $(OS_DETECTED)"
	@python3 $(MAIN) server
endif

dev-client:
ifeq ($(OS_DETECTED), Linux)
	@echo "Detected OS: Linux"
	@python3 $(MAIN) dev-client
else ifeq ($(OS_DETECTED), Darwin)
	@echo "Detected OS: macOS"
	@python $(MAIN) dev-client
else ifeq ($(OS_DETECTED), Windows)
	@echo "Detected OS: Windows"
	@python $(MAIN) dev-client
else
	@echo "Unknown OS: $(OS_DETECTED)"
	@python3 $(MAIN) dev-client
endif

dev-server:
ifeq ($(OS_DETECTED), Linux)
	@echo "Detected OS: Linux"
	@python3 $(MAIN) dev-server
else ifeq ($(OS_DETECTED), Darwin)
	@echo "Detected OS: macOS"
	@python $(MAIN) dev-server
else ifeq ($(OS_DETECTED), Windows)
	@echo "Detected OS: Windows"
	@python $(MAIN) dev-server
else
	@echo "Unknown OS: $(OS_DETECTED)"
	@python3 $(MAIN) dev-server
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