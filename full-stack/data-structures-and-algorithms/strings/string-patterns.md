# 🧩 Common String Patterns

## Five Techniques That Solve Most String Problems

After reversing, counting, and palindromes, the remaining string problems are mostly variations on a few
reusable patterns. Learn to *recognize* the pattern from the wording of a problem and you already know the
shape of the solution:

| Pattern | Typical wording | Core tool |
|---------|-----------------|-----------|
| Frequency counting | "anagram", "first unique", "same letters" | Dictionary or fixed-size count list |
| Two pointers | "reverse only the vowels", "from both ends" | Indexes moving inward or in step |
| Sliding window | "substring containing…", "permutation in…" | Window plus counts |
| Prefix scanning | "longest common prefix" | Compare column by column |
| Pattern matching | "find the pattern in the text" | Naive search, or KMP for guaranteed linear time |

Each section below shows one problem per pattern. All code was tested against a brute-force or built-in
reference on thousands of random inputs.

## 🔢 Pattern 1: Frequency Counting

### The First Character That Appears Only Once

Count everything in one pass; find the answer in a second pass that preserves the original order:

```python
def first_unique_char(text):
    counts = {}
    for ch in text:
        counts[ch] = counts.get(ch, 0) + 1
    for index, ch in enumerate(text):         # scan in the original order
        if counts[ch] == 1:
            return index
    return -1

print(first_unique_char("leetcode"))     # 0    — 'l'
print(first_unique_char("loveleetcode")) # 2    — 'v'
print(first_unique_char("aabb"))         # -1   — every character repeats
```

Two passes are still O(n) time, and the dictionary holds at most one entry per distinct character.

### Grouping Words That Are Anagrams of Each Other

Anagrams share the same letters, so they share a canonical form. Use that form as a dictionary key to bucket the
words. Two common keys:

```python
def group_anagrams_sorted(words):
    groups = {}
    for word in words:
        key = "".join(sorted(word))                  # "eat", "tea", "ate" all become "aet"
        groups.setdefault(key, []).append(word)
    return list(groups.values())

def group_anagrams_counts(words):
    groups = {}
    for word in words:
        counts = [0] * 26
        for ch in word:
            counts[ord(ch) - ord("a")] += 1          # lowercase a–z only
        groups.setdefault(tuple(counts), []).append(word)    # a list can't be a key; a tuple can
    return list(groups.values())

words = ["eat", "tea", "tan", "ate", "nat", "bat"]
print(group_anagrams_sorted(words))   # [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
print(group_anagrams_counts(words))   # [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
```

With `n` words of length at most `k`: the sorted key costs O(n · k log k); the count key costs O(n · k) (plus
26 slots per word). The key must be **hashable and immutable**, which is why a tuple works and a list does not —
the reason is explained in [hash-functions.md](../hashing/hash-functions.md), and this "compute a canonical key,
bucket by it" pattern is developed further in [hash-based-problem-solving.md](../hashing/hash-based-problem-solving.md).

## ↔️ Pattern 2: Two Pointers

### Reverse Only the Vowels

Walk inward from both ends; each pointer skips non-vowels, and when both sit on vowels, swap them:

```python
def reverse_vowels(text):
    vowels = set("aeiouAEIOU")
    chars = list(text)                       # strings are immutable, so edit a list
    left, right = 0, len(chars) - 1
    while left < right:
        while left < right and chars[left] not in vowels:
            left += 1
        while left < right and chars[right] not in vowels:
            right -= 1
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1
    return "".join(chars)

print(reverse_vowels("hello"))      # holle
print(reverse_vowels("leetcode"))   # leotcede
```

O(n) time. The `set` makes each membership test O(1) on average. If both pointers stop on the same position, the
swap is a harmless self-swap, exactly as in the
[move-zeroes example](../arrays/two-pointer-technique.md).

## 🪟 Pattern 3: Sliding Window With Counts

The [sliding window](../arrays/sliding-window.md) technique extends to text by keeping character counts for the
current window. Two classic problems show the two window types.

### Does the Text Contain a Permutation of the Pattern? (Fixed Window)

A permutation of the pattern is an anagram of it, so slide a window of exactly `len(pattern)` characters across
the text and compare counts. Instead of re-comparing whole dictionaries each step, track how many of the pattern's
distinct characters are currently satisfied:

```python
def contains_permutation(pattern, text):
    if len(pattern) > len(text):
        return False
    need = {}
    for ch in pattern:
        need[ch] = need.get(ch, 0) + 1
    window = {}
    satisfied = 0                                    # how many characters have exactly the needed count
    for right, ch in enumerate(text):
        window[ch] = window.get(ch, 0) + 1           # character enters the window
        if ch in need:
            if window[ch] == need[ch]:
                satisfied += 1
            elif window[ch] == need[ch] + 1:
                satisfied -= 1                       # it was satisfied, now it has one too many
        left = right - len(pattern)                  # the character that falls out of the window
        if left >= 0:
            out = text[left]
            window[out] -= 1
            if out in need:
                if window[out] == need[out]:
                    satisfied += 1
                elif window[out] == need[out] - 1:
                    satisfied -= 1
        if satisfied == len(need):
            return True
    return False

print(contains_permutation("ab", "eidbaooo"))   # True    — "ba" is a permutation of "ab"
print(contains_permutation("ab", "eidboaoo"))   # False
```

Each character enters and leaves the window once, and each update is O(1): **O(n) time**, O(k) space for the counts
(k = number of distinct characters). The brute-force alternative sorts or counts every window from scratch:
O(n · m log m).

### The Smallest Window Containing All Needed Characters (Variable Window)

Find the shortest part of `text` that contains every character of `pattern` (with multiplicity). Expand the right
edge until the window is valid, then shrink the left edge for as long as it stays valid, recording the best
window each time:

```python
def min_window(text, pattern):
    if not pattern or len(pattern) > len(text):
        return ""
    need = {}
    for ch in pattern:
        need[ch] = need.get(ch, 0) + 1
    missing = len(pattern)                           # how many needed characters are still missing
    best_start, best_length = 0, len(text) + 1
    left = 0
    for right, ch in enumerate(text):
        if need.get(ch, 0) > 0:
            missing -= 1                             # this character was still needed
        need[ch] = need.get(ch, 0) - 1               # may go negative: extra copies are fine
        while missing == 0:                          # window is valid: try to shrink it
            if right - left + 1 < best_length:
                best_start, best_length = left, right - left + 1
            need[text[left]] += 1
            if need[text[left]] > 0:                 # we just removed a character that was required
                missing += 1
            left += 1
    return "" if best_length > len(text) else text[best_start:best_start + best_length]

print(min_window("ADOBECODEBANC", "ABC"))   # BANC
print(min_window("a", "aa"))                # (empty)  — not enough characters
print(min_window("aa", "aa"))               # aa
```

The `need` dictionary does double duty: positive values are characters the window still lacks, zero means just
enough, and negative values mean surplus copies. Both pointers only move forward, so the nested `while` is amortized
O(n) — the same argument as in [sliding-window.md](../arrays/sliding-window.md) — giving **O(n + m) time**.

## 📏 Pattern 4: Prefix Scanning

### The Longest Common Prefix of Several Words

Compare the words **column by column** and stop at the first column where any word differs or ends:

```python
def longest_common_prefix(words):
    if not words:
        return ""
    first = words[0]
    for column, ch in enumerate(first):
        for word in words[1:]:
            if column == len(word) or word[column] != ch:
                return first[:column]
    return first

print(longest_common_prefix(["flower", "flow", "flight"]))   # fl
print(longest_common_prefix(["dog", "racecar", "car"]))      # (empty)
print(longest_common_prefix(["interview"]))                  # interview
```

Worst case O(S), where `S` is the total number of characters across all words, and O(1) extra space apart from the
returned slice. It never examines a character after the point where the prefix is already known to end.

## 🔍 Pattern 5: Finding a Pattern Inside Text

Searching for `pattern` (length `m`) in `text` (length `n`) is the problem behind `in`, `str.find`, and every text
editor's "Find." The straightforward algorithm slides the pattern across the text and compares character by
character:

```python
def find_naive(text, pattern):
    n, m = len(text), len(pattern)
    for start in range(n - m + 1):
        matched = 0
        while matched < m and text[start + matched] == pattern[matched]:
            matched += 1                              # compare one character at a time
        if matched == m:
            return start
    return -1

def find_naive_slices(text, pattern):                 # same idea, but each attempt is one slice comparison
    n, m = len(text), len(pattern)
    for start in range(n - m + 1):
        if text[start:start + m] == pattern:
            return start
    return -1

print(find_naive("hello world", "o w"))     # 4
print(find_naive("hello world", "xyz"))     # -1
```

In the worst case this does about `n · m` character comparisons: **O(n · m)**. The worst case needs a text and pattern
that match for a long stretch before failing — for example text `"aaaa…a"` and pattern `"aaa…ab"`. Every start position
matches `m − 1` characters before the last one fails.

### Knuth–Morris–Pratt (KMP): Never Re-Read the Text

When a mismatch happens after matching several characters, the naive search throws that knowledge away and
restarts one position later. KMP keeps it. It precomputes, for every prefix of the pattern, the length of the longest
proper prefix that is also a suffix — the **prefix table** — and uses it to decide how far the pattern can safely
shift:

```python
def prefix_table(pattern):
    table = [0] * len(pattern)
    k = 0                                         # length of the current matching prefix
    for i in range(1, len(pattern)):
        while k > 0 and pattern[i] != pattern[k]:
            k = table[k - 1]                      # fall back to the next shorter border
        if pattern[i] == pattern[k]:
            k += 1
        table[i] = k
    return table

print(prefix_table("ababaca"))   # [0, 0, 1, 2, 3, 0, 1]
print(prefix_table("aaaa"))      # [0, 1, 2, 3]
```

Read `table[i]` as: "in `pattern[:i+1]`, the longest proper prefix that is also a suffix has this length." For
`"ababaca"` the entry at index 4 is `3` because `"aba"` is both a prefix and a suffix of `"ababa"`. When a mismatch occurs
after matching `k` characters, the pattern can resume from `table[k - 1]` — the text pointer **never moves backward**:

```python
def kmp_search(text, pattern):
    if not pattern:
        return []
    table = prefix_table(pattern)
    matches = []
    k = 0                                         # characters of the pattern matched so far
    for i, ch in enumerate(text):
        while k > 0 and ch != pattern[k]:
            k = table[k - 1]                      # reuse earlier matches instead of restarting
        if ch == pattern[k]:
            k += 1
        if k == len(pattern):
            matches.append(i - k + 1)             # a full match ending at i
            k = table[k - 1]                      # keep going: matches may overlap
    return matches

print(kmp_search("ababcabababc", "abab"))   # [0, 5, 7]   — the matches at 5 and 7 overlap
print(kmp_search("aaaaa", "aa"))            # [0, 1, 2, 3]
print(kmp_search("hello", "xyz"))           # []
```

KMP runs in **O(n + m) time**: `k` increases by at most one per text character and every fallback decreases it, so the
total fallbacks cannot exceed the total increases (another amortized argument). It also returns *every* match,
including overlapping ones.

### Seeing the Difference

This benchmark fixes the text at 5,000 characters and doubles the pattern length. The text is all `a`; the pattern is
`a…ab`, the worst case for the naive search. Times are in milliseconds (best of three). The columns are the
character-by-character search, the slice-comparing version, KMP, and Python's built-in `str.find`:

```python
import timeit

text = "a" * 5_000
print(f"{'m':>5} | {'naive':>8} | {'slices':>7} | {'KMP':>6} | {'str.find':>8}   (ms)")
for m in (50, 100, 200, 400):
    pattern = "a" * (m - 1) + "b"
    times = [min(timeit.repeat(lambda: fn(text, pattern), number=1, repeat=3)) * 1000
             for fn in (find_naive, find_naive_slices, kmp_search, lambda t, p: t.find(p))]
    print(f"{m:>5} | {times[0]:8.2f} | {times[1]:7.2f} | {times[2]:6.2f} | {times[3]:8.3f}")
```

One run on the test machine printed:

```
    m |    naive |  slices |    KMP | str.find   (ms)
   50 |    17.01 |    0.36 |   0.87 |    0.004
  100 |    32.56 |    0.33 |   0.89 |    0.005
  200 |    63.50 |    0.37 |   0.92 |    0.005
  400 |   125.03 |    0.38 |   0.98 |    0.004
```

Two lessons. First, the textbook `naive` column grows roughly in step with the pattern length `m` — doubling `m`
about doubles the time — exactly what the `n · m` analysis predicts, while KMP stays flat because its cost depends on
`n + m` and `m` is small next to `n`. Second, the `slices` column barely moves: it is still O(n · m) in principle,
but each comparison runs inside C code, so the constant factor is tiny. **Big-O describes how cost grows, not how fast
the code is** — a "worse" algorithm with a fast inner loop can win at modest sizes. The built-in `str.find` is
implemented in C, is far faster than any of the Python versions, and is what you should use in practice. Writing KMP
yourself is for understanding — and for interviews.

(Another well-known approach, **Rabin–Karp**, compares a rolling *hash* of each text window with the pattern's hash;
it is built on hash functions, so it is covered in the Hashing module's
[hash-functions.md](../hashing/hash-functions.md).)

## 🧱 Pattern 6: Parsing With a Stack

Problems about matching brackets (`"({[]})"`) or nested structure rely on remembering the most recent unmatched
opener — a stack. A Python list used with `append` and `pop` is enough:

```python
def is_balanced(text):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)                      # remember the opener
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False                       # a closer with no matching opener
    return not stack                               # leftover openers mean it is unbalanced

print(is_balanced("({[]})"))   # True
print(is_balanced("([)]"))     # False   — closers in the wrong order
print(is_balanced("(("))       # False   — openers never closed
```

O(n) time and O(n) space in the worst case. The stack data structure gets its own module (Stacks and Queues) later
in this domain; this example shows why strings and stacks appear together so often.

## 🧭 Recognizing the Pattern

| If the problem says… | Think… |
|----------------------|--------|
| "same letters", "anagram", "unique", "how many of each" | Counts in a dictionary or 26-slot list |
| "from both ends", "reverse part of it", "palindrome" | Two pointers |
| "longest/shortest substring such that…", "contains all of…" | Sliding window with counts |
| "common prefix", "shared start" | Column-by-column scan |
| "find the pattern", "occurrences of" | `str.find` in practice; KMP to explain guaranteed O(n + m) |
| "balanced", "nested", "matching pairs" | A stack |

## Common Mistakes

- **Counting with a 26-slot list on text that is not lowercase `a`–`z`**, causing negative or out-of-range indexes —
  use a dictionary for general text.
- **Using a list as a dictionary key** for grouping; convert to a tuple or a string first.
- **Forgetting to shrink (or finalize) the window** after the loop, or shrinking it before it is valid.
- **Updating the best window outside the `while` loop** in variable-window problems, so the best answer is missed.
- **Resetting the KMP state to zero after a full match**, which loses overlapping matches.
- **Implementing your own substring search when `in` or `str.find` would do** in production code.
- **Forgetting the empty-pattern and pattern-longer-than-text edge cases.**

## Module Summary

The Strings module treated text as an array with three twists. [String Fundamentals](string-fundamentals.md)
covered immutability, Unicode code points versus bytes, comparison, and why building strings with repeated `+`
can be quadratic while `join` is linear. [String Manipulation](string-manipulation.md) practised reversing,
splitting, counting, run-length encoding, shifting letters, and rotation. [Palindrome Problems](palindrome-problems.md)
built on two pointers and expansion from the center. This file collected the recurring patterns — counting,
two pointers, windows, prefixes, matching, and stacks.

Carry these ideas forward:

- Strings are immutable: edit a list, build with `join`, and slice sparingly.
- Count with a dictionary; the next module develops that idea fully as **hashing**.
- Two pointers and sliding windows from the Arrays module apply directly to text.
- Naive substring search is O(n · m); KMP guarantees O(n + m).

## ➡️ Next

Continue to the [Recursion](../recursion/README.md) module, which introduces a different way to structure
a solution: define it in terms of a smaller version of itself.
