# Operators

## Arithmetic Operators

```js
5 + 3;   // 8
5 - 3;   // 2
5 * 3;   // 15
5 / 3;   // 1.666...
5 % 3;   // 2 (remainder)
5 ** 3;  // 125 (exponentiation)
```

## Comparison Operators

| Operator | Meaning |
|---|---|
| `==` | Loose equality — coerces types before comparing (avoid, see [type-coercion.md](type-coercion.md)) |
| `===` | Strict equality — no coercion; both value and type must match |
| `!=` / `!==` | Loose / strict inequality |
| `<`, `>`, `<=`, `>=` | Relational comparison |

```js
5 === "5";  // false — different types
5 == "5";   // true — "5" is coerced to 5 first
```

**Always prefer `===`/`!==`.** They eliminate an entire category of coercion-related bugs by
refusing to compare values of different types as if they were equal.

## Logical Operators

| Operator | Meaning | Notable behavior |
|---|---|---|
| `&&` | AND | Returns the first falsy operand, or the last operand if all are truthy |
| `\|\|` | OR | Returns the first truthy operand, or the last operand if all are falsy |
| `!` | NOT | Converts to boolean and inverts |
| `??` | Nullish coalescing | Returns the right side only if the left is `null`/`undefined` (not just falsy) |

```js
let name = userInput || "Guest";  // "Guest" if userInput is falsy (including "")
let count = userCount ?? 0;        // 0 only if userCount is null/undefined, NOT if it's 0
```

`||` vs. `??` is an important distinction: `||` falls back on *any* falsy value, while `??` falls
back only on `null`/`undefined` — meaning `userCount || 0` would incorrectly replace a genuine
value of `0` with `0` again (harmless here, but replacing a genuine `0`, `""`, or `false` with a
fallback is a real, common bug when `||` is used where `??` was actually intended).

## Assignment Operators

```js
let x = 5;
x += 3;  // x = x + 3
x -= 2;  // x = x - 2
x *= 2;  // x = x * 2
```

Compound assignment operators (`+=`, `-=`, etc.) combine an operation with reassignment in one
step.

## Common Mistakes

- Using `==`/`!=` instead of `===`/`!==`, allowing unintended type coercion into a comparison.
- Using `||` for a default value when the valid value could legitimately be `0`, `""`, or `false` —
  `??` is the correct tool for "only replace null/undefined."
- Confusing `&&`/`||`'s actual return value (the operand itself, not necessarily `true`/`false`)
  with a pure boolean result — this is a real, commonly used pattern (`condition && doSomething()`)
  but worth understanding precisely rather than by accident.

## Next

Continue to [type-coercion.md](type-coercion.md) for exactly how and when JavaScript converts
between types automatically.
