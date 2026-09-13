# Spread and Rest Operators — Quick Reference

This is a short index entry. Full treatment lives in
[array-methods.md](../arrays-and-objects/array-methods.md) and
[object-methods.md](../arrays-and-objects/object-methods.md) (spread for copying/merging) and
[parameters-and-return-values.md](../functions/parameters-and-return-values.md) (rest parameters).

## The Essentials

```js
const copy = [...originalArray];              // spread: expand into individual elements
const merged = { ...defaults, ...overrides };  // spread: merge objects, later keys win
function sum(...numbers) { /* numbers is a real array */ } // rest: collect into an array
```

Both use identical `...` syntax, doing opposite jobs depending on context: **spread** expands a
collection into individual elements/properties; **rest** collects individual arguments/elements
back into a single array.

## Next

Continue to [template-literals.md](template-literals.md) for a genuinely new topic in this module.
