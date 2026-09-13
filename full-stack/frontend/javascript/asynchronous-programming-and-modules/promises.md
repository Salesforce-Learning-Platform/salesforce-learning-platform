# Promises

## What a Promise Represents

A **Promise** is an object representing the eventual result of an asynchronous operation — it
exists in one of three states:

| State | Meaning |
|---|---|
| `pending` | Not yet resolved or rejected — still in progress |
| `fulfilled` | Completed successfully, with a resulting value |
| `rejected` | Failed, with a reason (usually an `Error`) |

Once a Promise settles (fulfilled or rejected), it stays that way permanently — it can never
change state again.

## `.then()` and `.catch()`

```js
getUser(userId)
  .then(user => getPosts(user.id))
  .then(posts => getComments(posts[0].id))
  .then(comments => console.log(comments))
  .catch(error => console.error("Something failed:", error));
```

Compare this directly to the nested callback version in [callbacks.md](callbacks.md): each `.then()`
receives the previous step's resolved value and returns a new Promise, allowing the chain to
continue flatly instead of nesting — and a single `.catch()` at the end handles a failure from
**any** step in the chain, rather than needing separate error handling at every level.

## Creating a Promise

```js
function delay(ms) {
  return new Promise((resolve, reject) => {
    setTimeout(() => resolve(`Waited ${ms}ms`), ms);
  });
}

delay(1000).then(message => console.log(message));
```

The `Promise` constructor takes a function receiving `resolve` and `reject` — calling `resolve(value)`
fulfills the Promise with that value; calling `reject(error)` rejects it.

## Combining Multiple Promises

```js
Promise.all([fetchUser(), fetchPosts(), fetchComments()])
  .then(([user, posts, comments]) => {
    // runs only once ALL three have resolved
  });
```

| Method | Behavior |
|---|---|
| `Promise.all()` | Resolves when all succeed; rejects immediately if any one fails |
| `Promise.allSettled()` | Waits for all to finish regardless of success/failure, reporting each outcome |
| `Promise.race()` | Settles as soon as the first Promise settles, whichever it is |

`Promise.all()` is appropriate when every result is required and any single failure should abort
the whole operation; `Promise.allSettled()` is appropriate when partial results are still useful
even if some individual operations fail.

## Common Mistakes

- Forgetting a `.catch()` entirely, leaving a rejected Promise unhandled — this produces a
  genuinely unhandled rejection, visible as a console warning/error rather than being silently
  ignored.
- Nesting `.then()` calls inside each other rather than chaining them flatly, recreating the exact
  callback-nesting problem Promises exist to solve.
- Using `Promise.all()` when partial results should still be usable even if one operation fails —
  `Promise.allSettled()` is the correct tool for that case.

## Next

Continue to [async-await.md](async-await.md) for the more readable modern syntax built directly on
top of Promises.
