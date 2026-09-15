# 🔤 SOLID Principles

## 📚 Overview

Building directly on [LLD Foundations](../lld-foundations/)'s object-oriented vocabulary, this
module covers the five SOLID principles — Single Responsibility, Open-Closed, Liskov Substitution,
Interface Segregation, and Dependency Inversion — coined by Robert C. Martin. Each addresses a
genuinely different way a class's design can go wrong, with a concrete before/after example
throughout.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Identify when a class has more than one genuine reason to change, and split it accordingly.
- Design new behavior as new classes implementing a shared interface, rather than modifying
  existing code.
- Recognize when an inheritance relationship isn't genuinely behaviorally substitutable, even when
  it seems intuitively correct.
- Split a "fat" interface into smaller, focused ones so no implementer is forced to support
  capabilities it doesn't have.
- Apply dependency injection so high-level code depends on abstractions, not concrete
  implementation details.

## 📋 Prerequisites

- [LLD Foundations](../lld-foundations/) — every SOLID principle in this module builds directly on the object-oriented vocabulary established there.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [single-responsibility-principle.md](single-responsibility-principle.md) | One class, one reason to change — with a before/after order-processing example |
| [open-closed-principle.md](open-closed-principle.md) | Extension through new classes, never modification of existing ones |
| [liskov-substitution-principle.md](liskov-substitution-principle.md) | The classic Rectangle/Square violation, and genuine behavioral substitutability |
| [interface-segregation-principle.md](interface-segregation-principle.md) | Splitting a "fat" interface so implementers aren't forced into meaningless methods |
| [dependency-inversion-principle.md](dependency-inversion-principle.md) | Both high- and low-level code depending on a shared abstraction, via dependency injection; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** regardless of prior OOP experience — SOLID is foundational vocabulary the Creational,
Structural, and Behavioral Design Patterns modules, later in this domain, assume throughout.

**Skim** only if you can already confidently explain and apply all five principles from memory —
but the Liskov Substitution file's Rectangle/Square example is worth a second look even then, since
it's commonly misunderstood.

## 🧠 Knowledge Check

<details>
<summary>Why does the classic Rectangle/Square example violate Liskov Substitution, even though a square is mathematically a rectangle?</summary>

LSP requires *behavioral* substitutability, not merely real-world or mathematical "is-a" truth. Code
written correctly against `Rectangle`'s interface (setting width and height independently) breaks
silently when handed a `Square`, because `Square` secretly changes both dimensions together to
maintain its own invariant — a behavior the `Rectangle` interface never promised or accounted for.

</details>

<details>
<summary>What does "inversion" actually refer to in the Dependency Inversion Principle?</summary>

The naive, intuitive dependency direction has high-level business logic depending directly on a
low-level implementation detail. DIP inverts this: both the high-level and low-level code instead
depend on a shared abstraction sitting between them, so neither depends directly on the other —
concretely realized through dependency injection.

</details>

## 📚 References

- [GeeksforGeeks - SOLID Principles](https://www.geeksforgeeks.org/system-design/solid-principle-in-programming-understand-with-real-life-examples/) — a widely-referenced explanation of all five principles with real-world examples

## ➡️ Continue Your Learning Path

Continue to [Creational Design Patterns](../creational-design-patterns/) to see named, proven
solutions to recurring design problems, built directly on these five principles.
