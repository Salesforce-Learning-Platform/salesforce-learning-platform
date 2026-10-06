# 🔤 Strings and Unicode

## Text Is Not as Simple as "A Sequence of Characters"

[data-types.md](../introduction-to-javascript/data-types.md) introduced strings as a primitive type.
Most day-to-day string work needs nothing deeper — but the moment text contains emoji, accents, or
non-English scripts, the question "how long is this string?" stops having one answer. This file
covers the string methods worth knowing, then the Unicode details behind the surprises.

## 🧰 The Methods You Will Use Most

```js
const s = "  Hello, World  ";

console.log(s.trim().slice(-5));          // World — negative index counts from the end
console.log(s.trim().at(-1));             // d     — at() accepts negative positions
console.log("abc".includes("b"));         // true
console.log("abc".startsWith("ab"));      // true
console.log("7".padStart(2, "0"));        // 07
console.log("ab".repeat(3));              // ababab
console.log("a-b-c".replaceAll("-", "+")); // a+b+c
console.log("a,b".split(","));            // [ 'a', 'b' ]
console.log("Hello".substring(1, 3));     // el
console.log("Hello".slice(-3, -1));       // ll
```

| Task | Prefer |
|------|--------|
| Part of a string | `slice(start, end)` (supports negative indexes) |
| Search | `includes`, `startsWith`, `endsWith`, `indexOf` (returns `-1` if absent) |
| Pad or repeat | `padStart`, `padEnd`, `repeat` |
| Replace | `replace` (first match or regex), `replaceAll` |
| Split / join | `split(separator)` / `array.join(separator)` |
| Trim | `trim`, `trimStart`, `trimEnd` |

The older `substr` is a legacy method; use `slice` instead. For pattern matching see
[regular-expressions.md](../additional-javascript-topics/regular-expressions.md).

### Strings Are Immutable

Every method returns a **new** string; the original never changes, and you cannot assign into one:

```js
const s = "abc";
s[0] = "X";                       // ignored in sloppy mode
console.log(s, s.toUpperCase(), s);   // abc ABC abc
```

In [strict mode](../execution-context-and-hoisting/strict-mode.md) the assignment throws
`TypeError: Cannot assign to read only property '0' of string 'abc'`.

### Raw Strings

A tagged template with `String.raw` keeps backslashes literally — handy for Windows paths and
regular-expression source:

```js
console.log(String.raw`C:\new\table`);   // C:\new\table
console.log(`C:\new`.length);            // 5 — "\n" became ONE newline character
console.log(String.raw`C:\new`.length);  // 6 — all characters kept
```

## 🧬 What a String Actually Is: UTF-16 Code Units

MDN: JavaScript strings are sequences of **UTF-16 code units** — 16-bit values — and `length` counts
those code units, **not** what a reader would call characters. Most common characters fit in a single
code unit. Characters outside the Basic Multilingual Plane, including most emoji, need **two** — a
*surrogate pair*:

```js
console.log("A".length);        // 1
console.log("😀".length);       // 2   — one visible character, two code units
console.log([..."😀"].length);  // 1   — spreading iterates by code POINT
console.log("😀".codePointAt(0));          // 128512
console.log(String.fromCodePoint(128512)); // 😀
console.log("😀".split(""));    // [ '\ud83d', '\ude00' ] — split("") tears the pair in half
```

Three different notions of "a character" are in play:

| Unit | What it is | Tools |
|------|------------|-------|
| **Code unit** | One 16-bit value | `length`, `charAt`, `str[i]`, `split("")` |
| **Code point** | One Unicode character (1 or 2 code units) | `codePointAt`, `for...of`, `[...str]` |
| **Grapheme cluster** | What a user perceives as one character | `Intl.Segmenter` |

`for...of` and spread iterate by code point, which fixes surrogate pairs — but not everything a user
sees as one character is one code point. An emoji with a skin-tone modifier, or a family emoji built
from several emoji joined together, is *several* code points:

```js
const family = "👨‍👩‍👧";
const hand = "👉🏿";
const segmenter = new Intl.Segmenter("en", { granularity: "grapheme" });

console.log(family.length, [...family].length, [...segmenter.segment(family)].length);  // 8 5 1
console.log(hand.length, [...hand].length, [...segmenter.segment(hand)].length);        // 4 2 1
```

One visible character; 8 code units, 5 code points, 1 grapheme. For user-facing logic — truncating
text, counting "characters" for a limit, reversing a string — use **`Intl.Segmenter`** with
grapheme granularity. MDN lists it as Baseline since April 2024 (it may be missing in older
environments):

```js
const parts = [...new Intl.Segmenter("en", { granularity: "grapheme" }).segment("Hello👋World")];
console.log(parts.map((p) => p.segment).join("|"));   // H|e|l|l|o|👋|W|o|r|l|d
```

## 🔡 Accents and Normalization

The same visible text can be encoded two ways: a precomposed character, or a base letter plus a
combining mark. They look identical but are not `===`:

```js
const a = "\u00e9";      // é as a single code point
const b = "e\u0301";     // e followed by a combining acute accent

console.log(a.length, b.length);                              // 1 2
console.log(a === b);                                         // false
console.log(a.normalize("NFC") === b.normalize("NFC"));       // true
```

Call `normalize()` on both sides before comparing text that came from different sources
(user input, files, databases).

## 🌍 Sorting and Case: Use the Locale

The default comparison and the default `sort()` compare **code units**, not alphabet order:

```js
console.log(["b", "a", "C"].sort());                                  // [ 'C', 'a', 'b' ] — uppercase first
console.log(["b", "a", "C"].sort((x, y) => x.localeCompare(y)));      // [ 'a', 'b', 'C' ]
console.log(["z", "ä"].sort());                                       // [ 'z', 'ä' ]
console.log(["z", "ä"].sort((x, y) => x.localeCompare(y, "de")));     // [ 'ä', 'z' ]
console.log("Z" < "a");                                               // true
```

`localeCompare` (optionally with a locale) gives language-aware ordering. Case conversion has its own
language rules:

```js
console.log("ß".toUpperCase());               // SS — one letter becomes two
console.log("i".toLocaleUpperCase("tr"));     // İ  — Turkish has a dotted capital I
```

## 🔎 Searching Returns Positions, Not Booleans

```js
console.log("hello".indexOf("z"));        // -1  — not found
console.log("hello".indexOf("l"));        // 2   — first match
console.log("hello".lastIndexOf("l"));    // 3
console.log("hello"[10]);                 // undefined
console.log("hello".charAt(10) === "");   // true
```

Beware `if (str.indexOf(x))` — `0` (found at the start) is falsy and `-1` (not found) is truthy; use
`includes` or compare against `-1`.

## 🎤 Interview Angle

- **"Why is `'😀'.length` equal to 2?"** `length` counts UTF-16 code units, and this emoji is a
  surrogate pair of two.
- **"How do you reverse a string correctly?"** Not with `split("")` — that splits surrogate pairs.
  Iterate by code point (`[...str]`) at minimum, and by grapheme cluster (`Intl.Segmenter`) to be
  safe with combined emoji.
- **"Are strings mutable?"** No — every string method returns a new string.
- **"Why does `['b','a','C'].sort()` put `'C'` first?"** The default sort compares code units, and
  uppercase letters have lower values than lowercase; use `localeCompare`.

## Common Mistakes

- **Using `str.length` as a visible-character count** for text that may contain emoji or accents.
- **Splitting or slicing in the middle of a surrogate pair**, producing broken characters.
- **Comparing strings from different sources without `normalize()`.**
- **Sorting user-facing text with the default `sort()`.**
- **Testing `indexOf(...)` for truthiness.**

## ➡️ Next

Continue to [numbers-math-and-bigint.md](numbers-math-and-bigint.md) for the other primitive with
famous surprises — floating-point arithmetic.
