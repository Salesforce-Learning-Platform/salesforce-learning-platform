# 🛡️ The Security Mindset

## 📚 Overview

This module opens the Web Security domain by establishing the mental shift every later module
builds on: thinking like an attacker, not just a developer building for the happy path. It covers
the OWASP Top 10 as an industry-verified map of real risk, the core principles behind nearly every
specific defense in this domain, a systematic threat-modeling process (STRIDE), and how to identify
an application's full attack surface.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain the mental shift from "does this work for a legitimate user?" to "what happens if someone
  doesn't follow the intended flow?"
- Name the current OWASP Top 10:2025 categories and explain why the list evolves over time.
- Apply the four core security principles: never trust input, least privilege, defense in depth,
  and fail securely.
- Walk a feature through the STRIDE threat-modeling framework.
- Identify and deliberately minimize an application's full attack surface.

## 📋 Prerequisites

- No prior security-specific experience assumed — this is the opening module of the Web Security domain.
- General familiarity with this repository's Backend domain is helpful, since examples reference real endpoints and forms.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [understanding-web-security.md](understanding-web-security.md) | The attacker mindset and the current OWASP Top 10:2025 |
| [security-principles.md](security-principles.md) | Never trust input, least privilege, defense in depth, fail securely |
| [threat-modeling-basics.md](threat-modeling-basics.md) | The STRIDE framework, applied to a real login form example |
| [attack-surface.md](attack-surface.md) | Mapping and minimizing every point an attacker can interact with; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** regardless of experience level — this module's mindset shift is the foundation every
other Web Security module assumes, and it's worth internalizing even if you already know specific
attack techniques.

**Skim** only if you've already completed formal security training covering the attacker mindset
and OWASP Top 10 elsewhere — the later modules in this domain still assume this foundation.

## 🧠 Knowledge Check

<details>
<summary>Why is "no legitimate user would do that" not a valid reason to dismiss a potential vulnerability?</summary>

An attacker is not a legitimate user, and isn't bound by an application's intended UI or flow. They
interact directly with whatever the underlying system actually accepts — sending malformed data,
calling an API endpoint directly, or skipping steps a legitimate user would never skip — specifically
looking for the gap between what a developer assumed and what the code actually allows.

</details>

<details>
<summary>According to the "fail securely" principle, what should an authorization check do if it encounters an unexpected error?</summary>

Default to denying access, never granting it. An error-handling path should never accidentally
become a path to broader, unintended access — the safe default in any failure case is to deny, so
an unrelated bug never turns into a security hole.

</details>

## 📚 References

- [OWASP - Top Ten 2025](https://top10.owasp.org/2025) — the official, current OWASP Top 10 list this module's risk categories are drawn from
- [Security Compass - What Is STRIDE in Threat Modeling?](https://www.securitycompass.com/blog/stride-in-threat-modeling/) — a well-known explanation of Microsoft's STRIDE framework

## ➡️ Continue Your Learning Path

Continue to [Injection Attacks](../injection-attacks/) to see the first, and one of the most
severe, categories from the OWASP Top 10 covered in full, hands-on depth.
