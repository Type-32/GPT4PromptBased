from textual import events
from textual.app import App, ComposeResult
from textual.containers import Horizontal, ScrollableContainer
from textual.widgets import Placeholder, Header, Footer, Button, Static

from gpt4 import Conversation, Gpt4Instance
from views.conversation_menu import ConversationMenu
from widgets.conversation_button import ConversationButton


class MainMenu(Static):
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Button("Refresh", variant="default", id="refresh-button"),
            Button("Create New Conversation", variant="primary", id="new-conv-button"),
            Button("Settings", variant="default", id="settings-button"),
            id="new-conv-container"
        )

        yield Horizontal(
            ScrollableContainer(id="scroll-container"), id="conv-container"
        )

    def set_conversations(self, convList: list[Conversation]):
        scrollContainer = self.query_one("#scroll-container", ScrollableContainer)
        scrollContainer.remove_children()

        for conv in convList:
            convObj = ConversationButton(conv.conv_name, f"Created on {conv.get_processed_timestamp()}", conv.timestamp)
            scrollContainer.mount(convObj)
            convObj.scroll_visible()
        self.refresh()
