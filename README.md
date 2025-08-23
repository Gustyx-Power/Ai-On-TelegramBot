# AI-On-TelegramBot
**Open-source, multi-backend Telegram chatbot.**

AI-On-TelegramBot is a versatile open-source Telegram chatbot that supports various AI backends. This project is designed to provide an easy-to-use, customizable, and robust chatbot solution that can be seamlessly integrated into the Telegram platform. With support for multiple AI models, including Groq, Gemini, Kimi K2, OpenAI, and Meta AI, this chatbot offers flexibility and a wide range of natural language processing capabilities.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg?logo=telegram)](https://telegram.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=yellow)](https://www.python.org/)
[![Shell Script](https://img.shields.io/badge/Shell%20Script-bash-green.svg?logo=gnu-bash&logoColor=white)](https://www.gnu.org/software/bash/)
[![Linux](https://img.shields.io/badge/Linux-Kernel-yellow.svg?logo=linux&logoColor=black)](https://www.kernel.org/)
[![Groq](https://img.shields.io/badge/Powered%20by-Groq-green.svg)](https://groq.com/)
[![Gemini](https://img.shields.io/badge/Powered%20by-Gemini-blue.svg)](https://deepmind.google/technologies/gemini/)
[![Kimi K2](https://img.shields.io/badge/Powered%20by-Kimi%20K2-orange.svg)](https://www.kimi.ai/)
[![OpenAI](https://img.shields.io/badge/Powered%20by-OpenAI-black.svg)](https://openai.com/)
[![Meta AI](https://img.shields.io/badge/Powered%20by-Meta%20AI-blueviolet.svg)](https://ai.meta.com/)
[![LLM](https://img.shields.io/badge/Technology-LLM-lightgrey.svg)]()

## Telegram Bot Demo
![Demo GIF](https://raw.githubusercontent.com/Gustyx-Power/Ai-On-TelegramBot/master/result.gif)

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
This means you are free to use, modify, and distribute the software, provided you adhere to the terms of the GPLv3.

---

### Key Features:
- **Multi-Backend Support:** Integrates with various AI providers such as Groq, Gemini, OpenAI, etc.
- **Customizable:** Open-source code allows for easy modification and customization.
- **GPLv3 License:** Ensures the freedom to use, modify, and distribute the software.
- **Easy Installation Scripts:** Simplified scripts to set up dependencies and run the bot.
- **User & Group Tracking:** Automatically tracks prompt counts and premium status for users, as well as joined group IDs.
- **Cross-Platform Compatibility:** Designed to run on Linux, Windows Subsystem for Linux, Termux-Proot, and Termux-Chroot.
- **Privacy-Focused:** Options for local LLMs to ensure data privacy.
- **Performance Optimized:** Capable of handling high request rates with efficient backend models.
- **Community-Driven:** Encourages contributions and improvements from the open-source community.
- **Comprehensive Documentation:** Provides clear instructions for installation, configuration, and usage.


## Quick Start

### 1. Choose Your Path
| Path | Command | Notes                                                                      |
| --- | --- |----------------------------------------------------------------------------|
| **API Cloud** | `./install-dependencies-api.sh` | Ensure you have an API key on [console.groq.com](https://console.groq.com) |
| **Local (Offline)** | `./install-local-llm.sh` | Requires approximately 8 GB RAM and a GPU (minimal 2GB VRAM) or 4 Core CPU |

### 2. Pick Your Bot
| File            | Backend                            | Description                                                                         |
|-----------------|------------------------------------|-------------------------------------------------------------------------------------|
| `bot-openai.py` | Groq / OpenAI                      | 185 t/s, 128 k context, model selection (LLaMA, Kimi K2, GPT 4.1, Meta Ai).         |
| `bot-gemini.py` | Gemini-1.5-Flash or Gemini-1.5-Pro | 60 req/min free.                                                                    |
| `bot-ollama.py` | Ollama local (Llama 3.2)           | Model Selection (LLaMA 3.2,LLaMA 3.1,Tinyllama or etc.), No internet, 100% privacy. |

### 3. Run Your Bot
```bash
./run-bot          # Run bot-openai.py
./run-mt           # Maintenance broadcast
./run-done-mt      # Broadcast “maintenance complete”
```

### Data
| File          | Function                                         |
| ------------- | ---------------------------------------------- |
| `users.json`  | Prompt count and premium status auto-tracking. |
| `groups.json` | Automatically joined group IDs. |

### Requirements
| OS                                                                 | Status                                   |
|--------------------------------------------------------------------|------------------------------------------|
| **Linux / Windows Subsystem Linux / Termux-Proot / Termux-Chroot** | 🚀 Supported                             |
| **Windows (native)**                                               | 🚫 Not supported (bash & ollama issues). |

### Additional Information
> [!TIP]
> - ⚠️ **Before Execution:** Read the entire code of each file to avoid token/API errors.
> - Ensure Python ≥ 3.11 and pip is installed.
> - For API-based bots, an internet connection is required.
> - For local LLM bots, ensure your system meets the specified hardware requirements.
> - The `users.json` and `groups.json` files are created automatically upon the first run if they don't exist.
> - It is recommended to back up your `users.json` and `groups.json` files regularly.
> - For troubleshooting, check the bot's console output for error messages.

**Built by [@Gustyx-Power](https://github.com/Gustyx-Power)**
