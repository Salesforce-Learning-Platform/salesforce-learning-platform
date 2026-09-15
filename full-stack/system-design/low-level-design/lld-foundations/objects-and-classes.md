# 🧱 Objects and Classes

## The Fundamental Building Blocks

A **class** is a blueprint — a definition of what data (attributes) and behavior (methods) a
certain kind of thing has. An **object** is a genuine, actual instance created from that blueprint —
this is the exact same class-and-instance relationship already introduced in
[Docker Images and Containers](../../../production-systems/docker-and-containerization/docker-images-and-containers.md),
earlier in this repository, now applied to code itself rather than container infrastructure.

## A Concrete Class Definition

```python
class BankAccount:
    def __init__(self, owner: str, balance: float = 0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float):
        self.balance += amount

    def withdraw(self, amount: float):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
```

`BankAccount` is the class — a definition. `BankAccount("Alice", 100)` creates an *object*, a real,
specific instance with its own actual `owner` and `balance` values, independent of any other
`BankAccount` object that might exist elsewhere.

## The Four Pillars of Object-Oriented Design

```
ENCAPSULATION  → bundling data (balance) WITH the behavior that
                 operates on it (deposit/withdraw) - and hiding
                 that data from direct, uncontrolled external
                 access

ABSTRACTION    → exposing only WHAT a class does (deposit,
                 withdraw), hiding HOW it actually does it
                 internally

INHERITANCE    → a class can be built as a specialized version of
                 another, more general class

POLYMORPHISM   → different classes can be treated interchangeably
                 through a SHARED interface, each responding to
                 the same method call in its own, distinct way
```

These four pillars are the vocabulary every later file in this domain assumes — worth genuinely
internalizing here, since [SOLID Principles](../solid-principles/) and every design pattern in this
domain are built directly on top of these exact ideas.

## Encapsulation in Practice: Why `balance` Isn't Public

```python
# BAD - balance can be set to ANY value, bypassing all validation
account.balance = -1000

# GOOD - balance can only change through methods that ENFORCE
# the account's own rules
account.withdraw(50)   # enforces the insufficient-funds check
```

This is the practical, concrete value of encapsulation: it's not merely a stylistic preference —
allowing direct access to `balance` means any part of a program can set it to an invalid value
(negative, for instance), entirely bypassing the validation logic the class itself was designed to
enforce.

## Polymorphism, Concretely

```python
class Notification:
    def send(self, message: str): raise NotImplementedError

class EmailNotification(Notification):
    def send(self, message: str): print(f"Emailing: {message}")

class SMSNotification(Notification):
    def send(self, message: str): print(f"Texting: {message}")

def notify_all(notifications: list[Notification], message: str):
    for n in notifications:
        n.send(message)   # each object responds in its OWN way
```

`notify_all` doesn't need to know or care whether each item is an `EmailNotification` or an
`SMSNotification` — it treats them all uniformly through the shared `Notification` interface, and
each object's own `send()` implementation handles the actual, specific behavior. This is the exact
mechanism [what-is-low-level-design.md](what-is-low-level-design.md)'s notification example pointed
toward.

## Common Mistakes

- Making class attributes directly, publicly writable, bypassing the validation logic the class was
  specifically designed to enforce.
- Using inheritance purely for code reuse when the actual relationship isn't genuinely an "is-a"
  relationship — a topic [liskov-substitution-principle.md](../solid-principles/liskov-substitution-principle.md),
  later in this domain, covers in depth.
- Writing a long `if/elif` chain checking an object's specific type, when polymorphism through a
  shared interface would let each type handle its own behavior directly.

## ➡️ Next

Continue to
[relationships-between-objects.md](relationships-between-objects.md) to see the different ways
classes can actually connect to and depend on each other.
