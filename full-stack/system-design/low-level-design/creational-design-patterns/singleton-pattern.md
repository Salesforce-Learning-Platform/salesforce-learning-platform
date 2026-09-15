# 🌟 Singleton Pattern

## Named Patterns: Proven Solutions to Recurring Problems

[SOLID Principles](../solid-principles/) established *how* to design individual classes well.
**Design patterns** are a level above that — named, proven solutions to design problems that recur
across many different applications. **Creational patterns**, covered in this module, specifically
address *how objects get created* — starting with the simplest and most widely recognized: Singleton.

## The Problem It Solves

```
Some resources should GENUINELY have only ONE instance across an
entire application - a database connection pool, a configuration
manager, a logging service - and every part of the application
needs to reach that SAME, single instance.
```

## The Pattern

```python
class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._settings = {}
        return cls._instance

    def set(self, key, value):
        self._settings[key] = value

    def get(self, key):
        return self._settings.get(key)
```

```python
config1 = ConfigManager()
config1.set("debug", True)

config2 = ConfigManager()
print(config2.get("debug"))   # True - config2 IS config1, the SAME instance
```

The constructor is intercepted (`__new__`) so that every attempt to create a `ConfigManager`
actually returns the *same* underlying instance — directly per Refactoring.guru's own definition,
this provides a global access point while genuinely preventing more than one instance from ever
existing.

## A Real Use Case: a Database Connection Pool

```
A database connection pool is genuinely expensive to CREATE
(establishing actual network connections) - creating a NEW pool
every time part of the application needs database access would be
wasteful and could exhaust the database's own connection limit.

A Singleton ensures every part of the application shares the
SAME pool.
```

This is directly the canonical real-world justification for Singleton — not "convenience," but a
genuine, structural need for exactly one shared instance managing a genuinely limited, expensive
resource.

## The Real, Well-Known Trade-Off: Global State

```
A Singleton is, functionally, a GLOBAL variable - and it carries
the SAME risks: HIDDEN dependencies (code anywhere can silently
reach into it), and genuine difficulty TESTING code that depends
on it (per Dependency Inversion, from SOLID Principles, earlier
in this domain - a Singleton is difficult to swap for a test
double).
```

This is a genuinely important, often-underweighted caveat — Singleton is one of the most
recognizable design patterns, but also one of the most frequently *overused*, precisely because its
global-state trade-off is easy to overlook when the pattern otherwise seems convenient.

## Common Mistakes

- Reaching for Singleton by default for any class that "feels like" it should only have one
  instance, rather than for a genuine, structural need (a truly shared, expensive resource).
- Using a Singleton for something that would actually benefit from dependency injection instead
  (per [Dependency Inversion](../solid-principles/dependency-inversion-principle.md)), making code
  that depends on it genuinely harder to test in isolation.
- Storing genuinely request-specific or user-specific state inside a Singleton, which is shared —
  and therefore visible — across the entire application.

## ➡️ Next

Continue to [factory-pattern.md](factory-pattern.md) to see the pattern for creating objects
without the calling code needing to know their exact, concrete type.
