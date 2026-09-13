# Cookies

## What Makes Cookies Different

Unlike `localStorage`/`sessionStorage` (purely client-side, never automatically sent anywhere),
**cookies** are small pieces of data that get automatically attached to every HTTP request to the
domain that set them — this is exactly the mechanism introduced conceptually in
[state-management-across-the-boundary.md](../../foundations/client-server-architecture/state-management-across-the-boundary.md)
as how servers maintain a session across stateless HTTP requests.

## Reading and Writing via JavaScript

```js
document.cookie = "theme=dark; path=/; max-age=31536000";
console.log(document.cookie); // "theme=dark" (and any other cookies, semicolon-separated)
```

`document.cookie` is a genuinely awkward API: reading it returns *all* cookies as one
semicolon-separated string (requiring manual parsing to extract a specific one), and writing to it
sets *one* cookie at a time without replacing the others — very different from a normal property
assignment.

## Security Attributes

| Attribute | Effect |
|---|---|
| `Secure` | Cookie only sent over HTTPS |
| `HttpOnly` | Cookie inaccessible to JavaScript entirely — settable only via the `Set-Cookie` response header, not `document.cookie` |
| `SameSite` | Controls whether the cookie is sent on cross-site requests (`Strict`, `Lax`, `None`) — a real defense against certain cross-site attacks |

**`HttpOnly` is the key security-relevant attribute for this module**: a cookie marked `HttpOnly`
can never be read or written by client-side JavaScript at all, meaning it's immune to the
XSS-based theft risk that applies to `localStorage`, `sessionStorage`, and any cookie *without*
`HttpOnly` set. This is exactly why session/authentication cookies set by a well-built backend are
typically `HttpOnly` — it removes an entire attack surface by design, at the cost of client-side
JavaScript being unable to read that value at all (which is usually fine, since the browser sends
it automatically anyway).

## Cookies vs. Web Storage — Choosing Correctly

| | Cookies | `localStorage`/`sessionStorage` |
|---|---|---|
| Automatically sent with every HTTP request? | Yes | No — client-side only |
| Can be made inaccessible to JavaScript (`HttpOnly`)? | Yes | No — always readable by any script |
| Typical use | Session/auth tokens the server needs to see | Client-side-only preferences and cached data |

If the server needs to see the value on every request, use a cookie. If it's purely a client-side
concern with no server involvement, Web Storage is simpler and avoids adding to every request's
size unnecessarily.

## Common Mistakes

- Storing a genuinely sensitive session token in `localStorage` "for convenience" instead of an
  `HttpOnly` cookie, unnecessarily exposing it to any script that can run on the page.
- Manually parsing `document.cookie`'s string format repeatedly throughout a codebase instead of
  centralizing that logic (or using a small, well-tested utility) in one place.
- Forgetting the `Secure` attribute on cookies in production, allowing them to be sent over
  unencrypted HTTP if a user somehow reaches the site that way.

## Module Summary

Across this module: browser APIs like storage mechanisms exist outside the JavaScript language
itself and don't automatically carry over to other environments like Node (see
[browser-apis.md](browser-apis.md)); `localStorage` persists indefinitely per origin (see
[local-storage.md](local-storage.md)); `sessionStorage` is scoped to a single tab and cleared on
close (see [session-storage.md](session-storage.md)); and cookies are the only one of the three
automatically sent with every HTTP request, with `HttpOnly` providing real protection against
XSS-based theft that Web Storage cannot offer.
