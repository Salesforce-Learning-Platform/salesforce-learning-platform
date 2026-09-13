# Utility Types

## Transforming Existing Types Instead of Redefining Them

TypeScript ships several built-in generic types (see [generics.md](generics.md)) that transform an
existing type into a related one — avoiding the need to manually redefine a nearly-identical shape
by hand every time a variant is needed.

## The Most Commonly Used Ones

```ts
interface User {
  id: string;
  name: string;
  email: string;
  role: string;
}

type PartialUser = Partial<User>;   // every property becomes optional — great for an update payload
type UserPreview = Pick<User, "id" | "name">;  // only the listed properties
type UserWithoutId = Omit<User, "id">;           // every property EXCEPT the listed ones
type ReadonlyUser = Readonly<User>;               // every property becomes readonly
type UserMap = Record<string, User>;               // an object type: { [key: string]: User }
```

| Utility | Effect |
|---|---|
| `Partial<T>` | Every property becomes optional |
| `Required<T>` | Every property becomes required (opposite of `Partial`) |
| `Readonly<T>` | Every property becomes read-only |
| `Pick<T, Keys>` | A new type with only the listed properties |
| `Omit<T, Keys>` | A new type with every property *except* the listed ones |
| `Record<Keys, T>` | An object type mapping each key to a value of type `T` |

## A Realistic Example: Update Payloads

```ts
interface User {
  id: string;
  name: string;
  email: string;
}

function updateUser(id: string, changes: Partial<Omit<User, "id">>) {
  // changes might contain name, email, both, or neither — but never id
}

updateUser("u1", { name: "Ada Lovelace" }); // valid — partial update
```

`Partial<Omit<User, "id">>` combines two utility types: first removing `id` (which should never be
part of an update payload), then making everything else optional (since an update typically
changes only some fields) — expressing a precise, realistic constraint in one line rather than
hand-writing a separate `UserUpdatePayload` interface that would need to be kept manually in sync
with `User` as it evolves.

## Common Mistakes

- Manually redefining a near-duplicate interface (like a separate `UserUpdate` type with every
  field marked optional by hand) instead of deriving it from the original with `Partial`/`Omit` —
  this duplication silently drifts out of sync as the original type evolves.
- Overusing deeply nested utility type compositions to the point where the resulting type is
  genuinely hard for a reader to mentally reconstruct — clarity should still win over cleverness.
- Forgetting that utility types, like all TypeScript types, are compile-time only — `Readonly<T>`
  provides no runtime enforcement, exactly like the plain `readonly` modifier from
  [interfaces.md](interfaces.md).

## Next

Continue to
[typescript-with-javascript-projects.md](typescript-with-javascript-projects.md) for adopting all
of this incrementally in a real, existing codebase.
