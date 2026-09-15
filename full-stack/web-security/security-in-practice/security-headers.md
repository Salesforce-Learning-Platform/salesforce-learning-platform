# 🛡️ Secure HTTP Headers and Environment Hygiene

## From Understanding Attacks to Practical, Everyday Defense

Every earlier module in this domain covered a specific attack in depth. This module shifts to the
practical, everyday habits that apply that knowledge across an entire real application — starting
with the fastest, most concrete win: configuring the security headers already discussed piecemeal
throughout this domain, all together in one place.

## Helmet: Setting Every Header at Once

```js
import helmet from "helmet";
const app = express();
app.use(helmet());
```

A single `app.use(helmet())` sets over a dozen security-relevant headers at once — including
`Content-Security-Policy` (per
[preventing-xss.md](../cross-site-scripting-xss/preventing-xss.md)), `X-Frame-Options` (per
[preventing-clickjacking.md](../csrf-and-clickjacking/preventing-clickjacking.md)),
`Strict-Transport-Security` (per
[https-and-tls.md](../cookies-cors-and-transport-security/https-and-tls.md)), and removes the
`X-Powered-By` header Express sets by default (which otherwise reveals the exact framework in use
to any attacker probing the application). This is genuinely the single highest-leverage, lowest-
effort step covered in this entire domain — one line, applying several of this domain's earlier
defenses simultaneously.

## Customizing Helmet's Defaults When Genuinely Needed

```js
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      scriptSrc: ["'self'", "https://trusted-cdn.example.com"],
    },
  },
}));
```

Helmet's defaults are deliberately strict — a real application occasionally needs to explicitly
allow a genuine, trusted third-party resource (an analytics script, a payment widget) that the
default policy would otherwise block. The correct approach is a narrow, deliberate exception, never
disabling the entire protection.

## Secrets Management: Never in Source Control

```bash
# .gitignore
.env
```

```js
// .env (NEVER committed)
DATABASE_URL=postgresql://...
JWT_SECRET=a-genuinely-random-32-byte-value
STRIPE_SECRET_KEY=sk_live_...
```

Every credential this domain has covered — a JWT signing secret (per
[jwt-security.md](../authentication-attacks/jwt-security.md)), a database connection string, a
payment provider's API key — needs to live in environment variables, loaded at runtime, **never**
committed directly into source code or version history.

## Environment Hygiene: Separate Secrets Per Environment

```
Development secrets  ≠  Staging secrets  ≠  Production secrets

A development database credential leaked has FAR lower stakes
than a PRODUCTION one - using genuinely SEPARATE secrets per
environment (per Environment Management, earlier in this
repository) limits the blast radius of any single leak.
```

This directly extends [environment-management.md](../../production-systems/devops-foundations/environment-management.md)'s
"configuration, not code, differs per environment" principle — applied specifically to secrets,
using a *different* actual secret value per environment, never the same one reused everywhere for
convenience.

## Common Mistakes

- Omitting `helmet()` entirely, missing a single-line, high-leverage step that applies several of
  this domain's earlier defenses at once.
- Committing a `.env` file (or any file containing real secrets) to version control, even
  temporarily, where it remains in git history indefinitely afterward.
- Reusing the exact same secret value across development, staging, and production, unnecessarily
  widening the blast radius of any single leaked credential.

## ➡️ Next

Continue to [dependency-security.md](dependency-security.md) to see how vulnerabilities in
third-party code — not code written in-house at all — are actually detected and managed.
