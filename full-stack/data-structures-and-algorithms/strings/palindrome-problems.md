# 🪞 Palindrome Problems

## One Idea, Many Questions

A **palindrome** reads the same forward and backward: `racecar`, `noon`, `A man, a plan, a canal: Panama`
(once you ignore spaces, punctuation, and case). Palindromes are a favorite interview family because a single
idea — *compare from the outside in, or grow from the inside out* — answers a whole range of questions of
increasing difficulty. This file works through six of them, from "is it a palindrome?" to "what is the
longest palindromic substring?".

Every function below was tested against a brute-force version on thousands of random strings, in addition to
the documented examples.

## 1️⃣ The Basic Check

Compare the first and last characters, then move inward. This is the opposite-ends
[two-pointer technique](../arrays/two-pointer-technique.md):

```python
def is_palindrome(text):
    left, right = 0, len(text) - 1
    while left < right:
        if text[left] != text[right]:
            return False
        left += 1
        right -= 1
    return True

print(is_palindrome("racecar"))   # True
print(is_palindrome("noon"))      # True    — an even-length palindrome
print(is_palindrome("python"))    # False
print(is_palindrome(""))          # True    — nothing to compare, so nothing can differ
print(is_palindrome("x"))         # True
```

O(n) time and O(1) extra space. The shorter alternative, `text == text[::-1]`, is correct and idiomatic, but
it builds a full reversed copy (O(n) space) and cannot stop early on a mismatch in the middle.

## 2️⃣ Ignoring Case, Spaces, and Punctuation

Real phrases are not clean. The "valid palindrome" version of the problem only considers letters and digits
and ignores case. The easy solution builds a cleaned string first (O(n) extra space). The better one keeps
two pointers and **skips** characters that do not count:

```python
def is_palindrome_phrase(text):
    left, right = 0, len(text) - 1
    while left < right:
        while left < right and not text[left].isalnum():
            left += 1                              # skip punctuation and spaces on the left
        while left < right and not text[right].isalnum():
            right -= 1                             # ...and on the right
        if text[left].lower() != text[right].lower():
            return False
        left += 1
        right -= 1
    return True

print(is_palindrome_phrase("A man, a plan, a canal: Panama"))   # True
print(is_palindrome_phrase("race a car"))                        # False
print(is_palindrome_phrase(".,"))                                # True    — no alphanumeric characters at all
```

The inner `while` loops still only move each pointer forward at most `n` times in total, so the whole function is
O(n) time and O(1) extra space. The extra `left < right` conditions in the inner loops prevent the pointers
from crossing while skipping — leaving them out is a classic source of `IndexError`. (As noted in
[string-fundamentals.md](string-fundamentals.md), `isalnum` and `lower` follow Unicode rules, which is usually
what you want for natural-language text.)

## 3️⃣ A Palindrome After Removing One Character

*Can the string become a palindrome by deleting at most one character?* Start the same way. At the first
mismatch, one of the two mismatched characters must be the one that gets deleted — there is no other
possibility, since everything outside them already matched. So try both options and check whether either
remainder is a palindrome:

```python
def valid_palindrome_after_one_removal(text):
    def is_pal(left, right):
        while left < right:
            if text[left] != text[right]:
                return False
            left += 1
            right -= 1
        return True

    left, right = 0, len(text) - 1
    while left < right:
        if text[left] != text[right]:
            return is_pal(left + 1, right) or is_pal(left, right - 1)
        left += 1
        right -= 1
    return True

print(valid_palindrome_after_one_removal("abca"))     # True    — remove 'b' or 'c' to get "aca" / "aba"
print(valid_palindrome_after_one_removal("abc"))      # False
print(valid_palindrome_after_one_removal("racecar"))  # True    — already a palindrome, zero removals needed
```

The helper takes **indexes instead of slices** so no substring is copied. The total work is two scans of at
most `n` characters — O(n) time, O(1) space. The brute-force alternative (try deleting each character and test
the result) is O(n²).

## 4️⃣ The Longest Palindromic Substring (Expand Around the Center)

Every palindrome has a center: a single character (odd length, like `aba`) or the gap between two characters
(even length, like `abba`). Instead of checking every substring — O(n³) — **grow outward from each center**
for as long as the characters on both sides match:

```python
def longest_palindromic_substring(text):
    if not text:
        return ""
    best_start, best_length = 0, 1

    def expand(left, right):
        while left >= 0 and right < len(text) and text[left] == text[right]:
            left -= 1
            right += 1
        return left + 1, right - left - 1          # start and length of the palindrome found

    for center in range(len(text)):
        for left, right in ((center, center), (center, center + 1)):   # odd, then even
            start, length = expand(left, right)
            if length > best_length:
                best_start, best_length = start, length
    return text[best_start:best_start + best_length]

print(longest_palindromic_substring("babad"))     # bab     — "aba" is equally long
print(longest_palindromic_substring("cbbd"))      # bb
print(longest_palindromic_substring("forgeeksskeegfor"))   # geeksskeeg
print(longest_palindromic_substring("a"))         # a
```

There are `2n - 1` centers, and each expansion costs up to O(n), so the worst case is **O(n²) time with O(1)
extra space**. The worst case really occurs: a string of identical characters makes every expansion run to
the edges. This benchmark times the function above on that input and on random letters:

```python
import random
import timeit

random.seed(1)
print(f"{'n':>6} | {'all a (worst)':>14} | {'random letters':>14}   (ms)")
for n in (500, 1000, 2000, 4000):
    worst = "a" * n
    typical = "".join(random.choice("abcdefghij") for _ in range(n))
    t_worst = min(timeit.repeat(lambda: longest_palindromic_substring(worst), number=1, repeat=3)) * 1000
    t_typical = min(timeit.repeat(lambda: longest_palindromic_substring(typical), number=1, repeat=3)) * 1000
    print(f"{n:>6,} | {t_worst:14.2f} | {t_typical:14.2f}")
```

One run on the test machine printed:

```
     n |  all a (worst) | random letters   (ms)
   500 |          12.85 |           0.30
 1,000 |          51.95 |           0.60
 2,000 |         208.77 |           1.21
 4,000 |         826.94 |           2.39
```

Doubling `n` roughly **quadruples** the worst-case time (quadratic), while the random input roughly doubles
(close to linear, because expansions stop after a character or two). That gap between worst case and typical
case is exactly what Big-O's "worst case" language describes — see
[time-complexity.md](../time-and-space-complexity/time-complexity.md).

Two alternatives exist, both beyond this module: a dynamic-programming table (O(n²) time *and* space — see the
Dynamic Programming module later in this domain), and **Manacher's algorithm**, which finds the answer in O(n)
time ([GeeksforGeeks: Manacher's Algorithm](https://www.geeksforgeeks.org/dsa/manachers-algorithm-linear-time-longest-palindromic-substring-part-1/)).
Expand-around-center is the standard interview answer because it is short and its O(1) space is hard to beat.

## 5️⃣ Counting Palindromic Substrings

The same expansion counts palindromes instead of finding the longest: **every successful step of an
expansion is one more palindromic substring**.

```python
def count_palindromic_substrings(text):
    total = 0

    def count_from(left, right):
        count = 0
        while left >= 0 and right < len(text) and text[left] == text[right]:
            count += 1
            left -= 1
            right += 1
        return count

    for center in range(len(text)):
        total += count_from(center, center)         # odd-length palindromes
        total += count_from(center, center + 1)     # even-length palindromes
    return total

print(count_palindromic_substrings("abc"))    # 3    — "a", "b", "c"
print(count_palindromic_substrings("aaa"))    # 6    — "a" x3, "aa" x2, "aaa"
```

Substrings are counted by *position*, so the two `"a"` palindromes at different places count separately.

## 6️⃣ Can the Letters Be Rearranged Into a Palindrome?

This one is about **counts**, not order. In any palindrome, every character appears an even number of times,
except possibly one (the middle of an odd-length palindrome). So the answer is yes when *at most one*
character has an odd count. A set that toggles membership tracks the odd counts without storing numbers:

```python
def can_form_palindrome(text):
    odd = set()
    for ch in text:
        if ch in odd:
            odd.remove(ch)       # seen an even number of times so far
        else:
            odd.add(ch)          # seen an odd number of times so far
    return len(odd) <= 1

print(can_form_palindrome("carrace"))   # True    — rearranges to "racecar"
print(can_form_palindrome("aabb"))      # True    — "abba"
print(can_form_palindrome("abc"))       # False   — three characters with odd counts
```

One pass, O(n) time, and the set never holds more than the number of distinct characters. This is a small
example of the [hash-based](../hashing/hash-based-problem-solving.md) "track what you have seen" pattern. The
brute-force alternative of generating every permutation would take O(n!) time.

## 🔢 A Related Question: Palindromic Numbers

Is `12321` a palindrome, **without converting it to a string**? Reverse only the *second half* of the digits
and compare it with the first half, which also avoids overflow in languages with fixed-size integers:

```python
def is_palindrome_number(x):
    if x < 0 or (x % 10 == 0 and x != 0):
        return False                          # negatives and numbers ending in 0 can't be palindromes
    reversed_half = 0
    while x > reversed_half:
        reversed_half = reversed_half * 10 + x % 10    # move the last digit of x onto reversed_half
        x //= 10
    return x == reversed_half or x == reversed_half // 10   # even digits / odd digits (drop the middle one)

print(is_palindrome_number(12321))   # True
print(is_palindrome_number(1221))    # True
print(is_palindrome_number(120))     # False
print(is_palindrome_number(-121))    # False
```

The loop runs about half as many times as there are digits, so it takes O(log₁₀ x) time and O(1) space.

## 🌀 A Recursive Version

Palindromes also have a natural recursive definition: *a string is a palindrome if its first and last
characters match and the part between them is a palindrome.* The [Recursion](../recursion/README.md) module
develops this style; here is the idea using indexes so that no substring is copied:

```python
def is_palindrome_recursive(text, left=0, right=None):
    if right is None:
        right = len(text) - 1
    if left >= right:                      # base case: zero or one character left
        return True
    if text[left] != text[right]:          # base case: a mismatch
        return False
    return is_palindrome_recursive(text, left + 1, right - 1)    # shrink the problem

print(is_palindrome_recursive("racecar"))    # True
print(is_palindrome_recursive("racecars"))   # False
```

Writing the recursion with slices (`text[1:-1]`) would be tidier but copies the remaining string at every
level, making the whole check O(n²). The call stack also uses O(n) space, so the iterative two-pointer version
is preferable in practice — see [recursion-fundamentals.md](../recursion/recursion-fundamentals.md).

## 🧠 Choosing the Approach

| Question | Technique | Time | Extra space |
|----------|-----------|------|-------------|
| Is it a palindrome? | Two pointers inward | O(n) | O(1) |
| ...ignoring case and punctuation? | Two pointers that skip characters | O(n) | O(1) |
| ...after removing one character? | Two pointers, branch at the first mismatch | O(n) | O(1) |
| Longest palindromic substring | Expand around each center | O(n²) | O(1) |
| Number of palindromic substrings | Expand around each center, count steps | O(n²) | O(1) |
| Can letters be rearranged into one? | Track odd counts with a set | O(n) | O(k) |
| Is an integer a palindrome? | Reverse half the digits | O(log x) | O(1) |

## Common Mistakes

- **Forgetting the empty string and single characters** — both are palindromes by definition.
- **Moving skipping pointers past each other**, which causes `IndexError` or wrong answers. Keep
  `left < right` in every inner loop.
- **Handling only odd-length (or only even-length) centers** in expand-around-center.
- **Returning the length when the substring is asked for**, or the reverse, when mixing up `start` and `length`.
- **Slicing inside loops or recursion**, quietly turning an O(n) idea into O(n²).
- **Counting by value instead of position** when the problem counts occurrences of palindromic substrings.
- **Forgetting that palindrome checks on phrases need a definition** of which characters count.

## ➡️ Next

Continue to [string-patterns.md](string-patterns.md) for the reusable techniques that most remaining string
problems are built from: frequency counting, windows, prefixes, and pattern matching.
