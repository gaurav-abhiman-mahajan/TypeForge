# TypeForge
A terminal typing game/tool that tests wpm for the user. 

## Version 1 Scope

Metrics <-> Modes <-> UI <-> Loop 

### Core loop

```
mermaid
flowchart TD
  A[Choose mode]
  B[Choose configuration]
  C[Typing test]
  D[Live Metrics]
  E[Result]
  F[Try again / Choose configuration / Quit]
  
  A ---o B
  B ---o C
  C ---o D
  D ---o E
  E ---o F
  F ---o A
```

### Metrics
* typing
  1. WPM - correct characters / 5 / elapsed time
  2. Raw WPM - typed characters / 5 / elapsed time
  3. CPM - correct characters / elapsed time
  4. Raw CPM - typed characters / elapsed time

* accuracy
  1. percentage correct characters - correct characters / typed characters * 100
  2. percentage correct words - (correct characters / 5) / (typed characters / 5) * 100
  3. words - correct and incorrect words
  4. characters - correct and incorrect characters

* completion / error
  1. completed words - `hello` (incomplete) v.s. `hello ` (complete)
  2. word errors - include incomplete words / words with wrong characters
  3. character errors - map out the most frequent error prone characters

* timing
  1. completion time
  2. time afk

* consistency
  ...

### Modes
* timed
  1. 15 secs
  2. 30 secs
  3. 60 secs
  4. 120 secs
  5. infinite - requires explicit stop event for the session to end

* words
word count derived from .json files
  1. 10 words
  2. 25 words
  3. 50 words
  4. 100 words

* quote
  1. pre-saved quotes

* book
  1. paragraphs from books

* practise
  1. incorrect words - most frequently typed incorrect words
  2. incorrect characters - words containing/starting most frequently typed incorrect characters

### Difficulty
difficulty affects the expected maintained metrics
  1. regular - no restricitons 
  2. hard - shoud maintain 0 errors
  3. expert - should maintain 100% word accuracy + wpm should not fall below 50 wpm - no backspace

### Punctuation
  1. on / off - `?!.,'";:-`

### Numbers
  1. on / off - 0123456789

### Language
  1. English

### Behaviours
  1. leading space
  2. backspace
  3. quiting 
  4. consequtive spacing

### Theme
  1. black
  2. white

## Settings / configuration
  Settings
  ├── mode
  ├── duration 
  ├── word_count
  ├── language
  ├── punctuation
  ├── numbers
  ├── difficulty
  ├── theme
  └── behaviours

## Internal settings orchestrator / validator
This ensures that mode, difficulty and behaviours are set according to each other and 
opting for one thing can disable you from chaning another



## Example UI reference (not the actual version 1 look)
### Home screen
┌──────────────────────────────────────────────┐
│                 TYPEFORGE                    │
│                                              │
│  [ Start Typing ]                            │
│                                              │
│  Mode       Time                             │
│  Duration   30s                              │
│  Language   English                          │
│  Words      1K                               │
│  Punctuation Off                             │
│  Numbers     Off                             │
│                                              │
│  Settings                         q Quit     │
└──────────────────────────────────────────────┘

### Typing screen
┌──────────────────────────────────────────────┐
│                                              │
│  the quick brown fox jumps over the lazy     │
│  dog and runs across the street...           │
│                                              │
│                                              │
│  WPM       74       Accuracy     96%         │
│  Time      21.4s    Errors       3           │
│                                              │
└──────────────────────────────────────────────┘

### Result screen
┌──────────────────────────────────────────────┐
│                 RESULT                       │
│                                              │
│              74 WPM                          │
│                                              │
│ Accuracy              96%                    │
│ Gross WPM             78                     │
│ CPM                   390                    │
│ Correct characters    235                    │
│ Errors                 10                    │
│ Backspaces              6                    │
│ Time                  30.2s                  │
│ Words completed        47                    │
│                                              │
│ [ Try Again ]   [ Change Mode ]   [ Quit ]   │
└──────────────────────────────────────────────┘

## Session snapshot
  session
  |--mode
  |--duration / word_count
  |--target / content metadata
  |--start time
  |--end time
  |--duration
  |--metrics (wpm, cpm, raw wpm, raw cpm)
  |--accuracy (correct/incorrect words/characters, percentages)

## Errors record
  1. CharacterErrorRecord:
    character -> frequency | last recorded
  2. WordErrorRecord:
    word -> frequency | last recorded

## Preference / Settings
Settings object persisted

## Persistence
**JSON** / **SQLite** help create persistence record:
  1. sessions
  2. settings / preference
  3. error record

Possible repository stored at: ~/.cache/typeforge/


## Core engine loop:

```
mermaid
---
config:
  layout: elk
---
flowchart TD
    incomingEvent[Incoming Event]
    isValid{Is Valid?}
    transitionState[Transition State]
    quit[Quit]
    
    incomingEvent --> isValid
    isValid -->|Yes| transitionState
    transitionState --> incomingEvent
    isValid -->|No| quit
```



