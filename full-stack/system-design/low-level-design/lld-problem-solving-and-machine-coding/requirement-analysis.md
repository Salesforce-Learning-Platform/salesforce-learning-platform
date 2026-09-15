# 📝 Requirement Analysis

## Applying Everything to a Complete, Realistic Problem

Every module in this domain — [LLD Foundations](../lld-foundations/),
[SOLID Principles](../solid-principles/), and the three design pattern modules — covered individual
concepts and patterns in isolation. This final module applies all of them together, to one complete,
realistic problem: designing a **Parking Lot System**, used as the running worked example
throughout every file in this module. It starts, deliberately, not with code — but with
understanding the actual problem.

## Why Requirements Come Before Any Class Design

```
Jumping STRAIGHT to writing classes, before genuinely
understanding the actual requirements, risks designing the WRONG
system correctly - a perfectly SOLID, well-patterned design for a
problem that was misunderstood in the first place.
```

This is a genuinely important discipline, easy to skip under time pressure — no amount of careful
class design, SOLID compliance, or pattern selection compensates for having solved the wrong
problem.

## Clarifying Functional Requirements

```
For a Parking Lot System, genuinely worth asking explicitly:
  - How many ENTRY/EXIT points does the lot have?
  - Are there DIFFERENT vehicle types (car, motorcycle, truck),
    each needing a DIFFERENT spot size?
  - How is PARKING FEE calculated - flat rate? hourly? by vehicle
    type?
  - Does a vehicle need to be ASSIGNED a specific spot, or can it
    park anywhere available?
```

These are the kind of genuinely clarifying questions worth asking explicitly — in a real interview
or a real project kickoff — *before* writing a single class. Each answer meaningfully shapes the
eventual design.

## Clarifying Non-Functional Requirements

```
- SCALE: how many parking spots total? Does this matter for the
  actual class design, or only for infrastructure decisions (per
  Cloud Infrastructure Fundamentals, earlier in this repository)?
- CONCURRENCY: can MULTIPLE vehicles be processed (entering,
  exiting) SIMULTANEOUSLY, and does the design need to handle
  that safely?
- EXTENSIBILITY: will NEW vehicle types or NEW fee structures
  genuinely need to be added later?
```

Non-functional requirements — especially **extensibility** — directly shape which SOLID principles
and design patterns actually end up mattering for this specific problem, previewed here and covered
in full in
[extensibility-and-maintainability.md](extensibility-and-maintainability.md), later in this module.

## Defining the Core Entities, Before Any Code

```
From the requirements above, the Parking Lot problem's CORE
entities emerge naturally:
  - ParkingLot (the overall system)
  - ParkingSpot (a single space, with a TYPE and a status)
  - Vehicle (with a TYPE - car, motorcycle, truck)
  - Ticket (issued on entry, used to calculate the fee on exit)
```

This is the direct bridge to [class-design.md](class-design.md), next in this module — these
entities, identified purely from the requirements themselves, become the actual starting point for
designing the system's real classes.

## A Practical Requirement-Gathering Checklist

```
☐ What are the DISTINCT types of "things" involved (entities)?
☐ What ACTIONS can be performed on/with them?
☐ What CONSTRAINTS or business rules genuinely apply?
☐ What's explicitly OUT of scope, for now?
```

The last question — explicitly defining what's *out* of scope — is genuinely as valuable as
defining what's in scope; it prevents a design from growing unboundedly complex trying to
anticipate every conceivable future requirement at once.

## Common Mistakes

- Jumping directly to class design before genuinely understanding the actual requirements, risking
  a well-designed solution to the wrong problem.
- Treating every stated requirement as equally fixed, without recognizing which ones are genuinely
  likely to change (and therefore deserve more design flexibility).
- Never explicitly defining what's out of scope, letting a design's complexity grow unboundedly
  trying to anticipate every conceivable future need.

## ➡️ Next

Continue to [class-design.md](class-design.md) to turn these requirements into the Parking Lot
system's actual classes.
