from typing import Optional
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen

from app.models.settings import PracticeSettings
from app.screens.command_palette import CommandPalette
from app.screens.result import ResultScreen
from app.widgets.typing_area import TypingArea


class TypingScreen(Screen):
    BINDINGS = [
        Binding("ctrl+r", "restart", "Restart Test", show=False),
        Binding("ctrl+k", "command_palette", "Command Palette", show=False),
        Binding("ctrl+q", "quit_app", "Quit", show=False),
    ]

    def __init__(self, settings: Optional[PracticeSettings] = None) -> None:
        super().__init__()
        self.settings = settings or PracticeSettings()

    def compose(self) -> ComposeResult:
        yield TypingArea(settings=self.settings)

    def on_typing_area_test_finished(self, message: TypingArea.TestFinished) -> None:
        def on_result_close(result_action: Optional[tuple[str, Optional[list[str]]]]) -> None:
            if not result_action:
                return
            action_type, target_words = result_action
            typing_area = self.query_one(TypingArea)
            if action_type == "repeat" and target_words:
                typing_area.reset_test(new_words=target_words)
            else:
                typing_area.reset_test()

        self.app.push_screen(
            ResultScreen(message.snapshot, message.target_words),
            callback=on_result_close,
        )

    def on_typing_area_test_aborted(self, message: TypingArea.TestAborted) -> None:
        pass

    def action_command_palette(self) -> None:
        def on_palette_dismiss(new_settings: Optional[PracticeSettings]) -> None:
            if new_settings:
                self.settings = new_settings
                typing_area = self.query_one(TypingArea)
                typing_area.apply_settings(self.settings, reset=True)

        self.app.push_screen(CommandPalette(self.settings), callback=on_palette_dismiss)

    def action_restart(self) -> None:
        typing_area = self.query_one(TypingArea)
        typing_area.reset_test()

    def action_quit_app(self) -> None:
        self.app.exit()
