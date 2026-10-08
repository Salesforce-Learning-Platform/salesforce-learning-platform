# 👁️ Intersection, Mutation, and Resize Observers

## Reacting to Change Without Polling

Pages constantly need to know about change: Did this image scroll into view? Did someone add an
element to the DOM? Did this box get bigger? The old answers — `scroll` handlers, `setInterval`
polling, a `resize` listener on `window` — are wasteful or incomplete. The browser offers three
**observer** APIs that share one shape: you register a callback for something you care about, and the
browser calls it **asynchronously, in batches**, when that thing changes.

| Observer | Watches | Typical use |
|----------|---------|-------------|
| `IntersectionObserver` | Whether an element is visible (in the viewport or another container) | Lazy loading, infinite scroll, "seen" analytics, pausing off-screen video |
| `MutationObserver` | Changes to the DOM tree (children, attributes, text) | Reacting to DOM changes you don't control |
| `ResizeObserver` | An element's size | Responsive components, canvas sizing |

(A fourth, `PerformanceObserver`, is covered in [performance-apis.md](performance-apis.md).)

## 🔭 IntersectionObserver

MDN describes it as asynchronously reporting when a target element enters, exits, or crosses
visibility thresholds relative to a **root** — the viewport by default, or an ancestor element.

### Why Not a Scroll Listener?

The old approach ran code on every `scroll` event, calling `getBoundingClientRect()` for each watched
element. MDN notes this forces layout work on the main thread for every event. With
`IntersectionObserver` the browser computes intersections itself and calls you only when a threshold
is crossed.

### Lazy Loading Images

```js
const observer = new IntersectionObserver((entries, obs) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.src = entry.target.dataset.src;   // start the real download now
      obs.unobserve(entry.target);                    // one-time work: stop watching
    }
  });
}, { rootMargin: "100px" });                          // begin 100px before it scrolls into view

document.querySelectorAll("img[data-src]").forEach((img) => observer.observe(img));
```

(Modern browsers also support the `loading="lazy"` attribute on `<img>` for the simple case; the
observer version is the tool when you need custom behavior.)

### Options and Entry Properties

| Option | Meaning |
|--------|---------|
| `root` | The ancestor used as the viewport; `null` (default) means the browser viewport |
| `rootMargin` | A CSS-style margin that grows or shrinks the root; a positive value triggers *before* the target is visible |
| `threshold` | A ratio (0–1) or array of ratios of the target's visible area that trigger the callback; default `0` |

Each entry reports `isIntersecting`, `intersectionRatio` (0.0–1.0), and the `target`.

### What a Run Looks Like

On a test page with one box near the top and another 4,000 px down, in a 700 px-tall viewport:

```
initial callback            near: visible ratio=1     far: hidden ratio=0
after scrolling to the far box   near: hidden ratio=0   far: visible ratio=1
```

Note the **initial callback**: every observed element reports its starting state once, right after
`observe()`. And `rootMargin` shifts the trigger point. With the page scrolled so the far box was
300 px *below* the viewport:

```
observer with rootMargin: "500px"   →  far: visible
observer without rootMargin         →  far: hidden
```

That early trigger is exactly what you want for lazy loading and infinite scroll: start loading
slightly before the user arrives.

### Infinite Scroll in One Observer

Watch a "sentinel" element at the end of the list and load the next page when it appears:

```js
const sentinel = document.querySelector("#load-more-sentinel");

new IntersectionObserver(async ([entry]) => {
  if (entry.isIntersecting) await loadNextPage();
}, { rootMargin: "300px" }).observe(sentinel);
```

### Caveats

- Callbacks are asynchronous but still run on the **main thread**; MDN advises keeping them short and
  deferring heavy work (for example with `requestIdleCallback`, see
  [timers-and-scheduling.md](../advanced-async-patterns/timers-and-scheduling.md)).
- You get percentage thresholds, not exact overlapping pixels.
- Observers are tied to the browser's rendering updates, so notifications are delayed or paused while
  the page is hidden — in testing inside a hidden browser pane, callbacks took noticeably longer to
  arrive.

## 🧬 MutationObserver

`MutationObserver` reports changes to the DOM tree. It replaced the old, slow "mutation events".

```js
const observer = new MutationObserver((records) => {
  for (const record of records) {
    console.log(record.type, record.attributeName);
  }
});

observer.observe(targetNode, {
  childList: true,        // children added or removed
  attributes: true,       // attribute changes
  subtree: true,          // …anywhere beneath the target, not just direct children
  characterData: true,    // text node content changes
});
```

Other options include `attributeFilter` (watch only named attributes), `attributeOldValue`, and
`characterDataOldValue`. Methods: `disconnect()` stops observing, and `takeRecords()` empties and
returns the queued records.

### Batched, and Delivered as a Microtask

Several changes made in one go arrive as **one callback with several records**, and the callback runs
as a *microtask* — after the current script but before timers:

```js
const order = [];
const observer = new MutationObserver((records) =>
  order.push(`MutationObserver callback (${records.length} records)`));
observer.observe(box, { childList: true, attributes: true, subtree: true, characterData: true });

setTimeout(() => order.push("setTimeout 0"), 0);
Promise.resolve().then(() => order.push("promise.then"));

box.append(document.createElement("span"));      // 1: childList
box.setAttribute("data-x", "1");                  // 2: attributes
box.querySelector("p").firstChild.data = "changed";   // 3: characterData
order.push("sync code finished");

// later: [ 'sync code finished', 'promise.then',
//          'MutationObserver callback (3 records)', 'setTimeout 0' ]
```

Three changes, one callback, three records (`childList`, `attributes`, `characterData`). Calling
`takeRecords()` before the callback runs hands you the pending records and the callback is *not*
invoked for them. With `attributeFilter: ["class"]` and `attributeOldValue: true`, only `class`
changes are reported, each with the previous value:

```
t.className = "a"  →  { attr: "class", old: null }
t.className = "b"  →  { attr: "class", old: "a" }
t.setAttribute("id", "ignored")  →  (no record)
```

### A Practical Use: Waiting for an Element to Exist

When a third-party widget or late-loading script injects markup you need, observe the document until
the element appears — and support cancellation
([cancellation-with-abortcontroller.md](../advanced-async-patterns/cancellation-with-abortcontroller.md)):

```js
function waitForElement(selector, { signal } = {}) {
  return new Promise((resolve, reject) => {
    const existing = document.querySelector(selector);
    if (existing) return resolve(existing);

    const observer = new MutationObserver(() => {
      const element = document.querySelector(selector);
      if (element) {
        observer.disconnect();
        resolve(element);
      }
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });

    signal?.addEventListener("abort", () => {
      observer.disconnect();
      reject(signal.reason);
    }, { once: true });
  });
}

const widget = await waitForElement("#late-widget");       // resolved when the element was added
// with an aborted signal, it rejects with AbortError and the observer is disconnected
```

### When Not to Use It

For DOM changes *your own code* makes, use direct calls, events, or your framework's state. Reserve
`MutationObserver` for changes you cannot hook into (third-party scripts, browser extensions, content
edited by users). Avoid modifying the observed subtree from inside its own callback — that triggers
the callback again — and avoid observing a whole large document with `subtree: true` when a narrower
target will do.

## 📐 ResizeObserver

`ResizeObserver` fires when an element's size changes — from CSS, content changes, or any cause, not
just a window resize. Each entry carries `contentRect` and `contentBoxSize` (and `borderBoxSize`).

```js
const resizeObserver = new ResizeObserver((entries) => {
  for (const entry of entries) {
    console.log(entry.contentRect.width, entry.borderBoxSize[0].inlineSize);
  }
});

resizeObserver.observe(box);
```

Measured on a box with `width: 100px`, `padding: 10px`, `border: 5px`, then widened to 200 px:

```
on observe()         content width 100, border-box width 130
after width: 200px   content width 200, border-box width 230
```

Two things to notice: the **initial callback** fires on `observe()` just like the other observers, and
content-box and border-box differ by the padding and border (30 px here). Pass
`{ box: "border-box" }` to `observe()` to choose which box triggers notifications.

This is more flexible than the `window` `resize` event, which reports only viewport changes. Use it for
components that adapt to their own container, and for keeping a `<canvas>` backing store matched to its
displayed size.

### The "Loop" Error

If your callback changes the size of something observed, the browser may be unable to deliver every
notification within the same frame and logs
`ResizeObserver loop completed with undelivered notifications.` MDN explains it does not freeze the page
— the browser defers the notifications to the next frame — but an endless cycle (a callback that keeps
growing an observed element) repeats it every frame. Fixes: avoid resizing when the element is already
the right size, or defer an intentional resize with `requestAnimationFrame`.

## 🧹 Clean Up

Observers hold references to their targets and callbacks. Call `unobserve(target)` when you are done
with one element and `disconnect()` when you are done with the observer — in a component, do this in the
teardown function so a removed component does not leak.

## 🎤 Interview Angle

- **"How would you implement lazy loading or infinite scroll?"** With an `IntersectionObserver`
  watching the images or a sentinel element, using `rootMargin` to start slightly early, and
  `unobserve` after the one-time work.
- **"Why is `IntersectionObserver` better than a scroll listener?"** The browser computes
  intersections and calls you only on threshold crossings, instead of running your code — and forcing
  layout — on every scroll event.
- **"When does a `MutationObserver` callback run?"** As a microtask after the current script, batching
  all changes made in that script into one call.
- **"How does `ResizeObserver` differ from the `window` `resize` event?"** It reports size changes of
  individual elements, whatever caused them.

## Common Mistakes

- **Using scroll handlers with `getBoundingClientRect`** for visibility checks.
- **Forgetting that each observer calls back once initially** and treating that as a "change."
- **Never calling `unobserve`/`disconnect`**, leaking elements and callbacks.
- **Mutating the observed DOM inside a `MutationObserver` callback**, causing a loop.
- **Resizing an observed element inside its `ResizeObserver` callback** without a guard.
- **Doing heavy work inside observer callbacks**, which run on the main thread.

## ➡️ Next

Continue to [url-and-history-apis.md](url-and-history-apis.md) to see how to parse, build, and change
URLs — including updating the address bar without reloading the page.
