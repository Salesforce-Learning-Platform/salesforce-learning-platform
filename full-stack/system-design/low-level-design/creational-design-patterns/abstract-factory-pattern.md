# 🏗️ Abstract Factory Pattern

## Factory Method's Bigger Sibling

[factory-pattern.md](factory-pattern.md) covered creating *one* product whose concrete type varies.
**Abstract Factory** addresses a related but genuinely larger problem: creating an entire *family*
of related products that must all be *consistent* with each other.

## The Problem: Consistency Across Multiple Related Objects

```python
# WITHOUT Abstract Factory - genuinely easy to accidentally MIX
# Windows and Mac components in the same UI
button = WindowsButton()
dialog = MacDialog()          # a MISMATCHED, inconsistent pairing -
text_field = WindowsTextField()  # nothing PREVENTS this mistake
```

Using [Factory Method](factory-pattern.md) alone for each individual component (a button factory, a
dialog factory, a text-field factory, each independent) leaves nothing structurally preventing an
accidental, inconsistent mix — genuinely easy to create a UI with a Windows button next to a
Mac-styled dialog.

## The Pattern

```python
class UIFactory:   # the ABSTRACT FACTORY
    def create_button(self): raise NotImplementedError
    def create_dialog(self): raise NotImplementedError
    def create_text_field(self): raise NotImplementedError

class WindowsUIFactory(UIFactory):
    def create_button(self): return WindowsButton()
    def create_dialog(self): return WindowsDialog()
    def create_text_field(self): return WindowsTextField()

class MacUIFactory(UIFactory):
    def create_button(self): return MacButton()
    def create_dialog(self): return MacDialog()
    def create_text_field(self): return MacTextField()

def build_ui(factory: UIFactory):
    return factory.create_button(), factory.create_dialog(), factory.create_text_field()
```

```python
build_ui(WindowsUIFactory())   # guaranteed ALL-Windows components
build_ui(MacUIFactory())        # guaranteed ALL-Mac components
```

Per Refactoring.guru's own definition, Abstract Factory produces entire families of related objects
together — `build_ui` receives *one* factory, and every product it creates through that single
factory is guaranteed to belong to the same, consistent family, structurally preventing the
mismatch the naive approach allowed.

## A Real Use Case: Cross-Platform UI Frameworks

```
A cross-platform UI framework needs COORDINATED sets of
components - buttons, dialogs, text fields - all styled
CONSISTENTLY for the SAME target platform. An AbstractUIFactory
interface, with a WindowsUIFactory and MacUIFactory implementation
EACH producing an entire matching family, ensures visual
consistency across the whole application.
```

This is directly the real-world justification from Refactoring.guru's own documentation — the
pattern earns its added structure (relative to plain Factory Method) specifically when *consistency
across multiple related objects* genuinely matters, not merely when multiple types need creating
independently.

## Recognizing When You've Actually Outgrown Factory Method

```
Multiple INDEPENDENT products, each varying on its own → Factory
  Method per product is often sufficient

Multiple RELATED products that must be CONSISTENT with each
  other (all from the "same family") → Abstract Factory
```

This is a genuinely useful practical signal for choosing between the two related patterns — the
deciding question is whether the products need to be *coordinated*, not merely whether more than
one type of product exists.

## Common Mistakes

- Reaching for Abstract Factory when the products created don't actually need to stay consistent
  with each other, adding unnecessary structure over plain Factory Method.
- Allowing product creation to bypass the abstract factory interface in some code paths, silently
  reopening the exact inconsistent-mixing risk this pattern exists to prevent.
- Confusing this pattern's genuine complexity increase as inherently "better" than Factory Method,
  rather than a deliberate trade-off justified specifically by the consistency requirement.

## ➡️ Next

Continue to [builder-pattern.md](builder-pattern.md) to see the pattern for constructing a single,
complex object step by step.
