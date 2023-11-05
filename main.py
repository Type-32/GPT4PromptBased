import os
import string

import gpt4
from gpt4 import Gpt4Instance

# Get the current console size
rows, columns = os.popen('stty size', 'r').read().split()


with open("key.openai_api_key_secure", 'r') as file:
    key = file.read()

instance: Gpt4Instance = Gpt4Instance(key=key)
prompt: string = ""
while prompt != "/quit/":
    prompt = input("> ")
    if prompt == "/new/":
        instance.newConversation()
        gpt4.clearScreen()
        continue
    elif prompt == ":/params quit":
        break

    print("-" * int(columns))
    gpt4.parse_markdown(instance.chat(prompt))
    print("-" * int(columns))
    print()
    # gpt4.dPrint(gpt4.parse_markdown_native(instance.chat(prompt) + "\n"), 1, True)