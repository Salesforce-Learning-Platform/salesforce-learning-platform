# Type Aliases

## A More General Naming Tool

```ts
type UserId = string;
type Point = { x: number; y: number };
type Status = "pending" | "active" | "closed"; // a union of literal string values
```

A `type` alias gives a name to *any* type — an object shape (like `interface` does), but also a
primitive alias, a union, a tuple, or a function signature. `interface` is restricted specifically
to describing object (and function) shapes; `type` has no such restriction.

## `interface` vs. `type` for Object Shapes

For a plain object shape, the two are nearly interchangeable:

```ts
interface User { name: string; }
type User2 = { name: string; };
```

The practical differences:

| | `interface` | `type` |
|---|---|---|
| Can describe a union (`"a" \| "b"`)? | No | Yes |
| Can be re-opened and extended later (declaration merging)? | Yes | No |
| Extending another shape | `extends` | `&` (intersection, see [unions-and-intersections.md](unions-and-intersections.md)) |

A common, reasonable convention: use `interface` for object shapes that represent a genuine
"thing" in your domain (a `User`, a component's `Props`), and `type` for everything else — unions,
tuples, function signatures, or utility compositions.

## Common Mistakes

- Assuming `type` and `interface` are fully interchangeable in every situation — a `type` cannot
  describe certain patterns (declaration merging) that `interface` supports, and `interface`
  cannot directly express a union.
- Picking one exclusively out of habit without knowing why, then being unable to explain the
  actual tradeoffs when reviewing someone else's choice.
- Reaching for a `type` alias for a trivial, single-use case where inline annotation would be
  simpler and equally clear.

## Next

Continue to [unions-and-intersections.md](unions-and-intersections.md) — the feature that most
clearly distinguishes what `type` can express beyond `interface`.
