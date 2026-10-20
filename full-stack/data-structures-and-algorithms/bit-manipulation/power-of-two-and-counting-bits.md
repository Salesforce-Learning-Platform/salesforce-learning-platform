# 📐 Power of Two and Counting Bits

## One Subtraction Reveals the Lowest Set Bit

Subtracting 1 from a binary number has a very regular effect on its bits. Look at the lowest bit that is 1: subtracting 1 turns that bit **into a 0** and turns every 0 below it **into a 1** (it borrows through them), while the bits above it stay as they are. For `44 = 101100`, the lowest set bit is at position 2, and `43 = 101011`: the `1` at position 2 became `0`, and the two zeros beneath it became ones.

Two patterns follow immediately, and most of this file is built from them:

- `n & (n - 1)` **clears the lowest set bit** — the bits that changed (the lowest 1 and the zeros under it) now disagree with the original, and AND turns them all to 0, while the bits above are unchanged.
- `n & -n` **isolates the lowest set bit**. Negation is "flip all bits and add one", so `-n` agrees with `n` at the lowest set bit and below it (zeros and that single one) and is the complement of `n` above it; the AND keeps only the lowest set bit.

```python
for n in (44, 8, 1):
    print(f"n         = {n:>3} = {n:08b}")
    print(f"n - 1     = {n - 1:>3} = {n - 1:08b}")
    print(f"n & (n-1) = {n & (n - 1):>3} = {n & (n - 1):08b}    (lowest set bit cleared)")
    print(f"-n        = {-n:>3} = {-n & 0xFF:08b}    (8-bit view)")
    print(f"n & -n    = {n & -n:>3} = {n & -n:08b}    (lowest set bit isolated)")
    print()
```

```text
n         =  44 = 00101100
n - 1     =  43 = 00101011
n & (n-1) =  40 = 00101000    (lowest set bit cleared)
-n        = -44 = 11010100    (8-bit view)
n & -n    =   4 = 00000100    (lowest set bit isolated)

n         =   8 = 00001000
n - 1     =   7 = 00000111
n & (n-1) =   0 = 00000000    (lowest set bit cleared)
-n        =  -8 = 11111000    (8-bit view)
n & -n    =   8 = 00001000    (lowest set bit isolated)

n         =   1 = 00000001
n - 1     =   0 = 00000000
n & (n-1) =   0 = 00000000    (lowest set bit cleared)
-n        =  -1 = 11111111    (8-bit view)
n & -n    =   1 = 00000001    (lowest set bit isolated)
```

All outputs in this file were produced by running the code on CPython 3.9.

## 🔍 Is It a Power of Two?

A power of two is a number with **exactly one set bit** (`1`, `10`, `100`, `1000`, …). Clearing the lowest set bit of such a number leaves nothing, so `n & (n - 1) == 0`. The converse holds for positive numbers: if clearing the lowest set bit leaves zero, there was only one set bit. The test needs one extra condition, because `0 & -1` is also `0` but zero is not a power of two:

```python
def is_power_of_two(n):
    return n > 0 and n & (n - 1) == 0

print([n for n in range(1, 130) if is_power_of_two(n)])         # [1, 2, 4, 8, 16, 32, 64, 128]
print(is_power_of_two(0), is_power_of_two(-8), is_power_of_two(2**100), is_power_of_two(2**100 + 1))      # False False True False
```

(The comparison `n & (n - 1) == 0` works as written in Python, where `&` binds tighter than `==`; in C it needs parentheses.) The same expression answers many practical questions: whether a buffer or FFT size is valid, whether a memory address is aligned to a power-of-two boundary (`address & (alignment - 1) == 0`), and whether a hash table can use the fast modulo described next.

### Modulo by a Power of Two Is a Mask

`n % 2ᵏ` is the value of the lowest `k` bits of `n`, which is exactly `n & (2ᵏ - 1)`. Hash tables and ring buffers use power-of-two capacities for this reason: the wrap-around index is one AND instead of a division. In Python the equivalence also holds for **negative** numbers, because both `%` and `&` follow floor semantics (in C, `%` of a negative number is negative, and the two disagree):

```python
capacity = 8
index = 0
visited = []
for _ in range(20):
    visited.append(index)
    index = (index + 1) & (capacity - 1)                 # wrap around without a division
print(visited)
print(-7 % 8, -7 & 7, 100 % 16, 100 & 15)                # 1 1 4 4
```

```text
[0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3]
1 1 4 4
```

## 🔢 Counting Set Bits (Population Count)

The number of 1 bits in a number is its **population count** or *Hamming weight*. It is the size of a bitset, the parity of a word, and — applied to `a ^ b` — the Hamming distance between two values ([Wikipedia: Hamming weight](https://en.wikipedia.org/wiki/Hamming_weight)).

### Clear One Bit at a Time

Since `n & (n - 1)` removes the lowest set bit, repeating it until `n` is zero takes **one iteration per set bit**. Peter Wegner described this in 1960; it is the method usually called Brian Kernighan's algorithm in interview material ([Wikipedia: Hamming weight](https://en.wikipedia.org/wiki/Hamming_weight)).

```python
def count_set_bits(n):
    """Population count by clearing the lowest set bit each time. n must be non-negative."""
    if n < 0:
        raise ValueError("expected a non-negative integer")
    count = 0
    while n:
        n &= n - 1                                       # remove the lowest set bit
        count += 1
    return count

n = 0b101100
steps = []
while n:
    steps.append(format(n, "06b"))
    n &= n - 1
print(" -> ".join(steps + ["000000"]), "=", count_set_bits(0b101100), "set bits")
print(count_set_bits(0), count_set_bits(255), count_set_bits(2**64 - 1), count_set_bits(2**64))      # 0 8 64 1
```

```text
101100 -> 101000 -> 100000 -> 000000 = 3 set bits
0 8 64 1
```

The guard against negative numbers is not decoration. In Python a negative number has infinitely many leading 1 bits (see [bitwise-operators.md](bitwise-operators.md)), so `n &= n - 1` never reaches zero — the loop would run forever. To count the bits of a negative number as a fixed-width pattern, mask it first: `count_set_bits(-1 & 0xFF)` is `8`.

### Other Ways to Count

The same count can be found by converting to text, by looking up bytes in a table, or by adding adjacent bit groups in parallel (a "SWAR" method, for SIMD within a register): add every pair of bits, then every pair of 2-bit counts, then nibbles, and finally sum the four bytes at once by multiplying by `0x01010101`. Wikipedia lists the 64-bit constants of this method ([Hamming weight](https://en.wikipedia.org/wiki/Hamming_weight)); the 32-bit version is:

```python
BYTE_COUNTS = [bin(i).count("1") for i in range(256)]

def count_with_text(n):
    return bin(n).count("1")

def count_with_table(n):
    count = 0
    while n:
        count += BYTE_COUNTS[n & 0xFF]
        n >>= 8
    return count

def count_in_parallel_32(x):
    x = x - ((x >> 1) & 0x55555555)                      # each pair of bits now holds its own count (0..2)
    x = (x & 0x33333333) + ((x >> 2) & 0x33333333)       # each nibble holds a count (0..4)
    x = (x + (x >> 4)) & 0x0F0F0F0F                      # each byte holds a count (0..8)
    return ((x * 0x01010101) & 0xFFFFFFFF) >> 24         # the top byte of the product is the sum of the four bytes

assert count_set_bits(0b1011) == count_with_text(0b1011) == count_with_table(0b1011) == count_in_parallel_32(0b1011) == 3
for value in range(1 << 12):
    assert count_set_bits(value) == count_with_text(value) == count_with_table(value) == count_in_parallel_32(value)
print("all four methods agree on every 12-bit number")
```

```text
all four methods agree on every 12-bit number
```

Which one is fastest in Python? The test below uses 10,000 random 32-bit values (average of about 16 set bits), then times the loop-based method on numbers with many and with few set bits:

```python
import random
import timeit

random.seed(1)
values = [random.getrandbits(32) for _ in range(10_000)]
for value in values[:2_000]:
    assert count_set_bits(value) == count_with_text(value) == count_with_table(value) == count_in_parallel_32(value)

print(f"{'method':>24} | {'time per call':>13}")
for label, method in [("bin(n).count('1')", count_with_text), ("clear lowest bit loop", count_set_bits),
                      ("byte table", count_with_table), ("parallel (SWAR) 32-bit", count_in_parallel_32)]:
    microseconds = min(timeit.repeat(lambda: [method(v) for v in values], number=1, repeat=3)) / len(values) * 1e6
    print(f"{label:>24} | {microseconds:>10.3f} us")

dense = [(1 << 32) - 1 - (1 << random.randrange(32)) for _ in range(1_000)]      # 31 set bits
sparse = [1 << random.randrange(32) for _ in range(1_000)]                       # 1 set bit
for label, data in [("loop on 31 set bits", dense), ("loop on 1 set bit", sparse)]:
    microseconds = min(timeit.repeat(lambda: [count_set_bits(v) for v in data], number=1, repeat=3)) / len(data) * 1e6
    print(f"{label:>24} | {microseconds:>10.3f} us")
```

Output:

```
                  method | time per call
       bin(n).count('1') |      0.222 us
   clear lowest bit loop |      0.840 us
              byte table |      0.318 us
  parallel (SWAR) 32-bit |      0.255 us
     loop on 31 set bits |      1.530 us
       loop on 1 set bit |      0.109 us
```

In CPython, `bin(n).count("1")` is the fastest of the four because it runs in compiled code, while the loop pays interpreter overhead for every set bit. The loop's cost tracks the **number of set bits**: it is more than ten times cheaper on a number with a single 1 than on one with 31. Python 3.10 added a built-in, `int.bit_count()`, which is documented as equivalent to `bin(n).count("1")` — for the absolute value of negative numbers — and is the right tool on those versions ([Python docs: `int.bit_count`](https://docs.python.org/3/library/stdtypes.html#int.bit_count)). It is not available on the Python 3.9 used to run this module, so the examples here use the equivalent forms.

### Counting the Bits of Every Number From 0 to n

A frequent task is the popcount of *all* numbers up to `n`. Calling the loop for each number costs O(n log n). A recurrence does it in O(n): the bits of `i` are the bits of `i >> 1` (everything except the last bit) plus the last bit; or equivalently, the bits of `i & (i - 1)` plus one:

```python
def counting_bits(n):
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i >> 1] + (i & 1)                 # drop the last bit, then add it back
    return bits

def counting_bits_clear_lowest(n):
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i & (i - 1)] + 1                  # clear the lowest set bit, then count it
    return bits

print(counting_bits(16))
assert counting_bits(50_000) == counting_bits_clear_lowest(50_000) == [bin(i).count("1") for i in range(50_001)]
```

```text
[0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4, 1]
```

Each entry is built from an earlier entry, so every number is computed once from a smaller one — the same idea as dynamic programming, which a later module develops fully.

## 🧱 More Single-Bit Patterns

The same family of tricks locates the lowest and highest set bits and rounds to powers of two:

```python
import math

def lowest_set_bit(n):
    return n & -n

def trailing_zeros(n):
    return (n & -n).bit_length() - 1                      # the position of the lowest set bit

def highest_set_bit(n):
    return 1 << (n.bit_length() - 1)

def floor_log2(n):
    return n.bit_length() - 1

def next_power_of_two(n):
    """The smallest power of two that is >= n (n >= 1)."""
    return 1 << (n - 1).bit_length()

print(f"{'n':>4} | {'binary':>9} | {'lowest bit':>10} | {'trailing zeros':>14} | {'highest bit':>11} | {'next power of 2':>15}")
for n in (1, 5, 12, 16, 17, 100):
    print(f"{n:>4} | {n:>9b} | {lowest_set_bit(n):>10} | {trailing_zeros(n):>14} | {highest_set_bit(n):>11} | {next_power_of_two(n):>15}")

big = 2**60 - 1
print(int(math.log2(big)), floor_log2(big))               # 60 59   — floating point rounds up; bit_length is exact
```

```text
   n |    binary | lowest bit | trailing zeros | highest bit | next power of 2
   1 |         1 |          1 |              0 |           1 |               1
   5 |       101 |          1 |              0 |           4 |               8
  12 |      1100 |          4 |              2 |           8 |              16
  16 |     10000 |         16 |              4 |          16 |              16
  17 |     10001 |          1 |              0 |          16 |              32
 100 |   1100100 |          4 |              2 |          64 |             128
60 59
```

`n.bit_length() - 1` is the exact integer logarithm. The last line shows why not to use `math.log2` for this: `2**60 - 1` is not a power of two, its floor logarithm is 59, but converting it to a floating-point number rounds it up to `2**60`, so `int(math.log2(...))` answers 60. Exact integer arithmetic is the safer tool for bit-level questions.

Rounding up works because `n - 1` has the same number of bits as the next power of two minus one: for `n = 17`, `n - 1 = 16` has 5 bits, and `1 << 5 = 32`; for `n = 16`, `n - 1 = 15` has 4 bits and `1 << 4 = 16` — already a power of two, so it is returned unchanged.

## ✅ Verification

All of these were compared with obvious reference computations — membership in a list of powers, string counting, and a direct search for the smallest power of two that is large enough:

```python
import random

random.seed(2)
powers = [2**k for k in range(80)]
for n in range(100_000):
    assert is_power_of_two(n) == (n in powers[:20])
for k in range(1, 200):
    assert is_power_of_two(2**k) and not is_power_of_two(2**k + 1) and (k < 2 or not is_power_of_two(2**k - 1))

for n in range(1, 5_000):
    assert next_power_of_two(n) == next(p for p in powers if p >= n)
    assert highest_set_bit(n) == max(p for p in powers if p <= n)
    assert lowest_set_bit(n) == next(p for p in powers if n % (2 * p) == p)
    assert trailing_zeros(n) == next(k for k in range(80) if (n >> k) & 1)
    assert n - lowest_set_bit(n) == n & (n - 1)

for _ in range(5_000):
    x, k = random.randint(-10**9, 10**9), random.randint(0, 20)
    assert x % (1 << k) == x & ((1 << k) - 1)

try:
    count_set_bits(-1)
except ValueError as error:
    print("ValueError:", error)
print(count_set_bits(-1 & 0xFF))                                                  # 8
print("power-of-two tests, lowest and highest bit, rounding, and modulo by mask agree with the references")
```

```text
ValueError: expected a non-negative integer
8
power-of-two tests, lowest and highest bit, rounding, and modulo by mask agree with the references
```

## Common Mistakes

- **Forgetting `n > 0` in the power-of-two test.** `0 & (0 - 1)` is `0`, so zero would be reported as a power of two.
- **Running the clear-lowest-bit loop on a negative number.** In Python it never terminates; validate the input or mask it to a width first.
- **Using floating-point logarithms for exact bit work.** Large integers round, and `int(math.log2(n))` can be off by one; use `bit_length()`.
- **Assuming `n & -n` works for 0.** It returns `0` — there is no set bit — so check for zero before using the result as a mask.
- **Counting the bits of a negative number with `bin(n).count("1")`.** It counts the bits of the *magnitude* (`bin(-5)` is `-0b101`), as does `int.bit_count()`; for a two's-complement pattern, mask to a width first.
- **Using the SWAR method on numbers wider than its width.** The 32-bit version above is only correct for values below `2**32`.

## Module Summary

This module treated an integer as what it really is: a row of bits you can inspect and change directly. [Bitwise Operators](bitwise-operators.md) introduced the vocabulary: binary, octal, and hex notation; AND, OR, XOR, NOT, and the shifts; how Python's unbounded integers behave like two's complement with infinitely many sign bits; right shifts that floor; and the precedence and `^`-versus-`**` traps. [Bit Masking](bit-masking.md) used masks to get, set, clear, and toggle single bits, to extract and insert multi-bit fields, to build flags, permissions, packed colors and network addresses, to enumerate subsets and submasks, and to store sets of small integers as bitsets. [XOR Tricks](xor-tricks.md) put XOR's algebra to work: the unpaired and missing numbers, range queries with prefix XOR, parity and RAID-style recovery, a toy cipher and its limits, Gray codes, and Hamming distance. This file showed that `n & (n - 1)` and `n & -n` expose the lowest set bit, and used them for power-of-two tests, population counts, per-number bit counts, and rounding.

Carry these ideas forward:

- `1 << i` builds a one-bit mask; `|` sets, `& ~` clears, `^` toggles, and `(x >> i) & 1` reads a bit.
- Python integers have no fixed width: mask with `& 0xFF…` when you need fixed-width behaviour, and remember that right shifts floor and `~x` equals `-x - 1`.
- XOR cancels equal values (`a ^ a == 0`) and undoes itself (`(a ^ b) ^ b == a`); that alone solves the unpaired-number family and powers parity and recovery schemes.
- `n & (n - 1)` clears the lowest set bit and `n & -n` isolates it; a power of two has exactly one set bit.
- In CPython, built-in operations such as `bin(n).count("1")` (or `int.bit_count()` on 3.10+) usually beat hand-written bit loops; the hand-written versions matter for understanding, interviews, and languages without the built-in.
- Bit tricks pay off for flags, compact sets, and exact integer checks, but readable code that states its intent is worth more than a saved line.

## ➡️ Next

Continue to the Dynamic Programming module, the next module in this domain, where the focus moves from manipulating single values to solving problems by building answers out of smaller answers.
