# 🔧 Extensibility and Maintainability

## Stress-Testing the Design Against Real Change

[class-design.md](class-design.md) produced a working Parking Lot design. This file applies the
genuine test every real design eventually faces: what happens when requirements *change*? A design
that only works for today's exact requirements, and requires significant rework for tomorrow's, has
a real, hidden cost.

## Applying Open-Closed: Adding a New Fee Structure

```python
class FeeStrategy:   # directly the Strategy pattern, from
    def calculate(self, ticket: "Ticket") -> float:   # Behavioral
        raise NotImplementedError                        # Design Patterns

class HourlyFeeStrategy(FeeStrategy):
    def calculate(self, ticket):
        hours = (ticket.exit_time - ticket.entry_time).total_seconds() / 3600
        return max(1, round(hours)) * 2.0   # $2/hour, minimum 1 hour

class FlatRateFeeStrategy(FeeStrategy):
    def calculate(self, ticket):
        return 10.0   # a flat $10, regardless of duration
```

```python
class ParkingLot:
    def __init__(self, spots: list[ParkingSpot], fee_strategy: FeeStrategy):
        self._spots = spots
        self._fee_strategy = fee_strategy   # INJECTED, per Dependency
                                              # Inversion, earlier in
                                              # this domain
```

This directly applies [Strategy](../behavioral-design-patterns/strategy-pattern.md) and
[Dependency Inversion](../solid-principles/dependency-inversion-principle.md), both from earlier in
this domain — adding an entirely new fee structure (a weekday/weekend rate, a membership discount)
means writing one new `FeeStrategy` subclass; `ParkingLot` itself never needs to change at all.

## Applying Observer: Notifying on a Spot Becoming Available

```python
class ParkingLot:
    def __init__(self, spots, fee_strategy):
        self._spots = spots
        self._fee_strategy = fee_strategy
        self._subscribers = []   # directly the Observer pattern

    def subscribe(self, observer):
        self._subscribers.append(observer)

    def remove_vehicle(self, ticket: "Ticket"):
        ticket.spot.remove_vehicle()
        for observer in self._subscribers:
            observer.on_spot_available(ticket.spot)
```

A genuinely new requirement — "notify a mobile app when a spot opens up" — is handled by directly
applying [Observer](../behavioral-design-patterns/observer-pattern.md), earlier in this domain,
without modifying `ParkingSpot`, `Vehicle`, or `Ticket` at all.

## Applying Factory Method: Adding a New Vehicle Type

```
Adding "electric vehicle" (needing a spot with a charging port) as
a NEW VehicleType, per Factory Method's pattern from Creational
Design Patterns, earlier in this domain, means the SAME
find_available_spot() logic already works UNCHANGED — it simply
now also matches against this new enum value, with no structural
change needed to ParkingLot itself.
```

This demonstrates something genuinely important: not every extension requires a *new* pattern —
sometimes a well-designed system's *existing* structure (here, `VehicleType` as an enum, checked
generically) already accommodates a new case cleanly, without needing any additional pattern at
all.

## A Genuine Test: Could This Design Handle Multiple Parking Lots?

```
"What if the system needs to manage MULTIPLE parking lots across
a city, with a SHARED fee strategy but INDEPENDENT spot
inventories?"

This design ALREADY supports it - each ParkingLot instance is
independent, and FeeStrategy objects can genuinely be SHARED
across multiple ParkingLot instances (per the Flyweight-adjacent
benefit of Strategy's stateless, reusable design).
```

This is a genuinely useful, practical exercise — deliberately asking "what if this specific new
requirement appeared?" against an already-completed design is exactly how to verify whether its
extensibility claims actually hold up in practice, not merely in theory.

## Common Mistakes

- Designing for every conceivable future requirement upfront, adding genuine complexity for
  flexibility that may never actually be needed — directly the same over-engineering risk already
  warned against in [Understanding AI Agents](../../../artificial-intelligence/understanding-ai-agents/when-to-use-multi-agent-systems-and-when-not-to.md),
  earlier in this repository, now applied to LLD.
- Hardcoding a fee calculation directly inside `ParkingLot` instead of extracting it into a
  swappable strategy, once it becomes clear fee structures genuinely vary.
- Never actually testing a design against a hypothetical future requirement, only discovering its
  real extensibility limits once that requirement genuinely arrives.

## ➡️ Next

Continue to
[approaching-machine-coding-problems.md](approaching-machine-coding-problems.md) to see this exact
design process applied step by step, under realistic, timed conditions.
