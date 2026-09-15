# 🔄 The Development-to-Production Lifecycle

## "It Works on My Machine" — Why That's Not Enough

Every developer has experienced this: code that runs perfectly on a local machine, then breaks —
subtly or completely — once deployed. This isn't bad luck; it's the predictable result of real,
structural gaps between a local development environment and a real production environment. The
**Twelve-Factor App** methodology, a widely-referenced set of best practices for building
deployable web applications, names this problem directly as "dev/prod parity."

## Three Named Gaps Between Dev and Prod

```
TIME GAP     → a developer might deploy code within MINUTES of
               writing it locally, or it might sit for WEEKS before
               reaching production — the longer that gap, the more
               the two environments can drift apart

PERSONNEL GAP → the person who WROTE the code isn't always the
               person who DEPLOYS or operates it (the very
               separation DevOps, per what-is-devops.md, aims to
               close)

TOOLS GAP     → local development commonly uses DIFFERENT backing
               services than production - SQLite locally, but
               PostgreSQL in production; an in-memory cache
               locally, but Redis in production
```

Of these three, the **tools gap** is the one most directly responsible for the classic "works
locally, breaks in production" bug — a subtle difference between SQLite's and PostgreSQL's SQL
dialect, or between an in-memory cache's behavior and Redis's, can pass every local test and still
fail once deployed.

## A Concrete Example of the Tools Gap

```python
# Works fine locally with SQLite - date comparisons are lenient
cursor.execute("SELECT * FROM orders WHERE created_at > '2024-01-01'")

# The SAME query can behave subtly differently against PostgreSQL,
# which enforces stricter type handling for date comparisons
```

This is exactly the kind of bug that no amount of local testing catches — the code is genuinely
correct against SQLite's behavior, and genuinely different once run against the production
database's actual behavior.

## The Recommendation: Minimize the Gaps Deliberately

```
"Keep development, staging, and production as similar as
possible" - use the SAME backing services (same database, same
cache) in every environment, not just similar or compatible ones.
```

This is the Twelve-Factor App's own direct guidance — and it's exactly the problem
[Docker and Containerization](../docker-and-containerization/), later in this domain, solves
practically: a containerized local development environment can run the *exact* same database and
cache versions used in production, closing the tools gap almost entirely rather than merely
narrowing it.

## Why This Matters More as a Team Grows

```
A SOLO developer might get away with "close enough" local tools,
since they alone understand both the local quirks and the
production behavior.

A TEAM, especially with the personnel gap in place, genuinely
NEEDS deliberate parity - otherwise, debugging a production issue
requires someone to first rule out "is this just a local-vs-prod
tools difference?" before investigating the real bug.
```

Dev/prod parity isn't just a best practice for its own sake — it removes an entire category of
wasted debugging time, letting a team trust that a bug reproduced locally is genuinely the same bug
happening in production.

## Common Mistakes

- Using a different, "close enough" database or cache locally than what actually runs in
  production, then being surprised when a bug only appears after deployment.
- Letting code sit unreleased for weeks, widening the time gap and making eventual deployment
  riskier and harder to reason about.
- Assuming automated tests alone guarantee production behavior, when the tests themselves may be
  running against the same non-production tools that caused the gap in the first place.

## ➡️ Next

Continue to [infrastructure-basics.md](infrastructure-basics.md) to see how Infrastructure as Code
makes environments like this genuinely reproducible, rather than manually and inconsistently
configured.
