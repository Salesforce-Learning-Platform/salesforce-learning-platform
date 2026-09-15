# 🎭 Behavioral Design Patterns

## 📚 Overview

Completing this domain's design-pattern coverage after [Creational](../creational-design-patterns/)
and [Structural](../structural-design-patterns/) patterns, this module covers **behavioral
patterns**: how objects communicate and distribute responsibility for behavior. All five patterns —
Observer, Strategy, State, Command, and Template Method — are covered with a real, verified use
case, including the precise distinctions between commonly-confused pairs (Strategy vs. State,
Template Method vs. Strategy).

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Use Observer to notify a dynamic, unknown set of subscribers about state changes.
- Use Strategy to swap between independent, interchangeable algorithms at runtime.
- Use State to let an object's behavior change based on its own internal state, with states aware
  of each other's transitions.
- Use Command to turn a request into a genuine object, enabling queuing, logging, and undo/redo.
- Use Template Method to fix a shared algorithm's sequence once, letting subclasses implement only
  the steps that genuinely differ.

## 📋 Prerequisites

- [Creational Design Patterns](../creational-design-patterns/) and [Structural Design Patterns](../structural-design-patterns/) — this module completes the same pattern-based vocabulary.
- [SOLID Principles](../solid-principles/) — Strategy and Template Method both directly apply Open-Closed to algorithm variation.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [observer-pattern.md](observer-pattern.md) | A publisher notifying a dynamic set of subscribers, the pattern behind event listeners |
| [strategy-pattern.md](strategy-pattern.md) | Client-chosen, independent, interchangeable algorithms |
| [state-pattern.md](state-pattern.md) | Behavior that changes with internal state, with states aware of each other |
| [command-pattern.md](command-pattern.md) | Turning a request into an object, enabling undo/redo |
| [template-method-pattern.md](template-method-pattern.md) | A fixed algorithm skeleton with subclass-implemented steps; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you're building anything with event-driven behavior (Observer), interchangeable
algorithms (Strategy), state machines (State), undoable actions (Command), or repeated-but-varying
processing steps (Template Method) — each pattern maps to a genuinely common real-world need.

**Skim** only if you already confidently distinguish Strategy from State and Template Method from
Strategy — these are the module's two most commonly confused pairs, worth a second look even with
prior experience.

## 🧠 Knowledge Check

<details>
<summary>Why can a State pattern's concrete states reference each other, while a Strategy pattern's concrete strategies deliberately cannot?</summary>

State's core feature is that each state can trigger a transition to a different state by directly
assigning the context's current state — this genuinely requires each state class to know about and
reference other state classes. Strategy's concrete strategies are deliberately independent and
unaware of each other, since the *client* — not the strategy itself — decides which one to use and
when to switch.

</details>

<details>
<summary>Why is Template Method described as static (inheritance-based) while Strategy is described as dynamic (composition-based)?</summary>

Template Method fixes an algorithm's overall sequence in a base class at the class-definition level
— a subclass's specific steps are determined by which class it is, decided once. Strategy holds a
reference to a strategy *object* that can be swapped out at runtime, letting the same context object
use a completely different algorithm from one moment to the next without any change to its class.

</details>

## 📚 References

- [Refactoring.Guru - Observer](https://refactoring.guru/design-patterns/observer), [Strategy](https://refactoring.guru/design-patterns/strategy), [State](https://refactoring.guru/design-patterns/state), [Command](https://refactoring.guru/design-patterns/command), [Template Method](https://refactoring.guru/design-patterns/template-method) — widely-referenced explanations with real-world examples for each pattern in this module

## ➡️ Continue Your Learning Path

Continue to [LLD Problem Solving and Machine Coding](../lld-problem-solving-and-machine-coding/),
the final module in this domain, to apply every pattern and principle covered so far to complete,
realistic design problems.
