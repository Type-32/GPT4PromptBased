import string

from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Static, Button, Label

from gpt4 import Gpt4Instance


class ConversationButton(Static):
    def __init__(self, conversation_name: string, description: str, timestamp: string):
        super().__init__()
        self.conversation_name = conversation_name
        self.description = description
        self.timestamp = timestamp

    def compose(self) -> ComposeResult:
        title = Static(self.conversation_name, id="conv-button-title")
        desc = Static(self.description, id="conv-button-desc")
        enter = Button("Enter", id="conv-button-enter", variant="default")
        delete = Button("Delete", id="conv-button-delete", variant="error")

        yield Horizontal(
            enter,
            Horizontal(title, desc, id="conv-button-text-container"),
            delete
        )

    def delete_conversation(self):
        Gpt4Instance().delete_conversation(self.timestamp + ".conv")

    def fetch_timestamp(self):
        return self.timestamp
