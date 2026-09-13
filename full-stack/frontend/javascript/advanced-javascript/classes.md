# Classes, Revisited

## `class` Desugars to Prototypes

[classes-and-inheritance.md](../object-oriented-programming/classes-and-inheritance.md) introduced
`class` syntax practically. Now that prototypes and prototypal inheritance are covered, the exact
translation can be made explicit:

```js
// This class...
class Animal {
  constructor(name) { this.name = name; }
  eat() { return `${this.name} is eating`; }
}

// ...is roughly equivalent to this constructor-function-plus-prototype pattern:
function Animal(name) { this.name = name; }
Animal.prototype.eat = function () { return `${this.name} is eating`; };
```

Every method defined in a `class` body is placed on the class's `.prototype` automatically —
exactly the pattern from
[constructors.md](../object-oriented-programming/constructors.md), just without needing to write
`ClassName.prototype.methodName = ...` by hand for every method.

## `extends` Desugars to Prototype Chaining

```js
// This...
class Dog extends Animal {
  bark() { return "woof"; }
}

// ...sets up a prototype chain roughly equivalent to:
Object.setPrototypeOf(Dog.prototype, Animal.prototype);
```

`extends` links `Dog.prototype`'s own prototype to `Animal.prototype` — precisely the
`Object.create()`-based chain-building from
[prototypal-inheritance.md](prototypal-inheritance.md), just handled automatically by the `class`
syntax rather than written out explicitly.

## `instanceof` Checks the Prototype Chain

```js
const rex = new Dog("Rex");
rex instanceof Dog;    // true
rex instanceof Animal;  // true — Animal.prototype is in rex's prototype chain
rex instanceof Object;   // true — everything's chain eventually reaches Object.prototype
```

`instanceof` isn't magic — it's directly checking whether the right-hand side's `.prototype` object
appears anywhere in the left-hand side's prototype chain, exactly the chain-walking mechanism from
[prototypes.md](prototypes.md).

## Why Understanding This Matters, Practically

This isn't purely academic: it explains real, observable behavior — why modifying
`SomeClass.prototype.method` after instances already exist affects every existing instance
(they all share the same prototype object, not a copy); why a class's methods aren't "own
properties" of an instance (`instance.hasOwnProperty("someMethod")` is `false` — the method lives
on the prototype); and why deeply nested inheritance hierarchies have a real, if usually small,
property-lookup cost, since each level not found on an instance requires walking further up the
same chain covered in [prototypes.md](prototypes.md).

## Common Mistakes

- Treating `class` as a fundamentally different mechanism from prototypes, rather than recognizing
  it as a clearer syntax over the exact same underlying system.
- Being surprised that `instance.hasOwnProperty("methodDefinedInClass")` returns `false` — class
  methods live on the prototype, not as the instance's own properties.
- Modifying a class's prototype directly at runtime (`SomeClass.prototype.newMethod = ...`) without
  understanding this affects every existing and future instance simultaneously, since they all
  share that one prototype object.

## Module Summary

Across this module: `this` is determined by *how* a function is called, following four
precedence-ordered binding rules, with arrow functions opting out entirely via lexical binding
(see [this-keyword.md](this-keyword.md)); every object has a prototype, and property lookup walks
that chain until found or exhausted (see [prototypes.md](prototypes.md)); `Object.create()`
demonstrates this mechanism directly, without any class syntax involved (see
[prototypal-inheritance.md](prototypal-inheritance.md)); and modern `class`/`extends` syntax is a
clearer layer over exactly this same prototype system — understanding the translation explains
otherwise-surprising class behavior rather than requiring it to be memorized as arbitrary.
