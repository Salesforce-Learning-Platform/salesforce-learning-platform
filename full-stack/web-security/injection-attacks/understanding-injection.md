# 💉 Understanding Injection

## When User Input Becomes Executable Code

**Injection** is what happens when an application takes untrusted input and inserts it directly
into a command, query, or interpreter — without properly separating "data" from "instructions" —
letting an attacker's input be *executed* rather than merely *processed* as inert data.

## A Minimal, Concrete Example

```js
// VULNERABLE - user input concatenated directly into a SQL query
const query = `SELECT * FROM users WHERE email = '${userInput}'`;
```

```
If userInput is: ' OR '1'='1

The query BECOMES:
SELECT * FROM users WHERE email = '' OR '1'='1'

'1'='1' is ALWAYS true - this returns EVERY row in the users
table, not just one matching the intended email.
```

This is the core mechanism of every injection attack: the application's code and the attacker's
data get concatenated together into one string, and the underlying interpreter (here, a SQL
database) has no way to distinguish which part was the *intended* query and which part was
attacker-supplied data — it just executes the combined result as written.

## Why This Is #A05 on the Current OWASP Top 10

```
Injection remains one of the most SEVERE and well-understood
categories on OWASP's Top 10:2025 (per understanding-web-
security.md, earlier in this domain) - severe because a
successful injection can grant an attacker DIRECT access to read,
modify, or delete data never meant to be exposed at all.
```

Injection's severity comes from *what* it grants an attacker: not a minor information leak, but
often direct, unrestricted access to an application's actual underlying data store — genuinely one
of the worst-case outcomes for a web application's security.

## Injection Isn't Limited to SQL

```
SQL INJECTION      → untrusted input inserted into a SQL query
                      (covered in sql-injection.md, next in this
                      module)

COMMAND INJECTION   → untrusted input inserted into an OS shell
                      command (covered in command-injection.md)

Other forms exist too: NoSQL injection, LDAP injection, template
injection - the SAME underlying mechanism, applied to a different
interpreter.
```

This is a genuinely important generalization: injection is a *pattern*, not a single specific
vulnerability — anywhere untrusted input gets combined with executable instructions for some
interpreter, without proper separation, the same fundamental risk exists.

## The Core Insight: Separate Data From Instructions

```
The FUNDAMENTAL fix, covered in depth in preventing-injection-
attacks.md, is always some form of the SAME idea: use a mechanism
that keeps the INSTRUCTIONS (the query/command structure) and the
DATA (user input) STRUCTURALLY SEPARATE, so the interpreter can
never confuse one for the other.
```

Every specific defense this module covers — parameterized queries, safe command execution APIs —
implements this exact same underlying principle in a different context, which is worth holding onto
as the unifying idea behind everything that follows.

## Common Mistakes

- Assuming injection is "just a SQL problem," missing that the same fundamental vulnerability
  pattern applies to shell commands, NoSQL queries, and other interpreters.
- Believing input validation alone (checking for suspicious characters) is a sufficient defense,
  rather than the structural separation of data and instructions this file's later modules cover.
- Underestimating injection's severity because a specific instance "only" reads data, when the same
  underlying vulnerability commonly permits full read/write/delete access.

## ➡️ Next

Continue to [sql-injection.md](sql-injection.md) to see this mechanism in full depth, including a
real, documented breach caused by exactly this vulnerability.
