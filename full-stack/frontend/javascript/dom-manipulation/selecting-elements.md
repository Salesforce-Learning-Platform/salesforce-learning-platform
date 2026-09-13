# Selecting Elements

## `querySelector` and `querySelectorAll` — The Modern Standard

```js
document.querySelector(".card");          // first matching element, or null
document.querySelectorAll(".card");        // ALL matching elements, as a NodeList
```

Both accept any valid CSS selector — the exact same selector syntax covered in
[css-syntax-and-selectors.md](../../css/css-core-fundamentals/css-syntax-and-selectors.md) — which
is what makes them the standard, flexible choice: anything you can select in CSS, you can select
in JavaScript with the identical syntax.

## Older, More Specific Selection Methods

```js
document.getElementById("header");         // a single element by id, no "#" prefix
document.getElementsByClassName("card");    // a live HTMLCollection by class
document.getElementsByTagName("li");         // a live HTMLCollection by tag
```

These predate `querySelector` and are more restrictive (each targets one specific attribute) but
also somewhat faster in narrow cases — `querySelector`/`querySelectorAll` are the recommended
default for readability and flexibility, and this legacy family is mainly worth recognizing when
reading older code.

## NodeList vs. HTMLCollection — Not Quite Arrays

```js
const cards = document.querySelectorAll(".card"); // NodeList
cards.forEach(card => console.log(card));            // NodeList supports forEach directly

const cards2 = document.getElementsByClassName("card"); // HTMLCollection
[...cards2].forEach(card => console.log(card));            // needs conversion first
```

`querySelectorAll` returns a **NodeList** (supports `forEach` directly, but not `map`/`filter`
without conversion via `Array.from()` or spread). `getElementsByClassName`/`getElementsByTagName`
return a **live HTMLCollection** that automatically updates if the DOM changes — a genuinely
different behavior from `querySelectorAll`'s static, point-in-time snapshot.

## Scoping a Selection to a Container

```js
const container = document.querySelector(".sidebar");
const links = container.querySelectorAll("a"); // only links INSIDE .sidebar
```

Calling `querySelector`/`querySelectorAll` on an element (not just `document`) scopes the search to
that element's descendants only — useful for avoiding accidental matches elsewhere on the page.

## Common Mistakes

- Calling array methods like `.map()` directly on a NodeList or HTMLCollection without converting
  it first (`Array.from(list)` or `[...list]`) — only `forEach` works directly on a NodeList, and
  even that doesn't work on an HTMLCollection.
- Not realizing an HTMLCollection is live — code that stores its length once and loops based on
  that stale value can behave unexpectedly if the DOM changes mid-loop.
- Reaching for the older, tag/class/id-specific methods out of habit when `querySelector`'s
  flexible CSS-selector syntax would be simpler and more consistent with CSS knowledge already
  covered elsewhere in this platform.

## Next

Continue to [manipulating-elements.md](manipulating-elements.md) to actually read and change what
you've selected.
