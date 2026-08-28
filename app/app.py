from textual.app import App
from textual.binding import Binding

from app.screens.screen import TypingScreen


class TypingApp(App):
    CSS = """
    Screen {
        background: #0f172a;
        color: #f8fafc;
        align: center middle;
    }

    TypingArea {
        width: 76;
        height: auto;
        padding: 1 2;
        border: round #334155;
        background: #1e293b;
    }

    ResultWidget {
        width: 76;
        height: auto;
        padding: 1 2;
        border: round #38bdf8;
        background: #1e293b;
    }
    """

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", show=False),
    ]

    def on_mount(self) -> None:
        self.push_screen(TypingScreen())
