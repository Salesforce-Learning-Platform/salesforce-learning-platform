# Forms — Introduction

## Scope of This File

This is a lightweight introduction to HTML forms, covering just enough to recognize and use the
basic elements. A full, dedicated treatment — input types, validation, accessibility patterns, and
handling submission — is covered in the
[HTML Forms and User Input](../html-forms-and-user-input/) module.

## The Core Elements

```html
<form action="/submit" method="post">
  <label for="email">Email</label>
  <input type="email" id="email" name="email">

  <button type="submit">Submit</button>
</form>
```

| Element | Role |
|---|---|
| `<form>` | Wraps the whole form; `action` and `method` control where and how it submits |
| `<label>` | Text describing an input — linked via `for`/`id`, this is what makes forms usable and accessible |
| `<input>` | The most common form control; its `type` attribute (`text`, `email`, `checkbox`, etc.) determines its behavior |
| `<button>` | A clickable control; `type="submit"` submits the form |

## Why `<label>` Is Not Optional

A `<label>` correctly associated with its input (via matching `for`/`id`, or by wrapping the input)
does two concrete things: it makes the label text itself clickable to focus the input (helpful for
small checkboxes/radio buttons), and it's what a screen reader announces when the input receives
focus. An input with only placeholder text and no `<label>` is effectively unlabeled for assistive
technology once the field has content in it.

## Common Mistakes

- Using placeholder text as a substitute for a `<label>` — placeholder text disappears once the
  user types, and isn't reliably announced by all assistive technology the same way a label is.
- Forgetting the `for`/`id` association, leaving a label visually near an input but not
  programmatically connected to it.
- Using a generic `<div>` with a click handler instead of an actual `<button>`, losing built-in
  keyboard activation and correct semantics.

## Next

Continue to [accessibility-basics.md](accessibility-basics.md) to see how the semantic choices
covered throughout this module directly determine whether a page is usable with assistive
technology.
