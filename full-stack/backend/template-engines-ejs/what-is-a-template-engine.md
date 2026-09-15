# 🧩 What Is a Template Engine?

## Generating HTML on the Server, With Real Data

```html
<!-- A template with placeholders -->
<h1><%= title %></h1>
<p>Welcome back, <%= user.name %>!</p>
```

A **template engine** takes a template file — HTML with embedded placeholders — and a set of real
values, and combines them into a finished HTML page sent directly to the browser. This is a
genuinely different approach from everything else in the [Backend domain](../../backend/) so far:
instead of returning JSON for a separate frontend to render (per
[REST API Design](../rest-api-design/)), the server itself produces the final HTML.

## When This Is the Right Choice

- **A content-driven site** — a blog, a marketing site, documentation — where the content itself
  matters more than rich, interactive client-side behavior.
- **An internal admin tool** — where development speed matters more than a polished, app-like
  experience, and a full separate [React](../../frontend/react/) frontend would be unnecessary
  overhead.
- **Server-generated emails** — an order confirmation or a password-reset email, rendered as HTML
  entirely on the server before being sent.

## When a Separate Frontend (React/Next.js) Is Still the Better Choice

A rich, highly interactive application — the kind covered throughout the
[React](../../frontend/react/) and [Next.js](../../frontend/nextjs/) domains — genuinely benefits
from a dedicated frontend framework's component model, client-side state management, and
[REST API Design](../rest-api-design/)'s clean separation between frontend and backend. Template
engines and a full frontend framework aren't competing for the exact same job; each fits a
genuinely different kind of project.

## Three Common Options

| Engine | Syntax style | Notable characteristic |
|---|---|---|
| **EJS** | Plain JavaScript embedded directly in HTML | The lowest learning curve for anyone who already knows JavaScript — this module's focus |
| **Handlebars** | A stricter, logic-light templating syntax | Deliberately limits embedded logic, encouraging simpler templates |
| **Pug** | Indentation-based, no closing tags | The most compact syntax, but the biggest departure from plain HTML |

EJS's core appeal, covered throughout the rest of this module, is that it doesn't introduce a new
templating language at all — it's plain JavaScript, embedded directly inside otherwise-normal HTML.

## Common Mistakes

- Reaching for a full separate frontend framework for a simple, mostly-static, content-driven site
  where a template engine would be simpler and faster to build.
- Building a genuinely rich, highly interactive application with a template engine, fighting
  against its server-rendered nature instead of using a frontend framework actually built for that
  job.
- Assuming all template engines work identically — Handlebars' deliberately limited logic and
  Pug's indentation-based syntax are real, meaningful differences from EJS's plain-JavaScript
  approach, not just cosmetic ones.

## ➡️ Next

Continue to [setting-up-ejs.md](setting-up-ejs.md) to configure EJS in a real Express application.
