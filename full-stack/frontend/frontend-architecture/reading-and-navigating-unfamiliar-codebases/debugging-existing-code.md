# Debugging Existing Code

## `console.log` Is a Start, Not a Strategy

```js
function calculateTotal(items) {
  console.log("items:", items); // where does this actually get printed,
                                 // and does it even run before the bug?
  return items.reduce((sum, item) => sum + item.price * item.qty, 0);
}
```

Scattering `console.log` calls is a reasonable first probe, but it only tells you a value *at one
point in time* — it can't show you the full call stack, doesn't let you pause and inspect further,
and requires editing (and later removing) the actual source code. For anything beyond a trivial
bug, the browser's own debugger is a far more precise tool.

## Setting a Breakpoint

```js
function calculateTotal(items) {
  debugger; // execution pauses here the instant this line runs, exactly
            // like clicking a line number in DevTools' Sources panel
  return items.reduce((sum, item) => sum + item.price * item.qty, 0);
}
```

A **breakpoint** — set either by clicking a line number in the browser DevTools' Sources panel, or
by writing a literal `debugger;` statement — pauses JavaScript execution at that exact line,
letting you inspect the real, live values of every variable in scope at that moment, rather than
guessing from a printed log line what they might have been. From there you can **step through**
execution line by line (step over, step into, step out) and watch exactly how each value changes.

## Conditional Breakpoints for Loops and Repeated Calls

```
# Right-click the line number → "Add conditional breakpoint"
item.id === "sku-4471"
```

A plain breakpoint inside a loop or a frequently-called function pauses on *every* iteration or
call — tedious when you only care about one specific case. A **conditional breakpoint** only pauses
when the condition you specify is true, letting you jump straight to the one call that actually
matters (e.g., only the item whose total is coming out wrong).

## Source Maps — Debugging the Code You Actually Wrote

Real production and even development builds are usually bundled and often transpiled or minified —
the code actually running in the browser rarely looks like the source files in the repository. A
**source map** is a generated file that maps positions in that transformed, bundled code back to
the original source files and line numbers. With source maps enabled (the default in most modern
dev tooling), DevTools' Sources panel shows and lets you set breakpoints in your *actual* source
files — the ones you'd read in the editor — rather than an unreadable bundled output.

## A Practical Debugging Workflow for Unfamiliar Code

1. Use [tracing-data-flow.md](tracing-data-flow.md)'s backward-tracing to form a hypothesis about
   roughly where the bug likely originates.
2. Set a breakpoint at that point (or a conditional one, if it's inside a loop or repeated call).
3. Reproduce the bug in the browser and let execution pause there.
4. Inspect the actual live variable values — confirm or reject the hypothesis directly, rather than
   continuing to guess.
5. If the values are correct at this point, the bug is further downstream (or the hypothesis was
   wrong); if they're already wrong here, step backward again, repeating from step 2 one layer
   further up the data flow.

## Common Mistakes

- Relying entirely on scattered `console.log` calls for a non-trivial bug, when a breakpoint would
  show the same information — plus the full call stack and every other variable in scope — without
  needing to edit and later clean up the source code.
- Debugging directly against minified or bundled production output because source maps weren't
  enabled or weren't available, making even simple bugs much harder to trace than necessary.
- Setting a plain (non-conditional) breakpoint inside a loop that runs hundreds of times, then
  manually clicking "resume" repeatedly instead of using a conditional breakpoint to jump straight
  to the relevant iteration.

## Module Summary

Across this module: understanding an unfamiliar project starts from the outside in — its README,
`package.json`, and its framework's own folder conventions — before reading any single file's logic
in detail (see
[understanding-project-structure.md](understanding-project-structure.md)); **entry points** are
where execution and the UI genuinely begin, at both the app level and the feature level, and
following them is faster than reading files in an arbitrary order (see
[identifying-entry-points.md](identifying-entry-points.md)); **tracing data flow** backward — from
what's rendered, through props, into state, and back to its real source — is the reliable way to
find where a value actually goes wrong (see [tracing-data-flow.md](tracing-data-flow.md)); and
browser DevTools breakpoints, conditional breakpoints, and source maps let you verify a hypothesis
about existing code directly, with real live values, instead of guessing from scattered
`console.log` output.
