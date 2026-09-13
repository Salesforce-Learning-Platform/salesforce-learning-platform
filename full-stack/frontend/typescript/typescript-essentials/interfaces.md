# Interfaces

## Defining an Object Shape

```ts
interface User {
  name: string;
  email: string;
  age: number;
}

function greet(user: User) {
  return `Hello, ${user.name}`;
}

greet({ name: "Ada", email: "ada@example.com", age: 36 }); // must match the shape
greet({ name: "Ada" }); // Error: missing email, age
```

An `interface` describes the required shape of an object — every property listed must be present
(unless marked optional), with the specified type.

## Optional and Readonly Properties

```ts
interface User {
  name: string;
  email: string;
  nickname?: string;   // optional — may be omitted entirely
  readonly id: string;  // can be set once, then never reassigned
}

const user: User = { name: "Ada", email: "ada@example.com", id: "u1" };
user.id = "u2"; // Error: Cannot assign to 'id' because it is a read-only property
```

`?` marks a property as optional; `readonly` allows reading a property but prevents reassigning it
after the object is created — a compile-time-enforced version of the immutability intent behind
`Object.freeze()` from
[object-methods.md](../../javascript/arrays-and-objects/object-methods.md), without the runtime
cost.

## Extending Interfaces

```ts
interface Person {
  name: string;
  email: string;
}

interface Employee extends Person {
  employeeId: string;
  department: string;
}
```

`extends` builds one interface on top of another, inheriting its properties — directly analogous
to `class extends` from
[classes-and-inheritance.md](../../javascript/object-oriented-programming/classes-and-inheritance.md),
but for describing a *shape*, not actual runtime behavior.

## Interfaces for Function Shapes

```ts
interface Comparator {
  (a: number, b: number): number;
}

const ascending: Comparator = (a, b) => a - b;
```

An interface can also describe a function's signature — useful for typing a callback parameter or
a variable expected to hold a function of a specific shape.

## Common Mistakes

- Forgetting `?` on a genuinely optional property, forcing every caller to provide a value that
  isn't actually always necessary.
- Assuming `readonly` provides the same guarantee as `Object.freeze()` — `readonly` is purely a
  compile-time check; nothing prevents a runtime `JSON.parse()`-derived object or JavaScript code
  that bypasses TypeScript from mutating it anyway.
- Defining an interface for a value that isn't actually an object shape at all (a union of
  primitives, for instance) — that's what `type` aliases, covered next, are for.

## Next

Continue to [type-aliases.md](type-aliases.md) to see the alternative, more general tool for
naming a type.
