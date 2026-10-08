# 🗺️ JavaScript Interview Topic Map

## One Page That Connects Interview Topics to Where They Are Taught

JavaScript interviews draw on a wide but predictable set of topic areas. This file organizes those areas,
shows where each one is taught in this platform, and points to the matching puzzle file when there is one.
It is a **study map**, not a list of questions: use it to find gaps in your preparation, then work through
the linked concept files and puzzles.

## 🧭 How to Use the Map

Work in four passes for each topic area:

1. **Learn** — read the concept files linked in the table, running the examples.
2. **Predict** — do the matching puzzles *without running them*, writing your trace as you go.
3. **Explain** — say the answer aloud in about a minute using the shape *definition → trace → pitfall →
   what you do in real code*. If you cannot, reread the concept file.
4. **Vary** — change one detail in a puzzle (swap `var` for `let`, add a `bind`, move a timer) and predict again.

The puzzle files are [closures-and-scope-puzzles.md](closures-and-scope-puzzles.md),
[hoisting-and-tdz-puzzles.md](hoisting-and-tdz-puzzles.md),
[this-and-prototype-puzzles.md](this-and-prototype-puzzles.md),
[coercion-and-equality-puzzles.md](coercion-and-equality-puzzles.md), and
[event-loop-ordering-puzzles.md](event-loop-ordering-puzzles.md).

## 🧱 Language Core

| Topic | Learn it | Practise it |
|-------|----------|-------------|
| Data types, `typeof`, primitives vs. objects | [data-types.md](../introduction-to-javascript/data-types.md) | [Coercion puzzles](coercion-and-equality-puzzles.md) |
| `var`, `let`, `const` | [variables.md](../introduction-to-javascript/variables.md), [let-and-const.md](../modern-javascript/let-and-const.md) | [Hoisting puzzles](hoisting-and-tdz-puzzles.md) |
| Operators, truthy/falsy, `==` vs. `===` | [operators.md](../operators-and-type-system/operators.md), [truthy-and-falsy.md](../operators-and-type-system/truthy-and-falsy.md), [type-coercion.md](../operators-and-type-system/type-coercion.md) | [Coercion puzzles](coercion-and-equality-puzzles.md) |
| Scope and the scope chain | [scope.md](../functions/scope.md), [execution-contexts-and-the-scope-chain.md](../execution-context-and-hoisting/execution-contexts-and-the-scope-chain.md) | [Closure puzzles](closures-and-scope-puzzles.md) |
| Closures | [closures.md](../functions/closures.md) | [Closure puzzles](closures-and-scope-puzzles.md) |
| Hoisting and the temporal dead zone | [hoisting-and-the-temporal-dead-zone.md](../execution-context-and-hoisting/hoisting-and-the-temporal-dead-zone.md) | [Hoisting puzzles](hoisting-and-tdz-puzzles.md) |
| Strict mode, automatic semicolon insertion | [strict-mode.md](../execution-context-and-hoisting/strict-mode.md), [automatic-semicolon-insertion.md](../execution-context-and-hoisting/automatic-semicolon-insertion.md) | [Hoisting puzzles](hoisting-and-tdz-puzzles.md) (strict-mode variations) |
| Function declarations vs. expressions, arrow functions | [function-declarations-and-expressions.md](../functions/function-declarations-and-expressions.md), [arrow-functions.md](../functions/arrow-functions.md), [parameters-and-return-values.md](../functions/parameters-and-return-values.md) | [Hoisting](hoisting-and-tdz-puzzles.md) and [`this`](this-and-prototype-puzzles.md) puzzles |
| `this`, `call`, `apply`, `bind` | [this-keyword.md](../advanced-javascript/this-keyword.md), [call-apply-and-bind.md](../functional-javascript/call-apply-and-bind.md) | [`this` puzzles](this-and-prototype-puzzles.md) |
| Prototypes, inheritance, classes | [prototypes.md](../advanced-javascript/prototypes.md), [prototypal-inheritance.md](../advanced-javascript/prototypal-inheritance.md), [classes.md](../advanced-javascript/classes.md), [private-class-fields.md](../objects-in-depth/private-class-fields.md) | [Prototype puzzles](this-and-prototype-puzzles.md) |
| Conditionals and loops | [conditional-statements.md](../conditionals-and-loops/conditional-statements.md), [loops.md](../conditionals-and-loops/loops.md), [switch-statements.md](../conditionals-and-loops/switch-statements.md) | Warm-up topics; expect them inside larger questions |

## 🧰 Functions and Patterns

| Topic | Learn it | Practise it |
|-------|----------|-------------|
| Higher-order functions | [higher-order-functions.md](../functional-javascript/higher-order-functions.md) | Write `once`, then your own versions of `map` and `filter` |
| Currying and partial application | [currying-and-partial-application.md](../functional-javascript/currying-and-partial-application.md) | Write `curry` for fixed and variable arity |
| Composition and pipelines | [function-composition-and-pipelines.md](../functional-javascript/function-composition-and-pipelines.md) | Write `compose` and `pipe` |
| Memoization | [memoization.md](../functional-javascript/memoization.md) | Write `memoize`, then a bounded (LRU-style) version |
| Pure functions, immutability | [pure-functions-and-immutability.md](../functional-javascript/pure-functions-and-immutability.md) | Rewrite a mutating function as a pure one |
| IIFE and the module pattern | [iife-and-the-module-pattern.md](../functional-javascript/iife-and-the-module-pattern.md) | [Closure puzzles](closures-and-scope-puzzles.md) (the loop-fix puzzle) |

## 🗃️ Objects, Arrays, and Built-Ins

| Topic | Learn it |
|-------|----------|
| Objects and object methods | [objects.md](../arrays-and-objects/objects.md), [object-methods.md](../arrays-and-objects/object-methods.md) |
| Arrays and array methods | [arrays.md](../arrays-and-objects/arrays.md), [array-methods.md](../arrays-and-objects/array-methods.md), [modern-array-and-object-methods.md](../modern-javascript/modern-array-and-object-methods.md) |
| Destructuring, spread, and rest | [destructuring.md](../arrays-and-objects/destructuring.md), [spread-and-rest-operators.md](../modern-javascript/spread-and-rest-operators.md) |
| Shallow vs. deep copy | [copying-objects-shallow-vs-deep.md](../objects-in-depth/copying-objects-shallow-vs-deep.md) |
| Freezing, sealing, immutability | [freezing-sealing-and-immutability.md](../objects-in-depth/freezing-sealing-and-immutability.md) |
| Property descriptors, getters and setters | [property-descriptors-and-getters-setters.md](../objects-in-depth/property-descriptors-and-getters-setters.md) |
| `Proxy` and `Reflect` | [proxy-and-reflect.md](../objects-in-depth/proxy-and-reflect.md) |
| JSON | [json-serialization.md](../objects-in-depth/json-serialization.md) |
| `Map`, `Set`, `WeakMap`, `WeakRef` | [map-and-set.md](../built-in-objects-and-collections/map-and-set.md), [weakmap-weakset-and-weakref.md](../built-in-objects-and-collections/weakmap-weakset-and-weakref.md) |
| Strings, numbers, `BigInt`, dates | [strings-and-unicode.md](../built-in-objects-and-collections/strings-and-unicode.md), [numbers-math-and-bigint.md](../built-in-objects-and-collections/numbers-math-and-bigint.md), [dates-and-intl.md](../built-in-objects-and-collections/dates-and-intl.md) |
| Symbols, iterators, generators, regular expressions | [symbols.md](../additional-javascript-topics/symbols.md), [iterators-and-generators.md](../additional-javascript-topics/iterators-and-generators.md), [regular-expressions.md](../additional-javascript-topics/regular-expressions.md) |

## ⏳ Asynchronous JavaScript

| Topic | Learn it | Practise it |
|-------|----------|-------------|
| Callbacks | [callbacks.md](../asynchronous-programming-and-modules/callbacks.md) | Wrap a callback-style function in a `new Promise` (the pattern is in [promises.md](../asynchronous-programming-and-modules/promises.md)) |
| Promises | [promises.md](../asynchronous-programming-and-modules/promises.md) | [Event loop puzzles](event-loop-ordering-puzzles.md) |
| `async`/`await` | [async-await.md](../asynchronous-programming-and-modules/async-await.md) | [Event loop puzzles](event-loop-ordering-puzzles.md) |
| The event loop, call stack, task queues | [call-stack.md](../event-loop/call-stack.md), [web-apis.md](../event-loop/web-apis.md), [callback-queue.md](../event-loop/callback-queue.md), [microtasks-and-macrotasks.md](../event-loop/microtasks-and-macrotasks.md) | [Event loop puzzles](event-loop-ordering-puzzles.md) |
| Promise combinators, retries, timeouts | [promise-combinators-in-depth.md](../advanced-async-patterns/promise-combinators-in-depth.md) | Write a `retry` with backoff and a `timeout` wrapper |
| Timers and scheduling | [timers-and-scheduling.md](../advanced-async-patterns/timers-and-scheduling.md) | [Event loop puzzles](event-loop-ordering-puzzles.md) |
| Cancellation | [cancellation-with-abortcontroller.md](../advanced-async-patterns/cancellation-with-abortcontroller.md) | Cancel an in-flight `fetch` |
| Unhandled rejections | [handling-unhandled-rejections.md](../advanced-async-patterns/handling-unhandled-rejections.md) | Explain why `try`/`catch` misses an un-awaited promise |
| Async iteration | [async-iterators-and-for-await.md](../advanced-async-patterns/async-iterators-and-for-await.md) | Consume a paged API with `for await` |
| Web Workers | [web-workers.md](../advanced-async-patterns/web-workers.md) | Move a CPU-heavy loop off the main thread |
| `fetch` and AJAX | [fetch-api.md](../asynchronous-programming-and-modules/fetch-api.md), [ajax-and-xmlhttprequest.md](../browser-apis-in-depth/ajax-and-xmlhttprequest.md) | Handle HTTP errors (a `404` does not reject) |

## ✨ Modules and Modern Syntax

| Topic | Learn it |
|-------|----------|
| ES modules vs. CommonJS | [javascript-modules.md](../asynchronous-programming-and-modules/javascript-modules.md), [javascript-runtimes-browser-vs-nodejs.md](../how-javascript-runs/javascript-runtimes-browser-vs-nodejs.md) |
| Template literals | [template-literals.md](../modern-javascript/template-literals.md) |
| Optional chaining and `??` | [optional-chaining-and-nullish-coalescing.md](../modern-javascript/optional-chaining-and-nullish-coalescing.md) |
| Logical assignment, numeric separators | [logical-assignment-and-numeric-separators.md](../modern-javascript/logical-assignment-and-numeric-separators.md) |
| Top-level `await`, import attributes | [top-level-await-and-import-attributes.md](../modern-javascript/top-level-await-and-import-attributes.md) |
| Static blocks, error `cause`, iterator helpers | [static-blocks-error-cause-and-iterator-helpers.md](../modern-javascript/static-blocks-error-cause-and-iterator-helpers.md) |

## 🌐 Browser and DOM

| Topic | Learn it |
|-------|----------|
| The DOM: selecting, changing, creating, removing | [dom-introduction.md](../dom-manipulation/dom-introduction.md), [selecting-elements.md](../dom-manipulation/selecting-elements.md), [manipulating-elements.md](../dom-manipulation/manipulating-elements.md), [creating-and-removing-elements.md](../dom-manipulation/creating-and-removing-elements.md) |
| Events, propagation, delegation | [event-listeners.md](../events/event-listeners.md), [event-object.md](../events/event-object.md), [event-propagation.md](../events/event-propagation.md), [event-delegation.md](../events/event-delegation.md) |
| Debouncing and throttling | [debouncing-and-throttling.md](../browser-apis-in-depth/debouncing-and-throttling.md) |
| Observers (intersection, mutation, resize) | [intersection-mutation-and-resize-observers.md](../browser-apis-in-depth/intersection-mutation-and-resize-observers.md) |
| Cookies and Web Storage | [cookies.md](../using-browser-functionalities/cookies.md), [local-storage.md](../using-browser-functionalities/local-storage.md), [session-storage.md](../using-browser-functionalities/session-storage.md) |
| IndexedDB, service workers, offline | [indexeddb.md](../offline-and-real-time-web-apis/indexeddb.md), [service-workers-and-the-cache-api.md](../offline-and-real-time-web-apis/service-workers-and-the-cache-api.md) |
| WebSockets and server-sent events | [websockets.md](../offline-and-real-time-web-apis/websockets.md), [server-sent-events.md](../offline-and-real-time-web-apis/server-sent-events.md), [choosing-a-real-time-strategy.md](../offline-and-real-time-web-apis/choosing-a-real-time-strategy.md) |
| Forms, URL and history, files, performance APIs | [forms-and-constraint-validation.md](../browser-apis-in-depth/forms-and-constraint-validation.md), [url-and-history-apis.md](../browser-apis-in-depth/url-and-history-apis.md), [files-blobs-and-clipboard.md](../browser-apis-in-depth/files-blobs-and-clipboard.md), [performance-apis.md](../browser-apis-in-depth/performance-apis.md) |

## 🛠️ Errors, Performance, and Tooling

| Topic | Learn it |
|-------|----------|
| Errors, `try`/`catch`/`finally`, debugging | [errors.md](../error-handling-and-debugging/errors.md), [try-catch-finally.md](../error-handling-and-debugging/try-catch-finally.md), [debugging-techniques.md](../error-handling-and-debugging/debugging-techniques.md) |
| Garbage collection and memory leaks | [memory-management-and-garbage-collection.md](../how-javascript-runs/memory-management-and-garbage-collection.md), [finding-and-fixing-memory-leaks.md](../how-javascript-runs/finding-and-fixing-memory-leaks.md) |
| Engines and JIT compilation | [javascript-engines-and-jit-compilation.md](../how-javascript-runs/javascript-engines-and-jit-compilation.md) |
| Transpilers, polyfills, bundlers | [transpilers-polyfills-and-browser-support.md](../how-javascript-runs/transpilers-polyfills-and-browser-support.md), [bundlers-tree-shaking-and-minification.md](../how-javascript-runs/bundlers-tree-shaking-and-minification.md) |

## 🔗 Related Areas Beyond Core JavaScript

Front-end interviews usually continue into neighbouring areas. This platform covers several of them in their
own sections:

| Area | Start here |
|------|------------|
| TypeScript | [TypeScript Essentials](../../typescript/typescript-essentials/README.md) |
| Front-end testing | [Frontend Testing Fundamentals](../../testing/frontend-testing-fundamentals/README.md) |
| Front-end performance | [Frontend Performance Fundamentals](../../performance/frontend-performance-fundamentals/README.md) |
| Cross-site scripting | [Cross-Site Scripting (XSS)](../../../web-security/cross-site-scripting-xss/README.md) |
| Data structures and algorithms | [Time and Space Complexity](../../../data-structures-and-algorithms/time-and-space-complexity/README.md), [Arrays](../../../data-structures-and-algorithms/arrays/README.md) |

## 🏋️ Classic Exercises and Their Building Blocks

Short coding exercises recur in interviews. These are the common ones that this platform has the building
blocks for; the linked file contains a worked implementation or the concepts you need.

| Exercise | Where to start |
|----------|----------------|
| Write `debounce` / `throttle` | [debouncing-and-throttling.md](../browser-apis-in-depth/debouncing-and-throttling.md) |
| Write `curry` | [currying-and-partial-application.md](../functional-javascript/currying-and-partial-application.md) |
| Write `memoize` (and a bounded cache) | [memoization.md](../functional-javascript/memoization.md) |
| Write `compose` / `pipe` | [function-composition-and-pipelines.md](../functional-javascript/function-composition-and-pipelines.md) |
| Write `once` | [higher-order-functions.md](../functional-javascript/higher-order-functions.md); also the final [closure puzzle](closures-and-scope-puzzles.md) |
| Implement `bind` | [call-apply-and-bind.md](../functional-javascript/call-apply-and-bind.md) ("How `bind` Works: A Simplified Version") |
| Deep-clone an object | [copying-objects-shallow-vs-deep.md](../objects-in-depth/copying-objects-shallow-vs-deep.md) |
| Retry a failing request with backoff | [promise-combinators-in-depth.md](../advanced-async-patterns/promise-combinators-in-depth.md) |
| Cancel an in-flight request | [cancellation-with-abortcontroller.md](../advanced-async-patterns/cancellation-with-abortcontroller.md) |
| Attach one listener for many items | [event-delegation.md](../events/event-delegation.md) |
| Group a list by a key | [modern-array-and-object-methods.md](../modern-javascript/modern-array-and-object-methods.md) (`Object.groupBy`) |

## ✅ Self-Check: Can You Explain These Without Notes?

If any item is shaky, follow the link, then redo the matching puzzles.

- Why `var` in a loop with a timer prints the final value, and two ways to fix it
  ([closures](closures-and-scope-puzzles.md)).
- The two phases of execution, and what each kind of declaration holds before its line runs
  ([hoisting](hoisting-and-tdz-puzzles.md)).
- The call-site rules for `this`, and why arrow functions ignore them
  ([`this`](this-and-prototype-puzzles.md)).
- What the prototype chain is, and what happens on read versus write
  ([prototypes](this-and-prototype-puzzles.md)).
- Why `[] == ![]` is `true`, and what you would write instead
  ([coercion](coercion-and-equality-puzzles.md)).
- The exact order of synchronous code, microtasks, and timers
  ([event loop](event-loop-ordering-puzzles.md)).
- When to use `??` instead of `||` ([operators](coercion-and-equality-puzzles.md)).
- How `async` functions report errors, and why `Promise.all` preserves input order
  ([async](event-loop-ordering-puzzles.md)).

## 🎤 Interview Angle

- **Prepare by area, not by question.** Interviewers rephrase; the underlying rules do not change.
- **Practise the explanation, not only the answer.** Saying "closures capture variables, so this prints the
  final value" shows the model behind the result.
- **Say what you would do in production.** After explaining a quirk, add the practical rule (`===`,
  `let`/`const`, arrow callbacks, `??` for defaults). It shows judgement, not just trivia knowledge.
- **Admit uncertainty precisely.** "I would check the specification or run it" is a better answer than a
  confident guess, and it is what you do on the job.

## Common Mistakes

- **Memorising outputs** instead of the rules that produce them.
- **Skipping the explain-aloud pass**, then struggling to articulate an answer you "know."
- **Practising only puzzles**, with no coding exercises (debounce, curry, memoize, retry).
- **Neglecting the browser and async topics** because the language puzzles feel more like "real" interview questions.

## ➡️ Back to the Module

Return to the [Interview Puzzles overview](README.md).
