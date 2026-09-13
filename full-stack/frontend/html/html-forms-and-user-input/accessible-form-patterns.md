# Accessible Form Patterns

## Building on the Basics

[accessibility-basics.md](../semantic-html-and-browser-rendering/accessibility-basics.md)
established that a correctly associated `<label>` is the foundation of form accessibility. This
file covers the patterns needed once a form has more than a single, simple field.

## Grouping Related Controls: `<fieldset>` and `<legend>`

When several inputs form one logical group — a set of radio buttons, or related checkboxes — wrap
them in a `<fieldset>` with a `<legend>` describing the group as a whole:

```html
<fieldset>
  <legend>Preferred contact method</legend>
  <input type="radio" id="contact-email" name="contact" value="email">
  <label for="contact-email">Email</label>
  <input type="radio" id="contact-phone" name="contact" value="phone">
  <label for="contact-phone">Phone</label>
</fieldset>
```

Without this grouping, a screen reader announces each radio button's own label ("Email," "Phone")
with no indication of what question they're answering together — the `<legend>` is what provides
that context.

## Associating Error Messages

A validation error message should be programmatically linked to its field, not just placed nearby
visually, using `aria-describedby`:

```html
<label for="email">Email</label>
<input type="email" id="email" aria-describedby="email-error" aria-invalid="true">
<span id="email-error">Please enter a valid email address.</span>
```

`aria-describedby` tells assistive technology to announce the referenced text as part of the
field's description — without it, a sighted user sees the error message next to the field, but a
screen reader user may never hear it associated with that specific field at all.

## Indicating Required Fields Clearly

The `required` HTML attribute is necessary but not sufficient for a good experience — also
communicate it visually and textually (an asterisk with a legend explaining it, or the word
"required" in the label itself), since a purely visual-only indicator (color alone) can fail both
accessibility and simple readability.

## Focus Management on Submission

When a form submission fails validation, moving keyboard focus to the first invalid field (or a
summary of errors) lets a keyboard or screen reader user immediately address the problem, rather
than having to search the page for what went wrong. Browsers do this automatically for native HTML
constraint validation failures (see
[html-validation-and-constraints.md](html-validation-and-constraints.md)); custom, JavaScript-driven
validation needs to replicate this deliberately.

## Common Mistakes

- Grouping related radio buttons or checkboxes visually (with spacing or a border) but without an
  actual `<fieldset>`/`<legend>`, leaving the grouping invisible to assistive technology.
- Displaying an error message that's only connected to its field by visual proximity, with no
  `aria-describedby` link.
- Relying on color alone (red text, a red border) to indicate an error, with no text or icon
  conveying the same information for someone who can't perceive that color difference.

## Next

Continue to [form-submission-and-data.md](form-submission-and-data.md) to see what actually
happens once a user submits a correctly built, accessible form.
