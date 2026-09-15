# 3️⃣ Liskov Substitution Principle

## The Principle, Stated Precisely

```
"Objects of a SUPERCLASS should be replaceable with objects of a
SUBCLASS without breaking the correctness of the program."
```

This directly formalizes the "is-a" relationship already introduced in
[relationships-between-objects.md](../lld-foundations/relationships-between-objects.md) — if `Square`
inherits from `Rectangle`, then *every* piece of code written to work with a `Rectangle` must
continue to behave correctly when handed a `Square` instead, with no special-casing required.

## Before: the Classic Rectangle/Square Violation

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_width(self, width): self.width = width
    def set_height(self, height): self.height = height
    def area(self): return self.width * self.height

class Square(Rectangle):   # mathematically, a Square IS a Rectangle...
    def set_width(self, width):
        self.width = width
        self.height = width    # a Square must keep both sides equal
    def set_height(self, height):
        self.height = height
        self.width = height
```

```python
def resize_and_check(rect: Rectangle):
    rect.set_width(5)
    rect.set_height(10)
    assert rect.area() == 50   # true for a Rectangle...

resize_and_check(Square(2, 2))   # FAILS - area is 100, not 50!
```

Even though a square *is*, mathematically, a rectangle, this inheritance genuinely violates LSP:
code written correctly for `Rectangle` silently breaks when handed a `Square`, because `Square`
secretly changes `set_height`'s actual behavior in a way the `Rectangle` interface's contract never
promised.

## Why This Happens: a Semantic Mismatch, Not a Coding Error

```
The BUG isn't in the CODE syntax - it's in the DESIGN DECISION to
model Square as a SUBCLASS of Rectangle at all. Mathematically
"is-a" and PROGRAMMATICALLY substitutable "is-a" are genuinely
DIFFERENT questions.
```

This is the real, important lesson: LSP violations often come from a design decision that felt
intuitively correct (a square certainly *is*, in the mathematical sense, a rectangle) but breaks
down once actual *behavioral* substitutability is required.

## After: Avoiding the Inheritance Relationship Entirely

```python
class Shape:
    def area(self): raise NotImplementedError

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width, self.height = width, height
    def area(self): return self.width * self.height

class Square(Shape):   # a SIBLING of Rectangle, not a subclass of it
    def __init__(self, side):
        self.side = side
    def area(self): return self.side ** 2
```

Making `Square` and `Rectangle` siblings under a shared `Shape` interface — rather than one
inheriting from the other — sidesteps the entire problem: neither class makes a behavioral promise
the other can't genuinely keep, since neither one claims to *be* a substitutable version of the
other.

## Recognizing an LSP Violation in Practice

```
A genuine warning sign: a subclass OVERRIDES a method specifically
to THROW an exception, do LESS than the parent promised, or
secretly CHANGE another property as a side effect (per the Square
example) - each is a sign the "is-a" relationship doesn't
genuinely hold at the BEHAVIORAL level.
```

## Common Mistakes

- Modeling an inheritance relationship based purely on real-world or mathematical "is-a" intuition,
  without verifying genuine behavioral substitutability.
- A subclass overriding a method to throw an exception for a case the parent class's interface
  promised to handle, silently breaking any code trusting that promise.
- Adding special-case checks (`if isinstance(shape, Square): ...`) in calling code to work around an
  LSP violation, rather than fixing the underlying design.

## ➡️ Next

Continue to
[interface-segregation-principle.md](interface-segregation-principle.md) to see why a large,
general-purpose interface can itself become a design problem.
