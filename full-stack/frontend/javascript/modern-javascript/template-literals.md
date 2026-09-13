# Template Literals

## Syntax

Template literals use backticks (`` ` ``) instead of quotes, and support **string interpolation**
— embedding an expression's value directly inline:

```js
const name = "Ada";
const age = 36;

const greeting = `Hello, ${name}! You are ${age} years old.`;
// "Hello, Ada! You are 36 years old."
```

`${...}` can contain any valid JavaScript expression, not just a plain variable — including
function calls, arithmetic, and ternaries:

```js
`Total: ${price * quantity}`;
`Status: ${isActive ? "active" : "inactive"}`;
```

## Multi-Line Strings

```js
const message = `Line one
Line two
Line three`;
```

Template literals preserve line breaks exactly as written — no `\n` escape characters needed, and
no string concatenation across multiple lines required, as older quote-based strings would have
needed.

## Comparison to String Concatenation

```js
// Old way
const greeting1 = "Hello, " + name + "! You are " + age + " years old.";

// Template literal
const greeting2 = `Hello, ${name}! You are ${age} years old.`;
```

The template literal reads closer to the final output, without the visual noise of alternating
quotes and `+` operators — a genuine readability improvement, especially as the number of
interpolated values grows.

## Tagged Templates — Advanced

```js
function highlight(strings, ...values) {
  return strings.reduce((result, str, i) =>
    `${result}${str}${values[i] ? `<mark>${values[i]}</mark>` : ""}`, "");
}

highlight`Hello, ${name}! You are ${age} years old.`;
```

A **tag function** placed immediately before a template literal (no parentheses) receives the
literal's string parts and interpolated values separately, letting it process them programmatically
before producing a final result — an advanced pattern, used by libraries like styled-components for
CSS-in-JS, but uncommon in typical application code.

## Common Mistakes

- Continuing to use `+`-based concatenation out of habit for anything with more than one
  interpolated value, missing the readability improvement template literals provide.
- Forgetting that `${}` requires valid JavaScript *expressions*, not statements — `${if (x) {...}}`
  is invalid, while `${x ? a : b}` (a ternary expression) works.
- Confusing backticks with regular quotes visually, since they look similar at a glance — most
  editors syntax-highlight them differently, which helps.

## Next

Continue to
[optional-chaining-and-nullish-coalescing.md](optional-chaining-and-nullish-coalescing.md) for
this module's other genuinely new topic.
