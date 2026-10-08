# ➕ Logical Assignment and Numeric Separators

## Two Small Syntax Features That Remove Everyday Boilerplate

The rest of this module covers features you will see in almost every modern codebase. These two are small
but remove real clutter: **logical assignment operators** (`||=`, `&&=`, `??=`) that combine a logical
operator with assignment, and **numeric separators** (`1_000_000`) that make big numbers readable. MDN
lists the logical assignment operators as Baseline *widely available* (working across browsers since
September 2020). Everything below was run in Node.js 24 and a real browser.

## 🔀 Logical Assignment Operators

You already know `x += 1` as shorthand for `x = x + 1`. The logical operators have the same shorthand:

| Operator | Reads as | Assigns the right side when the left side is… |
|----------|----------|-----------------------------------------------|
| `a \|\|= b` | `a \|\| (a = b)` | **falsy** |
| `a &&= b` | `a && (a = b)` | **truthy** |
| `a ??= b` | `a ?? (a = b)` | **`null` or `undefined`** |

```js
let a = 0, b = "", c = null, d = "set", e = true;

a ||= 10;              // a was falsy (0)        → 10
b ||= "default";       // b was falsy ("")       → "default"
c ??= "filled";        // c was null             → "filled"
d ??= "unused";        // d was not nullish      → stays "set"
e &&= "kept truthy";   // e was truthy           → "kept truthy"

console.log(a, b, c, d, e);   // 10 default filled set kept truthy
```

### `||=` vs. `??=`: Falsy Is Not the Same as Missing

This is the decision that matters. `||=` treats *every* falsy value (`0`, `""`, `false`, `NaN`) as
"missing"; `??=` treats only `null` and `undefined` as missing — the distinction explained in
[truthy-and-falsy.md](../operators-and-type-system/truthy-and-falsy.md) and in
[optional-chaining-and-nullish-coalescing.md](optional-chaining-and-nullish-coalescing.md):

```js
let count = 0, name = "";

let c1 = count; c1 ||= 10;      // 10   — a deliberate zero was overwritten!
let c2 = count; c2 ??= 10;      // 0    — the zero is kept
let n1 = name;  n1 ||= "Anonymous";   // "Anonymous" — an intentionally empty string was replaced
let n2 = name;  n2 ??= "Anonymous";   // ""          — kept
```

For defaults, **prefer `??=`** unless you genuinely want to replace every falsy value. A settings object
shows why:

```js
function config(options) {
  options.duration ??= 100;
  options.speed ??= 25;
  return options;
}

config({ duration: 125 });   // { duration: 125, speed: 25 }
config({});                  // { duration: 100, speed: 25 }
config({ duration: 0 });     // { duration: 0, speed: 25 }  — a zero duration is respected
```

### Short-Circuiting: Not Just Shorthand

`a ||= b` is **not** the same as `a = a || b`, and MDN calls the difference out. The logical-assignment
operators short-circuit: if the left side already satisfies the condition, the right side is not
evaluated and **no assignment happens at all**. That matters whenever assignment has effects, such as a
setter:

```js
const log = [];
const obj = {
  _v: "present",
  get v() { log.push("get"); return this._v; },
  set v(x) { log.push("set " + x); this._v = x; },
};

obj.v ||= "fallback";            // v is truthy → read once, setter NOT called
obj.v = obj.v || "fallback";     // always writes back, calling the setter

console.log(log);                // [ 'get', 'get', 'set present' ]
```

The first line produced a single `get`; only the long form triggered `set`. The same property explains a
`const` edge case: because no assignment occurs when the left side is truthy, this does not throw,
whereas the long form does:

```js
const x = 1;
x ||= 2;          // no error, x is still 1 (no assignment was attempted)

const y = 1;
y = y || 2;       // TypeError: Assignment to constant variable.
```

(Had `x` been falsy, `x ||= 2` would try to assign and throw too.) The right-hand side is also evaluated
lazily, which makes these operators a tidy way to initialize something expensive only once:

```js
const cache = {};
let computed = 0;
const compute = () => { computed++; return 42; };

cache.value ??= compute();
cache.value ??= compute();         // already set → compute() is not called again
console.log(cache.value, computed);   // 42 1
```

### When to Use Which

| Goal | Use |
|------|-----|
| Fill in a missing option or default (`undefined`/`null` only) | `??=` |
| Replace any "empty" value (`0`, `""`, `false`) with a fallback | `\|\|=` |
| Update a value only when it is already truthy (guard `null`/`0`) | `&&=` |
| Lazy, once-only initialization | `??=` |

## 🔢 Numeric Separators

Large numeric literals are hard to read: is `1000000000` a million or a billion? An underscore can be used
as a visual separator **inside** a numeric literal. It has no effect on the value:

```js
console.log(1_000_000);              // 1000000
console.log(1_000_000 === 1000000);  // true
console.log(3.141_592);              // 3.141592
console.log(0b1010_0001);            // 161   — binary, grouped in nibbles
console.log(0xA0_B0_C0);             // 10531008 — hex, grouped in bytes
console.log(1_000n);                 // 1000n — works with BigInt
console.log(1e1_0);                  // 10000000000
```

### Where Separators Are Not Allowed

MDN lists the restrictions, and the engine reports each with a `SyntaxError`:

```js
100__000   // SyntaxError: Only one underscore is allowed as numeric separator
100_       // SyntaxError: Numeric separators are not allowed at the end of numeric literals
0_1        // SyntaxError: Numeric separator can not be used after leading 0.
1_.5       // SyntaxError: Numeric separators are not allowed at the end of numeric literals
1._5       // SyntaxError: Invalid or unexpected token
```

(Messages are V8's wording.) Notice the last two: the separator must sit *between two digits* — not next
to the decimal point. And a leading underscore is not a separator at all, it is an identifier:

```js
_100       // ReferenceError: _100 is not defined   — parsed as a variable name
```

### Literals Only — Not Strings

Separators exist for **source code**. They are not part of the number format that string conversion
understands:

```js
console.log(Number("1_000"));        // NaN
console.log(parseInt("1_000"));      // 1      — parsing stops at the underscore
console.log(parseFloat("1_000.5"));  // 1
console.log(+"1_000");               // NaN
```

So never use separators in data you parse (CSV, JSON, user input); use them only for constants in code,
such as timeouts (`const TIMEOUT_MS = 30_000;`), byte sizes (`const MAX_UPLOAD = 5_242_880;`), or limits
(`const MAX_SAFE = 9_007_199_254_740_991;`). See [numbers-math-and-bigint.md](../built-in-objects-and-collections/numbers-math-and-bigint.md)
for the numeric limits themselves.

## 🛠️ Running on Older Targets

Both features are syntax, so a [transpiler](../how-javascript-runs/transpilers-polyfills-and-browser-support.md)
can rewrite them for older browsers: logical assignment becomes the equivalent `a || (a = b)` form, and
separators are simply stripped from the literal. If your declared targets already support them, nothing is
rewritten.

## 🎤 Interview Angle

- **"What does `a ||= b` do?"** Assigns `b` to `a` only if `a` is falsy — equivalent to `a || (a = b)`,
  not `a = a || b`.
- **"`??=` vs. `||=`?"** `??=` assigns only when the left side is `null`/`undefined`; `||=` assigns for
  any falsy value, including `0` and `""`.
- **"Why does `a ||= b` not trigger a setter when `a` is truthy?"** It short-circuits and performs no
  assignment.
- **"What are numeric separators?"** Underscores in numeric literals for readability; they don't change
  the value and are not recognized by `Number()`/`parseInt()`.

## Common Mistakes

- **Using `||=` for defaults** and overwriting legitimate `0`, `""`, or `false`.
- **Assuming `a ||= b` always assigns.**
- **Placing a separator next to the decimal point, at the end, or after a leading `0`.**
- **Putting separators in strings** that you later convert with `Number()`.
- **Using `&&=` where `if` would read more clearly.**

## ➡️ Next

Continue to [modern-array-and-object-methods.md](modern-array-and-object-methods.md) for the newer built-in
methods that replace several common workarounds.
