# 🔎 Reviewing AI-Generated Code: When to Trust It, When Not To

## AI-Generated Code Is Still Just Code — Review It Like Code

```
The fact that AI wrote it changes NOTHING about the review
standard it should be held to - the same code review discipline
that applies to a human teammate's pull request applies here,
in full.
```

This is the single most important mental shift: AI-generated code isn't a special category that
gets a pass on review, nor is it inherently more suspect than human-written code — it's simply code,
subject to the same review standard as anything else entering the codebase.

## A Practical Trust Spectrum, Not a Binary

```
HIGH-CONFIDENCE, easy to verify (formatting a date, a simple
CRUD endpoint matching an existing pattern):
  → a quick read-through is often genuinely sufficient

LOW-CONFIDENCE, hard to verify at a glance (a concurrency fix, a
security-sensitive auth check, a complex algorithm):
  → deserves the SAME depth of scrutiny as the highest-stakes
    code a human would write
```

Not every line of AI-generated code needs the same level of scrutiny — but the *decision* about how
much scrutiny a given piece of code needs should be made deliberately, based on its actual risk and
complexity, never based on "an AI wrote it, so it's probably fine."

## Specific Things to Actually Check

```
- Does it handle the EDGE CASES the prompt didn't explicitly
  mention (empty input, null, a network failure)?
- Does it actually match the codebase's EXISTING patterns, or did
  it quietly introduce a new, inconsistent approach?
- Are there SECURITY implications - a new endpoint without auth
  checks, an unescaped user input, a hardcoded secret?
- Does the ERROR HANDLING match this domain's own discipline (per
  Error Handling in AI Applications), or does it silently swallow
  failures?
```

These are exactly the categories a thorough human code review already checks — AI-generated code
doesn't need a different checklist, it needs the *same* checklist applied without skipping steps
just because the code compiled and looked reasonable on a first read.

## A Concrete Example: Catching a Subtle Bug

```python
# AI-generated code, looks correct at a glance:
def get_user_orders(user_id):
    return db.query(f"SELECT * FROM orders WHERE user_id = {user_id}")
```

```
A careful review catches: this is a SQL INJECTION vulnerability -
string interpolation directly into a query, instead of a
parameterized query. The code RUNS correctly for a normal
user_id, which is exactly why a superficial "does it work?" check
would miss it.
```

This is a genuinely realistic example of the risk: code that runs correctly for the happy path can
still contain a serious flaw a quick functional test would never surface — which is precisely why
reviewing AI-generated code means reading it with the same critical eye as any other code, not
just running it once and moving on.

## Running Tests Is Necessary, Not Sufficient

```
Passing tests confirm: the code does what the TESTS check for

Passing tests do NOT confirm: the code is secure, handles every
realistic edge case, or fits the codebase's actual conventions
```

This directly parallels
[Frontend Testing Fundamentals: The Testing Pyramid](../../frontend/testing/frontend-testing-fundamentals/the-testing-pyramid.md)'s
core lesson — tests build *confidence*, they don't provide a *guarantee*, especially against tests
an AI tool itself may have also generated and that might share the same blind spots as the
implementation.

## Common Mistakes

- Treating "it passed the tests" as equivalent to "it's correct and safe," when the tests
  themselves may share the same AI-introduced blind spots as the code.
- Applying a lighter review standard to AI-generated code than to a human teammate's pull request
  covering the same kind of change.
- Skipping a security-focused read of any new AI-generated code that touches authentication,
  authorization, or raw user input.

## ➡️ Next

Continue to
[shipping-an-ai-assisted-feature-and-defending-every-line.md](shipping-an-ai-assisted-feature-and-defending-every-line.md)
to see what genuine ownership of AI-assisted code looks like once it's ready to ship.
