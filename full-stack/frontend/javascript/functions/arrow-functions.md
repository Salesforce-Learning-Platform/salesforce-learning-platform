# Arrow Functions

## Syntax

```js
const add = (a, b) => a + b;              // implicit return, single expression
const square = x => x * x;                 // parentheses optional for exactly one parameter
const greet = name => { return `Hi ${name}`; }; // explicit return needed with a block body
const noop = () => {};                       // no parameters
```

Arrow functions offer a shorter syntax than `function` expressions, and — for a single expression
body with no curly braces — implicitly return that expression's value with no explicit `return`
needed.

## The Real Difference: Lexical `this`

The most important distinction isn't the shorter syntax — it's that arrow functions **do not have
their own `this`**. They capture `this` from their surrounding (lexical) scope at the point they're
defined, rather than depending on how they're called:

```js
class Timer {
  constructor() {
    this.seconds = 0;
    setInterval(() => {
      this.seconds++; // `this` refers to the Timer instance, as expected
    }, 1000);
  }
}
```

A regular `function` used in the same spot would have its own `this`, determined by how
`setInterval` calls it — typically `undefined` or the global object in that context, not the
`Timer` instance, which is a common, genuinely confusing source of bugs before arrow functions
existed.

## When Not to Use an Arrow Function

Because arrow functions don't bind their own `this`, they're the wrong choice for:

- **Object methods** that need to refer to the object itself via `this`.
- **Constructor functions** — arrow functions cannot be used with `new` at all.

```js
const obj = {
  value: 42,
  getValue: () => this.value, // wrong — `this` here is NOT `obj`
  getValueCorrect() { return this.value; } // correct — regular method syntax
};
```

## Common Mistakes

- Using an arrow function for an object method and being confused when `this` doesn't refer to the
  object as expected.
- Forgetting that an arrow function with a block body (`{ }`) needs an explicit `return` — omitting
  it (unlike the single-expression form) simply returns `undefined`.
- Assuming arrow functions are just "shorter regular functions" and missing the `this`-binding
  difference, which is the actual reason they exist as a distinct feature.

## Next

Continue to
[parameters-and-return-values.md](parameters-and-return-values.md) for the details of how
arguments and return values actually work.
