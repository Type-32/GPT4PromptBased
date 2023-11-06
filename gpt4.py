import json
import string
import time

import openai
from datetime import datetime
import os
from enum import Enum

class MsgRole(Enum):
    USER = "user"
    SYSTEM = "system"


class Conversation:
    def __init__(self, filename: string = None, prompt: string = None):
        if not os.path.exists('conversations'):
            os.makedirs('conversations')
        if filename:
            self.__readfile__(filename)
            self.timestamp = self.decode_timestamp(filename)
        else:
            self.history = {"messages": [{"role": "system", "content": "You are a helpful and knowledgeable assistant." if not prompt else prompt}], "responses": ["DefaultResponse"]}
            self.timestamp = datetime.now().strftime("date%Y-%m-%d_time%H.%M.%S")

    def get_messages(self, include_default: bool = False):
        result: list[string] = []
        for i in self.history['messages']:
            if i == {"role": "system", "content": "You are a helpful assistant."}: continue
            result.append(i.get("content"))
        return result

    def get_responses(self, include_default: bool = False):
        result: list[string] = []
        for i in self.history['responses']:
            if i == "DefaultResponse": continue
            result.append(i)
        return result

    def add_response(self, content: string):
        self.history['responses'].append(content)

    def add_msg(self, prompt: string, role: MsgRole):
        self.history["messages"].append(dict({"role": role.__str__(), "content": prompt}))

    def __readfile__(self, filename: string):
        """
        Extracts conversation file from file name.
        :param filename: conv_log file name.
        """
        fpath = os.path.join(os.path.curdir, 'conversations', filename)
        readResult = {}
        try:
            with open(fpath, 'r') as file:
                readResult = json.load(file)
                self.history = readResult
        except FileNotFoundError:
            print(f"File '{fpath}' not found.")

    def decode_timestamp(self, filename):
        """
        Extracts timestamp from conversation file names.
        :param filename: The file name.
        :return: The timestamp included in the file name.
        """
        timestamp_str = filename[4:-9]  # Extract the timestamp string from the filename
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

    def saveConversation(self, closeFile: bool = False):
        json.dump(self.currentConversation, self.log_file)
        if closeFile: self.log_file.close()

    def chat(self, prompt: string):
        """
        Uses the API and sends the API a prompt.
        :param prompt: The prompt for the Model.
        :return: The response for the prompt.
        """
        starttime = time.time()
        tokenlist = self.currentConversation.get_messages()
        tokenlist.append(prompt)
        response = openai.ChatCompletion.create(model="gpt-4", messages=tokenlist)['choices'][0]['message']['content']
        self.currentConversation.add_msg(prompt, MsgRole.USER)
        self.currentConversation.add_response(response)
        self.saveConversation()
        endtime = time.time() - starttime
        return response, endtime

    def new_conversation(self, prompt: string = None):
        """
        Creates a new conversation.
        """
        self.saveConversation(True)
        self.currentConversation = Conversation()
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
            result.append(Conversation(name))
        return result

    def refresh_conversations(self):
        self.conversations = self.fetch_conversation_saves()

    def __del__(self):
        self.log_file.close()
