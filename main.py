import os
import string
import sys

import gpt4
from gpt4 import Gpt4Instance

def clearScreen():
    # if the Operating System is Windows
    if sys.platform == "win32":
        os.system("cls")
    # if the Operating System is Linux or MacOS
    if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
        os.system("clear") # Clears the terminal screen.

with open("key.openai_api_key_secure", 'r') as file:
    key = file.read()

instance: Gpt4Instance = Gpt4Instance(key=key)
prompt: string = ""
while prompt != "/quit/":
    prompt = input("> ")
    if prompt == "/new/":
        instance.newConversation()
        clearScreen()
        continue

    gpt4.parse_markdown(instance.chat(prompt))
    print()
    # gpt4.dPrint(gpt4.parse_markdown_native(instance.chat(prompt) + "\n"), 1, True)