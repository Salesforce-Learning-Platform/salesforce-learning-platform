# Regular Expressions

## Creating a Regular Expression

```js
const re1 = /ab+c/;               // literal notation — most common
const re2 = new RegExp("ab+c");    // constructor — useful when the pattern is built dynamically
```

A **regular expression** (regex) describes a pattern for matching text — used for validation
(does this look like a valid email?), searching, and find-and-replace operations.

## Common Pattern Elements

| Syntax | Matches |
|---|---|
| `abc` | The literal characters "abc" |
| `.` | Any single character (except newline) |
| `\d` | Any digit |
| `\w` | Any word character (letter, digit, underscore) |
| `\s` | Any whitespace character |
| `*` | Zero or more of the preceding element |
| `+` | One or more of the preceding element |
| `?` | Zero or one of the preceding element |
| `[abc]` | Any one of the characters a, b, or c |
| `^` / `$` | Start / end of the string |
| `(...)` | A capturing group |

```js
const emailPattern = /^\w+@\w+\.\w+$/; // a simplified, illustrative email check
```

## Flags

```js
/pattern/g;  // global — find ALL matches, not just the first
/pattern/i;  // case-insensitive
/pattern/gi; // both combined
```

## Using Regular Expressions

```js
const re = /\d+/;

re.test("Room 42");        // true — does the string contain a match at all?
"Room 42".match(re);        // ["42", ...] — the actual match details
"Room 42, Room 7".match(/\d+/g); // ["42", "7"] — all matches, with the g flag
"Room 42".replace(/\d+/, "###"); // "Room ###"
"a,b,,c".split(/,+/);        // ["a", "b", "c"] — split on one or more commas
```

| Method | Returns |
|---|---|
| `regex.test(str)` | `true`/`false` — is there a match at all? |
| `str.match(regex)` | The match details (or all matches, with the `g` flag) |
| `str.replace(regex, replacement)` | A new string with matches replaced |
| `str.split(regex)` | An array, splitting the string wherever the pattern matches |

## When Regex Is (and Isn't) the Right Tool

Regular expressions are appropriate for relatively simple, well-defined text patterns —
validating a format, extracting a substring, splitting on a delimiter. They become genuinely hard
to read and maintain for deeply complex parsing tasks (like parsing an entire programming language
or a nested data format) — a dedicated parser is usually the better tool once a pattern's
complexity grows much beyond a few lines.

## Common Mistakes

- Writing an overly strict or overly permissive pattern for something like email or phone number
  validation — real-world formats vary more than a simple pattern often accounts for (this exact
  point was raised in [input-types-and-attributes.md](../../html/html-forms-and-user-input/input-types-and-attributes.md)
  regarding the `pattern` HTML attribute, which uses the same underlying regex syntax).
- Forgetting the `g` flag when all matches are needed, and being confused when only the first one
  is returned.
- Reaching for an increasingly complex regular expression for a parsing task that's genuinely
  outgrown what regex can cleanly express.

## Module Summary

Across this module: Symbols provide a guaranteed-unique primitive value, most useful as
collision-free object keys and as the mechanism behind well-known behaviors like
`Symbol.iterator` (see [symbols.md](symbols.md)); the iterator protocol
(`[Symbol.iterator]()` returning an object with `next()`) is what every `for...of`-compatible
structure implements, and generator functions (`function*`/`yield`) provide a dramatically simpler
way to implement it, with genuine lazy-evaluation benefits (see
[iterators-and-generators.md](iterators-and-generators.md)); and regular expressions provide a
compact pattern language for matching, extracting, and replacing text, appropriate for
well-defined patterns but not a substitute for a real parser once complexity grows.

This completes the JavaScript domain (OPS-063 through OPS-077).
