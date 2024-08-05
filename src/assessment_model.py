import openai
from dotenv import load_dotenv
import os
from prompt import get_instructions

def load_api_key():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")

def create_client(api_key):
    return openai.OpenAI(api_key=api_key)

def create_assistant(client):
    assistant = client.beta.assistants.create(
        name="Assessment model",
        instructions=get_instructions(),
        tools=[{"type": "code_interpreter"}],
        model="gpt-4-1106-preview",
    )
    return assistant

def create_thread(client):
    return client.beta.threads.create()

def create_message(client, thread_id, content):
    return client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content,
    )

def run_assistant(client, thread_id, assistant_id):
    return client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

def print_run_results(client, thread_id):
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    print("messages: ")
    for message in messages:
        assert message.content[0].type == "text"
        print({"role": message.role, "message": message.content[0].text.value})
