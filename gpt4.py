import asyncio
import string
import sys

from rich import print as printmd
from rich.markdown import Markdown
import openai
from datetime import datetime
import os

class Gpt4Instance:
    def __init__(self, header: string = "You are a helpful assistant.", key: string = ""):
        self.header = header
        self.key = key
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        self.responses = ["DefaultResponse"]
        self.conversationStamp: string = datetime.now().strftime("date%Y-%m-%d_time%H.%M.%S")

        if not os.path.exists('conversations'):
            os.makedirs('conversations')

        self.log_file = open(os.path.join('conversations',f"{self.conversationStamp}.conv_log"), "w")
        openai.api_key = key

    def chat(self, prompt: string):
        self.messages.append(dict({"role": "user", "content": prompt}))
        response = openai.ChatCompletion.create(model="gpt-4", messages=self.messages)['choices'][0]['message']['content']
        self.responses.append(response)
        self.log_file.write(f"> {prompt}\nResponse: {response}\n\n")
        return response

    def newConversation(self):
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        self.log_file.close()
        self.conversationStamp: string = datetime.now().strftime("date%Y-%m-%d_time%H.%M.%S")
        self.log_file = open(os.path.join('conversations',f"{self.conversationStamp}.conv_log"), "w")

    def __del__(self):
        self.log_file.close()

def dPrint(content, afterDelay: float = 0, returnLine: bool = True, delay: float = 0.01):
    asyncio.run(__delayedPrint__(content, afterDelay, returnLine, delay))

async def __delayedPrint__(content, afterDelay: float, returnLine: bool, delay: float = 0.01):    # Calculates the duration needed for pause between printing out each letter.
    for i in content: # Prints out the content letter by letter.
        print(i, end='')
        await asyncio.sleep(delay) # Uses an asynchronous await to sleep. similar to sys.sleep().
    if returnLine:
        print() # Returns the Line.
    await asyncio.sleep(afterDelay) # Delays the function after printing out the content. For custom purposes.

def parse_markdown_native(text):
    return Markdown(text)

def parse_markdown(text):
    md = Markdown(text)
    printmd(md)

def clearScreen():
    # if the Operating System is Windows
    if sys.platform == "win32":
        os.system("cls")
    # if the Operating System is Linux or MacOS
    if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
        os.system("clear") # Clears the terminal screen.
