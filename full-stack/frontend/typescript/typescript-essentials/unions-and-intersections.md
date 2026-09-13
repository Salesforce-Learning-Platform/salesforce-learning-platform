# Unions and Intersections

## Union Types (`|`) — "One of These"

```ts
type Status = "pending" | "active" | "closed";
type Id = string | number;

function printId(id: Id) {
  console.log(id);
}

printId(42);        // fine
printId("abc123");  // also fine
printId(true);        // Error — not part of the union
```

A **union** type says a value can be *any one* of several specified types — narrower and safer
than `any`, while still permitting legitimate variation.

## Narrowing a Union

```ts
function formatId(id: string | number): string {
  if (typeof id === "string") {
    return id.toUpperCase(); // TypeScript knows `id` is a string here
  }
  return id.toFixed(2);         // TypeScript knows `id` is a number here
}
```

Inside each branch of a type check (`typeof`, `instanceof`, or a custom check), TypeScript
**narrows** the union to the specific type that branch guarantees — this is what makes union types
practical to actually use, rather than needing a manual cast at every access.

## Intersection Types (`&`) — "Combined Requirements"

```ts
type Timestamped = { createdAt: Date };
type Named = { name: string };

type NamedAndTimestamped = Timestamped & Named;

const item: NamedAndTimestamped = {
  name: "Widget",
  createdAt: new Date(),
}; // must satisfy BOTH shapes
```

An **intersection** combines multiple types into one that must satisfy *all* of them
simultaneously — the opposite of a union's "any one of these."

## Union vs. Intersection — Don't Confuse Them

| | Union (`\|`) | Intersection (`&`) |
|---|---|---|
| Meaning | One of these types | All of these types, combined |
| A value needs to satisfy | Just one member | Every member simultaneously |

A very common beginner mistake: reaching for `&` when a union was actually intended (or vice
versa) — remembering that `|` reads as "or" and `&` reads as "and" maps directly onto their actual
behavior.

## Discriminated Unions — A Genuinely Powerful Pattern

```ts
type Circle = { kind: "circle"; radius: number };
type Square = { kind: "square"; side: number };
type Shape = Circle | Square;

function area(shape: Shape): number {
  if (shape.kind === "circle") {
    return Math.PI * shape.radius ** 2; // narrowed to Circle
  }
  return shape.side ** 2;                 // narrowed to Square
}
```

A shared literal property (`kind`) lets TypeScript narrow a union to the exact correct shape based
on a single check — an extremely common, idiomatic pattern for modeling "one of several distinct
variants," used constantly in real-world TypeScript, including in state-management patterns
covered later in the React domain.

## Common Mistakes

- Confusing `|` and `&`, especially since their English readings ("or"/"and") can feel
  counter-intuitive relative to how set intersection/union work mathematically.
- Trying to access a property that only exists on *some* members of a union without first
  narrowing — TypeScript correctly refuses this, since it can't guarantee the property exists on
  every possible member.
- Not using a discriminated union's shared literal property when modeling distinct variants,
  instead relying on multiple optional properties and manual `if` checks that TypeScript can't
  narrow as cleanly.

## Next

Continue to [enums.md](enums.md) for another way to model a fixed set of named values.
