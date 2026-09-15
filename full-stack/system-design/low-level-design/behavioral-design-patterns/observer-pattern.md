# 📡 Observer Pattern

## Behavioral Patterns: How Objects Communicate

[Structural Design Patterns](../structural-design-patterns/) covered how objects compose together.
**Behavioral patterns**, covered in this final module, address how objects *communicate* and
distribute responsibility for behavior between them — starting with Observer, one of the most
widely-recognized patterns of all, already used implicitly throughout this repository's own
event-driven code.

## The Problem: Notifying an Unknown, Changing Set of Interested Parties

```python
# WITHOUT Observer - the publisher would need to know, by NAME,
# every single object that might ever care about a change
class Store:
    def restock(self, product):
        email_customer_1(product)   # HARDCODED, specific customers -
        email_customer_2(product)    # genuinely doesn't scale, and
        sms_customer_3(product)       # can't handle NEW subscribers
```

Per Refactoring.guru's own framing: "the actual set of objects is unknown beforehand or changes
dynamically" — a store genuinely can't hardcode every future customer who might want a restock
notification, especially as customers subscribe and unsubscribe over time.

## The Pattern

```python
class Publisher:
    def __init__(self):
        self._subscribers = []

    def subscribe(self, subscriber):
        self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        self._subscribers.remove(subscriber)

    def notify(self, event):
        for subscriber in self._subscribers:
            subscriber.update(event)

class Store(Publisher):
    def restock(self, product):
        self.notify(f"{product} is back in stock!")

class EmailSubscriber:
    def update(self, event):
        print(f"Emailing: {event}")
```

```python
store = Store()
store.subscribe(EmailSubscriber())
store.restock("Wireless Headphones")   # notifies EVERY currently
                                          # subscribed observer,
                                          # whoever they are
```

The `Store` never needs to know the concrete type or identity of any specific subscriber — it
communicates purely through the shared `update()` interface, and subscribers can join or leave
dynamically at any time.

## A Real, Familiar Analogy: Magazine Subscriptions

```
You subscribe to a magazine ONCE - you don't need to keep
visiting the store to check for a new issue. The PUBLISHER sends
it directly, to YOU and every OTHER current subscriber, the
moment a new issue is actually published.
```

This is directly Refactoring.guru's own real-world analogy — and it's genuinely why the pattern's
own vocabulary (publisher/subscriber) comes directly from this exact real-world concept.

## Where This Pattern Is Already Used Throughout This Repository

```
Every event listener (a button's onClick handler, an EventEmitter
in Node.js, a webhook receiver per Real-Time Communication,
earlier in this repository's Backend domain) is, structurally, an
application of Observer - a PUBLISHER (the event source)
notifying an unknown, dynamic set of SUBSCRIBERS (the registered
handlers).
```

This is a genuinely useful realization — Observer isn't a specialized, rarely-used pattern; it's the
formal name for an interaction shape already used constantly throughout real, everyday application
code.

## Common Mistakes

- Hardcoding specific subscriber references directly into a publisher, rather than maintaining a
  genuinely dynamic, addable/removable subscription list.
- Forgetting to provide an `unsubscribe()` mechanism, causing subscribers that should have stopped
  listening to keep receiving notifications indefinitely (a genuine memory-leak risk in long-running
  applications).
- Having subscribers depend on the *order* in which they're notified, when Observer's contract
  doesn't actually guarantee any particular notification order.

## ➡️ Next

Continue to [strategy-pattern.md](strategy-pattern.md) to see a pattern for choosing between
interchangeable algorithms at runtime.
