# 1️⃣ Single Responsibility Principle

## SOLID: Five Principles, One Shared Goal

**SOLID** — Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, and
Dependency Inversion — are five design principles, coined by Robert C. Martin ("Uncle Bob"),
directly building on [LLD Foundations](../lld-foundations/)'s object-oriented vocabulary. Each
addresses a genuinely different way a class's design can go wrong; together, they define what
"well-designed" actually, concretely means in practice.

## The Principle, Stated Precisely

```
"A class should have ONE, and only ONE, reason to change."
```

This is deliberately more precise than "a class should do one thing" — a class can have several
*methods* and still satisfy SRP, as long as every one of those methods serves the *same* underlying
responsibility, changing for the *same* underlying reason.

## Before: A Class With Multiple, Unrelated Responsibilities

```python
class Order:
    def __init__(self, items):
        self.items = items

    def calculate_total(self):
        return sum(item.price for item in self.items)

    def save_to_database(self):
        db.execute("INSERT INTO orders ...")   # RESPONSIBILITY 1: persistence

    def send_confirmation_email(self):
        smtp.send(...)                          # RESPONSIBILITY 2: notifications

    def generate_invoice_pdf(self):
        pdf_generator.create(...)               # RESPONSIBILITY 3: document generation
```

```
This class has FOUR genuinely distinct reasons to change:
  - the order's own business logic changes
  - the DATABASE schema/technology changes
  - the EMAIL provider or template changes
  - the INVOICE format changes
```

Each of these is a completely independent concern, yet all four are tangled together inside one
class — a change to how invoices are formatted requires touching the exact same class as a change
to the order's core business logic, even though the two are entirely unrelated.

## After: One Responsibility Per Class

```python
class Order:
    def __init__(self, items):
        self.items = items

    def calculate_total(self):
        return sum(item.price for item in self.items)

class OrderRepository:
    def save(self, order: Order):
        db.execute("INSERT INTO orders ...")

class OrderNotifier:
    def send_confirmation(self, order: Order):
        smtp.send(...)

class InvoiceGenerator:
    def generate_pdf(self, order: Order):
        pdf_generator.create(...)
```

Now each class has exactly one reason to change — `Order` changes only when the order's own core
business rules change; `OrderRepository` changes only when persistence details change; and so on.
Each class can be understood, tested, and modified genuinely independently of the others.

## Why This Matters Beyond Tidiness

```
A class violating SRP has a LARGER "blast radius" for every
change - touching it for ONE reason risks accidentally breaking
UNRELATED functionality that happens to live in the same class.
```

This is the real, practical payoff — SRP isn't about aesthetic preference; it's about genuinely
limiting how much of a system a single change can accidentally affect, directly reducing the risk
and cost of every future modification.

## Common Mistakes

- Interpreting SRP as "one method per class," which is far too strict — a class can have several
  methods as long as they all serve the same underlying responsibility.
- Splitting a class along the wrong boundary, separating methods that genuinely belong together
  (the same actual responsibility) just to reduce a class's line count.
- Identifying "responsibility" by counting methods rather than by asking "what would cause this
  class to need to change?" for each piece of its behavior.

## ➡️ Next

Continue to [open-closed-principle.md](open-closed-principle.md) for the second SOLID principle:
designing a class that can be extended without being modified.
