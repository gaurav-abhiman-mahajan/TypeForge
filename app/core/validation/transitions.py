from app.models.typing import TypingState
from app.core.policies.typing import TypingPolicy
from app.models.events import Event, CharacterTyped, BackspacePressed, EscPressed


def is_valid_transition(
    policy: TypingPolicy, previous_state: TypingState, event: Event
) -> bool:
    match event:
        case CharacterTyped(char):
            if len(char) != 1:
                return False

            if (
                not policy.allow_leading_spaces
                and not previous_state.typed
                and char == " "
            ):
                return False

            if (
                not policy.allow_consecutive_spaces
                and previous_state.typed.endswith(" ")
                and char == " "
            ):
                return False

            if policy.stop_on_character_errors:
                for i, typed_char in enumerate(previous_state.typed):
                    if (
                        i < len(previous_state.target)
                        and typed_char != previous_state.target[i]
                    ):
                        return False

        case BackspacePressed():
            if not policy.allow_backspace:
                return False
            if not previous_state.typed:
                return False

        case EscPressed():
            if not policy.allow_quit:
                return False

    return True
