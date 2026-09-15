# 🎯 Approaching Machine Coding Problems Step by Step

## A Repeatable Process, Not Just a Finished Example

The Parking Lot system built across
[requirement-analysis.md](requirement-analysis.md),
[class-design.md](class-design.md), and
[extensibility-and-maintainability.md](extensibility-and-maintainability.md) followed a genuine,
repeatable *process* — this file names that process explicitly, so it can be applied to any new
machine-coding problem (a Vending Machine, an Elevator System, a Library Management System) under
realistic, often time-constrained conditions.

## The Six-Step Process, Named Explicitly

```
1. CLARIFY requirements (functional AND non-functional) - per
   requirement-analysis.md
2. IDENTIFY the core entities/nouns from those requirements
3. DEFINE relationships between entities (association, aggregation,
   composition, inheritance) - per relationships-between-objects.md
4. DESIGN classes with clean interfaces, applying SOLID - per
   class-design.md
5. APPLY design patterns WHERE they genuinely fit a real,
   identified need - never by default
6. WALK THROUGH the design against realistic scenarios, INCLUDING
   the specific extensibility scenarios from
   extensibility-and-maintainability.md
```

This is genuinely the same sequence already demonstrated across this module's prior three files,
now made explicit as a reusable checklist for a *new* problem.

## A Second Worked Example, Applied Quickly: a Vending Machine

```
1. CLARIFY: What products does it sell? Does it accept coins,
   cards, or both? Can it give change?

2. IDENTIFY entities: VendingMachine, Product, Inventory, Payment

3. RELATIONSHIPS: VendingMachine AGGREGATES Inventory; Inventory
   COMPOSES a collection of Product quantities

4. CLASSES, applying SOLID: a PaymentProcessor interface
   (Dependency Inversion) rather than hardcoding one payment method

5. PATTERNS: State pattern for the machine's own operational
   states (Idle, HasMoney, Dispensing, OutOfStock) - directly the
   State pattern from Behavioral Design Patterns, earlier in this
   domain, since the SAME "insert coin" action behaves genuinely
   differently depending on the machine's current state

6. WALK THROUGH: "what if a NEW payment method (mobile pay) is
   added?" - answered directly by the PaymentProcessor interface
   from step 4, with NO changes needed elsewhere
```

Notice this reuses the *exact* six-step process — applied to a genuinely different problem, it
surfaces a genuinely different, appropriate pattern (State, rather than Parking Lot's Strategy and
Observer), precisely because the process starts from the *actual* requirements each time, rather
than forcing a memorized pattern onto an unrelated problem.

## Managing Time Under Realistic, Interview-Style Constraints

```
A common, PRACTICAL time allocation for a 45-60 minute machine-
coding exercise:
  ~10 min: clarifying requirements and entities (steps 1-3)
  ~25 min: core class design and implementation (steps 4-5)
  ~10 min: walking through scenarios, discussing extensibility
    (step 6)
  ~10 min: handling questions, refining based on feedback
```

This is a genuinely practical, realistic pacing guideline — spending the entire allotted time on
step 4 alone, without ever reaching step 6's scenario walkthrough, is a common, avoidable mistake
under real time pressure.

## Communicating the Design Out Loud

```
Genuinely important in an interview setting: narrate the actual
REASONING behind each decision as it's made - "I'm using
COMPOSITION here because a ParkingSpot's vehicle reference
shouldn't be destroyed WITH the spot" - not just the final code.
```

This directly reflects [Engineering WITH AI](../../../artificial-intelligence/engineering-with-ai/)'s
"can you defend this line?" standard, earlier in this repository — the *reasoning* behind a design
decision is often more valuable to communicate than the specific code itself, since it demonstrates
genuine understanding rather than memorized syntax.

## Common Mistakes

- Spending the entire available time on step 4 (implementation) without ever reaching step 6
  (scenario walkthrough and extensibility discussion).
- Jumping to a specific, memorized design pattern before genuinely identifying whether the actual
  problem calls for it, rather than letting the pattern emerge naturally from the requirements.
- Writing code silently, without narrating the actual reasoning behind each design decision as it's
  made.

## ➡️ Next

Continue to [testing-your-design.md](testing-your-design.md) to see how this design is actually
verified to work correctly, not merely assumed to.
