import openai
from openai import OpenAI


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


openai_api_key = open_file('c:\\my\\git\\api-keys\\openaiapikey.txt')
# openai_api_key = userdata.get('openai')
client = OpenAI(api_key=openai_api_key)

gpt4 = "gpt-4-1106-preview"
gpt3 = "gpt-3.5-turbo-1106"
chatbot_role = "You are a helpful personal assistant"

def chatgpt3 (userinput, temperature=0.8, frequency_penalty=0.2, presence_penalty=0, system_role=chatbot_role, model = gpt3):
    messagein = [
        {"role": "user", "content": userinput },
        {"role": "system", "content": system_role}]
    response = client.chat.completions.create(
        model = model,
        temperature=temperature,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        messages=messagein
    )
    response_text = response.choices[0].message.content
    return response_text
# prompt = "hello"
# r = chatgpt3(prompt, model = gpt4)
# print(r)


class PersonalAssistant:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        self.chat_log = []

    def chat(self, prompt):
        self.chat_log.append(prompt)
        response = chatgpt3("\n".join(self.chat_log), model=gpt3)
        self.chat_log.append(response)
        return response


assistant = PersonalAssistant(openai_api_key)

while True:
    user_input = input("You: ")
    response = assistant.chat(user_input)
    
    # Save chat to file with timestamp
    # from datetime import datetime
    # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    # assistant.chat_log.append(timestamp + " You: " + user_input)
    # assistant.chat_log.append(timestamp + " Assistant: " + response)
    
    save_file('recent_chat.txt', '\n'.join(assistant.chat_log))
    
    print("Assistant:", response)


