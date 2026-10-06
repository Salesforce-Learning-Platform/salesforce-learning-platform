# 🧾 JSON Serialization

## A Text Format for Data

**JSON** (JavaScript Object Notation) is a plain-text format for exchanging data. It looks like a
JavaScript object literal but is stricter, and it is not JavaScript — it is a language-neutral format
that happens to be easy to produce and read from JavaScript. This platform has already used it in
[fetch-api.md](../asynchronous-programming-and-modules/fetch-api.md) (request and response bodies)
and [local-storage.md](../using-browser-functionalities/local-storage.md) (storing structured
data as text). This file covers exactly how the two core functions behave, including the cases that
surprise people.

## 📏 What Counts as Valid JSON

A JSON value is an object, array, string, number, `true`, `false`, or `null`. Compared to a
JavaScript literal, JSON is stricter in ways that cause most parse errors. MDN's `JSON.parse`
reference lists the invalid constructs:

- Trailing commas (`[1, 2,]`, `{"a": 1,}`)
- Single-quoted strings or keys (`{'a': 1}`)
- Unquoted keys (`{a: 1}`)
- Comments
- `undefined` values

## 📤 `JSON.stringify`

```js
JSON.stringify(value, replacer, space)
```

### What happens to each kind of value

```js
console.log(JSON.stringify({
  a: 1,
  b: undefined,
  c() {},
  d: Symbol("s"),
  e: null,
  f: NaN,
  g: Infinity,
  h: [undefined, () => 1, Symbol("x")],
}));
// {"a":1,"e":null,"f":null,"g":null,"h":[null,null,null]}
```

| Value | In an object property | In an array element |
|-------|-----------------------|---------------------|
| `undefined`, function, symbol | The property is **omitted** | Becomes `null` |
| `NaN`, `Infinity` | `null` | `null` |
| `Date` | ISO string (via its `toJSON`) | ISO string |
| `Map`, `Set` | `{}` (no enumerable own properties) | `{}` |
| `BigInt` | **Throws** `TypeError` | **Throws** |
| Circular reference | **Throws** `TypeError` | **Throws** |

Symbol-keyed properties and non-enumerable properties are always ignored. A circular structure
throws `TypeError: Converting circular structure to JSON` (the engine adds detail about where the
cycle closes), and a `BigInt` throws `TypeError: Do not know how to serialize a BigInt`. Error
wording varies by engine.

### Custom output with `toJSON`

If a value has a `toJSON()` method, `JSON.stringify` serializes whatever that method returns —
which is exactly how `Date` becomes an ISO string. Your own classes can use it too:

```js
class Money {
  constructor(cents, currency) {
    this.cents = cents;
    this.currency = currency;
  }
  toJSON() {
    return { amount: this.cents / 100, currency: this.currency };
  }
}

console.log(JSON.stringify({ price: new Money(1999, "EUR") }));
// {"price":{"amount":19.99,"currency":"EUR"}}
```

### The `replacer`: filter or transform

An **array** replacer is a whitelist of keys; a **function** replacer is called for every key/value
pair and its return value replaces the original (return `undefined` to omit):

```js
const user = { name: "Ada", password: "secret", age: 36 };

console.log(JSON.stringify(user, ["name", "age"]));
// {"name":"Ada","age":36}

console.log(JSON.stringify(user, (key, value) => (key === "password" ? undefined : value)));
// {"name":"Ada","age":36}
```

Dropping sensitive fields this way is a safety net, not a substitute for never putting secrets into
objects that get serialized in the first place.

### The `space` argument: readable output

```js
console.log(JSON.stringify({ a: 1, b: [1, 2] }, null, 2));
// {
//   "a": 1,
//   "b": [
//     1,
//     2
//   ]
// }
```

A number sets the indentation width (capped at 10); a string is used as the indent itself.

## 📥 `JSON.parse`

```js
JSON.parse(text, reviver)
```

### Parsing and error handling

`JSON.parse` returns the value described by the text, and throws a `SyntaxError` for anything that
is not valid JSON:

```js
JSON.parse("{'a': 1}");
// SyntaxError: Expected property name or '}' in JSON at position 1 (line 1 column 2)

JSON.parse('{"a": 1,}');
// SyntaxError: Expected double-quoted property name in JSON at position 8 (line 1 column 9)

JSON.parse("");
// SyntaxError: Unexpected end of JSON input
```

(The messages shown are from V8 in Node.js; other engines word them differently.) Any JSON that
arrives from outside your program — a network response, a stored value, user input — can be
malformed, so wrap the call in `try`/`catch`.

`JSON.parse` only *parses*; unlike `eval`, it never executes the text as code, which is why it is
the correct way to read JSON. Parsing guarantees the *syntax* is valid, not that the data has the
*shape* you expect — validate it with a schema, as in
[schema-validation-with-zod](../../../artificial-intelligence/schema-validation-with-zod/).

### The `reviver`: transform while parsing

JSON has no date type, so dates arrive as strings. A reviver is called for each key and value
(depth-first, innermost values first), and its return value replaces the parsed one:

```js
const text = '{"name":"Ada","joined":"2024-05-01T00:00:00.000Z"}';

const user = JSON.parse(text, (key, value) =>
  key === "joined" ? new Date(value) : value
);

console.log(user.joined instanceof Date);   // true
console.log(user.joined.getUTCFullYear());  // 2024
```

### Large Numbers Lose Precision

JSON numbers are parsed into ordinary JavaScript numbers, which are accurate only up to
`Number.MAX_SAFE_INTEGER` (9007199254740991):

```js
console.log(JSON.parse("12345678901234567890"));   // 12345678901234567000 — digits were lost
```

MDN documents a newer reviver feature for this: a third `context` argument whose `source` property
holds the original text of a primitive, letting you build a `BigInt` from it:

```js
console.log(JSON.parse('{"n": 12345678901234567890}', (key, value, context) =>
  key === "n" ? BigInt(context.source) : value
));
// { n: 12345678901234567890n }
```

This works in current Node.js; check MDN's compatibility table before relying on it in older
runtimes. Otherwise, the usual defense is to transmit large integers as strings.

## 🔄 The Round-Trip Is Lossy

`JSON.parse(JSON.stringify(x))` returns plain data, not the original: dates become strings,
`undefined` and functions vanish, `Map` and `Set` become `{}`, class instances become plain objects.
That is why it is a poor general-purpose deep copy — see
[copying-objects-shallow-vs-deep.md](copying-objects-shallow-vs-deep.md) for the alternatives.

## 🎤 Interview Angle

- **"What is JSON, and how does it differ from a JavaScript object?"** JSON is a text format with
  strict syntax — double-quoted keys and strings, no trailing commas, no comments, no `undefined`
  or functions. A JavaScript object is an in-memory value.
- **"What does `JSON.stringify` do with `undefined`?"** Omits it from objects, turns it into `null`
  in arrays; a bare `JSON.stringify(undefined)` returns `undefined`.
- **"How would you serialize a custom class?"** Give it a `toJSON()` method, or use a replacer.
- **"Why is `JSON.parse` safer than `eval`?"** It only parses data and never executes code.

## Common Mistakes

- **Calling `JSON.parse` without `try`/`catch`** on external input.
- **Assuming the parsed value has the right shape** because it parsed successfully.
- **Round-tripping dates, maps, or sets through JSON** and expecting them back unchanged.
- **Hand-writing JSON with single quotes or trailing commas.**
- **Letting large integer IDs pass through JSON as numbers.**

## ➡️ Next

Continue to [private-class-fields.md](private-class-fields.md) to see how classes can keep data
genuinely hidden — including from `JSON.stringify` and every other enumeration tool.
