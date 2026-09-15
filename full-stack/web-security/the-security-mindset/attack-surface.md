# 🎯 Attack Surface

## Everything an Attacker Could Possibly Interact With

An application's **attack surface** is the complete set of every point where an outside actor —
legitimate user or attacker — can actually interact with the system: every API endpoint, every
form field, every URL parameter, every third-party integration, every open network port. Threat
modeling (per [threat-modeling-basics.md](threat-modeling-basics.md)) needs to know this surface
exists before it can systematically examine it.

## Mapping a Real Application's Attack Surface

```
- Every PUBLIC API endpoint (not just the ones with a frontend UI
  built for them — an attacker can call ANY endpoint directly)
- Every FORM FIELD and URL PARAMETER
- Every FILE UPLOAD capability
- Every THIRD-PARTY integration and webhook receiver
- Every OPEN network port (per container-networking.md's expose-
  vs-publish distinction, earlier in this repository)
- Authentication and session mechanisms themselves
```

This list is deliberately broader than "the pages a user actually sees" — an API endpoint that
exists but has no UI built for it is still genuinely part of the attack surface, since nothing
prevents an attacker from calling it directly, bypassing the frontend entirely.

## Minimizing Attack Surface: Less Exposed Is Genuinely Safer

```
Every ADDITIONAL exposed endpoint, feature, or open port is
ANOTHER place a vulnerability could exist - reducing what's
actually exposed, to only what's genuinely necessary, directly
reduces the total realistic risk.
```

```
A debug/admin endpoint left accidentally accessible in
production, with no genuine legitimate use for regular traffic:
→ pure, unnecessary attack surface, providing zero benefit while
  adding real risk
```

This is a directly practical application of the least-privilege principle from
[security-principles.md](security-principles.md), applied at the *system* level rather than the
individual-credential level — every unnecessary exposed feature is unnecessary risk with no
offsetting benefit.

## Third-Party Dependencies Are Part of the Attack Surface Too

```
A vulnerability in a THIRD-PARTY npm package your application
depends on is JUST AS REAL a part of your attack surface as a
vulnerability in your own, directly-written code.
```

This directly connects to OWASP's own 2025 **Software Supply Chain Failures** category from
[understanding-web-security.md](understanding-web-security.md) — a dependency's own security
posture is genuinely part of an application's real attack surface, not somehow exempt just because
the vulnerable code wasn't written in-house.

## Reviewing Attack Surface as Part of Ordinary Development

```
Every NEW endpoint, every NEW feature, every NEW third-party
integration EXPANDS the attack surface - worth asking, as a
deliberate question during design and review: "does this
genuinely need to be exposed this broadly?"
```

This is the practical, ongoing discipline this file leads to: attack surface isn't a one-time
audit, it's a question worth revisiting continuously, as an application evolves and grows —
directly the same "review every line" discipline already established in
[Engineering WITH AI](../../artificial-intelligence/engineering-with-ai/)'s pre-ship checklist,
now applied specifically through a security lens.

## Common Mistakes

- Assuming an endpoint is "safe" simply because no frontend UI links to it — an attacker interacts
  directly with the actual API, entirely independent of the frontend.
- Treating third-party dependencies as outside the scope of an application's own security
  responsibility, when a vulnerable dependency is just as real a risk as first-party code.
- Leaving debug, admin, or development-only endpoints accessible in a production deployment, adding
  pure risk with no legitimate production benefit.

## Module Summary

Across this module: **the security mindset** requires thinking like an attacker — someone
unconstrained by an application's intended UI or flow — and consulting OWASP's own current,
authoritative Top 10 as a real, evidence-based map of where applications actually fail (see
[understanding-web-security.md](understanding-web-security.md)); **core security principles** —
never trust input, least privilege, defense in depth, and failing securely — underlie nearly every
specific defense this domain's later modules cover (see
[security-principles.md](security-principles.md)); **threat modeling**, using a systematic
framework like STRIDE, turns the attacker mindset into a repeatable, design-time process,
dramatically cheaper than discovering the same flaw after it ships (see
[threat-modeling-basics.md](threat-modeling-basics.md)); and **attack surface** — every point an
outside actor can actually interact with, including third-party dependencies — should be
deliberately minimized and continuously reviewed as an application evolves, not audited once and
forgotten.
