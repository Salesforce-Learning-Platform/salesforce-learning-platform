# Try, Catch, Finally

## Basic Structure

```js
try {
  const data = JSON.parse(userInput); // might throw if userInput isn't valid JSON
  console.log(data);
} catch (error) {
  console.error("Failed to parse input:", error.message);
} finally {
  console.log("Parsing attempt finished");
}
```

- **`try`**: code that might throw an error.
- **`catch`**: runs only if the `try` block throws — receives the thrown error as its parameter.
- **`finally`**: runs **always** — whether the `try` block succeeded, threw an error, or even hit a
  `return` statement early.

## What `finally` Actually Guarantees

```js
function example() {
  try {
    return "from try";
  } finally {
    console.log("finally still runs");
  }
}
```

Even though `try` returns immediately, `finally` still runs before the function actually returns.
This guarantee is exactly why `finally` is the correct place for cleanup that must always happen
regardless of outcome — closing a network connection, hiding a loading indicator, releasing a
resource — rather than duplicating that cleanup code in both the success and failure paths.

## When `try`/`catch` Is (and Isn't) the Right Tool

`try`/`catch` is for **exceptional, unexpected failures** — a network request failing, malformed
data, an operation that genuinely shouldn't normally fail. It's not the right tool for **expected,
routine conditions** that should be handled with an ordinary `if` check instead:

```js
// Overkill — this isn't an "exceptional" case
try {
  if (!user) throw new Error("no user");
  greet(user);
} catch { /* ... */ }

// Better — an ordinary, expected condition
if (user) {
  greet(user);
}
```

## Catching Specific Error Types

```js
try {
  riskyOperation();
} catch (error) {
  if (error instanceof TypeError) {
    // handle this specific case
  } else {
    throw error; // re-throw anything we don't know how to handle
  }
}
```

Re-throwing an error a `catch` block doesn't actually know how to handle is a deliberate,
important pattern — it prevents silently swallowing genuinely unexpected failures under the guise
of "handling" them, letting them propagate to somewhere that can actually deal with them (or
surface visibly, rather than failing silently).

## Common Mistakes

- Wrapping ordinary, expected conditional logic in `try`/`catch` when a plain `if` check is the
  simpler, more appropriate tool.
- Catching an error and doing nothing with it (an empty `catch` block), silently hiding failures
  that should have been visible somewhere.
- Forgetting that `finally` runs even after a `return` inside `try`, and accidentally relying on
  code after the `try`/`catch`/`finally` block that a `return` inside it actually skips.

## Next

Continue to [debugging-techniques.md](debugging-techniques.md) for systematically diagnosing
issues beyond `console.log`.
