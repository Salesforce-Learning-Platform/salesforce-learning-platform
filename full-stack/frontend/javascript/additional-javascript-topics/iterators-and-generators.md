# Iterators and Generators

## What Makes Something Iterable

[loops.md](../conditionals-and-loops/loops.md) introduced `for...of` as working on arrays,
strings, Maps, and Sets. What they all actually share is implementing the **iterator protocol**: an
object with a `[Symbol.iterator]()` method (see [symbols.md](symbols.md)) that returns an
**iterator** — an object with a `next()` method, which returns `{ value, done }` on each call.

```js
const numbers = [10, 20, 30];
const iterator = numbers[Symbol.iterator]();

iterator.next(); // { value: 10, done: false }
iterator.next(); // { value: 20, done: false }
iterator.next(); // { value: 30, done: false }
iterator.next(); // { value: undefined, done: true }
```

`for...of` is really just repeatedly calling `next()` until `done` is `true` — understanding this
is what explains *why* `for...of` works uniformly across such different data structures: they all
implement the exact same underlying protocol.

## Making Your Own Object Iterable

```js
const range = {
  from: 1,
  to: 3,
  [Symbol.iterator]() {
    let current = this.from;
    const last = this.to;
    return {
      next() {
        return current <= last
          ? { value: current++, done: false }
          : { value: undefined, done: true };
      },
    };
  },
};

for (const num of range) console.log(num); // 1, 2, 3
```

This manual approach works but is verbose — **generator functions** exist specifically to make
writing this pattern dramatically simpler.

## Generator Functions

```js
function* rangeGenerator(from, to) {
  for (let i = from; i <= to; i++) {
    yield i;
  }
}

for (const num of rangeGenerator(1, 3)) console.log(num); // 1, 2, 3
```

A **generator function** (declared with `function*`) automatically implements the entire iterator
protocol for you. Calling it doesn't run its body immediately — it returns a generator object; each
call to `.next()` (including the ones `for...of` performs automatically) resumes execution until
the next `yield`, pausing there and returning that value.

## Lazy Evaluation — A Genuine Practical Benefit

```js
function* infiniteCounter() {
  let n = 0;
  while (true) {
    yield n++;
  }
}

const counter = infiniteCounter();
counter.next().value; // 0
counter.next().value;  // 1
// never actually generates an infinite array — only computes what's requested
```

Because a generator only computes the next value when actually asked for one, it can represent
conceptually infinite or very large sequences without ever needing to materialize them all in
memory at once — something an ordinary array-returning function fundamentally cannot do.

## Common Mistakes

- Manually implementing the iterator protocol (as shown above) when a generator function would
  express the exact same logic far more concisely.
- Forgetting that calling a generator function doesn't run its body — it only starts executing,
  pausing at each `yield`, once `.next()` is actually called.
- Trying to convert an infinite generator into an array directly (`[...infiniteCounter()]`), which
  would run forever, since spreading tries to exhaust the iterator completely.

## Next

Continue to [regular-expressions.md](regular-expressions.md) for pattern matching in strings — an
unrelated but equally practical topic.
