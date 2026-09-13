# Local Storage

## Basic API

```js
localStorage.setItem("theme", "dark");
localStorage.getItem("theme");   // "dark"
localStorage.removeItem("theme");
localStorage.clear();              // removes everything for this origin
```

`localStorage` stores simple key-value pairs, **as strings only** — storing anything else requires
converting it first:

```js
localStorage.setItem("user", JSON.stringify({ name: "Ada", age: 36 }));
const user = JSON.parse(localStorage.getItem("user"));
```

## Persistence and Scope

`localStorage` data persists indefinitely — across page reloads, browser restarts, and even system
reboots — until explicitly cleared by code or the user. It's scoped **per origin** (scheme + host +
port): data stored by `https://example.com` is invisible to `https://other-site.com`, and even to
`http://example.com` (a different scheme counts as a different origin).

## What It's Good For

- Remembering user preferences (a theme choice, a dismissed banner) across visits.
- Caching non-sensitive data client-side to avoid refetching it every visit.
- Persisting draft content (an unsent form) so a user doesn't lose it on an accidental tab close.

## What It's Not Good For

- **Sensitive data.** `localStorage` is plain-text and fully readable by any JavaScript running on
  that origin — including malicious script injected via an XSS vulnerability (see
  [manipulating-elements.md](../dom-manipulation/manipulating-elements.md)). It offers no
  protection an attacker's script couldn't simply bypass by reading it directly.
- **Large amounts of data.** Storage quotas are limited (commonly a few megabytes per origin,
  varying by browser) and operations are synchronous, which can block the main thread for larger
  reads/writes — IndexedDB is the appropriate tool for larger or more complex client-side data.

## Common Mistakes

- Storing an object directly without `JSON.stringify()`, which silently stores the unhelpful string
  `"[object Object]"` instead of the actual data.
- Storing authentication tokens or other sensitive data in `localStorage`, exposing them to any
  script that can execute on the page.
- Assuming `localStorage` is shared across different origins or subdomains — it's strictly scoped
  per origin.

## Next

Continue to [session-storage.md](session-storage.md) for the tab-scoped alternative.
