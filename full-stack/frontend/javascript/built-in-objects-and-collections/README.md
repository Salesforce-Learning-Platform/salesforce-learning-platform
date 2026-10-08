# 🧰 Built-in Objects and Collections

## 📚 Overview

This module covers the standard-library building blocks that real programs lean on every day beyond
plain objects and arrays: `Map` and `Set`, weak collections, strings and the Unicode details behind
their surprises, numbers and `BigInt`, dates and the `Intl` formatting APIs, and typed arrays for raw
bytes. Each topic focuses on what the built-in actually guarantees — and on the quirks that cause
real bugs and frequent interview questions.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Choose between `Map`, `Set`, objects, and arrays, and explain SameValueZero equality and insertion
  order.
- Use `WeakMap` and `WeakSet` to attach data to objects without leaking memory, and explain why
  `WeakRef` is rarely the right tool.
- Explain why `"😀".length` is 2, and use code points, grapheme clusters (`Intl.Segmenter`),
  `normalize`, and `localeCompare` correctly.
- Explain floating-point behavior, compare numbers with a sensible tolerance, handle money with
  integers, and know when `BigInt` is required.
- Avoid the `Date` traps — zero-based months, UTC versus local parsing, DST, and silent overflow —
  and format values with `Intl`.
- Work with `ArrayBuffer`, typed arrays, `DataView`, and `TextEncoder`, including byte order and
  wrap-around.

## 📋 Prerequisites

- [Data Types](../introduction-to-javascript/data-types.md) — the primitive types this module examines more closely.
- [Arrays](../arrays-and-objects/arrays.md) and [Objects](../arrays-and-objects/objects.md) — the baseline collections `Map` and `Set` improve on.
- [Objects in Depth](../objects-in-depth/) — JSON behavior and shallow-versus-deep copying are referenced throughout.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [map-and-set.md](map-and-set.md) | `Map` and `Set`: key equality, ordering, comparison with objects, set operations, and performance |
| [weakmap-weakset-and-weakref.md](weakmap-weakset-and-weakref.md) | Weak collections, leak-free metadata, and why `WeakRef` is a last resort |
| [strings-and-unicode.md](strings-and-unicode.md) | String methods, UTF-16 code units, code points, grapheme clusters, normalization, and locale-aware sorting |
| [numbers-math-and-bigint.md](numbers-math-and-bigint.md) | Floating-point behavior, `NaN`, rounding, secure randomness, and `BigInt` |
| [dates-and-intl.md](dates-and-intl.md) | `Date` traps, time zones, and the `Intl` formatting APIs |
| [typed-arrays-and-binary-data.md](typed-arrays-and-binary-data.md) | `ArrayBuffer`, typed arrays, `DataView`, `TextEncoder`, and Base64; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** the strings, numbers, and dates files if you are preparing for interviews or work on
anything user-facing — floating-point surprises, Unicode length, and date-parsing off-by-one bugs are
among the most common sources of real defects and of "what does this print?" questions.

**Skim** the typed-arrays file unless you work with files, binary protocols, canvas, or WebAssembly —
but read its `TextEncoder` and Base64 sections, which matter for any text that crosses a network or
storage boundary.

## 🧠 Knowledge Check

<details>
<summary>Why does <code>new Date("2024-01-15").getDate()</code> return 14 in New York?</summary>

A date-only ISO string is interpreted as **UTC** midnight. In a time zone behind UTC — New York is
five hours behind in January — that instant is still the evening of January 14th locally, and
`getDate()` reads the *local* calendar day. A date-time string with no offset, such as
`"2024-01-15T00:00:00"`, is parsed as local time instead, which is why the two forms can disagree.

</details>

<details>
<summary>Why does a <code>Map</code> avoid a bug that a plain object has when counting words?</summary>

A plain object inherits keys from `Object.prototype`, so `counts["constructor"]` finds the inherited
`Object` constructor function instead of `undefined`, and `(counts[word] || 0) + 1` produces a string
instead of a count. A `Map` starts empty and has no inherited keys, so every word is looked up only in
the entries you added.

</details>

## 📚 References

- [MDN: `Map`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map) and [`Set`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set) — equality, ordering, set-composition methods, and the Map-versus-Object comparison.
- [MDN: `WeakMap`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakMap) and [`WeakRef`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakRef) — valid keys, use cases, and the guidance to avoid `WeakRef`.
- [MDN: `String`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String) and [`Intl.Segmenter`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Segmenter) — UTF-16, code points, and grapheme segmentation.
- [MDN: `Number`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number), [`Math.random()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random), and [`BigInt`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt) — floating-point, secure randomness, and BigInt rules.
- [MDN: `Date`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date) and [`Temporal`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Temporal) — the epoch model, parsing rules, and the replacement API's status.
- [MDN: JavaScript typed arrays](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Typed_arrays) and [`TextEncoder`](https://developer.mozilla.org/en-US/docs/Web/API/TextEncoder) — buffers, views, endianness, and UTF-8 encoding.
- [javascript.info: Map and Set](https://javascript.info/map-set), [WeakMap and WeakSet](https://javascript.info/weakmap-weakset), [Date and time](https://javascript.info/date), and [ArrayBuffer, binary arrays](https://javascript.info/arraybuffer-binary-arrays) — widely used walkthroughs.
- [W3Schools: JavaScript Maps](https://www.w3schools.com/js/js_maps.asp) and [JavaScript Dates](https://www.w3schools.com/js/js_dates.asp) — beginner-friendly overviews.

## ➡️ Continue Your Learning Path

Continue to the Advanced Asynchronous Patterns module, the next module in this section, which builds
on promises and the event loop with combinators, cancellation, async iteration, scheduling, and Web
Workers.
