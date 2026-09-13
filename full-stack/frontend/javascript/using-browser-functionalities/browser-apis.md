# Browser APIs

## Beyond the DOM

[DOM Manipulation](../dom-manipulation/) covered one major browser-provided API — the DOM itself.
But the browser exposes many more JavaScript-accessible APIs beyond it: storage mechanisms
(covered in this module), geolocation, notifications, the Fetch API for network requests, and
more. These aren't part of the JavaScript language itself (defined by ECMAScript, per
[what-is-javascript.md](../introduction-to-javascript/what-is-javascript.md)) — they're provided by
the browser environment JavaScript happens to be running in.

## Why This Distinction Matters

Because these are browser-provided, not language-provided, they don't exist in Node.js (which
provides its own, different set of environment APIs — filesystem access, for instance, which a
browser has no equivalent of). Code depending on `localStorage` or `document` will fail in Node,
exactly as code depending on Node's `fs` module would fail in a browser — both are valid
JavaScript, running in environments that simply don't provide the same surrounding APIs.

## The APIs This Module Covers

| API | Purpose |
|---|---|
| `localStorage` | Persistent, origin-scoped key-value storage |
| `sessionStorage` | Tab-scoped storage, cleared when the tab closes |
| `document.cookie` | Reading/writing cookies from client-side JavaScript |

All three exist specifically to solve the same underlying problem introduced in
[state-management-across-the-boundary.md](../../foundations/client-server-architecture/state-management-across-the-boundary.md):
HTTP itself has no memory between requests, so applications need a deliberate mechanism to persist
information on the client between page loads or requests.

## Common Mistakes

- Assuming every JavaScript API works identically in the browser and in Node — environment-provided
  APIs (like `localStorage` or `fs`) are not part of the language itself and don't automatically
  carry over.
- Treating "browser API" as synonymous with "part of JavaScript" — the distinction matters when
  debugging a script that behaves differently, or fails outright, in a different environment.

## Next

Continue to [local-storage.md](local-storage.md) for the first, most commonly used of these
storage mechanisms.
