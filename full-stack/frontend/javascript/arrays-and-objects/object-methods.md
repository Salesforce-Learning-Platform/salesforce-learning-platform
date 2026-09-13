# Object Methods

## `Object.keys()`, `Object.values()`, `Object.entries()`

```js
const user = { name: "Ada", age: 36 };

Object.keys(user);    // ["name", "age"]
Object.values(user);   // ["Ada", 36]
Object.entries(user);   // [["name", "Ada"], ["age", 36]]
```

These three convert an object's properties into arrays, which unlocks every array method covered
in [array-methods.md](array-methods.md) for working with object data — a very common and powerful
pattern:

```js
Object.entries(user)
  .map(([key, value]) => `${key}: ${value}`)
  .join(", ");
// "name: Ada, age: 36"
```

## The Spread Operator for Objects

```js
const base = { role: "user", active: true };
const admin = { ...base, role: "admin" }; // { role: "admin", active: true }
```

Spreading an object into a new object literal copies its properties; a property repeated after the
spread **overrides** the spread value — this ordering matters and is the standard pattern for
creating an updated copy of an object without mutating the original (essential for React state
updates, covered in its own domain).

## Merging Multiple Objects

```js
const merged = { ...defaults, ...userSettings }; // userSettings values win on conflict
```

When multiple objects are spread together, later spreads override earlier ones for any shared
keys — the same override rule as above, just applied across more than one source object.

## `Object.freeze()`

```js
const config = Object.freeze({ apiUrl: "https://api.example.com" });
config.apiUrl = "changed"; // silently fails (or throws in strict mode) — frozen
```

`Object.freeze()` prevents adding, removing, or changing an object's properties — a genuine,
runtime-enforced immutability, as opposed to `const`, which (as covered in
[variables.md](../introduction-to-javascript/variables.md)) only prevents reassigning the variable
binding itself, not the object's contents.

## Common Mistakes

- Mutating an object directly (`user.role = "admin"`) when an immutable update
  (`{ ...user, role: "admin" }`) was actually required — this matters enormously for frameworks
  like React that rely on detecting a new object reference to know something changed.
- Getting spread order backwards, accidentally letting default values override intentionally
  customized ones.
- Assuming `const` alone makes an object immutable, forgetting it only locks the variable binding —
  `Object.freeze()` is the tool for genuine content immutability.

## Next

Continue to [destructuring.md](destructuring.md) for a more concise way to extract values from
both arrays and objects.
