#!/usr/bin/env python3
"""
Python AI CLI Tool (Auto-Recovery Enhanced Version)
Detects memory-related Ollama errors and automatically retries in CPU mode.
"""

import click
import subprocess
import requests
import json
import sys
import os

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
    Automatically retries in CPU mode if memory errors occur.
    """
    model_name = model_opt or model
    user_prompt = prompt_opt or " ".join(prompt)

    if not model_name:
        model_name = click.prompt("Enter model name", type=str)
    if not user_prompt:
        user_prompt = click.prompt("Enter your prompt", type=str)

    click.secho(f"\n🧠 Running model '{model_name}' with prompt:\n{user_prompt}\n", fg="yellow")

    try:
        payload = {"model": model_name, "prompt": user_prompt}
        response = requests.post(f"{OLLAMA_API}/generate", json=payload, stream=True)

        if response.status_code == 200:
            click.secho("🤖 Model Response:\n", fg="cyan", bold=True)
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
            click.secho("\n" + full_text.strip() + "\n", fg="green")

        else:
            error_text = response.text
            if "model requires more system memory" in error_text:
                click.secho(
                    "⚠️  The model requires more memory than available. "
                    "Retrying in CPU mode...\n", fg="yellow"
                )
                os.environ["OLLAMA_NO_GPU"] = "1"
                retry_payload = {"model": model_name, "prompt": user_prompt}
                retry = requests.post(f"{OLLAMA_API}/generate", json=retry_payload, stream=True)

                if retry.status_code == 200:
                    click.secho("🤖 Model Response (CPU Mode):\n", fg="cyan", bold=True)
                    full_text = ""
                    for line in retry.iter_lines():
                        if not line:
                            continue
                        try:
                            data = json.loads(line.decode("utf-8"))
                            if "response" in data:
                                full_text += data["response"]
                        except Exception:
                            continue
                    click.secho("\n" + full_text.strip() + "\n", fg="green")
                else:
                    click.secho(
                        "❌ CPU mode also failed. Try using a smaller model like 'mistral' or 'llama2'.",
                        fg="red"
                    )
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
