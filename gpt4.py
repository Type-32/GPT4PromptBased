import json
import string
import time
from datetime import datetime

import openai
import os
from rich import print as printmd
from rich.markdown import Markdown

import putils
from conversation import Conversation
from msg_role import MsgRole


def decode_timestamp(filename):
    """
    Extracts timestamp from conversation file names.
    :param filename: The file name.
    :return: The timestamp included in the file name.
    """
    timestamp_str = filename[4:-5]  # Extract the timestamp string from the filename
    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d_time%H.%M.%S')  # Convert the string to a datetime object
    return timestamp


class Gpt4Instance:
    def __init__(self, header: string = "You are a helpful assistant.", key: string = ""):
        """
        Constructor for `Gpt4Instance`.
        :param header: The first prompt to the model. Will not be counted as a conversational prompt but sets the response style of the model.
        :param key: The OpenAI API Model Key.
        """
        self.log_file = None
        if not os.path.exists('conversations'):
            os.makedirs('conversations')
        self.header = header
        self.key = key
        self.conversations = self.fetch_conversation_saves()
        self.currentConversation: Conversation = None
        openai.api_key = key

    def save_conversation(self, closeFile: bool = False):
        if not self.log_file:
            return
        if self.log_file.closed:
            self.log_file = open(os.path.join('conversations', f"{self.currentConversation.timestamp}.conv"), "w")
        self.log_file.write("")
        self.log_file.flush()
        self.log_file.close()
        self.log_file = open(os.path.join('conversations', f"{self.currentConversation.timestamp}.conv"), "w")
        json.dump(self.currentConversation.to_dict(), self.log_file)
        if closeFile:
            self.currentConversation = None
            self.log_file.close()

    def chat(self, prompt: string):
        """
        Uses the API and sends the API a prompt.
        :param prompt: The prompt for the Model.
        :return: The response for the prompt.
        """
        if not self.currentConversation:
            self.new_conversation()
        starttime = time.time()
        tokenlist: list[dict[str, str]] = []
        for i in self.currentConversation.get_messages_raw():
            tokenlist.append(i)
        tokenlist.append(dict({"role": "user", "content": prompt}))
        return openai.ChatCompletion.create(model="gpt-4", messages=tokenlist, stream=True)

    def new_conversation(self, prompt: string = None, conv_name: string = "Untitled Conversation"):
        """
        Creates a new conversation.
        """
        if self.log_file:
            self.log_file.close()
        if self.currentConversation:
            self.save_conversation(True)
        self.currentConversation = Conversation(prompt=prompt, conv_name=conv_name)
        self.refresh_conversations()
        self.log_file = open(os.path.join('conversations', f"{self.currentConversation.timestamp}.conv"), "w")

    def fetch_conversation_saves(self):
        """
        Returns a list of Conversations.
        :return: List of Conversations.
        """
        dir_path = os.path.join(os.path.curdir, 'conversations')
        convNames = [f for f in os.listdir(dir_path) if f.endswith('.conv')]
        result: list[Conversation] = []
        for name in convNames:
            try:
                result.append(Conversation(name))
            except Exception:
                continue
        return result

    def set_conversation(self, conversation: Conversation, printPreviousConv: bool = True):
        if self.log_file:
            self.log_file.close()
        self.currentConversation = conversation
        self.log_file = open(os.path.join('conversations', f"{self.currentConversation.timestamp}.conv"), "w")
        if printPreviousConv:
            for i in range(len(self.currentConversation.get_messages())):
                print(f"> {self.currentConversation.get_messages()[i]}")
                putils.separator()
                putils.parse_markdown(self.currentConversation.get_responses()[i])
                putils.separator()
                print()

    def delete_conversation(self, filename) -> True:
        conversations_dir = os.path.join(os.path.curdir, 'conversations')
        file_to_delete = os.path.join(conversations_dir, filename)

        try:
            if os.path.isfile(file_to_delete):
                for i in self.conversations:
                    if i.timestamp + ".conv" == filename:
                        self.conversations.remove(i)
                        break
                os.remove(file_to_delete)
                return True
            else:
                return False
        except Exception:
            return False

    def refresh_conversations(self):
        self.conversations = self.fetch_conversation_saves()

    def __del__(self):
        self.save_conversation(True)