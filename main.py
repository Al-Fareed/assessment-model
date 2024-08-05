from src.assessment_model import *
def main():
    api_key = load_api_key()
    client = create_client(api_key)
    assistant = create_assistant(client)
    thread = create_thread(client)
    create_message(client, thread.id)
    
    run = run_assistant(client, thread.id, assistant.id)
    print("Run completed with status: " + run.status)

    if run.status == "completed":
        print_run_results(client, thread.id)

    client.beta.assistants.delete(assistant.id)

if __name__ == "__main__":
    main()