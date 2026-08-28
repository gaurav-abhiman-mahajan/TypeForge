from dataclasses import replace
from app.models.typing import TypingState
from app.models.events import Event, CharacterTyped, BackspacePressed


class StateTransitionEngine:
    def _process_char(self, state: TypingState, char: str) -> TypingState:
        """Handles character transition."""
        if len(char) != 1:
            raise ValueError("Only a single character allowed to be typed")

        return replace(state, typed=state.typed + char)

    def _process_backspace(self, state: TypingState) -> TypingState:
        """Handles backspace transition."""
        if not state.typed:
            return state

        return replace(state, typed=state.typed[:-1])

    def process_event(
        self,
        state: TypingState,
        event: Event,
    ) -> TypingState:
        match event:
            case CharacterTyped(char):
                return self._process_char(state, char)
            case BackspacePressed():
                return self._process_backspace(state)

        return state
