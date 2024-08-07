from src.assessment_model import *
from src.prompt import *

def main():
    response = ''
    # try:
    api_key = load_api_key()
    if not api_key:
        raise ValueError("API key is missing.")

    client = create_client(api_key)
    assistant = create_assistant(client)
    thread = create_thread(client)

    user_skill = input("Enter your skills (separated by commas): ")
    candidate_total_performance = []

    content = first_prompt(user_skill)
    response = handle_message_and_run(client, content, thread.id, assistant.id)
    if response:
        print_response(response)

    for i in range(2, 11):
        candidate_response = input("Choose an option: ")
        question = extract_question(response)
        candidate_total_performance.append(f"Q{i-1}: {question} A: {candidate_response}")
        content = evaluate_and_generate_next_question(candidate_response, question, i)

        response = handle_message_and_run(client, content, thread.id, assistant.id)
        if response:
            print_response(response)

    feedback_content = generate_feedback_prompt(candidate_total_performance)
    feedback_response = handle_message_and_run(client, feedback_content, thread.id, assistant.id)
    if feedback_response:
        print_response(feedback_response)

    client.beta.assistants.delete(assistant.id)

    # except Exception as e:
    #     print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
