# 🔡 Prefix Problems

## Problems a Sorted List Cannot Branch Through

A sorted list of words answers a plain prefix query beautifully, as [trie-fundamentals.md](trie-fundamentals.md) measured. But many real problems ask something a sorted list cannot express: *the best few completions by popularity*, *the shortest known prefix of a word*, *a pattern with a wildcard*, *every dictionary word hidden in a grid of letters*. What these have in common is that the answer depends on **many partial matches at once**, and a trie handles that by walking the prefix tree and **pruning** every branch that cannot lead anywhere.

This file works through five problems — ranked autocomplete, replacing words by their roots, wildcard search, the longest word that can be built one letter at a time, and finding dictionary words on a letter board — each with a brute-force or regex cross-check on thousands of random cases. They all share one small node class. All outputs were produced by running the code on CPython 3.9.

```python
class Node:
    __slots__ = ("children", "end", "freq")

    def __init__(self):
        self.children = {}                 # next character -> child node
        self.end = False                   # does a word end here?
        self.freq = 0                      # how often that word was used (for ranking)

class WordTrie:
    def __init__(self, words=()):
        self.root = Node()
        for word in words:
            self.insert(word)

    def insert(self, word, freq=1):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, Node())
        node.end = True
        node.freq += freq

    def walk(self, text):
        """The node reached by following text from the root, or None."""
        node = self.root
        for ch in text:
            node = node.children.get(ch)
            if node is None:
                return None
        return node
```

## 1️⃣ Ranked Autocomplete

*A search box suggests completions for what has been typed so far — but the most popular ones should come first, not just the alphabetically first.* Store a usage count on the node where each word ends. To suggest completions, walk to the prefix's node, collect every word in the subtree with its count, and keep the top `k` by count (ties broken alphabetically). `heapq.nsmallest` over the negated counts then selects the best `k` without sorting every candidate ([heap-problems.md](../heaps-and-priority-queues/heap-problems.md)):

```python
import heapq
import random

def suggest(trie, prefix, k):
    """The k most frequently used words that start with prefix; ties are broken alphabetically."""
    node = trie.walk(prefix)
    if node is None:
        return []
    candidates, stack = [], [(node, prefix)]
    while stack:
        current, text = stack.pop()
        if current.end:
            candidates.append((-current.freq, text))               # negate: nsmallest then gives the highest counts
        for ch, child in current.children.items():
            stack.append((child, text + ch))
    return [word for _, word in heapq.nsmallest(k, candidates)]

usage = {"i": 5, "island": 3, "ironman": 2, "iphone": 9, "ipad": 9, "ios": 4}
ranked = WordTrie()
for word, count in usage.items():
    ranked.insert(word, count)
print(suggest(ranked, "i", 3), suggest(ranked, "ip", 5), suggest(ranked, "is", 2), suggest(ranked, "x", 2))      # ['ipad', 'iphone', 'i'] ['ipad', 'iphone'] ['island'] []
```

The two most-used words, `ipad` and `iphone` (9 each), come first in alphabetical order, then `i` (5). The cost is the length of the prefix plus the size of the subtree below it; production systems cache the best `k` in each node to avoid that traversal, at the price of updating them whenever a count changes.

## 2️⃣ Replace Words With Their Shortest Roots

*Given a dictionary of "roots" and a sentence, replace every word that begins with a root by the shortest such root.* With roots `cat`, `bat`, and `rat`, the sentence `the cattle was rattled by the battery` becomes `the cat was rat by the bat`. Insert all roots into a trie; for each word, walk down its letters, and **stop at the first node that ends a root** — the first one reached is by construction the shortest:

```python
def replace_words(sentence, roots):
    trie = WordTrie(roots)
    result = []
    for word in sentence.split():
        node, replacement = trie.root, word
        for position, ch in enumerate(word):
            node = node.children.get(ch)
            if node is None:
                break                                              # no root starts like this word
            if node.end:
                replacement = word[:position + 1]                  # the first root reached is the shortest
                break
        result.append(replacement)
    return " ".join(result)

print(replace_words("the cattle was rattled by the battery", ["cat", "bat", "rat"]))        # the cat was rat by the bat
```

Each word costs at most the length of its shortest matching root, independent of the number of roots. Comparing each word against every root would cost `words × roots` string comparisons.

## 3️⃣ Wildcard Search

*A dictionary supports adding words and searching, where a search pattern may contain `.` meaning "any single letter".* A sorted list cannot do this, because `.` matches many different next letters. A trie **branches**: at a literal letter it follows that one edge; at a `.` it tries every child:

```python
class WildcardDictionary:
    def __init__(self):
        self.trie = WordTrie()

    def add(self, word):
        self.trie.insert(word)

    def search(self, pattern):
        def match(node, i):
            if i == len(pattern):
                return node.end                                    # the pattern is used up: it matches if a word ends here
            ch = pattern[i]
            if ch == ".":
                return any(match(child, i + 1) for child in node.children.values())
            child = node.children.get(ch)
            return child is not None and match(child, i + 1)
        return match(self.trie.root, 0)

dictionary = WildcardDictionary()
for word in ("bad", "dad", "mad"):
    dictionary.add(word)
print([dictionary.search(pattern) for pattern in ("pad", "bad", ".ad", "b..", "b.", "...")])      # [False, True, True, True, False, True]
```

The cost is proportional to the number of trie nodes that the pattern can actually reach: a pattern with no wildcards is as cheap as an ordinary lookup, and a pattern full of dots explores a subtree, but never more than the nodes at each depth. (The recursion depth equals the pattern length, so for very long patterns an explicit stack would be needed.)

## 4️⃣ The Longest Word Built One Letter at a Time

*Given a list of words, find the longest word such that every one of its prefixes (of length 1, 2, …) is also in the list; among equally long answers, return the alphabetically smallest.* In the list `a, ap, app, appl, apple, apply, banana`, the word `banana` is not buildable because `b` is not a word. In the trie, a word is buildable exactly when the path to it passes **only through word-ending nodes**. So traverse the trie but never step onto a child that does not end a word; the deepest node reached is the answer:

```python
def longest_buildable_word(words):
    trie = WordTrie(words)
    best = ""
    stack = [(trie.root, "")]
    while stack:
        node, text = stack.pop()
        if len(text) > len(best) or (len(text) == len(best) and text < best):
            best = text
        for ch, child in node.children.items():
            if child.end:                                          # only continue through nodes that are themselves words
                stack.append((child, text + ch))
    return best

print(longest_buildable_word(["w", "wo", "wor", "worl", "world"]), longest_buildable_word(["a", "banana", "app", "appl", "ap", "apply", "apple"]))       # world apple
```

## 5️⃣ Finding Dictionary Words on a Letter Board

*A grid of letters and a list of words: which words can be spelled by walking from cell to adjacent cell (up, down, left, right), never using a cell twice within one word?* The naive method searches the board once per word: for each word, try every starting cell and extend letter by letter. If the dictionary has 50,000 words, the board is searched 50,000 times, and the searches for `intern`, `internal`, and `internet` repeat the same walk over and over.

The trie turns the question around. Search the board **once**, carrying a pointer into the trie: stepping onto a cell is allowed only if the trie has an edge for that letter, so every path that is not a prefix of some word is **cut off immediately**, and any word reached on the way is recorded:

```python
from collections import Counter

NEIGHBOURS = ((1, 0), (-1, 0), (0, 1), (0, -1))

def board_words_with_trie(board, words):
    trie = WordTrie(words)
    rows, cols = len(board), len(board[0])
    found = set()

    def explore(r, c, node, path):
        letter = board[r][c]
        child = node.children.get(letter)
        if child is None:
            return                                                 # no word continues this way: prune
        path += letter
        if child.end:
            found.add(path)
        board[r][c] = "#"                                          # mark the cell as used on this path
        for dr, dc in NEIGHBOURS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
                explore(nr, nc, child, path)
        board[r][c] = letter                                       # un-mark when backtracking

    for r in range(rows):
        for c in range(cols):
            explore(r, c, trie.root, "")
    return found

def can_spell(board, word):
    rows, cols = len(board), len(board[0])
    def explore(r, c, i):
        if board[r][c] != word[i]:
            return False
        if i == len(word) - 1:
            return True
        letter, board[r][c] = board[r][c], "#"
        ok = any(0 <= r + dr < rows and 0 <= c + dc < cols and board[r + dr][c + dc] != "#" and explore(r + dr, c + dc, i + 1)
                 for dr, dc in NEIGHBOURS)
        board[r][c] = letter
        return ok
    return any(explore(r, c, 0) for r in range(rows) for c in range(cols))

def board_words_naive(board, words):
    return {word for word in words if can_spell(board, word)}

grid = [list("oaan"), list("etae"), list("ihkr"), list("iflv")]
print(sorted(board_words_with_trie([row[:] for row in grid], ["oath", "pea", "eat", "rain", "tea", "hike"])))      # ['eat', 'oath']
```

On the example board, `oath` runs `o → a → t → h` and `eat` runs `e → a → t`; `rain`, `pea`, `tea`, and `hike` cannot be traced. Both methods find the same words (the verification at the end of this file checks it on random boards). What differs is the work. The benchmark below uses the system word list (see [trie-fundamentals.md](trie-fundamentals.md) for its source), letters drawn with the frequencies they have in that list, and boards of growing size with growing word lists; the trie method's time **includes building the trie**:

```python
def load_vocabulary():
    for path in ("/usr/share/dict/words", "/usr/dict/words"):
        try:
            with open(path, encoding="utf-8", errors="ignore") as handle:
                words = {w.strip() for w in handle}
        except OSError:
            continue
        return sorted(w for w in words if w.isalpha() and w.islower() and w.isascii() and 3 <= len(w) <= 8), path
    rng = random.Random(1)
    syllables = ["ba", "ke", "li", "mo", "nu", "ra", "so", "ti", "ve", "wa", "zi", "the", "ing", "tion", "pre", "con", "un", "re"]
    return sorted({"".join(rng.choice(syllables) for _ in range(rng.randint(2, 4))) for _ in range(60_000)}), "synthetic syllable words"

vocabulary, source = load_vocabulary()
letter_counts = Counter("".join(vocabulary))
alphabet, weights = list(letter_counts), list(letter_counts.values())
print(f"vocabulary: {len(vocabulary):,} words of 3 to 8 letters ({source})")
```

```text
vocabulary: 76,089 words of 3 to 8 letters (/usr/share/dict/words)
```

```python
import timeit

random.seed(4)
print(f"{'board':>6} | {'words listed':>12} | {'words found':>11} | {'trie search':>11} | {'one search per word':>19}")
for size, count in ((4, 5_000), (5, 20_000), (6, 50_000)):
    board = [random.choices(alphabet, weights, k=size) for _ in range(size)]
    words = random.sample(vocabulary, min(count, len(vocabulary)))
    with_trie = board_words_with_trie([row[:] for row in board], words)
    assert with_trie == board_words_naive([row[:] for row in board], words)
    trie_ms = min(timeit.repeat(lambda: board_words_with_trie([row[:] for row in board], words), number=1, repeat=2)) * 1000
    naive_ms = min(timeit.repeat(lambda: board_words_naive([row[:] for row in board], words), number=1, repeat=2)) * 1000
    print(f"{size}x{size:<4} | {len(words):>12,} | {len(with_trie):>11} | {trie_ms:8.1f} ms | {naive_ms:16.1f} ms")
```

Output:

```
 board | words listed | words found | trie search | one search per word
4x4    |        5,000 |           1 |      6.8 ms |             19.4 ms
5x5    |       20,000 |          18 |     29.7 ms |            112.6 ms
6x6    |       50,000 |          36 |     80.4 ms |            407.2 ms
```

The trie finds the same words several times faster, and the advantage grows with the dictionary: the naive method pays for every word, while the trie pays only for the board paths that spell prefixes of some word. For a single board, part of the trie's time is building the trie from the word list; when many boards are searched against the same dictionary the trie is built once and reused.

## ✅ Verification

Each solution was compared with a brute-force or regular-expression oracle on thousands of random cases over small alphabets (so that prefixes and wildcards collide often): sorting all matches for the ranked suggestions, taking the minimum over all matching roots, `re.fullmatch` for the wildcard patterns, a set-based prefix check for the buildable words, and the one-search-per-word method for random boards:

```python
import re

def suggest_brute(usage, prefix, k):
    matches = sorted((-count, word) for word, count in usage.items() if word.startswith(prefix))
    return [word for _, word in matches[:k]]

def replace_words_brute(sentence, roots):
    return " ".join(min((r for r in roots if word.startswith(r)), key=len, default=word) for word in sentence.split())

def longest_buildable_brute(words):
    stored, best = set(words), ""
    for word in words:
        if all(word[:i] in stored for i in range(1, len(word) + 1)) and (len(word) > len(best) or (len(word) == len(best) and word < best)):
            best = word
    return best

random.seed(1)
for _ in range(500):
    usage = {"".join(random.choice("abc") for _ in range(random.randint(1, 5))): random.randint(1, 5) for _ in range(random.randint(0, 25))}
    ranked = WordTrie()
    for word, count in usage.items():
        ranked.insert(word, count)
    for _ in range(10):
        prefix = "".join(random.choice("abc") for _ in range(random.randint(0, 3)))
        k = random.randint(1, 5)
        assert suggest(ranked, prefix, k) == suggest_brute(usage, prefix, k)

for _ in range(1_000):
    roots = ["".join(random.choice("ab") for _ in range(random.randint(1, 3))) for _ in range(random.randint(0, 5))]
    sentence = " ".join("".join(random.choice("abc") for _ in range(random.randint(1, 6))) for _ in range(random.randint(1, 6)))
    assert replace_words(sentence, roots) == replace_words_brute(sentence, roots)

for _ in range(500):
    stored = {"".join(random.choice("abc") for _ in range(random.randint(0, 5))) for _ in range(random.randint(0, 12))}
    dictionary = WildcardDictionary()
    for word in stored:
        dictionary.add(word)
    for _ in range(15):
        pattern = "".join(random.choice("abc.") for _ in range(random.randint(0, 5)))
        assert dictionary.search(pattern) == any(re.fullmatch(pattern, word) for word in stored)

for _ in range(2_000):
    words = ["".join(random.choice("ab") for _ in range(random.randint(1, 5))) for _ in range(random.randint(0, 12))]
    assert longest_buildable_word(words) == longest_buildable_brute(words)

for _ in range(100):
    n = random.randint(2, 4)
    board = [random.choices(alphabet, weights, k=n) for _ in range(n)]
    words = random.sample(vocabulary, 400)
    assert board_words_with_trie([row[:] for row in board], words) == board_words_naive([row[:] for row in board], words)
print("ranked suggestions, root replacement, wildcard search, buildable words and board search agree with their oracles")
```

```text
ranked suggestions, root replacement, wildcard search, buildable words and board search agree with their oracles
```

## 🧭 When to Reach for a Trie

A trie is the right structure when the problem has these features:

- **Many strings share beginnings**, and the question depends on prefixes (completions, shortest or longest matching prefix, counts per prefix).
- **You must prune**: searching a space of letter sequences (a board, a pattern) where most branches die early, and a trie tells you instantly which branches are dead.
- **Branching patterns** (wildcards, edit-distance-limited search) that a sorted list cannot express.
- **Words arrive and leave over time**, and queries must stay fast throughout.

If the questions are only "exact match" or "does anything start with `p`" on a fixed word list, a set or a sorted list with binary search is simpler and — in Python — usually faster.

## Common Mistakes

- **Searching with the full trie when the first mismatch should stop the walk.** Always stop as soon as a letter has no edge.
- **Not undoing state when backtracking** on a board: forgetting to restore a cell's letter after exploring from it corrupts later searches.
- **Collecting duplicates.** A word can be spelled by several paths on a board; use a set or mark the word as found.
- **Forgetting that wildcard search can explore many branches.** The worst case is bounded by the trie size, not by the pattern length.
- **Reusing a trie across tests after mutating it.** The board search above only mutates the *board* (and restores it), never the trie; a version that deletes found words from the trie must rebuild it.
- **Recursing along very long inputs.** The wildcard and board searches recurse once per pattern letter or word letter; for very long inputs convert them to iteration with an explicit stack.

## ➡️ Next

Continue to [tries-with-bits-and-dp.md](tries-with-bits-and-dp.md): the same structure works over *bits* instead of letters — finding the pair of numbers with the largest XOR and routing IP addresses by longest prefix — and, combined with dynamic programming, solves word-segmentation problems in less time than testing every substring.
