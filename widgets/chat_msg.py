import asyncio
import os
import string
import sys
import time
from asyncio import Task
from collections.abc import Callable
from enum import Enum
from typing import Generator, Any

from openai.openai_object import OpenAIObject
from rich.markdown import Markdown
from textual import events
from textual.app import ComposeResult
from textual.containers import Horizontal, Container
from textual.reactive import Reactive, ReactiveType, reactive
from textual.widgets import Static, Placeholder, Label, MarkdownViewer, LoadingIndicator

from gpt4 import Gpt4Instance
from msg_role import MsgRole


class MsgAlignment(Enum):
    LEFT = "left"
    RIGHT = "right"


class ChatMsg(Static):
    def __init__(self, alignment: MsgAlignment, msg_content: string, username: string, prompt: string, gpt: Gpt4Instance):
        super().__init__()
        self.msg_content = msg_content
        self.username = username
        self.alignment = alignment
        self.prompt = prompt
        self.gpt = gpt
        self.markdownStatic = Static(Markdown(self.msg_content), id="user-msg" if self.alignment == MsgAlignment.RIGHT else "gpt-msg")

    def compose(self) -> ComposeResult:
        yield Container(
            Label(self.username),
            Horizontal(
                self.markdownStatic,
                id="chat-row"
            ), id="chat-row"
        )

    def on_mount(self) -> None:
        if self.prompt and self.gpt:
            asyncio.create_task(self.set_msg_from_stream(self.prompt, self.gpt))

    async def set_msg_from_stream(self, prompt: string, gpt: Gpt4Instance):
        self.refresh()
        response = gpt.chat(prompt)
        connected = ""
        mdview = self.query_one("#gpt-msg", Static)
        for chunk in response:
            result = chunk.to_dict().get("choices")[0].get("delta").get("content")
            if isinstance(result, str):
                connected += result
                self.msg_content = connected
                mdview.update(Markdown(connected))
                self.scroll_visible()
                self.refresh()
                mdview.refresh()
                await asyncio.sleep(0)
        gpt.currentConversation.add_msg(prompt, MsgRole.USER)
        gpt.currentConversation.add_response(connected)
        gpt.save_conversation()

    def get_message(self) -> string:
        return self.msg_content

    def get_alignment(self) -> MsgAlignment:
        return self.alignment
