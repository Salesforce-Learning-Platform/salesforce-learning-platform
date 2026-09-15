# 🏗️ What Is Low-Level Design?

## A New Domain: Designing Before Building

Every domain in this repository so far has focused on *implementing* — writing the actual code for
a feature, a backend, an AI pipeline. **Low-Level Design (LLD)** is a genuinely different, earlier
step: designing a system's actual classes, objects, and their relationships *before* — or while —
writing that implementation, so the resulting code is maintainable, extensible, and genuinely
well-structured rather than accidental.

## Low-Level vs. High-Level Design

```
HIGH-LEVEL DESIGN (HLD) → the BIG picture: which services exist,
  how they communicate, what database technology to use, how the
  system scales (covered in the High-Level Design module, later
  in this domain)

LOW-LEVEL DESIGN (LLD) → the DETAILED picture, WITHIN one
  component: which CLASSES exist, their RESPONSIBILITIES, how
  they RELATE to and communicate with each other
```

This is a genuinely useful distinction to hold onto throughout this entire module: HLD asks "what
are the pieces of the system, and how do they talk to each other?" — LLD asks "within *this one*
piece, what are the actual classes, and how are *they* structured?"

## Why This Matters Beyond "It Compiles and Works"

```
Code that WORKS, but is poorly designed:
  - a single class doing FIVE unrelated things
  - adding a genuinely new feature requires MODIFYING existing,
    already-working code in several unrelated places
  - two classes are so tightly coupled that changing ONE breaks
    the OTHER in surprising, hard-to-predict ways
```

This is the real, practical motivation for this entire module: code that technically works today can
still be genuinely difficult, risky, and slow to extend tomorrow — LLD is the discipline for
avoiding exactly this outcome, deliberately, rather than discovering it the hard way months into a
project.

## A Concrete Example: Designing a Notification System

```
POORLY designed: one giant NotificationService class with an
  if/else chain checking notification TYPE (email vs. SMS vs.
  push) inside EVERY method - adding a new notification type
  means modifying this SAME class again and again.

WELL designed: a shared Notification INTERFACE, with a separate
  class per notification type (EmailNotification,
  SMSNotification) - adding a new type means adding a NEW class,
  never modifying existing, already-tested ones.
```

This exact example is a direct preview of the **Open-Closed Principle**, covered in
[SOLID Principles](../solid-principles/), the next module in this domain — LLD's actual value only
becomes concrete once shown against a real design decision like this one.

## What This Module Builds Toward

```
This module → objects/classes, relationships, UML notation,
  clean interfaces (the VOCABULARY and NOTATION)

SOLID Principles → the underlying DESIGN PRINCIPLES

Creational/Structural/Behavioral Design Patterns → NAMED,
  PROVEN solutions to recurring design problems, built directly
  on this foundation
```

Every later module in this domain builds directly on the vocabulary and concepts established here —
this module is deliberately foundational, not a standalone topic to skim past.

## Common Mistakes

- Treating LLD as a purely academic exercise disconnected from real code, rather than a discipline
  that directly improves how maintainable and extensible actual, shipped code turns out to be.
- Confusing LLD with HLD — LLD is about a system's internal class structure, not its overall
  service architecture.
- Assuming good design only matters for large, complex systems — even a small, single-purpose
  module benefits from deliberate, thoughtful class design over accidental structure.

## ➡️ Next

Continue to [objects-and-classes.md](objects-and-classes.md) to build the fundamental vocabulary
this entire domain relies on.
