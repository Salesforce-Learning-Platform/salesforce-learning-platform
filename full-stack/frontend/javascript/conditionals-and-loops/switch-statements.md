# Switch Statements

## Basic Syntax

```js
switch (day) {
  case "Mon":
  case "Tue":
  case "Wed":
  case "Thu":
  case "Fri":
    console.log("Weekday");
    break;
  case "Sat":
  case "Sun":
    console.log("Weekend");
    break;
  default:
    console.log("Not a valid day");
}
```

`switch` compares one value against a series of exact matches (`case` clauses) using strict
equality (`===`, no coercion) — a cleaner alternative to a long `if`/`else if` chain when every
branch is checking the *same* value against different exact possibilities.

## Fall-Through — Real Behavior, Not a Bug

Without an explicit `break`, execution **falls through** to the next `case`, running its code
regardless of whether that case's own condition matches:

```js
switch (x) {
  case 1:
    console.log("one");
    // no break — falls through
  case 2:
    console.log("two");
    break;
}
// x === 1 logs BOTH "one" and "two"
```

This is a real, specification-defined behavior — sometimes deliberately used (as in the weekday
example above, where several `case`s intentionally share one block by "falling through" with no
code between them), but far more often an accidental bug when a `break` is simply forgotten.

## The `default` Case

`default` runs when no `case` matches — it doesn't have to be the last clause positionally, but
placing it last is the near-universal convention, since that's where a reader expects to find the
fallback behavior.

## Common Mistakes

- Forgetting `break` at the end of a case, causing unintended fall-through into the next case's
  code.
- Reaching for `switch` when the branches are actually checking different, unrelated conditions
  (not the same single value) — `if`/`else if` is the correct tool for that, since `switch` only
  compares one value against exact matches.
- Assuming `switch` uses loose equality like `==` — it uses strict comparison, the same as `===`.

## Next

Continue to [loops.md](loops.md) for repeating work rather than branching once.
