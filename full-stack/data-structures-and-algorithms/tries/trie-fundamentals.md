# 🌲 Trie Fundamentals

## A Tree Where Every Edge Is a Letter

A **trie** (also called a *prefix tree* or *digital tree*) stores a set of strings in a tree whose edges are labelled with characters. The root represents the empty string, each node represents the prefix spelled by the path from the root to it, and a flag on a node says "a stored word ends here". Words that start the same way **share a path**, so the question "does any word start with `pre`?" becomes "can I walk `p`, `r`, `e` from the root?" — and the answer takes time proportional to the **length of the query**, no matter how many words are stored.

The name comes from the middle syllable of *retrieval*: Edward Fredkin coined it in 1960, describing an idea that René de la Briandais had published in a computing context a year earlier and that Axel Thue had described abstractly in 1912 ([Wikipedia: Trie](https://en.wikipedia.org/wiki/Trie)). Tries are the standard structure behind autocomplete and spell checking and, in a bitwise form, IP routing; they are also the natural way to ask questions about *prefixes* of strings or of numbers. This file builds one, shows what it costs in operations and in memory, and measures it honestly against the alternatives (a set, and a sorted list searched with [binary search](../searching-algorithms/binary-search.md)) — the trie does not win everywhere, and knowing where it does matters more than the code. All outputs were produced by running the code on CPython 3.9.

## 🧱 The Structure

Take the words `tea`, `ten`, `to`, `in`, `inn`. The trie has one node for the empty prefix, one for each distinct prefix, and a flag (here `*`) on the nodes where a word ends:

```
(root)
├── t
│   ├── e
│   │   ├── a *       "tea"
│   │   └── n *       "ten"
│   └── o *           "to"
└── i
    └── n *           "in"
        └── n *       "inn"
```

The path `t → e` exists but has no flag, so `te` is a *prefix* of stored words without being a word itself. That distinction — "is it a path?" versus "is it a word?" — is the heart of the structure. Each node needs two things: a mapping from the next character to a child node, and the word-end flag.

```python
class TrieNode:
    __slots__ = ("children", "is_word")

    def __init__(self):
        self.children = {}                 # next character -> child node
        self.is_word = False               # does a stored word end at this node?

class Trie:
    def __init__(self, words=()):
        self.root = TrieNode()
        for word in words:
            self.insert(word)

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())      # follow the edge, creating the node if it is missing
        node.is_word = True

    def _walk(self, text):
        """The node reached by following text from the root, or None if the path does not exist."""
        node = self.root
        for ch in text:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_word

    def starts_with(self, prefix):
        return self._walk(prefix) is not None

def show(trie):
    """Print the trie as an indented tree; * marks nodes where a word ends."""
    def visit(node, label, depth):
        print("    " * depth + label + (" *" if node.is_word else ""))
        for ch in sorted(node.children):
            visit(node.children[ch], ch, depth + 1)
    visit(trie.root, "(root)", 0)

trie = Trie(["tea", "ten", "to", "in", "inn"])
show(trie)
print(trie.search("tea"), trie.search("te"), trie.starts_with("te"), trie.search("tex"), trie.starts_with("x"))       # True False True False False
```

```text
(root)
    i
        n *
            n *
    t
        e
            a *
            n *
        o *
True False True False False
```

All three operations — `insert`, `search`, and `starts_with` — walk at most one node per character of the argument. Their cost is O(L) for a word of length `L`, **independent of how many words the trie holds**. A hash set also answers `search` in O(L) (hashing the word reads every character), but it cannot answer `starts_with` at all without scanning, and it has no notion of a "next letter".

(`__slots__` on the node class saves memory by replacing each node's per-instance dictionary with fixed fields; with hundreds of thousands of nodes it matters.)

### Why the Flag Is Essential

Without `is_word`, a trie cannot tell a stored word from a mere prefix of one. After inserting only `inn`, the path for `in` exists, but `search("in")` must be false:

```python
only_inn = Trie(["inn"])
print(only_inn.search("in"), only_inn.starts_with("in"), only_inn.search("inn"))        # False True True
only_inn.insert("in")
print(only_inn.search("in"))                                                            # True
```

## 📏 How Much Does Prefix Sharing Save?

The whole point of sharing paths is that common beginnings are stored once. For a real vocabulary the saving is large. The block below builds a trie of the lowercase ASCII words in the system dictionary (`/usr/share/dict/words` on macOS and many Linux systems; if it is missing, the code falls back to a deterministic synthetic vocabulary, so the numbers in your run will differ) and compares the number of nodes with the total number of characters in the words:

```python
import random

def load_vocabulary():
    for path in ("/usr/share/dict/words", "/usr/dict/words"):
        try:
            with open(path, encoding="utf-8", errors="ignore") as handle:
                words = {w.strip() for w in handle}
        except OSError:
            continue
        words = sorted(w for w in words if w.isalpha() and w.islower() and w.isascii())
        return words, path
    rng = random.Random(1)                                          # fallback: pseudo-words built from syllables
    syllables = ["ba", "ke", "li", "mo", "nu", "ra", "so", "ti", "ve", "wa", "zi", "the", "ing", "tion", "pre", "con", "un", "re"]
    words = {"".join(rng.choice(syllables) for _ in range(rng.randint(2, 5))) for _ in range(60_000)}
    return sorted(words), "synthetic syllable words"

def count_nodes(trie):
    total, stack = 0, [trie.root]
    while stack:
        node = stack.pop()
        total += 1
        stack.extend(node.children.values())
    return total

vocabulary, source = load_vocabulary()
vocab_trie = Trie(vocabulary)
characters = sum(len(w) for w in vocabulary)
nodes = count_nodes(vocab_trie)
print(f"vocabulary: {len(vocabulary):,} words from {source}")
print(f"total characters: {characters:,}   trie nodes: {nodes:,}   nodes per character: {nodes / characters:.2f}")
```

```text
vocabulary: 210,773 words from /usr/share/dict/words
total characters: 2,039,158   trie nodes: 696,835   nodes per character: 0.34
```

Storing every word separately would take one slot per character; with this vocabulary the trie needs about one node for every three characters, because shared beginnings such as `pre-` and `un-` and every common stem are stored once. (The saving is concentrated near the root: the first few letters of English words repeat constantly, while the tails of words are mostly unique.)

## 🧠 The Catch: Memory in Python

Fewer nodes does not mean less memory. Each trie node is an object plus a dictionary, which together cost hundreds of bytes in Python, while a stored string costs about 50 bytes plus one per character. Measuring with `tracemalloc` on 50,000 words:

```python
import sys
import tracemalloc

random.seed(2)
sample = random.sample(vocabulary, 50_000)

class ArrayTrieNode:
    __slots__ = ("children", "is_word")

    def __init__(self):
        self.children = [None] * 26            # one slot per letter a-z: fast indexing, but mostly empty
        self.is_word = False

def build_array_trie(words):
    root = ArrayTrieNode()
    for word in words:
        node = root
        for ch in word:
            slot = ord(ch) - 97
            if node.children[slot] is None:
                node.children[slot] = ArrayTrieNode()
            node = node.children[slot]
        node.is_word = True
    return root

def traced(build):
    tracemalloc.start()
    before = tracemalloc.get_traced_memory()[0]
    result = build()
    used = tracemalloc.get_traced_memory()[0] - before
    tracemalloc.stop()
    return result, used

_, dict_trie_bytes = traced(lambda: Trie(sample))
_, array_trie_bytes = traced(lambda: build_array_trie(sample))
_, set_bytes = traced(lambda: set(sample))                     # the table only: the string objects already exist
string_bytes = sum(sys.getsizeof(w) for w in sample)
print(f"trie with dictionary children: {dict_trie_bytes / 1e6:7.1f} MB")
print(f"trie with 26-slot lists:       {array_trie_bytes / 1e6:7.1f} MB")
print(f"set of the words:              {(set_bytes + string_bytes) / 1e6:7.1f} MB   (table {set_bytes / 1e6:.1f} MB + strings {string_bytes / 1e6:.1f} MB)")
```

```text
trie with dictionary children:    56.1 MB
trie with 26-slot lists:          70.7 MB
set of the words:                  5.0 MB   (table 2.1 MB + strings 2.9 MB)
```

In Python, a trie of these words occupies more than ten times the memory of a plain set, and the array-of-26 variant is larger still, because most of its 26 slots are empty. The remedies that appear in practice are **compressed tries** (also called radix trees), which merge chains of single-child nodes ([Wikipedia: Radix tree](https://en.wikipedia.org/wiki/Radix_tree)), packed or array-based layouts in lower-level languages, and simply not using a trie when a sorted list will do. That last option deserves a fair test.

## ⏱️ Where a Trie Wins, and Where It Does Not

For a **fixed** set of words, a sorted list with `bisect` answers prefix questions well: all words starting with `p` are a contiguous slice, found by two binary searches (`bisect_left(p)` and `bisect_left(p + "￿")`). A linear scan with `str.startswith` is the naive baseline. Here are the three, answering "does any word start with this prefix?" and "list all words with this prefix", for a few prefixes:

```python
import bisect
import timeit

def prefix_exists_bisect(prefix):
    i = bisect.bisect_left(vocabulary, prefix)
    return i < len(vocabulary) and vocabulary[i].startswith(prefix)

def words_with_prefix_bisect(prefix):
    low = bisect.bisect_left(vocabulary, prefix)
    high = bisect.bisect_left(vocabulary, prefix + "￿")
    return vocabulary[low:high]

def words_with_prefix_trie(trie, prefix):
    node = trie._walk(prefix)
    found = []
    if node is None:
        return found
    def visit(current, letters):
        if current.is_word:
            found.append("".join(letters))
        for ch in sorted(current.children):
            letters.append(ch)
            visit(current.children[ch], letters)
            letters.pop()
    visit(node, list(prefix))
    return found

def microseconds(function, number):
    return min(timeit.repeat(function, number=number, repeat=3)) / number * 1e6

print(f"{'prefix':>16} | {'exists? trie':>12} | {'bisect':>9} | {'linear scan':>12}")
for prefix in ("pre", "intern", "xyl", "qz", "unconstitution"):
    assert vocab_trie.starts_with(prefix) == prefix_exists_bisect(prefix) == any(w.startswith(prefix) for w in vocabulary)
    scan = microseconds(lambda: any(w.startswith(prefix) for w in vocabulary), 3)
    print(f"{prefix:>16} | {microseconds(lambda: vocab_trie.starts_with(prefix), 2000):9.2f} us | {microseconds(lambda: prefix_exists_bisect(prefix), 2000):6.2f} us | {scan:9.0f} us")

print()
print(f"{'prefix':>16} | {'matches':>7} | {'list: trie':>11} | {'bisect':>10} | {'linear scan':>11}")
for prefix in ("pre", "intern", "xyl"):
    expected = [w for w in vocabulary if w.startswith(prefix)]
    assert words_with_prefix_trie(vocab_trie, prefix) == words_with_prefix_bisect(prefix) == expected
    print(f"{prefix:>16} | {len(expected):>7,} | {microseconds(lambda: words_with_prefix_trie(vocab_trie, prefix), 20) / 1000:8.3f} ms | "
          f"{microseconds(lambda: words_with_prefix_bisect(prefix), 200) / 1000:7.4f} ms | {microseconds(lambda: [w for w in vocabulary if w.startswith(prefix)], 3) / 1000:8.1f} ms")
```

Output:

```
          prefix | exists? trie |    bisect |  linear scan
             pre |      0.27 us |   0.45 us |      8321 us
          intern |      0.41 us |   0.43 us |      5330 us
             xyl |      0.27 us |   0.45 us |     12891 us
              qz |      0.22 us |   0.42 us |     12994 us
  unconstitution |      0.76 us |   0.41 us |     11695 us

          prefix | matches |  list: trie |     bisect | linear scan
             pre |   3,018 |    2.801 ms |  0.0047 ms |     12.1 ms
          intern |      46 |    0.035 ms |  0.0007 ms |     12.0 ms
             xyl |      66 |    0.052 ms |  0.0007 ms |     11.8 ms
```

The picture is nuanced:

- **Existence checks.** The trie costs about as much as a binary search (a fraction of a microsecond), and its cost grows with the *length of the query*, not with the vocabulary size. Both are thousands of times faster than scanning.
- **Listing the matches.** For a static vocabulary, the sorted list wins by a wide margin in Python: slicing a contiguous range is one C-level copy, while the trie visits each match in a Python-level traversal. A trie is not a speed-up for this task.

So why use a trie at all? Because the sorted list is only fast while the data is **fixed**. Inserting into a sorted list shifts every later element — O(n) per insert, O(n²) to build by insertion — while a trie insertion costs O(L) regardless of size:

```python
random.seed(3)
print(f"{'words inserted':>14} | {'sorted list + insort':>20} | {'trie':>9}")
for n in (25_000, 50_000, 100_000, 200_000):
    batch = random.sample(vocabulary, n)
    def build_with_insort():
        ordered = []
        for w in batch:
            bisect.insort(ordered, w)
        return ordered
    def build_trie():
        return Trie(batch)
    insort_ms = min(timeit.repeat(build_with_insort, number=1, repeat=2)) * 1000
    trie_ms = min(timeit.repeat(build_trie, number=1, repeat=2)) * 1000
    print(f"{n:>14,} | {insort_ms:17.0f} ms | {trie_ms:6.0f} ms")
```

Output:

```
words inserted | sorted list + insort |      trie
        25,000 |                46 ms |     48 ms
        50,000 |               172 ms |    100 ms
       100,000 |               662 ms |    205 ms
       200,000 |              2590 ms |    416 ms
```

The two start level and then diverge: each doubling of the input roughly quadruples the sorted list's time (quadratic) while the trie's time merely doubles (linear), so at 200,000 words the trie is about six times faster. When words arrive continuously, the trie's cost per word stays constant.

The honest summary is that a trie earns its place in three situations:

1. **The set changes constantly** and you still need prefix queries (autocomplete over a live dictionary).
2. **You need something per prefix**, not just the words: counts, best completions, a flag, a route. Each node *is* a prefix and can carry data ([trie-operations.md](trie-operations.md)).
3. **The question is a pattern, not a plain prefix**: wildcards, spelling variations, word searches on a board, longest-prefix matches, bitwise comparisons ([prefix-problems.md](prefix-problems.md) and [tries-with-bits-and-dp.md](tries-with-bits-and-dp.md)). A sorted list cannot branch.

## ✅ Verification

The trie was compared with a Python `set` on thousands of random operation sequences (alphabet `a`–`c`, so that prefixes overlap heavily): after each insertion, `search` and `starts_with` must agree with a plain set and a scan, including for the empty string, and the number of nodes must equal the number of distinct prefixes plus the root:

```python
def prefixes_of(words):
    return {w[:i] for w in words for i in range(1, len(w) + 1)}

random.seed(1)
for _ in range(400):
    trie = Trie()
    stored = set()
    for _ in range(40):
        word = "".join(random.choice("abc") for _ in range(random.randint(0, 5)))
        trie.insert(word)
        stored.add(word)
        probe = "".join(random.choice("abc") for _ in range(random.randint(0, 5)))
        assert trie.search(probe) == (probe in stored)
        assert trie.starts_with(probe) == (probe == "" or any(w.startswith(probe) for w in stored))      # the empty prefix always exists
        assert count_nodes(trie) == len(prefixes_of(stored)) + 1
print("search, starts_with and the node count agree with a set model on 400 random insertion sequences")
```

```text
search, starts_with and the node count agree with a set model on 400 random insertion sequences
```

## Common Mistakes

- **Forgetting the end-of-word flag**, so that every prefix of a stored word is reported as a word.
- **Treating `starts_with("")` carelessly.** The empty prefix is "walked" trivially from the root, so it is true even when the trie is empty; decide what your application means by it.
- **Using recursion for insertion or search.** A word of 10,000 characters exceeds Python's recursion limit; the loops above have no such limit.
- **Ignoring case and Unicode.** A trie is exact: `"Apple"` and `"apple"` are different paths. Normalize (`str.casefold`) before inserting and searching.
- **Choosing a 26-slot array by default.** It makes indexing fast but wastes memory when nodes have few children; a dictionary adapts to any alphabet.
- **Reaching for a trie when a sorted list and `bisect` would do.** For a static word list, binary search on a sorted list is simpler, smaller, and faster in Python.

## ➡️ Next

Continue to [trie-operations.md](trie-operations.md): deleting words without leaving dead branches, counting words that share a prefix, listing completions in alphabetical order, and finding the longest common prefix — each by storing a little extra information in the nodes.
