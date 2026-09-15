# 🧭 Strategy Pattern

## The Problem: a Class Bloated With Algorithm Variations

```python
# WITHOUT Strategy - EVERY new algorithm variant makes this class
# genuinely BIGGER, and genuinely harder to maintain
class Navigator:
    def calculate_route(self, start, end, mode):
        if mode == "driving":
            # driving-specific routing logic
            ...
        elif mode == "walking":
            # walking-specific routing logic
            ...
        elif mode == "cycling":
            # cycling-specific routing logic
            ...
```

Per Refactoring.guru's own framing: "Each time you added a new routing algorithm, the main class of
the navigator doubled in size" — this is a direct, concrete instance of the same
[Open-Closed](../solid-principles/open-closed-principle.md) violation already covered earlier in
this domain, now specifically applied to interchangeable *algorithms* rather than object types.

## The Pattern

```python
class RoutingStrategy:
    def calculate_route(self, start, end): raise NotImplementedError

class DrivingStrategy(RoutingStrategy):
    def calculate_route(self, start, end):
        return f"Driving route from {start} to {end}"

class WalkingStrategy(RoutingStrategy):
    def calculate_route(self, start, end):
        return f"Walking route from {start} to {end}"

class Navigator:   # the CONTEXT
    def __init__(self, strategy: RoutingStrategy):
        self._strategy = strategy

    def get_route(self, start, end):
        return self._strategy.calculate_route(start, end)
```

```python
nav = Navigator(DrivingStrategy())
print(nav.get_route("Home", "Work"))

nav._strategy = WalkingStrategy()   # SWITCH strategies at RUNTIME,
print(nav.get_route("Home", "Work"))   # with NO change to Navigator itself
```

`Navigator` (the **context**) delegates entirely to whichever `RoutingStrategy` it currently holds —
adding a new routing algorithm means adding one new class, never touching `Navigator` or any
existing strategy at all.

## A Real, Everyday Analogy: Getting to the Airport

```
You can take a bus, order a cab, or ride a bicycle - these are
your available TRANSPORTATION STRATEGIES. You choose ONE based on
your OWN criteria (budget, time) - the DESTINATION (the goal
itself) never changes, only WHICH strategy you use to get there.
```

This is directly Refactoring.guru's own real-world analogy — genuinely capturing the pattern's core
idea: several interchangeable ways to accomplish the *same* goal, chosen based on context.

## Strategy vs. State: a Precise, Important Distinction

```
STRATEGY: concrete strategies are INDEPENDENT and UNAWARE of each
  other - the CLIENT explicitly chooses which one to use

STATE: State can be considered an EXTENSION of Strategy - but
  concrete states are ALLOWED to change the CONTEXT's current
  state themselves, transitioning it to another state internally
```

Per Refactoring.guru's own direct comparison — this distinction matters genuinely: Strategy's
concrete implementations are deliberately independent and interchangeable by the *client*;
[state-pattern.md](state-pattern.md), next in this module, covers the related pattern where the
implementations themselves can trigger transitions.

## Common Mistakes

- Keeping algorithm-selection logic as an `if/elif` chain inside a context class, rather than
  extracting each variant into its own strategy class.
- Confusing Strategy (client-chosen, independent algorithms) with State (self-transitioning,
  context-aware states) — the two patterns share a very similar structural shape but solve
  genuinely different problems.
- Over-applying Strategy for a case with genuinely only one algorithm that will ever exist, adding
  unnecessary indirection for a variability that doesn't actually exist.

## ➡️ Next

Continue to [state-pattern.md](state-pattern.md) to see the closely related pattern this file just
distinguished Strategy from.
