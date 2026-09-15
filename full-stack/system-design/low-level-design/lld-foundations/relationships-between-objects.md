# 🔗 Relationships Between Objects

## Classes Rarely Exist in Isolation

A real system's classes genuinely depend on and interact with each other — a `Car` has an `Engine`,
an `Order` contains `LineItem`s, a `Student` enrolls in `Course`s. How these relationships are
actually structured has real, lasting consequences for how independently each class can change.

## Association: "Uses" or "Knows About"

```python
class Driver:
    def drive(self, car: "Car"):
        car.accelerate()
```

`Driver` and `Car` are **associated** — one uses the other, but neither genuinely owns the other's
lifecycle. A `Car` continues to exist whether or not a specific `Driver` object currently references
it.

## Aggregation: "Has-a," But Independent Lifecycles

```python
class Department:
    def __init__(self, employees: list["Employee"]):
        self.employees = employees   # Department HOLDS employees,
                                       # but doesn't OWN their lifecycle
```

```
If a Department is deleted, its Employees CONTINUE TO EXIST -
they could be reassigned to a DIFFERENT department entirely.
```

**Aggregation** is a "whole-part" relationship where the parts can genuinely exist independently of
the whole — an `Employee` isn't destroyed just because the `Department` object referencing them is.

## Composition: "Has-a," With a Shared Lifecycle

```python
class Car:
    def __init__(self):
        self.engine = Engine()   # the Car CREATES and OWNS its engine
```

```
If a Car object is destroyed, its Engine is destroyed WITH it -
that SPECIFIC Engine instance has no meaningful existence
independent of THIS specific Car.
```

**Composition** is a genuinely stronger relationship than aggregation: the contained object's
lifecycle is bound to its container's — this distinction (independent vs. bound lifecycle) is
precisely what separates aggregation from composition, and it's worth being deliberate about which
one a given relationship actually represents.

## Inheritance: "Is-a"

```python
class Vehicle:
    def move(self): pass

class Car(Vehicle):   # a Car IS-A Vehicle
    pass
```

Already introduced in [objects-and-classes.md](objects-and-classes.md) — inheritance models a
genuine "is-a" relationship, structurally different from association/aggregation/composition's
"has-a" or "uses" relationships. Confusing these two categories is one of the most common real
design mistakes — covered in depth in
[liskov-substitution-principle.md](../solid-principles/liskov-substitution-principle.md), later in
this domain.

## Why This Distinction Genuinely Matters in Practice

```
Choosing COMPOSITION when the relationship is really AGGREGATION:
  → deleting the "whole" object ACCIDENTALLY destroys "part"
    objects that should have survived independently

Choosing AGGREGATION when the relationship is really COMPOSITION:
  → "part" objects can be left ORPHANED, referenced by nothing,
    when they should have been cleaned up automatically
```

This is a genuinely practical, not merely academic, distinction — getting it wrong leads to either
premature data loss or a genuine memory/resource leak, depending on which direction the mistake goes.

## Visualizing These Relationships

```
These relationships are exactly what UML class diagrams are
DESIGED to express visually - a plain line (association), an open
diamond (aggregation), a filled diamond (composition), and a
hollow triangle (inheritance) - covered next in uml-basics.md.
```

## Common Mistakes

- Using composition for a relationship that's actually aggregation, causing "part" objects to be
  unintentionally destroyed when they should survive independently of the "whole."
- Confusing "has-a" relationships (association/aggregation/composition) with "is-a" relationships
  (inheritance), leading to an inheritance hierarchy that doesn't genuinely model reality.
- Never explicitly considering lifecycle ownership when designing a relationship, leaving it
  ambiguous whether a "part" object should be destroyed alongside its "whole."

## ➡️ Next

Continue to [uml-basics.md](uml-basics.md) to see how these relationships are actually notated and
communicated visually.
