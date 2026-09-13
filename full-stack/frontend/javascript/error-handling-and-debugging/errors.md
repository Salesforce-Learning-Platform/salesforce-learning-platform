# Errors

## Built-In Error Types

JavaScript throws different error types depending on what went wrong, which is a genuinely useful
diagnostic signal before even reading the message:

| Error type | Typically means |
|---|---|
| `ReferenceError` | Code referenced a variable that doesn't exist |
| `TypeError` | A value exists, but an operation isn't valid for its actual type (calling a non-function, reading a property of `undefined`) |
| `SyntaxError` | Malformed code — usually caught before the code even runs |
| `RangeError` | A value is outside an allowed range (an invalid array length, for instance) |

```js
undeclaredVariable;        // ReferenceError: undeclaredVariable is not defined
null.property;              // TypeError: Cannot read properties of null
new Array(-1);                // RangeError: Invalid array length
```

## Throwing Custom Errors

```js
function withdraw(balance, amount) {
  if (amount > balance) {
    throw new Error("Insufficient funds");
  }
  return balance - amount;
}
```

`throw` immediately stops normal execution and propagates the error up the call stack until
something catches it (see [try-catch-finally.md](try-catch-finally.md)) — or, if nothing does, the
program crashes (in Node) or the browser logs an uncaught error to the console.

## Custom Error Classes

```js
class InsufficientFundsError extends Error {
  constructor(message) {
    super(message);
    this.name = "InsufficientFundsError";
  }
}

throw new InsufficientFundsError("Insufficient funds");
```

Extending the built-in `Error` class creates a distinct, identifiable error type — useful when
different kinds of failure need different handling, since a `catch` block can check
`error instanceof InsufficientFundsError` to react specifically, rather than parsing a generic
error's message string to guess what went wrong.

## The `Error` Object's Useful Properties

```js
try {
  throw new Error("Something failed");
} catch (error) {
  error.message; // "Something failed"
  error.name;      // "Error" (or the custom class name, if extended)
  error.stack;      // a full stack trace — invaluable for debugging where the error originated
}
```

`error.stack` is non-standard but supported everywhere in practice, and is frequently the single
most useful piece of information for locating the actual source of a failure, especially in
production error logs where you can't attach a live debugger.

## Common Mistakes

- Throwing a plain string (`throw "failed"`) instead of an `Error` object — this loses the useful
  `stack` property and other `Error`-specific behavior that tooling generally expects.
- Writing generic error messages ("something went wrong") that give no indication of what actually
  failed or why, making the eventual `catch` block far less useful.
- Ignoring the specific error type/class in a `catch` block and treating every possible failure
  identically, when different failures often warrant genuinely different handling.

## Next

Continue to [try-catch-finally.md](try-catch-finally.md) for actually catching and responding to
these errors.
