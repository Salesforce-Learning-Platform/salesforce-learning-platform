# 🔢 Bitwise Operators

## Numbers Are Patterns of Bits

Every integer in a computer is stored as a pattern of bits: zeros and ones. Ordinary arithmetic hides that fact — you write `12 + 10` and never think about it — but **bitwise operators** let you work on the pattern directly: switch individual bits on and off, compare two patterns bit by bit, or slide a pattern left and right. A handful of cheap operations on bits can replace loops, lookups, and extra memory, and they are the foundation of flags and permissions, network addresses, compression, graphics, hashing, error detection, and a long list of interview puzzles.

This first file covers the vocabulary: how Python writes and prints binary numbers, the six bitwise operators and what each does to a pattern, how **negative numbers** behave (Python has no fixed word size, which changes the rules slightly from C or Java), why shifting is multiplication and division by powers of two, and the traps that catch beginners — operator precedence and `^` versus `**`. The later files in the module build on this: [masking](bit-masking.md), [XOR tricks](xor-tricks.md), and [power-of-two and bit-counting patterns](power-of-two-and-counting-bits.md). All outputs were produced by running the code on CPython 3.9.

## 🔟 Writing and Reading Binary, Octal, and Hexadecimal

A **bit** is one binary digit. Bits are numbered from the right, starting at **0**: in `1010`, bit 0 is `0`, bit 1 is `1`, bit 2 is `0`, and bit 3 is `1`. The value of a pattern is the sum of `2ᵢ` over the positions `i` that hold a 1 — so `1010` is `8 + 2 = 10`.

Python can write numbers in several bases directly, and convert between them:

```python
print(bin(10), oct(15), hex(255))                               # 0b1010 0o17 0xff
print(0b1010, 0o17, 0xFF)                                       # 10 15 255
print(format(10, "08b"), format(255, "#06x"), format(5, "b"))   # 00001010 0x00ff 101
print(int("1010", 2), int("ff", 16), int("17", 8))              # 10 255 15
print((255).bit_length(), (256).bit_length(), (0).bit_length()) # 8 9 0
```

- The prefixes `0b`, `0o`, and `0x` start binary, octal, and hexadecimal literals.
- `bin`, `oct`, and `hex` produce the strings; `format(n, "08b")` pads with zeros to a fixed width, which is how you line patterns up when printing.
- `int(text, base)` converts back.
- `n.bit_length()` is the number of bits needed to write `n` without leading zeros ([Python docs: `int.bit_length`](https://docs.python.org/3/library/stdtypes.html#int.bit_length)).

Hexadecimal is popular because **one hex digit is exactly four bits**: `0xFF` is `1111 1111`, `0xA5` is `1010 0101`. It is a compact way to write long bit patterns.

## ⚙️ The Six Operators

| Operator | Name | What it does to two patterns |
|----------|------|------------------------------|
| `a & b` | AND | A bit is 1 only where **both** have a 1 |
| `a \| b` | OR | A bit is 1 where **either** has a 1 |
| `a ^ b` | XOR (exclusive or) | A bit is 1 where the two bits **differ** |
| `~a` | NOT (complement) | Flips every bit |
| `a << n` | Left shift | Slides the pattern left by `n` places, filling with zeros |
| `a >> n` | Right shift | Slides the pattern right by `n` places, dropping bits that fall off |

The truth table for the three two-input operators, one bit at a time:

| `a` | `b` | `a & b` | `a \| b` | `a ^ b` |
|-----|-----|---------|----------|---------|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 | 0 |

```python
a, b = 0b1100, 0b1010
print(f"a      = {a:04b}")
print(f"b      = {b:04b}")
print(f"a & b  = {a & b:04b}    (1 only where both are 1)")
print(f"a | b  = {a | b:04b}    (1 where either is 1)")
print(f"a ^ b  = {a ^ b:04b}    (1 where they differ)")
print(f"a << 2 = {a << 2:06b}  (slide left; zeros enter on the right)")
print(f"a >> 2 = {a >> 2:04b}    (slide right; the low bits fall off)")
print(f"~a     = {~a}  (see the next section)")
```

```text
a      = 1100
b      = 1010
a & b  = 1000    (1 only where both are 1)
a | b  = 1110    (1 where either is 1)
a ^ b  = 0110    (1 where they differ)
a << 2 = 110000  (slide left; zeros enter on the right)
a >> 2 = 0011    (slide right; the low bits fall off)
~a     = -13  (see the next section)
```

Each of the first three operators works on **all the bits at once**, in a single operation. That is the source of their power: `a & b` compares as many bit positions as the numbers have, without a loop.

## ➖ Negative Numbers: Two's Complement With No Fixed Width

Computers store negative integers using **two's complement**: to negate a number, flip all its bits and add one ([Wikipedia: Two's complement](https://en.wikipedia.org/wiki/Two%27s_complement)). In a fixed 8-bit word, `5` is `00000101`, so `-5` is `11111010 + 1 = 11111011`.

Python integers have no fixed width, so the language defines bitwise operations as though the number had **an infinite string of sign bits** on the left: positive numbers are padded with infinitely many zeros, negative numbers with infinitely many ones ([Python docs: bitwise operations](https://docs.python.org/3/library/stdtypes.html#bitwise-operations-on-integer-types)). Two consequences follow:

- `~x` is always `-x - 1`, and `-x` is always `~x + 1`.
- `bin()` shows a negative number as a minus sign and a magnitude (`bin(-5)` is `-0b101`), *not* as its two's-complement bits. To see the bits a fixed-width computer would store, mask with `& 0xFF` (or `0xFFFF`, and so on).

```python
print(~5, -5 - 1, ~0, ~-1)                           # -6 -6 -1 0
print(-5 == ~5 + 1)                                  # True
print(bin(-5), (-5).bit_length())                    # -0b101 3
print(format(-5 & 0xFF, "08b"), -5 & 0xFF)           # 11111011 251
print(format(-1 & 0xFFFF, "016b"))                   # 1111111111111111
```

The last two lines show the 8-bit and 16-bit two's-complement patterns of `-5` and `-1`. Masking is the standard way to simulate fixed-width integers in Python: if you need the behavior of a 32-bit unsigned value, apply `& 0xFFFFFFFF`.

## ⏩ Shifts: Multiplying and Dividing by Powers of Two

Shifting left by `n` places multiplies by `2ⁿ`, and shifting right by `n` places divides by `2ⁿ` — but the division **rounds toward negative infinity**, exactly like `//`. The Python documentation states both equivalences ([Python docs: bitwise operations](https://docs.python.org/3/library/stdtypes.html#bitwise-operations-on-integer-types)). The rounding matters for negative numbers:

```python
print(f"{'x':>4} | {'x << 3':>6} | {'x * 8':>5} | {'x >> 2':>6} | {'x // 4':>6} | {'int(x / 4)':>10}")
for x in (13, 12, -12, -13):
    print(f"{x:>4} | {x << 3:>6} | {x * 8:>5} | {x >> 2:>6} | {x // 4:>6} | {int(x / 4):>10}")

try:
    1 << -1
except ValueError as error:
    print("ValueError:", error)                      # (the message is: negative shift count)
print(1 << 100)                                      # 1267650600228229401496703205376
```

```text
   x | x << 3 | x * 8 | x >> 2 | x // 4 | int(x / 4)
  13 |    104 |   104 |      3 |      3 |          3
  12 |     96 |    96 |      3 |      3 |          3
 -12 |    -96 |   -96 |     -3 |     -3 |         -3
 -13 |   -104 |  -104 |     -4 |     -4 |         -3
ValueError: negative shift count
1267650600228229401496703205376
```

- `-13 >> 2` is `-4`, the same as `-13 // 4` — not `-3`, which is what truncating toward zero (`int(x / 4)`) would give. A right shift of a negative number keeps the infinite string of sign bits, so the result stays negative: `-1 >> 10` is still `-1`.
- Shifting by a negative count is an error.
- Because Python integers grow as needed, `1 << 100` is fine; there is no overflow. (In C or Java, shifting a 32-bit `int` by 32 or more is undefined or wraps around.)

In Python you rarely need `<< 1` to double a number — multiplication is just as fast. Shifts earn their place when you are *building a mask* (`1 << i`, covered in [bit-masking.md](bit-masking.md)) or extracting fields from a packed value.

## ⚠️ Python-Specific Traps

**1. Precedence.** In Python, the bitwise operators bind *tighter* than comparisons but *looser* than arithmetic and shifts. From tightest to loosest: `~x`, then `* / // %`, then `+ -`, then `<< >>`, then `&`, then `^`, then `|`, then comparisons ([Python docs: operator precedence](https://docs.python.org/3/reference/expressions.html#operator-precedence)). So `x & 1 == 0` means `(x & 1) == 0` — different from C, where `==` binds tighter than `&`. But `+` binds tighter than `<<`, which surprises people who read `1 << n + 1` as "shift by n, then add one":

```python
x = 6
print(x & 1 == 0)                    # True    — parsed as (x & 1) == 0, which is what you want in Python
print(1 << 2 + 1)                    # 8       — parsed as 1 << (2 + 1)
print((1 << 2) + 1)                  # 5
```

When in doubt, add parentheses — and always parenthesize when the code may be read by someone used to C.

**2. `^` is XOR, not a power.** The power operator is `**`.

**3. `~` on booleans.** `True` and `False` are integers (`1` and `0`), so `~True` is `-2` and `~False` is `-1` — both truthy. Use `not` for boolean negation:

```python
print(2 ^ 3, 2 ** 3)                 # 1 8
print(~True, ~False)                 # -2 -1
print(bool(~True), bool(~False), not True)       # True True False
```

**4. `&`, `|`, and `^` on booleans do not short-circuit.** `True | expensive()` always calls `expensive()`, whereas `True or expensive()` does not. Use `and` / `or` for logic and `&` / `|` for bits.

## ✅ Identities, Verified

Bitwise operators obey exact algebraic laws, and checking a few of them on random integers — including negative ones — confirms that Python's infinite-sign-bit model behaves consistently:

```python
import random

random.seed(1)
for _ in range(20_000):
    a = random.randint(-10**6, 10**6)
    b = random.randint(-10**6, 10**6)
    n = random.randint(0, 40)
    assert ~(a & b) == ~a | ~b and ~(a | b) == ~a & ~b                   # De Morgan's laws
    assert a ^ b == (a | b) & ~(a & b)                                   # XOR is "or, but not both"
    assert a + b == (a ^ b) + 2 * (a & b)                                # add without carry, plus the carries
    assert a | b == a + b - (a & b)                                      # inclusion-exclusion on bits
    assert a << n == a * 2 ** n and a >> n == a // 2 ** n                # shifts are multiplication and floor division
    assert -a == ~a + 1 and ~a == -a - 1                                 # two's complement negation
print("all identities hold for 20,000 random pairs, including negative numbers")
```

```text
all identities hold for 20,000 random pairs, including negative numbers
```

The third identity deserves a second look: `a + b == (a ^ b) + 2 * (a & b)`. XOR gives the sum of each bit position *ignoring carries*, and `a & b` marks exactly the positions that generate a carry (both bits 1), which moves one place left — hence the `2 *`. Hardware adders are built on exactly this decomposition.

## 🧰 Where Bits Show Up

| Use | Idea |
|-----|------|
| Flags and permissions | One bit per yes/no option, many options in one integer ([masking](bit-masking.md)) |
| Packing data | Several small values in one integer: colors, IPv4 addresses, protocol headers |
| Sets of small integers | A bit per possible member; union, intersection, and difference become `\|`, `&`, `& ~` |
| Checksums and error detection | XOR and parity ([XOR tricks](xor-tricks.md)) |
| Fast checks and counts | Power-of-two tests, counting set bits ([power of two and counting bits](power-of-two-and-counting-bits.md)) |
| Hashing, encryption, and compression | Mixing bits with shifts and XOR |

## Common Mistakes

- **Reading `bin(-5)` as the stored bits.** It prints a sign and a magnitude; use `x & 0xFF` to see a fixed-width pattern.
- **Assuming a fixed word size.** Python has none: `~x` does not give "the 8-bit complement" but `-x - 1`; mask the result if you need a fixed width.
- **Forgetting that right shift floors.** `-13 >> 2` is `-4`, not `-3`.
- **Mixing up precedence with C.** In Python `x & 1 == 0` works as written; `1 << n + 1` does not mean `(1 << n) + 1`.
- **Using `^` for powers**, or `~` as logical NOT.
- **Shifting by a negative count**, which raises `ValueError`.

## ➡️ Next

Continue to [bit-masking.md](bit-masking.md): a **mask** is a pattern that selects bits, and with it you can test, set, clear, toggle, extract, and insert individual bits and fields — the technique behind flags, packed data, and subsets stored as integers.
