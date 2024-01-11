import openai
from openai import OpenAI 
import time
# import gradio as gr


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

openai_api_key = open_file('c:\\my\\git\\api-keys\\openaiapikey.txt')
client = OpenAI(api_key=openai_api_key)


file = client.files.create(
    file = open("Eva's Eternal Nightmare Trapped in the Time Cult's Web - story.txt", "rb"),
    purpose='assistants'
)


# Create assistant
assistant = client.beta.assistants.create(
    name = "PersonalAssistant",
    instructions = "You are a helpful personal assistant",
    tools = [{"type": "code_interpreter", "name": "python"}],
    model = "gpt-4-1106-preview"
)


# Create thread
thread = client.beta.threads.create() # create conversation thread


def main(query):

    # Add message to thread
    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role = "user",
        content = query
    )

    # Run assistant
    run = client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id=assistant.id,
        instructions="Please address user as Lasse"
    )

    #wait for run to conplete
    while True:
        time.sleep(5)

        run_status = client.beta.threads.runs.retrieve(
            thread_id = thread.id,
            run_id = run.id 
        )

        print(run_status.model_dump_json(indent=4))

        if run_status.status == "completed":
            messages = client.beta.threads.messages.list(
                thread_id = thread.id
            )

            response = ""
            for msg in messages.data:
                role = msg.role
                content = msg.content[0].text.value
                response += (f"{role.capitalize()}: {content}\n\n")
            return response + "\n\n"

        else:
            continue

main("Fortæl om den historie vi snakkede om")

# Create Gradio interface
iface = gr.Interface(fn=main, inputs="textbox", outputs="textbox", title="Personal Assistant").launch()
iface.launch()

thread_id = 'thread_dUsDPfKhAjrefGxr7RtIC7JU'
messages = client.beta.threads.messages.list(thread_id = thread_id)

