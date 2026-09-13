# Type Coercion

## Implicit vs. Explicit Coercion

**Coercion** is converting a value from one type to another. JavaScript does this **implicitly**
(automatically, often surprisingly) in many operations, and it can also be done **explicitly**
(deliberately, by the developer) using conversion functions.

```js
// Implicit
"5" + 3;      // "53" — number coerced to string
"5" - 3;      // 2   — string coerced to number
true + 1;     // 2   — boolean coerced to number

// Explicit
String(5);    // "5"
Number("5");  // 5
Boolean(0);   // false
```

## Why `+` and `-` Behave Differently

This is the source of the classic `"5" + 3` vs. `"5" - 3` confusion introduced in this module's
README: `+` is overloaded to mean both numeric addition and string concatenation, so if *either*
operand is a string, JavaScript concatenates. `-` has no string meaning at all, so JavaScript
instead coerces both operands to numbers before subtracting.

## `==` Performs Coercion; `===` Does Not

```js
0 == false;       // true  — both coerced to a common type before comparing
0 === false;      // false — different types, no coercion, immediately unequal

null == undefined;  // true  — a specific special case in the spec
null === undefined; // false — different types
```

`==`'s coercion rules are numerous and genuinely hard to memorize completely — this is the primary,
concrete reason `===` is universally recommended: it sidesteps the entire rule set by refusing to
compare across types at all.

## `NaN` — Not a Number, But Still a Number Type

```js
typeof NaN;      // "number" (yes, really)
NaN === NaN;      // false — NaN is never equal to anything, including itself
Number.isNaN(NaN); // true — the reliable way to actually check for NaN
```

`NaN` ("Not a Number") is the result of an invalid numeric operation (like `0 / 0` or
`Number("abc")`), and its self-inequality is a specification-defined property, not a bug —
`Number.isNaN()` is the correct, reliable way to test for it, rather than `=== NaN`, which always
returns `false`.

## Common Mistakes

- Relying on implicit coercion for correctness rather than as a well-understood, deliberate choice
  — code that works "by accident" through coercion is fragile to future changes.
- Using `value === NaN` to check for `NaN`, which always evaluates to `false` regardless of
  `value`.
- Assuming `==`'s coercion rules are simple or intuitive — they have enough edge cases that
  defaulting to `===` is safer than trying to memorize every `==` rule.

## Next

Continue to [truthy-and-falsy.md](truthy-and-falsy.md) to see how coercion applies specifically
inside conditions.
