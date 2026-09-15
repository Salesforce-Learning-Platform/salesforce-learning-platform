# 📄 Template Engines — EJS

## Purpose

Every backend module so far has returned **JSON** — the correct choice for an API consumed by a
separate [React](../../frontend/react/) or [Next.js](../../frontend/nextjs/) frontend. This module
covers the other real option: a **template engine**, which lets an Express server render actual
HTML pages directly, useful for server-rendered sites, admin panels, or email templates that don't
need a full separate frontend framework.

## 🎯 Learning Objectives

- Explain what a template engine is, and when rendering HTML server-side is the right choice.
- Compare EJS, Handlebars, and Pug as the three common template engine options.
- Set up EJS in an Express application.
- Use EJS's core syntax: output, unescaped output, and scriptlet tags.
- Use loops, conditionals, and locals inside a view.
- Serve static files (CSS, images) correctly alongside EJS templates.

## 📋 Prerequisites

- [Express.js Fundamentals](../expressjs-fundamentals/) — this module uses Express routing and
  `res` throughout, just replacing `res.json()` with `res.render()`.

## 📂 Files in This Module

| File | Covers |
|---|---|
| [what-is-a-template-engine.md](what-is-a-template-engine.md) | The concept, and EJS vs. Handlebars vs. Pug |
| [setting-up-ejs.md](setting-up-ejs.md) | Configuring `view engine`, the `views` directory, and `res.render()` |
| [ejs-syntax.md](ejs-syntax.md) | `<%= %>`, `<% %>`, and `<%- %>` |
| [loops-conditionals-and-locals.md](loops-conditionals-and-locals.md) | Rendering dynamic lists and conditional content in a view |
| [static-files-in-ejs.md](static-files-in-ejs.md) | Serving CSS and images correctly alongside rendered templates |

## 🔍 When to Deep-Dive vs. Skim

Deep-dive [ejs-syntax.md](ejs-syntax.md) — the distinction between `<%= %>` (escaped) and
`<%- %>` (unescaped) output is a genuine security concern, not just a syntax detail, and getting it
wrong is a real, common source of cross-site scripting vulnerabilities.

## ✅ Quick Knowledge Check

<details>
<summary>When would a project reach for EJS instead of building a separate React frontend?</summary>

When the project doesn't need a rich, interactive client-side application — a simple
content-driven site, an internal admin tool, or server-generated emails are all well served by
rendering HTML directly on the server, without the overhead of a separate frontend build and API
layer. See [what-is-a-template-engine.md](what-is-a-template-engine.md).

</details>

<details>
<summary>Should user-submitted content ever be rendered with &lt;%- %&gt;?</summary>

Only if it's already been deliberately sanitized — `<%- %>` outputs raw, unescaped HTML, so
rendering untrusted user input with it directly creates a cross-site scripting vulnerability.
`<%= %>` (escaped output) is the safe default for anything coming from user input. See
[ejs-syntax.md](ejs-syntax.md).

</details>

## 📚 References

- EJS, [Official site](https://ejs.co/)
- Express, [Using template engines with Express](https://expressjs.com/en/guide/using-template-engines.html)

## ➡️ Continue Your Learning Path

Continue to the [Handling Files with Express module](../handling-files-with-express/) to accept
file uploads from the forms this module's templates can render.
