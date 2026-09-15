# 🎯 Designing Clean Interfaces

## A Class's Public API Is a Promise

A class's **interface** — its public methods and their signatures — is the actual contract other
code relies on. Every concept from this module (encapsulation, relationships, UML) ultimately serves
one practical goal: designing an interface that's genuinely clear, minimal, and hard to misuse.

## Principle 1: Expose Only What's Genuinely Necessary

```python
# POOR - exposes internal implementation details
class ShoppingCart:
    def __init__(self):
        self.items = []           # PUBLIC - callers can mutate directly
        self._recalculate_total()  # internal helper, but not hidden

# BETTER - a minimal, deliberate public interface
class ShoppingCart:
    def __init__(self):
        self._items = []           # PRIVATE by convention

    def add_item(self, item):
        self._items.append(item)

    def get_total(self) -> float:
        return sum(item.price for item in self._items)
```

This directly extends [objects-and-classes.md](objects-and-classes.md)'s encapsulation principle —
a smaller, deliberate public interface means fewer ways for other code to misuse or bypass a class's
own internal invariants, and genuinely more freedom to change the *internal* implementation later
without breaking anything that depends on it.

## Principle 2: Method Names Should Say What They Do

```python
# UNCLEAR - what does this actually do? Does it MODIFY the cart,
# or just CHECK something?
def process(self, item): ...

# CLEAR - the name itself genuinely communicates the behavior
def add_item(self, item): ...
def remove_item(self, item_id): ...
def apply_discount(self, code: str) -> bool: ...
```

A genuinely well-named method is close to self-documenting — this is directly the same clarity
principle already established in
[writing-clear-instructions.md](../../../artificial-intelligence/prompt-engineering-fundamentals/writing-clear-instructions.md),
earlier in this repository's AI Engineering domain, now applied to naming a method for a *human*
reader rather than writing a prompt for a model.

## Principle 3: Fail Loudly and Predictably

```python
def withdraw(self, amount: float):
    if amount <= 0:
        raise ValueError("Withdrawal amount must be positive")
    if amount > self.balance:
        raise InsufficientFundsError(f"Cannot withdraw {amount}, balance is {self.balance}")
    self.balance -= amount
```

A clean interface makes its own failure conditions explicit and predictable — raising a specific,
clearly-named exception is far more useful to a caller than silently returning `None`, or (worse)
leaving the object in a genuinely invalid, inconsistent state.

## Principle 4: Depend on Abstractions, Not Concrete Details

```python
# TIGHTLY COUPLED - ShoppingCart depends on a SPECIFIC payment
# implementation
class ShoppingCart:
    def checkout(self):
        stripe_client.charge(self.get_total())   # locked into Stripe

# LOOSELY COUPLED - depends on an ABSTRACT interface instead
class ShoppingCart:
    def __init__(self, payment_processor: PaymentProcessor):
        self.payment_processor = payment_processor

    def checkout(self):
        self.payment_processor.charge(self.get_total())
```

This is a direct preview of the **Dependency Inversion Principle**, the final principle covered in
[SOLID Principles](../solid-principles/), immediately next in this domain — designing against an
abstract interface rather than one specific, concrete implementation is what makes a class genuinely
flexible and independently testable.

## Common Mistakes

- Exposing internal implementation details (mutable public attributes, internal helper methods)
  that should genuinely remain private to the class.
- Choosing vague, generic method names (`process`, `handle`, `doStuff`) that force a caller to read
  the implementation just to understand what a method actually does.
- Silently swallowing an invalid input or an error condition rather than failing loudly and
  predictably with a clear, specific exception.

## Module Summary

Across this module: **Low-Level Design** is the discipline of deliberately designing a system's
classes and their structure, distinct from High-Level Design's broader service-architecture
concerns (see
[what-is-low-level-design.md](what-is-low-level-design.md)); **objects and classes**, built on the
four pillars of encapsulation, abstraction, inheritance, and polymorphism, are the fundamental
vocabulary this entire domain assumes (see [objects-and-classes.md](objects-and-classes.md));
**relationships between objects** — association, aggregation, composition, and inheritance — each
carry genuinely distinct lifecycle and structural implications worth choosing deliberately (see
[relationships-between-objects.md](relationships-between-objects.md)); **UML class and sequence
diagrams** provide a shared, standardized notation for structure and behavior respectively, most
valuable as a lightweight communication tool rather than exhaustive documentation (see
[uml-basics.md](uml-basics.md)); and **clean interfaces** — minimal exposure, clear naming,
predictable failure, and dependency on abstractions — turn every concept in this module into
genuinely maintainable, extensible code.
