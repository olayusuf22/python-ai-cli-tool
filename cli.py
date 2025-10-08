#!/usr/bin/env python3
"""
Python AI CLI Tool
A command-line interface that interacts with locally installed Ollama models.
"""

import subprocess
import argparse
import sys

def list_models():
    """List all Ollama models available on the system."""
    try:
        # Use UTF-8 to handle all Unicode characters (e.g., emojis, special symbols)
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True
        )
        print("Available Ollama Models:\n")
        print(result.stdout)
    except FileNotFoundError:
        print("❌ Ollama not found. Please install Ollama from https://ollama.com/ first.")
    except subprocess.CalledProcessError as e:
        print("⚠️  Error listing models:", e.stderr)
    except Exception as e:
        print("❗ Unexpected error:", str(e))


def run_model(model_name: str, prompt: str):
    """Run a selected model with a given prompt."""
    try:
        print(f"🧠 Running model '{model_name}' with prompt:\n{prompt}\n")
        # Added encoding="utf-8" for Windows compatibility
        result = subprocess.run(
            ["ollama", "run", model_name, prompt],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True
        )
        print("🤖 Model Response:\n")
        print(result.stdout)
    except FileNotFoundError:
        print("❌ Ollama not found. Please install Ollama first.")
    except subprocess.CalledProcessError as e:
        print("⚠️  Error running model:", e.stderr)
    except Exception as e:
        print("❗ Unexpected error:", str(e))


def main():
    parser = argparse.ArgumentParser(
        description="Python CLI tool to interact with locally installed Ollama AI models."
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # `list` command
    subparsers.add_parser("list", help="List all installed Ollama models")

    # `run` command
    run_parser = subparsers.add_parser("run", help="Run a model with your prompt")
    run_parser.add_argument("model", help="Name of the Ollama model (e.g., llama3, codellama)")
    run_parser.add_argument("prompt", help="Text input for the model")

    args = parser.parse_args()

    if args.command == "list":
        list_models()
    elif args.command == "run":
        run_model(args.model, args.prompt)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
