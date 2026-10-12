# 🔤 String Fundamentals

## Text Is an Array of Characters — With Some Important Twists

A string is an ordered sequence of characters. That makes it a close cousin of the
[array](../arrays/array-fundamentals.md): characters sit in order, each has an index, and you read them
with `text[i]`. Almost everything you learned about arrays — traversal, two pointers, sliding windows —
transfers directly. But strings have three properties that arrays of numbers do not, and every
string-algorithm bug comes from forgetting one of them:

1. **They are immutable** in Python (and Java, JavaScript, C#, and Go) — you cannot change a character in
   place.
2. **Characters are not bytes.** A "character" is a Unicode code point, and what a human sees as one
   symbol may be several.
3. **Operations that look cheap can copy the whole string**, so cost depends on *how* you build and slice.

All Python results in this file were produced by running the code on CPython 3.9; the timings are from one
machine and will vary on yours, but the *shapes* (linear vs. quadratic growth) are what matter.

## 🧱 What You Can Do in O(1)

Because a Python `str` stores its characters contiguously and knows its own length, two operations are
constant time regardless of size:

```python
text = "hello"
print(len(text))       # 5      — the length is stored, not counted
print(text[1])         # e      — direct index, just like an array
print(text[-1])        # o      — negative indexes count from the end
```

On a ten-million-character string, `len(big)` and `big[5]` each took well under a tenth of a microsecond.
Everything else — slicing, searching, comparing, concatenating — touches characters, and costs more.

## 🧊 Immutability

You cannot assign to a position:

```python
text = "hello"
text[0] = "J"          # TypeError: 'str' object does not support item assignment
```

Every operation that seems to "change" a string actually builds a **new** one and leaves the original
untouched:

```python
original = "hello"
alias = original
original += "!"
print(original)        # hello!
print(alias)           # hello     — the other name still sees the old string
print(original is alias)   # False — two different objects now
```

Immutability has two practical consequences:

- **Safety.** A string can be shared, cached, and used as a dictionary key without anyone altering it
  behind your back (that is why strings are *hashable* — see
  [hash-functions.md](../hashing/hash-functions.md)).
- **Cost.** Repeated "modification" repeatedly copies. To change characters efficiently, convert to a
  mutable list, edit it, and join it back:

```python
chars = list("hello")      # O(n): one list element per character
chars[0] = "J"             # O(1): lists are mutable
print("".join(chars))      # Jello   — O(n) to build the new string
```

This `list → edit → join` pattern is the standard way to do "in-place" string algorithms such as the
two-pointer reversal in [string-manipulation.md](string-manipulation.md).

## 🌍 Characters, Code Points, and Bytes

A Python string is a sequence of **Unicode code points**. `ord` gives a character's number and `chr` goes
back:

```python
print(ord("a"), chr(97))     # 97 a
print(ord("A"), ord("€"))    # 65 8364
```

`len` counts code points — not bytes, and not necessarily the symbols a person would count:

```python
for text in ["abc", "é", "日本", "😀", "👨‍👩‍👧"]:
    print(repr(text), "code points:", len(text), "UTF-8 bytes:", len(text.encode("utf-8")))
# 'abc'   code points: 3   UTF-8 bytes: 3
# 'é'     code points: 1   UTF-8 bytes: 2
# '日本'   code points: 2   UTF-8 bytes: 6
# '😀'     code points: 1   UTF-8 bytes: 4
# '👨‍👩‍👧'   code points: 5   UTF-8 bytes: 18
```

The last line is the surprise: a family emoji is a *single symbol on screen* but five code points (three
people joined by invisible zero-width joiners). The same visible text can even have two different
representations:

```python
import unicodedata

composed = "é"              # é as a single code point
decomposed = "é"           # 'e' followed by a combining acute accent
print(composed, decomposed)                                   # (both render as é)
print(composed == decomposed)                                 # False
print(len(composed), len(decomposed))                         # 1 2
print(unicodedata.normalize("NFC", decomposed) == composed)   # True
```

The two look identical but compare unequal, so text from different sources should be **normalized**
(`unicodedata.normalize`) before comparing or counting. And reversing is not always safe:

```python
word = "café"              # "café" written with a combining accent
print(len(word))                 # 5
print(repr(word[::-1]))          # '́efac' — the accent now attaches to the wrong place
```

**What this means for the algorithms in this module.** The examples assume text where each code point is
one "character" (plain English letters and digits), which is what interviews and most exercises mean.
Real products must decide whether they are counting code points, bytes, or user-perceived characters, and
the three give different answers. The official [Unicode HOWTO](https://docs.python.org/3/howto/unicode.html)
is the reference.

### How Much Memory Does a Character Take?

CPython (the standard implementation) stores each string using the narrowest fixed width that fits its
widest character — the scheme described in [PEP 393](https://peps.python.org/pep-0393/). You can observe it
from the growth in size per extra character:

```python
import sys

for label, ch in [("ASCII", "a"), ("Latin-1", "é"), ("CJK", "日"), ("emoji", "😀")]:
    per_char = (sys.getsizeof(ch * 100) - sys.getsizeof(ch * 10)) / 90
    print(f"{label:8} {per_char:.0f} byte(s) per character")
# ASCII    1 byte(s) per character
# Latin-1  1 byte(s) per character
# CJK      2 byte(s) per character
# emoji    4 byte(s) per character
```

One emoji in a long ASCII string therefore makes *every* character of that string take four bytes. This is
a CPython detail rather than a rule of the language, but it explains why `len(text)` is O(1) and indexing is
O(1) even for Unicode: all characters in one string have the same width.

## ↕️ Comparing and Ordering

Strings compare **lexicographically by code point**, character by character, like words in a dictionary —
except that "dictionary order" is the order of Unicode numbers:

```python
print("apple" < "banana")     # True   — 'a' < 'b' decides at the first character
print("abc" < "abcd")         # True   — a proper prefix is smaller
print("" < "a")               # True   — the empty string is smaller than everything else
print("Z" < "a")              # True   — uppercase letters (65–90) come before lowercase (97–122)
print("10" < "9")             # True   — compares '1' with '9', not the numbers 10 and 9
```

Two habits follow from that:

- For **case-insensitive** comparison use `casefold()`, which is designed for it (and handles cases like
  German `ß`): `"straße".casefold() == "STRASSE".casefold()` is `True`.
- Convert to numbers *before* comparing numeric text.

Comparing two strings costs up to the length of the shorter one, because the scan stops at the first
difference. So `a == b` is O(min(len(a), len(b))) in the worst case — not O(1).

## ⚙️ What Common Operations Cost

| Operation | Cost | Why |
|-----------|------|-----|
| `len(s)`, `s[i]` | O(1) | Length is stored; characters are contiguous and fixed-width |
| `s[a:b]` (slice) | O(k), where k = `b - a` | A new string is built from the copied characters |
| `s + t` | O(len(s) + len(t)) | A new string is built |
| `s == t`, `s < t` | O(min length) worst case | Stops at the first difference |
| `t in s`, `s.find(t)` | at least O(len(s)) | Must scan the text; see [string-patterns.md](string-patterns.md) |
| `s.split()`, `s.upper()`, `s.strip()` | O(n) | Visit every character, build new strings |
| `"".join(parts)` | O(total length) | One pass to copy everything once |
| `list(s)` | O(n) | One element per character |

The slicing cost is easy to see. On a ten-million-character string, `big[:100]` copies 100 characters and
took under a tenth of a microsecond, while `big[1:]` copies almost ten million and took roughly 190
microseconds on the test machine — thousands of times longer. A loop that repeatedly writes
`text = text[1:]` therefore does O(n) work *per iteration* and O(n²) overall; use an index instead.

## 🏗️ Building Strings: The Cost of `+=`

Because each concatenation creates a new string, building a long string with `+=` in a loop *can* be
quadratic: step `i` may copy the first `i` characters again. The Python FAQ states the general case: the
total runtime cost is quadratic in the total string length, and recommends accumulating pieces in a list and
calling `str.join()`.

CPython has a special optimization that sometimes hides the problem, so measure it. This benchmark builds a
string of `n` characters five ways (best of three runs, milliseconds):

```python
import io, timeit

def concat_plain(n):                 # s += "x"
    s = ""
    for _ in range(n):
        s += "x"
    return s

def concat_aliased(n):               # s += "x", while another name refers to the old string
    s = ""
    old = ""
    for _ in range(n):
        old = s
        s += "x"
    return s

def concat_join(n):                  # collect pieces, join once
    parts = []
    for _ in range(n):
        parts.append("x")
    return "".join(parts)

def concat_stringio(n):              # write into an in-memory text buffer
    buffer = io.StringIO()
    for _ in range(n):
        buffer.write("x")
    return buffer.getvalue()

def prepend(n):                      # s = "x" + s
    s = ""
    for _ in range(n):
        s = "x" + s
    return s

print(f"{'n':>8} | {'+= plain':>9} | {'+= aliased':>10} | {'join':>7} | {'StringIO':>8} | {'prepend':>8}")
for n in (20_000, 40_000, 80_000, 160_000):
    row = [min(timeit.repeat(lambda: fn(n), number=1, repeat=3)) * 1000
           for fn in (concat_plain, concat_aliased, concat_join, concat_stringio, prepend)]
    print(f"{n:>8,} | {row[0]:9.2f} | {row[1]:10.2f} | {row[2]:7.2f} | {row[3]:8.2f} | {row[4]:8.2f}")
```

One run on the test machine produced:

```
       n |  += plain | += aliased |    join | StringIO |  prepend
  20,000 |      0.82 |       3.26 |    0.68 |     0.81 |     3.25
  40,000 |      1.64 |      11.80 |    1.36 |     1.61 |    12.10
  80,000 |      3.33 |      54.66 |    2.66 |     3.22 |    56.49
 160,000 |      6.71 |     264.60 |    5.35 |     6.10 |   270.02
```

Read the doubling behavior in each column. `+= plain`, `join`, and `StringIO` roughly **double** when `n`
doubles — linear growth. `+= aliased` and `prepend` grow about **four-fold** or more per doubling —
quadratic growth, and at 160,000 characters they are roughly 40 to 50 times slower than the linear versions.

Why does plain `+=` look fine? When nothing else refers to the string, CPython can extend it in place
instead of copying. As soon as a second reference exists (the `old = s` line), or you build from the front,
the copy comes back. [PEP 8](https://peps.python.org/pep-0008/) warns against depending on this: it calls the
optimization fragile and notes it is absent from implementations that do not use reference counting.

**The rule:** when building a string from many pieces, append the pieces to a list and call `"".join()` once.
It is linear on every implementation.

## 🔡 Working With Characters

Because characters have code-point numbers, you can do arithmetic on letters. A frequent idiom maps `'a'`
to `0`, `'b'` to `1`, and so on, which allows a plain 26-slot list to count letters:

```python
import string

print(string.ascii_lowercase)            # abcdefghijklmnopqrstuvwxyz

def letter_counts(text):
    counts = [0] * 26
    for ch in text:
        counts[ord(ch) - ord("a")] += 1  # 'a' -> 0, 'b' -> 1, ... 'z' -> 25
    return counts

counts = letter_counts("banana")
print(counts[:3])                        # [3, 1, 0]   — three a's, one b, zero c's
```

This is a tiny [hash table](../hashing/hash-tables.md) in disguise: the "hash function" is `ord(ch) - ord("a")`
and there are never collisions, because the alphabet is fixed. It only works for lowercase `a`–`z`; other
input needs a dictionary. The character-test methods deserve one warning, because they follow Unicode, not
just ASCII:

```python
print("٣".isdigit(), "٣".isdecimal(), int("٣"))   # True True 3   — an Arabic-Indic digit three
print("²".isdigit(), "²".isdecimal())              # True False    — superscript two
print("é".isalpha(), "é".isalnum())                # True True
```

`str.isdigit()` is `True` for superscripts and for digits from other scripts, so validating "is this an
ordinary number?" often needs `isdecimal()`, an explicit range check, or a regular expression, depending on
what you intend to accept.

## ✅ Choosing How to Work With a String

| Goal | Reach for |
|------|-----------|
| Read characters, count, compare | The string itself (`for ch in text`, `text[i]`) |
| Change characters in place | `list(text)`, edit, then `"".join(chars)` |
| Build from many pieces | Collect in a list, then `"".join(parts)` |
| Take a piece without copying a lot | Keep indexes (`start`, `end`) instead of slicing repeatedly |
| Compare text from different sources | Normalize (`unicodedata.normalize`) and `casefold()` first |

## Common Mistakes

- **Trying to assign to `text[i]`** — strings are immutable; use a list.
- **Building a long string with `s = s + piece` or `s = piece + s` in a loop** and assuming it is linear.
- **Slicing inside a loop** (`text = text[1:]`) and not noticing the O(n²) cost.
- **Assuming one character means one byte** or that `len(text)` equals the number of symbols a person sees.
- **Comparing numeric strings as text** (`"10" < "9"` is `True`).
- **Comparing Unicode text without normalizing**, so visually identical strings compare unequal.
- **Using `isdigit()` as a strict "is a number" test.**

## ➡️ Next

Continue to [string-manipulation.md](string-manipulation.md) to apply these ideas to the everyday
transformations: reversing, splitting, counting, encoding, and comparing text.
