# Form Submission and Data

## What Happens on Submit

When a `<form>` is submitted (via a submit button, or pressing Enter in a text field), the browser
gathers every named, enabled form control's current value and sends it as an HTTP request — this
is a concrete, form-specific instance of the request-response lifecycle covered in
[the-request-response-lifecycle.md](../../foundations/client-server-architecture/the-request-response-lifecycle.md).

## `method` and `action`

```html
<form action="/search" method="get">
  <input type="text" name="q">
</form>
```

- **`action`** is the URL the request is sent to.
- **`method`** determines the HTTP method used — `get` or `post` (see
  [http-methods-in-depth.md](../../foundations/understanding-http-and-https/http-methods-in-depth.md)
  for the full semantics).

## `GET` vs. `POST` Forms — Where the Data Actually Goes

| | `method="get"` | `method="post"` |
|---|---|---|
| Where data travels | Appended to the URL as a query string (`?q=value`) | In the request body, not visible in the URL |
| Bookmarkable/shareable? | Yes — the full state is in the URL | No |
| Appropriate for | Searches, filters — retrieving data | Creating, updating, or submitting sensitive data |
| Visible in browser history/logs? | Yes | No (though still visible on the wire unless HTTPS is used) |

This maps directly onto the safety/idempotency distinction in
[http-methods-in-depth.md](../../foundations/understanding-http-and-https/http-methods-in-depth.md):
a search form is naturally a `GET` (safe, bookmarkable, retrieval), while a form submitting a
password, payment detail, or anything creating/modifying data should be a `POST` — never exposed
in a URL, browser history, or server access logs.

## What's Actually Sent

Only controls with a `name` attribute are included, using that name as the key. `disabled` controls
are excluded entirely; unchecked checkboxes are excluded (not sent as `false` — their absence
*is* the "unchecked" signal, which is a common source of confusion when a backend expects an
explicit boolean).

```html
<form>
  <input type="text" name="username" value="alice">
  <input type="checkbox" name="subscribe" checked>
  <input type="checkbox" name="newsletter"> <!-- unchecked: NOT sent at all -->
</form>
```

## Intercepting Submission with JavaScript

Modern applications frequently handle submission with JavaScript instead of a full page
navigation — listening for the form's `submit` event, calling `event.preventDefault()` to stop the
browser's default navigation, then sending the data via `fetch()` and updating the page without a
reload. This doesn't remove any of the accessibility or validation behavior covered earlier in this
module — a JavaScript-driven form should still trigger native constraint validation, and should
still move focus to errors, exactly as covered in
[accessible-form-patterns.md](accessible-form-patterns.md).

## Common Mistakes

- Using `method="get"` for a form submitting sensitive data, exposing it in the URL, browser
  history, and server access logs.
- Forgetting that an unchecked checkbox sends no value at all, and having server-side code that
  assumes a missing key means something other than "unchecked."
- Intercepting form submission with JavaScript and forgetting to re-implement the focus-management
  and validation behavior the browser previously handled automatically.

## Module Summary

Across this module: `<input>` types configure both browser UI and mobile keyboard behavior for
free (see [input-types-and-attributes.md](input-types-and-attributes.md)); HTML's built-in
constraint validation is genuinely useful UX but never a substitute for server-side validation
(see [html-validation-and-constraints.md](html-validation-and-constraints.md)); grouping,
error-message association, and focus management are what make a form's validation actually
accessible (see [accessible-form-patterns.md](accessible-form-patterns.md)); and `method`/`action`
determine exactly how and where submitted data travels, with real security and usability
consequences riding on that choice.
