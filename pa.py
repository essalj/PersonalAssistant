# Import necessary libraries
import datetime
import os
import openai
from openai import OpenAI

# Set your OpenAI API key
openai.api_key = open_file('c:\\my\\git\\api-keys\\openaiapikey.txt')
# openai.api_key = "your_openai_api_key"



client = OpenAI(api_key=openai_api_key)
# Define the Personal Assistant class
class PersonalAssistant:
    def __init__(self):
        self.conversation_log = "conversation_log.txt"
        self.read_previous_conversations()
        self.session_id = str(datetime.datetime.now().timestamp())

    def read_previous_conversations(self):
        if os.path.exists(self.conversation_log):
            with open(self.conversation_log, "r") as file:
                self.history = file.read()
        else:
            self.history = ""

    def write_conversation(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.conversation_log, "a") as file:
            file.write(f"{timestamp}: {message}\n")

    def get_response(self, message):
        # Use OpenAI's Completion model to generate a response
          response = openai.ChatCompletion.create(
            #   response = client.chat.completions.create(
        # response = openai.Completion.create(
            # model="text-davinci-003",  # Replace with an appropriate model name
            # model = "gpt-4-1106-preview",
            model = "gpt-3.5-turbo-1106",
            prompt=self.history + "\n\n" + message,
            max_tokens=150,
            temperature=0.9,
            stop=None,
            n=1,
            stream=False,
            logprobs=None,
            echo=True,
            presence_penalty=0,
            frequency_penalty=0,
            best_of=1,
            logit_bias=None
        )
        return response.choices[0].text.strip()

    def handle_written_input(self, input_text):
        self.write_conversation(f"User: {input_text}")
        response = self.get_response(input_text)
        self.write_conversation(f"PA: {response}")
        return response

# Main interaction loop for written communication
def main_written_communication():
    pa = PersonalAssistant()
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                break
            pa_response = pa.handle_written_input(user_input)
            print(f"PA: {pa_response}")
        except EOFError:
            break

if __name__ == "__main__":
    main_written_communication()