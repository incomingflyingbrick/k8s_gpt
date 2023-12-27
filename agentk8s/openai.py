import openai
import os
import time
import json

openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

function_tool = {
    "type": "function",
    "function": {
        "name": "excute_kubectl_command",
        "description": "excute kubectl command",
        "parameters": {
            "type": "object",
            "properties": {
                "kubectl_command": {
                    "type": "string",
                    "description": "The kubectl command needed to execute, excute kubectl command if user want to use kubectl ",
                }
            },
            "required": ["kubectl_command"],
        },
    },
}

assistant = client.beta.assistants.create(
    name="k8s agent",
    instructions="You are now an Kubernetes expert, you should generate kubectl command or k8s yaml resource file by following instructions, when you output kubectl command you should call function excute_kubectl_command ",
    tools=[{"type": "code_interpreter"}, {"type": "retrieval"}, function_tool],
    model="gpt-4-1106-preview",
)


def excute_kubectl_command(kubectl_command):
    print(kubectl_command)
    os.system(kubectl_command)


thread = client.beta.threads.create()
while True:
    msg = input("Enter your msg:")
    if msg == "exit":
        exit()
    message = client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=msg
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id, assistant_id=assistant.id
    )
    while True:
        time.sleep(3)
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id
        )
        if run_status.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            for resp in messages.data:
                if resp.run_id == run.id and resp.role == "assistant":
                    print(resp.content)
            break
        elif run_status.status == "requires_action":
            print("function call")

            tool_calls = run_status.required_action.submit_tool_outputs.tool_calls
            for item in tool_calls:
                if item.function.name == "excute_kubectl_command":
                    args = json.loads(item.function.arguments)
                    excute_kubectl_command(args["kubectl_command"])
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread.id, run_id=run.id, tool_outputs=[{"tool_call_id": item.id, "output": "Done"}]
                    )
            break

        else:
            time.sleep(3)
