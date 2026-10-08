# 🔀 Type Coercion and Equality Puzzles

## 🧩 What These Puzzles Test

JavaScript converts values between types automatically — in arithmetic, comparisons, conditions, and string
building. Interview puzzles about it look like random trivia (`[] + {}`, `null >= 0`), but every answer
follows a small set of rules:

- `+` concatenates if **either side becomes a string**; every other arithmetic operator converts to numbers.
- `==` follows a conversion algorithm; `===` never converts.
- Objects become primitives through `valueOf` and `toString` (or `Symbol.toPrimitive`).
- Relational operators (`<`, `>=`) convert differently from `==`.

The thirteen puzzles below practise those rules. Every answer was **produced by running the code** (three
times, to confirm it is stable). The point is not to memorise results — it is to be able to *derive* them.

## 🛠️ How to Use This File

1. **Cover the answer** and predict the output of every line.
2. **For each operator, ask which rule applies**: is this `+` with a string? Is this `==` or `===`? Is an
   object involved?
3. **Compare** and, for each miss, write down the rule you forgot.

Output blocks show Node.js 24 formatting. The concept files behind these puzzles are
[type-coercion.md](../operators-and-type-system/type-coercion.md),
[operators.md](../operators-and-type-system/operators.md),
[truthy-and-falsy.md](../operators-and-type-system/truthy-and-falsy.md), and
[data-types.md](../introduction-to-javascript/data-types.md).

## 🧪 The Puzzles

### Puzzle 1 — Plus has two jobs

*Difficulty: ⭐ Warm-up*

```js
console.log(1 + "2");
console.log("3" - 1);
console.log("3" + 1 - 1);
console.log(1 + 2 + "3");
console.log("1" + 2 + 3);
console.log(+"", +" ", +"1e3", +"0x10", +"12px");
console.log("b" + "a" + +"a" + "a");
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
12
2
30
33
123
0 0 1000 16 NaN
baNaNa
```

The `+` operator has two meanings. If **either operand is a string** (after converting objects), it
concatenates; otherwise it adds numbers. Every other arithmetic operator (`-`, `*`, `/`) always converts
both sides to numbers.

- `1 + "2"` → `"12"` (string wins); `"3" - 1` → `2` (subtraction is always numeric).
- `"3" + 1 - 1` evaluates left to right: `"3" + 1` is `"31"`, then `"31" - 1` is `30`.
- `1 + 2 + "3"` is `(1 + 2) + "3"` → `"33"`, but `"1" + 2 + 3` is `("1" + 2) + 3` → `"123"`. Left to right
  decides when the string enters.
- The unary `+` converts to a number: an empty or whitespace-only string is `0`, `"1e3"` is `1000`,
  `"0x10"` is `16`, and `"12px"` is `NaN` (the whole string must be numeric, unlike `parseInt`).
- The last line is the famous one: `"b" + "a"` is `"ba"`, `+"a"` is `NaN`, and `"ba" + NaN` becomes
  `"baNaN"`, then `+ "a"` gives `"baNaNa"`.

See [type-coercion.md](../operators-and-type-system/type-coercion.md) ("Why `+` and `-` Behave Differently").

</details>

### Puzzle 2 — The equality table

*Difficulty: ⭐⭐ Interview standard*

```js
console.log(null == undefined);
console.log(null == 0);
console.log(undefined == 0);
console.log(NaN == NaN);
console.log("0" == false);
console.log("" == 0);
console.log([] == false);
console.log([] == ![]);
console.log("1" == 1);
console.log(null === undefined);
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
true
false
false
false
true
true
true
true
true
false
```

Loose equality (`==`) has a few special rules worth knowing:

- `null == undefined` is `true`, and **neither equals anything else** under `==` — so `null == 0` and
  `undefined == 0` are `false`.
- `NaN` is not equal to anything, including itself.
- When types differ and neither side is `null`/`undefined`, booleans and strings are converted **to
  numbers**: `"0" == false` becomes `0 == 0`; `"" == 0` becomes `0 == 0`; `"1" == 1` becomes `1 == 1`.
- An object compared to a primitive is converted to a primitive first: `[]` becomes `""`, then `0`, so
  `[] == false` is `0 == 0` → `true`.
- `[] == ![]` looks impossible. `![]` is `false` (arrays are truthy), so it is `[] == false`, which is `true`
  by the previous rule.

`===` performs no conversion, so `null === undefined` is `false`. The practical advice: **use `===`** and
convert deliberately; the one common exception is `x == null`, which checks for both `null` and `undefined`
in one test. See [type-coercion.md](../operators-and-type-system/type-coercion.md) ("`==` Performs Coercion;
`===` Does Not").

</details>

### Puzzle 3 — Arrays and objects in expressions

*Difficulty: ⭐⭐ Interview standard*

```js
console.log(JSON.stringify([] + []));
console.log(JSON.stringify([] + {}));
console.log(JSON.stringify([1, 2] + [3]));
console.log(Number([]), Number([5]), Number([1, 2]), Number({}));
console.log([] == 0, [0] == false, [1] == 1, [[]] == 0);
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
""
"[object Object]"
"1,23"
0 5 NaN NaN
true true true true
```

Arrays and plain objects are converted to primitives before `+` or `==` can use them, via their
`toString` method:

- `[].toString()` is `""`, `({}).toString()` is `"[object Object]"`, and `[1, 2].toString()` is `"1,2"`. So
  `[] + []` is `""`, `[] + {}` is `"[object Object]"`, and `[1, 2] + [3]` is `"1,23"`. (`JSON.stringify` is
  used above so that the empty string is visible.)
- `Number(array)` converts through that string: `""` → `0`, `"5"` → `5`, `"1,2"` → `NaN`; `Number({})` is
  `NaN` because `"[object Object]"` is not numeric.
- The same logic explains the comparisons: `[]` → `""` → `0`; `[0]` → `"0"` → `0`; `[1]` → `1`; and `[[]]`
  → `""` → `0`, so all four are `true`.

You will never write this in real code, but explaining it step by step — "the object becomes a string, the
string becomes a number" — is exactly what an interviewer wants to hear.

</details>

### Puzzle 4 — How objects become primitives

*Difficulty: ⭐⭐⭐ Tricky*

```js
const price = {
  valueOf() {
    return 10;
  },
  toString() {
    return "ten";
  },
};

console.log(price + 5);
console.log(`${price}`);
console.log(price * 2);
console.log(String(price));
console.log(price + "", typeof (price + ""));
console.log(price > 9);
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
15
ten
20
ten
10 string
true
```

When an object meets an operator, the engine asks it for a primitive with a **hint** — `"number"`,
`"string"`, or `"default"`. For ordinary objects, the hint decides the order of attempts: `"string"` tries
`toString()` first; `"number"` and `"default"` try `valueOf()` first.

- `price + 5` uses the default hint → `valueOf()` → `10 + 5` → `15`.
- A template literal and `String(price)` ask for a string → `toString()` → `"ten"`.
- `price * 2` and `price > 9` ask for numbers → `valueOf()` → `20` and `true`.
- `price + ""` surprises people: `+` uses the **default** hint, so it calls `valueOf()` (`10`) and *then*
  concatenates, giving the string `"10"` — not `"ten"`.

A `Symbol.toPrimitive` method overrides all of this and receives the hint directly (the variation prints each
branch: `42`, `forty-two`, `default:42`, and `42`). `Date` objects are special: their default hint is
`"string"`, so `date + 1` concatenates (a string) while `date - 1` is numeric. See
[symbols.md](../additional-javascript-topics/symbols.md).

**Variation — Symbol.toPrimitive and Date**

```js
const money = {
  [Symbol.toPrimitive](hint) {
    return hint === "number" ? 42 : hint === "string" ? "forty-two" : "default:42";
  },
};

console.log(+money, `${money}`, money + "", money * 1);
console.log(typeof (new Date(0) + 1), typeof (new Date(0) - 1));
```

```text
42 forty-two default:42 42
string number
```

</details>

### Puzzle 5 — Comparing with < and >=

*Difficulty: ⭐⭐⭐ Tricky*

```js
console.log("10" < "9");
console.log(10 < "9");
console.log("B" < "a");
console.log("abc" < "abd");
console.log(null >= 0, null > 0, null == 0);
console.log(undefined >= 0, undefined == 0);
console.log(NaN <= NaN);
console.log([2] > 1);
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
true
false
true
true
true false false
false false
false
true
```

Relational operators use their own conversion rules, separate from `==`:

- **Two strings** are compared character by character in code-unit order, not as numbers: `"10" < "9"` is
  `true` because `"1"` comes before `"9"`; `"B" < "a"` is `true` because uppercase letters have lower codes.
- **Anything else** is converted to numbers: `10 < "9"` becomes `10 < 9` → `false`.
- `null` converts to `0` for relational comparisons, so `null >= 0` is `true` and `null > 0` is `false` —
  yet `null == 0` is `false`, because `==` has its own `null` rule. This three-way mismatch is the classic
  trap.
- `undefined` converts to `NaN`, and any comparison with `NaN` is `false`: `undefined >= 0` is `false`
  (while `undefined == 0` is also `false`), and `NaN <= NaN` is `false`.
- `[2] > 1` converts `[2]` → `"2"` → `2`, so it is `true`.

The safe habit: compare values of the same type, and convert explicitly (`Number(x)`) when you mean numbers.

</details>

### Puzzle 6 — The default sort

*Difficulty: ⭐⭐ Interview standard*

```js
console.log([10, 9, 1, 100].sort());
console.log(["b", "a", "C"].sort());
console.log([3, 1, 2].sort((a, b) => b - a));
console.log([undefined, 3, null, 1].sort());
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
[ 1, 10, 100, 9 ]
[ 'C', 'a', 'b' ]
[ 3, 2, 1 ]
[ 1, 3, null, undefined ]
```

Without a comparator, `sort` converts elements to **strings** and compares them in code-unit order:
`"1" < "10" < "100" < "9"`, so the numbers come out as `[1, 10, 100, 9]`, and `"C"` sorts before `"a"` because
uppercase letters come first. A comparator such as `(a, b) => b - a` compares numerically (descending
here). `undefined` elements are always moved to the end; `null` is compared as the string `"null"`, so it
sorts after `"3"`. Sorting also **mutates** the array — see
[modern-array-and-object-methods.md](../modern-javascript/modern-array-and-object-methods.md) for `toSorted()`
and [array-methods.md](../arrays-and-objects/array-methods.md).

</details>

### Puzzle 7 — What typeof says

*Difficulty: ⭐ Warm-up*

```js
console.log(typeof null, typeof undefined, typeof NaN);
console.log(typeof [], typeof function () {}, typeof class {});
console.log(typeof Symbol(), typeof 10n, typeof undeclaredName);
console.log(typeof new String("x"), typeof String("x"), typeof Date());
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
object undefined number
object function function
symbol bigint undefined
object string string
```

- `typeof null` is `"object"` — a historical quirk that cannot be fixed without breaking the web. Test for
  `null` with `=== null`.
- `typeof NaN` is `"number"`: `NaN` is a numeric value meaning "not a valid number."
- Arrays are objects (`"object"`); use `Array.isArray()` to tell them apart. Functions and classes report
  `"function"`.
- `typeof` on an **undeclared** name returns `"undefined"` instead of throwing.
- `new String("x")` creates a wrapper **object**, so `typeof` gives `"object"`, while calling `String("x")`
  as a plain function converts to a primitive string. `Date()` without `new` returns a string too.

See [data-types.md](../introduction-to-javascript/data-types.md).

</details>

### Puzzle 8 — Floating-point and big numbers

*Difficulty: ⭐⭐ Interview standard*

```js
console.log(0.1 + 0.2);
console.log(0.1 + 0.2 === 0.3);
console.log(Math.abs(0.1 + 0.2 - 0.3) < Number.EPSILON);
console.log(2 ** 53 === 2 ** 53 + 1);
console.log((0.1 * 3).toFixed(2), (1.005).toFixed(2));
console.log(9007199254740993, Number.MAX_SAFE_INTEGER);
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
0.30000000000000004
false
true
true
0.30 1.00
9007199254740992 9007199254740991
```

JavaScript numbers are 64-bit binary floating-point values (IEEE 754). Many decimal fractions such as `0.1`
cannot be represented exactly, so `0.1 + 0.2` is `0.30000000000000004` and the `===` comparison with `0.3`
fails. Compare with a tolerance (`Number.EPSILON`) instead.

The same representation limits whole numbers: above `2 ** 53`, not every integer exists, so `2 ** 53 + 1`
rounds back to `2 ** 53` and the literal `9007199254740993` is displayed as `9007199254740992`. Use
`BigInt` for exact large integers. `(1.005).toFixed(2)` giving `"1.00"` rather than `"1.01"` is the same
effect: the stored value is slightly below `1.005`. See
[numbers-math-and-bigint.md](../built-in-objects-and-collections/numbers-math-and-bigint.md).

</details>

### Puzzle 9 — parseInt, Number, and map

*Difficulty: ⭐⭐⭐ Tricky*

```js
console.log(parseInt("08"), parseInt("12px"), Number("12px"));
console.log(parseInt(0.0000005), parseInt("0x1f"), parseInt("101", 2));
console.log(["10", "10", "10"].map(parseInt));
console.log(["10", "10", "10"].map(Number));
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
8 12 NaN
5 31 5
[ 10, NaN, 2 ]
[ 10, 10, 10 ]
```

`parseInt` reads as many leading digits as it can and stops at the first invalid character, so
`parseInt("12px")` is `12`, whereas `Number("12px")` requires the whole string to be numeric and gives
`NaN`. `parseInt` also understands `0x` hex prefixes and accepts a radix as its second argument.

`parseInt(0.0000005)` is `5` because it first converts the number to a *string*, which is `"5e-7"`, and parses
the leading `5`.

The `map(parseInt)` result `[10, NaN, 2]` is the best-known puzzle in the file. `map` passes **three**
arguments to its callback — `(value, index, array)` — and `parseInt` interprets the second as the **radix**.
So the calls are `parseInt("10", 0)` (radix `0` means default → `10`), `parseInt("10", 1)` (radix `1` is
invalid → `NaN`), and `parseInt("10", 2)` (binary → `2`). `Number` ignores the extra arguments, so
`map(Number)` works. Write `map((s) => parseInt(s, 10))` when you need `parseInt`.

</details>

### Puzzle 10 — Truthy and falsy surprises

*Difficulty: ⭐⭐ Interview standard*

```js
console.log(Boolean("false"), Boolean(" "), Boolean([]), Boolean({}));
console.log(Boolean(0), Boolean(-0), Boolean(0n), Boolean(""), Boolean(NaN));
console.log(Boolean(new Boolean(false)));
if (new Boolean(false)) {
  console.log("a wrapper object is always truthy");
}
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
true true true true
false false false false false
true
a wrapper object is always truthy
```

The falsy values are a short, fixed list: `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined`, and `NaN` (plus
the legacy `document.all`). **Everything else is truthy** — including the string `"false"`, a string
containing only a space, empty arrays, and empty objects.

`new Boolean(false)` is a wrapper *object*, and every object is truthy, so both the `Boolean(...)` call and
the `if` treat it as `true`. This is one of several reasons to avoid wrapper constructors (`new Number`,
`new String`, `new Boolean`). To check for an empty array, test `array.length`, not the array itself. See
[truthy-and-falsy.md](../operators-and-type-system/truthy-and-falsy.md).

</details>

### Puzzle 11 — Strict equality, Object.is, and NaN

*Difficulty: ⭐⭐ Interview standard*

```js
console.log(NaN === NaN, Object.is(NaN, NaN));
console.log(0 === -0, Object.is(0, -0));
console.log([NaN].includes(NaN), [NaN].indexOf(NaN));
console.log(new Set([NaN, NaN, 0, -0]).size);
console.log(1 / 0, -1 / 0, 1 / -0);
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
false true
true false
true -1
2
Infinity -Infinity -Infinity
```

`===` has two exceptions: `NaN === NaN` is `false`, and `0 === -0` is `true`. `Object.is` fixes both: it treats
`NaN` as equal to itself and distinguishes `0` from `-0` (the sign is visible through division: `1 / -0`
is `-Infinity`).

Library methods differ in which comparison they use. `indexOf` uses `===`, so it can never find `NaN`
(`-1`); `includes`, `Set`, and `Map` use the "same-value-zero" comparison, which treats `NaN` as equal to
itself but, like `===`, treats `0` and `-0` as equal. That is why the `Set` above holds only two values: `NaN`
and `0`.

</details>

### Puzzle 12 — Operators that return operands

*Difficulty: ⭐⭐ Interview standard*

```js
console.log([0 || "fallback", "" ?? "fallback", null ?? "fallback", 1 && 2 && 3, 1 && 0 && 3]);
console.log([null || undefined, undefined || null, false ?? true, 0 ?? 1]);

const user = { name: "", age: 0 };
console.log([user.name || "Anonymous", user.name ?? "Anonymous"]);
console.log([user.age || 18, user.age ?? 18]);
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
[ 'fallback', '', 'fallback', 3, 0 ]
[ undefined, null, false, 0 ]
[ 'Anonymous', '' ]
[ 18, 0 ]
```

`||`, `&&`, and `??` do not return booleans; they return **one of their operands**.

- `a || b` returns `a` if it is truthy, otherwise `b`. `a && b` returns `a` if it is falsy, otherwise `b`,
  so `1 && 2 && 3` is `3` and `1 && 0 && 3` is `0`.
- `a ?? b` returns `b` only when `a` is `null` or `undefined`. It keeps `""`, `0`, and `false`.

This difference matters for defaults. `user.age || 18` replaces a legitimate age of `0` with `18`, while
`user.age ?? 18` keeps it. Choose `??` for "missing," `||` for "empty or falsy." See
[optional-chaining-and-nullish-coalescing.md](../modern-javascript/optional-chaining-and-nullish-coalescing.md).

</details>

### Puzzle 13 — BigInt does not mix

*Difficulty: ⭐⭐ Interview standard*

```js
console.log(typeof 1n, 1n == 1, 1n === 1, 2n > 1, 1n + 2n);

try {
  console.log(1n + 1);
} catch (e) {
  console.log(e.name + ": " + e.message);
}

console.log(Number(2n) + 1, BigInt(2) + 1n, 5n / 2n);
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
bigint true false true 3n
TypeError: Cannot mix BigInt and other types, use explicit conversions
3 3n 2n
```

`BigInt` is a separate type. Loose equality and relational comparison compare *mathematical values* across
types (`1n == 1` and `2n > 1` are `true`), but strict equality sees different types (`1n === 1` is `false`).
Arithmetic refuses to guess: mixing a `BigInt` and a `Number` in `+` throws a `TypeError` rather than risk
losing precision, so you must convert explicitly. BigInt division truncates (`5n / 2n` is `2n`). See
[numbers-math-and-bigint.md](../built-in-objects-and-collections/numbers-math-and-bigint.md).

</details>

## 🧭 Patterns to Remember

| Pattern in the question | Rule to apply |
|-------------------------|---------------|
| `a + b` where either side is a string or object | Concatenation (objects convert to primitives first) |
| `-`, `*`, `/` with strings | Numeric conversion |
| `==` with `null` or `undefined` | Equal only to each other |
| `==` with booleans/strings against numbers | Converted to numbers |
| Object compared or added | `valueOf`/`toString` (or `Symbol.toPrimitive`), by hint |
| `<`, `>=` with two strings | Compared as text, not numbers |
| `<`, `>=` with `null`/`undefined` | `null` → `0`, `undefined` → `NaN` |
| Default `sort()` | Compares as strings |
| `map(parseInt)` | The index becomes the radix |
| `||` vs. `??` | Falsy vs. only `null`/`undefined` |

## 🎤 Interview Angle

- **Lead with the rule, not the result.** "`+` concatenates if either side is a string, so …" is a stronger
  answer than naming the output.
- **Give the practical conclusion.** After explaining a quirk, say what you do in real code: `===`,
  explicit `Number()`/`String()` conversions, `??` for defaults, comparator functions for `sort`.
- **Know `x == null`** as the one idiomatic use of loose equality.
- **Be ready to explain `0.1 + 0.2`** with "IEEE 754 binary floating point," and to name the remedies:
  tolerance comparison, integer cents, or `BigInt`/decimal libraries.

## Common Mistakes

- **Trusting `+` with user input** — form values are strings, so `"5" + 3` is `"53"`.
- **Using `||` for defaults** when `0`, `""`, or `false` are valid values.
- **Sorting numbers without a comparator.**
- **Passing `parseInt` directly to `map`.**
- **Testing for an array with `typeof`**, or for `null` with `typeof`.
- **Using `indexOf` to find `NaN`.**

## ➡️ Next

Continue to [event-loop-ordering-puzzles.md](event-loop-ordering-puzzles.md), the final puzzle file, where
the question is *when* each piece of code runs.
