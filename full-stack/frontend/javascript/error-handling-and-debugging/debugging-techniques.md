# Debugging Techniques

## Beyond `console.log`

`console.log` is a reasonable first step, but it requires guessing in advance what to log, and
re-running the code after every guess. Browser DevTools' Sources panel (see
[browser-devtools-essentials.md](../../foundations/preparing-your-machine/browser-devtools-essentials.md))
provides a genuinely more powerful tool: the **debugger**, which pauses execution and lets you
inspect the *actual* live state at that exact moment.

## Setting Breakpoints

In the Sources panel, clicking a line number sets a **breakpoint** — execution pauses right before
that line runs, with every variable in scope inspectable exactly as it exists at that moment,
rather than only whatever you thought to log beforehand.

```js
function calculateTotal(items) {
  let total = 0;
  for (const item of items) {
    total += item.price; // set a breakpoint here to inspect `item` and `total` each iteration
  }
  return total;
}
```

## The `debugger` Statement

```js
function calculateTotal(items) {
  debugger; // pauses execution here automatically, same as a manual breakpoint
  // ...
}
```

Placing `debugger;` directly in code has the same effect as manually setting a breakpoint in
DevTools, but travels with the source — useful when you know in advance exactly where you want
execution to pause, without needing to locate that line in the Sources panel first.

## Stepping Through Execution

Once paused, DevTools provides controls to move through code deliberately:

| Action | Effect |
|---|---|
| Step over | Run the current line, don't enter any function it calls |
| Step into | Enter the function being called on the current line |
| Step out | Finish the current function and return to its caller |
| Resume | Continue running normally until the next breakpoint |

## Reading a Stack Trace

When an error is thrown, its `stack` property (see [errors.md](errors.md)) — also shown directly
in the console for an uncaught error — lists the chain of function calls that led to it, most
recent first. Reading from the top down shows exactly where the error was thrown and the path of
calls that got there, which is usually far faster than guessing based on symptoms alone.

## A Systematic Approach

1. Reproduce the issue reliably before attempting to fix it — a fix for a bug you can't
   consistently reproduce is a guess, not a verified fix.
2. Set a breakpoint at the earliest point you suspect something goes wrong.
3. Step through and inspect actual values, narrowing down exactly where behavior diverges from
   what's expected.
4. Once the root cause is located, fix it and verify the original reproduction steps no longer
   trigger the bug.

## Common Mistakes

- Adding more and more `console.log` statements as a bug becomes harder to trace, instead of
  switching to a breakpoint that shows everything in scope at once.
- Guessing at a fix without first reliably reproducing the actual problem, risking a "fix" that
  doesn't address the real cause.
- Ignoring a stack trace's actual content and re-reading the same code repeatedly instead, when
  the trace often points directly at the failure's origin.

## Module Summary

Across this module: JavaScript's built-in error types (`TypeError`, `ReferenceError`, etc.) are a
diagnostic signal worth reading carefully, and custom `Error` subclasses let different failures be
handled distinctly (see [errors.md](errors.md)); `try`/`catch`/`finally` handles genuinely
exceptional failures, with `finally` guaranteed to run regardless of outcome — but isn't a
replacement for ordinary conditional logic (see
[try-catch-finally.md](try-catch-finally.md)); and breakpoints and the debugger statement let you
inspect a program's actual live state at a precise moment, which is typically far faster than
iteratively guessing with `console.log`.
