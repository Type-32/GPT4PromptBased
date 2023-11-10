from datetime import datetime
import json
import os
import string

from msg_role import MsgRole


class Conversation:
    def __init__(self, filename: string = None, prompt: string = None):
        if not os.path.exists('conversations'):
            os.makedirs('conversations')
        if filename is not None:
            self.__readfile__(filename)
            self.filename = filename
        else:
            self.history = {"messages": [{"role": "system", "content": "You are a helpful and knowledgeable assistant." if not prompt else prompt}], "responses": ["DefaultResponse"]}
            self.timestamp = datetime.now().strftime("date%Y-%m-%d_time%H.%M.%S")

        self.conv_name = ""

    def get_processed_timestamp(self) -> string:
        processed: string = self.timestamp[4:len(self.timestamp)]
        processed.replace("_time", ", ")
        return processed

    def to_dict(self):
        return {
            'history': self.history,
            'timestamp': self.timestamp,
            'conversation_name': self.conv_name
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
