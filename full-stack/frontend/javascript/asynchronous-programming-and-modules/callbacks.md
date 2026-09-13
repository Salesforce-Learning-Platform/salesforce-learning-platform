# Callbacks

## The Original Pattern

A **callback** is a function passed as an argument, to be called later once some operation
completes:

```js
setTimeout(() => {
  console.log("This runs after 1 second");
}, 1000);
```

`setTimeout` doesn't block execution waiting for the second to pass — it registers the callback and
returns immediately, letting the rest of the program continue. The callback runs later, once the
timer completes. This is JavaScript's original mechanism for asynchronous, non-blocking operations.

## "Callback Hell"

Chaining multiple dependent asynchronous steps with callbacks nests them progressively deeper:

```js
getUser(userId, (user) => {
  getPosts(user.id, (posts) => {
    getComments(posts[0].id, (comments) => {
      console.log(comments);
      // deeply nested, and error handling would need to be
      // duplicated at every single level
    });
  });
});
```

Each step depends on the previous one's result, forcing deeper nesting with every additional step —
informally called "callback hell" or the "pyramid of doom." Beyond the visual nesting, error
handling becomes genuinely painful: each level needs its own error-handling logic, since there's no
single, unified way to catch a failure from any step.

## Why This Motivated Promises

The core problems callback hell exposes — awkward error handling, deeply nested code that's hard
to read top-to-bottom, difficulty composing multiple async operations together — are exactly what
Promises (see [promises.md](promises.md)) were designed to solve, by giving asynchronous operations
a consistent, chainable interface instead of an ad hoc, per-API convention for handling completion
and errors.

## Where Callbacks Still Appear

Callbacks haven't disappeared — event listeners (see [event-listeners.md](../events/event-listeners.md))
are themselves callbacks, and array methods like `map`/`filter`/`forEach` (see
[array-methods.md](../arrays-and-objects/array-methods.md)) also take callback functions. The
specific problem callbacks struggle with is **chaining multiple sequential asynchronous steps**,
not callbacks as a general mechanism.

## Common Mistakes

- Assuming callbacks are obsolete entirely, rather than recognizing they remain the right tool for
  simple, non-chained cases like event listeners.
- Nesting several asynchronous callback-based operations without recognizing the maintenance cost,
  when Promises or `async`/`await` would flatten the same logic considerably.
- Forgetting to handle errors at every level of a callback chain, since there's no single
  centralized error-handling point the way `.catch()` provides for Promises.

## Next

Continue to [promises.md](promises.md) to see how JavaScript addressed these specific problems.
