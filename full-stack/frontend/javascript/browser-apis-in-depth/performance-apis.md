# 📈 Performance APIs

## Measure First, Optimize Second

"The page feels slow" is not actionable. The browser exposes a family of APIs, grouped under
`performance`, that let your own code record **how long things took** — your functions, the page load,
network requests, and the user-experience metrics (Core Web Vitals) the platform tracks. The
[frontend performance module](../../performance/frontend-performance-fundamentals/measuring-performance.md)
covers which metrics matter and which tools report them; this file shows how to collect the same data
**programmatically**, in the page, in real users' browsers.

## ⏱️ `performance.now()`: The Right Clock for Durations

`performance.now()` returns a high-resolution timestamp in milliseconds, relative to the page's time
origin. MDN stresses two properties that make it better than `Date.now()` for measuring durations:

- It is **monotonic** — it never goes backward and ignores system clock adjustments.
- It has sub-millisecond precision (`Date.now()` is whole milliseconds since 1970).

```js
const start = performance.now();
doWork();
const elapsed = performance.now() - start;
console.log(`doWork took ${elapsed.toFixed(2)} ms`);
```

Its resolution is deliberately **coarsened** to limit timing attacks and fingerprinting: MDN gives
5 microseconds in cross-origin-isolated contexts and 100 microseconds otherwise. Sampling successive
calls in a test page found a smallest step of exactly `0.1` ms. Treat sub-100 µs differences as noise,
and benchmark by repeating an operation many times and dividing.

Use `Date.now()` when you need a calendar time (a timestamp to store or display); use
`performance.now()` when you need to know how long something took.

## 🏷️ User Timing: Marks and Measures

Name moments with **marks**, then compute the time between them with a **measure**. The entries land
in the browser's performance timeline, where DevTools can display them too.

```js
performance.mark("task-start");
runExpensiveTask();
performance.mark("task-end", { detail: { rows: 42 } });    // optional metadata

const measure = performance.measure("task", "task-start", "task-end");
console.log(measure.name, Math.round(measure.duration));   // task 30   (a 30 ms task in the test)

console.log(performance.getEntriesByName("task").length);        // 1
console.log(performance.getEntriesByType("mark").map((m) => m.name));   // [ 'task-start', 'task-end' ]
console.log(performance.getEntriesByName("task-end")[0].detail);        // { rows: 42 }
```

`getEntriesByName` and `getEntriesByType` query the timeline; `performance.clearMarks()` and
`clearMeasures()` empty it (do this in long-lived pages, since entries accumulate).

## 👂 `PerformanceObserver`: Be Notified Instead of Polling

A `PerformanceObserver` calls you as new entries are recorded — no need to poll the timeline.

```js
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.log(`${entry.entryType}:${entry.name}`);
  }
});

observer.observe({ entryTypes: ["mark", "measure"] });

// …running the mark/measure code above logs, in order:
// mark:task-start
// measure:task
// mark:task-end
```

(Entries are listed by start time: the `measure` begins when `task-start` was recorded, so it appears
before the later `task-end` mark even though it was created after it.) `observe()` also accepts `{ type: "paint", buffered: true }` to
include entries recorded **before** you started observing — essential for load-time metrics, because
your script usually runs after they happen. `PerformanceObserver.supportedEntryTypes` lists what the
current browser supports; the Chromium-based test browser listed `mark`, `measure`, `navigation`,
`paint`, `resource`, `largest-contentful-paint`, `layout-shift`, `longtask`, `event`, `first-input`,
`long-animation-frame`, and more. Always feature-detect before relying on a type.

| Entry type | What it records |
|------------|-----------------|
| `mark`, `measure` | Your own user-timing entries |
| `navigation` | The page load itself |
| `resource` | Each fetched resource (script, image, `fetch`) |
| `paint` | First paint and first contentful paint |
| `largest-contentful-paint` | Core Web Vital: when the main content appeared |
| `layout-shift` | Core Web Vital: unexpected layout movement |
| `longtask` / `long-animation-frame` | Work that blocked the main thread |
| `event` / `first-input` | Input responsiveness (the basis of INP) |

## 🚀 Page Load: Navigation, Paint, and Resource Timing

The `navigation` entry describes the page load, with timestamps for each phase:

```js
const [nav] = performance.getEntriesByType("navigation");

console.log(nav.type);                  // "navigate" (vs "reload", "back_forward")
console.log(nav.responseEnd);           // when the HTML finished arriving
console.log(nav.domInteractive);        // when the document became interactive
console.log(nav.loadEventEnd);          // when the load event finished
console.log(nav.transferSize);          // bytes transferred over the network
```

Paint timing reports when the browser first drew something:

```js
console.log(performance.getEntriesByType("paint").map((p) => p.name));
// [ 'first-paint', 'first-contentful-paint' ]
```

And each network request the page made becomes a `resource` entry
(`performance.getEntriesByType("resource")`), with its URL, duration, and size — a quick way to find
slow or oversized assets from inside the page.

## 📡 Using the Data: Real-User Monitoring

Measuring in a developer's browser tells you about one fast machine. The valuable use is collecting the
same measurements from real users and sending them to your analytics endpoint, ideally with
`navigator.sendBeacon`, which is designed to deliver data reliably as a page unloads:

```js
function report(metric) {
  navigator.sendBeacon("/analytics", JSON.stringify(metric));
}

new PerformanceObserver((list) => {
  const entries = list.getEntries();
  report({ name: "LCP", value: entries[entries.length - 1].startTime });
}).observe({ type: "largest-contentful-paint", buffered: true });
```

The metrics worth collecting — LCP, INP, CLS — and their thresholds are explained in
[core-web-vitals.md](../../performance/frontend-performance-fundamentals/core-web-vitals.md), and the
back-end half of this pipeline (logging and monitoring what you collect) in
[Monitoring and Observability](../../../production-systems/monitoring-and-observability/).

## 🎤 Interview Angle

- **"`performance.now()` vs. `Date.now()`?"** `performance.now()` is monotonic, relative to page load,
  and sub-millisecond (though deliberately coarsened); `Date.now()` is wall-clock milliseconds and can
  jump if the system clock changes.
- **"How do you measure how long a function takes?"** `performance.now()` before and after, or
  `performance.mark`/`measure` so it shows in DevTools — repeated many times for stable results.
- **"How do you get Core Web Vitals in code?"** A `PerformanceObserver` for `largest-contentful-paint`,
  `layout-shift`, and event entries, with `buffered: true`.
- **"Why `buffered: true`?"** Some entries are recorded before your script runs; `buffered` replays them.

## Common Mistakes

- **Timing with `Date.now()`** and getting jumps or coarse results.
- **Benchmarking a single run** of a very fast operation.
- **Forgetting `buffered: true`** and missing load-time entries.
- **Assuming every browser supports every entry type** without checking `supportedEntryTypes`.
- **Never clearing marks and measures** in long-lived pages.
- **Optimizing without measuring** — or measuring only on a fast development machine.

## ➡️ Next

Continue to [debouncing-and-throttling.md](debouncing-and-throttling.md) to control how often
event-driven code runs.
