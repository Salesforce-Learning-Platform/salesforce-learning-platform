# 🔄 Async Iterators and `for await…of`

## Sequences That Arrive Over Time

[iterators-and-generators.md](../additional-javascript-topics/iterators-and-generators.md) covered
the synchronous protocol: an iterable hands out a value on every `next()` call, and `for...of` drives
it. Many real sequences are not available instantly — pages of an API, chunks of a download, lines of
a log, messages from a socket. The **async iteration protocol** is the same idea with one change:
`next()` returns a **promise**, so each step can wait.

## 🧩 The Protocol

```
ASYNC ITERABLE   an object with a [Symbol.asyncIterator]() method
ASYNC ITERATOR   an object with next() that returns a PROMISE of { value, done }
for await (const x of asyncIterable) { ... }   drives it, awaiting each step
```

`for await…of` is valid only where `await` is: inside an `async` function or at the top level of a
module. MDN notes that it also accepts ordinary (sync) iterables and awaits each value they produce.

## ⚙️ Async Generators: The Easy Way to Write One

An `async function*` is a generator whose body may both `await` and `yield`. Calling it returns an
`AsyncGenerator` — an async iterable. Here is a paginated API turned into a flat stream of items
(`delay(ms)` is the timer helper from
[promise-combinators-in-depth.md](promise-combinators-in-depth.md)):

```js
const pages = [["a", "b"], ["c"], []];
const fetchPage = async (page) => {
  await delay(10);                          // pretend network latency
  return pages[page - 1] ?? [];
};

async function* fetchItems() {
  let page = 1;
  try {
    while (true) {
      const items = await fetchPage(page);
      if (items.length === 0) return;       // an empty page ends the sequence
      yield* items;                          // hand out each item of this page
      page++;
    }
  } finally {
    console.log("(generator cleanup ran)");
  }
}

const collected = [];
for await (const item of fetchItems()) {
  collected.push(item);
}
console.log(collected);   // [ 'a', 'b', 'c' ]
```

The consumer sees one flat sequence and never touches page numbers; the generator fetches the next
page only when the loop asks for more items.

### Early Exit Cleans Up

When a `for await` loop ends early — with `break`, `return`, or an error — the iterator's `return()`
method is called, which runs the generator's `finally` block. That makes `finally` the right place to
close files, release locks, or cancel requests:

```js
const first = [];
for await (const item of fetchItems()) {
  first.push(item);
  if (item === "b") break;                  // stop early
}
// logs "(generator cleanup ran)" even though the sequence was not finished
console.log(first);   // [ 'a', 'b' ]
```

## 🐢 It Is Sequential by Design

Each iteration finishes before the next begins. That is exactly right for pagination and streams, and
exactly wrong for independent tasks that could run in parallel:

```js
async function* slowSequence() {
  for (const n of [1, 2, 3]) {
    await delay(50);
    yield n;
  }
}

for await (const n of slowSequence()) { /* about 150 ms in total */ }

// Three promises that are created together run in parallel — about 50 ms in total:
for await (const value of [delay(50, 1), delay(50, 2), delay(50, 3)]) { /* … */ }
```

For work that is independent, start the tasks together and combine them with
[`Promise.all` or a concurrency pool](promise-combinators-in-depth.md); reserve `for await` for data
that is genuinely produced one step at a time.

## 🌊 Backpressure for Free

The consumer *pulls*: the generator runs only until its next `yield`, then pauses until the loop asks
again. A slow consumer therefore slows the producer rather than letting values pile up:

```js
const log = [];

async function* produce() {
  for (let i = 1; i <= 3; i++) {
    log.push(`produce ${i}`);
    yield i;
  }
}

for await (const value of produce()) {
  log.push(`consume ${value}`);
  await delay(5);                           // a slow consumer
}

console.log(log);
// [ 'produce 1', 'consume 1', 'produce 2', 'consume 2', 'produce 3', 'consume 3' ]
```

## 🛠️ Writing the Protocol by Hand

Any object can be an async iterable — useful when wrapping a callback-style API:

```js
const ticker = {
  from: 1,
  to: 3,
  [Symbol.asyncIterator]() {
    let n = this.from;
    const to = this.to;
    return {
      async next() {
        await delay(5);
        return n <= to ? { value: n++, done: false } : { value: undefined, done: true };
      },
    };
  },
};

const seen = [];
for await (const n of ticker) seen.push(n);
console.log(seen);   // [ 1, 2, 3 ]
```

An async generator is almost always shorter, but the manual form shows there is no magic.

## 📥 Collecting Everything: `Array.fromAsync`

MDN lists `Array.fromAsync()` as Baseline widely available since January 2024. It awaits an async
(or sync) iterable and returns a promise of the array:

```js
console.log(await Array.fromAsync(slowSequence()));        // [ 1, 2, 3 ]
console.log(await Array.fromAsync([delay(5, "x"), "y"]));  // [ 'x', 'y' ]
```

## 🌍 Streaming a Response Body

MDN documents that a `ReadableStream` — such as `response.body` from `fetch` — can be consumed with
`for await…of`, receiving each chunk as it arrives instead of waiting for the whole download:

```js
const response = await fetch(url);
const decoder = new TextDecoder();

for await (const chunk of response.body) {
  console.log(decoder.decode(chunk));       // alpha, then beta, then gamma
}
```

(Here a test server wrote three pieces 30 ms apart and each arrived as its own chunk. Chunk
boundaries depend on the network, so never assume one chunk equals one logical message.) The chunks
are `Uint8Array`s — see
[typed-arrays-and-binary-data.md](../built-in-objects-and-collections/typed-arrays-and-binary-data.md).
Node.js streams and many libraries expose the same interface.

## ⚠️ Errors and Cancellation

A thrown error inside an async generator surfaces in the consumer's `try`/`catch` around the loop:

```js
async function* flaky() {
  yield 1;
  throw new Error("stream broke");
}

try {
  for await (const value of flaky()) console.log("got", value);   // got 1
} catch (error) {
  console.log(error.message);               // stream broke
}
```

Combine async generators with [`AbortSignal`](cancellation-with-abortcontroller.md) by checking the
signal each turn:

```js
async function* ticks(signal) {
  let i = 0;
  while (true) {
    signal.throwIfAborted();
    await delay(20);
    yield ++i;
  }
}

const controller = new AbortController();
setTimeout(() => controller.abort(), 35);

const seen = [];
try {
  for await (const n of ticks(controller.signal)) seen.push(n);
} catch (error) {
  console.log(error.name, seen);            // AbortError [ 1, 2 ]
}
```

## 🎤 Interview Angle

- **"What is the difference between `for…of` and `for await…of`?"** `for…of` drives a sync iterator;
  `for await…of` drives an async iterator whose `next()` returns promises, awaiting each step.
- **"What is an async generator?"** An `async function*` — a generator that can `await` and `yield`,
  returning an async iterable.
- **"When would you use `for await` instead of `Promise.all`?"** When values are produced
  sequentially over time (pages, streams); use `Promise.all` for independent tasks you want in
  parallel.
- **"What happens to a generator when the loop `break`s?"** Its `return()` runs, executing `finally`.

## Common Mistakes

- **Using `for await` for independent work** and serializing what could run in parallel.
- **Assuming one stream chunk equals one message or one character** — chunks split anywhere.
- **Putting cleanup anywhere but `finally`**, so it is skipped on `break`.
- **Using `for await` outside an async function** (outside a module's top level), which is a
  `SyntaxError`.
- **Forgetting to handle errors thrown mid-stream.**

## ➡️ Next

Continue to [timers-and-scheduling.md](timers-and-scheduling.md) to see the tools for deciding *when*
code runs: timers, animation frames, microtasks, and idle time.
