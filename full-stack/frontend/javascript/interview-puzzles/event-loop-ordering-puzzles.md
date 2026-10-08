# ⏱️ Event Loop Ordering Puzzles

## 🧩 What These Puzzles Test

"What order does this print?" is the most common asynchronous question in JavaScript interviews, and it has
a precise answer. After the synchronous code finishes, the runtime works through two kinds of queued work in
a fixed pattern:

1. **Run all synchronous code** on the call stack until it is empty.
2. **Drain the microtask queue completely** — promise callbacks (`then`, `catch`, `finally`), code after
   `await`, and `queueMicrotask` callbacks. Microtasks added *while draining* run in the same pass.
3. **Run one macrotask** (a timer callback, an I/O callback, a UI event), then go back to step 2.

If you can run that loop in your head, you can answer any ordering puzzle. The thirteen puzzles below
practise it, ending with two Node.js-specific ones.

Every answer was **produced by running the code** (three times, to confirm the order is stable). The
browser-compatible puzzles were also run in a real browser, with identical order.

## 🛠️ How to Use This File

1. **Cover the answer** and write down two lists as you read: the *microtask queue* and the *timer
   queue*. Print the synchronous logs immediately.
2. **When the synchronous code ends**, empty the microtask list in order (adding anything new at the end).
3. **Then take the next timer**, and repeat.

The concept files behind these puzzles are
[call-stack.md](../event-loop/call-stack.md),
[microtasks-and-macrotasks.md](../event-loop/microtasks-and-macrotasks.md),
[promises.md](../asynchronous-programming-and-modules/promises.md),
[async-await.md](../asynchronous-programming-and-modules/async-await.md), and
[timers-and-scheduling.md](../advanced-async-patterns/timers-and-scheduling.md).

## 🧪 The Puzzles

### Puzzle 1 — Sync, microtasks, then timers

*Difficulty: ⭐ Warm-up*

```js
console.log("1 sync");

setTimeout(() => console.log("2 timeout"), 0);

Promise.resolve().then(() => console.log("3 promise"));

queueMicrotask(() => console.log("4 queueMicrotask"));

console.log("5 sync");
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
1 sync
5 sync
3 promise
4 queueMicrotask
2 timeout
```

Trace the loop:

1. Synchronous code runs top to bottom: it logs `1 sync`, registers the timer, queues two microtasks, and logs
   `5 sync`.
2. The stack is empty, so the microtask queue drains in the order the jobs were added: `3 promise`, then
   `4 queueMicrotask` (a promise callback and a `queueMicrotask` callback share one queue).
3. Only then does the loop take the timer callback: `2 timeout`.

`setTimeout(…, 0)` does not mean "right now"; it means "as a macrotask, after all pending microtasks." See
[microtasks-and-macrotasks.md](../event-loop/microtasks-and-macrotasks.md).

</details>

### Puzzle 2 — The executor runs immediately

*Difficulty: ⭐ Warm-up*

```js
console.log("A");

new Promise((resolve) => {
  console.log("B (executor)");
  resolve("C");
  console.log("D (after resolve)");
}).then((value) => console.log(value));

console.log("E");
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
A
B (executor)
D (after resolve)
E
C
```

The function passed to `new Promise` (the executor) runs **synchronously**, right when the promise is
created. Calling `resolve` does not stop it: `D` still prints. What is asynchronous is the `.then`
callback, which is queued as a microtask and runs after the synchronous code finishes, so `C` comes last.

Rule: creating a promise is synchronous; *reacting* to it is always asynchronous, even when it is already
resolved. See [promises.md](../asynchronous-programming-and-modules/promises.md).

</details>

### Puzzle 3 — Two interleaved chains

*Difficulty: ⭐⭐⭐ Tricky*

```js
async function f() {
  console.log("f1");
  await null;
  console.log("f2");
  await null;
  console.log("f3");
}

f();

Promise.resolve()
  .then(() => console.log("p1"))
  .then(() => console.log("p2"))
  .then(() => console.log("p3"));

console.log("sync");
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
f1
sync
f2
p1
f3
p2
p3
```

Think of each `await` or `.then` as "put the continuation at the *back* of the microtask queue," and trace the
queue:

| Step | Event | Queue afterwards |
|------|-------|------------------|
| 1 | `f()` runs synchronously to the first `await`: logs `f1`, queues the continuation | `[f-continuation-1]` |
| 2 | `Promise.resolve().then(p1)` queues `p1` | `[f-cont-1, p1]` |
| 3 | `sync` is logged; the stack is empty | `[f-cont-1, p1]` |
| 4 | Run `f-cont-1`: logs `f2`, reaches the second `await`, queues `f-cont-2` | `[p1, f-cont-2]` |
| 5 | Run `p1`: logs `p1`, which resolves the next promise and queues `p2` | `[f-cont-2, p2]` |
| 6 | Run `f-cont-2`: logs `f3` | `[p2]` |
| 7 | Run `p2`, which queues `p3`, then `p3` | `[]` |

The two chains **take turns**, one step each. Awaiting a native promise or plain value costs exactly one
microtask turn in modern engines — V8's write-up on faster async functions describes the optimization that
took `await` from three turns down to one. See
[async-await.md](../asynchronous-programming-and-modules/async-await.md).

</details>

### Puzzle 4 — What happens after an await

*Difficulty: ⭐⭐ Interview standard*

```js
async function a() {
  console.log("a start");
  await b();
  console.log("a end");
}

async function b() {
  console.log("b");
}

console.log("script start");
a();
Promise.resolve().then(() => console.log("then"));
console.log("script end");
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
script start
a start
b
script end
a end
then
```

Calling `a()` runs it synchronously until its first `await`, so `a start` appears at once. The call to `b()`
inside the `await` expression *also* runs synchronously (logging `b`) and returns an already-resolved
promise. `await` then suspends `a`, queueing its continuation as a microtask.

That continuation was queued **before** the `.then` callback, so after `script end`, the queue runs `a end`
first, then `then`. A common mistake is to think `await` pushes everything after it into a timer: it does
not; it only moves the rest of the function to the microtask queue.

</details>

### Puzzle 5 — Returning a promise costs extra turns

*Difficulty: ⭐⭐⭐ Tricky*

```js
Promise.resolve()
  .then(() => {
    console.log("A1");
    return Promise.resolve("x");
  })
  .then(() => console.log("A2"));

Promise.resolve()
  .then(() => console.log("B1"))
  .then(() => console.log("B2"))
  .then(() => console.log("B3"))
  .then(() => console.log("B4"));
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
A1
B1
B2
B3
A2
B4
```

Both chains start with one microtask each, so `A1` and `B1` run first. But `A1`'s callback returns a
**promise**, not a plain value. Resolving a promise with another promise (a "thenable") is not instant: the
specification schedules an extra job to subscribe to the inner promise, and the inner promise's own
settlement needs another turn. The extra latency is why chain A's second step (`A2`) runs only after `B3`,
while chain B needed one turn per step. V8's article on fast async functions describes the same
`PromiseResolveThenableJob` mechanism when explaining `await`.

The practical advice is not to rely on such fine-grained ordering between independent chains. If the order
matters, make one chain wait for the other explicitly (`await`, `Promise.all`).

</details>

### Puzzle 6 — Microtasks keep going

*Difficulty: ⭐⭐ Interview standard*

```js
setTimeout(() => console.log("timeout"), 0);

Promise.resolve().then(() => {
  console.log("m1");
  queueMicrotask(() => console.log("m2 (queued from m1)"));
});

queueMicrotask(() => console.log("m3"));
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
m1
m3
m2 (queued from m1)
timeout
```

The microtask queue is drained **completely** — including jobs added while it is draining — before any
timer can run. `m1` and `m3` were queued during the synchronous phase, so they run first, in order. `m1`
queues `m2` while running; `m2` goes to the back of the same queue, so it runs after `m3` but *still before*
the timer.

This is also why an endless chain of microtasks can freeze a page or process: the loop never gets to the
macrotask stage. See [microtasks-and-macrotasks.md](../event-loop/microtasks-and-macrotasks.md) ("A Practical
Consequence: Starving the Macrotask Queue").

</details>

### Puzzle 7 — Microtasks between timers

*Difficulty: ⭐⭐ Interview standard*

```js
setTimeout(() => {
  console.log("T1");
  Promise.resolve().then(() => console.log("T1 microtask"));
}, 0);

setTimeout(() => console.log("T2"), 0);
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
T1
T1 microtask
T2
```

Two timers with the same delay run in the order they were registered, but they are separate macrotasks. After
each macrotask the loop empties the microtask queue, so the promise callback created inside `T1` runs
**before** `T2`. This was checked in both Node.js 24 and a real browser.

So the loop is: macrotask → all microtasks → macrotask → all microtasks.

</details>

### Puzzle 8 — Timer delays decide the order

*Difficulty: ⭐ Warm-up*

```js
setTimeout(() => console.log("100 ms"), 100);
setTimeout(() => console.log("10 ms"), 10);
setTimeout(() => console.log("0 ms"), 0);
console.log("sync");
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
sync
0 ms
10 ms
100 ms
```

Timers fire in order of their **due time**, not their registration order. All three are registered
immediately, `sync` is logged, and then the timers fire as their delays expire: `0 ms`, `10 ms`, `100 ms`.
Remember that a delay is a *minimum*; a busy call stack delays every timer. Timers with identical delays keep
registration order (as in the previous puzzle), so do not build logic on tiny differences such as `0` versus
`1` ms. See
[timers-and-scheduling.md](../advanced-async-patterns/timers-and-scheduling.md).

</details>

### Puzzle 9 — An async function never throws synchronously

*Difficulty: ⭐⭐ Interview standard*

```js
async function risky() {
  throw new Error("boom");
}

try {
  const promise = risky();
  console.log("no synchronous error");
  promise.catch((e) => console.log("caught later:", e.message));
} catch {
  console.log("caught synchronously");
}

console.log("end of script");
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
no synchronous error
end of script
caught later: boom
```

An `async` function converts any exception thrown inside it into a **rejected promise**. Calling it never
throws; the `try`/`catch` around the call is therefore useless. The error arrives later, through
`.catch` — or through `await` inside a `try`/`catch`:

```js
try {
  await risky();
} catch (e) { /* handled here */ }
```

If no handler is attached to a rejected promise, it becomes an *unhandled rejection*, which Node.js treats as
a fatal error by default. See
[handling-unhandled-rejections.md](../advanced-async-patterns/handling-unhandled-rejections.md) and
[try-catch-finally.md](../error-handling-and-debugging/try-catch-finally.md).

</details>

### Puzzle 10 — How a promise chain flows

*Difficulty: ⭐⭐ Interview standard*

```js
Promise.resolve(1)
  .then((value) => {
    console.log("then 1:", value);
    throw new Error("fail");
  })
  .then(() => console.log("skipped"))
  .catch((error) => {
    console.log("catch:", error.message);
    return "recovered";
  })
  .then((value) => console.log("then 2:", value))
  .finally(() => console.log("finally"));
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
then 1: 1
catch: fail
then 2: recovered
finally
```

Each `.then` returns a new promise, and the chain follows two tracks:

- A value returned from a callback keeps the chain on the **fulfilled** track.
- A thrown error switches to the **rejected** track, and every `.then(onFulfilled)` is skipped until a
  `.catch` handles it.

Here the error thrown in `then 1` skips the next `.then`, and `catch` handles it; because the `catch` callback
*returns* a value, the chain is fulfilled again and `then 2` receives `"recovered"`. `finally` runs at the
end either way. See [promises.md](../asynchronous-programming-and-modules/promises.md).

</details>

### Puzzle 11 — race versus all

*Difficulty: ⭐⭐ Interview standard*

```js
const wait = (ms, value) =>
  new Promise((resolve) => setTimeout(() => resolve(value), ms));

Promise.race([wait(30, "slow"), wait(10, "fast")]).then((value) =>
  console.log("race:", value)
);

Promise.all([wait(30, "a"), wait(10, "b")]).then((values) =>
  console.log("all:", values)
);
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
race: fast
all: [ 'a', 'b' ]
```

`Promise.race` settles with the **first** promise to settle: after 10 ms the `"fast"` promise wins, and
`race: fast` prints first. `Promise.all` waits for **every** promise (30 ms here) and then fulfills with an
array in the **original order** of the inputs — `['a', 'b']` — not in the order they finished. See
[promise-combinators-in-depth.md](../advanced-async-patterns/promise-combinators-in-depth.md).

</details>

### Puzzle 12 — Sequential versus parallel awaits

*Difficulty: ⭐⭐ Interview standard*

```js
const wait = (ms, label) =>
  new Promise((resolve) =>
    setTimeout(() => {
      console.log("done", label);
      resolve(label);
    }, ms)
  );

(async () => {
  await wait(20, "A");
  await wait(10, "B");
  console.log("sequential finished");

  await Promise.all([wait(20, "C"), wait(10, "D")]);
  console.log("parallel finished");
})();
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
done A
done B
sequential finished
done D
done C
parallel finished
```

Each `await` pauses the async function until its promise settles. In the first half the timers are started
**one after another**: `B`'s timer is not even created until `A` is done, so the waits add up (about 30 ms)
and the order is `A`, `B`.

In the second half, `Promise.all` receives promises that have **already started**, so both timers run
at once; the shorter one (`D`, 10 ms) finishes first, `C` follows at 20 ms, and the total is about 20 ms. If
two operations do not depend on each other, start them together and await them together. See
[async-await.md](../asynchronous-programming-and-modules/async-await.md).

</details>

### Puzzle 13 — Node.js only: nextTick

*Difficulty: ⭐⭐⭐ Tricky*

```js
Promise.resolve().then(() => console.log("promise"));
process.nextTick(() => console.log("nextTick"));
console.log("sync");
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
sync
nextTick
promise
```

`process.nextTick` is a Node.js-specific queue (browsers do not have it) that runs before the promise
microtask queue — **in CommonJS**. Node.js's documentation states the difference directly: in CommonJS
modules, `nextTick` callbacks run before `queueMicrotask` and promise callbacks; in ES modules the
order is reversed, because module evaluation itself already happens inside the microtask queue, so
promise callbacks go first. The first two outputs show this.

The third variation shows the Node.js phases. Inside an I/O callback, `setImmediate` is guaranteed to run
before a `setTimeout(…, 0)` — the Node.js event-loop guide says so explicitly. Called from the *main*
script, the order of those two is **not** guaranteed: the guide says it depends on the performance of
the process, so never rely on it. And `nextTick` and promise callbacks run right after the current callback,
before either. The Node.js documentation describes `process.nextTick` as legacy and recommends
`queueMicrotask` for new code. See [timers-and-scheduling.md](../advanced-async-patterns/timers-and-scheduling.md)
("Node.js Extras") and [javascript-runtimes-browser-vs-nodejs.md](../how-javascript-runs/javascript-runtimes-browser-vs-nodejs.md).

**Variation — The same code as an ES module (`.mjs`)**

```js
Promise.resolve().then(() => console.log("promise"));
process.nextTick(() => console.log("nextTick"));
console.log("sync");
```

```text
sync
promise
nextTick
```

**Variation — Inside an I/O callback**

```js
const fs = require("fs");

fs.readFile(__filename, () => {
  setTimeout(() => console.log("timeout"), 0);
  setImmediate(() => console.log("immediate"));
  process.nextTick(() => console.log("nextTick"));
  Promise.resolve().then(() => console.log("promise"));
});
```

```text
nextTick
promise
immediate
timeout
```

</details>

## 🧭 Patterns to Remember

| Pattern in the question | Rule |
|-------------------------|------|
| Synchronous `console.log` | Prints first, in order |
| `Promise.then`, code after `await`, `queueMicrotask` | Microtask queue, drained fully after sync code |
| `setTimeout`, I/O callbacks, UI events | Macrotasks: one at a time, microtasks drained between them |
| `new Promise(executor)` | The executor is synchronous; the reaction is not |
| `async` function call | Runs synchronously until its first `await`; never throws synchronously |
| `await value` | One microtask turn (for a native promise or plain value) |
| Returning a promise from `then` | Costs extra turns |
| Equal timer delays | Registration order |
| `process.nextTick` | Node.js only: before promise callbacks in CommonJS, after in ES modules |

## 🎤 Interview Angle

- **Say the loop out loud**: "synchronous code first, then all microtasks, then the next macrotask, then
  microtasks again." Interviewers listen for that model.
- **Draw the queues.** Write the microtask queue as a list and update it as you go — it prevents the usual
  slips and shows how you think.
- **Know what *not* to promise.** Fine-grained ordering between independent promise chains, or
  `setTimeout(0)` versus `setImmediate` in the main module, is not something to depend on in real code.
- **Connect it to practice**: long synchronous work blocks timers and rendering; endless microtasks starve
  them; and the cure for both is breaking work into slices — see
  [timers-and-scheduling.md](../advanced-async-patterns/timers-and-scheduling.md).

## Common Mistakes

- **Thinking `setTimeout(fn, 0)` runs immediately** or before promise callbacks.
- **Thinking `await` blocks the whole program** — it only pauses the async function.
- **Forgetting that the Promise executor is synchronous.**
- **Expecting `try`/`catch` to catch the error from an `async` function you did not `await`.**
- **Awaiting independent operations one after another** when they could run in parallel.
- **Relying on `process.nextTick` ordering** in code that may run as both CommonJS and ES modules.

## ➡️ Next

Continue to [interview-topic-map.md](interview-topic-map.md) for a study map that connects common interview
topic areas to the files in this platform where each one is taught.
