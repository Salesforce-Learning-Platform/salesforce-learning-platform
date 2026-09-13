# Conditional Statements

## `if` / `else if` / `else`

```js
if (score >= 90) {
  grade = "A";
} else if (score >= 80) {
  grade = "B";
} else {
  grade = "C";
}
```

Conditions are evaluated top to bottom; the first one that's truthy (see
[truthy-and-falsy.md](../operators-and-type-system/truthy-and-falsy.md)) runs, and the rest are
skipped entirely — even if a later condition would also have been true.

## The Ternary Operator

```js
const status = age >= 18 ? "adult" : "minor";
```

`condition ? valueIfTrue : valueIfFalse` is a compact expression form of `if`/`else` — it evaluates
to a *value*, which makes it useful directly inside an assignment or a template literal, where a
full `if`/`else` statement couldn't be used inline.

## Choosing Between Them

| Situation | Prefer |
|---|---|
| Assigning one of two values based on a condition | Ternary |
| Running different blocks of code (multiple statements, side effects) | `if`/`else` |
| More than two branches with genuinely different logic | `if`/`else if`/`else` (or `switch`, if comparing one value against several exact matches) |

Chaining multiple ternaries (`a ? b : c ? d : e`) to express more than one decision is technically
valid but reads poorly — an `if`/`else if` chain is almost always clearer once more than one
condition is involved.

## Common Mistakes

- Nesting ternaries to express complex branching logic, producing code that's hard to read at a
  glance — a plain `if`/`else if` chain is more readable past a single true/false decision.
- Writing `if (condition == true)` instead of simply `if (condition)` — redundant, and risks
  reintroducing the `==` coercion pitfalls from
  [type-coercion.md](../operators-and-type-system/type-coercion.md).
- Forgetting that only the first matching branch in an `if`/`else if` chain runs — order matters,
  and a broader condition placed before a narrower one can unintentionally shadow it.

## Next

Continue to [switch-statements.md](switch-statements.md) for an alternative when comparing one
value against several possible exact matches.
