# TypeForge Domain

TypeForge describes terminal-native typing practice and synchronous typing competition. This glossary keeps local practice, individual performance, and multiplayer competition distinct.

## People and identity

**Typist**:
A person who practices or competes by typing a presented text.
_Avoid_: User, player when no competition is involved

**Local Profile**:
A typist's identity, preferences, and practice history available without an online account.
_Avoid_: Guest account, offline account

**Account**:
An authenticated online identity used to synchronize a Local Profile and enter competition.
_Avoid_: Profile, login

**Typing Profile**:
The detailed model of a typist's habits and performance derived from synchronized Attempt histories.
_Avoid_: Account, Local Profile, statistics

## Typing activity

**Test**:
A configured typing challenge defined by its mode, rules, content, and completion limit.
_Avoid_: Session, game

**Test Mode**:
The completion model of a Test: Time, Words, Quote, Zen, or Custom.
_Avoid_: Test type, content type

**Content Set**:
A named source of text from which a Test is constructed, such as an English word list or Python code corpus.
_Avoid_: Language when the content is not a natural language, mode

**Rule Set**:
The immutable typing and scoring rules applied to an Attempt.
_Avoid_: Settings, difficulty

**Attempt**:
One typist's execution of a Test from start until completion or abandonment.
_Avoid_: Test, session, run

**Attempt Record**:
The durable chronological evidence of an Attempt, including every typing, editing, lifecycle, and timing event.
_Avoid_: Result, replay, event history

**Result**:
The final measured outcome of an Attempt.
_Avoid_: Metrics, score

**Correction**:
An edit that changes previously entered text without erasing the original input from an Attempt's history.
_Avoid_: Error, Backspace

**Keystroke Accuracy**:
The proportion of evaluable typing inputs that were correct when entered, including mistakes later corrected.
_Avoid_: Final-text correctness, word accuracy

**Qualified Speed**:
Typing speed credited only for text that satisfies the Test's correctness rules.
_Avoid_: Raw Speed, WPM when the qualification rule is unclear

**Raw Speed**:
Typing speed measured from all entered text regardless of correctness.
_Avoid_: Qualified Speed, gross score

**Character Outcome**:
The final classification of a target or entered character as correct, incorrect, extra, or missed.
_Avoid_: Keystroke Accuracy, error history

**Practice Run**:
A locally initiated sequence of one or more Attempts undertaken for practice.
_Avoid_: Session, match

**Practice Program**:
A strategy that selects Tests to develop a specific typing skill or address observed weaknesses.
_Avoid_: Test Mode, difficulty

## Competition

**Match**:
An authenticated online competition in which multiple typists perform the same Test under shared timing and rules.
_Avoid_: Session, lobby, game

**Race**:
The synchronous competitive format of a Match, including a shared start and live relative progress toward final placement.
_Avoid_: Match, challenge

**Matchmaking**:
The public process that forms a Match from authenticated typists of comparable competitive skill.
_Avoid_: Lobby, private room, queue

**Competitive Playlist**:
A platform-defined Test and Rule Set used to form comparable Matches and maintain a distinct skill rating.
_Avoid_: Test Mode, Matchmaking queue, user preset

**Skill Rating**:
A playlist-specific estimate of competitive ability derived from Match placement and opponent strength.
_Avoid_: WPM, personal best, account level

**Placement**:
A typist's ordered finishing position within a Match.
_Avoid_: Result, Skill Rating, score

**Forfeit**:
A competitive loss caused by abandoning a started Match or failing to reconnect within its allowed window.
_Avoid_: Failed Attempt, disconnection

**Match Authority**:
The online source of truth for a Match's Test, Rule Set, timing, accepted evidence, Placement, and rating outcome.
_Avoid_: Match server, client clock

**Match Summary**:
The public competitive record of a Match's playlist, participants, Placements, Results, and rating changes.
_Avoid_: Attempt Record, Result
