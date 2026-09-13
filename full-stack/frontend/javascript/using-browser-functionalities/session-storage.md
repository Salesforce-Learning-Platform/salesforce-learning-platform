# Session Storage

## Same API, Different Lifetime

```js
sessionStorage.setItem("checkoutStep", "2");
sessionStorage.getItem("checkoutStep"); // "2"
sessionStorage.removeItem("checkoutStep");
```

`sessionStorage`'s API is identical to `localStorage`'s (`setItem`/`getItem`/`removeItem`/`clear`,
strings only) — the entire difference is in **how long the data survives**.

## `localStorage` vs. `sessionStorage`

| | `localStorage` | `sessionStorage` |
|---|---|---|
| Survives a tab close? | Yes | No — cleared immediately |
| Survives a browser restart? | Yes | No |
| Shared across tabs of the same site? | Yes | No — each tab gets its own separate storage |
| Scope | Per origin | Per origin, per tab |

Opening the same site in two different tabs gives each tab its **own independent**
`sessionStorage`, even though they share the same `localStorage`.

## What It's Good For

- Multi-step form or checkout progress that should reset if the user starts a fresh tab, but
  should survive an accidental reload within the same tab.
- Data that's only meaningful for the current browsing session and shouldn't linger afterward.
- Avoiding unwanted state leakage between multiple tabs of the same application open
  simultaneously — since each tab's `sessionStorage` is independent.

## Common Mistakes

- Reaching for `sessionStorage` when data actually needs to persist across a closed tab or browser
  restart — `localStorage` is the correct tool for that.
- Assuming `sessionStorage` is shared across tabs the way `localStorage` is — each tab genuinely
  has its own separate storage, even for the same site.
- Storing sensitive data here under the assumption that its shorter lifetime makes it safer — the
  same XSS-readability concern from [local-storage.md](local-storage.md) applies equally to
  `sessionStorage`.

## Next

Continue to [cookies.md](cookies.md) for the older, but still widely used, client-side storage
mechanism — and the one with genuine server-visible and security-relevant properties the other two
lack.
