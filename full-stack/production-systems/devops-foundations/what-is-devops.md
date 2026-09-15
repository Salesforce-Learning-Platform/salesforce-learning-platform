# ⚙️ What Is DevOps?

## A New Phase, a New Kind of Problem

Every module in this repository up to this point has focused on *building* software — frontend
interfaces, backend APIs, databases, and, most recently, AI-powered features. **Production
Systems** is where the focus shifts to a genuinely different, equally essential question: how does
that software actually get onto a server, stay running reliably, and keep working as real users
depend on it? **DevOps** is the practice — and the mindset — built around answering that question.

## The Historical Gap: Development vs. Operations

```
DEVELOPMENT team's job: write code that implements features

OPERATIONS team's job: keep servers running, deploy code safely,
  respond when something breaks

Historically, these were SEPARATE teams with DIFFERENT incentives:
  Dev wants to SHIP CHANGES fast
  Ops wants STABILITY and few changes
```

This structural separation created a real, recurring conflict: a developer's finished feature would
get "thrown over the wall" to an operations team that had no part in building it, often resulting in
slow, error-prone, poorly-understood deployments — neither side had full visibility into the other's
half of the problem.

## DevOps: Breaking Down That Wall

```
DevOps = a set of practices and a CULTURE that combines software
  development (Dev) and IT operations (Ops) — the same people (or
  tightly collaborating teams) are responsible for BOTH building
  AND running the software
```

Rather than a specific tool or job title, DevOps is fundamentally a **cultural and process shift**:
developers take ownership of how their code actually runs in production, and operations concerns
(deployment, monitoring, reliability) become part of the development process itself, not an
afterthought handled by a separate team.

## CI/CD, Briefly — the Practical Backbone of DevOps

```
CI (Continuous Integration) → every code change is automatically
  built and tested as soon as it's pushed, catching problems early

CD (Continuous Delivery/Deployment) → code that passes those
  automated checks is automatically prepared for (or directly
  pushed to) production, rather than deployed manually
```

CI/CD is the concrete, automated mechanism that makes the DevOps philosophy practical at real
scale — without it, "developers own deployment" would mean manually, repeatedly running the same
error-prone steps by hand. [CI/CD Pipelines](../ci-cd-pipelines/), later in this domain, covers this
in full depth; this module only needs the concept as context for what follows.

## Infrastructure as Code, Briefly

```
Instead of manually clicking through a cloud provider's dashboard
to set up a server, DevOps treats infrastructure itself as CODE -
version-controlled, reviewable, and repeatable, exactly like
application code.
```

This is the other core practical pillar of DevOps — covered in depth in
[infrastructure-basics.md](infrastructure-basics.md), later in this module — extending the same
version-control and review discipline already used for application code to the infrastructure that
code runs on.

## Why This Matters for Every Developer, Not Just "DevOps Engineers"

```
A developer who understands DevOps concepts can:
  - reason about WHY a feature that works locally might fail in
    production
  - write code that's genuinely easier to deploy and monitor
  - debug a production incident far more effectively
```

This is why this module exists at the start of a domain aimed at every developer, not a specialized
subset — understanding how software actually reaches and survives in production is a foundational
skill, not an optional specialty.

## Common Mistakes

- Treating DevOps as simply "a job title" or "a specific tool" rather than the underlying
  collaborative practice and shared ownership it actually describes.
- Assuming DevOps concerns are someone else's responsibility, rather than an integrated part of the
  development process itself.
- Confusing DevOps (the practice/culture) with CI/CD or Infrastructure as Code (specific practical
  mechanisms *within* DevOps) as though they were interchangeable terms.

## ➡️ Next

Continue to
[development-to-production-lifecycle.md](development-to-production-lifecycle.md) to see exactly
why an application that works perfectly on a developer's own machine can still behave differently
once deployed.
