# 🔤 String Dynamic Programming

## Two Strings, Two Dimensions

Comparing two strings — how alike are they, how do I turn one into the other, what do they share — is a task where the answer for the whole strings is built from the answers for their **prefixes**. A table with one row per prefix of the first string and one column per prefix of the second holds every smaller question, and the answer sits in the bottom-right corner. This is the two-dimensional cousin of the [one-dimensional](one-dimensional-dp.md) and [knapsack](knapsack-patterns.md) tables, and the same five-step recipe from [dp-fundamentals.md](dp-fundamentals.md) applies.

These problems are practical, not just puzzles: the longest common subsequence is the heart of file-comparison tools such as `diff` ([Wikipedia: Longest common subsequence](https://en.wikipedia.org/wiki/Longest_common_subsequence)), edit distance drives spelling correction and fuzzy matching, and palindromic structure appears in sequence analysis. This file covers the longest common subsequence, edit distance, the longest palindromic subsequence, the longest palindromic substring, and the cheapest way to make a string a palindrome. Every solution is cross-checked against an exhaustive method — all subsequences, a breadth-first search over strings — on thousands of small inputs. All outputs were produced by running the code on CPython 3.9.

| Problem | State `table[i][j]` means… | Answer | Time | Space |
|---------|----------------------------|--------|------|-------|
| Longest common subsequence | LCS length of `a[:i]` and `b[:j]` | `table[m][n]` | O(mn) | O(mn), or O(min(m, n)) for the length |
| Edit distance | fewest edits turning `a[:i]` into `b[:j]` | `table[m][n]` | O(mn) | O(mn), or O(n) for the distance |
| Longest palindromic subsequence | longest palindromic subsequence of `s[i..j]` | `table[0][n−1]` | O(n²) | O(n²) |
| Longest palindromic substring | is `s[i..j]` a palindrome? | the longest `true` range | O(n²) | O(n²), or O(1) by expanding |

## 🔗 Longest Common Subsequence

A **subsequence** keeps characters in order but may skip some (`"ace"` is a subsequence of `"abcde"`); unlike a substring, it need not be contiguous. *What is the longest string that is a subsequence of both `a` and `b`?*

- **State:** `table[i][j]` = the length of the longest common subsequence (LCS) of the first `i` characters of `a` and the first `j` characters of `b`.
- **Transition:** compare the last characters `a[i − 1]` and `b[j − 1]`.
  - If they are **equal**, they can end a common subsequence: `table[i][j] = table[i − 1][j − 1] + 1`.
  - If they **differ**, at least one of them is not used: `table[i][j] = max(table[i − 1][j], table[i][j − 1])`.
- **Base cases:** `table[0][j] = table[i][0] = 0` (an empty string shares nothing).
- **Order:** row by row, left to right.
- **Answer:** `table[m][n]`.

To recover an actual subsequence, walk back from the corner: matching last characters go into the answer and move diagonally; otherwise move toward the larger neighbour.

```python
def lcs_table(a, b):
    m, n = len(a), len(b)
    table = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])
    return table

def lcs(a, b):
    """Return (length, one longest common subsequence)."""
    table = lcs_table(a, b)
    i, j, pieces = len(a), len(b), []
    while i and j:
        if a[i - 1] == b[j - 1]:
            pieces.append(a[i - 1])                                 # a matching character belongs to the subsequence
            i, j = i - 1, j - 1
        elif table[i - 1][j] >= table[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return table[len(a)][len(b)], "".join(reversed(pieces))

a, b = "AGGTAB", "GXTXAYB"
print(lcs(a, b))
print("      " + "  ".join(["-"] + list(b)))
for i, row in enumerate(lcs_table(a, b)):
    print(f"{'-' if i == 0 else a[i - 1]:>4}  " + "  ".join(str(cell) for cell in row))
```

```text
(4, 'GTAB')
      -  G  X  T  X  A  Y  B
   -  0  0  0  0  0  0  0  0
   A  0  0  0  0  0  1  1  1
   G  0  1  1  1  1  1  1  1
   G  0  1  1  1  1  1  1  1
   T  0  1  1  2  2  2  2  2
   A  0  1  1  2  2  3  3  3
   B  0  1  1  2  2  3  3  4
```

The first line is the answer: `GTAB`, length 4. The grid below it is the table: the value in each cell is the LCS length for the two prefixes that end at that row and column; the bottom-right cell holds 4. Whenever the row's letter equals the column's letter, the value is the diagonal neighbour plus one.

### Saving Memory

Row `i` depends only on row `i − 1`, so if only the *length* is needed, two rows suffice. Reconstructing the subsequence needs the whole table (or a smarter divide-and-conquer method).

```python
def lcs_length_two_rows(a, b):
    if len(b) > len(a):
        a, b = b, a                                                  # keep the rows as short as possible
    previous = [0] * (len(b) + 1)
    for ch in a:
        current = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            current[j] = previous[j - 1] + 1 if ch == b[j - 1] else max(previous[j], current[j - 1])
        previous = current
    return previous[-1]

print(lcs_length_two_rows("AGGTAB", "GXTXAYB"))                      # 4
```

The next block compares the two on two random DNA-like strings of 2,000 letters:

```python
import random
import sys
import timeit

random.seed(5)
x = "".join(random.choice("ACGT") for _ in range(2_000))
y = "".join(random.choice("ACGT") for _ in range(2_000))
full_table = lcs_table(x, y)
assert full_table[-1][-1] == lcs_length_two_rows(x, y)
table_bytes = sys.getsizeof(full_table) + sum(sys.getsizeof(row) for row in full_table)
rows_bytes = 2 * sys.getsizeof([0] * 2_001)
full_ms = min(timeit.repeat(lambda: lcs_table(x, y), number=1, repeat=2)) * 1000
rows_ms = min(timeit.repeat(lambda: lcs_length_two_rows(x, y), number=1, repeat=2)) * 1000
print(f"LCS length of two 2,000-letter strings: {full_table[-1][-1]}")
print(f"full table: {full_ms:6.0f} ms, {table_bytes / 1e6:6.1f} MB of list storage")
print(f"two rows:   {rows_ms:6.0f} ms, {rows_bytes / 1e3:6.1f} KB of list storage")
```

Output:

```
LCS length of two 2,000-letter strings: 1304
full table:    747 ms,   32.2 MB of list storage
two rows:      528 ms,   32.1 KB of list storage
```

Both do the same 4 million cell updates, but the two-row version needs about a thousand times less memory. The time difference is smaller because the work per cell is the same; it comes from allocating less.

## ✏️ Edit Distance

*What is the fewest single-character edits — insert a character, delete a character, or replace one — that turn string `a` into string `b`?* This is the **Levenshtein distance**, and it measures how different two words are: `"kitten"` becomes `"sitting"` in three edits.

- **State:** `d[i][j]` = the fewest edits to turn the first `i` characters of `a` into the first `j` characters of `b`.
- **Transition:** consider the last characters.
  - **Delete** `a[i − 1]`: `d[i − 1][j] + 1`.
  - **Insert** `b[j − 1]` at the end: `d[i][j − 1] + 1`.
  - **Replace** `a[i − 1]` by `b[j − 1]`: `d[i − 1][j − 1] + 1` — or `+ 0` if they are already equal.
  - Take the minimum of the three.
- **Base cases:** `d[i][0] = i` (delete everything) and `d[0][j] = j` (insert everything).
- **Answer:** `d[m][n]`.

As with the LCS, walking back through the table shows which edits were used:

```python
def edit_table(a, b):
    m, n = len(a), len(b)
    d = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        d[i][0] = i
    for j in range(n + 1):
        d[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            d[i][j] = min(d[i - 1][j] + 1,                              # delete
                          d[i][j - 1] + 1,                              # insert
                          d[i - 1][j - 1] + (a[i - 1] != b[j - 1]))     # replace, or keep when equal
    return d

def edit_script(a, b):
    """Return (distance, the list of operations that turns a into b)."""
    d = edit_table(a, b)
    i, j, operations = len(a), len(b), []
    while i or j:
        if i and j and d[i][j] == d[i - 1][j - 1] + (a[i - 1] != b[j - 1]):
            operations.append(("keep", a[i - 1]) if a[i - 1] == b[j - 1] else ("replace", a[i - 1], b[j - 1]))
            i, j = i - 1, j - 1
        elif i and d[i][j] == d[i - 1][j] + 1:
            operations.append(("delete", a[i - 1]))
            i -= 1
        else:
            operations.append(("insert", b[j - 1]))
            j -= 1
    return d[len(a)][len(b)], list(reversed(operations))

distance, operations = edit_script("kitten", "sitting")
print(distance)
for operation in operations:
    print(" ", operation)
print(edit_table("intention", "execution")[9][9], edit_table("", "abc")[0][3], edit_table("same", "same")[4][4])
```

```text
3
  ('replace', 'k', 's')
  ('keep', 'i')
  ('keep', 't')
  ('keep', 't')
  ('replace', 'e', 'i')
  ('keep', 'n')
  ('insert', 'g')
5 3 0
```

The three non-"keep" operations are the whole transformation: replace `k` by `s`, replace `e` by `i`, and insert `g` at the end. The classic pair `"intention"` and `"execution"` is 5 edits apart.

## 🪞 Palindromes in Strings

A **palindrome** reads the same forwards and backwards. Two related questions ask for a palindrome *inside* a string, and the difference between "subsequence" and "substring" changes the algorithm.

### Longest Palindromic Subsequence

*Which is the longest palindrome you can get by deleting characters (but keeping order)?* A palindromic subsequence of `s` is a subsequence of `s` that is also a subsequence of `s` reversed, and conversely a common subsequence of `s` and its reverse is a palindrome-shaped pattern — so the answer is simply the **LCS of `s` and `s[::-1]`**. A direct interval DP works as well:

- **State:** `best[i][j]` = the longest palindromic subsequence within `s[i..j]`.
- **Transition:** if `s[i] == s[j]`, they wrap the best palindrome inside: `best[i + 1][j − 1] + 2`; otherwise drop one end: `max(best[i + 1][j], best[i][j − 1])`.
- **Base case:** `best[i][i] = 1`.

```python
def longest_palindromic_subsequence(s):
    n = len(s)
    if n == 0:
        return 0
    best = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):                                     # i runs down so that row i + 1 is ready
        best[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                best[i][j] = best[i + 1][j - 1] + 2
            else:
                best[i][j] = max(best[i + 1][j], best[i][j - 1])
    return best[0][n - 1]

def longest_palindromic_subsequence_via_lcs(s):
    return lcs_table(s, s[::-1])[len(s)][len(s)]

print(longest_palindromic_subsequence("bbbab"), longest_palindromic_subsequence("cbbd"), longest_palindromic_subsequence_via_lcs("bbbab"))       # 4 2 4
```

For `"bbbab"` the longest palindromic subsequence is `"bbbb"`, found by skipping the `a`.

### Longest Palindromic Substring

*Which is the longest **contiguous** palindrome?* A DP table `is_palindrome[i][j]` can be filled by growing lengths (`s[i..j]` is a palindrome if `s[i] == s[j]` and the inside `s[i+1..j−1]` is one). But there is a simpler method that needs no table at all: every palindrome has a **center**, so expand outward from each of the `2n − 1` possible centers (each character, and each gap between two characters) while the two ends match. It is O(n²) time and O(1) space, and it is the standard answer; the strings module analyses it in [palindrome-problems.md](../strings/palindrome-problems.md), including the O(n) Manacher algorithm.

```python
def longest_palindromic_substring_expand(s):
    best_start, best_end = 0, 0
    for center in range(len(s)):
        for left, right in ((center, center), (center, center + 1)):      # odd-length and even-length palindromes
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left, right = left - 1, right + 1
            if right - left - 1 > best_end - best_start:
                best_start, best_end = left + 1, right
    return s[best_start:best_end]

def longest_palindromic_substring_table(s):
    n = len(s)
    if n == 0:
        return ""
    is_palindrome = [[False] * n for _ in range(n)]
    best = (0, 0)
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and (length <= 2 or is_palindrome[i + 1][j - 1]):
                is_palindrome[i][j] = True
                if length > best[1] - best[0] + 1:
                    best = (i, j)
    return s[best[0]:best[1] + 1]

print(longest_palindromic_substring_expand("babad"), longest_palindromic_substring_table("cbbd"), longest_palindromic_substring_expand("a"))        # bab bb a
```

(For `"babad"`, both `"bab"` and `"aba"` are correct answers of length 3; which one a method returns depends on its tie-breaking.)

### Fewest Insertions to Make a Palindrome

*What is the smallest number of characters that must be inserted into `s` to make it a palindrome?* Keep the longest palindromic subsequence in place — those characters already pair up — and insert a mirror for every other character. So the answer is **`len(s) − longest_palindromic_subsequence(s)`**. A small interval DP also builds the palindrome itself:

```python
def make_palindrome(s):
    """Return a shortest palindrome that has s as a subsequence (insertions only)."""
    n = len(s)
    if n == 0:
        return ""
    cost = [[0] * n for _ in range(n)]                                 # cost[i][j] = insertions needed for s[i..j]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cost[i][j] = cost[i + 1][j - 1] if s[i] == s[j] else 1 + min(cost[i + 1][j], cost[i][j - 1])
    left, right, i, j = [], [], 0, n - 1
    while i < j:
        if s[i] == s[j]:
            left.append(s[i]); right.append(s[j]); i, j = i + 1, j - 1
        elif cost[i + 1][j] <= cost[i][j - 1]:
            left.append(s[i]); right.append(s[i]); i += 1               # insert a mirror of s[i] on the right
        else:
            left.append(s[j]); right.append(s[j]); j -= 1               # insert a mirror of s[j] on the left
    middle = s[i] if i == j else ""
    return "".join(left) + middle + "".join(reversed(right))

for word in ("mbadm", "abcd", "level"):
    palindrome = make_palindrome(word)
    print(f"{word!r:>8} -> {palindrome!r:<12} insertions: {len(palindrome) - len(word)} = {len(word)} - {longest_palindromic_subsequence(word)}")
```

```text
 'mbadm' -> 'mbadabm'    insertions: 2 = 5 - 3
  'abcd' -> 'abcdcba'    insertions: 3 = 4 - 1
 'level' -> 'level'      insertions: 0 = 5 - 5
```

## ✅ Verification

Each solution was compared with a method that shares none of its logic: every subsequence for the LCS and the palindromic subsequence, a breadth-first search over strings for the edit distance and for the cheapest palindrome, and every substring for the longest palindromic substring:

```python
import random
from collections import deque

def is_subsequence(small, big):
    iterator = iter(big)
    return all(ch in iterator for ch in small)

def lcs_brute(a, b):
    return max(len(sub) for sub in ("".join(a[i] for i in range(len(a)) if mask >> i & 1) for mask in range(1 << len(a))) if is_subsequence(sub, b))

def palindromic_subsequence_brute(s):
    best = 0
    for mask in range(1 << len(s)):
        sub = "".join(s[i] for i in range(len(s)) if mask >> i & 1)
        if sub == sub[::-1]:
            best = max(best, len(sub))
    return best

def palindromic_substring_brute(s):
    return max((j - i for i in range(len(s)) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1]), default=0)

def edit_distance_by_search(a, b, alphabet="abc"):
    seen, queue = {a}, deque([(a, 0)])
    while queue:
        current, steps = queue.popleft()
        if current == b:
            return steps
        neighbours = set()
        for i in range(len(current) + 1):
            neighbours.update(current[:i] + ch + current[i:] for ch in alphabet)           # insertions
        for i in range(len(current)):
            neighbours.add(current[:i] + current[i + 1:])                                   # deletions
            neighbours.update(current[:i] + ch + current[i + 1:] for ch in alphabet)       # replacements
        for neighbour in neighbours:
            if neighbour not in seen and len(neighbour) <= max(len(a), len(b)) + 1:
                seen.add(neighbour)
                queue.append((neighbour, steps + 1))

def insertions_by_search(s):
    seen, queue = {s}, deque([(s, 0)])
    while queue:
        current, steps = queue.popleft()
        if current == current[::-1]:
            return steps
        for i in range(len(current) + 1):
            for ch in "ab":
                grown = current[:i] + ch + current[i:]
                if grown not in seen:
                    seen.add(grown)
                    queue.append((grown, steps + 1))

def apply_script(operations):
    return "".join(op[1] if op[0] in ("keep", "insert") else op[2] if op[0] == "replace" else "" for op in operations)

random.seed(1)
for _ in range(1_500):
    a = "".join(random.choice("abc") for _ in range(random.randint(0, 8)))
    b = "".join(random.choice("abc") for _ in range(random.randint(0, 8)))
    length, common = lcs(a, b)
    assert length == len(common) == lcs_brute(a, b) == lcs_length_two_rows(a, b)
    assert is_subsequence(common, a) and is_subsequence(common, b)
    s = "".join(random.choice("abc") for _ in range(random.randint(0, 10)))
    assert longest_palindromic_subsequence(s) == longest_palindromic_subsequence_via_lcs(s) == palindromic_subsequence_brute(s)
    centre, table = longest_palindromic_substring_expand(s), longest_palindromic_substring_table(s)
    assert len(centre) == len(table) == palindromic_substring_brute(s) and centre == centre[::-1] and table == table[::-1] and centre in s and table in s

for _ in range(250):
    a = "".join(random.choice("abc") for _ in range(random.randint(0, 4)))
    b = "".join(random.choice("abc") for _ in range(random.randint(0, 4)))
    distance, operations = edit_script(a, b)
    assert distance == edit_table(a, b)[len(a)][len(b)] == edit_distance_by_search(a, b)
    assert sum(op[0] != "keep" for op in operations) == distance and apply_script(operations) == b
    word = "".join(random.choice("ab") for _ in range(random.randint(0, 6)))
    palindrome = make_palindrome(word)
    assert len(palindrome) - len(word) == len(word) - longest_palindromic_subsequence(word) == insertions_by_search(word)
    assert palindrome == palindrome[::-1] and is_subsequence(word, palindrome)
print("LCS, edit distance, palindromic subsequence and substring, and shortest palindrome agree with exhaustive methods")
```

```text
LCS, edit distance, palindromic subsequence and substring, and shortest palindrome agree with exhaustive methods
```

## Common Mistakes

- **Confusing subsequence with substring.** A subsequence may skip characters; a substring is contiguous. The LCS and the longest common *substring* use different recurrences (the substring version resets to 0 on a mismatch).
- **Off-by-one between table and string indexes.** The table has `m + 1` rows and `n + 1` columns, so cell `[i][j]` refers to `a[i − 1]` and `b[j − 1]`.
- **Forgetting the base row and column** in edit distance: `d[i][0] = i` and `d[0][j] = j`, not 0.
- **Counting a replacement of equal characters as an edit.** The diagonal move costs `0` when the characters match.
- **Reconstructing a solution without keeping the table.** The two-row optimization gives the length only; keep the full table, or parent pointers, to recover the subsequence or the operations.
- **Using the palindromic-substring table when expand-around-center suffices.** The table costs O(n²) memory; the center expansion uses O(1) and is just as simple.
- **Assuming the answer is unique.** Many strings share several longest common subsequences or optimal edit scripts; tests should check the *length* or validity, not one specific string.

## Module Summary

This module turned recursion that repeats itself into algorithms that remember. [DP Fundamentals](dp-fundamentals.md) defined the two properties — optimal substructure and overlapping subproblems — showed the Fibonacci recursion collapse from millions of calls to a few dozen with a cache, compared top-down memoization with bottom-up tabulation (recursion limits, states visited, space optimization), gave the five-step recipe, and showed where greedy fails. [One-Dimensional DP](one-dimensional-dp.md) applied the recipe to climbing stairs, house robber, decode ways, coin change, maximum subarray, longest increasing subsequence (with an O(n log n) refinement), and word break. [Knapsack Patterns](knapsack-patterns.md) added a capacity dimension: 0/1 and unbounded knapsack, subset sum with a bitset shortcut, partition, signed sums, combinations versus permutations, and the meaning of pseudo-polynomial time. This file used two dimensions of string positions for the longest common subsequence, edit distance, and palindromes.

Carry these ideas forward:

- Write down the **state** in one sentence, then the **transition**, **base cases**, **order**, and **answer**; the time is the number of states times the work per state.
- A recursion with repeated subproblems becomes polynomial with a cache; use top-down when few states are reachable, bottom-up when the table is dense or the recursion is deep.
- If a row depends only on the previous one, keep only that row — but then you can recover the value, not the solution, unless you also store choices.
- Check every DP against a brute-force version on tiny inputs; most bugs are in base cases and indexes.
- Greedy is faster than DP when it is *provably* correct; when it is not, DP is the safe tool.
- Dynamic programming over a graph (Floyd-Warshall), over intervals (palindromes), over subsets, and over trees are all the same recipe with a different state.

## ➡️ Next

Continue to the [Tries](../tries/README.md) module, the next module in this domain, where the focus moves to a tree built for strings — one that answers prefix questions in time proportional to the length of the query, and that combines naturally with bit manipulation and with dynamic programming.
