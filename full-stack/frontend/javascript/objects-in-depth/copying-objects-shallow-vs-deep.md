# 📑 Copying Objects: Shallow vs. Deep

## Assignment Copies the Reference, Not the Object

Objects and arrays are held by **reference**. Assigning one to another variable creates a second
name for the *same* object — not a copy:

```js
const a = { n: 1 };
const b = a;
b.n = 2;

console.log(a.n, a === b);   // 2 true — one object, two names
```

Making an independent copy is a separate, deliberate step, and "independent" comes in two strengths.

## 🪞 Shallow Copies

A **shallow copy** creates a new top-level object but copies each property *value* as-is. If a value
is itself an object, the copy and the original end up pointing at the *same* nested object:

```js
const original = { name: "Ada", address: { city: "London" }, tags: ["x"] };

const copy = { ...original };          // spread — the usual shallow copy
copy.name = "Grace";                   // top-level change: independent
copy.address.city = "Paris";           // nested change: SHARED
copy.tags.push("y");                   // nested change: SHARED

console.log(original.name);            // Ada
console.log(original.address.city);    // Paris   ← the original changed too
console.log(original.tags);            // [ 'x', 'y' ]
console.log(copy.address === original.address);   // true — the very same object
```

Other shallow-copy tools behave the same way: `Object.assign({}, original)`, and for arrays
`[...arr]`, `arr.slice()`, and `Array.from(arr)`. This is the mistake behind most "I copied it but
it still changed" bugs — see the nested-update pattern in
[pure-functions-and-immutability.md](../functional-javascript/pure-functions-and-immutability.md)
for how to update nested data without a full deep copy.

### What a Shallow Copy Also Loses

Spread and `Object.assign` copy only an object's own **enumerable** properties and produce a plain
object, so they drop non-enumerable properties, the prototype, and accessors' *definitions*:

```js
class User {
  constructor(name) { this.name = name; }
  greet() { return "hi " + this.name; }
}

const u = new User("Ada");
const c = { ...u };

console.log(typeof u.greet, typeof c.greet);   // function undefined
console.log(c instanceof User);                // false — it is now a plain object
```

(Non-enumerable properties are skipped, as covered in
[property-descriptors-and-getters-setters.md](property-descriptors-and-getters-setters.md), and a
getter is evaluated and copied as a plain value.)

## 🧬 Deep Copies

A **deep copy** duplicates every nested level, so the copy shares nothing with the original.

### `structuredClone()` — the built-in answer

```js
const original = {
  when: new Date(0),
  tags: new Set(["a"]),
  lookup: new Map([["k", 1]]),
  nested: { deep: [1, 2] },
};
original.self = original;                 // a circular reference

const copy = structuredClone(original);

console.log(copy.when instanceof Date);          // true  — Dates stay Dates
console.log(copy.tags instanceof Set);           // true  — Sets and Maps survive
console.log(copy.lookup.get("k"));               // 1
console.log(copy.nested.deep !== original.nested.deep);   // true — truly independent
console.log(copy.self === copy);                 // true  — the cycle is reproduced
console.log(copy.self === original);             // false — and does not point back to the original
```

`structuredClone` is MDN-listed as widely available across browsers since March 2022 and is built on
the *structured clone algorithm*. Per MDN, that algorithm handles circular references and supports
`Date`, `Map`, `Set`, `RegExp`, typed arrays, `Error` types, and plain objects and arrays — but has
firm limits:

```js
structuredClone({ fn() {} });
// DataCloneError: fn() {} could not be cloned.   — functions cannot be cloned
```

It also does **not** preserve everything about an object. Per MDN, the prototype chain (class
identity), property descriptors and accessors, and class private elements are not carried over:

```js
class Point {
  #secret = 1;
  constructor(x) { this.x = x; }
  norm() { return this.x; }
  get double() { return this.x * 2; }
}

const p = new Point(3);
const c = structuredClone(p);

console.log(c);                                   // { x: 3 }
console.log(c instanceof Point, typeof c.norm);   // false undefined
```

An own getter is likewise flattened into a plain data property holding the value at clone time. The
clone is a plain object with the *data*, not an instance of the class.

### `JSON.parse(JSON.stringify(x))` — a common trick, with sharp edges

This works only for JSON-safe data, and silently damages everything else:

```js
const original = {
  when: new Date(0),
  skipped: undefined,
  method() {},
  notANumber: NaN,
  tags: new Set(["a"]),
  lookup: new Map([["k", 1]]),
  list: [undefined, () => 1],
};

console.log(JSON.parse(JSON.stringify(original)));
// {
//   when: '1970-01-01T00:00:00.000Z',   ← a string, not a Date
//   notANumber: null,                   ← NaN became null
//   tags: {},                           ← Set became an empty object
//   lookup: {},                         ← Map became an empty object
//   list: [ null, null ]                ← undefined and functions became null
// }                                      ← `skipped` and `method` vanished entirely
```

A circular reference makes it throw `TypeError: Converting circular structure to JSON`, and a
`BigInt` throws `TypeError: Do not know how to serialize a BigInt` (details in
[json-serialization.md](json-serialization.md)). Prefer `structuredClone` unless you specifically
want JSON semantics.

### Libraries and hand-written clones

When you must preserve class instances or other special types, write a copy method on the class, or
use a utility library's deep-clone function; both let you decide how each type is handled.

## 📊 Which Copy for Which Job

| Need | Use |
|------|-----|
| Independent top-level object, nested data may be shared | Spread / `Object.assign` / `slice` |
| Fully independent plain data (dates, maps, sets, cycles included) | `structuredClone` |
| JSON-only data and you want JSON semantics | `JSON.parse(JSON.stringify(x))` |
| Class instances, functions, or custom types | A custom copy method or a library |
| Updating one nested field without cloning everything | Copy only along the changed path |

Deep copies cost time and memory proportional to the size of the data, so avoid them in hot paths
and prefer targeted updates that share unchanged parts.

## 🎤 Interview Angle

- **"What is the difference between a shallow and a deep copy?"** A shallow copy duplicates only
  the top level — nested objects are shared. A deep copy duplicates every level.
- **"How do you deep clone an object?"** `structuredClone`; the JSON round-trip for JSON-safe data
  only; or a library or custom function for special types.
- **"What breaks with `JSON.parse(JSON.stringify(...))`?"** Dates become strings; `undefined`,
  functions, and symbols are dropped (or become `null` in arrays); `NaN` and `Infinity` become `null`;
  `Map` and `Set` become `{}`; cycles and `BigInt` throw.
- **"Does `{ ...obj }` copy methods on a class instance?"** No — prototype methods are not own
  properties, and the result is a plain object.

## Common Mistakes

- **Treating a shallow copy as independent** and mutating nested data.
- **Using the JSON trick on data containing dates, maps, or sets.**
- **Expecting `structuredClone` to keep class methods or accessors.**
- **Trying to `structuredClone` an object containing a function**, which throws.
- **Deep-copying large structures on every update** instead of copying only what changes.

## ➡️ Next

Continue to [json-serialization.md](json-serialization.md) for a closer look at the JSON format
itself and the options `JSON.stringify` and `JSON.parse` give you.
