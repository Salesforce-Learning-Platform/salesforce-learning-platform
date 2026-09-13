# Constructors

## A Constructor Function

```js
function User(name, email) {
  this.name = name;
  this.email = email;
}

const ada = new User("Ada", "ada@example.com");
```

A **constructor function** is an ordinary function, called with the `new` keyword, used as a
template for creating multiple similar objects — by convention, capitalized to visually
distinguish it from a regular function.

## What `new` Actually Does

Calling a function with `new` performs four steps automatically, behind the scenes:

1. Creates a brand-new, empty object.
2. Sets that new object as `this` inside the function body.
3. Links the new object's internal prototype to the constructor function's `.prototype` property
   (covered in [advanced-javascript/prototypes.md](../advanced-javascript/prototypes.md)).
4. Returns the new object automatically — unless the constructor explicitly returns a different
   object itself, which is unusual and generally avoided.

```js
function User(name) {
  // `new` has already created an empty object and set it as `this`, before this line runs
  this.name = name;
  // `new` will return `this` automatically once the function finishes
}
```

## Calling a Constructor Without `new` — A Real Bug Source

```js
const broken = User("Ada"); // forgot `new`!
```

Without `new`, `this` inside the function doesn't refer to a new object at all — in non-strict
mode, it can silently refer to the global object, meaning `this.name = "Ada"` sets a *global*
`name` property instead of creating a proper `User` object, and `broken` ends up `undefined` (since
nothing was explicitly returned). This is a real, historically common bug — one of several reasons
modern `class` syntax (see
[classes-and-inheritance.md](classes-and-inheritance.md)) is now generally preferred: JavaScript
throws an explicit error if a class is called without `new`, rather than silently misbehaving.

## Adding Shared Methods via the Prototype

```js
function User(name) { this.name = name; }

User.prototype.greet = function () {
  return `Hello, ${this.name}`;
};

const ada = new User("Ada");
ada.greet(); // "Hello, Ada"
```

Defining `greet` directly inside the constructor would create a brand-new function for *every*
single instance created; defining it once on `User.prototype` means every instance shares the
exact same function, which is both more memory-efficient and the traditional way methods were
attached before `class` syntax existed to do this implicitly.

## Common Mistakes

- Forgetting `new` when calling a constructor function, silently corrupting global state instead
  of raising a clear, immediate error.
- Defining methods directly on `this` inside the constructor rather than on `.prototype`,
  needlessly duplicating the same function across every instance.
- Not capitalizing constructor function names, making it harder for readers to distinguish a
  constructor (meant to be called with `new`) from an ordinary function at a glance.

## Next

Continue to [classes-and-inheritance.md](classes-and-inheritance.md) for the modern syntax that
addresses these exact rough edges.
