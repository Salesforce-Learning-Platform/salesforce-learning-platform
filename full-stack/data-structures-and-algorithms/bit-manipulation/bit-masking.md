# 🎭 Bit Masking

## A Mask Selects the Bits You Care About

A **mask** is a number whose 1 bits mark the positions you want to look at or change. Combine a mask with a value using the [bitwise operators](bitwise-operators.md) and you can read, switch, or replace exactly those bits while leaving all the others alone — in a single operation, without loops. Masks are how a single integer holds a dozen yes/no settings, how a 32-bit network address is split into parts, how a color is stored as three bytes, and how an algorithm can represent "which of these 20 items have I picked?" as one number.

The idea has three parts: **build** a mask, **combine** it with a value (`&` to keep or test bits, `|` to set them, `^` to flip them, `& ~` to clear them), and **shift** to move fields into place. This file starts with the five single-bit operations, extends them to multi-bit fields, applies them to permissions, packed data, and network addresses, and ends with two uses that reach beyond bit twiddling: enumerating all subsets of a set, and using a Python integer as a compact set of small integers. All outputs were produced by running the code on CPython 3.9.

## 🧱 The Five Single-Bit Operations

The key building block is `1 << i`: the number that has **only bit `i`** set. For `i = 3` it is `0b1000`. Every single-bit operation combines that mask with the value:

| Operation | Expression | How it works |
|-----------|------------|--------------|
| **Get** bit `i` | `(x >> i) & 1` | Slide bit `i` down to position 0, then keep only that bit |
| **Set** bit `i` (make it 1) | `x \| (1 << i)` | OR with the mask turns the bit on; other bits are unchanged |
| **Clear** bit `i` (make it 0) | `x & ~(1 << i)` | `~mask` is all 1s except bit `i`; AND keeps everything else and zeroes bit `i` |
| **Toggle** bit `i` | `x ^ (1 << i)` | XOR with 1 flips a bit; XOR with 0 leaves it alone |
| **Update** bit `i` to a value | `(x & ~(1 << i)) \| (value << i)` | Clear the bit, then OR in the new value |

```python
def get_bit(x, i):
    return (x >> i) & 1

def set_bit(x, i):
    return x | (1 << i)

def clear_bit(x, i):
    return x & ~(1 << i)

def toggle_bit(x, i):
    return x ^ (1 << i)

def update_bit(x, i, value):
    return (x & ~(1 << i)) | (value << i)

x = 0b10110
print(f"x                 = {x:05b}")
print(f"get_bit(x, 1)     = {get_bit(x, 1)}      get_bit(x, 3) = {get_bit(x, 3)}")
print(f"set_bit(x, 0)     = {set_bit(x, 0):05b}")
print(f"clear_bit(x, 2)   = {clear_bit(x, 2):05b}")
print(f"toggle_bit(x, 4)  = {toggle_bit(x, 4):05b}")
print(f"update_bit(x,3,0) = {update_bit(x, 3, 0):05b}")
```

```text
x                 = 10110
get_bit(x, 1)     = 1      get_bit(x, 3) = 0
set_bit(x, 0)     = 10111
clear_bit(x, 2)   = 10010
toggle_bit(x, 4)  = 00110
update_bit(x,3,0) = 10110
```

Bit positions are counted from the right, starting at 0. Python integers have no fixed width, so `~(1 << i)` is a negative number with infinitely many leading 1 bits — which is exactly what `&` needs: the mask keeps *every* other bit, however many there are. (In C or Java the width of the complement would matter; in Python it never does.)

## 📏 Fields: Several Bits at a Time

A **field** is a run of adjacent bits that together hold a small number. To work with a field you need two numbers: how far it is from the right edge (`shift`) and how wide it is (`width`). The mask of `width` ones is `(1 << width) - 1`:

| `width` | `(1 << width) - 1` | In binary |
|---------|--------------------|-----------|
| 1 | 1 | `1` |
| 4 | 15 | `1111` |
| 8 | 255 | `11111111` |

```python
def extract_bits(x, shift, width):
    """The `width` bits of x that start at bit position `shift`."""
    return (x >> shift) & ((1 << width) - 1)

def insert_bits(x, shift, width, field):
    """x with the `width` bits at position `shift` replaced by `field`."""
    mask = ((1 << width) - 1) << shift
    return (x & ~mask) | ((field << shift) & mask)

packed = 0b1101_0110_1011
print(f"packed                    = {packed:012b}")
print(f"extract_bits(packed,4,4)  = {extract_bits(packed, 4, 4):04b}   (the middle nibble)")
changed = insert_bits(packed, 4, 4, 0b1001)
print(f"insert_bits(packed,4,4,9) = {changed:012b}")
print(f"field too wide is cut off: {insert_bits(packed, 4, 4, 0b11111):012b}")
```

```text
packed                    = 110101101011
extract_bits(packed,4,4)  = 0110   (the middle nibble)
insert_bits(packed,4,4,9) = 110110011011
field too wide is cut off: 110111111011
```

`extract_bits` shifts the field down to the right edge and masks off everything above it. `insert_bits` builds a mask over the field's position, clears that region of `x`, and ORs in the new value, itself masked so that an over-wide `field` cannot spill into neighbouring bits.

## 🚩 Flags and Permissions

When a setting is yes or no, give it one bit. A single integer can then hold dozens of settings, and combining or checking them is one operation. Python's `enum.IntFlag` wraps this pattern in a readable class: the members are integers, they combine with `|`, and `in` tests membership ([Python docs: enum](https://docs.python.org/3/library/enum.html#enum.IntFlag)).

```python
import enum

class Permission(enum.IntFlag):
    EXECUTE = 1
    WRITE = 2
    READ = 4

mode = Permission.READ | Permission.WRITE
print(int(mode), Permission.WRITE in mode, Permission.EXECUTE in mode)        # 6 True False
mode |= Permission.EXECUTE                                                    # add a flag
mode &= ~Permission.WRITE                                                     # remove a flag
print(int(mode), format(int(mode), "03b"))                                    # 5 101
print([flag.name for flag in Permission if flag in mode])                     # ['EXECUTE', 'READ']
print(bool(mode & Permission.READ), bool(mode & Permission.WRITE))            # True False
```

The same encoding is behind Unix file permissions. A mode such as `0o755` is three groups of three bits — owner, group, other — where `r = 4`, `w = 2`, and `x = 1`; the octal digit is the sum of the bits that are on:

```python
import stat

mode = 0o755
print([(mode >> shift) & 0b111 for shift in (6, 3, 0)])                       # [7, 5, 5]
print(stat.filemode(0o100000 | mode))                                         # -rwxr-xr-x
print(bool(mode & stat.S_IWGRP), bool(mode & stat.S_IWUSR))                   # False True
```

The test `mode & stat.S_IWGRP` asks "is the group-write bit on?": a mask with a single 1, ANDed with the value. Octal is convenient here because each octal digit is exactly three bits ([Python docs: stat](https://docs.python.org/3/library/stat.html)).

## 📦 Packing Several Values Into One Integer

Fields let you store small values side by side. A color is three bytes — red, green, blue — that fit in 24 bits; an IPv4 address is four bytes in 32 bits:

```python
def pack_rgb(r, g, b):
    return (r << 16) | (g << 8) | b

def unpack_rgb(color):
    return (color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF

print(hex(pack_rgb(255, 128, 0)), unpack_rgb(0xFF8000))                       # 0xff8000 (255, 128, 0)

def ip_to_int(address):
    a, b, c, d = (int(part) for part in address.split("."))
    return (a << 24) | (b << 16) | (c << 8) | d

def int_to_ip(number):
    return ".".join(str((number >> shift) & 0xFF) for shift in (24, 16, 8, 0))

print(ip_to_int("192.168.1.10"), int_to_ip(3232235786), hex(ip_to_int("192.168.1.10")))    # 3232235786 192.168.1.10 0xc0a8010a
```

Packing also makes **network masks** a one-line test. An address belongs to a network when its first `prefix` bits match the network's. Build a mask with `prefix` ones followed by `32 - prefix` zeros, and AND:

```python
def in_network(address, network, prefix):
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    return ip_to_int(address) & mask == ip_to_int(network) & mask

print(format((0xFFFFFFFF << 8) & 0xFFFFFFFF, "032b"))                         # 11111111111111111111111100000000
print(in_network("192.168.1.77", "192.168.1.0", 24), in_network("192.168.2.77", "192.168.1.0", 24))      # True False
```

Notice the final `& 0xFFFFFFFF`: shifting left in Python never discards bits, so to get a 32-bit result you mask explicitly.

## 🧮 Subsets as Bit Patterns

A set of `n` items has `2ⁿ` subsets, and each subset can be written as an `n`-bit number: bit `i` is 1 when item `i` is in the subset. Counting from `0` to `2ⁿ - 1` therefore visits every subset exactly once:

```python
def subsets(items):
    n = len(items)
    for mask in range(1 << n):
        yield [items[i] for i in range(n) if (mask >> i) & 1]

print(list(subsets(["a", "b", "c"])))

def has_subset_with_sum(numbers, target):
    n = len(numbers)
    return any(sum(numbers[i] for i in range(n) if (mask >> i) & 1) == target for mask in range(1 << n))

print(has_subset_with_sum([3, 34, 4, 12, 5, 2], 9), has_subset_with_sum([3, 34, 4, 12, 5, 2], 30))   # True False
```

```text
[[], ['a'], ['b'], ['a', 'b'], ['c'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c']]
True False
```

The brute-force check costs O(2ⁿ · n), which is fine for about 20 items (a million masks) and hopeless for 40 (a trillion). When a problem has overlapping sub-structure, the [Dynamic Programming](../dynamic-programming/README.md) module shows how to avoid recomputation, and "bitmask DP" uses these same integers as states.

A neighbouring trick enumerates only the **submasks** of a given mask — the subsets of a subset. Starting from the mask itself, `(sub - 1) & mask` steps to the next smaller submask, because subtracting 1 flips the lowest set bit and everything below it, and the AND discards the bits that were never in the mask:

```python
def submasks(mask):
    sub = mask
    while True:
        yield sub
        if sub == 0:
            break
        sub = (sub - 1) & mask

print([format(s, "04b") for s in submasks(0b1011)])
```

```text
['1011', '1010', '1001', '1000', '0011', '0010', '0001', '0000']
```

A mask with `k` bits set has exactly `2ᵏ` submasks; these eight come out in decreasing order, each visited once, with no wasted steps.

## 🧰 A Python Integer as a Set of Small Integers

If the members of a set are small non-negative integers, you can store the set as a **bitset**: bit `v` is 1 when `v` is a member. Python integers can be arbitrarily long, so one integer can represent a set of any size:

| Set operation | Bitset operation |
|---------------|------------------|
| Add `v` | `bits \|= 1 << v` |
| Remove `v` | `bits &= ~(1 << v)` |
| Is `v` a member? | `(bits >> v) & 1` |
| Union | `a \| b` |
| Intersection | `a & b` |
| Difference | `a & ~b` |
| Symmetric difference | `a ^ b` |

```python
def to_bitset(values, universe):
    buffer = bytearray((universe + 7) // 8)
    for v in values:
        buffer[v >> 3] |= 1 << (v & 7)
    return int.from_bytes(buffer, "little")

def from_bitset(bits):
    return [i for i in range(bits.bit_length()) if (bits >> i) & 1]

A = to_bitset([1, 3, 5, 7], 16)
B = to_bitset([3, 4, 5, 6], 16)
print(from_bitset(A | B), from_bitset(A & B), from_bitset(A & ~B), from_bitset(A ^ B))
```

```text
[1, 3, 4, 5, 6, 7] [3, 5] [1, 7] [1, 4, 6, 7]
```

Each of these operations processes many members in one step. Here is how that compares with Python's built-in `set` for two sets of 50,000 members each, drawn from a universe of 100,000 possible values:

```python
import random
import sys
import timeit

random.seed(2)
universe = 100_000
set_a = set(random.sample(range(universe), 50_000))
set_b = set(random.sample(range(universe), 50_000))
bits_a, bits_b = to_bitset(set_a, universe), to_bitset(set_b, universe)
assert to_bitset(set_a & set_b, universe) == bits_a & bits_b
assert to_bitset(set_a | set_b, universe) == bits_a | bits_b
assert to_bitset(set_a - set_b, universe) == bits_a & ~bits_b

t_set = min(timeit.repeat(lambda: set_a & set_b, number=20, repeat=3)) / 20 * 1000
t_bits = min(timeit.repeat(lambda: bits_a & bits_b, number=20, repeat=3)) / 20 * 1000
print(f"intersection with set:    {t_set:9.4f} ms   memory per set: {sys.getsizeof(set_a):>9,} bytes")
print(f"intersection with bitset: {t_bits:9.4f} ms   memory per set: {sys.getsizeof(bits_a):>9,} bytes")
print(f"a bitset holding only the value 10,000,000 takes {sys.getsizeof(1 << 10_000_000):,} bytes; a set holding it takes {sys.getsizeof({10_000_000}):,}")
```

Output:

```
intersection with set:       1.0040 ms   memory per set: 2,097,368 bytes
intersection with bitset:    0.0003 ms   memory per set:    13,360 bytes
a bitset holding only the value 10,000,000 takes 1,333,360 bytes; a set holding it takes 216
```

When the universe is small and the sets are dense, the bitset wins by orders of magnitude in both time and memory. The last line shows the catch: a bitset needs one bit for **every possible value** up to its largest member, whether it is present or not, so sets drawn from a huge universe waste memory. Choose a bitset when the possible values are few (say, up to a few hundred thousand) and the sets are crowded; choose a `set` otherwise.

## ✅ Verification

The helpers were compared with straightforward references: a list of 0/1 digits for the single-bit operations and fields, the standard `ipaddress` module for the address functions, and `itertools.combinations` for subsets:

```python
import ipaddress
import itertools
import random

random.seed(1)
for _ in range(5_000):
    x = random.randint(0, 2**20)
    i = random.randint(0, 24)
    digits = [(x >> j) & 1 for j in range(40)]                           # the reference: one digit per bit
    assert get_bit(x, i) == digits[i]
    assert set_bit(x, i) == x + (0 if digits[i] else 2**i)
    assert clear_bit(x, i) == x - (2**i if digits[i] else 0)
    assert toggle_bit(x, i) == (x - 2**i if digits[i] else x + 2**i)
    value = random.randint(0, 1)
    assert get_bit(update_bit(x, i, value), i) == value
    shift, width = random.randint(0, 10), random.randint(1, 8)
    field = random.randint(0, 2**width - 1)
    inserted = insert_bits(x, shift, width, field)
    assert extract_bits(inserted, shift, width) == field
    assert inserted >> (shift + width) == x >> (shift + width)           # bits above the field are untouched
    assert inserted & ((1 << shift) - 1) == x & ((1 << shift) - 1)       # bits below the field are untouched

for _ in range(3_000):
    number = random.randint(0, 2**32 - 1)
    address = int_to_ip(number)
    assert ip_to_int(address) == number == int(ipaddress.IPv4Address(address))
    prefix = random.randint(0, 32)
    network = ipaddress.ip_network((random.randint(0, 2**32 - 1), prefix), strict=False)
    assert in_network(address, str(network.network_address), prefix) == (ipaddress.ip_address(address) in network)

for n in range(0, 9):
    items = list(range(n))
    expected = {frozenset(c) for size in range(n + 1) for c in itertools.combinations(items, size)}
    produced = [frozenset(s) for s in subsets(items)]
    assert len(produced) == 2**n and set(produced) == expected
    for mask in range(1 << n):
        assert len(list(submasks(mask))) == 2 ** bin(mask).count("1") == len(set(submasks(mask)))
print("single-bit operations, fields, addresses, network masks, subsets and submasks agree with the references")
```

```text
single-bit operations, fields, addresses, network masks, subsets and submasks agree with the references
```

## Common Mistakes

- **Counting bit positions from the left.** Position 0 is the least significant (rightmost) bit, so `1 << i` is the mask for position `i` counted from the right.
- **Using `^` to clear a bit.** `x ^ mask` *toggles*; clearing needs `x & ~mask`. Setting a bit that is already set with `^` would turn it off.
- **Forgetting to mask a field when inserting it.** A value wider than the field spills into its neighbours; `insert_bits` masks it.
- **Expecting a fixed width.** Python integers are unbounded: `x << 8` never loses the top bits. Mask with `& 0xFFFFFFFF` (or the width you need) when you want fixed-width behaviour.
- **Testing a flag with `==`.** `mode == Permission.READ` is true only when *nothing else* is set; use `mode & Permission.READ` (or `in`).
- **Enumerating subsets for large `n`.** `2ⁿ` grows explosively; 20 items are fine, 40 are not.
- **Using a bitset for a sparse set over a huge universe.** The memory is proportional to the largest value, not to the number of members.

## ➡️ Next

Continue to [xor-tricks.md](xor-tricks.md): the XOR operator has a short list of algebraic properties that solve surprising problems — finding the one unpaired number, swapping without a temporary, parity checks, and recovering lost data — in a single pass and constant space.
