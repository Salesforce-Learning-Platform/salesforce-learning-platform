# 🛡️ Understanding Web Security

## A New Domain, a New Way of Thinking

Every domain in this repository so far has focused on building something that *works*. Web
Security asks a genuinely different question: does it work *safely*, even when someone is
deliberately trying to make it fail, misbehave, or leak data it shouldn't? This module opens that
domain by establishing the core mindset shift every other module in this domain builds on.

## Thinking Like an Attacker

```
A DEVELOPER asks: "does this feature work correctly for a
  legitimate user, following the intended flow?"

An ATTACKER asks: "what happens if I DON'T follow the intended
  flow? What if I send data the form was never designed to
  receive? What if I call this API endpoint directly, skipping
  the UI entirely?"
```

This is the fundamental mental shift security requires: an attacker isn't bound by an application's
intended user interface or expected inputs at all — they interact directly with whatever the
*actual* underlying system accepts, probing for exactly the gap between "what the developer
assumed" and "what the code actually allows."

## The OWASP Top 10: An Industry Map of What Actually Goes Wrong

```
OWASP (Open Web Application Security Project) maintains the
"Top 10" - a periodically updated, broad-consensus list of the
MOST CRITICAL web application security risks, based on real,
observed data across the industry.
```

The current OWASP Top 10:2025 list: **Broken Access Control**, **Security Misconfiguration**,
**Software Supply Chain Failures**, **Cryptographic Failures**, **Injection**, **Insecure Design**,
**Authentication Failures**, **Software or Data Integrity Failures**, **Security Logging and
Alerting Failures**, and **Mishandling of Exceptional Conditions**. This isn't a theoretical or
academic list — it's compiled from real, observed vulnerability data across the industry, making it
a genuinely reliable map of where real applications actually fail in practice. This domain's
remaining modules cover the most common and severe of these categories in hands-on depth.

## Why This List Changes Over Time

```
The 2021 list and the 2025 list are NOT identical - some
categories were merged, renamed, or reprioritized (for instance,
"Software Supply Chain Failures" is a NEW 2025 category, directly
reflecting the industry's growing real-world exposure to
compromised dependencies).
```

This is worth understanding explicitly: security isn't a fixed, memorized checklist — the actual
landscape of real-world risk shifts as technology and attack patterns evolve, which is exactly why
consulting OWASP's own current, authoritative list matters more than relying on an older,
memorized version.

## Security Is Everyone's Responsibility, Not a Separate Team's

```
A vulnerability introduced in ANY layer - frontend, backend,
infrastructure, even AI-generated code (per Engineering WITH AI,
earlier in this repository) - is a REAL vulnerability, regardless
of which team or role wrote it.
```

This directly echoes [Engineering WITH AI](../../artificial-intelligence/engineering-with-ai/)'s
core lesson from earlier in this repository — security review deserves the same rigor and
ownership as any other code review, and treating it as "someone else's job" is exactly how real
vulnerabilities slip through.

## Common Mistakes

- Assuming a vulnerability is unlikely because "no legitimate user would do that" — an attacker is
  not a legitimate user, and is specifically looking for exactly what a legitimate user wouldn't do.
- Treating a memorized, possibly outdated security checklist as a substitute for consulting OWASP's
  own current, authoritative Top 10.
- Treating security as a separate team's exclusive responsibility rather than an integrated part of
  every developer's own work.

## ➡️ Next

Continue to [security-principles.md](security-principles.md) to see the core, timeless principles
that underlie defending against every category on that list.
