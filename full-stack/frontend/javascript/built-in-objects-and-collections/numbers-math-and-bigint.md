# 🔢 Numbers, Math, and BigInt

## One Number Type, With Famous Consequences

[data-types.md](../introduction-to-javascript/data-types.md) introduced `number`. Underneath, MDN
describes `Number` as an IEEE 754 double-precision 64-bit floating-point value — the same format
many other languages call `double`. That single design decision explains nearly every numeric
surprise in JavaScript, and it is why a second type, `BigInt`, exists.

## ⚠️ Floating-Point Arithmetic

```js
console.log(0.1 + 0.2);          // 0.30000000000000004
console.log(0.1 + 0.2 === 0.3);  // false
```

`0.1`, `0.2`, and `0.3` have no exact binary representation, so each is stored as the nearest
representable value, and the tiny errors show up when you compare. MDN notes that precision is
limited to roughly 15–17 significant decimal digits.

### Comparing With a Tolerance

`Number.EPSILON` is the gap between `1` and the next representable number (about `2.22e-16`). Used as
an *absolute* tolerance, it works for values near 1 — but not for larger ones:

```js
console.log(Math.abs((0.1 + 0.2) - 0.3) < Number.EPSILON);   // true

const a = 1.1 + 2.2;                                          // 3.3000000000000003
console.log(a === 3.3);                                       // false
console.log(Math.abs(a - 3.3));                               // 4.440892098500626e-16
console.log(Math.abs(a - 3.3) < Number.EPSILON);              // false — the check FAILS
```

Scale the tolerance to the magnitude of the numbers being compared:

```js
const nearlyEqual = (x, y) =>
  Math.abs(x - y) <= Number.EPSILON * Math.max(Math.abs(x), Math.abs(y));

console.log(nearlyEqual(1.1 + 2.2, 3.3));   // true
console.log(nearlyEqual(1, 1.0000001));     // false — genuinely different values
```

### Money: Use Integers

Never accumulate currency in floating-point. Store the smallest unit as an integer (cents) and
convert only for display:

```js
console.log(0.1 + 0.2);          // 0.30000000000000004
console.log((10 + 20) / 100);    // 0.3 — add whole cents, divide once at the end
```

Rounding to decimal places has its own trap, because `toFixed` and `Math.round` operate on the
*binary* value, not the decimal you typed:

```js
console.log((1.005).toFixed(2));               // 1.00  — not 1.01
console.log(Math.round(1.005 * 100) / 100);    // 1     — also not 1.01
console.log(typeof (1.5).toFixed(1));          // string — toFixed returns text
```

## 📏 Integer Limits and `NaN`

Integers are exact only up to `Number.MAX_SAFE_INTEGER` (2⁵³ − 1 = 9007199254740991); beyond it,
neighboring integers collapse together:

```js
console.log(Number.MAX_SAFE_INTEGER);                                      // 9007199254740991
console.log(Number.MAX_SAFE_INTEGER + 1 === Number.MAX_SAFE_INTEGER + 2);  // true — precision lost
console.log(Number.isSafeInteger(2 ** 53));                                // false
console.log(Number.isInteger(5.0));                                        // true
```

`NaN` ("not a number") is the result of failed numeric operations, and it has unique behavior:

```js
console.log(NaN === NaN);              // false — NaN is never equal to anything, itself included
console.log(Number.isNaN("NaN"));      // false — true only for the actual NaN value
console.log(isNaN("NaN"));             // true  — the global version coerces first
console.log(Object.is(NaN, NaN));      // true
console.log(Object.is(0, -0), 0 === -0);   // false true
console.log([NaN].includes(NaN));      // true  — includes() uses SameValueZero
console.log([NaN].indexOf(NaN));       // -1    — indexOf() uses ===
```

Prefer `Number.isNaN` over the global `isNaN`, as MDN's example shows.

## 🔄 Converting Strings to Numbers

```js
console.log(Number(""), Number("12px"), Number("  42  "));   // 0 NaN 42
console.log(parseInt("12px"), parseFloat("3.14abc"));         // 12 3.14
console.log(parseInt("0x1f"), parseInt("101", 2));            // 31 5
console.log(Number(null), Number(undefined), Number([]));     // 0 NaN 0
console.log(+"3");                                            // 3
```

`Number()` is strict (any trailing junk gives `NaN`); `parseInt` and `parseFloat` read as much as they
can. Always pass a radix to `parseInt` when it is not base 10 — and recall the
`map(parseInt)` trap in [higher-order-functions.md](../functional-javascript/higher-order-functions.md).
For the underlying coercion rules see
[type-coercion.md](../operators-and-type-system/type-coercion.md).

## ➗ The `Math` Object

```js
console.log(Math.round(2.5), Math.round(-2.5), Math.round(3.5));    // 3 -2 4   — ties round toward +∞
console.log(Math.round(-0.5));                                      // -0
console.log(Math.trunc(-4.7), Math.floor(-4.7), Math.ceil(-4.2));   // -4 -5 -4
```

`trunc` drops the fraction, `floor` rounds toward −∞, `ceil` toward +∞. Other staples: `Math.max`,
`Math.min` (with spread for arrays), `Math.abs`, `Math.sign`, `Math.hypot`, and `**` for powers.

### Random Numbers

`Math.random()` returns a number from `0` (inclusive) to `1` (exclusive). A random integer in a range
needs the standard formula:

```js
const randInt = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
console.log(randInt(3, 5));   // 3, 4, or 5
```

MDN warns that `Math.random()` is **not cryptographically secure** and must not be used for
security-related purposes — tokens, passwords, session IDs. Use the Web Crypto API instead:

```js
crypto.randomUUID();                           // a random UUID string
crypto.getRandomValues(new Uint32Array(2));    // cryptographically strong random integers
```

(The second call fills a [typed array](typed-arrays-and-binary-data.md).)

## 🐘 BigInt: Integers of Any Size

A `BigInt` is written with an `n` suffix, or created with `BigInt()`, and has no upper limit:

```js
console.log(2n ** 64n);                              // 18446744073709551616n
console.log(BigInt(Number.MAX_SAFE_INTEGER) + 2n);   // 9007199254740993n — exact where Number was not
console.log(typeof 1n);                              // bigint
console.log(5n / 2n, -7n / 2n);                      // 2n -3n — division truncates toward zero
console.log(BigInt("12345678901234567890"));         // 12345678901234567890n
```

The rules, per MDN:

- **No mixing** with `Number` in arithmetic — convert explicitly.
- **Comparisons** across types are allowed: `1n < 2` is `true`, `0n == 0` is `true`, and
  `0n === 0` is `false`.
- **No `Math` methods** — they throw.
- **JSON** — `JSON.stringify` throws on a `BigInt`.

```js
1n + 2;
// TypeError: Cannot mix BigInt and other types, use explicit conversions

Math.max(1n, 2n);
// TypeError: Cannot convert a BigInt value to a number

BigInt(1.5);
// RangeError: The number 1.5 cannot be converted to a BigInt because it is not an integer

JSON.stringify({ a: 1n });
// TypeError: Do not know how to serialize a BigInt
```

A replacer function is the usual workaround — serialize as a string:

```js
console.log(JSON.stringify({ a: 1n }, (key, value) =>
  typeof value === "bigint" ? value.toString() : value
));   // {"a":"1"}
```

Use `BigInt` for genuinely large integers — database IDs beyond 2⁵³, cryptography, exact
arithmetic — not for everyday counting, where `Number` is faster and works with `Math`.

## 🌐 Formatting Numbers for People

`toLocaleString` formats a number for a locale; the Intl APIs
([dates-and-intl.md](dates-and-intl.md)) give full control:

```js
console.log((1234567.891).toLocaleString("en-US"));   // 1,234,567.891
console.log((1234567.891).toLocaleString("de-DE"));   // 1.234.567,891
console.log((0.256).toLocaleString("en-US", { style: "percent" }));   // 26%
```

## 🎤 Interview Angle

- **"Why is `0.1 + 0.2 !== 0.3`?"** Numbers are binary floating-point doubles, and these decimals
  cannot be represented exactly; compare with a tolerance, or use integers (cents) for money.
- **"What is `Number.MAX_SAFE_INTEGER` and what happens beyond it?"** 2⁵³ − 1; larger integers lose
  precision, so use `BigInt`.
- **"Difference between `isNaN` and `Number.isNaN`?"** The global one coerces its argument first
  (`isNaN("NaN")` is `true`); `Number.isNaN` is `true` only for the actual `NaN`.
- **"Why not `Math.random()` for tokens?"** It isn't cryptographically secure; use
  `crypto.getRandomValues` or `crypto.randomUUID`.

## Common Mistakes

- **Comparing floating-point results with `===`.**
- **Using `Number.EPSILON` as an absolute tolerance for large numbers.**
- **Calculating money in floating-point instead of integer cents.**
- **Handling integers above 2⁵³ as `Number`** (IDs from other systems, for instance).
- **Trying to mix `BigInt` and `Number`**, or passing a `BigInt` to `Math` or `JSON.stringify`.
- **Using `parseInt` without a radix** on non-decimal input.

## ➡️ Next

Continue to [dates-and-intl.md](dates-and-intl.md) for JavaScript's date handling, whose quirks cause
some of the most expensive bugs in real applications, and the `Intl` APIs that format values for
people.
