# 5️⃣ Dependency Inversion Principle

## The Principle, Stated Precisely

```
"High-level modules should not depend on low-level modules. Both
should depend on ABSTRACTIONS."
```

This is a direct, full realization of
[designing-clean-interfaces.md](../lld-foundations/designing-clean-interfaces.md)'s Principle 4,
previewed briefly at the end of the LLD Foundations module — this file covers it completely, as the
capstone SOLID principle every other one builds toward.

## Before: A High-Level Class Depending on a Low-Level Detail

```python
class MySQLDatabase:
    def save(self, data): print(f"Saving to MySQL: {data}")

class UserService:                    # HIGH-LEVEL business logic
    def __init__(self):
        self.db = MySQLDatabase()      # depends DIRECTLY on a LOW-LEVEL detail

    def register_user(self, user_data):
        self.db.save(user_data)
```

```
UserService (the important, HIGH-LEVEL business logic) is
TIGHTLY COUPLED to MySQLDatabase (a LOW-LEVEL implementation
detail) - switching databases, or writing a test with a FAKE
database, means MODIFYING UserService itself.
```

This is genuinely backwards: `UserService` represents the actual, important business capability
("register a user"), while `MySQLDatabase` is a comparatively minor implementation detail — yet the
important class is the one forced to depend on, and change alongside, the less important one.

## After: Both Depend on a Shared Abstraction

```python
class Database:                        # the ABSTRACTION
    def save(self, data): raise NotImplementedError

class MySQLDatabase(Database):
    def save(self, data): print(f"Saving to MySQL: {data}")

class InMemoryDatabase(Database):        # trivial to swap in for TESTING
    def save(self, data): print(f"Saving to memory: {data}")

class UserService:
    def __init__(self, db: Database):    # depends on the ABSTRACTION
        self.db = db                      # not a specific implementation

    def register_user(self, user_data):
        self.db.save(user_data)

# The CALLER decides which concrete implementation to actually use:
user_service = UserService(MySQLDatabase())          # production
test_service = UserService(InMemoryDatabase())        # testing
```

Now `UserService` depends only on the abstract `Database` interface — both `UserService` and
`MySQLDatabase` depend on that shared abstraction, and neither depends directly on the other.
Swapping databases (or substituting a fake one for tests) requires zero changes to `UserService`
itself.

## Why "Inversion"? What's Actually Being Inverted

```
The NAIVE, natural direction: business logic --> depends on -->
  low-level database detail

The INVERTED direction: BOTH business logic AND the low-level
  detail --> depend on --> a shared ABSTRACTION
```

The "inversion" is specifically this: instead of the natural, intuitive dependency direction
(important code depending directly on a low-level detail), *both* sides depend on something more
stable and abstract sitting *between* them.

## This Is Exactly What Dependency Injection Enables

```
UserService(MySQLDatabase())   ← the concrete dependency is
                                  INJECTED from OUTSIDE, not
                                  created INSIDE the class itself
```

This is the direct, practical mechanism — often called **dependency injection** — that makes DIP
concrete in real code: a class receives its dependencies as constructor (or method) parameters,
rather than instantiating them internally, which is exactly what makes swapping implementations
(for production, for testing, for a future migration) possible without touching the class itself.

## Common Mistakes

- Instantiating a concrete, low-level dependency directly inside a high-level class's constructor,
  rather than receiving it as an injected parameter.
- Depending on a concrete class where an abstraction would genuinely serve just as well, losing the
  flexibility DIP is meant to provide.
- Creating an abstraction purely for its own sake, with only ever one real implementation and no
  genuine need for substitutability — adding indirection without a corresponding, real benefit.

## Module Summary

Across this module: **Single Responsibility** gives each class exactly one reason to change,
limiting the blast radius of any single modification (see
[single-responsibility-principle.md](single-responsibility-principle.md)); **Open-Closed** enables
new behavior through new classes implementing a shared interface, never by modifying existing,
working code (see [open-closed-principle.md](open-closed-principle.md)); **Liskov Substitution**
requires a subclass to be genuinely, behaviorally substitutable for its parent — not merely
intuitively "is-a" in the real-world sense, as the classic Rectangle/Square example shows (see
[liskov-substitution-principle.md](liskov-substitution-principle.md)); **Interface Segregation**
keeps interfaces small and focused, so no implementer is forced to support capabilities it
genuinely doesn't have (see
[interface-segregation-principle.md](interface-segregation-principle.md)); and **Dependency
Inversion** — both high-level and low-level code depending on a shared abstraction, realized
concretely through dependency injection — ties every other principle together into genuinely
flexible, testable, independently-changeable code.
