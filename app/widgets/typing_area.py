from typing import Optional
from textual import events
from textual.message import Message
from textual.widgets import Static

from app.content.targets import TargetProvider, get_default_target_provider
from app.core.session import TypingSession
from app.models.events import BackspacePressed, CharacterTyped, EscPressed
from app.models.session import SessionLifecycle, SessionSnapshot
from app.models.settings import PracticeSettings
from app.models.typing import TypingState


class TypingArea(Static):
    can_focus = True

    class TestFinished(Message):
        def __init__(self, snapshot: SessionSnapshot, target_words: list[str]) -> None:
            super().__init__()
            self.snapshot = snapshot
            self.target_words = target_words

    class TestAborted(Message):
        def __init__(self, snapshot: SessionSnapshot) -> None:
            super().__init__()
            self.snapshot = snapshot

    def __init__(
        self,
        settings: Optional[PracticeSettings] = None,
        target_provider: Optional[TargetProvider] = None,
        target_words: Optional[list[str]] = None,
    ) -> None:
        super().__init__()
        self.settings = settings or PracticeSettings()
        self.provider = target_provider or get_default_target_provider(self.settings.language)

        if target_words:
            self.target_words = target_words
        else:
            self.target_words = self.provider.generate(
                count=self.settings.word_count,
                punctuation=self.settings.punctuation,
                numbers=self.settings.numbers,
            )

        self.state = TypingState(target_words=self.target_words, typed="")
        self.session = TypingSession(
            policy=self.settings.get_policy(),
            state=self.state,
        )

    def on_mount(self) -> None:
        self.focus()
        self.set_interval(0.1, self._on_timer_tick)

    def _on_timer_tick(self) -> None:
        if self.session.lifecycle is SessionLifecycle.RUNNING:
            self.refresh()

    def apply_settings(self, settings: PracticeSettings, reset: bool = True) -> None:
        self.settings = settings
        if reset:
            self.reset_test()
        else:
            self.refresh()

    def reset_test(self, new_words: Optional[list[str]] = None) -> None:
        if new_words:
            self.target_words = new_words
        else:
            self.target_words = self.provider.generate(
                count=self.settings.word_count,
                punctuation=self.settings.punctuation,
                numbers=self.settings.numbers,
            )

        self.state = TypingState(target_words=self.target_words, typed="")
        self.session = TypingSession(
            policy=self.settings.get_policy(),
            state=self.state,
        )
        self.refresh()

    def on_key(self, event: events.Key) -> None:
        if self.session.lifecycle in (
            SessionLifecycle.ABORTED,
            SessionLifecycle.FINISHED,
        ):
            return

        domain_event = None

        if event.key == "escape":
            domain_event = EscPressed()
        elif event.key == "backspace":
            domain_event = BackspacePressed()
        elif event.key == "tab":
            return
        elif event.character and len(event.character) == 1:
            domain_event = CharacterTyped(event.character)
        else:
            return

        # Process domain event through pure session aggregate
        self.session.process(domain_event)

        snapshot = self.session.snapshot
        self.state = snapshot.state

        if self.session.lifecycle == SessionLifecycle.FINISHED:
            self.post_message(self.TestFinished(snapshot, self.target_words))
        elif self.session.lifecycle == SessionLifecycle.ABORTED:
            self.post_message(self.TestAborted(snapshot))

        self.refresh()

    def render(self) -> str:
        # Configuration header tags
        punc_str = "punc" if self.settings.punctuation else "no-punc"
        num_str = "num" if self.settings.numbers else "no-num"
        config_bar = (
            f"[dim #475569]MODE:[/] [bold #38bdf8]words {self.settings.word_count}[/]  "
            f"[dim #475569]LANG:[/] [bold #94a3b8]{self.settings.language}[/]  "
            f"[dim #475569]DIFF:[/] [bold #94a3b8]{self.settings.difficulty}[/]  "
            f"[dim #64748b][{punc_str} • {num_str}][/]"
        )

        target_text = self.state.target
        typed_text = self.state.typed
        rendered_chars = []

        target_len = len(target_text)
        cursor_pos = len(typed_text)

        for i, ch in enumerate(target_text):
            if i < cursor_pos:
                typed_char = typed_text[i]
                if typed_char == ch:
                    rendered_chars.append(f"[bold #22c55e]{ch}[/]")
                else:
                    rendered_chars.append(f"[bold #ef4444 underline]{typed_char}[/]")
            elif i == cursor_pos:
                rendered_chars.append(f"[reverse bold #38bdf8]{ch}[/]")
            else:
                rendered_chars.append(f"[#94a3b8]{ch}[/]")

        # Handle any extra typed characters past target length
        if cursor_pos > target_len:
            for extra_char in typed_text[target_len:]:
                rendered_chars.append(f"[bold #dc2626 underline]{extra_char}[/]")

        content = "".join(rendered_chars)
        metrics = self.session.metrics

        # Status bar
        if self.session.lifecycle == SessionLifecycle.ABORTED:
            status_bar = "[bold #ef4444]TEST ABORTED[/]  •  [dim]Press [bold #38bdf8]Ctrl+R[/] to restart[/]"
        else:
            status_bar = (
                f"[bold #0284c7]WPM:[/] [bold #f8fafc]{metrics.wpm:4.0f}[/]   "
                f"[bold #0284c7]ACC:[/] [bold #f8fafc]{metrics.accuracy:3.0f}%[/]   "
                f"[bold #0284c7]RAW:[/] [bold #94a3b8]{metrics.raw_wpm:4.0f}[/]   "
                f"[bold #0284c7]TIME:[/] [bold #94a3b8]{self.session.snapshot.elapsed_time:4.1f}s[/]"
            )

        hints = "[dim]Ctrl+K: Commands  •  Esc: Abort  •  Ctrl+R: Restart  •  Ctrl+Q: Quit[/]"

        return f"{config_bar}\n\n{content}\n\n\n{status_bar}\n\n{hints}\n"
