# 📦 Dependency Vulnerabilities and Supply-Chain Awareness

## Someone Else's Code, Your Application's Risk

[attack-surface.md](../the-security-mindset/attack-surface.md), earlier in this domain, already
named third-party dependencies as genuinely part of an application's real attack surface. This file
covers the practical tooling for actually managing that risk on an ongoing basis, directly reflecting
OWASP's own current **Software Supply Chain Failures** category from
[understanding-web-security.md](../the-security-mindset/understanding-web-security.md).

## `npm audit`: Scanning for Known Vulnerabilities

```bash
npm audit
```

```
npm audit checks every dependency (direct, dev, bundled, and
optional) against a database of KNOWN, publicly disclosed
vulnerabilities - reporting each one's severity and, where
available, a fixed version.
```

This is a genuinely simple, immediately actionable check — a single command, built directly into
npm itself, surfacing exactly which of an application's dependencies carry a known, disclosed
security issue right now.

## `npm audit fix`: Automated Remediation, With Real Limits

```bash
npm audit fix
```

```
Per npm's own documentation, this updates vulnerable packages to
a FIXED version - but ONLY within the semver range already
declared in package.json. A fix requiring a MAJOR version bump is
NOT applied automatically, since that could introduce genuinely
breaking changes.
```

```bash
npm audit fix --force   # forces major-version updates too -
                          # genuinely risks breaking the application
```

This distinction matters practically: `npm audit fix` alone is safe to run routinely, but
`--force` should be a deliberate, tested decision — not a reflexive habit — since it can pull in
breaking API changes the application code isn't actually prepared for.

## Making This a Routine Part of Development, Not a One-Time Check

```yaml
# Adding npm audit to the CI pipeline, per CI/CD Pipelines,
# earlier in this repository's Production Systems domain
- name: Audit dependencies
  run: npm audit --audit-level=high
```

This directly applies [Automated Testing in a Pipeline](../../production-systems/ci-cd-pipelines/automated-testing.md)'s
"catch problems on every change, automatically" principle from earlier in this repository — running
a dependency audit as part of CI means a newly disclosed vulnerability in an existing dependency
(or a genuinely vulnerable new dependency someone adds) is surfaced automatically, not discovered
months later during an unrelated, manual check.

## Being Deliberate About What Gets Added as a Dependency

```
Before adding a NEW dependency, worth asking:
  - is it ACTIVELY maintained (recent commits, responsive to
    reported issues)?
  - does it have a REASONABLE number of its OWN transitive
    dependencies (each one is ADDITIONAL attack surface)?
  - is the SPECIFIC functionality genuinely worth the added
    supply-chain risk, or could it be written directly, simply,
    in-house instead?
```

This is a genuinely practical, everyday discipline — not every small utility function needs to be
an external dependency, and each one added is a small, permanent addition to the application's real
attack surface, worth weighing deliberately rather than adding reflexively.

## Common Mistakes

- Running `npm audit fix --force` reflexively without testing afterward, risking a genuinely
  breaking change reaching production undetected.
- Treating a dependency audit as a one-time, manual check rather than an automated, routine part of
  CI — missing newly disclosed vulnerabilities in already-installed dependencies.
- Adding a new dependency for trivially simple functionality without weighing its actual maintenance
  status and transitive dependency footprint.

## ➡️ Next

Continue to [input-validation.md](input-validation.md) to see this domain's recurring
input-validation principle brought together as one unified, practical discipline.
