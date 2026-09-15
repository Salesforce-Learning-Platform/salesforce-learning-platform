# 🔄 CI/CD Pipelines

## 📚 Overview

Every prior module in this domain covered a piece of deployment manually — building an image,
configuring HTTPS, provisioning infrastructure. This module automates the entire sequence: CI/CD
pipelines that build, test, and deploy code automatically on every change, using GitHub Actions as
the concrete, hands-on tool throughout.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain Continuous Integration and the distinction between Continuous Delivery and Continuous
  Deployment.
- Write a build pipeline that produces a commit-SHA-tagged, cacheable, deployable artifact.
- Configure automated testing as a genuine, enforced gate using required status checks.
- Build a deployment pipeline that only runs after build and test succeed, with a clear rollback
  path.
- Route different branches to different environments with appropriate, environment-specific
  guardrails.

## 📋 Prerequisites

- [DevOps Foundations](../devops-foundations/) — this module directly implements its environment-management principles.
- [Docker and Containerization](../docker-and-containerization/) — the build stage produces exactly the kind of image covered there.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [introduction-to-ci-cd.md](introduction-to-ci-cd.md) | CI vs. CD, and a real, minimal GitHub Actions workflow |
| [build-pipelines.md](build-pipelines.md) | Commit-SHA image tagging, dependency caching, and failing fast |
| [automated-testing.md](automated-testing.md) | Running the testing pyramid in CI, and required status checks |
| [deployment-pipelines.md](deployment-pipelines.md) | Deploying only after build/test succeed, zero-downtime deploys, and rollback |
| [environment-based-deployments.md](environment-based-deployments.md) | Branch-based targeting, GitHub environments, and scoped secrets; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you'll be setting up or maintaining CI/CD for a real project — every file here is
directly, immediately applicable.

**Skim** if you're joining a team with an already-established pipeline — the underlying concepts
still help you understand and reason about that existing pipeline's design.

## 🧠 Knowledge Check

<details>
<summary>Why is a deployment job configured with <code>needs: [build, test]</code> rather than being its own independent job?</summary>

`needs` structurally guarantees the deployment job only runs after both the build and test jobs have
genuinely succeeded — this is what turns "never deploy broken code" from a hoped-for convention into
an enforced, automated rule that can't be accidentally bypassed.

</details>

<details>
<summary>Why does tagging every build with its exact commit SHA make rolling back a bad deployment simple?</summary>

Because every previously deployed version is already built, tested, and stored under its own exact,
traceable tag, a rollback is simply redeploying a known-good previous image — not a separate,
special process requiring new work, just the same ordinary deployment mechanism pointed at an
older tag.

</details>

## 📚 References

- [GitHub Actions - Quickstart](https://docs.github.com/en/actions/writing-workflows/quickstart) — official documentation for GitHub Actions workflow syntax
- [GitHub Changelog - Artifacts v4](https://github.blog/changelog/2023-12-14-github-actions-artifacts-v4-is-now-generally-available/) — official documentation confirming current action versions used in this module's examples

## ➡️ Continue Your Learning Path

Continue to [Monitoring and Observability](../monitoring-and-observability/) to see how a
successfully deployed application's actual runtime health is tracked afterward.
