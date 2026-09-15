# 🔌 Adapter Pattern

## Structural Patterns: How Objects Compose Together

[Creational Design Patterns](../creational-design-patterns/) covered how objects get *created*.
**Structural patterns**, covered in this module, address a genuinely different question: how
existing objects and classes are *composed together* into larger structures — starting with
Adapter, the pattern for making two genuinely incompatible interfaces work together.

## The Problem: Incompatible Interfaces

```python
# A third-party analytics library that only accepts JSON
class AnalyticsLibrary:
    def process(self, json_data: dict): ...

# YOUR application's existing data is in XML
xml_data = "<order><id>42</id></order>"
```

```
Integrating this third-party library DIRECTLY is impossible - its
interface expects JSON, but your application's existing data is
in a completely different format. Neither side can be MODIFIED
(the library is third-party; your existing XML data pipeline is
already established elsewhere).
```

This is directly Refactoring.guru's own canonical example — the Adapter pattern exists specifically
for exactly this situation: two genuinely incompatible interfaces that both need to keep working as
they already are.

## The Pattern

```python
class XMLToJSONAdapter:
    def __init__(self, analytics_library: AnalyticsLibrary):
        self._library = analytics_library

    def process(self, xml_data: str):
        json_data = self._convert_xml_to_json(xml_data)   # the TRANSLATION
        return self._library.process(json_data)

    def _convert_xml_to_json(self, xml_data: str) -> dict:
        # actual XML -> JSON conversion logic
        ...
```

```python
adapter = XMLToJSONAdapter(AnalyticsLibrary())
adapter.process(xml_data)   # the CALLER uses the adapter's own,
                              # familiar interface, unaware of the
                              # translation happening underneath
```

The adapter sits *between* the two incompatible interfaces, translating calls from one shape into
the other — neither the third-party library nor the existing application code needs to change at
all.

## A Real, Physical Analogy: Power Plug Adapters

```
A US laptop charger's plug doesn't fit a German wall socket -
neither the LAPTOP nor the WALL SOCKET can be changed. A physical
power adapter sits BETWEEN them, translating one plug standard
into the other.
```

This is directly Refactoring.guru's own, genuinely intuitive real-world analogy — and it captures
the pattern's essence precisely: an adapter is a *translator*, not a replacement for either side it
connects.

## A Real Software Use Case: Wrapping a Legacy or Third-Party API

```
Migrating from an OLD payment provider's API to a NEW one, but
large parts of the existing application still call methods
matching the OLD provider's interface - an Adapter implementing
the OLD interface, internally calling the NEW provider, lets the
migration happen GRADUALLY, without rewriting every existing call
site at once.
```

This is a genuinely common, practical use case beyond the abstract example — Adapter is often the
right tool specifically during a migration, letting old and new code coexist without a disruptive,
all-at-once rewrite.

## Common Mistakes

- Modifying the third-party or legacy interface directly instead of introducing an Adapter, when
  the original interface genuinely can't (or shouldn't) be changed.
- Letting an Adapter accumulate real business logic beyond pure translation, blurring its single,
  focused responsibility.
- Reaching for Adapter when the two interfaces are actually similar enough that a simpler refactor
  would resolve the incompatibility directly.

## ➡️ Next

Continue to [facade-pattern.md](facade-pattern.md) to see a related pattern for simplifying access
to a genuinely complex subsystem.
