#!/usr/bin/env python3
"""
Python AI CLI Tool (PowerShell-Safe Enhanced Version)
Supports both flag and positional arguments, adds colorized output,
and prevents PowerShell from misinterpreting model responses as commands.
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
            click.secho("\n📦 Available Ollama Models:\n", fg="cyan", bold=True)
            click.echo(result.stdout.strip() + "\n")
        else:
            click.secho("⚠️  Error listing models.", fg="yellow")
    except FileNotFoundError:
        click.secho("❌ Ollama not found. Please install Ollama first (https://ollama.com/download).", fg="red")
    except Exception as e:
        click.secho(f"❗ Unexpected error: {e}", fg="red")


@cli.command(context_settings=dict(ignore_unknown_options=True))
@click.argument("model", required=False)
@click.argument("prompt", required=False, nargs=-1)
@click.option("--model", "model_opt", help="Name of the Ollama model (e.g., llama3, mistral)")
@click.option("--prompt", "prompt_opt", help="Text prompt for the model")
def run(model, prompt, model_opt, prompt_opt):
    """
    Run a specific model with a user prompt and display clean text output.

    Examples:
      python cli.py run llama3 "Explain Macmillan Learning"
      python cli.py run --model llama3 --prompt "Explain Macmillan Learning"
    """
    # Determine values from either positional or option args
    model_name = model_opt or model
    user_prompt = prompt_opt or " ".join(prompt)

    # If missing, ask interactively
    if not model_name:
        model_name = click.prompt("Enter model name", type=str)
    if not user_prompt:
        user_prompt = click.prompt("Enter your prompt", type=str)

    try:
        click.secho(f"\n🧠 Running model '{model_name}' with prompt:\n{user_prompt}\n", fg="yellow")

        payload = {"model": model_name, "prompt": user_prompt}
        response = requests.post(f"{OLLAMA_API}/generate", json=payload, stream=True)

        if response.status_code == 200:
            click.secho("🤖 Model Response:\n", fg="cyan", bold=True)

            # Collect clean text only
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

            # Display safely with spacing so PowerShell won't misinterpret
            click.secho("\n" + full_text.strip() + "\n", fg="green")
        else:
            click.secho(f"⚠️  Error: {response.status_code} - {response.text}", fg="yellow")

    except requests.exceptions.ConnectionError:
        click.secho("❌ Could not connect to Ollama. Please make sure it's running locally.", fg="red")
    except Exception as e:
        click.secho(f"❗ Unexpected error: {e}", fg="red")


def safe_cli():
    """Prevent SystemExit tracebacks for clean exit."""
    try:
        cli()
    except SystemExit as e:
        if e.code != 0:
            sys.exit(e.code)


if __name__ == "__main__":
    safe_cli()
