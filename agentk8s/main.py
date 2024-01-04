import json
import os
import typer
from rich import print
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from typing_extensions import Annotated
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import chromadb
from typing import Optional
from rich.prompt import Prompt

client = chromadb.Client()
app = typer.Typer()


@app.callback()
def callback():
    print("[green]K-GPT Command Running :rocket:[/green]")


@app.command(name='local')
def local_cluster(
        cmd: Annotated[
            str, typer.Argument(help="Enter \"start\" or \"stop\" for turn on/off of minikube local cluster")]):
    """
    Start a minikube cluster locally or stop minikube cluster locally
    """
    if cmd == 'start':
        os.system('minikube start')
    elif cmd == 'stop':
        os.system('minikube stop')


@app.command(name='chat')
def chat(prompt: Annotated[str, typer.Argument(help="Enter a prompt like \"Show all deployments and services\" or "
                                                    "\"Read this yaml file, and found out what's wrong wit the "
                                                    "configuration.\"")],
         doc: Annotated[list[str], typer.Option(help="Enter url or file path, you can enter multiple --doc options,"
                                                     "Accepted file formats:\"['xml', 'htm',"
                                                     "'msg', 'docx',"
                                                     "'org', 'pptx', 'jsonl',"
                                                     "'txt', 'tsv', 'yml', 'json', 'md', 'pdf', 'xlsx', 'csv', "
                                                     "'html', 'log',"
                                                     "'yaml', 'doc', 'odt', 'rtf', 'ppt', 'epub', 'rst']\"")] = [],
         run_code: Annotated[bool, typer.Option(help="Weather to turn on code execution when --doc option is "
                                                     "supplied.")] = False):
    """
    Start chat with the k8s agent, let agent do things for you, you can chat with doc using --doc /path/to/doc/folder
    or --doc doc_url or for multiple docs you can enter option like this --doc /path/to/docs/folder --doc doc_url
    """
    config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
    termination_notice = (
        '\n\nDo not show appreciation in your responses, say only what is necessary. '
        'if "Thank you" or "You\'re welcome" are said in the conversation, then say TERMINATE '
        'to indicate the conversation is finished and this is your last message.'
    )
    if len(doc) > 0:
        # Running assistant with RAG
        try:
            client.delete_collection('autogen-docs')
        except ValueError:
            # print('Chromadb autogen-docs collection already deleted')
            pass
        assistant = RetrieveAssistantAgent(
            name="K-GPT (RAG enabled)",
            system_message='You are now an Kubernetes (k8s) expert.' 'You should use kubectl '
                           'command to complete task, you should output code blocks in shell '
                           'format',
            llm_config={
                "temperature": 0,
                "timeout": 600,
                "cache_seed": 42,
                "config_list": config_list,
            },
        )

        rag_proxy_agent = RetrieveUserProxyAgent(
            name="User",
            human_input_mode="TERMINATE",
            max_consecutive_auto_reply=15,
            retrieve_config={
                "task": "default",
                "docs_path": doc,
                "model": config_list[0]["model"],
                "embedding_model": "all-mpnet-base-v2",
                "get_or_create": False,
                "must_break_at_empty_line": False
            },
            code_execution_config={"work_dir": "coding", "use_docker": False} if run_code else False,
            llm_config={"temperature": 0, "seed": 42,
                        "config_list": config_list}
        )
        prompt += termination_notice
        assistant.reset()
        rag_proxy_agent.initiate_chat(assistant, problem=prompt, clear_history=True)
    else:
        if run_code:
            print("Option [red]--doc[/red] is not supplied, so [red]--run-code[/red] option is ignored")
        # Running assistant without RAG
        assistant = AssistantAgent("K-GPT", llm_config={"temperature": 0, "seed": 41,
                                                        "config_list": config_list},
                                   system_message='You are now an Kubernetes (k8s) expert.' 'You should use kubectl '
                                                  'command to complete task, you should output code blocks in shell '
                                                  'format, do not output yaml')

        user_proxy = UserProxyAgent("User", max_consecutive_auto_reply=15, human_input_mode="TERMINATE",
                                    code_execution_config={"work_dir": "coding", "use_docker": False},
                                    llm_config={"temperature": 0, "seed": 41,
                                                "config_list": config_list})
        prompt += termination_notice
        assistant.reset()
        user_proxy.initiate_chat(assistant, message=prompt, clear_history=True)


@app.command(name='setup')
def setup():
    """
    Run this command first after you install \"agentk8s\ with pip", it will prompt you to enter your openAI GPT-4 API-KEY
    """
    api_key = Prompt.ask("Enter your openAI GPT-4 API KEY :rocket:")
    config_list = [{
        "model": "gpt-4-1106-preview",
        "api_key": api_key
    }]
    config_path = "./OAI_CONFIG_LIST"
    with open(str(config_path), 'w') as file:
        json.dump(config_list, file)
    print("[green]K-GPT Setup Success[/green]")


@app.command(name='model')
def change_model(
        model_name: Annotated[str, typer.Argument(help="Change LLM model, default is GPT-4")] = "gpt-4-1106-preview"):
    """
    Change the default model, the default model is gpt-4-1106-preview
    """
    file_path = './OAI_CONFIG_LIST'
    data = None
    try:
        # Open the file in read mode
        with open(file_path, 'r') as json_file:
            # Load the JSON data from the file into a Python dictionary
            data = json.load(json_file)
    except FileNotFoundError:
        print(f"Config file '{file_path}' not found. Run \"kgpt setup first\"")
        raise typer.Abort()
    except json.JSONDecodeError:
        print(f"Failed to decode JSON in '{file_path}'.")
        raise typer.Abort()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise typer.Abort()
    if data is None:
        print("[red]Model change failed[/red]")
        raise typer.Abort()

    config_list = [{
        "model": model_name,
        "api_key": data[0]['api_key']
    }]
    config_path = "./OAI_CONFIG_LIST"
    with open(str(config_path), 'w') as file:
        json.dump(config_list, file)
    print("[green]Model change success[/green]")
