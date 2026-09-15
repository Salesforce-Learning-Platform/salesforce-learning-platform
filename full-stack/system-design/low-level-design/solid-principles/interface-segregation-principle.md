# 4️⃣ Interface Segregation Principle

## The Principle, Stated Precisely

```
"No class should be forced to depend on methods it does not use."
```

This addresses a genuinely different problem than
[Liskov Substitution](liskov-substitution-principle.md) — ISP isn't about whether a subclass can
correctly *replace* its parent; it's about whether an interface itself is well-shaped in the first
place, or bundles together unrelated capabilities that force implementers to support things they
genuinely don't need.

## Before: One Large, "Fat" Interface

```python
class Worker:
    def work(self): raise NotImplementedError
    def eat(self): raise NotImplementedError
    def sleep(self): raise NotImplementedError

class HumanWorker(Worker):
    def work(self): print("Working...")
    def eat(self): print("Eating lunch...")
    def sleep(self): print("Sleeping...")

class RobotWorker(Worker):
    def work(self): print("Working...")
    def eat(self):
        raise NotImplementedError("Robots don't eat!")   # forced,
    def sleep(self):                                       # meaningless
        raise NotImplementedError("Robots don't sleep!")   # implementation
```

`RobotWorker` is forced to implement `eat()` and `sleep()` — methods that are genuinely meaningless
for it — purely because they happen to be bundled into the same `Worker` interface as `work()`,
which it *does* genuinely need.

## Why This Is a Real, Practical Problem

```
Any code calling worker.eat() has NO WAY to know, just from the
Worker interface itself, whether that call will actually SUCCEED
or throw an exception - the interface makes a PROMISE ("every
Worker can eat") that ISN'T actually true for every implementer.
```

This directly connects back to [Liskov Substitution](liskov-substitution-principle.md) — a
`RobotWorker` that throws on `eat()` is *also* an LSP violation, but the *root cause* here is
different: the interface itself was poorly shaped from the start, bundling unrelated capabilities
together.

## After: Smaller, Focused Interfaces

```python
class Workable:
    def work(self): raise NotImplementedError

class Eatable:
    def eat(self): raise NotImplementedError

class Sleepable:
    def sleep(self): raise NotImplementedError

class HumanWorker(Workable, Eatable, Sleepable):
    def work(self): print("Working...")
    def eat(self): print("Eating lunch...")
    def sleep(self): print("Sleeping...")

class RobotWorker(Workable):   # implements ONLY what it genuinely needs
    def work(self): print("Working...")
```

`RobotWorker` now implements only `Workable` — the one capability it genuinely has — with no forced,
meaningless implementations of `eat()` or `sleep()` at all. Each interface makes a narrow, *honest*
promise that every implementer can genuinely keep.

## The Direct Connection to Open-Closed

```
Smaller, focused interfaces also make future EXTENSION cleaner -
adding a "Learnable" capability for SOME workers (but not all)
means adding ONE new, small interface, never touching the
EXISTING Workable/Eatable/Sleepable interfaces at all - directly
the Open-Closed Principle, applied at the interface level.
```

## Common Mistakes

- Designing one large, "convenient" interface bundling every capability a system might ever need,
  rather than smaller, genuinely cohesive ones.
- Implementing a method that throws `NotImplementedError` as a routine, accepted pattern instead of
  a clear signal that the interface itself needs to be split.
- Over-segregating into interfaces so narrow (one method each, with no genuine cohesion) that the
  design becomes needlessly fragmented rather than genuinely clearer.

## ➡️ Next

Continue to
[dependency-inversion-principle.md](dependency-inversion-principle.md) for the final SOLID
principle, tying every earlier principle together.
