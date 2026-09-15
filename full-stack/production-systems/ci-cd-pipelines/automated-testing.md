# ✅ Automated Testing in a Pipeline

## Running the Testing Pyramid, Automatically

[The Testing Pyramid](../../frontend/testing/frontend-testing-fundamentals/the-testing-pyramid.md),
covered earlier in this repository's Frontend domain, established the shape of a well-balanced test
suite — many unit tests, fewer integration tests, fewer still end-to-end tests. A CI pipeline is
what actually *runs* that entire suite automatically, on every single change, rather than relying on
a developer remembering to run it manually before pushing.

## A Complete Test Stage

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - run: npm install
      - name: Run unit tests
        run: npm run test:unit
      - name: Run integration tests
        run: npm run test:integration
      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage/
```

Separating unit and integration test commands into distinct steps means a pipeline failure clearly
indicates *which* category of test actually failed — directly the same per-stage attribution
principle already established in
[debugging-difficulty-across-agents.md](../../artificial-intelligence/multi-agent-architecture-concerns/debugging-difficulty-across-agents.md),
now applied to a testing pipeline instead of a multi-agent one.

## Failing the Pipeline on a Failed Test

```
A test command that returns a NON-ZERO exit code automatically
FAILS the entire pipeline step - this is why `npm test` (or
equivalent) exits non-zero on any failing test, without any
special CI-specific configuration needed.
```

This is a genuinely important, easy-to-overlook mechanism: CI/CD platforms don't have any special
knowledge of "tests" specifically — they simply treat a non-zero exit code from any command as a
failure, which is exactly why a test runner's own standard exit-code behavior is sufficient to
correctly fail a pipeline.

## Testing in a Genuinely Isolated Environment

```
CI runs in a FRESH, isolated environment on EVERY run - no
leftover state from a previous test run, no developer-specific
local configuration quietly making a test pass that would
actually fail elsewhere.
```

This directly reinforces the dev/prod parity principle from
[development-to-production-lifecycle.md](../devops-foundations/development-to-production-lifecycle.md),
earlier in this domain — a CI pipeline's genuinely clean, consistent environment is exactly what
catches a test that only "worked" because of some unintentional, undocumented local state on one
particular developer's machine.

## Required Status Checks — Making Tests Actually Block Merging

```
A repository can be configured so a pull request CANNOT be merged
until its CI checks pass - turning "tests should pass before
merging" from a SUGGESTION into an ENFORCED rule.
```

This is the practical mechanism that gives automated testing real teeth: without this
configuration, a failing CI check is merely informational — a team can still merge a pull request
with a broken pipeline. Requiring the check to pass makes automated testing a genuine, structural
gate rather than an optional signal.

## Common Mistakes

- Running only unit tests in CI while skipping integration or end-to-end tests entirely, missing
  exactly the class of bugs those higher-pyramid-level tests exist to catch.
- Never configuring required status checks, leaving CI failures as purely informational rather than
  an actual, enforced barrier to merging broken code.
- Writing tests that pass locally but fail in CI (or vice versa) due to undocumented local state —
  exactly the dev/prod parity problem this module's earlier files already warned against.

## ➡️ Next

Continue to [deployment-pipelines.md](deployment-pipelines.md) to see what happens after code has
successfully built and passed every test.
