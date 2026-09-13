# Async/Await

## Syntax

```js
async function loadUserData(userId) {
  const user = await getUser(userId);
  const posts = await getPosts(user.id);
  const comments = await getComments(posts[0].id);
  return comments;
}
```

Compare this directly to the equivalent `.then()` chain in [promises.md](promises.md): `async`/`await`
lets asynchronous code read almost identically to synchronous code — no chained `.then()` calls,
no nested callbacks, just sequential statements.

## The Rules

- **`async`** marks a function as returning a Promise automatically — even a plain `return value;`
  inside an `async` function is wrapped in a resolved Promise.
- **`await`** can only be used inside an `async` function (with one narrow exception: top-level
  `await` in a module). It pauses execution of *that function* until the awaited Promise settles,
  then unwraps its resolved value directly — without pausing the rest of the program, only that
  function's own execution.

```js
async function example() {
  return 42; // implicitly returns Promise.resolve(42)
}

example().then(value => console.log(value)); // 42
```

## Error Handling with `try`/`catch`

```js
async function loadUserData(userId) {
  try {
    const user = await getUser(userId);
    const posts = await getPosts(user.id);
    return posts;
  } catch (error) {
    console.error("Failed to load user data:", error);
    throw error; // re-throw if the caller needs to know too
  }
}
```

A rejected Promise, when awaited, throws — meaning ordinary `try`/`catch` (from
[try-catch-finally.md](../error-handling-and-debugging/try-catch-finally.md)) works directly for
handling async failures, rather than needing a separate `.catch()` mechanism.

## `async`/`await` Is Built on Promises — Not a Replacement

This is worth stating precisely: `async`/`await` doesn't introduce a new asynchronous mechanism —
it's syntax that makes working with Promises read more like synchronous code. Every `async`
function still returns a real Promise, and `Promise.all()` (see [promises.md](promises.md))
remains the correct tool for running multiple `await`s concurrently rather than sequentially:

```js
// Sequential — each waits for the previous to finish (often unnecessarily slow)
const user = await getUser(id);
const settings = await getSettings(id);

// Concurrent — both start immediately, only wait once, at the end
const [user, settings] = await Promise.all([getUser(id), getSettings(id)]);
```

## Common Mistakes

- Awaiting independent operations one after another sequentially, when they could run concurrently
  via `Promise.all()` — unnecessarily slowing down code with no actual dependency between the
  steps.
- Forgetting `try`/`catch` around `await`, leaving an unhandled rejection that can crash an
  otherwise-working function.
- Using `await` outside an `async` function (outside the narrow top-level-await-in-a-module
  exception), which is a syntax error.

## Next

Continue to [fetch-api.md](fetch-api.md) to see `async`/`await` applied to the most common
real-world asynchronous operation: making a network request.
