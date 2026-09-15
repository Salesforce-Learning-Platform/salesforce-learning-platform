# 🏭 Factory Method Pattern

## The Problem: Creation Logic Tangled With Business Logic

```python
# WITHOUT Factory Method - the caller must know EVERY concrete
# class and pick the right one itself
if platform == "windows":
    button = WindowsButton()
elif platform == "web":
    button = HTMLButton()
```

Scattering this kind of concrete-type-selection logic across a codebase directly violates
[Open-Closed](../solid-principles/open-closed-principle.md), covered earlier in this domain — every
new platform requires finding and modifying every place this `if/elif` chain appears.

## The Pattern

```python
class Dialog:
    def create_button(self):   # the FACTORY METHOD
        raise NotImplementedError

    def render(self):
        button = self.create_button()   # doesn't know or care WHICH
        button.render()                  # concrete type it actually got

class WindowsDialog(Dialog):
    def create_button(self):
        return WindowsButton()

class WebDialog(Dialog):
    def create_button(self):
        return HTMLButton()
```

Per Refactoring.guru's own definition: the pattern "provides an interface for creating objects in a
superclass, but allows subclasses to alter the type of objects that will be created." `Dialog.render()`
works with the abstract `Button` interface, entirely unaware of which concrete button type
`create_button()` actually returns — each subclass decides that independently.

## A Real Use Case: Cross-Platform UI Rendering

```
A UI framework's Dialog needs a DIFFERENT concrete button
implementation depending on the platform it's actually running
on - WindowsDialog returns a real WindowsButton, WebDialog
returns a real HTMLButton - while the SHARED render() logic in
Dialog never needs platform-specific code at all.
```

This is directly the same real-world example Refactoring.guru's own documentation uses — a
genuinely common, practical need: the *what to create* decision varies by context, while the *what
to do with it once created* logic stays entirely shared and unchanged.

## Why This Is Genuinely an Open-Closed Application

```
Adding a NEW platform (e.g. MacDialog) means adding ONE new
subclass - the EXISTING Dialog.render() method, and every OTHER
existing Dialog subclass, remain completely untouched.
```

This is a direct, concrete instance of
[Open-Closed](../solid-principles/open-closed-principle.md)'s own principle, applied specifically to
object *creation* — the Factory Method pattern is, in a genuine sense, simply OCP applied to the
question "which concrete class should be instantiated here?"

## Common Mistakes

- Reaching for Factory Method when there's only ever going to be one, single concrete type — the
  pattern's value comes specifically from supporting multiple, varying implementations.
- Putting genuine business logic inside the factory method itself, rather than keeping it focused
  purely on the creation decision.
- Confusing Factory Method (creating ONE product, decided by a subclass) with Abstract Factory
  (creating a whole FAMILY of related products) — covered next, a genuinely distinct pattern despite
  the similar name.

## ➡️ Next

Continue to [abstract-factory-pattern.md](abstract-factory-pattern.md) to see how this pattern
extends to creating entire families of related objects together.
