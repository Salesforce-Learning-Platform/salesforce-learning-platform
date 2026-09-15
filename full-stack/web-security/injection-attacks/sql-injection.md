# 🗄️ SQL Injection

## A Real Breach: TalkTalk, 2015

```
In October 2015, UK telecom TalkTalk suffered a breach affecting
156,959 customers - including 15,656 whose actual BANK ACCOUNT
DETAILS were exposed. The attackers used SQLmap, an automated SQL
injection tool, to exploit a LEGACY webpage inherited from a
company acquisition, running an outdated, unpatched MySQL version.

The UK's Information Commissioner's Office fined TalkTalk
£400,000 - a RECORD fine at the time - explicitly citing that SQL
injection is "a well understood method of cyber-attack for which
known defences exist," and that TalkTalk had already suffered TWO
prior SQL injection attacks earlier that same year without taking
remedial action.
```

This is a genuinely important, real detail beyond the technical mechanism: the vulnerability that
caused this breach had a publicly available patch for over *three years* before the attack — this
wasn't a novel, undiscoverable flaw, but a well-known, well-understood risk left unaddressed.

## The Vulnerable Pattern

```js
app.get("/users", (req, res) => {
  const email = req.query.email;
  db.query(`SELECT * FROM users WHERE email = '${email}'`);   // VULNERABLE
});
```

```
Attacker sends: GET /users?email=' OR '1'='1

Resulting query:
SELECT * FROM users WHERE email = '' OR '1'='1'

Returns EVERY user row - a direct, total data exposure.
```

An even more severe variant chains multiple statements together (`'; DROP TABLE users; --`),
potentially destroying data entirely — the exact severity depends on what the underlying database
driver and permissions actually allow, but the root cause is identical either way.

## The Fix: Parameterized Queries

```js
app.get("/users", (req, res) => {
  const email = req.query.email;
  db.query("SELECT * FROM users WHERE email = $1", [email]);   // SAFE
});
```

This is the concrete, structural fix [understanding-injection.md](understanding-injection.md)
pointed toward: `$1` is a **placeholder**, and `email` is passed *separately*, as data — never
concatenated into the query string itself. The database driver sends the query structure and the
actual value as genuinely distinct pieces, so no attacker-supplied string can ever be interpreted as
part of the query's own instructions, no matter what it contains.

## Why This Works Even Against a Cleverly Crafted Attack

```
email = "' OR '1'='1"

With parameterized queries, this entire string is treated as the
LITERAL VALUE to search for - the database looks for a user whose
email address is literally the text "' OR '1'='1" (which won't
exist), rather than interpreting any part of it as SQL syntax.
```

This is the genuine strength of this fix: it doesn't rely on detecting or filtering "suspicious"
characters at all — the entire class of attack becomes structurally impossible, since the database
driver never treats user-supplied data as anything other than a literal value, regardless of its
content.

## ORMs Provide This Protection by Default

```js
// Using an ORM (like Prisma, Sequelize, or Mongoose) - parameterized
// queries happen AUTOMATICALLY, without manual placeholder syntax
const user = await User.findOne({ where: { email: req.query.email } });
```

This directly connects to patterns already used throughout this repository's Backend domain — an
ORM's query-builder methods parameterize values automatically, which is exactly why raw, manually
concatenated SQL strings should be avoided whenever a safer, equivalent ORM method exists.

## Common Mistakes

- Concatenating user input directly into a SQL query string, even "just this once" for a seemingly
  low-risk internal tool.
- Relying on manual input sanitization (stripping quotes, escaping characters) instead of
  parameterized queries — sanitization is error-prone and easy to bypass with an unanticipated
  encoding or character sequence.
- Using raw SQL string concatenation inside an ORM's own "raw query" escape hatch, losing the
  automatic protection the ORM would otherwise provide.

## ➡️ Next

Continue to [command-injection.md](command-injection.md) to see the same underlying vulnerability
pattern applied to operating system commands instead of database queries.
