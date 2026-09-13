# Function Declarations and Expressions

## Function Declaration

```js
function greet(name) {
  return `Hello, ${name}`;
}
```

A named function defined as its own statement. Function declarations are **fully hoisted** — both
the name and the complete function body are available anywhere in their enclosing scope, even
before the declaration's line in the source:

```js
console.log(greet("Ada")); // works — hoisted before this line runs
function greet(name) { return `Hello, ${name}`; }
```

## Function Expression

```js
const greet = function (name) {
  return `Hello, ${name}`;
};
```

A function assigned to a variable, treated as a value. Unlike a declaration, a function expression
is only available once its assignment line actually executes — calling it earlier throws a
`ReferenceError` (for `const`/`let`) because the variable exists but hasn't been initialized yet.

```js
console.log(greet("Ada")); // ReferenceError — greet not yet assigned
const greet = function (name) { return `Hello, ${name}`; };
```

## Named vs. Anonymous Function Expressions

```js
const greet = function sayHello(name) { return `Hello, ${name}`; }; // named
const greet2 = function (name) { return `Hello, ${name}`; };         // anonymous
```

A named function expression's internal name (`sayHello`) is only accessible *inside its own body*
(useful for self-referential recursion) — outside, the function is still only reachable via the
variable it was assigned to (`greet`).

## Choosing Between Them

| | Declaration | Expression |
|---|---|---|
| Hoisted (usable before its line)? | Yes | No |
| Common use | Top-level, general-purpose functions | Assigning to a variable, passing as a callback, conditional definition |

Neither is strictly "better" — declarations are convenient for a function meant to be broadly
available throughout a file; expressions are necessary when a function needs to be defined
conditionally, passed directly as an argument, or assigned based on some other runtime logic.

## Common Mistakes

- Relying on hoisting for a function declaration defined far below where it's called, which works
  but can make code harder to read top-to-bottom.
- Assuming a function expression is hoisted the same way a declaration is, and being surprised by
  a `ReferenceError` when calling it too early.
- Overusing named function expressions when the name provides no real benefit — the
  variable name alone is usually sufficient outside of self-referential recursion.

## Next

Continue to [arrow-functions.md](arrow-functions.md) for the more concise modern syntax.
