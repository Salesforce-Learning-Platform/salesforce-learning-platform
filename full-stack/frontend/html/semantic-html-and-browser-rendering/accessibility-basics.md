# Accessibility Basics

## Scope of This File

This is a foundational introduction — the direct payoff of the semantic HTML choices covered
throughout this module. A full, dedicated treatment (ARIA, keyboard navigation patterns, focus
management, testing) is covered in the
[HTML Accessibility](../html-accessibility/) module.

## Semantic HTML Is the First Accessibility Layer

Every semantic element covered in this module already does real accessibility work before any
extra effort is added:

- `<nav>`, `<main>`, `<header>` give screen reader users **landmarks** to jump between directly.
- A correct heading hierarchy (see
  [content-structure-and-heading-hierarchy.md](content-structure-and-heading-hierarchy.md)) lets
  users navigate by heading level.
- `<button>` and `<a>` provide correct keyboard behavior and semantics for free, with no extra
  code.
- `<label>` (see [forms-introduction.md](forms-introduction.md)) makes form fields identifiable to
  assistive technology.

This is why "use semantic HTML" is consistently the first and highest-leverage accessibility
recommendation — it's foundational infrastructure, not a finishing touch.

## Alternative Text for Images

Every meaningful `<img>` needs an `alt` attribute describing its content or purpose, so a screen
reader (or a failed image load) still conveys the same information:

```html
<img src="chart.png" alt="Bar chart showing 40% revenue growth in Q3 2026">
```

A purely decorative image (contributing no information) should use `alt=""` (empty, not omitted) —
this correctly tells assistive technology to skip it entirely, rather than announcing the filename
as a fallback.

## Keyboard Accessibility

A page should be fully usable without a mouse. Semantic interactive elements (`<a>`, `<button>`,
form controls) are keyboard-accessible by default; recreating their behavior with a styled `<div>`
and a click handler requires manually reimplementing focus, keyboard activation, and correct
announced role — easy to get subtly wrong, and unnecessary when the native element already does it
correctly.

## Common Mistakes

- Adding `alt` text that just repeats the filename or says "image" — describe what the image
  communicates, or mark it `alt=""` if purely decorative.
- Building custom interactive controls from non-interactive elements (`<div onclick="...">`)
  instead of native `<button>`/`<a>`, losing keyboard support in the process.
- Treating accessibility as a final pass applied after the page is built, rather than a consequence
  of the semantic choices made throughout — most of it is free if handled from the start.

## Next

Continue to [how-browsers-render-pages.md](how-browsers-render-pages.md) to shift from markup
semantics to what the browser actually does with the HTML you write.
