from typing import Optional
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.widgets import Input, OptionList, Static
from textual.widgets.option_list import Option

from app.models.settings import PracticeSettings


class CommandPalette(ModalScreen[Optional[PracticeSettings]]):
    CSS = """
    CommandPalette {
        align: center middle;
        background: rgba(15, 23, 42, 0.75);
    }

    #palette-container {
        width: 68;
        height: auto;
        max-height: 22;
        border: round #38bdf8;
        background: #1e293b;
        padding: 1 2;
    }

    #palette-title {
        color: #38bdf8;
        text-style: bold;
        margin-bottom: 1;
    }

    Input {
        border: solid #475569;
        background: #0f172a;
        color: #f8fafc;
        margin-bottom: 1;
    }

    OptionList {
        background: #0f172a;
        border: solid #334155;
        height: 12;
    }
    """

    BINDINGS = [
        Binding("escape", "cancel", "Cancel", show=False),
    ]

    def __init__(self, settings: PracticeSettings) -> None:
        super().__init__()
        self.settings = PracticeSettings(
            word_count=settings.word_count,
            language=settings.language,
            punctuation=settings.punctuation,
            numbers=settings.numbers,
            difficulty=settings.difficulty,
        )
        self.all_commands: list[tuple[str, str, str]] = []
        self._build_command_list()

    def _build_command_list(self) -> None:
        punc_status = "ON" if self.settings.punctuation else "OFF"
        num_status = "ON" if self.settings.numbers else "OFF"

        self.all_commands = [
            ("words_10", "Words: 10 Words", "Set target length to 10 words"),
            ("words_25", "Words: 25 Words", "Set target length to 25 words"),
            ("words_50", "Words: 50 Words", "Set target length to 50 words"),
            ("words_100", "Words: 100 Words", "Set target length to 100 words"),
            ("toggle_punc", f"Rules: Punctuation [Currently {punc_status}]", "Toggle punctuation and capitalization"),
            ("toggle_num", f"Rules: Numbers [Currently {num_status}]", "Toggle random numbers"),
            ("diff_regular", "Difficulty: Regular", "Normal rules with backspace enabled"),
            ("diff_hard", "Difficulty: Hard", "Stop on character errors"),
            ("diff_expert", "Difficulty: Expert", "No backspace allowed"),
            ("restart", "Action: Restart Test", "Start a fresh test immediately"),
            ("quit", "Action: Quit TypeForge", "Exit application"),
        ]

    def compose(self) -> ComposeResult:
        with Static(id="palette-container"):
            yield Static("TYPEFORGE // COMMAND PALETTE", id="palette-title")
            yield Input(placeholder="Search commands or settings...", id="palette-input")
            yield OptionList(id="palette-options")

    def on_mount(self) -> None:
        self._populate_options()
        self.query_one(Input).focus()

    def _populate_options(self, filter_text: str = "") -> None:
        option_list = self.query_one(OptionList)
        option_list.clear_options()

        filter_lower = filter_text.strip().lower()
        for cmd_id, title, desc in self.all_commands:
            if not filter_lower or filter_lower in title.lower() or filter_lower in desc.lower():
                prompt = f"[bold #f8fafc]{title}[/]\n  [dim #94a3b8]{desc}[/]"
                option_list.add_option(Option(prompt, id=cmd_id))

    def on_input_changed(self, event: Input.Changed) -> None:
        self._populate_options(event.value)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        option_list = self.query_one(OptionList)
        if option_list.option_count > 0:
            highlighted = option_list.highlighted
            if highlighted is not None:
                option = option_list.get_option_at_index(highlighted)
                self._execute_option(option.id)
            else:
                option = option_list.get_option_at_index(0)
                self._execute_option(option.id)

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self._execute_option(event.option.id)

    def _execute_option(self, option_id: Optional[str]) -> None:
        if not option_id:
            return

        if option_id == "words_10":
            self.settings.word_count = 10
        elif option_id == "words_25":
            self.settings.word_count = 25
        elif option_id == "words_50":
            self.settings.word_count = 50
        elif option_id == "words_100":
            self.settings.word_count = 100
        elif option_id == "toggle_punc":
            self.settings.punctuation = not self.settings.punctuation
        elif option_id == "toggle_num":
            self.settings.numbers = not self.settings.numbers
        elif option_id == "diff_regular":
            self.settings.difficulty = "regular"
        elif option_id == "diff_hard":
            self.settings.difficulty = "hard"
        elif option_id == "diff_expert":
            self.settings.difficulty = "expert"
        elif option_id == "quit":
            self.app.exit()
            return

        self.dismiss(result=self.settings)

    def action_cancel(self) -> None:
        self.dismiss(result=None)
