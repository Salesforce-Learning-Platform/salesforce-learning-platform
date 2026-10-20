# 🧬 Tries with Bits and Dynamic Programming

## The Same Tree, Different Edges

A trie's edges do not have to be letters. Any sequence of symbols works, and one choice turns out to be extraordinarily useful: the **bits** of a fixed-width number. A trie over bits — a **binary trie** or *bitwise trie* — has exactly two edges per node, `0` and `1`, and a path from the root spells out a number's binary representation from the most significant bit down ([Wikipedia: Trie](https://en.wikipedia.org/wiki/Trie) lists the bitwise trie as a notable variant). Because the *most significant* bits come first, a path that agrees with another number for longer is a number that is "closer" in the sense of the high bits — which is precisely what XOR and network prefixes care about.

This file puts the trie to work in two unexpected combinations. First with [bit manipulation](../bit-manipulation/README.md): finding the pair of numbers with the **largest XOR**, the **subarray with the largest XOR**, and **longest-prefix matching** for IP routing. Then with [dynamic programming](../dynamic-programming/README.md): segmenting a string into dictionary words, counting the segmentations, and counting the distinct substrings of a string. Every algorithm is cross-checked against a brute-force definition on thousands of random inputs, and the benchmarks include the places where the trie does *not* win. All outputs were produced by running the code on CPython 3.9.

## 🔟 A Binary Trie for Numbers

To store non-negative integers below `2³¹`, give every number a path of 31 edges, one per bit from bit 30 down to bit 0. Two numbers that share their top `k` bits share the first `k` nodes of their paths. Nodes are numbered, and each stores the indexes of its two children (or `-1`):

```python
class BinaryTrie:
    def __init__(self, bits=31):
        self.bits = bits                                  # numbers are below 2 ** bits
        self.child = [[-1, -1]]                           # node 0 is the root; child[node][bit] is a node index or -1

    def insert(self, number):
        node = 0
        for i in range(self.bits - 1, -1, -1):            # from the most significant bit down
            bit = (number >> i) & 1
            if self.child[node][bit] == -1:
                self.child.append([-1, -1])
                self.child[node][bit] = len(self.child) - 1
            node = self.child[node][bit]

    def max_xor_with(self, number):
        """The largest number ^ stored over all stored numbers (the trie must not be empty)."""
        node, result = 0, 0
        for i in range(self.bits - 1, -1, -1):
            bit = (number >> i) & 1
            opposite = bit ^ 1
            if self.child[node][opposite] != -1:
                result |= 1 << i                          # a stored number differs here: this bit of the XOR is 1
                node = self.child[node][opposite]
            else:
                node = self.child[node][bit]
        return result
```

### The Pair With the Largest XOR

*Given a list of numbers, find the largest value of `a ^ b` over all pairs.* The brute-force method tries all `n(n − 1)/2` pairs. The trie method asks, for each number `x`, "which stored number gives the largest XOR with `x`?" — and answers greedily from the top bit: **at each level, take the child whose bit is the opposite of `x`'s bit if it exists**. This is optimal because a `1` at a higher bit is worth more than every lower bit combined (`2ᵏ > 2ᵏ⁻¹ + … + 1`), so it is never worth giving up a high 1 for lower ones. Each lookup takes 31 steps, so the whole task costs O(n · 31) instead of O(n²).

```python
import itertools
import random

def max_xor_pair(nums):
    trie = BinaryTrie()
    best = 0
    for index, x in enumerate(nums):
        if index:
            best = max(best, trie.max_xor_with(x))        # compare x with everything stored so far
        trie.insert(x)
    return best

def max_xor_pair_brute(nums):
    return max((a ^ b for a, b in itertools.combinations(nums, 2)), default=0)

print(max_xor_pair([3, 10, 5, 25, 2, 8]), max_xor_pair([14, 70, 53, 83, 49, 91, 36, 80, 92, 51, 66, 70]))       # 28 127
```

The first list's best pair is `5 ^ 25 = 28`: `00101` against `11001` differ in the top bit and in two more. The two lists were solved with the binary trie; the next block times it against the pair-by-pair method on random 31-bit numbers:

```python
import timeit

random.seed(2)
print(f"{'n':>6} | {'binary trie':>11} | {'all pairs':>10}")
for n in (500, 1_000, 2_000, 4_000):
    numbers = [random.randint(0, 2**31 - 1) for _ in range(n)]
    assert max_xor_pair(numbers) == max_xor_pair_brute(numbers)
    trie_ms = min(timeit.repeat(lambda: max_xor_pair(numbers), number=1, repeat=3)) * 1000
    brute_ms = min(timeit.repeat(lambda: max_xor_pair_brute(numbers), number=1, repeat=2)) * 1000
    print(f"{n:>6,} | {trie_ms:8.1f} ms | {brute_ms:7.1f} ms")
```

Output:

```
     n | binary trie |  all pairs
   500 |      6.5 ms |     5.6 ms
 1,000 |     12.5 ms |    23.4 ms
 2,000 |     25.3 ms |    90.3 ms
 4,000 |     51.0 ms |   360.0 ms
```

Doubling `n` doubles the trie's time and quadruples the brute-force time. With only 500 numbers, the all-pairs method is about as fast; the break-even is a few hundred numbers, and past that the trie pulls rapidly ahead.

### The Subarray With the Largest XOR

*Find the contiguous run of a list whose XOR is as large as possible.* The [prefix XOR](../bit-manipulation/xor-tricks.md) trick turns "the XOR of `nums[i..j]`" into `prefix[j + 1] ^ prefix[i]`. So the best subarray ending at `j` is the best earlier prefix to pair with `prefix[j + 1]` — exactly the max-XOR query. Insert each prefix as you go (starting with the empty prefix `0`):

```python
def max_xor_subarray(nums):
    trie = BinaryTrie()
    trie.insert(0)                                        # the empty prefix
    prefix, best = 0, 0
    for x in nums:
        prefix ^= x
        best = max(best, trie.max_xor_with(prefix))      # the best earlier prefix to cancel against
        trie.insert(prefix)
    return best

def max_xor_subarray_brute(nums):
    best = 0
    for start in range(len(nums)):
        running = 0
        for end in range(start, len(nums)):
            running ^= nums[end]
            best = max(best, running)
    return best

print(max_xor_subarray([8, 1, 2, 12, 7, 6]))              # 15
```

The best run in the example is `[1, 2, 12]` (`1 ^ 2 ^ 12 = 15`), found in O(n · 31) instead of O(n²).

## 🌐 IP Routing: Longest-Prefix Match

A router holds a table of networks, each written as an address prefix such as `10.1.0.0/16` ("the first 16 bits"), with a *next hop* for each. An incoming address may match several entries — `10.1.9.9` lies inside both `10.0.0.0/8` and `10.1.0.0/16` — and the router must pick the **most specific** one, the entry with the longest matching prefix ([Wikipedia: Longest prefix match](https://en.wikipedia.org/wiki/Longest_prefix_match)). A table usually also holds a *default route* (`0.0.0.0/0`, the shortest possible prefix) as a fallback.

A binary trie over the 32 bits of an address is the natural structure. Inserting a route follows its first `length` bits and stores the next hop at the node reached. To look up an address, walk its bits from the top, **remember the deepest route seen on the way**, and stop when the path ends. At most 32 steps, regardless of the number of routes:

```python
import ipaddress

class RouteTable:
    def __init__(self):
        self.child = [[-1, -1]]
        self.route = [None]                               # route[node] = (network, next hop) if a route ends at this node

    def add(self, cidr, next_hop):
        network = ipaddress.ip_network(cidr)
        value, length = int(network.network_address), network.prefixlen
        node = 0
        for i in range(31, 31 - length, -1):              # only the first `length` bits of the address matter
            bit = (value >> i) & 1
            if self.child[node][bit] == -1:
                self.child.append([-1, -1])
                self.route.append(None)
                self.child[node][bit] = len(self.child) - 1
            node = self.child[node][bit]
        self.route[node] = (cidr, next_hop)

    def lookup(self, address):
        value = int(ipaddress.ip_address(address))
        node, best = 0, self.route[0]                     # the default route, if there is one
        for i in range(31, -1, -1):
            node = self.child[node][(value >> i) & 1]
            if node == -1:
                break
            if self.route[node] is not None:
                best = self.route[node]                   # a more specific route than any seen so far
        return best

table = RouteTable()
for cidr, hop in (("0.0.0.0/0", "default"), ("10.0.0.0/8", "A"), ("10.1.0.0/16", "B"), ("10.1.2.0/24", "C"), ("192.168.0.0/16", "D")):
    table.add(cidr, hop)
for address in ("10.9.9.9", "10.1.9.9", "10.1.2.200", "192.168.5.5", "8.8.8.8"):
    print(f"{address:>12} -> {table.lookup(address)}")
```

```text
    10.9.9.9 -> ('10.0.0.0/8', 'A')
    10.1.9.9 -> ('10.1.0.0/16', 'B')
  10.1.2.200 -> ('10.1.2.0/24', 'C')
 192.168.5.5 -> ('192.168.0.0/16', 'D')
     8.8.8.8 -> ('0.0.0.0/0', 'default')
```

Each address picks the longest of its matching routes; `8.8.8.8` matches nothing but the default. Real routers use compressed forms of this structure and dedicated hardware, but the principle — a trie over address bits, with the deepest match winning — is the one shown.

## 🔤 Trie + DP: Segmenting a String

The [word break](../dynamic-programming/one-dimensional-dp.md) problem asks whether a string can be cut into dictionary words. The dynamic program tracks `ok[i]` — can the first `i` characters be segmented? — and the usual transition tests every split point `j < i`: is `ok[j]` true and is `s[j:i]` a word? That is O(n²) substring lookups. Two observations improve it:

1. **Words have a maximum length `m`.** Only split points within `m` characters need testing: O(n · m).
2. **A trie can drive the transition forward.** From each reachable position `i`, walk the trie along `s[i], s[i+1], …`; every time you pass a node that ends a word at position `j`, mark `j + 1` reachable; stop the moment the trie has no edge for the next character. Only the *prefixes of dictionary words* are ever examined — no substrings are created, and dead ends are abandoned at once.

The same forward pass **counts** the segmentations if reachable flags are replaced by counts: `ways[j + 1] += ways[i]` at every word end.

```python
class Node:
    __slots__ = ("children", "end")

    def __init__(self):
        self.children = {}
        self.end = False

def build_trie(words):
    root = Node()
    for word in words:
        node = root
        for ch in word:
            node = node.children.setdefault(ch, Node())
        node.end = True
    return root

def word_break_with_trie(s, root):
    reachable = [False] * (len(s) + 1)
    reachable[0] = True
    for i in range(len(s)):
        if not reachable[i]:
            continue
        node = root
        for j in range(i, len(s)):
            node = node.children.get(s[j])
            if node is None:
                break                                      # no dictionary word starts like s[i..j]
            if node.end:
                reachable[j + 1] = True                    # s[i..j] is a word
    return reachable[-1]

def count_segmentations_with_trie(s, root):
    ways = [0] * (len(s) + 1)
    ways[0] = 1
    for i in range(len(s)):
        if not ways[i]:
            continue
        node = root
        for j in range(i, len(s)):
            node = node.children.get(s[j])
            if node is None:
                break
            if node.end:
                ways[j + 1] += ways[i]
    return ways[-1]

def word_break_all_splits(s, dictionary):
    ok = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        ok[i] = any(ok[j] and s[j:i] in dictionary for j in range(i))
    return ok[-1]

def word_break_bounded(s, dictionary, longest):
    ok = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        ok[i] = any(ok[j] and s[j:i] in dictionary for j in range(max(0, i - longest), i))
    return ok[-1]

small = build_trie(["cat", "cats", "and", "sand", "dog"])
print(word_break_with_trie("catsanddog", small), count_segmentations_with_trie("catsanddog", small), word_break_with_trie("catsandog", small))       # True 2 False
pineapple = build_trie(["apple", "pen", "applepen", "pine", "pineapple"])
print(count_segmentations_with_trie("pineapplepenapple", pineapple))                                                                              # 3
```

`catsanddog` splits as `cats and dog` and as `cat sand dog` (two ways). `pineapplepenapple` splits as `pine apple pen apple`, `pineapple pen apple`, and `pine applepen apple` (three ways). How do the three methods compare on a real-sized dictionary? The test uses 20,000 words of up to 8 letters and strings made by gluing random dictionary words together (so each string *can* be segmented). The trie is built once, as it would be in a service that answers many queries, and its build time is reported separately; each timing is for a single string:

```python
import timeit

def load_vocabulary():
    for path in ("/usr/share/dict/words", "/usr/dict/words"):
        try:
            with open(path, encoding="utf-8", errors="ignore") as handle:
                found = {w.strip() for w in handle}
        except OSError:
            continue
        return sorted(w for w in found if w.isalpha() and w.islower() and w.isascii() and 3 <= len(w) <= 8), path
    rng = random.Random(1)
    syllables = ["ba", "ke", "li", "mo", "nu", "ra", "so", "ti", "ve", "wa", "zi", "the", "ing", "tion", "pre", "con", "un", "re"]
    return sorted({"".join(rng.choice(syllables) for _ in range(rng.randint(2, 4))) for _ in range(60_000)}), "synthetic syllable words"

vocabulary, source = load_vocabulary()
random.seed(7)
words = random.sample(vocabulary, min(20_000, len(vocabulary)))
dictionary = set(words)
longest = max(map(len, words))
build_ms = min(timeit.repeat(lambda: build_trie(words), number=1, repeat=3)) * 1000
root = build_trie(words)
print(f"{len(words):,} words from {source}; longest word {longest} letters; building the trie: {build_ms:.1f} ms (building the set: "
      f"{min(timeit.repeat(lambda: set(words), number=1, repeat=3)) * 1000:.2f} ms)")
print(f"{'string length':>13} | {'trie walk':>10} | {'bounded split lengths':>21} | {'all split points':>16}")
for count in (200, 500, 1_000, 2_000):
    text = "".join(random.choice(words) for _ in range(count))
    assert word_break_with_trie(text, root) and word_break_bounded(text, dictionary, longest)
    trie_ms = min(timeit.repeat(lambda: word_break_with_trie(text, root), number=3, repeat=3)) / 3 * 1000
    bounded_ms = min(timeit.repeat(lambda: word_break_bounded(text, dictionary, longest), number=3, repeat=3)) / 3 * 1000
    if len(text) < 4_000:
        all_ms = f"{min(timeit.repeat(lambda: word_break_all_splits(text, dictionary), number=1, repeat=1)) * 1000:13.1f} ms"
    else:
        all_ms = f"{'(too slow)':>16}"
    print(f"{len(text):>13,} | {trie_ms:7.2f} ms | {bounded_ms:18.2f} ms | {all_ms}")
```

Output:

```
20,000 words from /usr/share/dict/words; longest word 8 letters; building the trie: 24.8 ms (building the set: 0.54 ms)
string length |  trie walk | bounded split lengths | all split points
        1,311 |    0.18 ms |               0.86 ms |          69.7 ms
        3,331 |    0.47 ms |               2.15 ms |         762.6 ms
        6,724 |    0.95 ms |               4.37 ms |       (too slow)
       13,464 |    1.90 ms |               8.58 ms |       (too slow)
```

Three results stand out. Testing **every** split point is quadratic and hopeless for long strings (hundreds of times slower than the bounded version already at 3,000 characters). Merely **bounding the split length** by the longest word fixes the asymptotic problem with a one-line change. And the trie walk is several times faster still once it exists, because it never builds substrings or hashes them and abandons a path at the first impossible letter — but it costs far more to build than a set (tens of milliseconds against under a millisecond here), so it pays off when the same dictionary is used for many strings.

## 🔠 Suffix Tries: Counting Distinct Substrings

Insert **every suffix** of a string into a trie. Each distinct substring of the string is a prefix of some suffix, so it corresponds to exactly one non-root node. Therefore the number of distinct substrings equals the number of nodes (minus the root):

```python
def count_distinct_substrings(s):
    root, nodes = Node(), 0
    for start in range(len(s)):
        node = root
        for ch in s[start:]:
            if ch not in node.children:
                node.children[ch] = Node()
                nodes += 1                                # a new node is a new distinct substring
            node = node.children[ch]
    return nodes

print(count_distinct_substrings("banana"), count_distinct_substrings("aaaa"), count_distinct_substrings("abcd"))       # 15 4 10
```

`banana` has 15 distinct substrings (21 positions-and-lengths, with repeats such as `a`, `an`, `ana`, and `na`); `aaaa` has just 4 (`a`, `aa`, `aaa`, `aaaa`); and a string of `n` all-different letters has `n(n + 1)/2`, here 10. A suffix trie uses O(n²) nodes in the worst case; the compressed version, the *suffix tree*, needs only O(n) ([Wikipedia: Suffix tree](https://en.wikipedia.org/wiki/Suffix_tree)) and is the structure behind fast substring search in text editors and genome analysis.

## ✅ Verification

Each algorithm was compared with a brute-force definition on thousands of random inputs: all pairs and all subarrays for the XOR problems, `ipaddress` containment tests for the routing table, a plain recursion and the two substring-set programs for word break, and the set of all substrings for the suffix trie:

```python
def brute_lookup(routes, address):
    ip, best = ipaddress.ip_address(address), None
    for cidr, hop in routes.items():
        network = ipaddress.ip_network(cidr)
        if ip in network and (best is None or network.prefixlen > ipaddress.ip_network(best[0]).prefixlen):
            best = (cidr, hop)
    return best

def count_brute(s, words):
    return 1 if s == "" else sum(count_brute(s[len(w):], words) for w in words if s.startswith(w))

random.seed(1)
for _ in range(2_000):
    nums = [random.randint(0, 2 ** random.choice((3, 8, 20, 31)) - 1) for _ in range(random.randint(0, 12))]
    assert max_xor_pair(nums) == max_xor_pair_brute(nums)
    small_nums = [random.randint(0, 255) for _ in range(random.randint(0, 12))]
    assert max_xor_subarray(small_nums) == max_xor_subarray_brute(small_nums)

for _ in range(300):
    routes = {}
    for _ in range(random.randint(1, 10)):
        length = random.randint(0, 24)
        base = random.getrandbits(32) & ((0xFFFFFFFF << (32 - length)) & 0xFFFFFFFF) if length else 0
        routes[f"{ipaddress.ip_address(base)}/{length}"] = f"hop{len(routes)}"
    router = RouteTable()
    for cidr, hop in routes.items():
        router.add(cidr, hop)
    for _ in range(20):
        address = str(ipaddress.ip_address(random.getrandbits(32)))
        assert router.lookup(address) == brute_lookup(routes, address)

for _ in range(3_000):
    vocabulary_small = {"".join(random.choice("ab") for _ in range(random.randint(1, 3))) for _ in range(random.randint(1, 5))}
    text = "".join(random.choice("ab") for _ in range(random.randint(0, 9)))
    trie_root = build_trie(vocabulary_small)
    expected = count_brute(text, vocabulary_small)
    assert count_segmentations_with_trie(text, trie_root) == expected
    assert word_break_with_trie(text, trie_root) == (expected > 0) == word_break_all_splits(text, vocabulary_small)
    assert word_break_bounded(text, vocabulary_small, max(map(len, vocabulary_small))) == (expected > 0)

for _ in range(1_000):
    text = "".join(random.choice("abc") for _ in range(random.randint(0, 10)))
    assert count_distinct_substrings(text) == len({text[i:j] for i in range(len(text)) for j in range(i + 1, len(text) + 1)})
print("binary-trie XOR searches, routing lookups, trie word break and segmentation counts, and the suffix trie agree with brute force")
```

```text
binary-trie XOR searches, routing lookups, trie word break and segmentation counts, and the suffix trie agree with brute force
```

## Common Mistakes

- **Inserting bits from the least significant end.** A binary trie must be built from the most significant bit down, or "closest in the high bits" no longer means "deepest shared path".
- **Using too few bits.** If numbers can reach `2³¹` or beyond, `BinaryTrie(bits=31)` silently ignores the high bits; set `bits` to cover the largest value (for 64-bit values use 64).
- **Querying an empty trie** for the maximum XOR. The first number has nobody to pair with; insert before querying, or seed the trie as the subarray version does.
- **Forgetting the default route and "no match" in longest-prefix lookups.** Decide what `lookup` returns when no route matches, and make sure a shorter route stays as the fallback when a longer path dead-ends.
- **Rebuilding the trie for every query.** The build costs far more than a query; build once and reuse, or use a set with a bounded split length for one-off strings.
- **Counting segmentations without big integers in mind.** The number of segmentations can grow exponentially; Python's integers are exact, but in other languages the count may need to be taken modulo a number.
- **Expecting a suffix trie to be small.** It has O(n²) nodes; use a suffix tree or automaton for long strings.

## Module Summary

This module built one structure — a tree whose edges are symbols — and showed how much a node's *position as a prefix* can carry. [Trie Fundamentals](trie-fundamentals.md) defined the structure, measured how much prefix sharing saves, and compared it honestly with a set and with a sorted list searched by binary search: in Python a trie costs about ten times the memory of a set and does not beat `bisect` on a fixed word list, but it overtakes a sorted list once words are inserted continuously. [Trie Operations](trie-operations.md) added per-node counters, deletion that prunes dead branches, alphabetical autocomplete with early termination, and longest common prefix, all verified by a model test that checks the structure's invariant after every step. [Prefix Problems](prefix-problems.md) used the tree's ability to branch and prune for ranked suggestions, shortest roots, wildcard search, the longest word built one letter at a time, and a letter-board search that is several times faster than searching once per word. This file switched the edges to bits for the largest XOR pair and subarray and for longest-prefix IP routing, and combined the trie with dynamic programming for word segmentation and substring counting.

Carry these ideas forward:

- A trie answers prefix questions in time proportional to the length of the query, independent of the number of stored items; each node *is* a prefix and can carry data (a flag, a count, a route).
- Use it when the set changes, when you need per-prefix information, or when the question is a pattern or a pruned search; for a fixed word list in Python, a sorted list with `bisect` is simpler and usually faster.
- Prune early: the power of a trie search comes from abandoning a path the moment no stored item continues it.
- A binary trie over the most significant bits first makes "closest in the high bits" mean "deepest shared path", which is what XOR maximization and longest-prefix matching need.
- Build costs matter: a trie is expensive to construct in Python, so amortize it over many queries.
- Verify structures with a model: compare against a plain set or brute force on random operation sequences and check invariants (such as "no dead branches") after every step.

## ➡️ Next

Continue to the Operating Systems module, the first in the Computer Science Foundations domain, where the focus moves from the data structures and algorithms programs are built from to the system that runs them: processes, memory, scheduling, and files.
