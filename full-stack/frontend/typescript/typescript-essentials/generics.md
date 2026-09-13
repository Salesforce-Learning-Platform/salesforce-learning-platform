# Generics

## The Problem Generics Solve

```ts
function firstElement(arr: any[]): any {
  return arr[0];
}

const num = firstElement([1, 2, 3]);   // typed as `any` — TypeScript lost track of what's inside
num.toUpperCase();                        // no error at compile time — but crashes at runtime!
```

Using `any` here "works," but throws away exactly the type safety TypeScript exists to provide —
the function's return type gives no useful information at all about what's actually inside.

## The Generic Solution

```ts
function firstElement<Type>(arr: Type[]): Type {
  return arr[0];
}

const num = firstElement([1, 2, 3]);      // inferred as `number`
const str = firstElement(["a", "b"]);        // inferred as `string`
num.toUpperCase();                             // Error — TypeScript correctly knows `num` is a number
```

`<Type>` is a **type parameter** — a placeholder that gets filled in with the actual type used at
each call site. The function works for *any* array type, while still preserving full, accurate
type information for each individual call — the best of both worlds compared to either duplicating
the function per type or falling back to `any`.

## Generic Interfaces and Types

```ts
interface ApiResponse<Data> {
  data: Data;
  status: number;
}

const userResponse: ApiResponse<User> = {
  data: { name: "Ada", email: "ada@example.com" },
  status: 200,
};
```

This is an extremely common real-world pattern — a single generic `ApiResponse` shape reused for
every different kind of API endpoint's actual response data, rather than defining an entirely
separate response type for each one.

## Generic Constraints

```ts
interface HasLength {
  length: number;
}

function logLength<Type extends HasLength>(item: Type): Type {
  console.log(item.length);
  return item;
}

logLength("hello");     // fine — strings have .length
logLength([1, 2, 3]);    // fine — arrays have .length
logLength(42);            // Error — numbers have no .length
```

`extends` on a type parameter **constrains** it — rather than accepting truly any type, this
requires the type parameter to satisfy a minimum shape, letting TypeScript safely allow operations
(like accessing `.length`) that wouldn't be safe for a genuinely unconstrained type parameter.

## Common Mistakes

- Reaching for `any` to "make it work for multiple types," when a generic type parameter would
  preserve accurate, specific type information for each actual call.
- Over-constraining a generic unnecessarily, making a function less reusable than it needs to be.
- Under-constraining a generic, then needing unsafe workarounds inside the function body because
  TypeScript correctly won't assume operations the type parameter doesn't actually guarantee.

## Next

Continue to [utility-types.md](utility-types.md) for built-in generics that transform existing
types.
