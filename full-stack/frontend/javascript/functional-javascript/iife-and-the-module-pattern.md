# 📦 IIFEs and the Module Pattern

## Closures as an Encapsulation Tool

Before ES modules, `let`/`const`, and class private fields existed, JavaScript had one tool for
keeping variables out of the global scope and away from other code: a function's own scope. An
**immediately invoked function expression (IIFE)** is a function that is created and called in the
same breath, so its variables exist only inside it. Combined with a [closure](../functions/closures.md),
it yields the **module pattern**: private state with a controlled public interface. You will meet
both in older codebases, bundler output, and interviews — and the underlying idea remains useful.

## ▶️ What an IIFE Is

```js
(function () {
  console.log("runs now");
})();

(() => {
  console.log("arrow IIFE");
})();
```

MDN describes an IIFE as a function expression, enclosed in parentheses, that is invoked
immediately. The parentheses are not decoration: without them the parser reads `function` at the
start of a statement as a *declaration*, which requires a name and cannot be called on the spot:

```js
function () { console.log("x"); }();
// SyntaxError: Function statements require a function name
```

Wrapping the function in parentheses forces the parser to treat it as an expression (see
[execution-contexts-and-the-scope-chain.md](../execution-context-and-hoisting/execution-contexts-and-the-scope-chain.md)
for how declarations and expressions differ at set-up time).

## 🎯 What IIFEs Are Used For

MDN lists three main uses, each of which still appears today:

- **Avoiding global pollution** — wrapping a script so its variables stay local. (Largely replaced
  by block-scoped `let`/`const` and ES modules.)
- **Computing a value with several statements** — an IIFE is an *expression*, so it can initialize
  a `const` with logic that needs temporary variables:

```js
const mode = (() => {
  const hour = 20;
  return hour >= 18 ? "dark" : "light";
})();

console.log(mode);   // dark
```

- **Creating an async context** — `await` is only valid inside an `async` function or at the top
  level of a module, so in a classic script an async IIFE provides the context:

```js
await Promise.resolve(1);
// SyntaxError: await is only valid in async functions and the top level bodies of modules

(async () => {
  const value = await Promise.resolve(7);
  console.log(value);   // 7
})();
```

## 🧰 The Module Pattern: Private State, Public API

Returning an object of functions from an IIFE gives you private variables (captured by the closure)
and a public interface (the returned object):

```js
const cart = (function () {
  const items = [];                                   // private: no outside access

  return {                                             // public API
    add(name, price) {
      items.push({ name, price });
    },
    total() {
      return items.reduce((sum, item) => sum + item.price, 0);
    },
    list() {
      return items.map((item) => ({ ...item }));       // hand out COPIES, not the private objects
    },
  };
})();

cart.add("Book", 12);
cart.add("Pen", 3);
console.log(cart.total());   // 15

cart.list()[0].price = 0;    // modifies a copy only
console.log(cart.total());   // 15
console.log(cart.items);     // undefined — the array is not reachable from outside
```

Three properties make this work:

1. **`items` lives in the IIFE's scope** — nothing outside can name it.
2. **The returned methods close over it**, so they can use it for as long as the cart exists.
3. **`list()` returns copies.** Returning `items` itself would leak a live reference and let callers
   mutate private state — a very common way for this pattern to leak.

The **revealing module pattern** is a naming convention of the same idea: define every function
privately, then return an object that "reveals" only the chosen ones.

## 🔄 Modern Equivalents

| Goal | Today's tool |
|------|--------------|
| Keep variables out of the global scope | ES modules — each file has its own scope; see [javascript-modules.md](../asynchronous-programming-and-modules/javascript-modules.md) |
| Private state with a public interface | A class with `#private` fields |
| A temporary scope | A block `{ }` with `let`/`const` |

The same cart as a class, with a truly private field:

```js
class Cart {
  #items = [];

  add(name, price) {
    this.#items.push({ name, price });
  }

  total() {
    return this.#items.reduce((sum, item) => sum + item.price, 0);
  }
}

const c = new Cart();
c.add("Book", 12);
c.add("Pen", 3);
console.log(c.total());   // 15
console.log(c.items);     // undefined
// c.#items               // SyntaxError: Private field '#items' must be declared in an enclosing class
```

Private fields enforce privacy in the language itself and are covered in the Objects in Depth
module, later in this section. Prefer them (or modules) for new code; understanding IIFEs and the
module pattern remains valuable for reading existing code and for grasping what closures make
possible.

## ⚠️ The Semicolon Trap

An IIFE starts with `(`, which can continue the previous line if that line lacks a semicolon:

```js
const config = {}
(function () { console.log("setup"); })()
// TypeError: {} is not a function
```

This is one of the classic automatic semicolon insertion failures — see
[automatic-semicolon-insertion.md](../execution-context-and-hoisting/automatic-semicolon-insertion.md).
End the previous statement with `;`, or (in a semicolon-less style) begin the IIFE line with `;`.

## 🎤 Interview Angle

- **"What is an IIFE and why would you use one?"** A function expression invoked immediately, to
  create a private scope — avoiding global variables, computing a value with temporary variables, or
  providing an async context.
- **"How could you create private variables before classes had `#private` fields?"** With a
  closure: keep the variable inside a function's scope and expose only functions that use it — the
  module pattern.
- **"Why are the parentheses around the function required?"** They make the parser treat `function`
  as an expression rather than a declaration, which cannot be invoked immediately.

## Common Mistakes

- **Forgetting the trailing `()`**, which defines the function but never runs it.
- **Starting an IIFE after a statement with no semicolon**, so the `(` is read as a call.
- **Returning the private array or object itself** from the public API, leaking mutable state.
- **Reaching for an IIFE out of habit** where a block, a `const`, or a module would be clearer.

## Module Summary

Across this module: **higher-order functions** take or return functions, which is possible because
functions are first-class values, and wrappers like `withLogging` and `once` build new behavior
without editing the original (see [higher-order-functions.md](higher-order-functions.md));
**`call`, `apply`, and `bind`** control `this` and arguments, with `bind` producing a permanently
bound new function (see [call-apply-and-bind.md](call-apply-and-bind.md)); **currying and partial
application** build specialized functions by supplying arguments in stages, with the `fn.length`
caveat for optional parameters (see
[currying-and-partial-application.md](currying-and-partial-application.md)); **composition**
chains small single-argument functions with `compose` and `pipe` (see
[function-composition-and-pipelines.md](function-composition-and-pipelines.md)); **pure functions
and immutability** — same inputs, same output, no side effects, updates by replacement — are what
make composition and caching safe (see
[pure-functions-and-immutability.md](pure-functions-and-immutability.md)); **memoization** caches
pure functions' results, with careful cache keys and bounded size (see
[memoization.md](memoization.md)); and **IIFEs and the module pattern** use closures to create
private state, a technique now largely served by modules and `#private` fields (see this file).

## ➡️ Next

Continue to the Objects in Depth module, the next module in this section, which examines property
descriptors, freezing, copying, JSON, private fields, and `Proxy`.
