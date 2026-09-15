# 🖱️ Understanding Clickjacking

## Tricking a Click, Not Forging a Request

[CSRF](understanding-csrf.md) forges an entire request without any user interaction at all.
**Clickjacking** takes a genuinely different approach: it tricks a *real, legitimate user* into
actually clicking something — while making them believe they're clicking something else entirely.

## The Core Mechanism: an Invisible, Overlaid iframe

```html
<style>
  iframe {
    opacity: 0.0001;   /* nearly invisible, but still receives clicks */
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 2;
  }
</style>

<div>Click here to claim your free prize!</div>
<iframe src="https://mybank.example.org/transfer?amount=1000&to=attacker"></iframe>
```

```
The victim SEES a big, tempting "claim your prize" button - but
is ACTUALLY clicking an invisible, precisely-positioned iframe
containing the REAL bank's transfer confirmation button, layered
directly on top.
```

The victim genuinely, deliberately clicks — that's exactly what makes this attack effective: it
doesn't rely on tricking a request the way CSRF does; it tricks the *user's own real click*,
landing it on a hidden, legitimate element instead of the visible decoy underneath it.

## Why This Requires the Victim to Already Be Logged In

```
The invisible iframe loads the REAL bank's page - if the victim
has an active session (cookie) with that bank, the page loads
already AUTHENTICATED, and the victim's genuine click acts as a
genuine, authenticated confirmation.
```

This is exactly the same underlying exploitation of an active authenticated session already covered
in [understanding-csrf.md](understanding-csrf.md) — clickjacking and CSRF both rely on a victim
having an active session with the target site, just exploiting it through entirely different
mechanisms (a forged request vs. a tricked genuine click).

## Real-World Clickjacking Targets

```
- Social media "like" or "follow" buttons hidden under a decoy
- A bank/payment confirmation button (the classic, high-stakes
  example)
- Account settings toggles (e.g. "make my profile public")
  layered under a game or quiz
```

This is genuinely broader than financial transactions — any single-click, consequential action
(changing a privacy setting, granting a permission) is a viable clickjacking target if the site
allows itself to be embedded in an attacker's frame at all.

## The Attacker Never Needs to Bypass Any Authentication

```
Clickjacking does NOT steal credentials, does NOT forge a
request, and does NOT inject code - it simply misdirects a
GENUINE, real click from an ALREADY-authenticated user onto a
hidden, legitimate element.
```

This is worth stating explicitly: clickjacking's entire premise depends on the target page being
embeddable in a frame at all — which is exactly the vulnerability
[preventing-clickjacking.md](preventing-clickjacking.md), next in this module, directly closes.

## Common Mistakes

- Assuming clickjacking requires stealing credentials or injecting code, missing that it works
  purely by misdirecting a genuine, already-authenticated user's own real click.
- Underestimating clickjacking's real-world impact because a single click "seems minor" — a single
  well-placed click can trigger a genuinely consequential action (a payment, a permission grant).
- Focusing security review only on forms and API endpoints, overlooking that ANY page allowing
  itself to be framed is a potential clickjacking target.

## ➡️ Next

Continue to [preventing-clickjacking.md](preventing-clickjacking.md) to see the direct, effective
defense: simply preventing the page from being framed at all.
