# 🎣 Understanding CSRF

## Exploiting Trust, Not Injecting Code

[Cross-Site Scripting](../cross-site-scripting-xss/) injected attacker-controlled *code* into a
page. **Cross-Site Request Forgery (CSRF)** is genuinely different: no code injection at all —
instead, it tricks a victim's *browser* into making a real, authenticated request the victim never
actually intended, exploiting the browser's own automatic inclusion of session credentials.

## The Attack, Step by Step

```
1. Victim logs into their bank (my-bank.example.org) - receives
   a session cookie
2. WITHOUT logging out, the victim visits an attacker's
   malicious page (evil.com)
3. That malicious page contains a HIDDEN form targeting the
   bank's own transfer endpoint, auto-submitted via JavaScript:

<form action="https://my-bank.example.org/transfer" method="POST">
  <input type="hidden" name="recipient" value="attacker" />
  <input type="hidden" name="amount" value="1000" />
</form>
<script>document.querySelector("form").submit();</script>

4. The victim's BROWSER automatically includes the bank's own
   session cookie with this request - because that's simply how
   cookies work, regardless of which page initiated the request
5. The bank's server sees a VALID, authenticated request and
   processes the transfer
```

This is directly from MDN's own official explanation of the attack — the server has no way to
distinguish "the victim genuinely clicked a transfer button on our own site" from "the victim's
browser was tricked into submitting a hidden form on a completely different site," because both
requests arrive carrying the exact same valid session cookie.

## Why This Works: the Cookie Is Automatic, the Intent Is Not

```
CSRF is possible specifically when:
  - state-changing actions happen via ordinary HTTP requests
  - ONLY a cookie is used to verify the requester is authenticated
  - the request's parameters are PREDICTABLE (an attacker can
    guess or construct a valid-looking request)
```

This is the core insight worth holding onto: a cookie proves *which browser/session* is making a
request, but says absolutely nothing about whether the *user* genuinely intended that specific
action — CSRF exploits exactly this gap between "authenticated" and "intentional."

## Why This Isn't the Same as XSS

```
XSS: the attacker's CODE runs inside the VICTIM's own page,
     directly, with full access to that page's DOM and data

CSRF: NO attacker code ever runs on the bank's site at all - the
     attacker's page simply causes the VICTIM's browser to send a
     legitimate-LOOKING request TO the bank, from a page the
     victim never trusted in the first place
```

This distinction genuinely matters for choosing the right defense — XSS defenses (output escaping,
CSP) don't prevent CSRF at all, since no code injection into the target site is involved; CSRF needs
its own, separate defense mechanism entirely.

## Common Mistakes

- Assuming session-cookie authentication alone is sufficient proof of genuine user intent, missing
  that a browser includes cookies automatically regardless of which page initiated the request.
- Confusing CSRF with XSS, and applying XSS defenses (output escaping) that do nothing to actually
  prevent CSRF.
- Believing a victim must be actively using the vulnerable site at the time of the attack — they
  only need to have an active, unexpired session, even in a background tab.

## ➡️ Next

Continue to [csrf-protection.md](csrf-protection.md) to see the actual defenses that close this
gap between "authenticated" and "intentional."
