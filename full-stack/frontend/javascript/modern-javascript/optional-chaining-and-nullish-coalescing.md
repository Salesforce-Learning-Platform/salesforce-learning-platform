# Optional Chaining and Nullish Coalescing

## The Problem: Chained Access on Possibly-Missing Values

[objects.md](../arrays-and-objects/objects.md) flagged this exact common mistake: accessing a
property on a value that might be `undefined` throws a `TypeError`:

```js
user.address.city; // TypeError if `user.address` doesn't exist
```

## Optional Chaining (`?.`)

```js
user.address?.city;      // undefined, safely, if `address` is null/undefined — no error
user.getPreferences?.();  // calls the method only if it actually exists; otherwise undefined
users?.[0]?.name;          // works with bracket notation and array indexing too
```

`?.` short-circuits: the moment it encounters `null` or `undefined`, it immediately stops and
evaluates the whole expression to `undefined`, without attempting the rest of the chain (and
without throwing).

## Chaining Multiple `?.`

```js
user?.address?.city?.toUpperCase();
```

Each `?.` independently guards against its own immediately preceding value being nullish — the
whole expression safely evaluates to `undefined` if *any* link in the chain is missing, without
needing a separate check for each level.

## Nullish Coalescing (`??`)

```js
const displayName = user.nickname ?? "Anonymous";
```

As introduced in [operators.md](../operators-and-type-system/operators.md), `??` provides a
fallback specifically for `null`/`undefined` — unlike `||`, it does **not** treat other falsy
values (`0`, `""`, `false`) as needing replacement:

```js
const count = 0;
count || 10;  // 10 — WRONG if 0 is a genuinely valid value, not "missing"
count ?? 10;  // 0  — correctly preserves a genuine value of 0
```

## `?.` and `??` Combined — A Common, Powerful Pairing

```js
const city = user?.address?.city ?? "Unknown";
```

This single line safely navigates a potentially-missing nested path (`?.`) and provides a sensible
fallback specifically for when the final result is genuinely missing (`??`) — replacing what would
otherwise require several explicit `if`/`null` checks.

## Common Mistakes

- Using `?.` everywhere reflexively, even on values that are never actually expected to be
  missing — this can silently hide a genuine bug (an object that *should* always exist but
  doesn't) behind a quietly returned `undefined`, instead of surfacing the problem clearly.
- Using `||` instead of `??` for a fallback when the valid value could legitimately be `0`, `""`,
  or `false` — exactly the mistake flagged in
  [operators.md](../operators-and-type-system/operators.md).
- Forgetting that `?.` only guards against `null`/`undefined` specifically — it doesn't protect
  against other kinds of errors, like calling something that exists but isn't actually a function.

## Module Summary

This module consolidated already-covered ES6+ features (`let`/`const`, destructuring, spread/rest —
see their quick-reference files) and went deep on two genuinely new ones: template literals for
readable string interpolation and multi-line strings (see
[template-literals.md](template-literals.md)), and optional chaining combined with nullish
coalescing for safely navigating and defaulting potentially-missing nested values (this file) —
directly solving the exact "chaining onto a possibly-undefined value" problem flagged earlier in
[objects.md](../arrays-and-objects/objects.md).
