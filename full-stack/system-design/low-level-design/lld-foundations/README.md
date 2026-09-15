# 🏗️ LLD Foundations

## 📚 Overview

This module opens the Low-Level Design domain, establishing the vocabulary and notation every later
module builds on: what LLD actually is (and how it differs from High-Level Design), objects and
classes, the different ways classes can relate to each other, UML notation for visualizing both
structure and behavior, and the principles behind a genuinely clean, well-designed interface.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Distinguish Low-Level Design from High-Level Design.
- Apply the four pillars of object-oriented design: encapsulation, abstraction, inheritance, and
  polymorphism.
- Choose the correct relationship type (association, aggregation, composition, inheritance) for a
  given design, and explain the lifecycle implications of each.
- Read and sketch basic UML class and sequence diagrams.
- Design a class interface that's minimal, clearly named, and fails predictably.

## 📋 Prerequisites

- General programming experience with classes and objects (any language) — this module assumes familiarity with basic OOP syntax, not the underlying design principles themselves.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [what-is-low-level-design.md](what-is-low-level-design.md) | LLD vs. HLD, and why deliberate class design matters beyond "it works" |
| [objects-and-classes.md](objects-and-classes.md) | The four pillars of OOP, with concrete encapsulation and polymorphism examples |
| [relationships-between-objects.md](relationships-between-objects.md) | Association, aggregation, composition, and inheritance, distinguished by lifecycle |
| [uml-basics.md](uml-basics.md) | Class diagrams (structure) and sequence diagrams (behavior), with Mermaid examples |
| [designing-clean-interfaces.md](designing-clean-interfaces.md) | Minimal exposure, clear naming, predictable failure, and dependency on abstractions; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you're new to deliberate object-oriented design, or want a shared vocabulary before
tackling SOLID principles and design patterns — this module is genuinely foundational to the rest
of this domain.

**Skim** if you already have strong OOP design experience — but confirm your understanding of
aggregation vs. composition specifically, since that distinction is easy to get subtly wrong.

## 🧠 Knowledge Check

<details>
<summary>What's the key difference between aggregation and composition, and why does it matter practically?</summary>

Both are "has-a" relationships, but aggregation's parts can exist independently of the whole (an
Employee survives if their Department is deleted), while composition's parts share the whole's
lifecycle (an Engine is destroyed along with its Car). Getting this wrong in practice leads to
either accidentally destroying data that should have survived, or leaving orphaned objects that
should have been cleaned up automatically.

</details>

<details>
<summary>Why does exposing a minimal, deliberate public interface matter more than simply making everything work?</summary>

A smaller public interface means fewer ways for other code to misuse a class or bypass its internal
invariants, and it gives genuine freedom to change the internal implementation later without
breaking anything that depends on the class. A class's public interface is effectively a promise to
every caller — the smaller and clearer that promise, the easier the class is to maintain and extend.

</details>

## 📚 References

- [Miro - Understanding UML Class Diagrams](https://miro.com/diagramming/what-is-a-uml-class-diagram/) — visibility notation and structure
- [GeeksforGeeks - UML Sequence Diagrams](https://www.geeksforgeeks.org/system-design/unified-modeling-language-uml-sequence-diagrams/) — lifelines, messages, and interaction notation

## ➡️ Continue Your Learning Path

Continue to [SOLID Principles](../solid-principles/) to see the design principles that build
directly on this module's foundation.
