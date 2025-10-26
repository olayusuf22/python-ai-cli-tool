#!/usr/bin/env python3
"""
Python AI CLI Tool (Clean Output Version with Safe Exit)
A cross-platform CLI that interacts with locally installed Ollama models.
Now displays clean AI responses instead of raw JSON and handles SystemExit gracefully.
"""

import click
import subprocess
import requests
import json
import sys

OLLAMA_API = "http://localhost:11434/api"

@click.group()
def cli():
    """Python CLI Tool for interacting with Ollama models."""
    pass

@cli.command()
def list():
    """List all available Ollama models."""
    try:
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, encoding="utf-8"
        )
        if result.returncode == 0:
            click.echo("Available Ollama Models:\n")
            click.echo(result.stdout)
        else:
            click.echo("⚠️  Error listing models.")
    except FileNotFoundError:
        click.echo("❌ Ollama not found. Please install Ollama first (https://ollama.com/download).")
    except Exception as e:
        click.echo(f"❗ Unexpected error: {e}")

@cli.command()
@click.option("--model", prompt="Enter model name", help="Name of the Ollama model (e.g., llama3, mistral)")
@click.option("--prompt", prompt="Enter your prompt", help="Text prompt for the model")
def run(model, prompt):
    """Run a specific model with a user prompt and display clean text output."""
    try:
        click.echo(f"🧠 Running model '{model}' with prompt:\n{prompt}\n")

        payload = {"model": model, "prompt": prompt}
        response = requests.post(f"{OLLAMA_API}/generate", json=payload, stream=True)

        if response.status_code == 200:
            click.echo("🤖 Model Response:\n")

            # Collect text responses only (ignore metadata)
            full_text = ""
            for line in response.iter_lines():
                if not line:
                    continue
                try:
                    data = json.loads(line.decode("utf-8"))
                    if "response" in data:
                        full_text += data["response"]
                except Exception:
                    continue

            click.echo(full_text.strip())
        else:
            click.echo(f"⚠️  Error: {response.status_code} - {response.text}")

    except requests.exceptions.ConnectionError:
        click.echo("❌ Could not connect to Ollama. Please make sure it's running locally.")
    except Exception as e:
        click.echo(f"❗ Unexpected error: {e}")

def safe_cli():
    """Wrapper to prevent SystemExit: 0 output when Click finishes normally."""
    try:
        cli()
    except SystemExit as e:
        # Only suppress SystemExit if exit code is 0 (normal termination)
        if e.code != 0:
            sys.exit(e.code)

if __name__ == "__main__":
    safe_cli()
