# 🔄 Introduction to CI/CD

## From Manual Deployment to Automation

Every module in this domain so far has covered pieces of a deployment — containers, HTTPS, a
reverse proxy, cloud infrastructure — but assembling them has been implicitly manual: build an
image, push it, run it. **CI/CD** automates this entire sequence, running it consistently, every
time, without a human manually executing each step.

## CI: Continuous Integration

```
Every time code is PUSHED (or a pull request opened):
  1. The code is automatically BUILT
  2. Automated TESTS run against it
  3. The result (pass/fail) is reported back, visibly, on the
     pull request itself
```

Continuous Integration is about catching problems **early** — the moment a change is pushed, not
days later when it's already merged and other developers have built on top of it. This is a direct,
automated extension of the code-review discipline already covered in
[Engineering WITH AI](../../artificial-intelligence/engineering-with-ai/), earlier in this
repository — CI provides an objective, automated first check before any human review even begins.

## CD: Continuous Delivery / Deployment

```
CONTINUOUS DELIVERY  → code that passes CI is automatically
                        PREPARED for deployment (built into a
                        deployable artifact), but a human still
                        triggers the actual release

CONTINUOUS DEPLOYMENT → code that passes CI is automatically
                        DEPLOYED, with no manual trigger at all
```

This distinction matters: "delivery" keeps a human decision point before something actually reaches
users; "deployment" removes it entirely, trusting the automated pipeline's checks completely. Which
one a team chooses is a deliberate risk-tolerance decision, not simply a technical default.

## A Minimal GitHub Actions Workflow

```yaml
name: CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository code
        uses: actions/checkout@v6
      - name: Run tests
        run: npm test
```

This is a real, working GitHub Actions workflow — `on: [push]` triggers it on every push,
`runs-on: ubuntu-latest` specifies the environment, and `steps` lists exactly what runs, in order.
GitHub Actions is one of the most widely-used CI/CD platforms, directly integrated with GitHub
itself — the same platform hosting the pull requests and issues already central to this
repository's own development workflow.

## Why Automate What a Developer Could Do Manually?

```
MANUAL: "did I remember to run the tests before pushing?" -
  depends entirely on individual discipline, every single time

AUTOMATED: tests run on EVERY push, for EVERY developer,
  UNCONDITIONALLY - no discipline required, no exceptions
```

This is the real, practical value of CI/CD: it removes reliance on individual memory and discipline
for a critical, repeatable process — exactly the same reasoning
[implementing-retry-mechanisms.md](../../artificial-intelligence/error-handling-in-ai-applications/implementing-retry-mechanisms.md)
applied to letting a system's own SDK handle a repeatable concern automatically, rather than relying
on a human to remember it every time.

## Common Mistakes

- Treating CI as optional or "something to add later," when the value of catching problems early is
  highest at the very start of a project, before bad patterns have a chance to compound.
- Choosing continuous deployment before a team's automated test coverage and pipeline reliability
  genuinely justify removing the human review checkpoint.
- Writing a workflow file with no actual verification steps (tests, linting) — a pipeline that only
  builds code without checking it provides much less real value.

## ➡️ Next

Continue to [build-pipelines.md](build-pipelines.md) to see what actually happens in the "build"
stage of a CI/CD pipeline, beyond just running tests.
