import math
import string
import sys

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
        print(f"1 - {putils.processStyle("Start a New Conversation", 'blue','bold')}")
        print(f"2 - {putils.processStyle("Open Previous Conversations", 'yellow','italic')}")
        print(f"3 - {putils.processStyle("Preferences", 'orange','underlined')}")
        while True:
            try:
                response = input("> ")
                if response == ":/quit":
                    sys.exit(0)
                menuIndex = int(response)
                if 3 < menuIndex < 1:
                    continue
                putils.clearScreen()
                break
            except Exception:
                continue

    elif menuIndex == 1:
        prompt = input("> ")
        if prompt == ":/new":
            instance.new_conversation()
            putils.clearScreen()
            continue
        elif prompt == ":/quit":
            menuIndex = 0
            instance.save_conversation(True)
            continue
        putils.separator()
        response, timetaken = instance.chat(prompt)
        putils.parse_markdown(response)
        putils.separator()
        print(putils.processStyle(f"Time taken to generate response: {math.trunc(timetaken)} seconds","aqua", "italic"))
        print()

    elif menuIndex == 2:
        files = instance.fetch_conversation_saves()
        for i in range(len(files)):
            print(f"{i + 1} -> {files[i].__str__()}")
        print()
        response = 0
        while True:
            try:
                response = input("> ")
                if response == ":/quit":
                    menuIndex = 0
                    break
                if 0 > int(response) > len(files): continue

                putils.clearScreen()
                menuIndex = 1
                instance.set_conversation(files[int(response) - 1])
                break
            except:
                continue
