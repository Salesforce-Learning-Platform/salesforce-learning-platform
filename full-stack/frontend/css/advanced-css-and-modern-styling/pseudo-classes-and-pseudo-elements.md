# Pseudo-Classes and Pseudo-Elements

## The Distinction

Both start with colons, but target fundamentally different things:

- A **pseudo-class** (one colon: `:hover`) selects an element that's in a particular *state* or
  *structural position* — it's still a real element, just matched conditionally.
- A **pseudo-element** (two colons: `::before`) selects a specific, *generated* part of an element
  that has no corresponding node in the actual DOM.

## Common Pseudo-Classes

| Pseudo-class | Matches |
|---|---|
| `:hover` | While the pointer is over the element |
| `:focus` | While the element has keyboard focus (see [keyboard-navigation-and-focus-management.md](../../html/html-accessibility/keyboard-navigation-and-focus-management.md)) |
| `:focus-visible` | Focus specifically from keyboard/non-pointer interaction |
| `:active` | While being clicked/pressed |
| `:disabled` / `:checked` | Form control states |
| `:first-child` / `:last-child` | Structural position among siblings |
| `:nth-child(n)` | The nth element among siblings, supporting formulas like `2n` (even) or `3n+1` |
| `:not(selector)` | Excludes elements matching the given selector |

```css
tr:nth-child(even) {
  background-color: #f5f5f5; /* zebra-striping a table with no extra classes needed */
}

button:focus-visible {
  outline: 2px solid #1a73e8; /* visible only for keyboard focus, not mouse clicks */
}
```

`:nth-child()` zebra-striping is a good example of what pseudo-classes are for: expressing a
structural pattern in CSS alone, without adding a class to every other row in the markup.

## Common Pseudo-Elements

| Pseudo-element | Targets |
|---|---|
| `::before` / `::after` | Generated content inserted before/after an element's actual content |
| `::first-line` / `::first-letter` | The first line or letter of a text block |
| `::placeholder` | The placeholder text of a form input |
| `::selection` | Text currently selected/highlighted by the user |

```css
.required::after {
  content: " *";
  color: red;
}
```

`::before`/`::after` require a `content` property (even if empty: `content: "";`) to render at
all — without it, the pseudo-element generates no box. This pattern is common for adding purely
decorative content (an icon, an asterisk) without cluttering the HTML with elements that carry no
semantic meaning.

## An Important Accessibility Caveat

Content inserted via `::before`/`::after`'s `content` property is inconsistently exposed to
assistive technology (support varies, and it's often not announced at all) — meaningful content
should never be delivered *only* through generated pseudo-element content. It's appropriate for
purely decorative additions, not for anything a user genuinely needs to perceive.

## Common Mistakes

- Confusing single-colon and double-colon syntax — modern CSS distinguishes them (`:hover` vs.
  `::before`), though browsers still accept the old single-colon form for pseudo-elements for
  backward compatibility, which can obscure the distinction.
- Relying on `::before`/`::after` generated content to convey information a user actually needs,
  when it may not be reliably announced by assistive technology.
- Using `:hover` alone for an interactive affordance with no `:focus` equivalent, leaving keyboard
  users without the same visual feedback mouse users get.

## Next

Continue to [transitions-and-animations.md](transitions-and-animations.md) for animating changes
in state, including the ones these pseudo-classes trigger.
