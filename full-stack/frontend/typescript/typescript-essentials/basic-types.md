# Basic Types

## Annotating Variables

```ts
let age: number = 36;
let name: string = "Ada";
let isActive: boolean = true;
let tags: string[] = ["admin", "verified"];   // an array of strings
let coords: [number, number] = [12.5, 45.2];  // a tuple — fixed length, specific types per position
```

## Type Inference — Annotations Are Often Optional

```ts
let age = 36; // TypeScript infers `number` automatically — no annotation needed here
age = "36";     // Error: Type 'string' is not assignable to type 'number'
```

TypeScript infers a variable's type from its initial value whenever possible — explicit
annotations are most valuable (and often required) for function parameters, since there's no
initial value for the compiler to infer from.

## Annotating Functions

```ts
function add(a: number, b: number): number {
  return a + b;
}

const multiply = (a: number, b: number): number => a * b;
```

Parameter types are effectively required in practice (TypeScript otherwise treats them as an
implicit, unchecked `any` in permissive configurations); the return type is often inferable and
can be omitted, though writing it explicitly serves as useful, self-documenting confirmation of
intent.

## `any` — The Escape Hatch, Used Sparingly

```ts
let value: any = 42;
value = "now a string"; // allowed — `any` disables type checking entirely for this value
```

`any` opts a value out of TypeScript's type checking completely — it's occasionally a necessary
escape hatch (working with a genuinely untyped third-party library, for instance) but defeats the
entire purpose of using TypeScript wherever it's used. `unknown` (below) is nearly always the
better choice when a value's type genuinely isn't known upfront.

## `unknown` — The Safer Alternative to `any`

```ts
let value: unknown = fetchSomeData();

value.toUpperCase(); // Error — can't call methods on `unknown` without narrowing first

if (typeof value === "string") {
  value.toUpperCase(); // fine — TypeScript now knows it's a string in this branch
}
```

`unknown` forces you to check (narrow) the actual type before doing anything with the value —
`any` allows literally any operation with no such check, which is exactly why `unknown` is safer
for representing genuinely uncertain data (like an API response) while `any` should be treated as
a near-last resort.

## `void` and `null`/`undefined`

```ts
function logMessage(message: string): void {
  console.log(message); // returns nothing meaningful
}

let maybeName: string | null = null; // explicitly allows null, via a union (see unions-and-intersections.md)
```

## Common Mistakes

- Reaching for `any` by default whenever a type is unclear, instead of `unknown` — silently
  disabling type checking rather than being forced to verify the actual type before use.
- Over-annotating variables whose type TypeScript can already infer correctly, adding noise without
  benefit.
- Forgetting that TypeScript's array/tuple distinction matters — `string[]` means "any number of
  strings," while `[string, number]` means "exactly this shape, in this order."

## Next

Continue to [interfaces.md](interfaces.md) to define the shape of objects, not just individual
values.
