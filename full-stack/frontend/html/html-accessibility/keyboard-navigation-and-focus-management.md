# Keyboard Navigation and Focus Management

## Why This Is Non-Negotiable

Some users cannot use a mouse at all — due to a motor disability, because they use a screen reader
(which relies on keyboard navigation), or simply by preference. A page that's only usable with a
mouse excludes them entirely, regardless of how visually polished it is.

## Focusable Elements and Tab Order

Native interactive elements (`<a href>`, `<button>`, form controls) are keyboard-focusable by
default, in the order they appear in the DOM — this was introduced in
[links-and-navigation-flow.md](../semantic-html-and-browser-rendering/links-and-navigation-flow.md).
Two attributes let you adjust this deliberately:

| Attribute | Effect |
|---|---|
| `tabindex="0"` | Makes a non-interactive element (like a `<div>`) focusable, inserted into the natural tab order |
| `tabindex="-1"` | Makes an element programmatically focusable (via JavaScript) but removes it from the natural Tab-key order |
| `tabindex="1"` or higher | Forces a specific tab order — almost always a mistake, since it's easy to create a confusing order that doesn't match visual/reading order |

## Visible Focus Indicators

The browser's default focus outline is what tells a keyboard user which element is currently
active. A common but harmful pattern is removing it globally:

```css
/* Don't do this without providing a replacement */
*:focus {
  outline: none;
}
```

If a custom focus style is needed for visual design reasons, replace the outline with an equally
visible alternative — never remove it with nothing in its place. `:focus-visible` (rather than
`:focus`) can be used to show the indicator only for keyboard users while leaving mouse-click
focus styling unobtrusive, without removing keyboard accessibility.

## Managing Focus in Dynamic Interfaces

When JavaScript opens a new piece of UI (a modal dialog, a menu), focus should move to it
deliberately, and return to a sensible place when it closes:

- **Opening a modal**: move focus to the modal itself (or its first focusable element), and trap
  Tab navigation inside it while open — a keyboard user should not be able to tab to content
  behind the modal.
- **Closing a modal**: return focus to the element that opened it, so keyboard navigation resumes
  exactly where the user left off, rather than being reset to the top of the page.

This is a natural extension of the form-error focus management introduced in
[accessible-form-patterns.md](../html-forms-and-user-input/accessible-form-patterns.md) — the same
underlying principle (focus should always land somewhere meaningful after a UI change) applies
throughout an application, not just to forms.

## Common Mistakes

- Removing the default focus outline with `outline: none` and providing no visible replacement —
  one of the single most common, and most damaging, accessibility regressions.
- Building a custom dropdown or modal that traps mouse users' attention visually but leaves
  keyboard users able to tab to (and interact with) content hidden behind it.
- Using very high `tabindex` values to "fix" tab order instead of fixing the actual DOM order to
  match the intended reading/interaction order.

## Next

Continue to [inclusive-design-principles.md](inclusive-design-principles.md) to place these
specific techniques within a broader way of thinking about who you're actually designing for.
