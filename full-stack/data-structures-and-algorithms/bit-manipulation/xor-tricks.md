# ⚡ XOR Tricks

## The Operator That Undoes Itself

**XOR** (exclusive or, written `^` in Python) is true when its two inputs *differ*. Of the bitwise operators, it has the nicest algebra: a few simple properties that, combined, turn a surprising number of puzzles into a single loop with one variable. XOR is also what the hardware calls "addition without carrying", which is why it appears in checksums, error correction, RAID storage, and cryptography.

The properties, for any integers `a`, `b`, and `c`:

| Property | Statement | Why it is useful |
|----------|-----------|------------------|
| Identity | `a ^ 0 == a` | XOR with zero changes nothing |
| Self-inverse | `a ^ a == 0` | Equal values cancel completely |
| Commutative | `a ^ b == b ^ a` | Order does not matter |
| Associative | `(a ^ b) ^ c == a ^ (b ^ c)` | Grouping does not matter, so you can fold a whole list |
| Undo | `(a ^ b) ^ b == a` | XORing twice with the same value restores the original |

The last row is the engine behind encryption and recovery tricks; the second row, together with the first, is the engine behind the "find the odd one out" tricks. This file works through the classic ones — swapping, the unpaired number, the missing number, range queries, parity and recovery, a toy cipher, Gray codes, and distance — each verified against an independent method. All outputs were produced by running the code on CPython 3.9.

```python
a, b, c = 0b1100, 0b1010, 0b0110
print(a ^ 0 == a, a ^ a == 0, a ^ b == b ^ a, (a ^ b) ^ c == a ^ (b ^ c), (a ^ b) ^ b == a)     # True True True True True
```

## 🔄 Swapping Without a Temporary Variable (and Why You Should Not)

Three XORs swap two values with no third variable: `a ^= b; b ^= a; a ^= b`. After the first line `a` holds `a ^ b`; the second makes `b = b ^ (a ^ b) = a`; the third makes `a = (a ^ b) ^ a = b`.

```python
x, y = 5, 9
x ^= y
y ^= x
x ^= y
print(x, y)                                         # 9 5

def xor_swap(items, i, j):
    items[i] ^= items[j]
    items[j] ^= items[i]
    items[i] ^= items[j]

numbers = [3, 7, 11]
xor_swap(numbers, 0, 2)
print(numbers)                                      # [11, 7, 3]
xor_swap(numbers, 1, 1)                             # "swap" an element with itself...
print(numbers)                                      # [11, 0, 3]   — and the element was zeroed
a, b = 5, 9
a, b = b, a                                         # the Python way: clear, safe, and just as fast
print(a, b)                                         # 9 5
```

The second call shows the trap: when both positions are the same, the first XOR computes `v ^ v = 0`, and the value is lost. This *aliasing* problem is the reason the XOR swap must not be used blindly ([Wikipedia: XOR swap algorithm](https://en.wikipedia.org/wiki/XOR_swap_algorithm)). It also has no speed advantage on modern processors — the same article notes it can be slower than a temporary variable — and Python's tuple assignment `a, b = b, a` is the idiomatic swap. The trick is a classic interview question, and a useful way to see the properties above in action, but not code to write.

## 1️⃣ The Number That Has No Partner

*Every value in a list appears exactly twice, except one. Find the one.* A hash table or a sort would do it, but XOR folds the entire list into one value: pairs cancel (`v ^ v = 0`), zero is the identity, and the order does not matter, so only the unpaired value survives — in one pass and constant space.

```python
from functools import reduce
from operator import xor

def single_number(nums):
    """Every value occurs twice except one: the XOR of everything is that one."""
    return reduce(xor, nums, 0)

print(single_number([4, 1, 2, 1, 2]))               # 4
print(single_number([7]))                           # 7
```

### Two Unpaired Numbers

Now suppose **two** different values appear once and all others appear twice. XORing everything gives `a ^ b`, which is not enough by itself — but it is *non-zero*, and every 1 bit in it marks a position where `a` and `b` differ. Pick the lowest such bit (`both & -both`, from [power-of-two-and-counting-bits.md](power-of-two-and-counting-bits.md)). Split the list into numbers that have that bit set and numbers that do not: `a` and `b` land in different groups, and every pair stays together in one group (two equal numbers agree on every bit). XORing each group then cancels its pairs and leaves one unpaired number each.

```python
def two_single_numbers(nums):
    """Every value occurs twice except two different ones. Returns those two, sorted."""
    both = reduce(xor, nums, 0)                      # a ^ b; non-zero because a != b
    splitter = both & -both                          # the lowest bit where a and b differ
    a = b = 0
    for n in nums:
        if n & splitter:
            a ^= n
        else:
            b ^= n
    return sorted((a, b))

print(two_single_numbers([1, 2, 1, 3, 2, 5]))       # [3, 5]
```

## 2️⃣ The Missing Number

*A list contains the numbers `0` to `n` with exactly one absent. Which one?* XOR every index `0..n-1` and every value in the list together with `n`. Each present number appears twice (once as a value, once as an index or as `n`) and cancels; the absent number appears only once, as an index, so it is what remains.

```python
def missing_number(nums):
    """nums holds 0..n with one value absent."""
    result = len(nums)
    for index, value in enumerate(nums):
        result ^= index ^ value
    return result

print(missing_number([3, 0, 1]), missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1]), missing_number([0, 1]))      # 2 8 2
```

This is the XOR solution that [cyclic-sort.md](../sorting-algorithms/cyclic-sort.md) timed against the other approaches. Like the sum formula, it finds exactly one missing number; unlike the sum, it cannot overflow in languages with fixed-width integers, because XOR never carries.

## ➕ Prefix XOR: Range Queries in O(1)

Prefix sums answer "what is the sum of items `left..right`?" with one subtraction. XOR is its own inverse, so the same trick works for XOR: build `prefix[i] = nums[0] ^ … ^ nums[i-1]`; then the XOR of `left..right` is `prefix[right + 1] ^ prefix[left]`, because the shared prefix cancels:

```python
def build_prefix_xor(nums):
    prefix = [0]
    for value in nums:
        prefix.append(prefix[-1] ^ value)
    return prefix

def range_xor(prefix, left, right):
    """XOR of nums[left..right], inclusive."""
    return prefix[right + 1] ^ prefix[left]

nums = [4, 8, 2, 7]
prefix = build_prefix_xor(nums)
print(prefix, range_xor(prefix, 1, 3), 8 ^ 2 ^ 7)
```

```text
[0, 4, 12, 14, 9] 13 13
```

## 🧩 Parity and Recovering Lost Data

The **parity** of a number is whether it has an odd or even count of 1 bits, and XOR computes it: the XOR of all the bits is 1 exactly when the count is odd. Instead of examining 32 bits one at a time, you can **fold** the word onto itself — XOR the top half into the bottom half, then the top quarter, and so on — and reach the answer in five steps:

```python
def parity(x):
    """1 if the 32-bit value x has an odd number of 1 bits, else 0."""
    x ^= x >> 16
    x ^= x >> 8
    x ^= x >> 4
    x ^= x >> 2
    x ^= x >> 1
    return x & 1

print(parity(0b1011), parity(0b1111), parity(0xFFFFFFFF), parity(0x80000000))                 # 1 0 0 1
```

Parity is how storage systems survive a failed disk. If three data blocks `d1`, `d2`, and `d3` are stored alongside a parity block `p = d1 ^ d2 ^ d3`, then any one lost block equals the XOR of the three surviving blocks — by the undo property. RAID arrays that store parity use exactly this idea: when a drive fails, the remaining data is combined with the parity data using XOR to reconstruct the missing contents ([Wikipedia: Parity bit](https://en.wikipedia.org/wiki/Parity_bit)).

```python
blocks = [b"hello world!", b"parity demo.", b"xor is cool."]
parity_block = bytes(x ^ y ^ z for x, y, z in zip(*blocks))
rebuilt = bytes(p ^ x ^ z for p, x, z in zip(parity_block, blocks[0], blocks[2]))        # block 1 is "lost": rebuild it
print(parity_block.hex())
print(rebuilt, rebuilt == blocks[1])
```

```text
606b6c25722a7768786e6721
b'parity demo.' True
```

## 🔐 A Toy Cipher (and Why It Is Only a Toy)

The undo property gives a reversible scrambling: XOR each byte of a message with a byte of a key, and XOR again with the same key to get the message back.

```python
def xor_bytes(data, key):
    return bytes(byte ^ key[i % len(key)] for i, byte in enumerate(data))

secret = xor_bytes(b"attack at dawn", b"key")
print(secret.hex())
print(xor_bytes(secret, b"key"))
```

```text
0a110d0a06124b040d4b01181c0b
b'attack at dawn'
```

Repeating a short key like this is **not secure**: anyone who can guess part of the message can recover the key, and then the rest. The only XOR cipher that is provably unbreakable is the *one-time pad*, which requires a key that is truly random, at least as long as the message, and never reused ([Wikipedia: One-time pad](https://en.wikipedia.org/wiki/One-time_pad)). XOR is a building block in real ciphers, but scrambling data with a short repeating key is obfuscation, not encryption.

## 🔢 Gray Code: Counting With One Change at a Time

In ordinary binary, counting from 7 to 8 flips four bits at once (`0111` to `1000`), which is a problem for mechanical encoders and error-prone hardware that can read intermediate states. A **Gray code** orders the numbers so that each step changes exactly one bit; the binary-reflected Gray code is used in position encoders for this reason ([Wikipedia: Gray code](https://en.wikipedia.org/wiki/Gray_code)). It is computed with one XOR and one shift:

```python
def to_gray(n):
    return n ^ (n >> 1)

def from_gray(g):
    n = 0
    while g:
        n ^= g
        g >>= 1
    return n

print([format(to_gray(i), "04b") for i in range(16)])
```

```text
['0000', '0001', '0011', '0010', '0110', '0111', '0101', '0100', '1100', '1101', '1111', '1110', '1010', '1011', '1001', '1000']
```

Read down the list: each code differs from its neighbour in exactly one position, including from the last code to the first (`1000` to `0000`).

## 📏 Distance and Sign Tricks

Because `a ^ b` has a 1 exactly where `a` and `b` differ, the number of 1 bits in it is the **Hamming distance**: how many positions differ between the two patterns ([Wikipedia: Hamming weight](https://en.wikipedia.org/wiki/Hamming_weight) describes this use). It measures how many bit errors separate two received words, and is the basis of nearest-match searches on fingerprints and hashes. XOR of two integers is negative exactly when their signs differ, because the sign bit of the result is `1` only when the sign bits differ:

```python
def hamming_distance(a, b):
    return bin(a ^ b).count("1")

print(hamming_distance(0b1011101, 0b1001001), hamming_distance(1, 4), hamming_distance(255, 0))     # 2 2 8
print((7 ^ -3) < 0, (7 ^ 3) < 0, (-7 ^ -3) < 0)                                                      # True False False
```

(Finding the pair in a list whose XOR is *largest* is a classic problem that is solved efficiently with a trie of the numbers' bits; [tries-with-bits-and-dp.md](../tries/tries-with-bits-and-dp.md) shows how.)

## ✅ Verification

Every function was compared with an independent method on thousands of random inputs — a `Counter` for the unpaired numbers, direct loops for ranges, and a bit-by-bit count for parity and Gray codes:

```python
import random
from collections import Counter

random.seed(1)
for _ in range(3_000):
    pairs = [random.randint(0, 50) for _ in range(random.randint(0, 10))]
    single = random.randint(100, 200)
    nums = pairs * 2 + [single]
    random.shuffle(nums)
    assert single_number(nums) == single == next(v for v, c in Counter(nums).items() if c == 1)
    first, second = random.sample(range(100, 200), 2)
    nums = pairs * 2 + [first, second]
    random.shuffle(nums)
    assert two_single_numbers(nums) == sorted((first, second))

for _ in range(2_000):
    n = random.randint(1, 30)
    absent = random.randint(0, n)
    nums = [v for v in range(n + 1) if v != absent]
    random.shuffle(nums)
    assert missing_number(nums) == absent

    nums = [random.randint(0, 255) for _ in range(random.randint(1, 20))]
    prefix = build_prefix_xor(nums)
    left = random.randint(0, len(nums) - 1)
    right = random.randint(left, len(nums) - 1)
    assert range_xor(prefix, left, right) == reduce(xor, nums[left:right + 1])

for _ in range(5_000):
    value = random.getrandbits(32)
    assert parity(value) == bin(value).count("1") % 2
    p, q = random.randint(-100, 100), random.randint(-100, 100)
    assert ((p ^ q) < 0) == ((p < 0) != (q < 0))

codes = [to_gray(i) for i in range(1 << 10)]
assert all(bin(codes[i] ^ codes[(i + 1) % len(codes)]).count("1") == 1 for i in range(len(codes)))
assert sorted(codes) == list(range(1 << 10)) and all(from_gray(to_gray(i)) == i for i in range(100_000))
for n in range(40):
    message = bytes(random.getrandbits(8) for _ in range(n))
    assert xor_bytes(xor_bytes(message, b"k3y"), b"k3y") == message                       # XOR twice restores the message

for _ in range(300):
    length = random.randint(1, 16)
    data = [bytes(random.getrandbits(8) for _ in range(length)) for _ in range(4)]
    parity_block = bytes(reduce(xor, column) for column in zip(*data))
    lost = random.randrange(4)
    survivors = [block for i, block in enumerate(data) if i != lost]
    assert bytes(reduce(xor, column, p) for p, column in zip(parity_block, zip(*survivors))) == data[lost]
print("unpaired numbers, missing number, range XOR, parity, sign test, Gray codes, the cipher and parity recovery agree with the references")
```

```text
unpaired numbers, missing number, range XOR, parity, sign test, Gray codes, the cipher and parity recovery agree with the references
```

## Common Mistakes

- **Using the XOR swap on an array element with itself** (aliasing), which zeroes it. Prefer `a, b = b, a`.
- **Applying the "unpaired number" trick when values can appear a different number of times.** It relies on every other value appearing an *even* number of times; with triples or a mix of counts the answer is meaningless.
- **Confusing `^` with exponentiation.** In Python `2 ^ 3` is `1`; the power operator is `**`.
- **Treating repeating-key XOR as encryption.** It hides nothing from an attacker who knows or guesses a little of the message.
- **Forgetting that `a ^ b == 0` means `a == b`** — which makes XOR a branch-free equality test, but not a way to compare *which* is larger.
- **Using a signed trick on fixed-width data in another language.** The sign test `(a ^ b) < 0` is simple in Python because integers never overflow; in C it depends on the integer type.

## ➡️ Next

Continue to [power-of-two-and-counting-bits.md](power-of-two-and-counting-bits.md): subtracting 1 from a number flips its lowest set bit and everything below it, which makes `n & (n - 1)` a one-step test for powers of two, the basis of a bit-counting loop, and the start of a small family of patterns for lowest bits, trailing zeros, and rounding.
