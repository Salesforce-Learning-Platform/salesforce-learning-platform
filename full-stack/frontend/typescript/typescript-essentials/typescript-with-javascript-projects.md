# TypeScript with JavaScript Projects

## You Don't Have to Convert Everything at Once

A common misconception is that adopting TypeScript means rewriting an entire existing JavaScript
codebase upfront. In practice, TypeScript is explicitly designed for **incremental adoption** —
`.js` and `.ts` files can coexist in the same project, and files are typically converted one at a
time as they're touched for other reasons.

## `allowJs` and `checkJs`

```json
// tsconfig.json
{
  "compilerOptions": {
    "allowJs": true,
    "checkJs": false
  }
}
```

- **`allowJs`**: lets the TypeScript compiler process `.js` files alongside `.ts` files, so they
  can coexist in one build.
- **`checkJs`**: when enabled, applies TypeScript's type checking to plain `.js` files too (using
  inferred types, or types from JSDoc comments) — a genuinely useful intermediate step before fully
  converting a file to `.ts`.

## JSDoc as a Bridge

```js
/**
 * @param {string} name
 * @param {number} age
 */
function greet(name, age) {
  return `${name} is ${age}`;
}
```

With `checkJs` enabled, TypeScript reads JSDoc comments like these and applies the same type
checking as if they were real TypeScript annotations — letting a team get real type-checking
benefits in existing `.js` files without renaming them to `.ts` or changing any actual runtime
code at all.

## A Practical Adoption Path

1. Add TypeScript as a dev dependency and create a `tsconfig.json` with `allowJs: true`.
2. Optionally enable `checkJs` and start adding JSDoc type comments to existing, frequently-touched
   `.js` files.
3. Convert files to `.ts` incrementally — typically starting with new files, then working backward
   through existing ones as they're modified for other reasons anyway.
4. Gradually tighten `tsconfig.json`'s strictness settings (like `strict: true`) as the codebase's
   type coverage genuinely improves, rather than turning on maximum strictness from day one against
   a codebase not yet ready for it.

## Common Mistakes

- Assuming a TypeScript migration requires converting every file before gaining any benefit —
  incremental adoption, file by file, is the standard, realistic approach for an existing codebase.
- Enabling maximum strictness (`strict: true`) immediately on a large existing JavaScript codebase,
  producing an overwhelming number of errors before any incremental progress can be made.
- Ignoring JSDoc-based typing as "not real TypeScript" — with `checkJs` enabled, it provides
  genuine compile-time type checking without requiring a file rename at all.

## Module Summary

Across this module: TypeScript adds compile-time-only static typing on top of JavaScript, catching
a real category of bugs before code runs, with zero runtime cost or protection of its own (see
[introduction-to-typescript.md](introduction-to-typescript.md)); basic type annotations, `unknown`
over `any`, and type inference form the foundation (see [basic-types.md](basic-types.md));
interfaces describe object and function shapes (see [interfaces.md](interfaces.md)), while type
aliases are more general and required for unions (see [type-aliases.md](type-aliases.md));
unions model "one of several options" and intersections model "all of these combined," with
discriminated unions as a particularly powerful pattern (see
[unions-and-intersections.md](unions-and-intersections.md)); enums are a real tradeoff against
string union literals, particularly around API/JSON boundaries (see [enums.md](enums.md));
generics preserve accurate type information across reusable functions and types, an alternative to
`any` that doesn't sacrifice safety (see [generics.md](generics.md)); built-in utility types like
`Partial`/`Pick`/`Omit` derive new types from existing ones instead of duplicating them by hand
(see [utility-types.md](utility-types.md)); and TypeScript is designed for gradual, file-by-file
adoption into an existing JavaScript codebase, not an all-or-nothing rewrite.
