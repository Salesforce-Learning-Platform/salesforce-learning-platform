# Enums

## Basic Syntax

```ts
enum Status {
  Pending,
  Active,
  Closed,
}

let current: Status = Status.Active;
```

An **enum** defines a named set of related constants. By default, each member is assigned a
numeric value starting at `0` (`Pending = 0`, `Active = 1`, `Closed = 2`), though string values can
be specified explicitly:

```ts
enum Status {
  Pending = "PENDING",
  Active = "ACTIVE",
  Closed = "CLOSED",
}
```

## The Real Tradeoff: Enums vs. String Union Literals

```ts
// Enum
enum Status { Pending, Active, Closed }

// String union literal (from unions-and-intersections.md)
type Status = "pending" | "active" | "closed";
```

Both express "one of a fixed set of named options," but they differ in practice:

| | `enum` | String union literal |
|---|---|---|
| Compiles to actual runtime JavaScript code? | Yes — a real object exists at runtime | No — completely erased, exactly like other types |
| Works naturally with plain JSON/API data? | Requires the exact enum member, not just a matching string | A plain string value already satisfies it directly |

Because `enum` produces real runtime code (not just erased at compile time, unlike everything else
covered in this module), and because API responses typically arrive as plain strings rather than
actual enum instances, many modern TypeScript codebases prefer string union literals for this exact
use case — genuinely worth knowing as a deliberate choice, not because enums are wrong, but because
the union alternative is often a better fit for data crossing a real boundary (an API response, for
instance).

## When Enums Are Still a Reasonable Choice

Enums remain a reasonable, common choice for a fixed, purely internal set of related constants
that never needs to round-trip through JSON or an external API as a bare string — the choice is a
genuine tradeoff, not a strict rule.

## Common Mistakes

- Reaching for `enum` by default without considering whether a string union literal would integrate
  more naturally with API data the values will actually need to match against.
- Assuming enums are "free" like other TypeScript types — they generate actual runtime JavaScript,
  a real (if usually small) difference from most of this module's other constructs.
- Mixing numeric and explicit-string enum members inconsistently within the same enum, making the
  underlying values harder to predict at a glance.

## Next

Continue to [generics.md](generics.md) for writing type-safe code that works across multiple
types.
