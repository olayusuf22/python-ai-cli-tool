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

cd python-ai-cli-tool
pip install -r requirements.txt
python cli.py list
python cli.py run llama3 "Explain Macmillan Learning in one sentence"