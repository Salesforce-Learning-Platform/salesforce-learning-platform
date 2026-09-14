# Backend Architecture

## Purpose

This is the capstone module of the Backend domain. Every prior module built one piece — a server,
routing, a database, authentication. This module is about organizing all of those pieces together
into a real, scalable project structure, the way an actual production backend is organized —
directly mirroring what [Frontend Architecture](../../frontend/frontend-architecture/) did for the
frontend side of this platform.

## Learning Objectives

- Explain layered architecture, and why separating concerns into layers matters at scale.
- Apply the controller-service-repository pattern to organize a real Express codebase.
- Manage configuration correctly across development, staging, and production environments.
- Manage dependencies deliberately as a codebase and its team grow.
- Design a consistent error-handling architecture, not ad hoc per-route error handling.
- Structure a backend project's folders for genuine, long-term scalability.

## Prerequisites

- Every prior module in this domain — this module is specifically about organizing everything
  they built.

## Files in This Module

| File | Covers |
|---|---|
| [layered-architecture.md](layered-architecture.md) | Why and how to separate a backend into distinct layers |
| [controllers-services-and-repositories.md](controllers-services-and-repositories.md) | The concrete controller/service/repository pattern for Express |
| [configuration-management.md](configuration-management.md) | Environment-based configuration, and the Twelve-Factor App's Config principle |
| [dependency-management.md](dependency-management.md) | Managing a growing dependency tree deliberately |
| [error-handling-architecture.md](error-handling-architecture.md) | A consistent, centralized error-handling strategy, not ad hoc per-route handling |
| [scalable-backend-structure.md](scalable-backend-structure.md) | A real, production-shaped folder structure, and how it all fits together |

## When to Deep-Dive vs. Skim

Deep-dive [controllers-services-and-repositories.md](controllers-services-and-repositories.md) —
this pattern is the concrete, practical mechanism that makes "layered architecture" (the previous
file's abstract idea) actually real in an Express codebase, and it's the single most transferable
skill in this module to any real backend job.

## Quick Knowledge Check

<details>
<summary>Should a controller function ever contain a raw database query directly?</summary>

No — in the controller-service-repository pattern, a controller's job is to handle the HTTP
request/response cycle only (reading `req`, sending `res`); database access belongs in the
repository layer, called through the service layer. A controller with a raw query embedded
directly violates the separation the pattern exists to provide. See
[controllers-services-and-repositories.md](controllers-services-and-repositories.md).

</details>

<details>
<summary>Is it acceptable to commit different config files per environment (config.dev.json, config.prod.json) to version control?</summary>

Only if they contain no secrets — actual credentials should never be committed, per the
Twelve-Factor App's Config principle, which specifically argues for environment variables over
committed config files precisely because secrets shouldn't live in source control at all. See
[configuration-management.md](configuration-management.md).

</details>

## References

- The Twelve-Factor App, [III. Config](https://12factor.net/config)
- Martin Fowler, [Repository](https://martinfowler.com/eaaCatalog/repository.html)

## Continue Your Learning Path

This is the final module of the core Backend domain. See the platform's root
[README](../../../README.md) for the full repository structure and what comes next.
