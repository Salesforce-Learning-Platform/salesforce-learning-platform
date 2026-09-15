# 🔁 Loops, Conditionals, and Locals

## Looping Over a List

```html
<ul>
  <% products.forEach(function(product) { %>
    <li><%= product.name %> — $<%= product.price %></li>
  <% }); %>
</ul>
```

Because EJS scriptlets are plain JavaScript, rendering a list means using a completely ordinary
`forEach` (or a `for` loop) — a scriptlet tag (`<% %>`) opens the loop, an escaped-output tag
(`<%= %>`, per [ejs-syntax.md](ejs-syntax.md)) renders each item's data, and the scriptlet closes
the loop. This is directly comparable to
[React's list rendering with `.map()`](../../frontend/react/components-jsx-and-props/jsx.md), just
executed once, server-side, rather than reactively in the browser.

## Conditional Rendering

```html
<% if (user.isLoggedIn) { %>
  <p>Welcome back, <%= user.name %>!</p>
<% } else { %>
  <p><a href="/login">Log in</a></p>
<% } %>
```

```html
<% if (products.length === 0) { %>
  <p>No products found.</p>
<% } else { %>
  <ul>
    <% products.forEach(function(product) { %>
      <li><%= product.name %></li>
    <% }); %>
  </ul>
<% } %>
```

An `if`/`else` inside scriptlet tags controls which section of the template actually renders —
directly comparable to the ternary/`&&`-based conditional rendering already covered in
[jsx.md](../../frontend/react/components-jsx-and-props/jsx.md), again executed once on the server
rather than reactively.

## "Locals" — the Data Object Passed to `res.render()`

```js
res.render("products/list", {
  products: allProducts,
  user: req.user, // per authentication-and-authorization/protecting-routes.md
});
```

```html
<!-- Every key in the object passed to res.render() becomes directly
     available inside the template as a variable — a "local" -->
<h1>Hello, <%= user.name %></h1>
```

Every property of the object passed as `res.render()`'s second argument becomes directly available
inside the template by that same name — these are called **locals**. If a template references a
local that wasn't actually passed in, EJS throws a runtime error the moment that line renders,
exactly the failure mode already noted in
[setting-up-ejs.md](setting-up-ejs.md).

## Partials — Reusing a Template Fragment

```html
<%- include('partials/header') %>
<h1>Product List</h1>
<%- include('partials/footer') %>
```

`include()` inserts another `.ejs` file's rendered output directly into the current template — the
EJS equivalent of a
[reusable component](../../frontend/react/component-architecture-and-composition/reusable-component-design.md),
letting a header or footer be written once and reused across every page, rather than duplicated in
every template file.

## Common Mistakes

- Referencing a local variable that wasn't actually passed to `res.render()`, causing a runtime
  error at the exact moment that template line executes.
- Writing deeply nested loops and conditionals directly inline in a large template, making it hard
  to read — extracting a repeated section into a partial (via `include()`) is usually the better
  fix, the same reasoning behind extracting a reusable component in React.
- Forgetting that `include()` itself needs `<%- %>` (unescaped), since it's inserting real,
  already-rendered HTML, not a plain text value.

## ➡️ Next

Continue to [static-files-in-ejs.md](static-files-in-ejs.md) to serve the CSS and images a
rendered page actually needs.
