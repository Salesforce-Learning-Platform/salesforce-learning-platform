# Arrays

## Creating and Accessing Arrays

```js
const fruits = ["apple", "banana", "cherry"];

fruits[0];       // "apple"
fruits.length;    // 3
fruits[fruits.length - 1]; // "cherry" — last element
fruits.at(-1);      // "cherry" — modern, more readable equivalent
```

Arrays are zero-indexed; `.at(-1)` (a more recent addition) reaches the last element directly
without the `length - 1` arithmetic.

## Basic Mutation

```js
fruits.push("date");     // adds to the end
fruits.pop();              // removes from the end, returns it
fruits.unshift("apricot"); // adds to the beginning
fruits.shift();             // removes from the beginning, returns it
```

`push`/`pop` operate at the end (efficient); `unshift`/`shift` operate at the beginning (less
efficient, since every remaining element must shift index). All four **mutate** the original array
in place.

## Checking for a Value

```js
fruits.includes("banana"); // true
fruits.indexOf("banana");   // 1 (or -1 if not found)
```

## Arrays Are Objects — Compared by Reference

```js
const a = [1, 2, 3];
const b = [1, 2, 3];
const c = a;

a === b; // false — different array objects, even with identical contents
a === c; // true  — c refers to the SAME array object as a
```

As introduced conceptually in
[data-types.md](../introduction-to-javascript/data-types.md), arrays (being objects) are compared
by reference, not by contents. This also means mutating an array through one variable affects
every other variable referencing that same array:

```js
c.push(4);
console.log(a); // [1, 2, 3, 4] — a and c are the same array
```

## Copying an Array

```js
const copy = [...fruits];        // spread syntax
const copy2 = fruits.slice();     // slice() with no arguments
```

Both produce a genuinely new array with the same top-level contents — a **shallow copy**. Nested
arrays or objects inside it are still shared by reference between the original and the copy.

## Common Mistakes

- Assuming `arrayA = arrayB` copies the array, when it actually just makes both variables point to
  the same array — mutating one affects the other.
- Forgetting that a "copy" made with spread or `slice()` is shallow — nested objects/arrays within
  it are still shared references, not independently copied.
- Confusing `indexOf` (returns a position, or `-1`) with `includes` (returns a boolean) when only a
  yes/no answer was actually needed.

## Next

Continue to [array-methods.md](array-methods.md) for the higher-level methods used constantly in
real code.
