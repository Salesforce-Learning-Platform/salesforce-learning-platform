# Loops

## `for` — When You Know How Many Iterations

```js
for (let i = 0; i < 5; i++) {
  console.log(i);
}
```

The classic three-part loop: initialization (`let i = 0`), condition (checked before each
iteration), and an afterthought (run after each iteration). All three parts are individually
optional, though omitting them is unusual outside specific edge cases.

## `while` and `do...while`

```js
while (condition) {
  // runs zero or more times — condition checked before each iteration
}

do {
  // runs at least once — condition checked after each iteration
} while (condition);
```

`while` is the right choice when the number of iterations isn't known in advance, only a
condition to keep repeating on. `do...while`'s defining difference is guaranteeing at least one
execution, since it checks the condition only after the first run.

## `for...of` — Iterating Values

```js
const fruits = ["apple", "banana", "cherry"];
for (const fruit of fruits) {
  console.log(fruit); // "apple", "banana", "cherry"
}
```

`for...of` iterates over the actual **values** of an iterable (arrays, strings, Maps, Sets) — the
standard, modern way to loop over an array's contents directly.

## `for...in` — Iterating Keys

```js
const user = { name: "Ada", age: 36 };
for (const key in user) {
  console.log(key, user[key]); // "name" "Ada", "age" 36
}
```

`for...in` iterates over an object's enumerable property **keys** — appropriate for plain objects,
but a poor fit for arrays, where it iterates over string index keys ("0", "1", "2"...) rather than
the values themselves, and can also pick up inherited enumerable properties unexpectedly.

| | Iterates | Best for |
|---|---|---|
| `for...of` | Values | Arrays, strings, Maps, Sets — anything iterable |
| `for...in` | Keys (property names) | Plain objects |

## `break` and `continue`

```js
for (let i = 0; i < 10; i++) {
  if (i === 5) break;     // exits the loop entirely
  if (i % 2 === 0) continue; // skips to the next iteration
  console.log(i);
}
```

`break` exits the loop immediately; `continue` skips the rest of the current iteration and moves to
the next one. In nested loops, both apply only to the innermost enclosing loop by default (labeled
statements can target an outer loop, though this is uncommon in typical code).

## Common Mistakes

- Using `for...in` to iterate over an array, picking up string index keys instead of actual values,
  and potentially inherited properties.
- Writing an infinite loop by forgetting to update the condition variable inside a `while` loop's
  body.
- Confusing `break` (stop the loop entirely) with `continue` (skip just this iteration) — using one
  where the other was intended silently changes the loop's behavior rather than raising an error.

## Module Summary

Across this module: `if`/`else if`/`else` and the ternary operator handle branching, with the
ternary best reserved for simple value-selection rather than complex nested logic (see
[conditional-statements.md](conditional-statements.md)); `switch` compares one value against exact
matches using strict equality, with fall-through as real, deliberate (or accidentally forgotten)
behavior (see [switch-statements.md](switch-statements.md)); and choosing the correct loop —
`for` for known iteration counts, `while`/`do...while` for condition-driven repetition, `for...of`
for values, `for...in` for object keys — is what keeps iteration code both correct and readable.
