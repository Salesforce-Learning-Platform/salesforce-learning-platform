# ARIA: When HTML Isn't Enough

## The First Rule of ARIA

Directly from the [WAI-ARIA specification's guidance](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA):
if a native HTML element already has the semantics and behavior you need, use it instead of
adding ARIA to a repurposed generic element. A native `<button>` is keyboard-operable, focusable,
and correctly announced by assistive technology automatically — recreating that with a `<div>`
plus ARIA roles requires manually reimplementing all of it, and it's easy to miss something.

**ARIA can never add missing behavior — only describe it.** Adding `role="button"` to a `<div>`
tells a screen reader to announce it as a button, but does nothing to make it respond to the
`Enter` or `Space` keys — that still has to be added manually with JavaScript. This is the single
most important thing to understand about ARIA.

## What ARIA Actually Provides

ARIA (Accessible Rich Internet Applications) is a set of HTML attributes that describe roles,
states, and properties to assistive technology, for the cases where no native element already
covers what you're building — most commonly, complex widgets HTML has no built-in equivalent for
(a tab panel, a combobox, a tree view).

| Category | Examples | Purpose |
|---|---|---|
| **Roles** | `role="tablist"`, `role="dialog"` | Declares what kind of widget this is |
| **States** | `aria-expanded`, `aria-checked`, `aria-disabled` | Describes current, changeable condition |
| **Properties** | `aria-label`, `aria-describedby`, `aria-required` | Describes relationships and additional labeling |

```html
<!-- A custom, non-native toggle button -->
<div role="button" tabindex="0" aria-pressed="false" onclick="toggle(this)">
  Mute
</div>
```

Note this example still needs `tabindex="0"` (to make it focusable at all) and JavaScript to
handle keyboard activation — none of that comes from `role="button"` alone. A native `<button>`
needs none of this extra work, which is exactly why the first rule of ARIA recommends it whenever
possible.

## Live Regions

`aria-live` announces dynamic content changes to screen readers without requiring the user to
have focus on the changed element — useful for things like a form submission result or a live
notification count:

```html
<div aria-live="polite">3 new messages</div>
```

`polite` waits for the user to pause before announcing; `assertive` interrupts immediately and
should be reserved for genuinely time-critical updates (like an error that blocks progress).

## Common Mistakes

- Adding ARIA roles to a custom element without also implementing the keyboard behavior a native
  equivalent would have provided automatically — this is worse than doing nothing, because it
  tells assistive technology the element behaves like something it doesn't.
- Overusing `aria-label` to override text that's already visible and correct, creating a mismatch
  between what's displayed and what's announced.
- Using `aria-live="assertive"` for routine, non-urgent updates, which interrupts the user
  unnecessarily.

## Next

Continue to
[keyboard-navigation-and-focus-management.md](keyboard-navigation-and-focus-management.md) for the
keyboard behavior that ARIA alone does not provide.
