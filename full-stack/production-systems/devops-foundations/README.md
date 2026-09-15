# ⚙️ DevOps Foundations

## 📚 Overview

Every prior domain in this repository focused on *building* software. This module opens the
Production Systems domain by shifting to a genuinely different question: how does software actually
reach real users, stay running reliably, and keep behaving consistently across environments? DevOps
— the culture, and the concrete practices (CI/CD, Infrastructure as Code, environment management)
built around it — is the foundation the rest of this domain builds on.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain what DevOps actually means as a cultural and process shift, not just a job title or tool.
- Name the three concrete gaps (time, personnel, tools) between development and production, and
  why the tools gap is the most common source of "works on my machine" bugs.
- Explain what Infrastructure as Code is and its write/plan/apply workflow.
- Distinguish dev, staging, and production environments by purpose, configuration, and guardrails —
  never by different code.

## 📋 Prerequisites

- General familiarity with this repository's Backend domain — this module assumes you already understand how a typical web application is built, and now covers how it's actually deployed and operated.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [what-is-devops.md](what-is-devops.md) | DevOps as culture, with CI/CD and IaC as its core practical pillars |
| [development-to-production-lifecycle.md](development-to-production-lifecycle.md) | The Twelve-Factor App's time/personnel/tools gaps, and why the tools gap causes the most bugs |
| [infrastructure-basics.md](infrastructure-basics.md) | Infrastructure as Code: the write/plan/apply workflow, with a real Terraform example |
| [environment-management.md](environment-management.md) | Dev, staging, and production: distinct purposes, configuration over code, and deliberate guardrails; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you've mostly worked on application code so far and haven't yet had to reason about
how that code actually gets deployed, configured across environments, or kept running reliably.

**Skim** if you already have hands-on DevOps or infrastructure experience — this module establishes
foundational vocabulary the rest of this domain (CI/CD, Docker, cloud infrastructure) builds on.

## 🧠 Knowledge Check

<details>
<summary>Of the three dev/prod gaps (time, personnel, tools), which one is most directly responsible for the classic "works locally, breaks in production" bug, and why?</summary>

The tools gap. Using different backing services locally than in production — SQLite instead of
PostgreSQL, an in-memory cache instead of Redis — means code can be genuinely correct against the
local tool's behavior and genuinely different once run against production's actual behavior, even
though every local test passes.

</details>

<details>
<summary>Why should the same application never need different CODE to run correctly in dev, staging, and production?</summary>

What should differ across environments is configuration (database URLs, log levels, resource
sizing), not the code's own logic. An application that needs environment-specific code branches has
reintroduced the same dev/prod parity gap this module warns against — the whole point of consistent
environments is that the same code behaves the same way everywhere, with only its configuration
changing.

</details>

## 📚 References

- [The Twelve-Factor App - Dev/Prod Parity](https://12factor.net/dev-prod-parity) — the official source for this module's dev/prod gap analysis
- [HashiCorp - Introduction to Terraform](https://developer.hashicorp.com/terraform/intro) and [Terraform AWS Get Started Tutorial](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/aws-build) — official documentation and tutorial for the Infrastructure as Code example in this module

## ➡️ Continue Your Learning Path

Continue to [Docker and Containerization](../docker-and-containerization/) to see the practical
technology that makes dev/prod parity genuinely achievable, not just a best practice to aim for.
