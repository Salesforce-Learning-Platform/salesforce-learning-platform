# 🎁 Decorator Pattern

## The Problem: "Combinatorial Explosion" Through Inheritance

```python
# WITHOUT Decorator - a NEW subclass for every COMBINATION of
# features, which grows COMBINATORIALLY as more features are added
class Notifier: ...
class EncryptedNotifier(Notifier): ...
class CompressedNotifier(Notifier): ...
class EncryptedCompressedNotifier(Notifier): ...   # a THIRD class,
                                                       # just for ONE
                                                       # combination
```

```
Adding just ONE more optional feature (e.g. logging) DOUBLES the
number of subclasses needed to cover every possible combination -
this is precisely the "combinatorial explosion of subclasses"
Refactoring.guru's own documentation names directly.
```

This is exactly the notification-library example already referenced in
[Open-Closed Principle](../solid-principles/open-closed-principle.md), earlier in this domain —
inheritance is genuinely the wrong tool here, since the number of needed subclasses grows far faster
than the number of actual features.

## The Pattern: Wrapping, Not Subclassing

```python
class Notifier:
    def send(self, message: str): raise NotImplementedError

class BasicNotifier(Notifier):
    def send(self, message: str): print(f"Sending: {message}")

class NotifierDecorator(Notifier):
    def __init__(self, wrapped: Notifier):
        self._wrapped = wrapped
    def send(self, message: str):
        self._wrapped.send(message)

class EncryptionDecorator(NotifierDecorator):
    def send(self, message: str):
        encrypted = f"[encrypted]{message}"
        self._wrapped.send(encrypted)   # delegates to whatever it wraps

class CompressionDecorator(NotifierDecorator):
    def send(self, message: str):
        compressed = f"[compressed]{message}"
        self._wrapped.send(compressed)
```

```python
notifier = CompressionDecorator(EncryptionDecorator(BasicNotifier()))
notifier.send("Hello!")   # compressed AND encrypted - achieved by
                            # LAYERING two independent decorators,
                            # no new "EncryptedCompressedNotifier"
                            # class needed at all
```

Each decorator implements the *same* `Notifier` interface, wraps another `Notifier`, and adds its
own behavior before delegating onward — any combination of decorators can be composed together, at
runtime, without a single new subclass for each possible pairing.

## A Real, Physical Analogy: Layers of Clothing

```
Wearing a sweater, then a jacket, then a raincoat, adds
capabilities in LAYERS - each garment WRAPS around you, each adds
its OWN function (warmth, wind resistance, waterproofing),
without changing WHO you fundamentally are underneath.
```

This is directly Refactoring.guru's own real-world analogy — genuinely capturing the pattern's
essence: each decorator layer is independent, composable, and adds its own specific capability on
top of whatever it wraps.

## Why This Directly Solves the Open-Closed Violation

```
Adding a NEW optional feature (e.g. logging) means adding ONE new
decorator class - EVERY existing decorator, and the base
BasicNotifier, remain completely untouched.
```

This is a direct, concrete extension of
[Open-Closed](../solid-principles/open-closed-principle.md)'s principle, earlier in this domain —
Decorator is, in a genuine sense, the structural pattern for achieving open-for-extension,
closed-for-modification specifically when the "extension" in question is *optional, composable
behavior* rather than an entirely new type.

## Common Mistakes

- Reaching for subclassing when a genuinely optional, combinable feature is needed, hitting exactly
  the combinatorial-explosion problem Decorator exists to solve.
- Building decorators that depend on a *specific* concrete wrapped type rather than the shared
  interface, losing the ability to compose them in arbitrary order.
- Confusing Decorator's behavior-extension purpose with Proxy's access-control purpose, despite
  their structurally similar "wrapping" shape (per [proxy-pattern.md](proxy-pattern.md)).

## ➡️ Next

Continue to [composite-pattern.md](composite-pattern.md) to see a structural pattern for treating
individual objects and groups of objects uniformly.
