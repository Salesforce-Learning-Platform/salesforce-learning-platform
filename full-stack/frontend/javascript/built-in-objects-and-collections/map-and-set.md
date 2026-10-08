# 🗺️ Map and Set

## Collections Built for Their Job

Plain objects and arrays can imitate a dictionary and a unique list, but each was designed for
something else — [objects](../arrays-and-objects/objects.md) for records with known fields, and
[arrays](../arrays-and-objects/arrays.md) for ordered lists. **`Map`** and **`Set`** are the
purpose-built alternatives: a `Map` is a key-to-value dictionary, and a `Set` is a collection of
unique values. Both remember insertion order, both are directly iterable, and both are designed for
fast lookups and frequent additions and removals.

## 🗂️ Map: A Dictionary With Any Kind of Key

```js
const m = new Map();
m.set("a", 1).set(2, "two").set(true, "yes");   // set() returns the map, so calls chain

const key = { id: 1 };
m.set(key, "obj");                                // an object can be a key

console.log(m.size);          // 4
console.log(m.get("a"));      // 1
console.log(m.get(key));      // obj
console.log(m.get({ id: 1 })); // undefined — a different object, even with identical contents
console.log(m.has(true));     // true
console.log(m.delete(2));     // true — returns whether something was removed
console.log(m.size);          // 3
```

Iterating gives `[key, value]` pairs in insertion order:

```js
for (const [k, v] of m) {
  console.log(typeof k, v);
}
// string 1
// boolean yes
// object obj
```

`m.keys()`, `m.values()`, and `m.entries()` return iterators, and `[...m]` converts the whole map to
an array of pairs. Converting to and from plain objects:

```js
console.log(Object.fromEntries(new Map([["x", 1], ["y", 2]])));   // { x: 1, y: 2 }
console.log(new Map(Object.entries({ p: 1, q: 2 })));             // Map(2) { 'p' => 1, 'q' => 2 }
```

### Key Equality: SameValueZero

MDN states that `Map` (and `Set`) compare keys with **SameValueZero**: like `===`, except that `NaN`
equals `NaN`, and `+0` and `-0` are the same. Objects compare by *reference*:

```js
const m = new Map();
m.set(NaN, "nan");
m.set(0, "zero");

console.log(m.get(NaN));            // nan  — works, even though NaN === NaN is false
console.log(m.get(-0));             // zero — -0 and +0 are the same key
console.log(NaN === NaN);           // false
```

### Why Not Just Use an Object?

MDN's comparison highlights what a `Map` gives you:

| | `Map` | Plain object |
|---|-------|--------------|
| Key types | **Any** value (objects, functions, primitives) | Strings and symbols only |
| Key order | Insertion order, guaranteed | Less straightforward |
| Size | `map.size` | Count the keys yourself |
| Iteration | Directly iterable | Not iterable by default |
| Inherited keys | None | Has a prototype chain |
| Frequent add/remove | Designed for it | Not optimized for it |
| JSON | No native support | `JSON.stringify` / `JSON.parse` |

The "inherited keys" row is a source of real bugs. A word-frequency counter built on an object
trips on a word that happens to be a name on `Object.prototype`:

```js
const counts = {};
for (const word of ["constructor", "a"]) {
  counts[word] = (counts[word] || 0) + 1;
}
console.log(counts.constructor);   // function Object() { [native code] }1   ← a string, not a count!

const mapCounts = new Map();
for (const word of ["constructor", "a", "a"]) {
  mapCounts.set(word, (mapCounts.get(word) ?? 0) + 1);
}
console.log(mapCounts);            // Map(2) { 'constructor' => 1, 'a' => 2 }
```

`counts["constructor"]` found the inherited `Object` constructor, and `|| 0` never ran. A `Map`
starts empty — no inherited keys to collide with.

### Gotchas

```js
const m = new Map();
m["a"] = 1;                         // sets an ordinary PROPERTY on the map object…
console.log(m.size, m.get("a"));    // 0 undefined — …not an entry
console.log(m.a);                   // 1
```

Always use `set()` and `get()`. And a `Map` does not serialize to JSON:

```js
const m = new Map([["a", 1]]);
console.log(JSON.stringify(m));                      // {}
console.log(JSON.stringify([...m]));                 // [["a",1]]
console.log(JSON.stringify(Object.fromEntries(m)));  // {"a":1}
```

(See [json-serialization.md](../objects-in-depth/json-serialization.md) for the full picture.)

### Insertion Order, Precisely

Updating an existing key keeps its position; deleting and re-adding moves it to the end:

```js
const m = new Map([["a", 1], ["b", 2], ["c", 3]]);
m.set("a", 99);
console.log([...m.keys()]);   // [ 'a', 'b', 'c' ]
m.delete("a");
m.set("a", 1);
console.log([...m.keys()]);   // [ 'b', 'c', 'a' ]
```

That behavior is what makes a `Map` a natural basis for an LRU cache — see the bounded cache in
[memoization.md](../functional-javascript/memoization.md).

### A Typical Use: Grouping

```js
const people = [
  { name: "Ada", team: "x" },
  { name: "Bob", team: "y" },
  { name: "Cy",  team: "x" },
];

const byTeam = new Map();
for (const p of people) {
  if (!byTeam.has(p.team)) byTeam.set(p.team, []);
  byTeam.get(p.team).push(p.name);
}

console.log(byTeam);   // Map(2) { 'x' => [ 'Ada', 'Cy' ], 'y' => [ 'Bob' ] }
```

## 🔵 Set: A Collection of Unique Values

```js
console.log([...new Set([1, 2, 2, 3, 1])]);   // [ 1, 2, 3 ]  — the classic de-duplication

const s = new Set();
console.log(s.add(1) === s);   // true  — add() returns the set, so calls chain
console.log(s.has(1));         // true
console.log(s.delete(1));      // true
console.log(s.size);           // 0
```

Uniqueness uses the same SameValueZero rule, and objects are compared by reference:

```js
console.log(new Set([NaN, NaN, 0, -0]).size);       // 2 — one NaN, one zero
console.log(new Set([{ a: 1 }, { a: 1 }]).size);    // 2 — two different objects
console.log(new Set("hello").size);                  // 4 — "l" appears once
```

### Membership: Why `has` Beats `includes`

MDN notes that `Set.prototype.has` runs in sublinear time on average — far faster than scanning an
array with `includes`, which must examine elements one by one (the O(1) vs. O(n) difference from
[time-complexity.md](../../../data-structures-and-algorithms/time-and-space-complexity/time-complexity.md)).
A single measured run, looking up the *last* of 100,000 numbers 1,000 times:

```
array.includes × 1000:  ~15 ms
set.has        × 1000:  ~0.03 ms
```

(Timings vary by machine; the gap is what matters.) The Hashing module of the Data Structures and
Algorithms section explains the data structure that makes this possible.

### Set Operations

```js
const a = new Set([1, 2, 3]);
const b = new Set([2, 3, 4]);

console.log(a.union(b));                  // Set(4) { 1, 2, 3, 4 }
console.log(a.intersection(b));           // Set(2) { 2, 3 }
console.log(a.difference(b));             // Set(1) { 1 }
console.log(a.symmetricDifference(b));    // Set(2) { 1, 4 }
console.log(a.isSubsetOf(new Set([1, 2, 3, 4])));   // true
console.log(a.isSupersetOf(new Set([1])));          // true
console.log(a.isDisjointFrom(new Set([9])));        // true
```

These composition methods are comparatively recent — MDN flags their support as more limited than
the rest of `Set`, so check its compatibility table for your target environments. The long-standing
equivalents work everywhere:

```js
console.log(new Set([...a, ...b]));                        // union
console.log(new Set([...a].filter((x) => b.has(x))));      // intersection
console.log(new Set([...a].filter((x) => !b.has(x))));     // difference
```

## 🧭 Choosing

| Need | Use |
|------|-----|
| A record with known field names | Object |
| A lookup table with arbitrary or changing keys, or non-string keys | `Map` |
| An ordered list that may repeat | Array |
| Unique values or fast "have I seen this?" checks | `Set` |
| Keys that are objects you don't want to keep alive | `WeakMap` (next file) |

## 🎤 Interview Angle

- **"Map vs. Object?"** `Map` accepts any key type, preserves insertion order, has `size`, is
  iterable, and has no inherited keys; objects are best for fixed-shape records and JSON.
- **"How do you remove duplicates from an array?"** `[...new Set(array)]`.
- **"How does `Set` decide two values are the same?"** SameValueZero — `NaN` equals `NaN`, objects
  by reference.
- **"Why is `set.has(x)` faster than `array.includes(x)`?"** Average sublinear (hash-table) lookup
  versus a linear scan.

## Common Mistakes

- **Using bracket notation on a `Map`** (`map[key] = value`) instead of `set()`.
- **Counting words or ids in a plain object** and colliding with inherited names like
  `constructor`.
- **Expecting two equal-looking objects to be the same `Map` key or `Set` member.**
- **Calling `JSON.stringify` on a `Map` or `Set`** and getting `{}`.
- **Using an array and `includes` for large membership checks.**

## ➡️ Next

Continue to [weakmap-weakset-and-weakref.md](weakmap-weakset-and-weakref.md) to see the variants that
hold their keys without keeping them alive.
