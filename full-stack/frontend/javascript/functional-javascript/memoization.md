# 🧠 Memoization

## Remembering Results Instead of Recomputing Them

**Memoization** caches a function's return value, keyed by the arguments it was called with, so
that a repeat call with the same arguments returns instantly instead of recomputing. It builds
directly on two earlier ideas: a closure holds the cache
([higher-order-functions.md](higher-order-functions.md)), and the technique is only *correct* for
[pure functions](pure-functions-and-immutability.md) — if the same arguments could legitimately
produce different results, a cached value would be wrong.

## 🧮 A General `memoize`

```js
function memoize(fn) {
  const cache = new Map();
  return function (...args) {
    const key = JSON.stringify(args);          // build a cache key from the arguments
    if (cache.has(key)) {
      return cache.get(key);                   // cache hit: no recomputation
    }
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}
```

`memoize` takes a function and returns a wrapped one — a [higher-order function](higher-order-functions.md)
— using `apply` so `this` and the arguments pass through
([call-apply-and-bind.md](call-apply-and-bind.md)).

## ⚡ The Classic Demonstration: Fibonacci

The naive recursive Fibonacci recomputes the same sub-problems over and over. Counting the calls
shows how badly:

```js
let calls = 0;
const slowFib = (n) => {
  calls++;
  return n < 2 ? n : slowFib(n - 1) + slowFib(n - 2);
};

console.log(slowFib(30), calls);   // 832040 2692537
```

Computing the 30th Fibonacci number takes about 2.7 million calls. With memoization each distinct
`n` is computed once:

```js
calls = 0;
const fastFib = memoize((n) => {
  calls++;
  return n < 2 ? n : fastFib(n - 1) + fastFib(n - 2);   // recurse through the memoized version
});

console.log(fastFib(30), calls);   // 832040 31
```

Thirty-one calls — one per value of `n` from 0 to 30. Note that the recursion must go through the
*memoized* function (`fastFib`), not the original, or the cache is never consulted for the
sub-problems.

## ⚠️ The Hard Part: Cache Keys

`JSON.stringify(args)` is a convenient key, but it has real limitations:

```js
console.log(JSON.stringify([undefined]), JSON.stringify([null]));
// [null] [null]   — undefined and null produce the SAME key (a collision)

console.log(JSON.stringify([{ a: 1, b: 2 }]) === JSON.stringify([{ b: 2, a: 1 }]));
// false           — equal objects with different key order get different keys (a missed hit)

console.log(JSON.stringify([() => 1]), JSON.stringify([new Date(0)]));
// [null] ["1970-01-01T00:00:00.000Z"]   — functions vanish into null; dates become strings

JSON.stringify([1n]);
// TypeError: Do not know how to serialize a BigInt
```

Collisions (`undefined` vs. `null`, functions vs. `null`) return *wrong* cached answers, which is
worse than a miss. For functions with a single primitive argument, use that argument itself as the
`Map` key and skip serialization entirely. For object arguments, key by identity (a `Map` or
`WeakMap` keyed by the object) rather than by serialized contents.

## 📏 Keeping the Cache From Growing Forever

An unbounded cache is a memory leak with good intentions: every distinct argument adds an entry
that is never freed. Two standard remedies:

- **Limit the size** and evict old entries. A `Map` iterates in insertion order, which makes a small
  least-recently-used (LRU) cache straightforward:

```js
function memoizeLRU(fn, limit = 100) {
  const cache = new Map();
  return (arg) => {
    if (cache.has(arg)) {
      const value = cache.get(arg);
      cache.delete(arg);              // re-insert so this key becomes the most recent
      cache.set(arg, value);
      return value;
    }
    const result = fn(arg);
    cache.set(arg, result);
    if (cache.size > limit) {
      cache.delete(cache.keys().next().value);   // evict the oldest (least recently used) entry
    }
    return result;
  };
}

const computed = [];
const square = memoizeLRU((n) => { computed.push(n); return n * n; }, 2);

square(1); square(2); square(1); square(3); square(2);
console.log(computed);   // [ 1, 2, 3, 2 ]
```

The trace: `1` and `2` are computed; the second `square(1)` is a hit (and makes `1` the most
recent); `square(3)` pushes the cache over its limit of 2 and evicts `2`; the final `square(2)`
therefore has to be recomputed.

- **Hold object keys weakly.** A `WeakMap` lets cached entries disappear when the key object is
  garbage-collected — covered in the Built-in Objects and Collections module, later in this section.

## 🚫 When Not to Memoize

- **Impure functions** — anything depending on time, randomness, I/O, or outside state; the cache
  would serve stale answers.
- **Cheap functions** — a cache lookup can cost more than the computation it saves.
- **Arguments that rarely repeat** — the cache never hits and only consumes memory.
- **Memory-constrained code paths** — without a size limit, caches grow with the number of distinct
  inputs.

Measure first: memoization is an optimization, and optimizations belong where a profiler shows a
real cost.

## 🔗 The Same Idea in React

React's `useMemo`, `useCallback`, and `React.memo` apply the same principle — reuse the previous
result when the inputs have not changed — with a dependency array in place of an argument-based
key; see [memoization.md](../../react/performance-optimization-in-react/memoization.md) in the React
performance module.

## 🎤 Interview Angle

- **"What is memoization?"** Caching a function's results by its arguments so repeated calls with
  the same arguments return the stored result.
- **"Implement `memoize`."** A closure holding a `Map`, building a key from the arguments, returning
  the cached value on a hit and storing the computed one on a miss.
- **"When does memoization break?"** With impure functions, with keys that collide or fail to
  serialize, and with unbounded cache growth.
- **"How does it change Fibonacci's cost?"** From exponential (about 2.7 million calls for `n = 30`)
  to linear (31 calls).

## Common Mistakes

- **Memoizing an impure function** and serving stale or wrong results.
- **Recursing through the original function** instead of the memoized one, so sub-problems are never
  cached.
- **Using `JSON.stringify` keys carelessly** — collisions on `undefined`/`null`, order-sensitive
  objects, unserializable values.
- **Never bounding the cache**, creating a slow memory leak.
- **Memoizing everything** instead of measuring where the cost actually is.

## ➡️ Next

Continue to [iife-and-the-module-pattern.md](iife-and-the-module-pattern.md) for the closure-based
pattern that kept private state private before classes and modules existed.
