# 🧰 Modern Array and Object Methods

## Newer Built-Ins That Replace Old Workarounds

[array-methods.md](../arrays-and-objects/array-methods.md) covers the classic array toolkit and warns
about mutating methods like `sort` and `reverse`. Over the last few years the language added methods
that fix long-standing awkward spots: reading from the end of an array, finding the *last* match,
sorting without mutating, checking object ownership safely, and grouping. MDN lists each of these as
Baseline *widely available* (the dates are in the table below), so they are safe in current browsers and
Node.js. All results shown were run in Node.js 24 and a real browser.

| Method | Replaces | Widely available since (per MDN) |
|--------|----------|:--------------------------------:|
| `array.at(i)` | `array[array.length - 1]` | March 2022 |
| `array.findLast()` / `findLastIndex()` | Reversing, then `find` | August 2022 |
| `toSorted()`, `toReversed()`, `toSpliced()`, `with()` | Copying, then `sort`/`reverse`/`splice`/assigning | July 2023 |
| `Object.hasOwn(obj, key)` | `obj.hasOwnProperty(key)` | March 2022 |
| `Object.groupBy()` / `Map.groupBy()` | Hand-written `reduce` grouping | March 2024 |

## 🎯 `at()`: Relative Indexing

```js
const a = [5, 12, 8, 130, 44];

console.log(a.at(0), a.at(-1), a.at(-2));   // 5 44 130
console.log(a[a.length - 1]);                // 44   — the old way to get the last element
console.log(a.at(10), a.at(-10));            // undefined undefined — out of range is not an error
console.log("str".at(-1));                   // r    — strings have it too
```

A negative index counts from the end (it is `index + length`). The bracket form `a[-1]` does **not** do
this — it looks for a property literally named `"-1"` and returns `undefined`.

## 🔎 `findLast()` and `findLastIndex()`

Search from the end instead of the start:

```js
const a = [1, 2, 3, 4, 5, 6];

console.log(a.findLast((n) => n % 2 === 1));        // 5   — the last odd number
console.log(a.findLastIndex((n) => n % 2 === 1));   // 4   — its index
console.log(a.findLast((n) => n > 100));            // undefined — no match
console.log(a.findLastIndex((n) => n > 100));       // -1        — no match
```

Typical uses: the most recent matching log entry, the last item satisfying a condition, "latest
version" lookups — without `[...array].reverse().find(...)` and the copy that costs.

## 🔁 Change-Array-by-Copy: Non-Mutating `sort`, `reverse`, `splice`, and Assignment

`sort`, `reverse`, and `splice` change the array in place — a recurring source of bugs when other code
holds the same array, and a problem for immutable-update styles (see
[pure-functions-and-immutability.md](../functional-javascript/pure-functions-and-immutability.md)). Each
has a copying twin that returns a **new** array and leaves the original untouched:

| Mutating | Copying equivalent |
|----------|--------------------|
| `arr.sort(fn)` | `arr.toSorted(fn)` |
| `arr.reverse()` | `arr.toReversed()` |
| `arr.splice(start, deleteCount, ...items)` | `arr.toSpliced(start, deleteCount, ...items)` |
| `arr[i] = value` | `arr.with(i, value)` |

```js
const original = [3, 1, 2];

console.log(original.toSorted());               // [ 1, 2, 3 ]
console.log(original.toReversed());             // [ 2, 1, 3 ]
console.log(original.toSpliced(1, 1, "x", "y")); // [ 3, 'x', 'y', 2 ]
console.log(original.with(0, 99));              // [ 99, 1, 2 ]
console.log(original);                           // [ 3, 1, 2 ] — never changed
```

The distinction is visible in what each returns:

```js
const a = [3, 1, 2];
console.log(a.sort() === a);          // true  — sort returns the SAME array, now mutated
const b = [3, 1, 2];
console.log(b.toSorted() !== b);      // true  — toSorted returns a NEW array
```

Two details inherited from their originals: with no comparator, `toSorted` compares values **as strings**
(`[1, 10, 21, 2].toSorted()` gives `[1, 10, 2, 21]`), so pass `(a, b) => a - b` for numbers; and
`with()` accepts negative indexes but throws a `RangeError` for an index outside the array:

```js
console.log([1, 2, 3].with(-1, 99));   // [ 1, 2, 99 ]
[1, 2, 3].with(10, 1);                 // RangeError: Invalid index : 10
```

For a React-style state update, `setItems((items) => items.toSpliced(i, 1))` removes an item without
mutating — replacing `items.filter((_, index) => index !== i)` or a copy-then-`splice` dance.

## 🔐 `Object.hasOwn()`: The Safe Ownership Check

`obj.hasOwnProperty("key")` asks "is this property on the object itself, not inherited?" — but it is a
method *on the object*, so it can be missing or replaced. MDN shows the failing case, and a second one
follows from the same cause:

```js
const bare = Object.create(null);              // an object with NO prototype (a "dictionary")
bare.prop = "exists";

console.log(Object.hasOwn(bare, "prop"));      // true
bare.hasOwnProperty("prop");                    // TypeError: bare.hasOwnProperty is not a function

const shadowed = { hasOwnProperty() { return false; }, x: 1 };
console.log(shadowed.hasOwnProperty("x"));      // false — the object lies
console.log(Object.hasOwn(shadowed, "x"));      // true

console.log(Object.hasOwn({ a: 1 }, "toString"), "toString" in { a: 1 });   // false true
```

The last line shows the other distinction worth remembering: `in` also finds *inherited* properties,
`Object.hasOwn` only own ones. This matters for objects used as lookup tables
(compare the `"constructor"` word-count bug in [map-and-set.md](../built-in-objects-and-collections/map-and-set.md)).
Use `Object.hasOwn(obj, key)` everywhere you would have written `obj.hasOwnProperty(key)`.

## 🗂️ `Object.groupBy()` and `Map.groupBy()`

Grouping items by a computed key used to need a `reduce` with an accumulator. Now:

```js
const orders = [
  { id: 1, status: "paid", total: 30 },
  { id: 2, status: "open", total: 10 },
  { id: 3, status: "paid", total: 55 },
];

const byStatus = Object.groupBy(orders, (order) => order.status);

console.log(byStatus);
// [Object: null prototype] {
//   paid: [ { id: 1, status: 'paid', total: 30 }, { id: 3, status: 'paid', total: 55 } ],
//   open: [ { id: 2, status: 'open', total: 10 } ]
// }
console.log(Object.getPrototypeOf(byStatus), Object.keys(byStatus));   // null [ 'paid', 'open' ]
```

Per MDN, the result is a **null-prototype object** with one array per group — so keys like `"toString"` or
`"constructor"` cannot collide with inherited properties (the same reason `Object.hasOwn` exists). Because
it is a plain object, **group keys are coerced to strings**:

```js
const g = Object.groupBy([1, 2, 3], (n) => n % 2);
console.log(g, Object.keys(g), typeof Object.keys(g)[0]);
// [Object: null prototype] { '0': [ 2 ], '1': [ 1, 3 ] } [ '0', '1' ] string
```

When keys should keep their type (numbers, objects), use **`Map.groupBy`**, which returns a `Map`:

```js
const buckets = Map.groupBy([1, 2, 3, 4, 5, 6, 7], (n) => (n % 3 === 0 ? "fizz" : n % 2 === 0 ? 2 : "other"));
console.log(buckets);
// Map(3) { 'other' => [ 1, 5, 7 ], 2 => [ 2, 4 ], 'fizz' => [ 3, 6 ] }   — the number key 2 stays a number

const bySize = Map.groupBy(["a", "bb", "cc", "d"], (s) => s.length);
console.log(bySize.get(2), typeof [...bySize.keys()][0]);   // [ 'bb', 'cc' ] number
```

Pick `Object.groupBy` for string-like keys you will read by name (`byStatus.paid`), and `Map.groupBy` for
anything else ([map-and-set.md](../built-in-objects-and-collections/map-and-set.md) explains why a `Map`
suits arbitrary keys).

## 🛠️ Older Targets

These are *methods*, not syntax, so a transpiler cannot add them — a [polyfill](../how-javascript-runs/transpilers-polyfills-and-browser-support.md)
(for example from core-js) must, if your targets lack them. Widely-available status means that is rarely
needed for current browsers, but check your Browserslist targets. You can always feature-detect:
`if (typeof Array.prototype.toSorted !== "function") { … }`.

## 🎤 Interview Angle

- **"How do you get the last element of an array?"** `array.at(-1)` (or `array[array.length - 1]`).
- **"How do you sort without mutating?"** `array.toSorted()` — or, in older code, `[...array].sort()`.
- **"Why prefer `Object.hasOwn` to `hasOwnProperty`?"** It works on null-prototype objects and cannot be
  overridden by the object itself.
- **"What does `Object.groupBy` return, and why is its prototype `null`?"** An object mapping group names
  to arrays; the null prototype prevents key collisions with inherited properties.
- **"`Object.groupBy` vs. `Map.groupBy`?"** The object coerces keys to strings; the `Map` keeps any key type.

## Common Mistakes

- **Using `a[-1]`** instead of `a.at(-1)`.
- **Calling `toSorted()` without a comparator on numbers.**
- **Expecting `with()` to extend the array** — an out-of-range index throws.
- **Assuming `Object.groupBy` keys keep their type.**
- **Using `in` to test ownership**, which also matches inherited properties.
- **Forgetting that `sort()` mutates** when `toSorted()` was intended.

## ➡️ Next

Continue to [top-level-await-and-import-attributes.md](top-level-await-and-import-attributes.md) for how
modules can now wait for asynchronous setup and import non-JavaScript files such as JSON.
