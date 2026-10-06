# 🪢 WeakMap, WeakSet, and WeakRef

## Holding Something Without Keeping It Alive

A `Map` keeps every key — and its value — alive for as long as the `Map` exists. That is exactly
wrong when you only want to *attach* information to objects that someone else owns. If the owner is
finished with an object, a regular `Map` still holds a reference to it, so the garbage collector can
never reclaim it: a memory leak. **Weak collections** solve this by holding their keys **weakly**: a
key that is otherwise unreachable can be garbage-collected, taking its entry with it. (See the How
JavaScript Runs module, later in this section, for how garbage collection works.)

## 🗝️ WeakMap

```js
const wm = new WeakMap();
const user = {};

wm.set(user, "meta");

console.log(wm.get(user));   // meta
console.log(wm.has(user));   // true
console.log(wm.delete(user)); // true
console.log(wm.has(user));   // false
```

Per MDN, a `WeakMap`'s keys must be **objects** or **non-registered symbols**. Anything else throws:

```js
new WeakMap().set(1, "x");
// TypeError: Invalid value used as weak map key

new WeakMap().set("k", "x");
// TypeError: Invalid value used as weak map key

const wm2 = new WeakMap();
const sym = Symbol("k");           // a non-registered symbol: allowed
wm2.set(sym, 1);
wm2.set(Symbol.for("reg"), 2);     // a registered symbol: TypeError
```

### What It Deliberately Cannot Do

A `WeakMap` has no `size`, no `clear()`, and cannot be iterated:

```js
console.log(wm.size);                    // undefined
console.log(typeof wm[Symbol.iterator]); // undefined
```

MDN explains why: listing the keys would make program behavior depend on *when* the garbage
collector happened to run. If you need to enumerate entries, use a `Map`.

### What It Is For

MDN lists the typical uses: associating **private or auxiliary data** with an object without adding
a property to it, attaching **metadata to DOM elements**, and **caching** results keyed by an object.
The cache case, building on [memoization.md](../functional-javascript/memoization.md):

```js
const cache = new WeakMap();
let computed = 0;

function expensive(obj) {
  if (cache.has(obj)) return cache.get(obj);
  computed++;
  const result = Object.keys(obj).length;   // stand-in for real work
  cache.set(obj, result);
  return result;
}

const config = { a: 1, b: 2 };
console.log(expensive(config), expensive(config), computed);   // 2 2 1
```

When `config` is no longer referenced anywhere, its cache entry becomes collectable too — no manual
cleanup, no unbounded growth.

## 🔖 WeakSet

A `WeakSet` is the same idea for membership: a set of objects held weakly, with only `add`, `has`,
and `delete`. A handy use is "have I already processed this object?":

```js
const seen = new WeakSet();

function once(obj) {
  if (seen.has(obj)) return false;
  seen.add(obj);
  return true;
}

const a = {};
console.log(once(a), once(a), once({}));   // true false true
```

## 👁️ WeakRef and FinalizationRegistry

A **`WeakRef`** holds a weak reference to a single object; `deref()` returns the object, or
`undefined` if it has been collected. A **`FinalizationRegistry`** lets you register a callback to
run after an object is collected.

```js
// Run with:  node --expose-gc demo.mjs   (an ES module, so top-level await works;
//            the flag exposes global.gc for demonstration purposes only)
let obj = { name: "temp" };
const ref = new WeakRef(obj);
const registry = new FinalizationRegistry((held) => console.log("finalized:", held));
registry.register(obj, "temp-object");

console.log("before:", ref.deref()?.name);   // before: temp

obj = null;                                   // drop the only strong reference
await new Promise((r) => setTimeout(r, 0));   // let the current job finish
global.gc();                                  // force a collection (Node only, with the flag)
await new Promise((r) => setTimeout(r, 10));

console.log("after gc:", ref.deref());        // after gc: undefined
// also logged by the registry:               finalized: temp-object
```

This is an illustration, **not** a pattern to rely on. MDN strongly recommends avoiding `WeakRef`
where possible, for three reasons:

- **Garbage collection is not deterministic.** When — or whether — an object is collected depends on
  the engine and can differ between engines and versions.
- **Reclamation is only observable between event-loop turns.** An object stays alive for the rest
  of the current job, which is why the example waits a tick before collecting.
- **Callbacks may never run.** Logic that *requires* a finalizer to execute is fragile.

Reach for `WeakMap` and `WeakSet` first; they cover almost every legitimate need without the
non-determinism.

## 🆚 Map vs. WeakMap

| | `Map` | `WeakMap` |
|---|-------|-----------|
| Key types | Anything | Objects and non-registered symbols |
| Holds keys | Strongly (prevents collection) | Weakly (allows collection) |
| Iterable, `size`, `clear` | Yes | No |
| Use when | You own the data and need to enumerate it | You are attaching data to objects you don't own |

## 🎤 Interview Angle

- **"What is the difference between `Map` and `WeakMap`?"** A `Map` keeps its keys alive and can be
  iterated; a `WeakMap` holds object keys weakly, so an unreferenced key can be collected, and it is
  not iterable and has no `size`.
- **"Why can't you iterate a `WeakMap`?"** Because the contents would depend on when garbage
  collection runs, which would make behavior non-deterministic.
- **"How would you avoid a memory leak when caching data per object?"** Key the cache with a
  `WeakMap`, so entries disappear with their objects.
- **"When would you use `WeakRef`?"** Rarely; MDN advises avoiding it because garbage collection
  behavior is not guaranteed.

## Common Mistakes

- **Using a `Map` to attach metadata to objects you don't own**, leaking them for the life of the
  `Map`.
- **Trying to use a string or number as a `WeakMap` key.**
- **Expecting to inspect a `WeakMap`** (iterate it or read its size).
- **Writing logic that depends on a finalization callback or `deref()` returning `undefined` at a
  particular moment.**

## ➡️ Next

Continue to [strings-and-unicode.md](strings-and-unicode.md) to look at the built-in collection you
use most — text — and the Unicode details that make `length` surprising.
