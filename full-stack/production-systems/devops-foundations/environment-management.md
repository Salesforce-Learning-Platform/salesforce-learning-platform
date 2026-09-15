# 🌍 Dev, Staging, and Production Environments

## Three Environments, Three Distinct Purposes

```
DEVELOPMENT (dev)   → a developer's own local machine, or a
                       personal cloud sandbox - fast iteration,
                       frequent breakage is expected and fine

STAGING              → a environment that mirrors production as
                       closely as possible - the LAST place to
                       catch problems before real users are affected

PRODUCTION (prod)    → the real, live environment real users
                       actually depend on - stability is the
                       overriding priority
```

These aren't just three copies of the same thing — each environment serves a genuinely distinct
purpose in the deployment lifecycle, with a deliberately different tolerance for risk and
instability at each stage.

## Why Staging Exists at All

```
Without staging: code goes STRAIGHT from a developer's local
  machine to production - any gap between "works for me" and
  "works for real users" is discovered AFTER real users are
  already affected

With staging: that same code runs in an environment that mirrors
  production's actual infrastructure and data shape FIRST -
  catching dev/prod parity gaps (per
  development-to-production-lifecycle.md) before they reach users
```

Staging is the practical, concrete answer to the dev/prod parity problem this module already
covered: rather than *hoping* local testing caught every discrepancy, staging is a real, dedicated
checkpoint specifically designed to surface exactly this class of problem before it becomes a
genuine incident.

## Environment-Specific Configuration, Not Environment-Specific Code

```bash
# .env.development
DATABASE_URL=postgresql://localhost:5432/myapp_dev
LOG_LEVEL=debug

# .env.production
DATABASE_URL=postgresql://prod-db.internal:5432/myapp
LOG_LEVEL=warn
```

The *code* itself should be identical across every environment — what changes is **configuration**,
typically via environment variables, exactly the pattern this repository's own backend modules
already establish for handling secrets and per-environment settings. An application that needs
different *code* (not just different configuration) to run in different environments has already
reintroduced the tools/parity gap this module warned against.

## Using Infrastructure as Code Across Environments

```hcl
resource "aws_instance" "app_server" {
  ami           = var.ami_id
  instance_type = var.instance_type  # "t2.micro" for staging, larger for prod

  tags = {
    Name        = "app-server-${var.environment}"
    Environment = var.environment
  }
}
```

Directly building on [infrastructure-basics.md](infrastructure-basics.md), the *same* IaC
configuration, parameterized by environment (staging vs. production), is what makes real dev/prod
parity practically achievable — staging genuinely mirrors production's infrastructure shape because
it's provisioned from the same underlying definition, with only a few deliberate values (instance
size, resource count) differing.

## Guarding Production Deliberately

```
A staging environment can tolerate frequent, casual changes and
occasional breakage.

Production needs DELIBERATE guardrails: who can deploy, what
approval is required, what automated checks must pass first -
often enforced directly by the CI/CD pipeline (per CI/CD Pipelines,
later in this domain).
```

This asymmetric treatment is intentional and important — the same speed and casualness that makes
staging (and especially dev) productive would be genuinely dangerous applied directly to production,
which is exactly why real teams enforce stricter process specifically at that final boundary.

## Common Mistakes

- Skipping staging entirely for a "quick fix," removing the one checkpoint specifically designed to
  catch dev/prod parity gaps before they reach real users.
- Writing environment-specific *code* (an `if (environment === "production")` branch containing
  genuinely different logic) instead of environment-specific *configuration* — reintroducing the
  exact parity gap this module has covered throughout.
- Applying the same casual, low-friction deployment process to production as to staging, without
  deliberate additional guardrails appropriate to production's actual stakes.

## Module Summary

Across this module: **DevOps** is fundamentally a culture and set of practices that breaks down the
historical separation between development and operations, with CI/CD and Infrastructure as Code as
its two core practical pillars (see [what-is-devops.md](what-is-devops.md)); **the dev/prod gap** —
named directly by the Twelve-Factor App methodology as time, personnel, and tools gaps — is the root
cause of "works on my machine" bugs, with the tools gap (different backing services locally vs. in
production) being the most common, concrete culprit (see
[development-to-production-lifecycle.md](development-to-production-lifecycle.md)); **Infrastructure
as Code** replaces manual, one-off infrastructure setup with version-controlled, reviewable,
repeatable configuration files, following a write/plan/apply workflow (see
[infrastructure-basics.md](infrastructure-basics.md)); and **dev, staging, and production
environments** each serve a distinct purpose in the deployment lifecycle, differing in
*configuration* (never code) and in the deliberate guardrails applied as risk tolerance decreases
from dev toward production.
