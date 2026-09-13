# HTML Forms and User Input

## Purpose

[forms-introduction.md](../semantic-html-and-browser-rendering/forms-introduction.md) covered the
bare minimum: `<form>`, `<label>`, `<input>`, `<button>`. This module goes deep on forms
specifically — the full range of input types, how HTML's built-in validation actually works, and
how to keep forms accessible and usable, since forms are where most real user input (and most real
usability and accessibility failures) happen.

## Learning Objectives

- Choose the correct `<input>` type for a given kind of data, and explain what each type gains you
  for free (mobile keyboards, built-in validation, browser UI).
- Use HTML's built-in constraint validation attributes correctly, and explain why they're a UX
  layer, not a security boundary.
- Structure a form so every field is genuinely accessible, including grouped controls.
- Explain what actually happens when a form is submitted.

## Prerequisites

[Semantic HTML and Browser Rendering](../semantic-html-and-browser-rendering/), and
[Frontend and Backend Responsibilities](../../foundations/client-server-architecture/frontend-and-backend-responsibilities.md)
for the client-vs-server validation distinction this module depends on.

## Files in This Module

| File | Covers |
|---|---|
| [input-types-and-attributes.md](input-types-and-attributes.md) | The full range of `<input>` types and the attributes that configure them |
| [html-validation-and-constraints.md](html-validation-and-constraints.md) | Built-in constraint validation: `required`, `pattern`, `min`/`max`, and why it's UX, not security |
| [accessible-form-patterns.md](accessible-form-patterns.md) | Grouping related controls, error messaging, and other accessible form structure |
| [form-submission-and-data.md](form-submission-and-data.md) | What actually happens when a form submits, and how that data reaches the server |

## When to Deep-Dive vs. Skim

Deep-dive [html-validation-and-constraints.md](html-validation-and-constraints.md) if you've ever
relied on client-side validation alone and been surprised that bad data still reached your
database — this is the most consequential misunderstanding this module corrects. If you're already
comfortable with basic inputs, you can skim
[input-types-and-attributes.md](input-types-and-attributes.md) as a reference to revisit later.

## Quick Knowledge Check

<details>
<summary>Why use `type="email"` instead of `type="text"` for an email field?</summary>

It gives you a mobile keyboard optimized for email addresses, basic built-in format validation,
and semantic meaning for assistive technology and browser autofill — all for free, with no extra
code. See [input-types-and-attributes.md](input-types-and-attributes.md).

</details>

<details>
<summary>Is the `required` attribute on an input enough to guarantee that field is never empty in your database?</summary>

No. It's enforced by the browser and can be bypassed (disabled JavaScript won't stop it, but a
direct API request skipping the form entirely will). The server must independently re-validate. See
[html-validation-and-constraints.md](html-validation-and-constraints.md).

</details>

## References

- MDN Web Docs, [The Input (Form Input) element](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input)
- MDN Web Docs, [Using HTML form validation and the Constraint Validation API](https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Constraint_validation)

## Continue Your Learning Path

Next: [HTML Accessibility](../html-accessibility/) — see the
[Frontend learning path](../../README.md) for the full sequence.
