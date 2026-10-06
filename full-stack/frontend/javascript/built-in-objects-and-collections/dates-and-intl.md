# 📅 Dates and Intl

## The Built-In With the Most Surprising Behavior

Dates look simple and cause some of the costliest bugs in software: off-by-one days, wrong months,
times that shift when a user travels or the clocks change. JavaScript's `Date` object has several
well-known quirks. MDN itself describes `Date` as a legacy feature and recommends the newer
`Temporal` API for new code — but `Temporal` is not yet available everywhere (more below), so
understanding `Date` remains essential. This file covers how `Date` really works, its traps, and the
`Intl` APIs that format dates, numbers, and lists correctly for any locale.

## 🕰️ What a `Date` Holds

A `Date` stores a **single number**: milliseconds since January 1, 1970, 00:00:00 UTC (the *epoch*).
That number identifies one instant in history, independent of any time zone. Time zones only matter
when you *read* the instant as a year, month, and day — or *parse* a string into one.

```js
console.log(new Date(0).toISOString());   // 1970-01-01T00:00:00.000Z
console.log(typeof Date.now());           // number — the current time in milliseconds
```

`Date` offers parallel method families: local-time getters (`getFullYear`, `getMonth`, `getDate`,
`getHours`) and UTC getters (`getUTCFullYear`, `getUTCMonth`, …).

## 🪤 Trap 1: Months Are Zero-Based

```js
const d = new Date(2024, 0, 15);          // January 15, 2024 — month 0 is January
console.log(d.getMonth());                // 0
console.log(d.getDate());                 // 15 — the day of the month (1–31)
console.log(d.getDay());                  // 1  — the day of the WEEK (0 = Sunday, 1 = Monday)
```

Months run 0–11, days of the month 1–31, and days of the week 0–6. Mixing up `getDate` (day of
month) and `getDay` (weekday) is a classic slip.

## 🪤 Trap 2: Date-Only Strings Are UTC; Date-Time Strings Are Local

MDN documents the most dangerous inconsistency: a **date-only** ISO string is interpreted as **UTC**,
while a **date-time** string with **no offset** is interpreted as **local time**. The same calendar
day therefore means different instants — and the difference depends on the machine's time zone. Run
under three different time zones:

```js
const a = new Date("2024-01-15");            // date-only          → UTC
const b = new Date("2024-01-15T00:00:00");   // date-time, no zone → LOCAL

console.log(a.toISOString(), a.getDate(), b.toISOString());
```

```
TZ=UTC               2024-01-15T00:00:00.000Z   getDate() 15   2024-01-15T00:00:00.000Z
TZ=America/New_York  2024-01-15T00:00:00.000Z   getDate() 14   2024-01-15T05:00:00.000Z
TZ=Asia/Kolkata      2024-01-15T00:00:00.000Z   getDate() 15   2024-01-14T18:30:00.000Z
```

In New York, `new Date("2024-01-15").getDate()` is **14** — midnight UTC is still the evening of the
14th locally. This single behavior produces a steady stream of "the date is off by one" bugs. The
habits that avoid it:

- **Store and transmit instants in UTC**, as ISO strings with an explicit `Z` or offset
  (`date.toISOString()`).
- **Never rely on non-ISO strings.** Only the ISO format is guaranteed by the specification; other
  formats (`"01/02/2024"`) are interpreted at each engine's discretion.
- **Use the `getUTC...` methods** when you mean the UTC calendar day.

## 🪤 Trap 3: A "Day" Is Not Always 24 Hours

Daylight saving time makes some days 23 or 25 hours long, so dividing a millisecond difference by
`86_400_000` is only approximately a day count:

```js
const start = new Date(2024, 2, 10);   // March 10, local midnight
const next  = new Date(2024, 2, 11);   // March 11, local midnight

console.log((next - start) / 3_600_000);   // hours between them
// TZ=UTC:               24
// TZ=America/New_York:  23   ← the clocks "sprang forward" on March 10, 2024
```

For calendar arithmetic ("tomorrow", "next month") use the setter methods or a date library rather
than adding milliseconds.

## 🪤 Trap 4: Setters Overflow Silently

```js
const d = new Date(2024, 0, 31);   // January 31
d.setMonth(1);                     // ask for February — which has no 31st
console.log(d.getMonth(), d.getDate());   // 2 2 — it rolled over to March 2
```

Out-of-range values do not raise errors; they roll into the next unit. That is convenient for
`setDate(d.getDate() + 30)` and surprising everywhere else.

## 🪤 Trap 5: Invalid Dates Fail Quietly

```js
const bad = new Date("nope");
console.log(String(bad));      // Invalid Date
console.log(bad.getTime());    // NaN
console.log(isNaN(bad));       // true — the way to test for validity

bad.toISOString();             // RangeError: Invalid time value
```

An invalid `Date` is still a `Date` object. Check `Number.isNaN(date.getTime())` before using
user-supplied dates.

## 🌐 `Intl`: Formatting for Every Locale

Don't build date or number strings by hand. The built-in `Intl` APIs know every locale's conventions.

### `Intl.DateTimeFormat`

```js
const when = new Date(Date.UTC(2024, 0, 15, 13, 45));

console.log(new Intl.DateTimeFormat("en-US", { dateStyle: "long", timeZone: "UTC" }).format(when));
// January 15, 2024
console.log(new Intl.DateTimeFormat("de-DE", { dateStyle: "long", timeZone: "UTC" }).format(when));
// 15. Januar 2024
console.log(new Intl.DateTimeFormat("en-GB", { dateStyle: "short", timeStyle: "short", timeZone: "UTC" }).format(when));
// 15/01/2024, 13:45
```

The `timeZone` option controls which zone the instant is displayed in; omit it to use the user's
local zone. Storing UTC and formatting for the viewer with `Intl.DateTimeFormat` is the robust
pattern.

### `Intl.NumberFormat`

```js
console.log(new Intl.NumberFormat("de-DE", { style: "currency", currency: "EUR" }).format(1234.5));
// 1.234,50 €      (a non-breaking space precedes the symbol)
console.log(new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(1234.5));
// $1,234.50
console.log(new Intl.NumberFormat("en-IN").format(1234567.891));
// 12,34,567.891   — Indian digit grouping
```

### `Intl.RelativeTimeFormat` and `Intl.ListFormat`

```js
const rtf = new Intl.RelativeTimeFormat("en", { numeric: "auto" });
console.log(rtf.format(-1, "day"));   // yesterday
console.log(rtf.format(3, "day"));    // in 3 days
console.log(rtf.format(0, "day"));    // today

console.log(new Intl.ListFormat("en", { style: "long", type: "conjunction" }).format(["a", "b", "c"]));
// a, b, and c
```

`Intl.PluralRules` picks the correct plural category for a language
(`new Intl.PluralRules("en").select(1)` is `"one"`, and `select(2)` is `"other"`), which matters for
languages with more than two plural forms.

## 🔭 What About `Temporal`?

`Temporal` is a new date-and-time API designed to replace `Date`: separate types for instants,
calendar dates, wall-clock times, and time zones, plus durations and nanosecond precision. As of
MDN's current documentation it has **limited availability** and is **not Baseline** — in
Node.js 24, `typeof Temporal` is still `"undefined"`. Check
[MDN's Temporal page](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Temporal)
for current status; until it is universally available, either use a polyfill or keep to the safe
`Date` practices above.

## 🎤 Interview Angle

- **"What does a JavaScript `Date` actually store?"** A single number: milliseconds since the Unix
  epoch, in UTC.
- **"Why might `new Date('2024-01-15').getDate()` return 14?"** A date-only ISO string is parsed as
  UTC midnight, and in a time zone behind UTC the local calendar date is still the 14th.
- **"Why are months zero-based?"** A historical design inherited from earlier languages; plan for
  `getMonth()` returning 0–11.
- **"How should you store and display dates?"** Store UTC instants (ISO strings or timestamps);
  format for the user with `Intl.DateTimeFormat`.

## Common Mistakes

- **Writing `new Date(2024, 1, 15)` and expecting January.**
- **Parsing date-only strings and reading local getters**, producing off-by-one days.
- **Treating every day as 86,400,000 milliseconds.**
- **Assuming out-of-range setters throw** — they roll over.
- **Using `new Date(userString)` without checking for `Invalid Date`.**
- **Concatenating date and number strings by hand** instead of using `Intl`.

## ➡️ Next

Continue to [typed-arrays-and-binary-data.md](typed-arrays-and-binary-data.md) to work with raw
bytes — files, network data, and the text-to-bytes conversions that Unicode requires.
