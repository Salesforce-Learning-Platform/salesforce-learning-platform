# 🎯 Threat Modeling Basics

## Turning "Think Like an Attacker" Into a Repeatable Process

[understanding-web-security.md](understanding-web-security.md) established the attacker mindset as
a general disposition. **Threat modeling** turns that mindset into a structured, repeatable process
— a deliberate exercise for identifying a specific system's actual, realistic threats before they're
ever exploited, rather than discovering them after an incident.

## STRIDE: A Widely-Used Threat Modeling Framework

```
Developed by Microsoft, STRIDE categorizes threats into six types:

S poofing                → pretending to be someone/something else
T ampering                → unauthorized modification of data
R epudiation               → denying having performed an action
I nformation Disclosure    → exposing data to those unauthorized
                             to see it
D enial of Service         → disrupting legitimate availability
E levation of Privilege    → gaining MORE access than intended
```

STRIDE gives a threat-modeling exercise a concrete, systematic checklist to work through for a
specific feature — rather than trying to imagine "what could go wrong?" unguided, each category
prompts a specific, focused question worth asking deliberately.

## Applying STRIDE to a Real Feature: a Login Form

```
S poofing: could an attacker impersonate another user by guessing
  or stealing their credentials?
T ampering: could a request's data (e.g. a hidden "role" field)
  be modified in transit to grant unintended access?
R epudiation: if a user changes their password, is there a
  record proving THEY genuinely did it (not someone else, later
  denying it)?
I nformation Disclosure: does a failed login attempt reveal
  WHETHER a given email address exists in the system at all?
D enial of Service: could an attacker LOCK OUT a legitimate user
  by repeatedly submitting wrong passwords, triggering an account
  lockout?
E levation of Privilege: could a regular user's session somehow
  be used to perform an ADMIN-only action?
```

Walking through even one small, familiar feature — a login form — against all six STRIDE
categories surfaces genuinely specific, concrete questions worth deliberately answering, well
beyond a vague, general "is this secure?" — several of these specific questions map directly onto
[Authentication Attacks](../../web-security/authentication-attacks/), covered later in this domain.

## Data Flow Diagrams: Mapping Where Data Actually Moves

```
User Browser → [HTTPS] → Backend API → [internal network] →
Database

Each ARROW is a place data crosses a boundary - and each
boundary is a place worth asking the STRIDE questions.
```

A simple data flow diagram — even a rough sketch — helps identify exactly *where* a system's trust
boundaries actually are, directly building on
[hybrid-logic-ai-and-code.md](../../artificial-intelligence/function-calling-tool-calling/hybrid-logic-ai-and-code.md)'s
earlier point about trusted vs. untrusted context: threat modeling systematically asks this same
question at every single boundary a system's data actually crosses.

## When to Actually Do This

```
BEFORE building a genuinely new, security-sensitive feature
(authentication, payments, access control) - identifying real
threats at DESIGN time is far cheaper than discovering them after
the feature ships.
```

This is the real, practical value of threat modeling as a *deliberate* exercise — catching a design
flaw before a single line of code is written is dramatically cheaper than fixing a vulnerability
already live in production, exactly the same "shift left" reasoning already established for
[automated-testing.md](../../production-systems/ci-cd-pipelines/automated-testing.md)'s CI checks
earlier in this domain.

## Common Mistakes

- Treating threat modeling as a one-time exercise done once, ever, rather than revisiting it when a
  feature's design meaningfully changes.
- Skipping threat modeling for "small" features, when even a simple login form (per this file's own
  example) surfaces genuinely real, specific threats worth deliberately addressing.
- Threat modeling without a systematic framework (like STRIDE), relying on unguided intuition that
  tends to miss entire categories of real risk.

## ➡️ Next

Continue to [attack-surface.md](attack-surface.md) to see how to identify everything a threat
model actually needs to cover in the first place.
