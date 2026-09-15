# ⚙️ Secure Server Configuration

## The Configuration Layer Beneath Every Attack in This Module

[SSRF](server-side-request-forgery-ssrf.md), [path traversal](path-traversal.md), and
[file upload risks](file-upload-security.md) each have their own specific, application-level fixes.
This file covers the broader *server configuration* discipline that limits real damage even when a
specific application-level defense somehow fails — directly extending
[Infrastructure Basics](../../production-systems/devops-foundations/infrastructure-basics.md) and
[Least Privilege](../the-security-mindset/security-principles.md), both covered earlier in this
repository.

## Running as a Non-Root, Least-Privilege User

```dockerfile
# In a Dockerfile, per Writing Dockerfiles, earlier in this domain
FROM node:20-slim
RUN addgroup --system app && adduser --system --ingroup app app
USER app   # NEVER run the application process as root
```

If an application process somehow gets compromised — via any of this module's attacks succeeding
despite the specific defenses — running as a genuinely restricted, non-root user directly limits
what that compromised process can actually do: it can't read arbitrary system files, modify other
users' data, or take actions requiring elevated privileges, regardless of what the compromised
application code itself attempts.

## Disabling Unnecessary Services and Features

```
Every RUNNING service, every ENABLED feature, that isn't
genuinely needed is pure, unnecessary attack surface (per
attack-surface.md, earlier in this domain) - a debug endpoint left
enabled in production, an admin panel with NO additional access
control, a development-only feature flag left on.
```

This is a direct, concrete application of
[attack-surface.md](../the-security-mindset/attack-surface.md)'s minimization principle, specifically
at the server-configuration level — every unnecessary running service or enabled feature is real,
avoidable risk with zero corresponding benefit.

## Keeping Software Genuinely Up to Date

```
The TalkTalk breach (per SQL Injection, earlier in this domain)
was caused by a vulnerability with a PUBLICLY AVAILABLE PATCH for
OVER THREE YEARS before the actual attack.
```

This is worth restating explicitly at the infrastructure level: a genuinely disciplined patching and
update process — for the OS, the runtime, every dependency — closes off entire categories of
already-known, already-patched vulnerabilities before they can ever be exploited, exactly the kind
of well-understood risk that caused one of this domain's own cited real breaches.

## Environment-Appropriate Error Handling

```js
// PRODUCTION - never leak internal details
app.use((err, req, res, next) => {
  console.error(err);   // log the FULL detail internally
  res.status(500).json({ error: "An unexpected error occurred." });   // reveal NOTHING externally
});
```

A production server should never expose a full stack trace, an internal file path, or a database
error message directly to an external client — each one hands an attacker genuinely useful
reconnaissance information (directory structure, technology stack, query patterns) that
meaningfully aids further, more targeted attacks.

## A Server-Hardening Checklist

```
☐ The application process runs as a non-root, least-privilege user
☐ No unnecessary services, ports, or debug/admin endpoints exposed
  in production
☐ Software (OS, runtime, dependencies) is kept genuinely current
☐ Error responses never leak internal implementation details
  externally
☐ Every specific defense from this module's earlier files (SSRF
  allowlisting, path validation, upload restrictions) is actually
  in place
```

## Common Mistakes

- Running an application process as root "for convenience," removing a genuinely significant
  containment layer if the application is ever compromised through any other means.
- Leaving debug or admin endpoints reachable in production because "no one would guess the URL,"
  relying on obscurity rather than genuine access control.
- Returning detailed internal error messages to external clients, handing an attacker free
  reconnaissance information about the system's internals.

## Module Summary

Across this module: **SSRF** tricks a server into making an unintended request, carrying the
server's own network-level trust — grounded in the real, documented 2019 Capital One breach ($80M
penalty, $190M settlement, 106 million records) — prevented with allowlisting rather than
blocklisting (see [server-side-request-forgery-ssrf.md](server-side-request-forgery-ssrf.md));
**path traversal** escapes an intended directory via `../` sequences, prevented by validating the
fully resolved path rather than the raw input string, verified against OWASP's own guidance (see
[path-traversal.md](path-traversal.md)); **file upload security** means never trusting a
client-supplied `Content-Type`, validating actual file content via magic bytes, and storing renamed
uploads outside any directly-executable directory (see
[file-upload-security.md](file-upload-security.md)); and **secure server configuration** — least-
privilege process users, minimized services, current software, and careful error handling — provides
the broader, defense-in-depth foundation that limits real damage even if a specific,
application-level defense somehow fails.
