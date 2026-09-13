# Manipulating Elements

## Reading and Setting Text Content

```js
const heading = document.querySelector("h1");
heading.textContent;              // reads the current text
heading.textContent = "New Title"; // replaces it entirely, as plain text
```

`textContent` treats its value as **plain text** — assigning a string containing `<script>` or any
other markup renders it literally as visible text, not as parsed HTML.

## `innerHTML` — More Powerful, More Dangerous

```js
const container = document.querySelector(".card");
container.innerHTML = "<strong>Bold text</strong>"; // parsed and rendered as actual HTML
```

`innerHTML` parses its assigned string as HTML, creating real elements from it. This is genuinely
useful for inserting structured markup, but it carries a real security risk: assigning **unsanitized
user input** to `innerHTML` allows an attacker to inject arbitrary HTML and JavaScript into the
page — a classic **cross-site scripting (XSS)** vulnerability. `textContent` should always be
preferred when inserting plain text (including anything derived from user input); `innerHTML`
should be reserved for trusted, controlled markup.

## Working with Attributes

```js
const link = document.querySelector("a");
link.getAttribute("href");            // read
link.setAttribute("href", "/new-path"); // write
link.hasAttribute("target");            // check existence
link.removeAttribute("target");          // remove
```

Common attributes also have direct property access (`link.href`, `image.src`), which is often more
convenient — `getAttribute`/`setAttribute` remain necessary for custom or less common attributes
without a dedicated property shortcut.

## Working with Classes

```js
const card = document.querySelector(".card");
card.classList.add("active");
card.classList.remove("hidden");
card.classList.toggle("expanded"); // adds if absent, removes if present
card.classList.contains("active"); // boolean check
```

`classList` is the standard, preferred way to manage an element's CSS classes — far less
error-prone than manually manipulating the raw `className` string, which requires manual string
splitting to add or remove a single class without disturbing the others.

## Inline Styles

```js
card.style.backgroundColor = "blue";
card.style.display = "none";
```

Directly setting `element.style` properties applies **inline styles**, which override
stylesheet-defined rules per the specificity rules from
[specificity-and-cascade.md](../../css/css-core-fundamentals/specificity-and-cascade.md) — useful
for one-off, dynamic JavaScript-driven style changes, but toggling a CSS class (via `classList`) is
generally preferred for anything with a defined, reusable visual state, keeping styling
concerns in CSS rather than scattered through JavaScript.

## Common Mistakes

- Assigning unsanitized, user-provided content to `innerHTML`, creating a genuine XSS
  vulnerability — this is a security issue, not just a style preference.
- Manually manipulating `element.className` as a raw string instead of using `classList`, risking
  accidentally clobbering other existing classes.
- Reaching for inline `style` manipulation for states that would be more maintainably expressed as
  a toggled CSS class.

## Next

Continue to
[creating-and-removing-elements.md](creating-and-removing-elements.md) to add and remove entire
elements, not just modify existing ones.
