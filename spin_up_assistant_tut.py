import openai
from openai import OpenAI 



def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

openai_api_key = open_file('c:\\my\\git\\api-keys\\openaiapikey.txt')
client = OpenAI(api_key=openai_api_key)

asssistant = client.beta.assistants.create(
    name = "PersonalAssistant",
    instructions = "You are a helpful personal assistant",
    tools = [{"type": "code_interpreter", "name": "python"}],
    model = "gpt-4-1106-preview"
)

thread = client.beta.threads.create() # create conversation thread

message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role = "user",
    content = "I need to solve this equation: 3x + 11 = 20. Can you help me."
)

run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id=asssistant.id,
    instructions="Please address user as Lasse"
)

#wait for run to conplete
import time
time.sleep(10)

run_status = client.beta.threads.runs.retrieve(
    thread_id = thread.id,
    run_id = run.id 
)

if run_status.status == "completed":
    messages = client.beta.threads.messages.list(
        thread_id = thread.id
    )

for msg in messages.data:
    role = msg.role
    content = msg.content[0].text.value
    print(f"{role.capitalize()}: {content}")
