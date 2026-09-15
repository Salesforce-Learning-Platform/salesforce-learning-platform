# 🔨 Brute Force and Credential Stuffing

## Attacking the Login Process Itself

[jwt-security.md](jwt-security.md) and [session-attacks.md](session-attacks.md) covered attacking
an *already-issued* credential. This file covers attacks against the login process itself —
repeatedly attempting to authenticate as someone else, at scale.

## Brute Force: Trying Many Passwords Against One Account

```
Attacker repeatedly submits login attempts for ONE known
username, trying MANY different password guesses - either
systematically (every possible combination) or against a
dictionary of common, real-world passwords.
```

This attack's practicality depends entirely on how weak the actual target password is, and how many
attempts the application allows before intervening — a genuinely strong, random password makes pure
brute force computationally infeasible, but a weak or common one can be guessed quickly.

## Credential Stuffing: Reusing Breached Credentials at Scale

```
Attacker takes a LIST of real username/password pairs LEAKED
from a COMPLETELY DIFFERENT, unrelated service's own past breach
- and tries those SAME pairs against YOUR application, betting
that some fraction of users REUSED the same password across
sites.
```

This is genuinely the more common, more effective attack in practice today — it doesn't require
guessing anything at all; it exploits the extremely common human behavior of password reuse across
different, unrelated services, using credentials already proven valid somewhere else.

## The Fix: Rate Limiting Login Attempts

```js
import rateLimit from "express-rate-limit";

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,   // 15 minutes
  max: 5,                      // 5 attempts per window, per IP
  message: "Too many login attempts, please try again later.",
});

app.post("/login", loginLimiter, handleLogin);
```

This directly applies [Rate Limits: Handling 429](../../artificial-intelligence/calling-llm-apis-properly/rate-limits-handling-429-backoff-and-retries.md)'s
underlying idea from earlier in this repository — the same rate-limiting concept, now applied
specifically to the login endpoint, makes both brute force and credential stuffing dramatically
slower and less practical to carry out at scale.

## Account Lockout: a Double-Edged Defense

```
LOCKING an account after N failed attempts stops brute force -
but can also be WEAPONIZED as a denial-of-service: an attacker
deliberately submits WRONG passwords for a KNOWN victim's account,
LOCKING THEM OUT of their own, legitimate account.
```

This is a genuinely important trade-off worth understanding explicitly — a naive lockout policy
trades one risk for another; a more sophisticated approach (per-IP rate limiting combined with
progressively increasing delays, rather than an outright account lock) avoids handing an attacker
this alternate way to cause real harm.

## CAPTCHA and Multi-Factor Authentication

```
CAPTCHA  → adds real friction specifically against AUTOMATED,
           scripted attack tools, without meaningfully
           inconveniencing a genuine, single human user

MFA      → even a FULLY correct password guess is insufficient
           alone - a second factor (an authenticator app, an SMS
           code) is still required
```

MFA in particular is a genuinely powerful mitigation against both brute force *and* credential
stuffing — even a perfectly guessed or reused password becomes insufficient on its own, closing off
the entire attack category rather than merely slowing it down.

## Common Mistakes

- Implementing no rate limiting at all on login endpoints, leaving both brute force and credential
  stuffing computationally cheap and fast for an attacker to carry out.
- Using a hard account lockout without considering it can be weaponized to lock a legitimate user
  out of their own account.
- Treating a strong password requirement alone as sufficient, when credential stuffing exploits
  password reuse regardless of how strong the original password actually was.

## ➡️ Next

Continue to [credential-security.md](credential-security.md) to see how credentials themselves
should actually be stored and handled to limit the damage from a future breach.
