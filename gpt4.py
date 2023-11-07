import json
import string
import time

import openai
from datetime import datetime
import os
from enum import Enum

import putils


class MsgRole(Enum):
    USER = "user"
    SYSTEM = "system"


def decode_timestamp(filename):
    """
    Extracts timestamp from conversation file names.
    :param filename: The file name.
    :return: The timestamp included in the file name.
    """
    timestamp_str = filename[4:-5]  # Extract the timestamp string from the filename
    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d_time%H.%M.%S')  # Convert the string to a datetime object
    return timestamp


class Conversation:
    def __init__(self, filename: string = None, prompt: string = None):
        if not os.path.exists('conversations'):
            os.makedirs('conversations')
        if filename is not None:
            self.__readfile__(filename)
        else:
            self.history = {"messages": [{"role": "system", "content": "You are a helpful and knowledgeable assistant." if not prompt else prompt}], "responses": ["DefaultResponse"]}
            self.timestamp = datetime.now().strftime("date%Y-%m-%d_time%H.%M.%S")

    def to_dict(self):
        return {
            'history': self.history,
            'timestamp': self.timestamp
        }

    def get_messages(self, include_default: bool = False):
        result: list[string] = []
        for i in self.history['messages']:
            if i["role"] == "system": continue
            result.append(i.get("content"))
        return result

    def get_messages_raw(self, include_default: bool = True):
        return self.history['messages']

    def get_responses(self, include_default: bool = False):
        result: list[string] = []
        for i in self.history['responses']:
            if i == "DefaultResponse": continue
            result.append(i)
        return result

    def get_responses_raw(self, include_default: bool = True):
        return self.history['responses']

    def add_response(self, content: string):
        self.history['responses'].append(content)

    def add_msg(self, prompt: string, role: MsgRole):
        self.history["messages"].append(dict({"role": role.value, "content": prompt}))

    def __readfile__(self, filename: string):
        """
        Extracts conversation file from file name.
        :param filename: conv_log file name.
        """
        readResult = None
        with open(os.path.join(os.path.curdir, 'conversations', filename), 'r') as file:
            readResult = json.load(file)
            self.history = readResult['history']
            self.timestamp = readResult['timestamp']

            # try:
            #     readResult = json.loads(next(file))
            #     self.history = readResult['history']
            #     self.timestamp = readResult['timestamp']
            #     return True
            # except Exception:
            #     print("exception")
            #     return False

    def __str__(self):
        return f"Conversation initiated at {self.timestamp}"


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
        response = openai.ChatCompletion.create(model="gpt-4", messages=tokenlist)['choices'][0]['message']['content']
        self.currentConversation.add_msg(prompt, MsgRole.USER)
        self.currentConversation.add_response(response)
        self.save_conversation()
        endtime = time.time() - starttime
        return response, endtime

    def new_conversation(self, prompt: string = None):
        """
        Creates a new conversation.
        """
        if self.log_file:
            self.log_file.close()
        if self.currentConversation:
            self.save_conversation(True)
        self.currentConversation = Conversation(prompt=prompt)
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

    def refresh_conversations(self):
        self.conversations = self.fetch_conversation_saves()

    def __del__(self):
        self.save_conversation(True)