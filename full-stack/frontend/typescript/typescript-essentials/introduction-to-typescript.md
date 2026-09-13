# Introduction to TypeScript

## What TypeScript Actually Is

TypeScript is a **superset** of JavaScript — every valid JavaScript file is already valid
TypeScript — that adds static type annotations, checked by a compiler (`tsc`) before the code ever
runs. TypeScript is compiled ("transpiled") down to plain JavaScript; browsers and Node never run
TypeScript directly.

## The Problem It Solves

Recall from
[what-is-javascript.md](../../javascript/introduction-to-javascript/what-is-javascript.md) that
JavaScript is dynamically and loosely typed — a function has no built-in way to guarantee it was
called with the arguments it expects:

```js
function greet(name) {
  return `Hello, ${name.toUpperCase()}`;
}

greet(42); // runtime TypeError: name.toUpperCase is not a function — only discovered when this actually runs
```

```ts
function greet(name: string) {
  return `Hello, ${name.toUpperCase()}`;
}

greet(42); // COMPILE-TIME error — caught before the code ever runs, by your editor and the compiler
```

This is the entire value proposition in one example: TypeScript catches an entire category of
mistakes — wrong argument types, typos in property names, forgetting a possible `null`/`undefined`
— **before** the code runs, often directly in your editor as you type, rather than as a runtime
crash a user might actually hit in production.

## Type Erasure — No Runtime Cost, No Runtime Protection

```ts
function add(a: number, b: number): number {
  return a + b;
}
```

Compiles down to plain JavaScript with the type annotations completely stripped:

```js
function add(a, b) {
  return a + b;
}
```

This is worth being precise about: TypeScript's type checking exists **only at compile time**. The
compiled JavaScript that actually runs has zero runtime type checking of its own — if untyped data
crosses a boundary TypeScript couldn't see through (data from `JSON.parse()`, a third-party API
response), TypeScript's static guarantees don't extend to it automatically, and runtime validation
(covered in the AI-as-coding-partner and backend modules) is still genuinely necessary at those
boundaries.

## Getting Started

```bash
npm install --save-dev typescript
npx tsc --init   # creates a tsconfig.json
npx tsc           # compiles .ts files per tsconfig.json
```

Most real projects use a build tool (Vite, Next.js, etc. — covered in their own modules) that
handles TypeScript compilation automatically as part of the existing dev/build workflow, rather
than invoking `tsc` manually.

## Common Mistakes

- Assuming TypeScript provides runtime type safety — it only checks types before compiling; the
  actual JavaScript has no memory of those types at all once running.
- Treating every JavaScript-to-TypeScript migration as needing to happen all at once — see
  [typescript-with-javascript-projects.md](typescript-with-javascript-projects.md) for the
  incremental approach that's actually standard practice.
- Not validating data at genuine runtime boundaries (an API response, `JSON.parse()`) just because
  it's typed as if it were trustworthy — TypeScript's compile-time guarantee doesn't extend past
  boundaries it can't see through.

## Next

Continue to [basic-types.md](basic-types.md) to start actually annotating code.
