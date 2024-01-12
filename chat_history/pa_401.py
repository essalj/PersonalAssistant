import openai
from openai import OpenAI


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def save_file(filepath, content):
    with open(filepath, 'a', encoding='utf-8') as outfile:
        outfile.write(content)


openai_api_key = open_file('c:\\my\\git\\api-keys\\openaiapikey.txt')
# openai_api_key = userdata.get('openai')
client = OpenAI(api_key=openai_api_key)

gpt4 = "gpt-4-1106-preview"
gpt3 = "gpt-3.5-turbo-1106"
chatbot_role = "You are a helpful personal assistant"

# memory = open_file('recent_chat.txt')
# conversation = []

def load_conversation_history(filepath):
    conversation_history = []
    try:
        with open(filepath, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        for i in range(0, len(lines), 2):
            if i + 1 < len(lines):
                user_msg = lines[i].strip()
                assistant_msg = lines[i + 1].strip()
                conversation_history.append({"role": "user", "content": user_msg})
                conversation_history.append({"role": "assistant", "content": assistant_msg})
    except FileNotFoundError:
        print(f"File not found: {filepath}. Starting a new conversation.")
    return conversation_history


def save_chat_history(userinput, response):
  with open('recent_chat.txt', 'a', encoding='utf-8') as outfile:
    outfile.write('\n')
    outfile.write(userinput + '\n' + response + '\n')

def chatgpt(userinput, temperature=0.8, frequency_penalty=0.2, presence_penalty=0, system_role=chatbot_role, model = gpt3):
  conversation.append({"role": "user", "content": userinput})
  messagein = conversation
  response = client.chat.completions.create(
    model = model,
    temperature=temperature,
    frequency_penalty=frequency_penalty,
    presence_penalty=presence_penalty,
    messages=messagein
  )
  response_text = response.choices[0].message.content
  conversation.append({"role": "assistant", "content": response_text})
  
  save_chat_history(userinput, response_text)
  
  return response_text

# def personal_assistant():
#   while True:
#     user_input = input("How can I assist you? ")
#     response = chatgpt(user_input)
#     print(response)


def personal_assistant():
    global conversation
    conversation = load_conversation_history('recent_chat.txt')  # Load previous conversation

    while True:
        user_input = input("How can I assist you? ")
        if user_input.lower() in ['exit', 'quit']:  # Option to exit the conversation
            print("Goodbye!")
            break
        response = chatgpt(user_input)
        print(response)
personal_assistant()

