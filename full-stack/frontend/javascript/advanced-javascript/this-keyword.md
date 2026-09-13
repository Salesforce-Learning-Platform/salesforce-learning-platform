# The `this` Keyword

## The Core Rule: `this` Depends on How a Function Is Called

Unlike a variable resolved through lexical scope (see
[scope.md](../functions/scope.md)), `this` is determined dynamically, based on **how a function is
invoked** — not where it's defined. The same function can have a completely different `this` on
two different calls.

## The Four Binding Rules

**1. Default binding** — calling a plain function with no context:

```js
function show() { console.log(this); }
show(); // undefined (strict mode) or the global object (non-strict)
```

**2. Implicit binding** — calling a method on an object:

```js
const user = {
  name: "Ada",
  greet() { return `Hello, ${this.name}`; },
};
user.greet(); // "Hello, Ada" — `this` is `user`, the object before the dot
```

**3. Explicit binding** — forcing a specific `this` with `call`, `apply`, or `bind`:

```js
function greet() { return `Hello, ${this.name}`; }
const user = { name: "Ada" };

greet.call(user);              // "Hello, Ada" — calls immediately with `this` set to `user`
greet.apply(user, []);          // same as call, but arguments passed as an array
const bound = greet.bind(user);  // returns a NEW function permanently bound to `user`
bound();                          // "Hello, Ada"
```

**4. Lexical binding** — arrow functions, which ignore all of the above and instead capture `this`
from their surrounding scope at the time they're defined (see
[arrow-functions.md](../functions/arrow-functions.md)).

## Losing `this` — A Classic, Recurring Bug

```js
const user = {
  name: "Ada",
  greet() { return `Hello, ${this.name}`; },
};

const detached = user.greet;
detached(); // "Hello, undefined" — this is now the DEFAULT binding, not `user`
```

`user.greet` extracted the function itself, disconnected from the object it was called on — when
called as a bare `detached()`, the implicit binding rule no longer applies (there's no object
before the dot), and it falls back to default binding instead. This exact pattern is why passing
`this.handleClick` directly as a callback (common in earlier, pre-arrow-function React class
components) required explicit `.bind(this)` to work correctly.

## Precedence Between the Rules

When more than one rule could apply, explicit binding (`call`/`apply`/`bind`) wins over implicit
binding (a method call), which wins over default binding. Arrow functions ignore this precedence
order entirely, since they never look at how they were called in the first place.

## Common Mistakes

- Passing an object method as a bare callback (`element.addEventListener("click", obj.method)`)
  and being surprised `this` inside it no longer refers to `obj`.
- Forgetting that `bind()` returns a **new** function rather than modifying the original — the
  original function's `this` behavior is unaffected by calling `.bind()` on it.
- Using a regular `function` where an arrow function's lexical `this` was actually needed (or vice
  versa) — revisit [arrow-functions.md](../functions/arrow-functions.md) for exactly this
  distinction.

## Next

Continue to [prototypes.md](prototypes.md) to see the mechanism underneath object method lookup
itself.
