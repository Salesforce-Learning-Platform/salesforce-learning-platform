# 🏭 Creational Design Patterns

## 📚 Overview

Building on [SOLID Principles](../solid-principles/), this module covers the first of three design
pattern categories in this domain: **creational patterns**, addressing how objects actually get
created. Each of the five classic Gang-of-Four creational patterns — Singleton, Factory Method,
Abstract Factory, Builder, and Prototype — is covered with a real, verified use case.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Apply Singleton for a genuinely shared resource, while recognizing its global-state trade-off.
- Use Factory Method to let a subclass decide which concrete product to create.
- Distinguish Abstract Factory from Factory Method by whether product consistency across a family
  genuinely matters.
- Build a complex object step by step with Builder's fluent interface.
- Clone an existing object with Prototype, correctly distinguishing shallow from deep copies.

## 📋 Prerequisites

- [SOLID Principles](../solid-principles/) — Factory Method and Abstract Factory are both direct, concrete applications of the Open-Closed Principle covered there.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [singleton-pattern.md](singleton-pattern.md) | Exactly one instance, with a database-connection-pool use case and the global-state trade-off |
| [factory-pattern.md](factory-pattern.md) | A subclass decides the concrete product, with a cross-platform UI example |
| [abstract-factory-pattern.md](abstract-factory-pattern.md) | Creating consistent families of related products together |
| [builder-pattern.md](builder-pattern.md) | Step-by-step construction with a fluent interface, and the optional Director |
| [prototype-pattern.md](prototype-pattern.md) | Cloning instead of building, and the shallow-vs-deep-copy distinction; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you're new to named design patterns — this module establishes the pattern-based
vocabulary the Structural and Behavioral Design Patterns modules, later in this domain, assume.

**Skim** if you already recognize and correctly apply all five creational patterns — but the
Abstract Factory vs. Factory Method distinction is worth a second look, since it's commonly
conflated.

## 🧠 Knowledge Check

<details>
<summary>What's the actual deciding factor for choosing Abstract Factory over plain Factory Method?</summary>

Not simply "there's more than one product type" — the deciding factor is whether the products
created together genuinely need to stay *consistent* with each other (all from the same "family," like
all-Windows or all-Mac UI components). If the products vary independently with no consistency
requirement, Factory Method per product is usually sufficient on its own.

</details>

<details>
<summary>Why can a shallow copy in the Prototype pattern introduce a subtle bug that a deep copy avoids?</summary>

A shallow copy copies the top-level object but leaves nested objects (like a list or another object)
shared by reference between the original and the copy. Modifying the copy's nested data then also
silently modifies the original's — a deep copy recursively copies every nested object, making the
clone genuinely, completely independent.

</details>

## 📚 References

- [Refactoring.Guru - Singleton](https://refactoring.guru/design-patterns/singleton), [Factory Method](https://refactoring.guru/design-patterns/factory-method), [Builder](https://refactoring.guru/design-patterns/builder) — widely-referenced explanations with real-world examples for each pattern in this module

## ➡️ Continue Your Learning Path

Continue to [Structural Design Patterns](../structural-design-patterns/) to see patterns focused on
how objects and classes are composed together, rather than how they're created.
