# 🚦 State Pattern

## The Problem: Behavior That Genuinely Depends on Internal State

```python
# WITHOUT State - EVERY method needs to check the current state,
# and this REPEATS across every method as more states are added
class Document:
    def publish(self):
        if self.state == "draft":
            self.state = "moderation"
        elif self.state == "moderation":
            self.state = "published"
        elif self.state == "published":
            pass   # already published, do nothing
```

Per Refactoring.guru's own direct framing: "The biggest weakness of a state machine based on
conditionals reveals itself once we start adding more and more states and state-dependent
behaviors" — every single method touching state-dependent behavior needs its own repeated
conditional, and this genuinely compounds as more states and methods are added.

## The Pattern

```python
class DocumentState:
    def publish(self, document): raise NotImplementedError

class DraftState(DocumentState):
    def publish(self, document):
        document.state = ModerationState()

class ModerationState(DocumentState):
    def publish(self, document):
        document.state = PublishedState()

class PublishedState(DocumentState):
    def publish(self, document):
        pass   # already published - genuinely nothing to do

class Document:   # the CONTEXT
    def __init__(self):
        self.state = DraftState()

    def publish(self):
        self.state.publish(self)   # delegates entirely to the
                                     # CURRENT state object
```

```python
doc = Document()
doc.publish()   # Draft -> Moderation
doc.publish()   # Moderation -> Published
```

Each state class knows exactly how `publish()` should behave *for that specific state*, and — this
is the pattern's genuinely distinctive feature — each state can *transition* the context to a
different state itself, by directly reassigning `document.state`.

## A Real Use Case: an Audio Player

```
The SAME "play" button produces GENUINELY different behavior
depending on the player's current state:
  ReadyState  → starts playing music
  PlayingState → pauses playback
  LockedState  → ignores the button entirely (except unlock)
```

This is directly Refactoring.guru's own real-world example — genuinely intuitive, since anyone
who's used a media player has already experienced this exact state-dependent behavior directly.

## The Key Distinction From Strategy, Restated Precisely

```
STRATEGY: the CLIENT explicitly chooses and swaps which algorithm
  to use - concrete strategies never know about each other

STATE: the CURRENT STATE ITSELF decides when and how to
  TRANSITION to a different state - concrete states GENUINELY
  need to know about (and reference) other state classes
```

This is the precise, structural difference worth holding onto from
[strategy-pattern.md](strategy-pattern.md) — in State, `DraftState.publish()` directly creates and
assigns a `ModerationState`, meaning concrete states are genuinely *aware* of each other, unlike
Strategy's deliberately independent, mutually-unaware implementations.

## Common Mistakes

- Keeping state-transition logic scattered across many conditional checks in the context class,
  rather than letting each state class own its own transition logic.
- Confusing State with Strategy simply because both share the same delegation-to-a-held-object
  structural shape, missing that State's implementations are genuinely aware of and reference each
  other.
- Allowing the context class to still contain state-specific `if` checks anywhere, which reopens
  exactly the problem State was introduced to solve.

## ➡️ Next

Continue to [command-pattern.md](command-pattern.md) to see a pattern for turning a request itself
into an object.
