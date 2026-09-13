# Destructuring and Default Parameters — Quick Reference

This is a short index entry. Full treatment lives in
[destructuring.md](../arrays-and-objects/destructuring.md) (arrays and objects) and
[parameters-and-return-values.md](../functions/parameters-and-return-values.md) (default
parameters).

## The Essentials

```js
const [first, second] = ["a", "b"];        // array destructuring — positional
const { name, age = 0 } = user;             // object destructuring — by name, with a default
function greet(name = "Guest") { /* ... */ } // default parameter
```

Both destructuring defaults and default parameters apply the same rule: the default is used only
when the value is `undefined` — not for other falsy values like `null` or `0`.

## Next

Continue to [spread-and-rest-operators.md](spread-and-rest-operators.md).
