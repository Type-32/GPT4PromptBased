import string
from collections.abc import Callable
from enum import Enum

from rich.markdown import Markdown
from textual.app import ComposeResult
from textual.containers import Horizontal, Container
from textual.reactive import Reactive, ReactiveType, reactive
from textual.widgets import Static, Placeholder, Label, MarkdownViewer

from gpt4 import Gpt4Instance
from msg_role import MsgRole


class MsgAlignment(Enum):
    LEFT = "left"
    RIGHT = "right"


class ChatMsg(Static):
    def __init__(self, alignment: MsgAlignment, msg_content: string, username: string):
        super().__init__()
        self.msg_content = msg_content
        self.username = username
        self.alignment = alignment
        self.content_view = MarkdownViewer(self.msg_content, id=("user-msg" if self.alignment else "gpt-msg"))

    def compose(self) -> ComposeResult:
        with Container(id="chat-row"):
            yield Label(self.username)
            yield Horizontal(
                self.content_view,
                id="chat-row"
            )

    def set_stream(self, gpt: Gpt4Instance, prompt: string):
        response = gpt.chat(prompt)
        connected = ""
        for chunks in response:
            result = chunks.to_dict().get("choices")[0].get("delta").get("content")
            if isinstance(result, str):
                try:
                    connected += result
                    self.msg_content = connected
                    self.content_view._markdown = connected
                    self.content_view.refresh()
                except Exception:
                    self.msg_content = "N/A"
        gpt.currentConversation.add_msg(prompt, MsgRole.USER)
        gpt.currentConversation.add_response(connected)
        gpt.save_conversation()


    def get_message(self) -> string:
        return self.msg_content

    def get_alignment(self) -> MsgAlignment:
        return self.alignment
