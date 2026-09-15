# ✅ Security in Practice

## 📚 Overview

This module closes out the Web Security domain by shifting from understanding individual attacks to
the practical, everyday habits that apply everything covered throughout this domain to a real
application: secure HTTP headers and secrets management, dependency vulnerability scanning, the
unifying input-validation principle, security testing (SAST/DAST), and a consolidated, practical
pre-ship checklist.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Apply Helmet's security headers and proper secrets/environment hygiene as fast, high-leverage
  defenses.
- Use `npm audit` and CI integration to catch known dependency vulnerabilities before they're
  exploited.
- Recognize allowlist-based input validation as the unifying principle behind nearly every defense
  in this domain.
- Distinguish SAST from DAST, and write automated tests that verify security defenses actually
  work.
- Apply a consolidated, practical checklist drawing on every module in the Web Security domain.

## 📋 Prerequisites

- Every prior module in the Web Security domain — this module consolidates and operationalizes them.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [security-headers.md](security-headers.md) | Helmet, secrets management, and per-environment secret hygiene |
| [dependency-security.md](dependency-security.md) | `npm audit`, CI integration, and deliberate dependency selection |
| [input-validation.md](input-validation.md) | The unifying allowlist-validation principle behind this domain's earlier defenses |
| [security-testing.md](security-testing.md) | SAST vs. DAST, writing security-specific tests, CI integration |
| [security-review-checklist.md](security-review-checklist.md) | A consolidated, practical pre-ship checklist; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** regardless of how much of this domain you've already covered — this module turns
individual attack knowledge into an actual, repeatable practice, which is where the real, ongoing
value lies.

**Skim** only the specific files covering practices your team already has fully automated and
enforced — but read [security-review-checklist.md](security-review-checklist.md) regardless, as a
genuine, consolidated reference.

## 🧠 Knowledge Check

<details>
<summary>Why is allowlist validation described as the unifying principle behind nearly every defense covered in this domain?</summary>

Parameterized queries (injection), output escaping (XSS), SSRF host allowlisting, and resolved-path
validation (path traversal) are all specific applications of the same underlying idea: defining what
is explicitly allowed, and rejecting everything else, rather than trying to anticipate and block
every possible malicious variant. This structural approach is more robust than any denylist, since
it doesn't depend on anticipating every attack in advance.

</details>

<details>
<summary>Why should this module's checklist be applied continuously during development rather than only right before shipping?</summary>

This directly follows the "cheaper at design time" principle from this domain's own threat-modeling
coverage — catching a missing defense while a feature is still being built is far less costly than
discovering it in a final review (or, worse, after it ships). Treating the checklist as a one-time,
last-minute gate also risks it becoming a rushed formality rather than a genuine, deliberate check.

</details>

## 📚 References

- [npm Docs - npm audit](https://docs.npmjs.com/cli/v11/commands/npm-audit/) — official documentation for dependency vulnerability scanning
- [Jit - What OWASP ZAP Can Do, and When to Use It](https://www.jit.io/resources/owasp-zap) — coverage of ZAP (formerly OWASP ZAP) as a DAST tool, including its current governance

## ➡️ Continue Your Learning Path

This is the final module of the Web Security domain. Continue to
[Low-Level Design](../../system-design/low-level-design/) to begin the System Design domain.
