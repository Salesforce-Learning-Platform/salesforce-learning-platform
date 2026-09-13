# HTML Validation and Constraints

## The Constraint Validation API

HTML forms have built-in validation, enforced by the browser before a form submits, using
attributes like `required`, `min`/`max`, `minlength`/`maxlength`, and `pattern`. This is called the
**Constraint Validation API**, and it prevents a form from submitting at all if any constraint is
violated — the browser shows a native error message and focuses the invalid field automatically.

```html
<input type="text" required minlength="4" maxlength="8" pattern="[A-Za-z0-9]+">
```

This single line, with no JavaScript, enforces: not empty, 4–8 characters, alphanumeric only.

## What This Actually Protects Against

Built-in HTML validation is enforced **by the browser rendering the form** — which means it
protects against accidental mistakes by a well-behaved user filling out the form normally
(forgetting a required field, typing an obviously malformed email). It does **not** protect
against:

- A request sent directly to the server's endpoint, bypassing the form and the browser's
  validation entirely (via a script, `curl`, or a modified request).
- A user with browser DevTools removing the `required` attribute or the whole constraint before
  submitting.
- JavaScript calling `form.submit()` in ways that can bypass some constraint checks, depending on
  how the code is written.

This is a direct application of the principle from
[frontend-and-backend-responsibilities.md](../../foundations/client-server-architecture/frontend-and-backend-responsibilities.md):
**the client is never trustworthy**. HTML constraint validation is real, useful UX — instant
feedback with zero network round trip — but the server must always independently re-validate every
field, exactly as if the HTML-level constraints didn't exist at all.

## Checking Validity Programmatically

```js
const input = document.querySelector('input');
input.checkValidity();       // returns true/false
input.setCustomValidity("Custom error message"); // forces a custom validation error
```

`checkValidity()` lets JavaScript inspect the same built-in validation state the browser uses,
useful for custom UI around validation errors without abandoning the native constraint system
entirely.

## Styling Validation States

CSS pseudo-classes let you style fields based on their current validation state without any
JavaScript:

| Pseudo-class | Matches |
|---|---|
| `:required` | Fields with the `required` attribute |
| `:optional` | Fields without it |
| `:valid` | Fields currently passing all constraints |
| `:invalid` | Fields currently failing at least one constraint |

## Common Mistakes

- Treating `required`/`pattern`/`min`/`max` as a security control rather than a UX convenience —
  see [frontend-and-backend-responsibilities.md](../../foundations/client-server-architecture/frontend-and-backend-responsibilities.md)
  for why this specific mistake is a recurring, real source of vulnerabilities.
- Styling every field red with `:invalid` immediately on page load, before the user has even had a
  chance to fill anything in — usually better applied only after a field has been interacted with.
- Writing an overly strict `pattern` that rejects legitimately valid input (an uncommon but real
  email format, an international phone number).

## Next

Continue to
[accessible-form-patterns.md](accessible-form-patterns.md) to ensure these validated forms are
actually usable with assistive technology.
