# 🎚️ Debouncing and Throttling

## Taming Events That Fire Too Often

Some events fire in torrents: `input` on every keystroke, `scroll` and `resize` dozens of times per
second, `mousemove` constantly. Running expensive code on each one — a network request, a layout
calculation — wastes work and can make the page janky. **Debouncing** and **throttling** are two
standard ways to limit how often a handler actually runs. They are built from the timers in
[timers-and-scheduling.md](../advanced-async-patterns/timers-and-scheduling.md), closures
([closures.md](../functions/closures.md)), and the `this`/argument forwarding from
[call-apply-and-bind.md](../functional-javascript/call-apply-and-bind.md) — so they make a good
exercise in all three, and a very common interview question.

```
DEBOUNCE   wait until the calls STOP, then run once.
           "Run this after the user has paused for 300 ms."

THROTTLE   run at most once per interval, however many calls arrive.
           "Run this at most every 100 ms while the user keeps scrolling."
```

## ⏳ Debounce

Every call resets a timer; only when the timer is allowed to expire does the function run — with the
arguments of the **last** call:

```js
function debounce(fn, wait) {
  let timer;
  function debounced(...args) {
    clearTimeout(timer);                              // a new call cancels the pending one
    timer = setTimeout(() => fn.apply(this, args), wait);
  }
  debounced.cancel = () => clearTimeout(timer);       // lets callers drop a pending run
  return debounced;
}
```

Ten calls 10 ms apart, debounced by 50 ms, produce a single run once the calls stop. (`delay(ms)` is the
timer helper from [promise-combinators-in-depth.md](../advanced-async-patterns/promise-combinators-in-depth.md),
and `elapsed()` stands for "milliseconds since the script started".)

```js
const log = [];
const handler = debounce((n) => log.push(`call(${n}) @${elapsed()}ms`), 50);

for (let i = 1; i <= 10; i++) { handler(i); await delay(10); }
await delay(120);

console.log(log);   // [ 'call(10) @150ms' ]  — one run, with the last call's argument, 50 ms after the last call
```

The classic use is a search box: without debouncing, typing "hello" sends five requests; with it,
one:

```js
const requests = [];
const search = debounce((query) => requests.push(query), 100);

for (const query of ["h", "he", "hel", "hell", "hello"]) {
  search(query);
  await delay(30);                                    // keystrokes 30 ms apart
}
await delay(150);

console.log(requests);   // [ 'hello' ]
```

### Leading-Edge Debounce

Sometimes you want the **first** call to run immediately and the rest of the burst ignored — for
example a "Save" button that should respond at once but not fire twice:

```js
function debounceLeading(fn, wait) {
  let timer;
  return function (...args) {
    if (!timer) fn.apply(this, args);                 // first call of a burst runs immediately
    clearTimeout(timer);
    timer = setTimeout(() => { timer = undefined; }, wait);   // the burst "ends" after a quiet period
  };
}
```

With the same ten-call burst, this version runs `call(1)` at 0 ms and nothing else.

### Cancelling

`debounced.cancel()` discards a pending run, which matters when the thing the call was for has gone
away (a component unmounted, a form closed). Forgetting this is a common source of "state update on an
unmounted component" bugs.

## 🚰 Throttle

A throttled function runs immediately, then at most once per `wait` milliseconds. A good throttle also
schedules one **trailing** call, so the final state is not lost:

```js
function throttle(fn, wait) {
  let last = 0;
  let timer;
  let pendingArgs;

  function throttled(...args) {
    const now = Date.now();
    const remaining = wait - (now - last);
    if (remaining <= 0) {                             // enough time has passed: run now
      clearTimeout(timer);
      timer = undefined;
      last = now;
      fn.apply(this, args);
    } else {
      pendingArgs = args;                             // remember the LATEST call…
      timer ??= setTimeout(() => {                    // …and run it when the interval ends
        last = Date.now();
        timer = undefined;
        fn.apply(this, pendingArgs);
      }, remaining);
    }
  }

  throttled.cancel = () => { clearTimeout(timer); timer = undefined; };
  return throttled;
}
```

The same ten-call burst through `throttle(fn, 30)`:

```
call(1)  @0ms
call(3)  @30ms
call(6)  @60ms
call(9)  @90ms
call(10) @120ms     ← the trailing call, so the last value is not dropped
```

A steady rhythm of runs, roughly every 30 ms, while the calls keep coming. (Which call number lands on
each beat depends on exact timing — it is always the most recent one at that moment.)

## 🎞️ For Visual Updates: Throttle With `requestAnimationFrame`

When the work updates the screen — moving an element as the user scrolls — the right throttle is "once
per frame." A flag plus `requestAnimationFrame` achieves it without any timer arithmetic:

```js
let ticking = false;

addEventListener("scroll", () => {
  if (!ticking) {
    ticking = true;
    requestAnimationFrame(() => {
      updateParallax();                               // runs once per frame, at most
      ticking = false;
    });
  }
});
```

In a test, 50 `scroll` events dispatched back-to-back caused exactly **one** handler run. Because the
callback runs just before the next repaint, the update is also perfectly timed for rendering.

## 🆚 Choosing

| Situation | Use | Why |
|-----------|-----|-----|
| Search-as-you-type, autosave, validation on input | **Debounce** | Only the final value matters |
| Window `resize` handling that recalculates layout | **Debounce** (or `ResizeObserver`) | Wait for the resizing to finish |
| `scroll`, `mousemove`, drag, live position tracking | **Throttle** (or `requestAnimationFrame`) | You need regular updates *during* the gesture |
| Button that must react instantly but not double-fire | **Leading debounce** | Immediate response, ignore the rest |

Two related options often make both unnecessary: **passive listeners**
(`addEventListener("scroll", fn, { passive: true })`, see
[event-listeners.md](../events/event-listeners.md)) so scrolling is never blocked waiting on your
handler, and the [observer APIs](intersection-mutation-and-resize-observers.md), which replace a lot of
scroll- and resize-handler code outright.

## 📚 Use a Library When You Need the Edge Cases

Hand-rolled versions are great for learning and for simple cases. For production code with `leading`,
`trailing`, `maxWait`, `flush`, and `cancel` semantics, a tested implementation such as lodash's
[`debounce` and `throttle`](https://lodash.com/docs/#debounce) saves you from subtle bugs — lodash's
`_.debounce` documents `leading`, `trailing`, and `maxWait` options and `cancel`/`flush` methods.

## 🎤 Interview Angle

- **"What is the difference between debouncing and throttling?"** Debounce waits for a pause and runs
  once after the calls stop; throttle runs at a steady maximum rate during the calls.
- **"Implement `debounce`."** A closure holding a timer: clear it on every call and start a new one that
  invokes the function with the latest arguments.
- **"Which would you use for a search box? For scroll?"** Debounce for search; throttle (or
  `requestAnimationFrame`) for scroll.
- **"What must a good wrapper preserve?"** `this` and all arguments (`fn.apply(this, args)`), plus a way
  to cancel.

## Common Mistakes

- **Creating the debounced function inside the handler or on every render**, so each call gets a fresh
  timer and nothing is ever debounced — create it once and reuse it.
- **Using arrow functions where `this` is needed** inside the wrapper.
- **Debouncing something that needs regular updates** (a drag), making the UI feel frozen.
- **Not cancelling** pending calls on teardown.
- **Reaching for debounce/throttle when an observer or a passive listener would remove the problem.**

## ➡️ Next

Continue to [forms-and-constraint-validation.md](forms-and-constraint-validation.md) for the
browser's built-in form validation — and why it does not replace server-side checks.
