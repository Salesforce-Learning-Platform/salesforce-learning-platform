# Scope

## What Scope Means

**Scope** determines where a variable is accessible. JavaScript uses **lexical scope**: a
variable's accessibility is determined by *where it's written* in the source code, not by how or
from where a function is later called.

## The Scope Chain

When code references a variable, JavaScript looks for it in the current scope first, then walks
outward through each enclosing scope until it finds it (or reaches the global scope and throws a
`ReferenceError` if it's nowhere to be found):

```js
const globalVar = "global";

function outer() {
  const outerVar = "outer";

  function inner() {
    const innerVar = "inner";
    console.log(innerVar);   // found in inner's own scope
    console.log(outerVar);   // found by walking up to outer's scope
    console.log(globalVar);  // found by walking up to global scope
  }

  inner();
}
```

This outward-searching chain is the **scope chain** — and it only goes outward. `outer()` cannot
access `innerVar`; a function's inner scope is never visible to its enclosing scope.

## Block Scope vs. Function Scope, Revisited

As introduced in
[variables.md](../introduction-to-javascript/variables.md), `let`/`const` are block-scoped (`{ }`
boundaries), while `var` is function-scoped. This matters directly for scope chains — a `let`
declared inside an `if` block is invisible immediately outside that block, even within the same
function.

## Global Scope — Use Sparingly

Any variable declared outside every function or block lives in the **global scope**, accessible
from anywhere in the program. Relying heavily on global variables makes code harder to reason
about (any part of the program could modify a global value, unpredictably affecting other,
seemingly unrelated code) — keeping variables as narrowly scoped as possible (inside the function
or block that actually needs them) is a core practice for maintainable code.

## Common Mistakes

- Assuming scope is determined by *call* location rather than *definition* location — lexical
  scope means what a function can see is fixed by where it's written, regardless of where it's
  eventually invoked from.
- Overusing global variables for convenience, creating implicit, hard-to-trace dependencies
  between unrelated parts of a program.
- Forgetting that inner scopes can shadow (reuse the same name as) an outer variable, which can
  make code read as though it refers to one variable when it actually refers to a different, more
  local one.

## Next

Continue to [closures.md](closures.md) to see what happens when an inner function is allowed to
outlive the outer scope it was defined in.
