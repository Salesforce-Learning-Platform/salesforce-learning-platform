# 🔨 Builder Pattern

## The Problem: Constructors With Too Many Parameters

```python
# WITHOUT Builder - a genuinely unwieldy constructor, and it only
# gets WORSE as more optional configuration is added
car = Car(4, "V8", True, False, True, None, "red", True, False)
```

```
What does the SIXTH positional argument actually mean here,
without checking the Car class's own definition? A constructor
with many parameters (especially many OPTIONAL ones) becomes
genuinely error-prone and unreadable.
```

Per Refactoring.guru's own framing, this problem specifically arises when constructing a genuinely
*complex* object with many optional parameters — a plain constructor (or a proliferation of
subclasses for every possible combination) handles this poorly.

## The Pattern

```python
class CarBuilder:
    def __init__(self):
        self._seats = 4
        self._engine = None
        self._gps = False

    def set_seats(self, seats):
        self._seats = seats
        return self   # returning self enables CHAINING

    def set_engine(self, engine):
        self._engine = engine
        return self

    def set_gps(self, has_gps):
        self._gps = has_gps
        return self

    def build(self):
        return Car(self._seats, self._engine, self._gps)
```

```python
car = (CarBuilder()
       .set_seats(2)
       .set_engine("V8")
       .set_gps(True)
       .build())
```

Each method call is self-documenting — `set_engine("V8")` is immediately clear in a way a bare
positional argument never is — and only the options genuinely relevant to a given car need to be
set at all, with sensible defaults for everything else.

## A Real Use Case: Car Manufacturing With Matching Documentation

```
Building actual cars with VARYING features (sports car, SUV,
cabriolet) without a Builder means a NEW subclass for every
possible combination. With Builder: a CarBuilder produces the
real vehicle, while a SEPARATE CarManualBuilder - following the
SAME set_seats()/set_engine()/set_gps() steps - produces the
MATCHING documentation.
```

This is directly Refactoring.guru's own real-world example — the genuinely valuable insight is that
the *same sequence of construction steps* can be reused across entirely different builders, each
producing a different kind of output from that identical sequence.

## The Optional `Director`: Reusable Construction Sequences

```python
class CarDirector:
    def construct_sports_car(self, builder: CarBuilder):
        return builder.set_seats(2).set_engine("V8").set_gps(True).build()

    def construct_suv(self, builder: CarBuilder):
        return builder.set_seats(7).set_engine("V6").set_gps(True).build()
```

A `Director` captures a *specific, named, reusable* construction sequence — genuinely useful when
certain combinations of options recur often enough to deserve their own name, rather than being
re-specified manually every single time.

## Common Mistakes

- Using Builder for a genuinely simple object with few, mostly-required parameters, adding
  unnecessary ceremony where a plain constructor would already be perfectly clear.
- Forgetting to `return self` from each setter method, breaking the chained, fluent call syntax the
  pattern's readability depends on.
- Allowing `build()` to return a genuinely incomplete or invalid object when required fields were
  never actually set, rather than validating before construction completes.

## ➡️ Next

Continue to [prototype-pattern.md](prototype-pattern.md) to see a genuinely different approach to
object creation: cloning an existing object instead of building one from scratch.
