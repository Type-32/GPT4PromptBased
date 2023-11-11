import string

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.validation import Function
from textual.widgets import Static, Label, Input, Button, ContentSwitcher

from views.main_menu import MainMenu


class NewConversationModal(ModalScreen):
    valid_name = False

    def compose(self) -> ComposeResult:
        yield Container(
            Label("Enter a name for your new conversation."),
            Input(placeholder="Enter Conversation Name...", validators=[
                Function(self.validate_conversation_name, "Cannot be Null or Empty or Contain Ambiguous Characters")
            ], id="new-conv-name-input"),
            Horizontal(
                Button("Confirm", variant="success", id="confirm-create-new-conv"),
                Button("Cancel", variant="error", id="cancel-create-new-conv"), id="new-conv-modal-buttons"
            ), id="new-conv-modal"
        )

    def validate_conversation_name(self, value: str) -> bool:
        special_characters = string.punctuation
        if value:
            for char in value:
                if char in special_characters:
                    return False
            return True

        return False

    @on(Input.Changed)
    def show_invalid_reasons(self, event: Input.Changed) -> None:
        # Updating the UI to show the reasons why validation failed
        if not event.validation_result.is_valid:
            # self.query_one(Pretty).update(event.validation_result.failure_descriptions)
            self.valid_name = False
        else:
            # self.query_one(Pretty).update([])
            self.valid_name = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        event.stop()
        if event.button.id == "confirm-create-new-conv":
            if self.valid_name:
                self.app.__create_new_conversation__(self.query_one("#new-conv-name-input", Input).value, self)

        if event.button.id == "cancel-create-new-conv":
            self.app.pop_screen()
