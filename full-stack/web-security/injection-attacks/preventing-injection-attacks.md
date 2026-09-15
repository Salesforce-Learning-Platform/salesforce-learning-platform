# 🛡️ Preventing Injection Attacks

## One Underlying Principle, Applied Consistently

[sql-injection.md](sql-injection.md) and [command-injection.md](command-injection.md) each covered
a specific fix — parameterized queries, `execFile`. This file names the general principle both
fixes actually implement, so it can be recognized and applied to *any* injection risk, including
ones this module hasn't explicitly covered.

## The General Principle: Structural Separation

```
EVERY effective injection defense does the SAME underlying thing:
keeps DATA and INSTRUCTIONS structurally separate, at the level
the interpreter itself understands - never relying on string
manipulation to keep them apart.
```

```
SQL injection fix:     placeholders ($1) + a separate parameter
                        array - the DATABASE DRIVER keeps them apart

Command injection fix: execFile()'s argument array - the OPERATING
                        SYSTEM keeps them apart (no shell parsing
                        involved at all)
```

Recognizing this as one general pattern — not two unrelated fixes — is what makes it possible to
correctly defend against an injection risk this module never explicitly named: NoSQL injection,
LDAP injection, template injection all have their own equivalent "keep data and instructions
structurally separate" mechanism worth specifically seeking out.

## Defense in Depth, Applied to Injection

```
Layer 1: INPUT VALIDATION - reject obviously malformed input early
  (per Schema Validation with Zod, earlier in this repository)
Layer 2: PARAMETERIZED QUERIES / execFile - the STRUCTURAL fix,
  genuinely preventing the attack regardless of input content
Layer 3: LEAST-PRIVILEGE database/system credentials - limits the
  DAMAGE even if Layers 1-2 somehow both failed
```

This directly applies [defense in depth](../the-security-mindset/security-principles.md), from
earlier in this domain: input validation alone is never sufficient on its own (it can be bypassed by
an unanticipated input), but combined with the structural fix and a least-privilege database
account, no single layer's failure leads directly to full compromise.

## Why Sanitization/Escaping Alone Is a Weaker Defense

```
Escaping/sanitizing SPECIFIC characters relies on the developer
correctly anticipating EVERY dangerous character or encoding, for
EVERY interpreter involved - genuinely easy to miss an edge case.

Structural separation (parameterized queries, execFile) makes the
entire CLASS of attack impossible, REGARDLESS of the input's
actual content.
```

This is the real, practical reason this module's fixes are preferred over manual sanitization —
structural separation doesn't require anticipating every possible malicious input pattern in
advance; it removes the *mechanism* the attack depends on entirely.

## A Practical Checklist for Any New Feature

```
☐ Does this feature build a database query using user input?
  → use parameterized queries / an ORM, never string concatenation
☐ Does this feature run a shell command using user input?
  → use execFile() with an argument array, never exec() with a
    concatenated string
☐ Does this feature pass user input to ANY other interpreter
  (a template engine, an LDAP query)?
  → find and use that interpreter's OWN structural-separation
    mechanism specifically
```

This checklist is deliberately generalizable well beyond this module's two specific examples — the
underlying question ("is user input reaching an interpreter without structural separation from
instructions?") applies to any new interpreter a feature might introduce.

## Common Mistakes

- Relying on input validation or sanitization as the *sole* defense, without the structural fix
  (parameterized queries, `execFile`) actually preventing the attack at its root.
- Applying this module's specific SQL and command-injection fixes without recognizing the
  underlying general principle, missing an equivalent fix needed for a different interpreter
  entirely.
- Assuming a least-privilege database account alone is sufficient protection, when it only limits
  damage *after* an injection has already succeeded — it's a layer of defense in depth, not a
  substitute for the structural fix itself.

## Module Summary

Across this module: **injection** occurs when untrusted input is combined with executable
instructions for some interpreter without structural separation, and it remains one of OWASP's most
severe risk categories precisely because a successful attack often grants direct, unrestricted data
access (see [understanding-injection.md](understanding-injection.md)); **SQL injection** — real and
severe, as the documented 2015 TalkTalk breach (156,959 customers affected, a record £400,000 fine)
shows — is prevented with parameterized queries, which structurally separate a query's instructions
from its data regardless of that data's content (see [sql-injection.md](sql-injection.md));
**command injection** applies the identical pattern to shell commands, prevented by using
`execFile()` (verified against Node.js's own official documentation) instead of `exec()`, avoiding
shell interpretation entirely (see [command-injection.md](command-injection.md)); and **preventing
injection generally** means recognizing structural data/instruction separation as the underlying
principle behind every specific fix, combined with input validation and least-privilege credentials
as complementary, defense-in-depth layers — never as substitutes for the structural fix itself.
