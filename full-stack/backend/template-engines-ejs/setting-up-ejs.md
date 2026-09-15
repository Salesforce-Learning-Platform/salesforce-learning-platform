# ⚙️ Setting Up EJS

## Installing EJS

```bash
npm install ejs
```

EJS is a regular dependency — the running application genuinely needs it to render views, so
(unlike a build-time-only tool) it belongs in `dependencies`, per
[npm-and-package-management.md](../starting-with-nodejs/npm-and-package-management.md)'s
distinction.

## Configuring Express to Use It

```js
import express from "express";
const app = express();

app.set("views", "./views");     // where template files live
app.set("view engine", "ejs");   // which engine to use
```

`app.set("view engine", "ejs")` tells Express which template engine to use whenever `res.render()`
is called; `app.set("views", ...)` tells it where to find the actual `.ejs` files. Express expects
any compliant template engine to export a specific rendering function internally — EJS already
does this, so no further wiring is needed beyond these two `app.set()` calls.

## The `views` Folder Structure

```
views/
├── index.ejs
├── products/
│   ├── list.ejs
│   └── detail.ejs
└── partials/
    ├── header.ejs
    └── footer.ejs
```

By convention, `.ejs` files live in a `views/` folder, often organized by feature — directly
mirroring [scalable-backend-structure.md](../backend-architecture/scalable-backend-structure.md)'s
broader principle of a project's folder structure reflecting its actual architecture.

## Rendering a View

```js
app.get("/", (req, res) => {
  res.render("index", { title: "My Shop", message: "Welcome!" });
});
```

```html
<!-- views/index.ejs -->
<html>
  <head><title><%= title %></title></head>
  <body><h1><%= message %></h1></body>
</html>
```

`res.render(viewName, data)` replaces `res.json()` from every prior module — it locates
`views/index.ejs`, compiles it with the given `data` object, and sends the resulting HTML directly
as the response. This is a genuinely different response mechanism than everything covered in
[REST API Design](../rest-api-design/), which was built entirely around `res.json()`.

## Common Mistakes

- Forgetting to call both `app.set("views", ...)` and `app.set("view engine", "ejs")` — Express
  needs both to know where to look and how to render what it finds there.
- Passing a data object to `res.render()` that's missing a variable the template actually
  references — this throws a runtime error the moment that template tries to render, rather than
  failing at the route definition itself.
- Mixing `res.json()` and `res.render()` inconsistently across an application with no clear rule
  for which routes serve HTML and which serve an API — a real, common source of confusion in a
  codebase that started as one kind of app and grew the other capability later.

## ➡️ Next

Continue to [ejs-syntax.md](ejs-syntax.md) to actually write dynamic template content.
