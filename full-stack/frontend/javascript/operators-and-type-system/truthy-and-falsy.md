# Truthy and Falsy

## The Complete List of Falsy Values

When a value is used where a boolean is expected (an `if` condition, `&&`/`||`, a ternary), it's
implicitly coerced to `true` or `false`. JavaScript defines exactly eight falsy values — **every
other value is truthy**:

```text
false
0
-0
0n        (BigInt zero)
""        (empty string)
null
undefined
NaN
```

## Everything Else Is Truthy — Including Some Surprising Cases

```js
if ([]) { }        // truthy — an empty array is still an object
if ({}) { }         // truthy — an empty object is still an object
if ("0") { }         // truthy — a non-empty string, even containing "0"
if ("false") { }      // truthy — a non-empty string, even containing the word "false"
```

Empty arrays and objects being truthy is the single most common surprise here — beginners
frequently expect `[]` or `{}` to be falsy since they "feel empty," but they're still objects, and
all objects are truthy regardless of their contents.

## Using Truthiness in Practice

```js
function greet(name) {
  if (!name) {
    name = "Guest"; // handles "", null, undefined, and 0 uniformly
  }
  return `Hello, ${name}`;
}
```

This pattern is powerful specifically because it uniformly handles multiple different "empty-ish"
inputs (`""`, `null`, `undefined`) with one check — but it can also be *too* broad, incorrectly
treating a legitimate `0` or `false` value as "empty" when that wasn't intended (this is exactly
the `||` vs. `??` distinction from [operators.md](operators.md)).

## Checking for Emptiness Precisely

When a legitimate falsy value (like `0`) must be distinguished from genuine absence, check
explicitly rather than relying on general truthiness:

```js
if (value === null || value === undefined) { /* genuinely absent */ }
// or, more concisely:
if (value == null) { /* == null also matches undefined, per the special case in type-coercion.md */ }
```

## Common Mistakes

- Assuming `[]` or `{}` are falsy because they "look empty" — both are truthy, since they're
  objects.
- Using a general truthiness check (`if (!value)`) when the actual intent was "check specifically
  for null/undefined," incorrectly treating a valid `0` or `""` as missing.
- Forgetting `NaN` is falsy, leading to unexpected behavior when a failed numeric parse (`NaN`)
  flows into a truthiness check instead of being explicitly handled.

## Module Summary

Across this module: JavaScript's operators include several with commonly misunderstood behavior —
`+`'s dual role, `??` vs. `||`, and the return value of `&&`/`||` (see
[operators.md](operators.md)); implicit type coercion explains most of JavaScript's "weird"
comparison results, and `===`/`!==` sidestep the need to memorize `==`'s coercion rules entirely
(see [type-coercion.md](type-coercion.md)); and exactly eight values are falsy, with everything
else — including empty arrays and objects — truthy, which matters directly for writing correct
conditions.
