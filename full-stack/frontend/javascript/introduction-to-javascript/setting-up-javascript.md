# Setting Up JavaScript

## Three Ways to Run JavaScript

**1. The browser console** — open DevTools (see
[browser-devtools-essentials.md](../../foundations/preparing-your-machine/browser-devtools-essentials.md))
and type directly into the Console panel. Fastest way to experiment with a single expression, with
no file needed at all.

**2. A `<script>` tag in an HTML file:**

```html
<!doctype html>
<html>
  <body>
    <script src="app.js"></script>
  </body>
</html>
```

Placing `<script>` just before the closing `</body>` tag (or using the `defer` attribute) ensures
the HTML has been parsed before the script runs and tries to interact with it — a script that runs
before the page's elements exist can't find them yet.

**3. Node.js, from the terminal:**

```bash
node app.js
```

This runs the same JavaScript language outside a browser entirely, with no HTML involved — the
correct choice for scripts, tooling, and anything covered later in the backend or CLI tooling
context.

## `console.log` — Your Primary Feedback Tool

```js
console.log("Hello, JavaScript");
console.log(2 + 2); // 4
```

`console.log()` prints a value to the console (visible in DevTools for browser code, or directly
in the terminal for Node) — the most immediate way to check what a piece of code is actually doing
while learning or debugging.

## Comments

```js
// A single-line comment

/* A
   multi-line
   comment */
```

Comments are ignored by the JavaScript engine entirely — they exist purely for human readers of the
code.

## Common Mistakes

- Placing a `<script>` tag in `<head>` without `defer`, causing it to run before the page's HTML
  elements exist, and failing to find them.
- Forgetting that browser-only APIs (like anything DOM-related) don't exist in Node, and
  vice versa (Node's filesystem APIs don't exist in a browser) — the language is shared, the
  surrounding APIs are not.
- Debugging exclusively by reading code rather than running it and checking actual `console.log`
  output — for a beginner, actually running code is almost always faster than reasoning about it
  purely on paper.

## Next

Continue to [variables.md](variables.md) to start writing actual JavaScript.
