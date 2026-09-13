# Variables

## Three Declaration Keywords

```js
let count = 1;
const name = "Ada";
var legacy = "avoid this";
```

| Keyword | Scope | Reassignable? | Recommended? |
|---|---|---|---|
| `let` | Block | Yes | Yes, when the value needs to change |
| `const` | Block | No (the binding, not necessarily the contents) | Yes, as the default choice |
| `var` | Function | Yes | No — legacy, avoid in new code |

## `const` Doesn't Mean "Never Changes"

`const` prevents *reassigning* the variable itself, but does **not** make an object or array
immutable — its contents can still be changed:

```js
const user = { name: "Ada" };
user.name = "Grace"; // allowed — the object's contents changed, not the binding
user = {};           // TypeError — reassigning the const binding itself is not allowed
```

This is a frequent point of confusion: `const` is about the *variable binding*, not the *value's*
mutability.

## Block Scope vs. Function Scope

`let`/`const` are scoped to the nearest enclosing block (`{ }` — an `if`, a loop, or any bare
block); `var` is scoped to the nearest enclosing *function*, ignoring block boundaries entirely:

```js
if (true) {
  let blockScoped = "only visible in this block";
  var functionScoped = "visible in the whole function";
}
console.log(functionScoped); // works — var ignored the if-block boundary
console.log(blockScoped);    // ReferenceError — let respected the if-block boundary
```

This is the core reason `var` is avoided in modern code: block-scoping (`let`/`const`) matches how
most developers actually expect variables to behave, and prevents variables from unexpectedly
"leaking" outside the block they were declared in.

## Default to `const`

A widely followed convention: use `const` by default, and only reach for `let` when you know the
variable's value genuinely needs to be reassigned later. This makes code easier to reason about —
seeing `const` tells a reader "this value won't be reassigned" without needing to trace the rest of
the function to confirm it.

## Common Mistakes

- Using `var` out of habit (common when following outdated tutorials), missing the block-scoping
  benefits of `let`/`const`.
- Assuming `const` makes an object or array fully immutable, when it only prevents reassigning the
  variable binding itself.
- Declaring every variable with `let` "just in case," rather than defaulting to `const` and
  reaching for `let` only when reassignment is genuinely needed.

## Next

Continue to [data-types.md](data-types.md) to see what kinds of values these variables can hold.
