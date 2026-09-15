# 💉 Injection Attacks

## 📚 Overview

[The Security Mindset](../the-security-mindset/) named injection as one of the most severe OWASP
Top 10 categories. This module covers it in full, hands-on depth: the general mechanism, SQL
injection with real, documented breach context, command injection, and the general prevention
principle — structural separation of data from instructions — that defends against both, and
generalizes to injection risks beyond what this module explicitly covers.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain the injection mechanism: untrusted input combined with executable instructions without
  proper separation.
- Prevent SQL injection with parameterized queries, and explain why they work regardless of input
  content.
- Prevent command injection with `execFile()` instead of `exec()`.
- Apply the general "structural separation" principle to recognize and defend against an injection
  risk this module doesn't explicitly cover.

## 📋 Prerequisites

- [The Security Mindset](../the-security-mindset/) — this module's defense-in-depth application builds directly on the principles covered there.
- [Schema Validation with Zod](../../artificial-intelligence/schema-validation-with-zod/) — the input-validation layer referenced as one part of this module's defense-in-depth strategy.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [understanding-injection.md](understanding-injection.md) | The general injection mechanism, and why it's not limited to SQL |
| [sql-injection.md](sql-injection.md) | The 2015 TalkTalk breach, the vulnerable pattern, and parameterized queries |
| [command-injection.md](command-injection.md) | The same pattern applied to shell commands, and `execFile()` as the fix |
| [preventing-injection-attacks.md](preventing-injection-attacks.md) | The general "structural separation" principle and a practical checklist; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you write any code that builds a database query, shell command, or other
interpreter call incorporating user input — this is directly, immediately applicable to real,
common code patterns.

**Skim** if you already consistently use an ORM and never call `exec()` with user input — but read
[preventing-injection-attacks.md](preventing-injection-attacks.md) regardless, since its general
principle applies beyond this module's two specific examples.

## 🧠 Knowledge Check

<details>
<summary>Why do parameterized queries prevent SQL injection regardless of what characters the attacker's input actually contains?</summary>

The query's structure (the SQL instructions) and the user-supplied value are sent to the database
driver as genuinely separate pieces — the placeholder marks exactly where a literal value goes, and
the driver never interprets that value as part of the query's own syntax, no matter its content.
This is why it defends against every possible malicious string, not just specific, anticipated ones.

</details>

<details>
<summary>Why is <code>execFile()</code> safer than <code>exec()</code> for running a command with user-supplied input?</summary>

`exec()` spawns a shell that parses the entire command string, so shell metacharacters (like `;` or
`|`) in user input can be interpreted as separate commands. `execFile()` doesn't spawn a shell by
default — it passes arguments directly to the executable as literal values, with no shell present to
misinterpret them.

</details>

## 📚 References

- [OWASP - Top Ten 2025](https://top10.owasp.org/2025) — Injection remains a current, severe category
- [2015 TalkTalk Data Breach (Wikipedia, citing ICO findings)](https://en.wikipedia.org/wiki/2015_TalkTalk_data_breach) — the real breach this module's SQL injection coverage is grounded in
- [Node.js - Child Process Documentation](https://nodejs.org/api/child_process.html) — official documentation for `exec()` vs. `execFile()` and their security warnings

## ➡️ Continue Your Learning Path

Continue to [Cross-Site Scripting (XSS)](../cross-site-scripting-xss/) to see a different injection
category — one that targets the browser rather than a server-side interpreter.
