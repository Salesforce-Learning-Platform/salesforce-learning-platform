# ✂️ String Manipulation

## The Everyday Transformations — and the Patterns Behind Them

Most string problems are built from a handful of moves: reverse something, split text into pieces, count
characters, compare two texts, rewrite characters one by one. This file practises each move on a small
problem and, for each, states the cost — remembering from
[string-fundamentals.md](string-fundamentals.md) that strings are immutable, so "changing" text means
building a new string.

Every function below was run and checked: against Python's built-in equivalents or a brute-force version
on thousands of random inputs, plus the documented examples.

## 🔄 Reversing

Three ways to reverse a string, with different costs and uses:

```python
text = "python"

print(text[::-1])                  # nohtyp   — slice with a step of -1; builds a new string, O(n)
print("".join(reversed(text)))     # nohtyp   — reversed() walks backward; join builds the result, O(n)

def reverse_with_two_pointers(text):
    chars = list(text)             # strings are immutable, so work on a list
    left, right = 0, len(chars) - 1
    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1
    return "".join(chars)

print(reverse_with_two_pointers(text))   # nohtyp
```

In Python the slice is the idiomatic one-liner. The two-pointer version is the one interviewers ask for,
because it shows the technique from [two-pointer-technique.md](../arrays/two-pointer-technique.md); it
becomes genuinely in place in languages whose strings are mutable arrays of characters. All three are O(n)
time. The list-based version uses O(n) extra space (the list of characters) — in Python there is no way to
reverse a `str` in O(1) extra space, because a new string must be created anyway.

### Reverse the Words, Not the Letters

"the sky is blue" → "blue is sky the". The Python one-liner splits on whitespace, reverses the list of
words, and joins them:

```python
def reverse_words(sentence):
    return " ".join(reversed(sentence.split()))

print(reverse_words("the sky is blue"))        # blue is sky the
print(reverse_words("  hello   world  "))      # world hello   — extra spaces are dropped
```

`split()` with no argument splits on any run of whitespace and discards empty pieces, which is why the
leading, trailing, and repeated spaces vanish. Note the contrast with `split(" ")`:

```python
print("  a  b ".split())       # ['a', 'b']
print("  a  b ".split(" "))    # ['', '', 'a', '', 'b', '']   — one empty string per extra space
```

If the problem requires **preserving** the original spacing, use the classic trick: reverse the entire
character list, then reverse each word back to its original orientation. Both steps are reversals, so the
whole thing is O(n) time and works on a list in place:

```python
def reverse_words_in_place(chars):
    def reverse(low, high):
        while low < high:
            chars[low], chars[high] = chars[high], chars[low]
            low += 1
            high -= 1

    reverse(0, len(chars) - 1)              # step 1: reverse everything
    start = 0
    for i in range(len(chars) + 1):
        if i == len(chars) or chars[i] == " ":
            reverse(start, i - 1)           # step 2: reverse each word back
            start = i + 1

letters = list("  hello world  ")
reverse_words_in_place(letters)
print(repr("".join(letters)))             # '  world hello  ' — the spaces stayed where they were
```

Trace: `"  hello world  "` → reverse all → `"  dlrow olleh  "` → reverse each word → `"  world hello  "`.

## ✂️ Splitting, Cleaning, and Joining

These built-ins each make one pass over the text, so all are O(n):

```python
line = "  alice, bob ,carol  "
names = [part.strip() for part in line.split(",")]
print(names)                          # ['alice', 'bob', 'carol']
print(" | ".join(names))              # alice | bob | carol

messy = "too    many\tspaces\nhere"
print(" ".join(messy.split()))        # too many spaces here   — normalizes any whitespace
print("a-b-c".replace("-", ""))       # abc
```

`split(",")` followed by `strip()` on each part is the usual way to parse simple delimited text. For real
CSV with quoted fields, use the standard `csv` module — splitting on commas breaks when a value itself
contains a comma.

## 🔢 Counting Characters

Counting how often each character appears is the most reusable string tool. A dictionary maps each
character to its count:

```python
def char_frequency(text):
    counts = {}
    for ch in text:
        counts[ch] = counts.get(ch, 0) + 1
    return counts

freq = char_frequency("mississippi")
print(freq)                           # {'m': 1, 'i': 4, 's': 4, 'p': 2}
print(max(freq, key=freq.get))        # i   — the (first) most frequent character
```

One pass, O(n) time, and O(k) space where `k` is the number of distinct characters (at most the alphabet
size). The standard library offers the same thing ready-made as `collections.Counter`, and the idea of
using a dictionary this way is the subject of the [Hashing](../hashing/README.md) module — in particular
[hash-based-problem-solving.md](../hashing/hash-based-problem-solving.md).

### Are Two Words Anagrams?

Two strings are anagrams if they contain exactly the same characters with the same counts. There are two
standard solutions:

```python
def is_anagram_sorted(a, b):
    return sorted(a) == sorted(b)            # O(n log n): sorting dominates

def is_anagram_counts(a, b):
    if len(a) != len(b):
        return False
    counts = {}
    for ch in a:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in b:
        if counts.get(ch, 0) == 0:           # b has a character a doesn't have enough of
            return False
        counts[ch] -= 1
    return True                               # equal lengths + never ran out => all counts are zero

print(is_anagram_sorted("listen", "silent"))   # True
print(is_anagram_counts("listen", "silent"))   # True
print(is_anagram_counts("rat", "car"))         # False
```

The sorting version is shortest; the counting version is O(n) time and O(k) space. Mentioning both, and
saying *why* counting is faster (it avoids ordering the characters, which the question never needs), is
exactly the kind of answer interviewers look for.

## 🗜️ Run-Length Encoding

Compress repeated characters into `character + count`: `"aaabccdddd"` becomes `"a3b1c2d4"`. The idea is
to scan once, tracking the current run:

```python
def rle_encode(text):
    if not text:
        return ""
    pieces = []
    run_char, run_length = text[0], 1
    for ch in text[1:]:
        if ch == run_char:
            run_length += 1
        else:
            pieces.append(f"{run_char}{run_length}")
            run_char, run_length = ch, 1
    pieces.append(f"{run_char}{run_length}")      # don't forget the final run
    return "".join(pieces)

def rle_decode(encoded):
    pieces = []
    i = 0
    while i < len(encoded):
        ch = encoded[i]
        i += 1
        digits_start = i
        while i < len(encoded) and "0" <= encoded[i] <= "9":
            i += 1
        pieces.append(ch * int(encoded[digits_start:i]))
    return "".join(pieces)

print(rle_encode("aaabccdddd"))               # a3b1c2d4
print(rle_decode("a3b1c2d4"))                 # aaabccdddd
print(rle_decode(rle_encode("x" * 12)))       # xxxxxxxxxxxx   — a run of 12 is stored as "x12"
print(rle_encode("abc"))                      # a1b1c1   — encoding can make the text longer
```

Three details worth remembering: the **last run** must be flushed after the loop (the most common bug);
counts can have **several digits**, so the decoder reads digits until it meets the next letter; and this
format assumes the original text contains **no digits**, otherwise the decoder cannot tell data from
counts. Encoding runs in O(n) and uses a list plus `join` instead of `+=`, as recommended in
[string-fundamentals.md](string-fundamentals.md). Run-length encoding only helps when the input has long
runs; for `"abc"` it triples the size.

## 🔐 Shifting Letters (Caesar Cipher)

Letter arithmetic from [string-fundamentals.md](string-fundamentals.md) in action: shift each letter
forward by `shift` positions, wrapping around the alphabet, leaving other characters alone.

```python
def caesar(text, shift):
    result = []
    for ch in text:
        if "a" <= ch <= "z":
            result.append(chr((ord(ch) - ord("a") + shift) % 26 + ord("a")))
        elif "A" <= ch <= "Z":
            result.append(chr((ord(ch) - ord("A") + shift) % 26 + ord("A")))
        else:
            result.append(ch)                      # spaces, digits, punctuation unchanged
    return "".join(result)

secret = caesar("Hello, World!", 3)
print(secret)                      # Khoor, Zruog!
print(caesar(secret, -3))          # Hello, World!   — shifting back decodes it
print(caesar("xyz", 3))            # abc             — wraps past 'z'
```

The `% 26` does the wrapping. Python's `%` always returns a non-negative result for a positive modulus, so a
negative shift also works (`-3 % 26` is `23`); in languages such as C, Java, and JavaScript the remainder of
a negative number is negative, and you must add 26 first. This is a teaching cipher, not security — it can be
broken by trying all 25 shifts.

## 🔁 Is One String a Rotation of Another?

`"waterbottle"` rotated is `"erbottlewat"`. Brute force tries every rotation (O(n²)). A neat observation
does it with one substring search: every rotation of `a` appears inside `a + a`.

```python
def is_rotation(a, b):
    return len(a) == len(b) and b in a + a

print(is_rotation("waterbottle", "erbottlewat"))   # True
print(is_rotation("abc", "acb"))                    # False
print(is_rotation("abc", "abcd"))                   # False   — different lengths
```

The length check matters: without it, `"abc"` would count as a "rotation" of `"abcd"`'s prefix. The cost is
that of building `a + a` (O(n)) plus one substring search — see
[string-patterns.md](string-patterns.md) for how substring search works.

## 🧼 Removing and Replacing Characters

For filtering, a generator inside `join` is clear; for bulk replacement or deletion of single characters,
`str.translate` with a table from `str.maketrans` is fast and tidy:

```python
vowels = "aeiouAEIOU"
text = "Programming Language"

print("".join(ch for ch in text if ch not in vowels))    # Prgrmmng Lngg
print(text.translate(str.maketrans("", "", vowels)))      # Prgrmmng Lngg   — same result via a table

punctuation = str.maketrans({ch: None for ch in ".,!?"})
print("Wait... what?!".translate(punctuation))             # Wait what
```

Both are O(n). The `ch not in vowels` test scans a 10-character string for each character, which is a
constant amount of work because the vowel string has a fixed size — if the set of characters to remove were
large, a `set` would be the better choice.

## 📋 Summary of the Moves

| Task | Approach | Time | Extra space |
|------|----------|------|-------------|
| Reverse a string | Slice, `reversed`, or two pointers on a list | O(n) | O(n) |
| Reverse the words | `split` + `reversed` + `join`, or double reversal | O(n) | O(n) |
| Parse delimited text | `split` + `strip` | O(n) | O(n) |
| Count characters | Dictionary / `Counter` | O(n) | O(k) |
| Check anagrams | Sort both, or compare counts | O(n log n) or O(n) | O(n) or O(k) |
| Run-length encode | One scan tracking the current run | O(n) | O(n) |
| Shift letters | `ord`/`chr` arithmetic with `% 26` | O(n) | O(n) |
| Rotation test | `b in a + a` after a length check | O(n) plus search | O(n) |
| Delete / replace characters | Generator + `join`, or `translate` | O(n) | O(n) |

## Common Mistakes

- **Forgetting the last run or last word.** Loops that emit a result when the character changes need one
  more emit after the loop.
- **Using `split(" ")` instead of `split()`** and getting empty strings for repeated spaces.
- **Building the result with `+=` or `+` in a loop** instead of collecting pieces and joining.
- **Treating the Caesar `% 26` like C's `%`** when porting to another language: negative shifts break.
- **Checking `a in b + b` without comparing lengths** first for rotations.
- **Assuming run-length decoding handles single-digit counts only**, so runs of 10 or more break.
- **Splitting CSV by commas** when fields can contain quoted commas.

## ➡️ Next

Continue to [palindrome-problems.md](palindrome-problems.md) for one of the most common string-interview
families, built on the two-pointer technique.
