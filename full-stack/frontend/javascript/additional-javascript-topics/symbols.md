# Symbols

## A Distinct Primitive Type

`Symbol` is one of the seven primitive types introduced in
[data-types.md](../introduction-to-javascript/data-types.md), with one defining property: **every
Symbol is guaranteed unique**, even two created with the identical description.

```js
const a = Symbol("id");
const b = Symbol("id");
a === b; // false — different Symbols, despite the same description
```

The string passed to `Symbol()` is just a description for debugging purposes (shown in console
output) — it plays no role in equality or identity at all.

## The Main Use Case: Collision-Free Object Keys

```js
const id = Symbol("id");
const user = {
  name: "Ada",
  [id]: 12345, // a Symbol-keyed property
};

user[id]; // 12345
Object.keys(user); // ["name"] — Symbol keys are NOT included
```

Because a Symbol is guaranteed unique, using one as an object key guarantees it will never
accidentally collide with a string key added by unrelated code (a genuine, if rare, real-world
concern in a large codebase or when extending an object you don't fully control). As a side
effect, Symbol-keyed properties are excluded from `Object.keys()`, `for...in`, and `JSON.stringify()`
by default — a form of "soft" internal/non-enumerable-by-default property, without being fully
private the way `#` class fields are.

## Well-Known Symbols

JavaScript itself uses Symbols internally to let objects customize built-in behavior — most
notably `Symbol.iterator`, which is exactly how an object declares itself iterable for `for...of`,
covered in depth in
[iterators-and-generators.md](iterators-and-generators.md).

## Common Mistakes

- Expecting `Symbol("id") === Symbol("id")` to be `true` because the descriptions match — Symbols
  are unique regardless of description.
- Assuming a Symbol-keyed property is genuinely private/secure — it's hidden from *casual*
  enumeration (`Object.keys`, `for...in`), but still discoverable via
  `Object.getOwnPropertySymbols()` for code that specifically looks for it.
- Reaching for Symbols as a general-purpose solution when a plain string key would work fine — the
  unique-key guarantee only matters when key collisions are a genuine, realistic risk.

## Next

Continue to [iterators-and-generators.md](iterators-and-generators.md) to see one of JavaScript's
own well-known Symbols in action.
