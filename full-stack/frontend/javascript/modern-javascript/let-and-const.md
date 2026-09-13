# Let and Const — Quick Reference

This is a short index entry. The full treatment — block vs. function scope, why `const` doesn't
mean "never changes," and why `var` is avoided — lives in
[variables.md](../introduction-to-javascript/variables.md), where it's covered as soon as
variables are first introduced.

## The Essentials

```js
const name = "Ada";  // default choice — binding cannot be reassigned
let count = 0;         // use only when reassignment is genuinely needed
count += 1;              // allowed
name = "Grace";           // TypeError — const cannot be reassigned
```

- Default to `const`.
- Use `let` only when a variable's value genuinely needs to change.
- Avoid `var` entirely in new code — see
  [variables.md](../introduction-to-javascript/variables.md) for exactly why its function-scoping
  behavior causes real bugs, and
  [closures.md](../functions/closures.md) for the classic loop-and-closure bug `let` fixes that
  `var` cannot.

## Next

Continue to
[destructuring-and-default-parameters.md](destructuring-and-default-parameters.md).
