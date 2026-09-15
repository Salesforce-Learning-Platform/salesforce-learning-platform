# 🎯 LLD Problem Solving and Machine Coding

## 📚 Overview

This final module of the Low-Level Design domain applies everything covered so far —
[LLD Foundations](../lld-foundations/), [SOLID Principles](../solid-principles/), and all three
design pattern modules — to one complete, realistic worked example: a **Parking Lot System**, built
across requirement analysis, class design, and an extensibility stress-test, then generalized into
a repeatable six-step process and verified with real tests.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Clarify functional and non-functional requirements before beginning any class design.
- Turn identified entities into classes with deliberate relationships and SOLID-compliant
  interfaces.
- Apply the right design pattern to a genuinely identified need, rather than by default.
- Follow a repeatable, six-step process for approaching a new machine-coding problem under
  realistic time constraints.
- Write tests that verify a design's actual behavior and its specific extensibility claims.

## 📋 Prerequisites

- [LLD Foundations](../lld-foundations/), [SOLID Principles](../solid-principles/), and the [Creational](../creational-design-patterns/), [Structural](../structural-design-patterns/), and [Behavioral](../behavioral-design-patterns/) Design Patterns modules — this module applies all of them together.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [requirement-analysis.md](requirement-analysis.md) | Clarifying functional/non-functional requirements and identifying core entities |
| [class-design.md](class-design.md) | Turning entities into classes, relationships, and a class diagram |
| [extensibility-and-maintainability.md](extensibility-and-maintainability.md) | Stress-testing the design with Strategy, Observer, and new requirements |
| [approaching-machine-coding-problems.md](approaching-machine-coding-problems.md) | A repeatable six-step process, applied to a second example (Vending Machine) |
| [testing-your-design.md](testing-your-design.md) | Verifying behavior and extensibility claims with real, automated tests; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** regardless of how much of this domain you've already covered — this module is where
every prior concept gets applied together, which is where the real, practical understanding
actually solidifies.

**Skim** only if you've already worked through a complete, realistic LLD problem end-to-end
elsewhere — but the six-step process in
[approaching-machine-coding-problems.md](approaching-machine-coding-problems.md) is worth a look
regardless, as a genuinely reusable checklist.

## 🧠 Knowledge Check

<details>
<summary>Why does requirement analysis come before any class design, rather than starting with classes and refining them as requirements become clearer?</summary>

No amount of careful class design, SOLID compliance, or pattern selection compensates for having
solved the wrong problem. A perfectly well-designed system built on a misunderstood requirement is
still the wrong system — clarifying requirements first ensures the design effort is actually spent
solving the genuine problem.

</details>

<details>
<summary>What's a concrete, measurable signal that a design has drifted from Open-Closed compliance?</summary>

Needing to *modify* existing, already-passing tests (rather than simply *adding* new ones) when
extending the system with a genuinely new feature. If adding a new `FeeStrategy` required changing
`ParkingLot`'s own existing tests, that would indicate the design isn't actually open for extension
without modification, despite what the design might claim.

</details>

## 📚 References

- Every reference already verified throughout the Low-Level Design domain's prior modules — this module applies that content directly rather than introducing new external sources.

## ➡️ Continue Your Learning Path

This is the final module of the Low-Level Design domain. Continue to the High-Level Design domain
to move from a single component's internal class structure to an entire system's architecture.
