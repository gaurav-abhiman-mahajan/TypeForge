from dataclasses import dataclass, field, replace


@dataclass(frozen=True)
class BehaviorPolicy:
    allow_leading_spaces: bool = False
    allow_consecutive_spaces: bool = False
    allow_backspace: bool = True
    allow_quit: bool = True


@dataclass(frozen=True)
class ConstraintPolicy:
    stop_on_character_errors: bool = False
    min_wpm_speed: float | None = None


@dataclass(frozen=True)
class TypingPolicy:
    behavior: BehaviorPolicy = field(default_factory=BehaviorPolicy)
    constraints: ConstraintPolicy = field(default_factory=ConstraintPolicy)

    @property
    def allow_leading_spaces(self) -> bool:
        return self.behavior.allow_leading_spaces

    @property
    def allow_consecutive_spaces(self) -> bool:
        return self.behavior.allow_consecutive_spaces

    @property
    def allow_backspace(self) -> bool:
        return self.behavior.allow_backspace

    @property
    def allow_quit(self) -> bool:
        return self.behavior.allow_quit

    @property
    def stop_on_character_errors(self) -> bool:
        return self.constraints.stop_on_character_errors

    @property
    def min_wpm_speed(self) -> float | None:
        return self.constraints.min_wpm_speed


DEFAULT_BEHAVIOR = BehaviorPolicy(
    allow_leading_spaces=False,
    allow_consecutive_spaces=False,
    allow_backspace=True,
    allow_quit=True,
)

DEFAULT_CONSTRAINTS = ConstraintPolicy(
    stop_on_character_errors=False,
    min_wpm_speed=None,
)

DEFAULT_POLICY = TypingPolicy(behavior=DEFAULT_BEHAVIOR, constraints=DEFAULT_CONSTRAINTS)
REGULAR = DEFAULT_POLICY

HARD = TypingPolicy(
    behavior=DEFAULT_BEHAVIOR,
    constraints=replace(DEFAULT_CONSTRAINTS, stop_on_character_errors=True),
)

EXPERT = TypingPolicy(
    behavior=replace(DEFAULT_BEHAVIOR, allow_backspace=False),
    constraints=ConstraintPolicy(
        stop_on_character_errors=True,
        min_wpm_speed=60.0,
    ),
)


def update_policy(policy: TypingPolicy, **changes) -> TypingPolicy:
    return replace(policy, **changes)


def setup_policy(
    allow_backspace: bool = True,
    allow_quit: bool = True,
    allow_leading_spaces: bool = False,
    allow_consecutive_spaces: bool = False,
    stop_on_character_errors: bool = False,
    min_wpm_speed: float | None = None,
) -> TypingPolicy:
    return TypingPolicy(
        behavior=BehaviorPolicy(
            allow_leading_spaces=allow_leading_spaces,
            allow_consecutive_spaces=allow_consecutive_spaces,
            allow_backspace=allow_backspace,
            allow_quit=allow_quit,
        ),
        constraints=ConstraintPolicy(
            stop_on_character_errors=stop_on_character_errors,
            min_wpm_speed=min_wpm_speed,
        ),
    )
