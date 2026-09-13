# Array Methods

## The Core Transformation Methods

```js
const numbers = [1, 2, 3, 4, 5];

numbers.map(n => n * 2);          // [2, 4, 6, 8, 10] — transform each element
numbers.filter(n => n % 2 === 0);  // [2, 4]           — keep matching elements
numbers.reduce((sum, n) => sum + n, 0); // 15            — combine into one value
numbers.find(n => n > 3);           // 4               — first matching element, or undefined
numbers.forEach(n => console.log(n)); // runs a function per element, returns undefined
```

| Method | Returns | Use for |
|---|---|---|
| `map` | A new array, same length | Transforming every element |
| `filter` | A new array, possibly shorter | Keeping only elements matching a condition |
| `reduce` | A single accumulated value | Combining all elements into one result (a sum, an object, another array) |
| `find` | The first matching element (or `undefined`) | Locating one specific element |
| `some` / `every` | A boolean | Checking if any/all elements match a condition |
| `forEach` | `undefined` | Running side effects per element (logging, DOM updates) — not for building a new array |

## Mutating vs. Non-Mutating — The Critical Distinction

| Non-mutating (return a new array/value) | Mutating (change the array in place) |
|---|---|
| `map`, `filter`, `reduce`, `find`, `slice`, `concat` | `push`, `pop`, `shift`, `unshift`, `splice`, `sort`, `reverse` |

```js
const original = [3, 1, 2];

const sorted = [...original].sort(); // copy first, then sort the copy
original.sort();                       // mutates `original` directly — no copy
```

This distinction matters enormously once other code holds a reference to the same array (a very
common situation) — a mutating method silently changes the array for every reference to it, while
a non-mutating method leaves the original completely untouched and produces a new one. React's
correctness (covered in its own domain) depends specifically on treating state as immutable and
using non-mutating operations, which is exactly why this distinction is called out here as worth
deep-diving.

## Chaining

```js
const total = numbers
  .filter(n => n % 2 === 0)
  .map(n => n * 10)
  .reduce((sum, n) => sum + n, 0);
// filters to [2, 4], maps to [20, 40], reduces to 60
```

Because `map`/`filter` return new arrays, their results can be chained directly — a common,
readable pattern for a multi-step transformation, though very long chains can become harder to
debug than an equivalent loop with named intermediate variables.

## Common Mistakes

- Using `forEach` when the goal is actually to build a new array — `map`/`filter`/`reduce` express
  that intent directly and return something usable, where `forEach` returns nothing.
- Calling a mutating method (like `.sort()`) on an array another part of the program still expects
  to be unchanged.
- Forgetting `reduce`'s initial value (the second argument) — omitting it uses the array's first
  element as the initial accumulator, which can produce a different (and sometimes wrong) result
  than intended, especially on an empty array, where it throws.

## Next

Continue to [objects.md](objects.md) for JavaScript's other core data structure.
