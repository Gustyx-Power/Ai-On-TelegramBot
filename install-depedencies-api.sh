#!/bin/bash

echo "===== ChatAi API-TG one-time install ====="

python --version
# Install Python dependencies
echo "Installing Depedencies"
cd (dirname (status --current-filename))
source venv/bin/activate  # For BashRC Shell
## source venv/bin/activate.fish # For Fish Shell
## source venv/bin/activate.zsh # For ZSH Shell
python -m pip install --user -r requirements.txt
echo "Dependencies installed"