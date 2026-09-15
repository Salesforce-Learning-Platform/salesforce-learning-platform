# 🕵️ Proxy Pattern

## Controlling Access, Not Simplifying or Translating It

[facade-pattern.md](facade-pattern.md) simplified access to a complex subsystem;
[adapter-pattern.md](adapter-pattern.md) translated between incompatible interfaces. **Proxy**
solves a genuinely different problem: providing a stand-in for a real object that controls *access*
to it — the same public interface as the real object, but with real logic interposed before (or
after) each call actually reaches it.

## The Pattern

```python
class RealImage:
    def __init__(self, filename):
        self.filename = filename
        self._load_from_disk()   # GENUINELY expensive - happens at
                                    # construction time

    def _load_from_disk(self):
        print(f"Loading {self.filename} from disk...")

    def display(self):
        print(f"Displaying {self.filename}")

class ImageProxy:   # SAME interface as RealImage - display()
    def __init__(self, filename):
        self.filename = filename
        self._real_image = None   # NOT loaded yet

    def display(self):
        if self._real_image is None:
            self._real_image = RealImage(self.filename)   # loaded
        self._real_image.display()                          # LAZILY,
                                                               # only when
                                                               # genuinely needed
```

```python
image = ImageProxy("large-photo.jpg")   # NOTHING loaded yet -
                                          # genuinely cheap to create
# ... later, only IF actually displayed:
image.display()   # NOW the expensive load genuinely happens
```

This is a **lazy-loading (virtual) proxy** — the real, expensive object is only actually constructed
the moment it's genuinely needed, not the instant a reference to it is created.

## Other Common Proxy Purposes

```
ACCESS control: check permissions BEFORE forwarding a call to the
  real object

CACHING: return a CACHED result for a repeated call, rather than
  hitting the real, expensive object again

LOGGING: record every call BEFORE forwarding it to the real object

REMOTE proxy: represents an object that ACTUALLY lives on a
  different server/process - a common shape behind RPC/gRPC
  client stubs
```

Each of these shares the exact same structural shape — an object implementing the same interface as
the real one, interposing real logic before delegating (or choosing not to delegate) to the actual,
underlying object.

## Proxy vs. Decorator: the Precise Distinction

```
PROXY:     controls ACCESS to an object - the interface stays
  IDENTICAL, and the proxy may choose NOT to forward a call at all
  (an access-denied case, a cache hit)

DECORATOR: EXTENDS an object's behavior - the client explicitly
  chooses to layer decorators together, and every call genuinely
  DOES reach the wrapped object eventually
```

Per Refactoring.guru's own direct comparison, this is the precise, structural distinction worth
holding onto — both patterns wrap an object behind the same interface, but Proxy's own purpose is
*managing access* (which can mean withholding it entirely), while Decorator's purpose is genuinely
*adding capability* on top of behavior that always still happens.

## A Real Use Case: Database Connection Proxies

```
A DatabaseProxy checks whether the CALLING code has genuine
permission to run a given query BEFORE forwarding it to the real
database connection - unauthorized calls are REJECTED by the
proxy itself, NEVER even reaching the real database at all.
```

## Common Mistakes

- Confusing Proxy with Decorator simply because both "wrap" an object behind the same interface,
  missing their genuinely different purposes (access control vs. behavior extension).
- Adding so much unrelated logic to a proxy that it stops being a focused access-control layer and
  becomes its own, separate subsystem.
- Using a caching proxy without a genuine cache-invalidation strategy, silently serving stale data
  indefinitely.

## ➡️ Next

Continue to [decorator-pattern.md](decorator-pattern.md) to see the pattern this file just
contrasted Proxy against, in full detail.
