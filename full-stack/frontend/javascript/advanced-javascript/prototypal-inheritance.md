# Prototypal Inheritance

## Inheritance Without `class`

`class`/`extends` (see
[classes-and-inheritance.md](../object-oriented-programming/classes-and-inheritance.md)) is the
modern, recommended syntax — but understanding what it actually does requires seeing the same
inheritance built directly with `Object.create()` and prototypes, which is JavaScript's genuinely
native mechanism.

```js
const animal = {
  eat() { return `${this.name} is eating`; },
};

const dog = Object.create(animal); // dog's prototype is `animal`
dog.name = "Rex";
dog.bark = function () { return `${this.name} says woof`; };

dog.eat();  // "Rex is eating" — inherited from `animal`
dog.bark(); // "Rex says woof" — defined directly on `dog`
```

`Object.create(proto)` creates a brand-new object whose prototype is set directly to `proto` — this
is the single most direct way to establish a prototype link, without a constructor function or
`class` involved at all.

## Building a Deeper Chain

```js
const animal = { eat() { return "eating"; } };
const dog = Object.create(animal);
dog.bark = function () { return "woof"; };

const puppy = Object.create(dog);
puppy.play = function () { return "playing"; };

puppy.play(); // own property
puppy.bark();  // inherited from `dog`
puppy.eat();    // inherited from `dog`'s own prototype, `animal`
```

Each `Object.create()` call adds one more link in the chain — `puppy` → `dog` → `animal` →
`Object.prototype` → `null`, exactly matching the chain-walking lookup process from
[prototypes.md](prototypes.md).

## Why This Matters, Given `class` Exists

You'll rarely write `Object.create()`-based inheritance directly in modern code — `class` is
clearer for the vast majority of cases. But understanding this underlying mechanism explains real,
observable behaviors of `class` that would otherwise seem arbitrary: why methods defined in a
class body are shared across all instances (they're placed on the prototype, exactly like
`Dog.prototype.bark = ...` from [constructors.md](../object-oriented-programming/constructors.md)),
and why `instanceof` works the way it does (it's literally checking whether a given prototype
appears anywhere in the object's prototype chain).

## Common Mistakes

- Assuming `Object.create()`-based inheritance and `class`-based inheritance are unrelated
  mechanisms, rather than recognizing `class` as a syntax layer over exactly this.
- Building unnecessarily deep, hand-rolled prototype chains for a simple use case where a single
  `class` would be far more readable and maintainable.
- Modifying a shared prototype object after many instances already exist and being surprised every
  existing instance reflects the change — the prototype is one shared object, not copied per
  instance.

## Next

Continue to [classes.md](classes.md) to see this same mechanism from the other direction — how
`class` syntax translates directly into what's covered in this file.
