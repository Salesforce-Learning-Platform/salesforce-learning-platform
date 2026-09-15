# 2️⃣ Open-Closed Principle

## The Principle, Stated Precisely

```
"Software entities should be OPEN for extension, but CLOSED for
modification."
```

This means: adding new behavior should be possible *without* changing existing, already-tested
code — this is exactly the notification-system example already previewed in
[what-is-low-level-design.md](../lld-foundations/what-is-low-level-design.md), now covered in full.

## Before: Adding a New Case Requires Modifying Existing Code

```python
class NotificationSender:
    def send(self, notification_type: str, message: str):
        if notification_type == "email":
            print(f"Emailing: {message}")
        elif notification_type == "sms":
            print(f"Texting: {message}")
        # adding "push" means MODIFYING this method, again
```

```
Every NEW notification type requires editing this SAME method -
risking breaking the EXISTING, already-working "email" and "sms"
cases while adding the new one.
```

This is the core violation: `NotificationSender` is never truly "done" — it must be *modified*,
repeatedly, every time a genuinely new requirement appears, with each modification risking the
already-working cases.

## After: Extended Through New Classes, Never Modified

```python
class Notification:
    def send(self, message: str): raise NotImplementedError

class EmailNotification(Notification):
    def send(self, message: str): print(f"Emailing: {message}")

class SMSNotification(Notification):
    def send(self, message: str): print(f"Texting: {message}")

class PushNotification(Notification):   # a NEW type, added WITHOUT
    def send(self, message: str):        # touching ANY existing class
        print(f"Push: {message}")

class NotificationSender:
    def send_all(self, notifications: list[Notification], message: str):
        for n in notifications:
            n.send(message)   # works for ANY Notification subtype,
                                # including ones that don't exist yet
```

Adding `PushNotification` required writing exactly one new class — `NotificationSender`,
`EmailNotification`, and `SMSNotification` are never touched at all. This is the direct, concrete
payoff of designing against an abstraction (the shared `Notification` interface) rather than a
concrete `if/elif` chain.

## Why "Closed for Modification" Doesn't Mean "Never Changes"

```
OCP means: adding a NEW use case shouldn't require modifying
EXISTING, working code.

It does NOT mean a class can never be changed AT ALL - a genuine
BUG in EmailNotification's own logic still needs to be fixed
directly, in that class.
```

This is a genuinely important nuance worth stating explicitly — OCP is about *extension* (new
behavior) not requiring modification, not an absolute prohibition on ever touching existing code for
any reason at all.

## The Mechanism: Polymorphism, Directly

```
OCP is achieved almost ENTIRELY through the SAME polymorphism
mechanism already covered in objects-and-classes.md, earlier in
this domain - a shared interface/abstract base class, with new
behavior added as NEW implementations of it.
```

## Common Mistakes

- Adding a new `if/elif` branch to an existing method as the default way to support a new case,
  rather than considering whether a new class implementing a shared interface would be more
  appropriate.
- Over-applying OCP preemptively — designing elaborate extension points for variations that may
  never actually materialize, adding complexity for a flexibility that's never actually used.
- Confusing "closed for modification" with "can never be touched," when genuine bug fixes to
  existing code remain entirely legitimate.

## ➡️ Next

Continue to
[liskov-substitution-principle.md](liskov-substitution-principle.md) to see what makes a subclass
genuinely substitutable for its parent class.
