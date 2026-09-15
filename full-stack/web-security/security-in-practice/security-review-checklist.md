# ✅ A Pre-Ship Security Checklist

## Bringing the Entire Domain Together

This is the final file of the Web Security domain — a practical, consolidated checklist drawing on
every module covered, from [The Security Mindset](../the-security-mindset/) through this module's
own practical habits. Use it as a genuine, deliberate pre-ship review, not a box-checking formality.

## Input and Injection

```
☐ Every request body, query parameter, and header is validated
  against an explicit schema/allowlist (per input-validation.md)
☐ Database queries use parameterized queries / an ORM - never
  raw string concatenation (per SQL Injection)
☐ Any shell command execution uses execFile(), never exec(), with
  user-supplied input (per Command Injection)
```

## Output and Client-Side Safety

```
☐ User-generated content is escaped before rendering (or relies
  on a framework's default escaping) (per XSS)
☐ A Content Security Policy is configured as defense-in-depth
  (per Preventing XSS)
☐ textContent is used instead of innerHTML wherever real HTML
  rendering isn't genuinely needed (per DOM-Based XSS)
```

## Session, Cookies, and Cross-Origin

```
☐ Session cookies set Secure, HttpOnly, and an appropriate
  SameSite value (per Secure Cookie Attributes)
☐ State-changing requests require anti-CSRF tokens or are
  protected by SameSite=Strict (per CSRF Protection)
☐ X-Frame-Options or frame-ancestors is set for any page that
  shouldn't be embeddable (per Preventing Clickjacking)
☐ CORS uses an explicit, validated allowlist - never a wildcard
  combined with credentials, never a blind Origin reflection
  (per CORS Misconfigurations)
```

## Authentication and Server-Side

```
☐ JWT verification explicitly pins the expected algorithm (per
  JWT Security)
☐ Passwords are hashed with bcrypt/argon2, never a fast general-
  purpose hash (per Credential Security)
☐ Login endpoints are rate-limited (per Brute Force Attacks)
☐ Any server-side fetch of a user-supplied URL uses an allowlist
  (per SSRF)
☐ File-serving endpoints validate the fully resolved path (per
  Path Traversal)
☐ File uploads validate actual content (magic bytes), not just
  claimed type, and are stored outside any executable directory
  (per File Upload Security)
```

## Operational Discipline

```
☐ HTTPS is enforced everywhere, with HSTS configured (per
  HTTPS/TLS in Practice)
☐ helmet() is applied for baseline security headers (per Secure
  HTTP Headers)
☐ Secrets live in environment variables, never committed to
  source control, and differ per environment (per Environment
  Hygiene)
☐ npm audit runs as part of CI, and dependencies are added
  deliberately (per Dependency Security)
☐ The application runs as a non-root, least-privilege user in
  production (per Secure Server Configuration)
```

## Using This Checklist Effectively

```
This is a STARTING POINT, not an exhaustive guarantee - genuinely
apply it PER FEATURE as it's built (shift-left, per this domain's
own Threat Modeling coverage), not only as a single, final gate
right before shipping.
```

Directly per [threat-modeling-basics.md](../the-security-mindset/threat-modeling-basics.md)'s own
"cheaper at design time" principle from the very start of this domain — this checklist is most
valuable applied continuously, throughout development, rather than treated as a one-time hurdle
right before a release.

## Common Mistakes

- Treating this checklist as a formality to rush through right before shipping, rather than a
  genuine, deliberate review applied throughout development.
- Checking a box without actually verifying the underlying defense works — per
  [security-testing.md](security-testing.md), an automated test is a far stronger confirmation than
  a checked box alone.
- Assuming this checklist is exhaustive — it consolidates this domain's own coverage, not the
  entirety of web application security; new risks and techniques continue to emerge over time.

## Module Summary

Across this module: **secure HTTP headers and environment hygiene** — Helmet's single-line,
high-leverage header configuration, plus never committing secrets to source control — are the
fastest, most concrete wins available (see [security-headers.md](security-headers.md));
**dependency security** uses `npm audit` (verified against npm's own official documentation),
integrated into CI, to catch known vulnerabilities in third-party code before they're exploited
(see [dependency-security.md](dependency-security.md)); **input validation** names the unifying
principle behind nearly every defense in this domain — allowlist validation at every trust boundary,
not just the obvious one (see [input-validation.md](input-validation.md)); **security testing**
distinguishes SAST from DAST and treats every fix as needing its own automated verification, not
just implementation (see [security-testing.md](security-testing.md)); and this **pre-ship
checklist** consolidates the entire Web Security domain into one practical, continuously-applied
review — the mindset, principles, and specific defenses from every prior module, brought together
into a single, genuinely usable reference.
