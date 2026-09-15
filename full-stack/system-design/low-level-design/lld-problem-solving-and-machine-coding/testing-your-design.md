# ✅ Testing Your Design

## Verifying the Design Genuinely Works, Not Just That It Compiles

Every prior file in this module built and reasoned about the Parking Lot design. This final file
applies the same discipline already established in
[The Testing Pyramid](../../../frontend/testing/frontend-testing-fundamentals/the-testing-pyramid.md),
earlier in this repository — a design that merely *compiles* hasn't yet been genuinely *verified*
to behave correctly.

## Writing Real Tests Against the Parking Lot Design

```python
def test_parks_vehicle_in_available_spot():
    spot = ParkingSpot("A1", VehicleType.CAR)
    lot = ParkingLot([spot], HourlyFeeStrategy())
    car = Vehicle("ABC-123", VehicleType.CAR)

    ticket = lot.park_vehicle(car)

    assert spot.vehicle == car
    assert ticket.spot == spot

def test_raises_when_no_spot_available():
    lot = ParkingLot([], HourlyFeeStrategy())   # NO spots at all
    car = Vehicle("ABC-123", VehicleType.CAR)

    with pytest.raises(ValueError):
        lot.park_vehicle(car)

def test_does_not_park_wrong_vehicle_type_in_mismatched_spot():
    motorcycle_spot = ParkingSpot("M1", VehicleType.MOTORCYCLE)
    lot = ParkingLot([motorcycle_spot], HourlyFeeStrategy())
    car = Vehicle("ABC-123", VehicleType.CAR)

    with pytest.raises(ValueError):
        lot.park_vehicle(car)   # no MATCHING spot exists
```

These tests verify genuine *behavior*, not merely that the code runs — each one checks a specific,
meaningful claim about how the system should behave, including the deliberately chosen failure
cases (no spot available, a type mismatch) that a "happy path only" test suite would miss entirely.

## Testing the Extensibility Claims Directly

```python
def test_flat_rate_strategy_ignores_duration():
    ticket = Ticket(vehicle=car, spot=spot)
    ticket.exit_time = ticket.entry_time + timedelta(hours=10)   # a LONG stay

    fee = FlatRateFeeStrategy().calculate(ticket)

    assert fee == 10.0   # UNCHANGED regardless of duration -
                            # genuinely verifying the STRATEGY
                            # pattern's actual, real independence
```

This directly tests the very claim made in
[extensibility-and-maintainability.md](extensibility-and-maintainability.md) — that swapping fee
strategies genuinely works without touching `ParkingLot` — turning a design *argument* into an
actual, verified, automatable fact.

## Edge Cases Worth Deliberately Testing

```
☐ The system with ZERO spots at all
☐ EVERY spot already occupied (a genuinely full lot)
☐ A vehicle type with NO matching spot type available at all
☐ Removing a vehicle that was NEVER actually parked
☐ Calculating a fee for a ticket that HASN'T been exited yet
  (exit_time is still None)
```

These edge cases are exactly the kind of scenario
[approaching-machine-coding-problems.md](approaching-machine-coding-problems.md)'s step 6 (scenario
walkthrough) should surface during design — and each one deserves its own explicit test, not just a
verbal mention during a design discussion.

## Testing SOLID Compliance Indirectly, Through Behavior

```
A genuinely well-tested design INDIRECTLY confirms its SOLID
compliance - if adding a NEW FeeStrategy required modifying
ParkingLot's own tests (not just adding NEW ones), that would be
a real, concrete SIGNAL the design has drifted from Open-Closed.
```

This is a genuinely useful, practical heuristic: needing to *change* existing tests (rather than
simply *add* new ones) when extending a system is often a concrete, measurable sign that Open-Closed
has been violated somewhere in the actual implementation.

## Common Mistakes

- Testing only the happy path, missing the deliberately chosen failure and edge cases that reveal
  whether a design genuinely handles unusual, but realistic, situations.
- Never actually testing the specific extensibility claims made during design, leaving them as
  untested assertions rather than verified facts.
- Needing to modify existing, passing tests when adding a genuinely new feature — a concrete signal
  worth treating as feedback about the design's actual Open-Closed compliance.

## Module Summary

Across this module: **requirement analysis** — clarifying functional and non-functional
requirements, and identifying core entities — comes deliberately before any class design, since no
amount of careful design compensates for solving the wrong problem (see
[requirement-analysis.md](requirement-analysis.md)); **class design** turns those entities into
actual classes with deliberate relationships, directly applying this domain's LLD Foundations and
SOLID principles (see [class-design.md](class-design.md)); **extensibility and maintainability**
stress-tests the resulting design against genuinely new requirements, applying Strategy, Observer,
and Dependency Inversion exactly where they fit a real, identified need (see
[extensibility-and-maintainability.md](extensibility-and-maintainability.md)); **approaching
machine-coding problems** names the repeatable six-step process demonstrated throughout this
module, applied to a second example (a Vending Machine) to show it generalizes (see
[approaching-machine-coding-problems.md](approaching-machine-coding-problems.md)); and **testing
your design** turns every design claim — including extensibility claims — into genuine, automated,
verified facts rather than untested assertions, closing out this domain's complete progression from
LLD Foundations through named patterns to a fully worked, tested design.
