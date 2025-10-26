# 🧠 Python AI CLI Tool

A simple and modular **Python-based Command-Line Interface (CLI)** for interacting with locally installed **Ollama AI models**.

---

## 🎯 Goal

This project fulfills the requirements of the **Python AI CLI Tool Assignment**, which involves building a CLI that:
- Lists all Ollama models installed locally.
- Runs a prompt on a selected model and displays the output in the terminal.
- Includes a **bonus idea** on how the CLI can be extended for **Kubernetes diagnostics** (see [BONUS.md](BONUS.md)).

---

## ⚙️ Features

- 🧩 **List available models:** Displays all Ollama models installed on your system.
- 💬 **Run a model prompt:** Sends any text prompt to a selected Ollama model and prints the response.
- 🧱 **Error handling:** Detects missing installations or invalid inputs and shows clean error messages.
- 🌍 **Cross-platform:** Works on Windows, macOS, and Linux.
- 📄 **UTF-8 safe:** Handles Unicode and emojis gracefully (no encoding errors on Windows).

---

## 🧰 Requirements

- **Python 3.8+**
- **Ollama** installed locally  
  → [Download Ollama](https://ollama.com/download)
- **Dependencies:** (install via pip)
  
  ```bash
  pip install -r requirements.txt

### HOW TO TEST #######

# Move into the project directory
cd python-ai-cli-tool

# Install dependencies
pip install -r requirements.txt

# List available Ollama models
python cli.py list

# Run a model (Option 1 )
python cli.py run --model llama3 --prompt "Explain Macmillan Learning in one sentence"

# Or (Option 2 - interactive mode)
python cli.py run
Enter model name: llama3
Enter your prompt: Explain Macmillan Learning in one sentence
