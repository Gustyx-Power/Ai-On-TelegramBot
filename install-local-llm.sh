#!/usr/bin/env bash
set -e
echo "===== Ollama-TG one-time install ====="

# 1. Ollama
if ! command -v ollama &>/dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

# 2. Model 1B (One Time Only)
if ! ollama list | grep -q llama3.2:3b; then
    echo "Pulling llama3.2:3b ..."
    ollama pull llama3.2:3b
fi

# 3. Python deps
cd (dirname (status --current-filename))
source venv/bin/activate  # For BashRC Shell
## source venv/bin/activate.fish # For Fish Shell
## source venv/bin/activate.zsh # For ZSH Shell
python -m pip install --user -r requirements.txt
echo "Install selesai. Selanjutnya: ~/ollama-tg/run-ollama"