# ⚙️ Trie Operations

## Giving Every Prefix a Memory

In [trie-fundamentals.md](trie-fundamentals.md) a node stored only its children and a "word ends here" flag. Because **each node stands for exactly one prefix**, a node can also remember facts *about that prefix*. The most useful one is a counter: how many stored words pass through this node. With it, the trie answers "how many words start with `pre`?" in time proportional to the length of `pre`, supports **deletion** that keeps the structure clean, and drives **autocomplete** in alphabetical order with an early stop.

This file builds a `Trie` that behaves like a Python set of strings — `in`, `len`, iteration — and adds `discard`, `count_prefix`, `complete`, and a longest-common-prefix function. Every operation is checked against a plain `set` model on thousands of random operation sequences, and an invariant (the trie never contains a dead branch) is verified after every single step. All outputs were produced by running the code on CPython 3.9.

## 🧱 The Node and the Class

Each node gets a third field, `passing`: the number of stored words whose path goes through the node (a word that *ends* at the node counts, too). The root's `passing` is therefore the number of words in the trie. Here is the complete class; the sections that follow explain `count_prefix`, `discard`, and `complete` one at a time.

```python
class TrieNode:
    __slots__ = ("children", "is_word", "passing")

    def __init__(self):
        self.children = {}                  # next character -> child node
        self.is_word = False                # does a stored word end here?
        self.passing = 0                    # how many stored words go through this node

class Trie:
    def __init__(self, words=()):
        self.root = TrieNode()
        self.size = 0
        for word in words:
            self.add(word)

    def __len__(self):
        return self.size

    def _walk(self, text):
        """The node reached by following text from the root, or None."""
        node = self.root
        for ch in text:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def __contains__(self, word):
        node = self._walk(word)
        return node is not None and node.is_word

    def add(self, word):
        """Insert word; return True if it was new."""
        if word in self:
            return False                     # counters must change only for words that were not already stored
        node = self.root
        node.passing += 1
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
            node.passing += 1
        node.is_word = True
        self.size += 1
        return True

    def discard(self, word):
        """Remove word if present; return True if something was removed."""
        if word not in self:
            return False
        node = self.root
        node.passing -= 1
        trail = []                                       # (parent, character) pairs along the path
        for ch in word:
            trail.append((node, ch))
            node = node.children[ch]
            node.passing -= 1
        node.is_word = False
        self.size -= 1
        for parent, ch in reversed(trail):               # prune from the bottom up
            if parent.children[ch].passing == 0:
                del parent.children[ch]                  # nothing passes through this node any more
            else:
                break                                    # it still serves other words, and so do all its ancestors
        return True

    def count_prefix(self, prefix):
        """How many stored words start with prefix: one walk, no scanning."""
        node = self._walk(prefix)
        return 0 if node is None else node.passing

    def _complete(self, prefix, limit=None):
        """Return (the first `limit` words starting with prefix in alphabetical order, nodes visited)."""
        node = self._walk(prefix)
        if node is None or limit == 0:
            return [], 0
        found, visited = [], 0
        stack = [(node, prefix)]
        while stack:
            current, text = stack.pop()
            visited += 1
            if current.is_word:
                found.append(text)
                if limit is not None and len(found) == limit:
                    break
            for ch in sorted(current.children, reverse=True):      # push in reverse so the smallest letter is popped first
                stack.append((current.children[ch], text + ch))
        return found, visited

    def complete(self, prefix, limit=None):
        return self._complete(prefix, limit)[0]

    def __iter__(self):
        return iter(self.complete(""))

    def node_count(self):
        count, stack = 0, [self.root]
        while stack:
            current = stack.pop()
            count += 1
            stack.extend(current.children.values())
        return count

trie = Trie(["tea", "ten", "to", "in", "inn", "team"])
print(len(trie), trie.node_count(), list(trie))
```

```text
6 10 ['in', 'inn', 'tea', 'team', 'ten', 'to']
```

The `if word in self` check at the top of `add` matters: inserting a word twice must not count it twice. The six words use ten nodes: the root plus the nine distinct prefixes `i`, `in`, `inn`, `t`, `te`, `tea`, `team`, `ten`, and `to`.

## 🔢 Counting Words by Prefix

Because `passing` is kept up to date by `add` and `discard`, `count_prefix` is just a walk to the prefix's node and a read of one number — O(L), without touching any of the words:

```python
print(trie.count_prefix("te"), trie.count_prefix("t"), trie.count_prefix("i"), trie.count_prefix("x"), trie.count_prefix(""))        # 3 4 2 0 6
```

`te` is shared by `tea`, `team`, and `ten`; `t` additionally by `to`; the empty prefix is shared by all six words; and nothing starts with `x`.

## ➖ Deletion

Deleting a word has two parts. First, **unmark** it: clear the flag at the end node, and decrement `passing` on every node along the path. Second, **prune**: any node whose `passing` has fallen to zero no longer leads to any word, so it should be removed — and removing it can leave its parent with nothing beneath it, so the pruning continues upward until it reaches a node that still serves other words. This is what the loop at the end of `discard` does.

Deleting `to` from the trie above removes the `to` node, but `t` stays because `tea`, `team`, and `ten` still pass through it. Deleting `team` afterwards removes only the `team` node: `tea` is a word in its own right, so the node `tea` stays.

```python
print(trie.discard("to"), trie.discard("to"), trie.node_count(), trie.count_prefix("t"))        # True False 9 3
print(trie.discard("team"), trie.node_count(), trie.complete("te"))                             # True 8 ['tea', 'ten']
```

The second call to `discard("to")` returns `False` — the word is already gone — and the node counts confirm the pruning: 10 nodes, then 9 after `to`, then 8 after `team`.

Without the pruning step, a deleted word would still be reported correctly (`is_word` is cleared), but its nodes would linger forever: the trie would leak memory, and a prefix check such as "does anything start with `to`?" would wrongly answer yes. The counter makes the prune test a single comparison.

## 🔍 Autocomplete: Completions in Alphabetical Order

To list the words that start with a prefix, walk to the prefix's node and then traverse the **subtree below it**. Visiting children in alphabetical order yields the words in alphabetical order — a depth-first, pre-order traversal of a trie *is* a lexicographic sort of its words ([Wikipedia: Trie](https://en.wikipedia.org/wiki/Trie)). Two properties make this practical:

- The traversal can **stop early**: for an autocomplete box that shows five suggestions, there is no need to visit the other 3,000 matches.
- The cost is the length of the prefix plus the number of nodes *visited*, not the size of the whole dictionary.

`_complete` uses an explicit stack instead of recursion, so words of any length are safe, and it reports how many nodes it visited so that the early stop can be seen.

```python
print(trie.complete("t"), trie.complete("t", limit=1), trie.complete("zzz"), trie.complete("t", limit=0))        # ['tea', 'ten'] ['tea'] [] []
```

## 🧪 How Early Termination Pays Off

The cost of `complete` is the number of nodes it *visits*. On a vocabulary of over 200,000 words, asking for the first five completions of the empty prefix, or of `pre`, visits a few dozen nodes — a tiny fraction of the trie — while listing all 3,018 words that begin with `pre` visits over ten thousand:

```python
import random

def load_vocabulary():
    for path in ("/usr/share/dict/words", "/usr/dict/words"):
        try:
            with open(path, encoding="utf-8", errors="ignore") as handle:
                words = {w.strip() for w in handle}
        except OSError:
            continue
        return sorted(w for w in words if w.isalpha() and w.islower() and w.isascii()), path
    rng = random.Random(1)
    syllables = ["ba", "ke", "li", "mo", "nu", "ra", "so", "ti", "ve", "wa", "zi", "the", "ing", "tion", "pre", "con", "un", "re"]
    return sorted({"".join(rng.choice(syllables) for _ in range(rng.randint(2, 5))) for _ in range(60_000)}), "synthetic syllable words"

vocabulary, source = load_vocabulary()
big = Trie(vocabulary)
print(f"{len(big):,} words, {big.node_count():,} nodes ({source})")
print(f"{'prefix':>8} | {'limit':>5} | {'words returned':>14} | {'nodes visited':>13}")
for prefix, limit in (("", 5), ("pre", 5), ("pre", None), ("zy", 3), ("qz", 3)):
    found, visited = big._complete(prefix, limit)
    print(f"{prefix!r:>8} | {str(limit):>5} | {len(found):>14,} | {visited:>13,}")
print(big.complete("", 5))
```

```text
210,773 words, 696,835 nodes (/usr/share/dict/words)
  prefix | limit | words returned | nodes visited
      '' |     5 |              5 |             7
   'pre' |     5 |              5 |            27
   'pre' |  None |          3,018 |        10,858
    'zy' |     3 |              3 |            13
    'qz' |     3 |              0 |             0
['a', 'aa', 'aal', 'aalii', 'aam']
```

This is the key property of the structure: a handful of suggestions cost a handful of node visits, however large the dictionary. A sorted list can produce the same slice quickly (see [trie-fundamentals.md](trie-fundamentals.md) for the comparison); the trie's advantage is that the dictionary can change between keystrokes and each node can carry extra data, as the next file shows.

## 🔗 Longest Common Prefix

*What is the longest string that starts every word in a list?* Build a trie of the words and walk down from the root as long as the current node has **exactly one child** and **is not itself the end of a word** — a branch point, or a word ending, is where the words stop agreeing:

```python
import os

def longest_common_prefix(words):
    trie = Trie(words)
    node, letters = trie.root, []
    while len(node.children) == 1 and not node.is_word:
        (ch, node), = node.children.items()              # the only child
        letters.append(ch)
    return "".join(letters)

print(longest_common_prefix(["flower", "flow", "flight"]), repr(longest_common_prefix(["dog", "racecar"])), longest_common_prefix(["interview", "internet", "interval"]), longest_common_prefix(["alone"]))   # fl '' inter alone
print(os.path.commonprefix(["flower", "flow", "flight"]))                                                                                                                                                       # fl
```

The standard library has this function for strings, `os.path.commonprefix`, which compares characters directly in O(total length) without a trie — for this single question it is the simpler tool (and the trie version is shown because the trie gives the same answer for free once it exists). Note that `os.path.commonprefix` works character by character, not path component by path component, despite living in `os.path`.

## ⏱️ Costs at a Glance

| Operation | Time | Notes |
|-----------|------|-------|
| `add(word)`, `word in trie`, `discard(word)` | O(L) | `L` = length of the word; independent of the number of words |
| `count_prefix(prefix)` | O(L) | Reads one counter |
| `complete(prefix, limit)` | O(L + nodes visited) | Plus a sort of each visited node's children (at most the alphabet size) |
| Iterate all words | O(number of nodes) | Alphabetical, because children are visited in order |
| Space | O(total nodes) | At most one node per character of every word, usually far fewer |

## ✅ Verification

The `Trie` was checked against a plain Python `set` on 400 random sequences of 60 operations each — adds, deletes, membership tests, prefix counts, and completions with and without limits. After **every** operation, the test also checks that the length matches, that iteration yields exactly the sorted words, that the root counter equals the size, and that the number of nodes equals the number of distinct prefixes plus one (the root) — which proves that no dead branches survive deletion:

```python
def prefixes_of(words):
    return {w[:i] for w in words for i in range(1, len(w) + 1)}

random.seed(1)
for _ in range(400):
    trie, model = Trie(), set()
    for _ in range(60):
        operation = random.choice(("add", "add", "discard", "check"))
        word = "".join(random.choice("abc") for _ in range(random.randint(0, 5)))
        if operation == "add":
            assert trie.add(word) == (word not in model)
            model.add(word)
        elif operation == "discard":
            assert trie.discard(word) == (word in model)
            model.discard(word)
        else:
            assert (word in trie) == (word in model)
            assert trie.count_prefix(word) == sum(1 for stored in model if stored.startswith(word))
            limit = random.choice((None, 0, 1, 3))
            expected = sorted(stored for stored in model if stored.startswith(word))
            assert trie.complete(word, limit) == (expected if limit is None else expected[:limit])
        assert len(trie) == len(model) == trie.root.passing
        assert list(trie) == sorted(model)
        assert trie.node_count() == len(prefixes_of(model)) + 1

for _ in range(2_000):
    words = ["".join(random.choice("ab") for _ in range(random.randint(0, 6))) for _ in range(random.randint(0, 6))]
    assert longest_common_prefix(words) == os.path.commonprefix(words)
print("add, discard, count_prefix, complete, iteration and longest_common_prefix agree with a set model; no dead branches ever remained")
```

```text
add, discard, count_prefix, complete, iteration and longest_common_prefix agree with a set model; no dead branches ever remained
```

The vocabulary check closes the loop on a real data set: delete every word beginning with `pre` and the node count must drop by exactly the number of nodes in that subtree.

```python
subtree_nodes = big._complete("pre", None)[1]
before = big.node_count()
for word in [w for w in vocabulary if w.startswith("pre")]:
    big.discard(word)
print(f"nodes before: {before:,}   after deleting every 'pre' word: {big.node_count():,}   removed: {before - big.node_count():,}   (subtree had {subtree_nodes:,})")
print(f"count_prefix('pre') is now {big.count_prefix('pre')}, and 'pr' still has {big.count_prefix('pr'):,} words")
```

```text
nodes before: 696,835   after deleting every 'pre' word: 685,977   removed: 10,858   (subtree had 10,858)
count_prefix('pre') is now 0, and 'pr' still has 2,926 words
```

## Common Mistakes

- **Counting a word twice.** Inserting a duplicate must not change the counters; `add` checks membership first.
- **Deleting by only clearing the flag.** The word disappears from `in`, but its branch stays, `count_prefix` can mislead, and memory is never returned. Decrement the counters and prune.
- **Pruning too far.** Stop at the first ancestor that still has words passing through it (or that is itself a word end — its counter covers that case because words that end there are counted in `passing`).
- **Recursing along the length of a word.** A deep recursion fails for very long keys; iterate with an explicit loop or stack.
- **Returning completions in arbitrary order.** Dictionary iteration order is insertion order; sort the children (or keep them sorted) if alphabetical order matters.
- **Rebuilding the trie to remove words.** Deletion is O(L); there is no need to rebuild.

## ➡️ Next

Continue to [prefix-problems.md](prefix-problems.md): ranking completions by popularity, replacing words with their shortest roots, searching with wildcards, and finding every dictionary word on a letter board — the problems where a trie's ability to branch and prune beats a sorted list.
