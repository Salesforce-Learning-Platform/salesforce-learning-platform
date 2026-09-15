# 🧬 Prototype Pattern

## Creating Objects by Cloning, Not Building

Every pattern so far in this module — Singleton, Factory Method, Abstract Factory, Builder — builds
a new object from scratch. **Prototype** takes a genuinely different approach: creating a new
object by *copying* an already-existing one, then modifying only what's actually different.

## The Problem: Expensive or Complex Initialization

```python
class GameCharacter:
    def __init__(self, name, stats, inventory, skill_tree):
        self.name = name
        self.stats = stats                # expensive to compute from scratch
        self.inventory = inventory
        self.skill_tree = skill_tree      # a genuinely complex object graph
```

```
Creating a NEW GameCharacter identical to an EXISTING one, but
with a different name, would normally require RECOMPUTING every
one of these fields from scratch - even though most of them are
IDENTICAL to the original.
```

For an object that's genuinely expensive to construct, or has a deeply nested structure, rebuilding
it from scratch just to get a near-identical copy is wasteful — Prototype avoids this by cloning
directly.

## The Pattern

```python
import copy

class GameCharacter:
    def __init__(self, name, stats, inventory, skill_tree):
        self.name = name
        self.stats = stats
        self.inventory = inventory
        self.skill_tree = skill_tree

    def clone(self):
        cloned = copy.deepcopy(self)   # a DEEP copy - independent of the original
        return cloned
```

```python
original = GameCharacter("Warrior Template", stats={"str": 15}, inventory=[], skill_tree=default_tree)

player_character = original.clone()
player_character.name = "Aldric"   # only the DIFFERENCE is set explicitly
```

`clone()` produces a genuinely independent copy — modifying `player_character` afterward never
affects `original` at all, since `copy.deepcopy()` recursively copies every nested object rather
than merely copying references to the same underlying data.

## Shallow vs. Deep Copy: a Genuinely Important Distinction

```
SHALLOW copy: copies the top-level object, but nested objects
  (like inventory, a list) are SHARED between original and copy -
  modifying the copy's inventory ALSO modifies the original's

DEEP copy: recursively copies EVERY nested object too - the copy
  is GENUINELY, completely independent of the original
```

This distinction is genuinely easy to get wrong in practice — a shallow copy can silently introduce
a bug where modifying what looks like an independent clone actually mutates the original object's
own nested data as well, exactly the kind of hard-to-trace bug that motivates being deliberate about
which copy semantics a `clone()` implementation actually uses.

## A Real Use Case: Object Pools and Templates

```
A game with MANY enemies sharing a mostly-identical base
configuration (stats, default equipment) - a single "template"
prototype is cloned for each new enemy spawned, rather than
reconstructing that same configuration from scratch every time.
```

This is a genuinely common, practical application — anywhere a "template" or "default configuration"
concept exists, Prototype is often the natural fit: clone the template, then customize only the
specific differences for this particular instance.

## Common Mistakes

- Implementing `clone()` as a shallow copy when the object's nested data genuinely needs to be
  independent, causing subtle, hard-to-trace mutation bugs later.
- Reaching for Prototype when object construction is already cheap and simple — the pattern's value
  comes specifically from avoiding genuinely expensive or complex re-initialization.
- Forgetting that a deep copy has its own real performance cost — for a very large, deeply nested
  object graph, cloning isn't automatically free either.

## Module Summary

Across this module: **Singleton** ensures exactly one instance of a genuinely shared, expensive
resource, at the real cost of introducing global state (see
[singleton-pattern.md](singleton-pattern.md)); **Factory Method** lets a subclass decide which
concrete product to create, directly applying Open-Closed to the creation decision itself (see
[factory-pattern.md](factory-pattern.md)); **Abstract Factory** extends this to entire *families*
of related products that must stay consistent with each other (see
[abstract-factory-pattern.md](abstract-factory-pattern.md)); **Builder** constructs a complex object
step by step through a fluent, self-documenting interface, with an optional Director capturing
reusable construction sequences (see [builder-pattern.md](builder-pattern.md)); and **Prototype**
creates new objects by cloning an existing one rather than building from scratch, with the
shallow-vs-deep-copy distinction being the pattern's most important practical detail to get right.
