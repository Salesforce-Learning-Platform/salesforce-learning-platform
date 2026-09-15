# ⌘ Command Pattern

## The Problem: Coupling UI Directly to Business Logic

```python
# WITHOUT Command - EVERY button needs to know EXACTLY which
# business logic method to call directly
class SaveButton:
    def on_click(self):
        document_editor.save()   # directly coupled

class SaveMenuItem:
    def on_click(self):
        document_editor.save()   # the SAME logic, duplicated
                                   # in a SECOND place
```

Per Refactoring.guru's own framing: trying to handle every UI trigger through inheritance alone
leads to "an enormous number of subclasses" — and directly coupling every button, menu item, and
keyboard shortcut straight to specific business logic means the *same* operation's invocation logic
gets duplicated everywhere it's triggered from.

## The Pattern: Turning a Request Into an Object

```python
class Command:
    def execute(self): raise NotImplementedError

class SaveCommand(Command):
    def __init__(self, editor):
        self._editor = editor
    def execute(self):
        self._editor.save()

class Button:   # the INVOKER - doesn't know WHAT it triggers,
    def __init__(self, command: Command):   # only THAT it can
        self._command = command
    def click(self):
        self._command.execute()
```

```python
save_button = Button(SaveCommand(document_editor))
save_menu_item = Button(SaveCommand(document_editor))   # the SAME
                                                            # command object,
                                                            # reused
save_button.click()
```

Any UI element (a `Button`) can trigger *any* command, without knowing anything about what that
command actually does — the command object itself encapsulates both the action and the specific
data it needs to perform it.

## A Real Use Case: Undo/Redo

```
BEFORE executing an operation (cut, paste), a Command creates a
BACKUP of the relevant state. After executing, the Command is
pushed onto a HISTORY stack. Undoing means popping the most
RECENT command and restoring ITS OWN backup - the application
itself never needs to know WHICH specific operation is being
undone.
```

This is directly Refactoring.guru's own canonical real-world example — and it's genuinely the
clearest illustration of why turning a request into a full *object* (rather than a plain function
call) matters: an object can carry its own state (the backup), be stored in a history list, and be
"replayed" or reversed later, none of which a bare function call can do on its own.

## Why This Enables Genuinely Powerful Capabilities

```
Because a Command is a genuine OBJECT, not just a function call,
it can be:
  - QUEUED (execute later, or on a different thread)
  - LOGGED (record every command executed, for auditing)
  - UNDONE (per the undo/redo example above)
  - composed into a MACRO (a list of Commands executed together)
```

This is the real, structural payoff — none of these capabilities are available to a plain, direct
method call; they become possible specifically because the request itself is now a first-class
object that can be stored, passed around, and manipulated like any other piece of data.

## Common Mistakes

- Directly coupling multiple UI triggers to the same business logic method, duplicating invocation
  logic across every trigger point instead of sharing one Command object.
- Implementing undo without each Command genuinely capturing enough state to reverse its own
  specific effect.
- Letting a Command's `execute()` method reach far beyond its own focused, single operation, turning
  it into an unfocused catch-all rather than one clean, reusable action.

## ➡️ Next

Continue to [template-method-pattern.md](template-method-pattern.md) for the final behavioral
pattern in this domain.
