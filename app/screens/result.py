from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Static

from app.models.session import SessionSnapshot


class ResultWidget(Static):
    def __init__(self, snapshot: SessionSnapshot) -> None:
        super().__init__()
        self.snapshot = snapshot

    def render(self) -> str:
        m = self.snapshot.metrics
        elapsed = self.snapshot.elapsed_time
        outcomes = m.outcomes

        return (
            f"[bold #38bdf8]TYPEFORGE // TEST RESULTS[/]\n\n"
            f"  [bold #0284c7]Qualified Speed:[/]  [bold #22c55e]{m.wpm:5.1f} WPM[/]\n"
            f"  [bold #0284c7]Keystroke Accuracy:[/] [bold #38bdf8]{m.accuracy:5.1f} %[/]\n"
            f"  [bold #0284c7]Raw Speed:[/]         [bold #94a3b8]{m.raw_wpm:5.1f} WPM[/]\n"
            f"  [bold #0284c7]Active Duration:[/]   [bold #94a3b8]{elapsed:5.2f} s[/]\n\n"
            f"[bold #64748b]────────────────────────────────────────────[/]\n"
            f"[bold #0284c7]Character Outcomes:[/] "
            f"[#22c55e]{outcomes.correct} correct[/] / "
            f"[#ef4444]{outcomes.incorrect} incorrect[/] / "
            f"[#eab308]{outcomes.extra} extra[/] / "
            f"[#64748b]{outcomes.missed} missed[/]\n"
            f"[bold #0284c7]Word Statistics:[/]    "
            f"[#f8fafc]{m.correct_words} correct words[/] of [dim]{m.completed_words} completed[/]\n"
            f"[bold #64748b]────────────────────────────────────────────[/]\n\n"
            f"  [bold #38bdf8]Enter[/]   Next Test (new words)\n"
            f"  [bold #38bdf8]Ctrl+R[/]  Repeat Target\n"
            f"  [bold #38bdf8]Ctrl+Q[/]  Quit\n"
        )


class ResultScreen(Screen):
    BINDINGS = [
        Binding("enter", "next_test", "Next Test", show=False),
        Binding("ctrl+r", "repeat_test", "Repeat Test", show=False),
        Binding("r", "repeat_test", "Repeat Test", show=False),
        Binding("ctrl+q", "quit_app", "Quit", show=False),
        Binding("escape", "quit_app", "Quit", show=False),
        Binding("q", "quit_app", "Quit", show=False),
    ]

    def __init__(
        self, snapshot: SessionSnapshot, target_words: list[str]
    ) -> None:
        super().__init__()
        self.snapshot = snapshot
        self.target_words = target_words

    def compose(self) -> ComposeResult:
        yield ResultWidget(self.snapshot)

    def action_next_test(self) -> None:
        self.dismiss(result=("next", None))

    def action_repeat_test(self) -> None:
        self.dismiss(result=("repeat", self.target_words))

    def action_quit_app(self) -> None:
        self.app.exit()
