# 🧹 Memory Management and Garbage Collection

## You Never Call `free` — So Who Does?

In JavaScript you create objects, arrays, strings, and closures without ever releasing them. Memory is
reclaimed by the engine's **garbage collector** (GC). That convenience is real, but it hides a rule
every developer must understand to avoid leaks: **the collector frees only what is unreachable.** Keeping
things reachable by accident is the entire story of
[JavaScript memory leaks](finding-and-fixing-memory-leaks.md); this file builds the model underneath.

## ♻️ The Life Cycle

MDN's memory-management guide describes three steps common to every language:

1. **Allocate** — memory is claimed when you create a value (`{}`, `[]`, `"text"`, a function).
2. **Use** — you read and write it.
3. **Release** — memory is returned when it is no longer needed.

In JavaScript, steps 1 and 3 are implicit. The hard question is deciding what is "no longer needed."

## 🎯 Reachability, Not Usefulness

The engine cannot know whether you will use an object again — that is undecidable in general. It
approximates with something it *can* compute: **reachability**. Per MDN, collection starts from **roots**
(the global object, the currently running functions' variables) and follows references; anything it can
reach is kept, and the rest is garbage.

This is the **mark-and-sweep** idea (used by all modern engines): *mark* everything reachable from the
roots, then *sweep* away what is unmarked. It replaced simple **reference counting** ("free an object
when nothing points to it"), which MDN notes no modern engine uses, because objects that reference each
other in a cycle keep each other's counts above zero forever. With reachability, cycles are not a
problem — an unreachable cycle is simply unreachable. A test confirmed it:

```js
let a = { name: "a" };
let b = { name: "b" };
a.other = b;
b.other = a;                    // a cycle: each references the other

const ref = new WeakRef(a);     // observe without keeping alive (see weakmap-weakset-and-weakref.md)
a = b = null;                   // drop both outside references

// after a garbage collection:
ref.deref();                    // undefined — the whole cycle was collected
```

And the other direction — an object that is still referenced elsewhere is never collected, no matter how
long ago you finished with it ("object still referenced is NOT collected: true" in the same test).

> Running these experiments needs Node's `--expose-gc` flag and a `global.gc()` call, which are for
> testing only. In normal operation, collection timing is up to the engine
> ([weakmap-weakset-and-weakref.md](../built-in-objects-and-collections/weakmap-weakset-and-weakref.md)).

## 🧪 Watching Memory Move

`process.memoryUsage()` in Node.js reports `rss`, `heapTotal`, `heapUsed`, `external`, and
`arrayBuffers`; `heapUsed` is the number to watch for JavaScript objects. Allocating three million small
objects, then dropping the reference and collecting:

```js
const mb = (n) => Math.round(n / 1024 / 1024);
const heapMB = () => mb(process.memoryUsage().heapUsed);

global.gc();
const base = heapMB();                                            // baseline
let big = Array.from({ length: 3_000_000 }, (_, i) => ({ i }));
const during = heapMB();                                          // holding 3M objects
big = null;                                                       // drop the only reference
global.gc();

console.log(`baseline ${base} MB -> holding ${during} MB -> after drop + gc ${heapMB()} MB`);
// baseline 4 MB -> holding 118 MB -> after drop + gc 4 MB
```

Memory rose from 4 MB to 118 MB while the array was reachable and fell back to 4 MB once it was not —
the collector can only reclaim after the last reference is gone.

## 🏗️ How V8 Collects: Generations

V8's collector is **generational**, built on the observation (the *generational hypothesis*) that most
objects die young. From V8's "Trash talk" article:

- The heap has a **young generation** (new objects) and an **old generation** (objects that survived).
- A **minor GC**, the **Scavenger**, collects only the young generation. It copies the survivors into a
  fresh space and discards the rest, so its cost tracks the number of survivors, not the number of
  allocations. It is cheap and frequent.
- A **major GC**, **Mark-Compact**, collects the whole heap in three phases — mark the reachable objects,
  sweep the dead gaps, and compact fragmented pages. It is more expensive and rarer.
- Under the project name **Orinoco**, V8 moves GC work off the main thread: **parallel** (helper threads
  during a pause), **incremental** (small slices interleaved with your code), and **concurrent** (helper
  threads while your code runs) techniques that keep pauses short.

`node --trace-gc` shows the collections as they happen. A script that allocated four million short-lived
objects (keeping only one in 200) produced 48 collections, every one a Scavenge, each taking well under a
millisecond:

```
24 ms: Scavenge 4.4 (5.3) -> 3.7 (6.3) MB, 0.62 / 0.00 ms  allocation failure
25 ms: Scavenge 4.4 (6.3) -> 3.9 (6.8) MB, 0.67 / 0.00 ms  allocation failure
26 ms: Scavenge 4.7 (6.8) -> 4.1 (8.8) MB, 0.75 / 0.00 ms  allocation failure
28 ms: Scavenge 5.9 (8.8) -> 4.3 (8.8) MB, 0.58 / 0.00 ms  allocation failure
…
48 Scavenge (minor) collections; 0 Mark-Compact (major) collections
```

Each line shows heap size before → after the collection and the pause. The short-lived objects were
cheap to throw away; that is the generational design working as intended.

## 📏 Measuring Memory

| Where | Tool |
|-------|------|
| Node.js | `process.memoryUsage()`, `v8.getHeapStatistics()` (`total_heap_size`, `used_heap_size`, `heap_size_limit`, …), `v8.writeHeapSnapshot()` |
| Browser | DevTools Memory panel: heap snapshots, allocation timelines, allocation sampling |
| Production | Process memory graphs and alerts, via your monitoring system ([Monitoring and Observability](../../../production-systems/monitoring-and-observability/)) |

Note that `heapUsed` includes garbage not yet collected, so a single reading proves little; trends over
time, ideally after a collection, are what reveal a leak.

## ✅ Writing GC-Friendly Code

- **Let go of references you no longer need** — end the scope, clear a variable, remove an entry. Most
  of the time simply letting functions return is enough.
- **Avoid unbounded growth** in module-level arrays, maps, and caches.
- **Reduce allocation in hot loops** (creating objects millions of times) *when profiling shows GC time
  matters*; short-lived garbage is cheap but not free.
- **Use weak collections** (`WeakMap`, `WeakSet`) to attach data to objects without keeping them alive.
- **Don't try to out-think the collector.** Calling `gc()`, pooling everything, or nulling every variable
  usually adds complexity without benefit.

## 🎤 Interview Angle

- **"How does garbage collection work in JavaScript?"** Reachability: starting from roots, the engine
  marks everything reachable and reclaims the rest (mark-and-sweep).
- **"Why did reference counting get abandoned?"** Circular references keep counts above zero, leaking
  memory.
- **"What is generational GC?"** Most objects die young, so the heap is split into a frequently, cheaply
  collected young generation and a less frequently collected old one.
- **"Can you force garbage collection?"** Not from normal code; only debugging flags such as Node's
  `--expose-gc` expose it.
- **"What does it mean for an object to be 'reachable'?"** There is a chain of references to it from a
  root.

## Common Mistakes

- **Thinking you must free memory** — or that setting a variable to `null` is generally necessary.
- **Equating "no longer used" with "collectable"** — only *unreachable* objects are collected.
- **Reading one `heapUsed` value** as proof of a leak.
- **Forcing GC in production.**
- **Allocating heavily inside hot loops** without measuring.

## ➡️ Next

Continue to [finding-and-fixing-memory-leaks.md](finding-and-fixing-memory-leaks.md) for the specific
ways programs keep memory reachable by accident, and how to find them.
