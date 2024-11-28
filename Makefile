QDRANT_VERSION := 1.12.4
QDRANT_URL := https://github.com/qdrant/qdrant/releases/download/v$(QDRANT_VERSION)/qdrant_$(QDRANT_VERSION)-1_amd64.deb

STORAGE_DIR := $(PWD)/qdrant_storage
DOWNLOADS_DIR := $(PWD)/downloads

.PHONY: all clean setup-dirs download-ollama download-qdrant run-qdrant stop-ollama stop-qdrant stop

all: setup-dirs download-ollama download-qdrant

setup-dirs:
	mkdir -p $(STORAGE_DIR) $(DOWNLOADS_DIR)

download-ollama:
	if ! command -v ollama >/dev/null 2>&1; then \
		echo "Downloading and installing Ollama..."; \
		curl -fsSL https://ollama.com/install.sh | sh; \
	else \
		echo "Ollama is already installed in the system"; \
	fi

download-qdrant:
	if ! command -v qdrant >/dev/null 2>&1; then \
		echo "Downloading and installing Qdrant..."; \
		curl -L -o "$(DOWNLOADS_DIR)/qdrant.deb" "$(QDRANT_URL)"; \
		sudo dpkg -i "$(DOWNLOADS_DIR)/qdrant.deb"; \
		rm "$(DOWNLOADS_DIR)/qdrant.deb"; \
	else \
		echo "Qdrant is already installed in the system"; \
	fi

run-ollama-screen:
	screen -dmS ollama bash -c 'ollama serve; exec bash'
	@echo "Ollama server started in screen session 'ollama'"

run-qdrant-screen:
	screen -dmS qdrant bash -c 'qdrant --config-path config/config.yaml 2>&1 | tee qdrant.log; exec bash'
	@echo "Qdrant server started in screen session 'qdrant'"

run-screens: run-qdrant-screen run-ollama-screen
