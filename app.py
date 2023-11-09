from textual import on
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, Horizontal
from textual.widgets import Header, Footer, Button, Static, ContentSwitcher, Input, Label

from conversation import Conversation
from gpt4 import Gpt4Instance
from views.conversation_menu import ConversationMenu
from views.main_menu import MainMenu
from widgets.chat_msg import MsgAlignment
from widgets.conversation_button import ConversationButton

class ChatApp(App):
    """A Textual app to manage stopwatches."""
    CSS_PATH = [
        "app.tcss",
        "views/main_menu.tcss", "views/conversation_menu.tcss",
        "widgets/conversation_button.tcss", "widgets/chat_msg.tcss"
    ]
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    main_menu = MainMenu(id="__main-menu-view__")
    conversation_menu = ConversationMenu(id="__conversation-menu-view__")

    def __init__(self, gpt_instance: Gpt4Instance):
        super().__init__()
        self.gpt_instance = gpt_instance

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed"""
        if event.button.id == "new-conv-button":
            event.stop()
            self.query_one(ContentSwitcher).current = "__conversation-menu-view__"
            self.gpt_instance.new_conversation()
            self.query_one("#__conversation-menu-view__", ConversationMenu).set_conversation(self.gpt_instance.currentConversation)

        if event.button.id == "back-button":
            event.stop()
            self.gpt_instance.save_conversation(True)
            self.query_one(ContentSwitcher).current = "__main-menu-view__"
            self.refresh_conversations()

        if event.button.id == "refresh-button":
            event.stop()
            self.refresh_conversations()

        if event.button.id == "conv-button-enter":
            event.stop()
            timestamp = event.button.parent.parent.fetch_timestamp()
            self.gpt_instance.set_conversation(Conversation(timestamp + ".conv"))
            self.query_one(ContentSwitcher).current = "__conversation-menu-view__"
            self.query_one("#__conversation-menu-view__", ConversationMenu).set_conversation(self.gpt_instance.currentConversation)

        if event.button.id == "conv-button-delete":
            event.stop()
            flag: bool = event.button.parent.parent.delete_conversation()
            self.refresh_conversations()

    @on(Input.Submitted)
    def on_submit_input(self, event: Input.Submitted) -> None:
        event.stop()
        if event.input.id == "prompt-input":
            hintLabel = self.query_one("#prompt-error-hint", Label)
            if not event.validation_result.is_valid:
                hintLabel.update(event.validation_result.failure_descriptions[0])
            else:
                hintLabel.update("")
                val = event.input.value
                event.input.clear()
                menu = self.query_one(ConversationMenu)
                menu.add_message(val, "User", MsgAlignment.RIGHT)
                menu.stream_message(self.gpt_instance, val)

    def refresh_conversations(self):
        self.query_one("#__main-menu-view__", MainMenu).set_conversations(self.gpt_instance.fetch_conversation_saves())
        self.refresh()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with ContentSwitcher(initial="__main-menu-view__"):
            yield self.main_menu
            yield self.conversation_menu

    def on_mount(self):
        self.refresh_conversations()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

