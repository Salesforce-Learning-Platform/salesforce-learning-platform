# Prototypes

## Every Object Has a Prototype

Every JavaScript object has an internal link to another object — its **prototype** — from which it
can inherit properties and methods. When you access a property, JavaScript doesn't just check the
object itself; if the property isn't found there, it walks up this chain of prototypes.

```js
const animal = {
  eat() { return "eating"; }
};

const dog = Object.create(animal); // dog's prototype is `animal`
dog.bark = function () { return "woof"; };

dog.bark(); // "woof" — found directly on `dog`
dog.eat();   // "eating" — NOT found on `dog`, so JavaScript checks its prototype (`animal`)
```

## The Prototype Chain

This lookup continues up the chain until the property is found, or the chain ends at `null`:

```text
dog → animal → Object.prototype → null
```

`Object.prototype` sits at the top of nearly every prototype chain, which is why every plain
object has access to methods like `.toString()` or `.hasOwnProperty()` without ever explicitly
defining them.

## `prototype` vs. `__proto__` vs. `Object.getPrototypeOf()`

This trio is a frequent source of confusion:

| | What it is |
|---|---|
| `Constructor.prototype` | A property *on a constructor function*, used to set up new instances' prototype link (see [constructors.md](../object-oriented-programming/constructors.md)) |
| `instance.__proto__` | A legacy, informal accessor to an *instance's own* prototype link — works, but discouraged |
| `Object.getPrototypeOf(instance)` | The modern, correct way to actually read an instance's prototype |

```js
function Dog() {}
const rex = new Dog();

Object.getPrototypeOf(rex) === Dog.prototype; // true
```

## Own Properties vs. Inherited Properties

```js
dog.hasOwnProperty("bark"); // true — defined directly on `dog`
dog.hasOwnProperty("eat");   // false — inherited from `animal`, not `dog`'s own property
```

`hasOwnProperty()` (or the modern `Object.hasOwn()`) distinguishes a property that genuinely
exists on the object itself from one that's only reachable via the prototype chain — a meaningful
distinction when iterating over an object's properties, since a naive `for...in` loop (see
[loops.md](../conditionals-and-loops/loops.md)) picks up inherited enumerable properties too,
unless explicitly filtered.

## Common Mistakes

- Using `__proto__` directly in new code instead of the standard `Object.getPrototypeOf()` /
  `Object.setPrototypeOf()` methods.
- Assuming a property found via `for...in` is necessarily the object's own, when it might be
  inherited from further up the prototype chain.
- Building excessively deep prototype chains, which genuinely does slow down property lookup —
  each level not found requires walking further up the chain before failing or succeeding.

## Next

Continue to
[prototypal-inheritance.md](prototypal-inheritance.md) to build inheritance directly with this
mechanism, without `class` syntax.
