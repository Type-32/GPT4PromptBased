import string

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, ScrollableContainer, Container
from textual.validation import Number, Validator, ValidationResult
from textual.widgets import Placeholder, Header, Footer, Button, Static, Label, Input, TextArea, Pretty

from gpt4 import Gpt4Instance, Conversation
from widgets.chat_msg import ChatMsg, MsgAlignment
from widgets.conversation_button import ConversationButton


class PromptValidator(Validator):
    def validate(self, value: str) -> ValidationResult:
        if value.isspace() or not value:
            return self.failure("Prompt cannot be empty or whitespace")
        return self.success()


class ConversationMenu(Static):

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Button("Back", id="back-button"),
            Horizontal(Static("Uninitialized Chat", id="conv-window-title_text")),
            Button("Refresh", variant="primary", id="refresh-conv-button"),
            id="conv-window-title_bar"
        )

        with Horizontal(id="content-container"):
            yield ScrollableContainer(id="scroll-container")
        yield Container(
            Label("", id="prompt-error-hint"),
            Input(placeholder="Enter your prompt here...",
                validators=[
                    PromptValidator()
                ],
                validate_on=["submitted"], id="prompt-input"), id="prompt-input-row"
        )

    def add_message(self, msg: string, username: string, alignment: MsgAlignment):
        msgObj = self.query_one("#scroll-container", ScrollableContainer)
        msgObj.mount(ChatMsg(alignment, msg, username))
        msgObj.scroll_visible()
        self.refresh()

    def stream_message(self, gpt: Gpt4Instance, prompt: string):
        obj = ChatMsg(MsgAlignment.LEFT, "", "GPT-4")
        msgObj = self.query_one("#scroll-container", ScrollableContainer)
        msgObj.mount(obj)
        msgObj.scroll_visible()
        obj.set_stream(gpt, prompt)
        obj.refresh()
        self.refresh()

    def remove_message(self, msg: string, alignment: MsgAlignment):
        widgets = self.query(ChatMsg)
        for w in widgets:
            if w.get_message() == msg and w.get_alignment() == alignment:
                w.remove()
                self.refresh()
                return

    def set_conversation(self, conversation: Conversation):
        self.query_one("#scroll-container", ScrollableContainer).remove_children()
        self.query_one("#prompt-input", Input).clear()
        msgList = conversation.get_messages()
        responseList = conversation.get_responses()
        for i in range(len(msgList)):
            self.add_message(msgList[i],"User", MsgAlignment.RIGHT)
            self.add_message(responseList[i], "GPT", MsgAlignment.LEFT)

        window_title = self.query_one("#conv-window-title_text")
        window_title.renderable = f"Conversation at {conversation.get_processed_timestamp()}"
        window_title.refresh()
        self.refresh()
