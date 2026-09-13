# Parameters and Return Values

## Default Parameters

```js
function greet(name = "Guest") {
  return `Hello, ${name}`;
}

greet();        // "Hello, Guest" — default used
greet("Ada");   // "Hello, Ada"
greet(undefined); // "Hello, Guest" — undefined explicitly triggers the default
```

A default parameter's value is used whenever the argument is omitted **or** explicitly passed as
`undefined` — but not for other falsy values like `null` or `0`, which are used as-is.

## Rest Parameters

```js
function sum(...numbers) {
  return numbers.reduce((total, n) => total + n, 0);
}

sum(1, 2, 3); // 6
```

`...numbers` collects any number of remaining arguments into a real array — the modern, preferred
way to accept a variable number of arguments.

## The `arguments` Object — Legacy

Regular `function`s (not arrow functions) have access to an older, array-*like* `arguments` object
containing every passed argument:

```js
function oldStyleSum() {
  let total = 0;
  for (let i = 0; i < arguments.length; i++) total += arguments[i];
  return total;
}
```

`arguments` predates rest parameters, is not a real array (lacking array methods like `.map()`
without conversion), and is unavailable in arrow functions entirely — rest parameters are
uniformly preferred in modern code.

## Return Values

```js
function double(x) {
  return x * 2;
}
```

A function without an explicit `return` implicitly returns `undefined`. Only one `return`
statement executes per call — reaching a `return` immediately exits the function, skipping any
remaining code in its body.

```js
function example() {
  if (true) {
    return "early";
  }
  console.log("never runs"); // unreachable after the return above
}
```

## Common Mistakes

- Using `arguments` in new code instead of rest parameters, missing real array methods and losing
  compatibility with arrow functions.
- Forgetting that a missing `return` produces `undefined`, and being surprised when a function's
  result is used elsewhere as if it returned something meaningful.
- Passing `null` expecting a default parameter to apply — only `undefined` (or a truly omitted
  argument) triggers a default; `null` is used as the actual value.

## Next

Continue to [scope.md](scope.md) to see what a function can actually see and access from outside
itself.
