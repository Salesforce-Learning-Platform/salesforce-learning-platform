# What Is JavaScript?

## A Language for Two Environments

JavaScript was created in 1995 to make web pages interactive directly in the browser — before it,
a web page was static once loaded. Today, JavaScript runs in two major environments:

- **The browser**: every major browser includes a JavaScript engine (Chrome/Edge use V8, Firefox
  uses SpiderMonkey, Safari uses JavaScriptCore) that executes scripts embedded in or linked from
  HTML pages.
- **Node.js**: a runtime that executes JavaScript outside the browser entirely — on a server, in a
  build tool, or in a CLI — introduced in
  [installing-a-package-manager-and-node.md](../../foundations/preparing-your-machine/installing-a-package-manager-and-node.md).

The same core language runs in both, though each environment adds its own additional APIs (the
browser adds DOM APIs; Node adds filesystem and networking APIs neither environment shares with
the other).

## JavaScript and ECMAScript

**ECMAScript** is the official language specification, standardized by TC39 and published as
ECMA-262; "JavaScript" is the language as implemented by browsers and Node, conforming to that
specification. New language features (like `let`/`const`, arrow functions, or optional chaining)
are proposed, refined, and eventually standardized through TC39, then implemented by JavaScript
engines — this is why "ECMAScript 2015" (also called ES6) and later editions are frequently
referenced when discussing which JavaScript features are available in a given environment.

## Dynamically and Loosely Typed

JavaScript is **dynamically typed**: a variable's type is determined at runtime and can change
(the same variable can hold a number, then later a string). It's also **loosely typed** (or
"weakly typed"): the language often converts between types automatically rather than raising an
error — covered in detail in
[operators-and-type-system/type-coercion.md](../operators-and-type-system/type-coercion.md). Both
properties give JavaScript flexibility, at the cost of some behaviors that surprise developers
coming from strictly, statically typed languages — this is exactly the gap TypeScript (covered in
its own domain) was created to close.

## Common Mistakes

- Assuming "JavaScript" and "ECMAScript" are unrelated terms rather than "the language" and "its
  formal specification."
- Confusing Java and JavaScript — beyond a superficially similar name (a deliberate marketing
  decision in 1995), they are unrelated languages with different syntax, design, and use cases.
- Assuming JavaScript only runs in browsers, missing Node.js's role in build tooling, servers, and
  the CLI tools used throughout [Preparing Your Machine](../../foundations/preparing-your-machine/).

## Next

Continue to [setting-up-javascript.md](setting-up-javascript.md) to actually run some.
