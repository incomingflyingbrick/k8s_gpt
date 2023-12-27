import json
import os
import typer
from rich import print
from agentk8s.constant import app_name
from pathlib import Path

app = typer.Typer()


@app.callback()
def callback():
    print("Callback executed")


@app.command(name='chat')
def chat():
    """
    Start chat with the k8s agent, let agent do things for you
    """


@app.command(name='setup')
def setup():
    api_key = typer.prompt("Enter your GPT-4 API KEY")
    config_list = [{
        "model": "gpt-4",
        "api_key": api_key
    }]
    config_path = "./OAI_CONFIG_LIST"
    with open(str(config_path), 'w') as file:
        json.dump(config_list, file)

