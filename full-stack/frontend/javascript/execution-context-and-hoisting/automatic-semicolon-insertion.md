# ⏭️ Automatic Semicolon Insertion

## Why JavaScript Lets You Leave Semicolons Out — and When It Bites

Plenty of working JavaScript has no semicolons, and plenty has them everywhere. Both are legal
because the parser has a rule set, **automatic semicolon insertion (ASI)**, that adds missing
semicolons in specific situations. ASI is not "the engine guesses what you meant": it is a small,
mechanical error-correction rule. When you know the rules, the failure cases are predictable;
when you don't, they look like impossible bugs.

## 📜 The Three Rules

These are the rules as MDN's lexical grammar reference states them (paraphrased):

1. **A token the grammar does not allow** is found, and it is separated from the previous token by at
   least one line break (or it is a closing `}`): a semicolon is inserted **before** it.
2. **The end of the input** is reached and the program is not yet complete: a semicolon is inserted
   at the end.
3. **Restricted productions** — a few constructs forbid a line break at a particular point. If a line
   break appears there, a semicolon is inserted. These include `return`, `throw`, `yield`, a `break`
   or `continue` followed by a label, postfix `++` and `--`, and the arrow `=>`.

The crucial detail in rule 1 is *"a token the grammar does not allow."* ASI only fires when the
parser would otherwise hit a syntax error. If the next line can legally continue the current
statement, **no semicolon is inserted** — even when you plainly meant one.

## 💥 Pitfall 1: `return` Followed by a Line Break

```js
function getUser() {
  return
  {
    name: "Ada"
  };
}

console.log(getUser());   // undefined
```

`return` is a restricted production: a line break right after it ends the statement, so the function
returns `undefined` and the object literal below is never reached. The fix is to start the value on
the same line as `return`:

```js
function getUser() {
  return {
    name: "Ada"
  };
}
```

## 💥 Pitfall 2: A Line That Starts With `(`, `[`, or a Template Literal

These characters can legally continue the previous line (as a call, a property access, or a tagged
template), so no semicolon is inserted:

```js
const b = 1
(2).toString()
// TypeError: 1 is not a function      — parsed as  1(2).toString()
```

```js
const a = 1
[1, 2, 3].forEach(n => console.log(n))
// TypeError: Cannot read properties of undefined (reading 'forEach')
// parsed as  1[1, 2, 3].forEach(...)  — the comma operator picks 3, and 1[3] is undefined
```

The same trap catches an immediately-invoked function expression after an unterminated line:

```js
const config = {}
(function () { console.log("setup"); })()
// TypeError: {} is not a function
```

And a template literal becomes a tag call:

```js
const name = "Ada"
const prefix = "Hello, "
`${name}`.toUpperCase()
// TypeError: "Hello, " is not a function   — parsed as a tagged template on the previous line
```

Terminating the previous statement fixes each of these:

```js
const b = 1;
(2).toString();
```

## 💥 Pitfall 3: Postfix `++` and `--` Across a Line Break

```js
let a = 1, b = 2
a
++b
console.log(a, b)   // 1 3
```

Postfix `++` may not be preceded by a line break, so the parser treats `a` as a complete statement and
`++b` as a separate, *prefix* increment — which is often not what the author pictured.

## 💥 Pitfall 4: Line Breaks After `throw` and Before `=>`

```js
throw
new Error("x")
// SyntaxError: Illegal newline after throw

const f = (x)
=> x * 2
// SyntaxError: Unexpected token '=>'
```

Not every restricted production silently changes meaning; some simply produce a syntax error. Both
are cheap to spot once you know the rule.

## 🧭 Two Defensible Styles

| Style | Rule to follow |
|-------|----------------|
| **Semicolons always** | End every statement with `;`. This is Prettier's default (`semi: true`). |
| **Semicolon-less** | Omit them, but begin any line starting with `(`, `[`, or a backtick with a `;`. Prettier's `--no-semi` option does exactly this — it adds semicolons only at the beginning of lines that may introduce ASI failures. |

```js
const a = 1
;[1, 2, 3].forEach(n => console.log(n))   // logs 1, 2, 3
```

Either style is valid; what matters is choosing one and enforcing it with a formatter, so no one has
to remember the exceptions. ESLint's
[`no-unexpected-multiline`](https://eslint.org/docs/latest/rules/no-unexpected-multiline) rule, part
of its recommended set, flags the "looks like two statements but parses as one" cases from
Pitfall 2.

## 🎤 Interview Angle

- **"What is ASI?"** A parser rule that inserts semicolons when the grammar would otherwise fail
  at a line break, at a closing brace, or at the end of input — plus fixed rules for restricted
  productions such as `return`.
- **"Give an example where ASI breaks code."** `return` followed by a newline and an object literal
  returns `undefined`.
- **"Does omitting semicolons make code unsafe?"** Not inherently — but lines beginning with `(`,
  `[`, or a template literal need care, so teams standardize on one style and automate it.

## Common Mistakes

- **Putting the returned value on the line after `return`**, including multi-line objects or JSX.
- **Starting a line with `(` or `[` after a statement with no semicolon**, such as an IIFE.
- **Assuming ASI "adds a semicolon wherever one is missing"** — it only repairs places where the
  parse would otherwise fail.
- **Mixing both styles in one codebase** instead of enforcing one with tooling.

## Module Summary

Across this module: an **execution context** is the engine's record for running code — an
environment of variables, an outer link, and a `this` value — and the **scope chain** is the chain
of environments fixed by where code is *written*, which also explains closures (see
[execution-contexts-and-the-scope-chain.md](execution-contexts-and-the-scope-chain.md));
**hoisting** is the visible result of setting up bindings before code runs, with `function`
declarations fully available, `var` giving `undefined`, and `let`/`const`/`class` guarded by the
**temporal dead zone** (see [hoisting-and-the-temporal-dead-zone.md](hoisting-and-the-temporal-dead-zone.md));
**strict mode** turns accidental globals, writes to read-only properties, and a stray `this` into
errors, and is already on in modules and classes (see [strict-mode.md](strict-mode.md)); and
**automatic semicolon insertion** is a mechanical error-correction rule whose failure cases —
`return` plus a newline, lines starting with `(` or `[` — are avoided by choosing one style and
enforcing it (see this file).

## ➡️ Next

Continue to the Functional JavaScript Patterns module, the next module in this section, which builds
on closures and scope to cover higher-order functions, currying, and memoization.
