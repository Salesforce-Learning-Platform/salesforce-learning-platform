# 🎨 Static Files in EJS

## Serving CSS, Images, and Client-Side JS

```js
app.use(express.static("public"));
```

```
public/
├── css/
│   └── styles.css
├── images/
│   └── logo.png
└── js/
    └── main.js
```

A rendered EJS page still needs real static assets — a stylesheet, an image, maybe a small piece
of client-side JavaScript. `express.static()`, already introduced in
[Express's middleware.md](../expressjs-fundamentals/middleware.md), serves files from a folder
directly, with no route needed per file — exactly what a template's `<link>` and `<img>` tags need
to actually resolve.

## Referencing Static Files From a Template

```html
<html>
  <head>
    <link rel="stylesheet" href="/css/styles.css">
  </head>
  <body>
    <img src="/images/logo.png" alt="Company logo">
    <script src="/js/main.js"></script>
  </body>
</html>
```

The path used in `href`/`src` is relative to the static folder's **root**, not to the folder on
disk — `public/css/styles.css` is referenced as `/css/styles.css`, since `express.static("public")`
already serves everything inside `public/` as if it were the site's root.

## A Realistic, Complete Setup

```js
import express from "express";
const app = express();

app.set("views", "./views");
app.set("view engine", "ejs");
app.use(express.static("public"));

app.get("/products", (req, res) => {
  res.render("products/list", { products: allProducts });
});
```

```html
<!-- views/products/list.ejs -->
<html>
  <head>
    <link rel="stylesheet" href="/css/styles.css">
  </head>
  <body>
    <ul>
      <% products.forEach(function(product) { %>
        <li><%= product.name %></li>
      <% }); %>
    </ul>
  </body>
</html>
```

This combines every piece from this module: view engine configuration
([setting-up-ejs.md](setting-up-ejs.md)), a loop rendering real data
([loops-conditionals-and-locals.md](loops-conditionals-and-locals.md)), and a static stylesheet
served correctly alongside the rendered HTML.

## Common Mistakes

- Referencing a static asset's path as if it included the `public/` folder name (`/public/css/
  styles.css`) — `express.static("public")` already strips that prefix; the correct reference is
  `/css/styles.css`.
- Forgetting `express.static()` entirely and wondering why a rendered page's CSS never actually
  loads, even though the template's `<link>` tag looks correct.
- Placing sensitive files (like a `.env` file, per
  [environment-variables.md](../nodejs-core-concepts/environment-variables.md)) inside the static
  folder — anything in it is served publicly, with no access control at all.

## Module Summary

Across this module: a **template engine** renders HTML directly on the server, a genuinely
different response mechanism than the JSON APIs covered throughout the rest of this domain, and a
better fit for content-driven sites and internal tools than a full separate frontend framework (see
[what-is-a-template-engine.md](what-is-a-template-engine.md)); **EJS** is configured in Express
with `app.set("view engine", "ejs")` and rendered with `res.render()` (see
[setting-up-ejs.md](setting-up-ejs.md)); its three tags — `<%= %>` (escaped, the safe default),
`<% %>` (logic, no output), and `<%- %>` (raw, genuinely risky on untrusted input) — carry real
security implications, not just stylistic ones (see [ejs-syntax.md](ejs-syntax.md)); **loops,
conditionals, and locals** render dynamic data using plain JavaScript directly inside a template,
with `include()` enabling reusable partials (see
[loops-conditionals-and-locals.md](loops-conditionals-and-locals.md)); and **static files**, served
via `express.static()`, provide the CSS, images, and client-side JS a rendered page still needs.
