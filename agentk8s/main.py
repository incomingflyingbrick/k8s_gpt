import json
import os
import typer
from rich import print
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

app = typer.Typer()


@app.callback()
def callback():
    print("Callback executed")


@app.command(name='local')
def local_cluster(cmd: str):
    """
    Start a minikube cluster locally or stop minikube cluster locally
    """
    if cmd == 'start':
        os.system('minikube start')
    elif cmd == 'stop':
        os.system('minikube stop')


@app.command(name='chat')
def chat(prompt: str):
    """
    Start chat with the k8s agent, let agent do things for you
    """
    # Load LLM inference endpoints from an env variable or a file
    # See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
    # and
    termination_notice = (
        '\n\nDo not show appreciation in your responses, say only what is necessary. '
        'if "Thank you" or "You\'re welcome" are said in the conversation, then say TERMINATE '
        'to indicate the conversation is finished and this is your last message.'
    )
    config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
    assistant = AssistantAgent("K-GPT", llm_config={"temperature": 0, "seed": 41,
                                                    "config_list": config_list},
                               system_message='You are now an Kubernetes (k8s) expert.' 'You should use kubectl '
                                              'command to complete task, you should output code blocks in shell format, do not output yaml')

    user_proxy = UserProxyAgent("user", max_consecutive_auto_reply=15, human_input_mode="TERMINATE",
                                code_execution_config={"work_dir": "coding", "use_docker": False},
                                llm_config={"temperature": 0, "seed": 41,
                                            "config_list": config_list})
    prompt += termination_notice
    user_proxy.initiate_chat(assistant, message=prompt)


@app.command(name='setup')
def setup():
    api_key = typer.prompt("Enter your GPT-4 API KEY")
    config_list = [{
        "model": "gpt-4-1106-preview",
        "api_key": api_key
    }]
    config_path = "./OAI_CONFIG_LIST"
    with open(str(config_path), 'w') as file:
        json.dump(config_list, file)
