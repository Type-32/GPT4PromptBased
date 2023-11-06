import os
import string

import gpt4
import putils
from gpt4 import Gpt4Instance

# Get the current console size
columns = 30

with open("key.openai_api_key_secure", 'r') as file:
    key = file.read()

instance: Gpt4Instance = Gpt4Instance(key=key)
prompt: string = ""

menuIndex: int = 0
fileSelect: int = 0

while True:
    if menuIndex == 0:
        putils.clearScreen()
        print("1 - Start a New Conversation")
        print("2 - Open Previous Conversations")
        print("3 - Preferences\n")
        while True:
            try:
                menuIndex = int(input("> "))
                if 3 < menuIndex < 1:
                    continue
            except Exception:
                continue

    elif menuIndex == 1:
        prompt = input("> ")
        if prompt == ":/params new":
            instance.new_conversation()
            putils.clearScreen()
            continue
        elif prompt == ":/params quit":
            break
        putils.separator()
        putils.parse_markdown(instance.chat(prompt))
        putils.separator()
        print()

    elif menuIndex == 2:
        putils.clearScreen()
        files: list[string] = instance.fetch_conversation_saves()
        for i in range(len(files)):
            print(f"{i} -> {files[i]}")