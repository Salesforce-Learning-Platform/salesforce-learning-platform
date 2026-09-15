# 🧩 Structural Design Patterns

## 📚 Overview

Following [Creational Design Patterns](../creational-design-patterns/)'s coverage of object
creation, this module covers **structural patterns**: how existing objects and classes are composed
together into larger structures. All five classic patterns — Adapter, Facade, Proxy, Decorator, and
Composite — are covered with a real, verified use case, including the precise distinctions between
commonly-confused pairs (Adapter vs. Facade, Proxy vs. Decorator).

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Use Adapter to make two genuinely incompatible interfaces work together without modifying either.
- Use Facade to simplify access to a genuinely complex subsystem, and distinguish it from Adapter.
- Use Proxy to control access to an object, and distinguish it precisely from Decorator.
- Use Decorator to add optional, composable behavior without combinatorial subclass explosion.
- Use Composite to treat individual objects and groups uniformly through a shared, recursive
  interface.

## 📋 Prerequisites

- [Creational Design Patterns](../creational-design-patterns/) and [SOLID Principles](../solid-principles/) — this module's patterns build directly on both.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [adapter-pattern.md](adapter-pattern.md) | Translating incompatible interfaces, with the canonical power-plug analogy |
| [facade-pattern.md](facade-pattern.md) | Simplifying a complex subsystem, distinguished from Adapter |
| [proxy-pattern.md](proxy-pattern.md) | Controlling access (lazy-loading, caching, permissions), distinguished from Decorator |
| [decorator-pattern.md](decorator-pattern.md) | Composable, optional behavior via layered wrapping, solving combinatorial subclass explosion |
| [composite-pattern.md](composite-pattern.md) | Uniform treatment of individuals and groups via a recursive tree structure; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you're building anything involving third-party integration (Adapter), a complex
internal subsystem (Facade), controlled resource access (Proxy), optional feature composition
(Decorator), or hierarchical data (Composite) — each pattern maps to a genuinely common real-world
need.

**Skim** if you already confidently distinguish Adapter from Facade and Proxy from Decorator — these
two pairs are the module's most commonly confused distinctions, worth double-checking even with
prior pattern experience.

## 🧠 Knowledge Check

<details>
<summary>What's the precise difference between Adapter and Facade, given that both "wrap" something?</summary>

Adapter solves an *incompatibility* problem — translating one existing interface into a different
one so two things that don't naturally fit together can work together, typically wrapping one
object. Facade solves a *complexity* problem — providing a simpler interface to a genuinely complex
subsystem, typically wrapping many objects together. The purposes are genuinely different even
though the structural shape (wrapping) looks similar.

</details>

<details>
<summary>Why can a Proxy choose not to forward a call to the real object, while a Decorator cannot?</summary>

Proxy's entire purpose is controlling access — it may legitimately reject a call (an unauthorized
request, a cache hit that doesn't need to reach the real object). Decorator's purpose is extending
behavior around a call that will always still genuinely happen — every decorator ultimately
delegates to what it wraps, adding capability rather than gatekeeping access.

</details>

## 📚 References

- [Refactoring.Guru - Adapter](https://refactoring.guru/design-patterns/adapter), [Decorator](https://refactoring.guru/design-patterns/decorator), [Composite](https://refactoring.guru/design-patterns/composite) — widely-referenced explanations with real-world examples for each pattern in this module

## ➡️ Continue Your Learning Path

Continue to [Behavioral Design Patterns](../behavioral-design-patterns/) to see patterns focused on
how objects communicate and distribute responsibility for behavior.
