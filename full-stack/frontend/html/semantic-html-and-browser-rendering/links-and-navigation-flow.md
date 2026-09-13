# Links and Navigation Flow

## The Anchor Element

`<a href="...">` is how HTML represents a hyperlink — a reference a user can navigate to. It's one
of the oldest and most fundamental elements in HTML, and also one of the most frequently misused.

## Writing Accessible Link Text

- **Link text should make sense out of context.** "Click here" or "Read more" convey nothing when
  a screen reader user pulls up a list of all links on the page (a common navigation strategy) —
  "Read the full accessibility report" does.
- **Don't use a link for something that isn't navigation.** A control that submits a form or
  toggles UI state should be a `<button>`, not an `<a>` with `href="#"` — this preserves correct
  keyboard behavior (Enter activates a link, Space activates a button) and correct semantics for
  assistive technology.

## Internal vs. External Links

| Link type | `href` example | Notes |
|---|---|---|
| Same page anchor | `href="#section-2"` | Jumps to an element with `id="section-2"` |
| Relative internal | `href="/about"` | Stays within the same site |
| Absolute external | `href="https://example.com"` | Leaves the site |

For external links opening in a new tab (`target="_blank"`), also add `rel="noopener noreferrer"`
— `noopener` prevents the new page from being able to access and manipulate the originating page
via `window.opener` (a real security consideration), and `noreferrer` additionally withholds
referrer information.

## Skip Links

A **skip link** is a link, usually the very first focusable element on the page, that lets
keyboard users jump directly past repeated navigation to the main content — without it, a keyboard
user must tab through every navigation link on every single page load before reaching the content:

```html
<a href="#main-content" class="skip-link">Skip to main content</a>
...
<main id="main-content">...</main>
```

It's typically visually hidden until it receives keyboard focus, at which point it becomes visible.

## Navigation Flow and Tab Order

Interactive elements (`<a>`, `<button>`, form controls) are focusable by keyboard `Tab` navigation
in the order they appear in the HTML by default. Keeping DOM order matching visual/logical reading
order is what keeps this default tab order sensible — reordering elements purely with CSS while
leaving the underlying HTML order illogical creates a confusing experience for keyboard-only
users, even though sighted mouse users notice nothing wrong.

## Common Mistakes

- Using non-descriptive link text ("click here," "learn more") repeated multiple times on one
  page, indistinguishable to a screen reader's link-list navigation.
- Using `<a href="#">` or `<a href="javascript:void(0)">` to fake a button — use an actual
  `<button>` element instead.
- Visually reordering interactive elements with CSS without also correcting the underlying tab
  order, creating a mismatch between visual and keyboard navigation flow.

## Next

Continue to [forms-introduction.md](forms-introduction.md) for the basics of the other major
category of interactive HTML elements.
