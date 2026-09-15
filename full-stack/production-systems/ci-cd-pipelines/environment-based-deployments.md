# 🌍 Environment-Based Deployments

## Bringing Back Dev, Staging, and Production

[Environment Management](../devops-foundations/environment-management.md), earlier in this domain,
established *why* dev, staging, and production exist as distinct environments. This file covers how
a CI/CD pipeline actually targets each of them differently — automatically, based on which branch
triggered the pipeline.

## Branch-Based Environment Targeting

```yaml
jobs:
  deploy-staging:
    needs: [build, test]
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - run: ./deploy.sh staging

  deploy-production:
    needs: [build, test]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: ./deploy.sh production
```

A push to `develop` triggers `deploy-staging`; a push (or merge) to `main` triggers
`deploy-production` — the *same* build and test stages run identically for both, with only the final
deployment target actually differing. This directly implements
[environment-management.md](../devops-foundations/environment-management.md)'s core principle:
identical code, environment-specific configuration and targeting.

## GitHub Environments — Adding Deliberate Guardrails

```yaml
deploy-production:
  environment: production   # can require manual approval before
                             # this job actually runs
```

GitHub's own `environment` key can be configured with **protection rules** — for instance, requiring
a specific person to manually approve the deployment before it actually proceeds. This is the
concrete, practical mechanism behind
[environment-management.md](../devops-foundations/environment-management.md)'s "production needs
deliberate guardrails" principle — staging might deploy automatically with zero friction, while
production requires an explicit, human approval click first.

## Environment-Specific Secrets and Configuration

```yaml
steps:
  - name: Deploy
    env:
      DATABASE_URL: ${{ secrets.DATABASE_URL }}   # different value
                                                     # per environment,
                                                     # per GitHub's
                                                     # own environment-
                                                     # scoped secrets
    run: ./deploy.sh
```

GitHub Actions supports environment-scoped secrets — the *same* secret name (`DATABASE_URL`) can
hold a genuinely different value depending on which `environment` the job targets, directly
implementing the environment-variable-based configuration pattern from
[environment-management.md](../devops-foundations/environment-management.md) at the pipeline level.

## A Complete Picture: One Pipeline, Multiple Destinations

```
push to a feature branch  → build + test ONLY, no deployment
push to develop            → build + test + deploy to STAGING
merge to main               → build + test + deploy to PRODUCTION
                              (possibly gated by manual approval)
```

This is the complete, practical shape of a real CI/CD pipeline — one consistent set of build and
test stages, with deployment behavior branching based on exactly which branch triggered the run,
directly enforcing the different risk tolerances appropriate to each environment.

## Common Mistakes

- Using the identical deployment target for every branch, losing the deliberate staging checkpoint
  that exists specifically to catch problems before they reach production.
- Hardcoding environment-specific configuration values directly in the workflow file instead of
  using properly scoped secrets/environment variables per environment.
- Configuring production deployment with the same low-friction, no-approval-required settings as
  staging, removing the deliberate guardrail this stage's higher stakes call for.

## Module Summary

Across this module: **CI/CD** automates the entire build-test-deploy sequence, with Continuous
Integration catching problems early on every push and Continuous Delivery/Deployment distinguishing
a human-gated release from a fully automatic one (see
[introduction-to-ci-cd.md](introduction-to-ci-cd.md)); **build pipelines** turn source code into a
deployable, commit-SHA-tagged artifact, with dependency caching keeping builds fast (see
[build-pipelines.md](build-pipelines.md)); **automated testing** runs the full testing pyramid on
every change in a clean, isolated environment, made a genuine structural gate through required
status checks (see [automated-testing.md](automated-testing.md)); **deployment pipelines** only run
after build and test genuinely succeed, with commit-SHA tagging making rollback simply a matter of
redeploying a known-good previous image (see
[deployment-pipelines.md](deployment-pipelines.md)); and **environment-based deployments** route
different branches to different environments automatically, with GitHub's own protection rules and
scoped secrets providing the deliberate, environment-appropriate guardrails this domain's earlier
modules established the need for.
