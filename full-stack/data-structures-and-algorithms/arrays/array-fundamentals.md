# 🧱 Array Fundamentals

## The First Concrete Data Structure

[big-o-notation.md](../time-and-space-complexity/big-o-notation.md) and
[time-complexity.md](../time-and-space-complexity/time-complexity.md) gave this domain a precise
vocabulary for cost. This module applies that vocabulary to the most widely used data structure of
all: the **array** — the first *linear* structure named in
[what-are-data-structures.md](../introduction-to-data-structures-and-algorithms/what-are-data-structures.md),
and the storage underneath many of the structures that come later.

## 📦 What an Array Is

```
An ARRAY is a collection of elements stored in CONTIGUOUS memory
(one block, no gaps), where each element is identified by its
numeric INDEX, counting from 0.
```

```
index:      0      1      2      3      4
         ┌──────┬──────┬──────┬──────┬──────┐
value:   │  10  │  20  │  30  │  40  │  50  │
         └──────┴──────┴──────┴──────┴──────┘
address:  1000   1004   1008   1012   1016     (4-byte elements, block starts at 1000)
```

## ⚡ Why Index Access Is O(1)

```
address of items[i] = base_address + i × element_size

address of items[3] = 1000 + 3 × 4 = 1012
```

The computer never *searches* for an element by index — it *calculates* where the element lives:
one multiplication, one addition, one memory read. That costs the same for index 3 as for index
3,000,000, which is exactly why `get_first` in
[big-o-notation.md](../time-and-space-complexity/big-o-notation.md) is O(1).

## 🔬 See It for Yourself

Python's `array` module stores plain C integers in one compact block, which makes the arithmetic
above directly observable:

```python
import ctypes
from array import array

nums = array("i", [10, 20, 30, 40, 50])
base, length = nums.buffer_info()   # (memory address, number of elements)
size = nums.itemsize                # bytes per element

for i in range(length):
    # Read raw memory at base + i * size — no indexing involved
    print(i, ctypes.c_int.from_address(base + i * size).value)
```

```
0 10
1 20
2 30
3 40
4 50
```

Reading the memory at `base + i * size` returned each element in order — the formula is not a
metaphor, it is what the hardware does. (`itemsize` was 4 bytes on the machine used for this
output; it is the size of a C `int`, so it can differ between platforms. Reading raw memory is only
safe here because every address stays inside the array's own buffer.)

## 🔄 Fixed-Size vs. Dynamic Arrays

A plain array in C or Java has its **size fixed at creation** — the block is allocated once, and
growing it means allocating a new, larger block and copying everything across. A **dynamic array**
(Python's `list`, JavaScript's `Array`, Java's `ArrayList`, C++'s `std::vector`) automates that
resizing and keeps spare room so it doesn't have to happen on every append:

```python
class DynamicArray:
    def __init__(self):
        self._capacity = 1                       # slots allocated
        self._length = 0                          # slots in use
        self._slots = [None] * self._capacity

    def __len__(self):
        return self._length

    def __getitem__(self, index):
        if not 0 <= index < self._length:
            raise IndexError("index out of range")
        return self._slots[index]

    def append(self, value):
        if self._length == self._capacity:        # full: grow
            self._resize(self._capacity * 2)
        self._slots[self._length] = value
        self._length += 1

    def _resize(self, new_capacity):
        new_slots = [None] * new_capacity
        for i in range(self._length):             # copy every element: O(n)
            new_slots[i] = self._slots[i]
        self._slots = new_slots
        self._capacity = new_capacity
```

Appending nine values and printing `length` and `capacity` after each one shows the pattern:

```
length=1 capacity=1
length=2 capacity=2
length=3 capacity=4
length=4 capacity=4
length=5 capacity=8
length=6 capacity=8
length=7 capacity=8
length=8 capacity=8
length=9 capacity=16
```

Most appends write into a free slot at O(1) cost. Only occasionally is the array full, forcing an
O(n) copy — which is why the honest description of `append` is **amortized O(1)**, the same
qualifier [time-complexity.md](../time-and-space-complexity/time-complexity.md) attached to it.

### Why the Occasional Copy Doesn't Ruin the Average

When capacity doubles, the copy work across *all* resizes is a geometric sum: 1 + 2 + 4 + 8 + …
Counting it for 1,000 appends with the loop below gives 1,023 copied elements in total — fewer than
2 × 1,000. Spread over 1,000 appends, that is about one extra copy per append: a constant.

```python
n = 1000
copies = 0
capacity = 1
for length in range(n):
    if length == capacity:      # array full: copy `length` elements
        copies += length
        capacity *= 2
print(copies)                   # 1023
```

## 🐍 What a Python `list` Actually Is

The Python documentation describes CPython's list as a variable-length array built on a
**contiguous array of references** to other objects (see the official
[design FAQ](https://docs.python.org/3/faq/design.html)). Two consequences follow:

- `items[i]` is still the address arithmetic described above, so it stays O(1).
- A list of integers stores *references* to integer objects, not the integers themselves, so it uses
  more memory than the compact `array("i", ...)` shown earlier.

The over-allocation is observable with `sys.getsizeof`:

```python
import sys

items = []
last = sys.getsizeof(items)
for i in range(20):
    items.append(i)
    size = sys.getsizeof(items)
    if size != last:
        print(f"length {len(items):>2} -> allocated size jumped to {size} bytes")
        last = size
```

```
length  1 -> allocated size jumped to 88 bytes
length  5 -> allocated size jumped to 120 bytes
length  9 -> allocated size jumped to 184 bytes
length 17 -> allocated size jumped to 248 bytes
```

(Output from CPython 3.9 on a 64-bit machine; exact numbers differ between versions and platforms.)
The allocation changes only occasionally — not on every append — and the growth is not exactly
doubling (the last jump above went from room for 16 references to room for 24). That is a
deliberate implementation choice; what matters for analysis is the amortized O(1) guarantee, which
the [Python Wiki's time-complexity table](https://wiki.python.org/moin/TimeComplexity) lists for
`append`.

## 🌐 The Same Idea Across Languages

| Language | Typical resizable array type |
|----------|------------------------------|
| Python | `list` |
| JavaScript | `Array` |
| Java | `ArrayList` |
| C++ | `std::vector` |

The details differ — in JavaScript, reading past the end returns `undefined` instead of raising an
error, `items[-1]` is `undefined` (use `items.at(-1)` for the last element), and assigning past the
end leaves empty holes:

```js
const a = [1, 2, 3];
console.log(a[-1], a[5], a.at(-1));   // undefined undefined 3
a[5] = 9;
console.log(a, a.length);              // [ 1, 2, 3, <2 empty items>, 9 ] 6
```

In Python, `items[-1]` is the last element and an out-of-range read raises `IndexError`:

```python
a = [10, 20, 30]
print(a[-1], a[-3])   # 30 10
a[3]                  # IndexError: list index out of range
```

## ⚙️ The Cost Profile at a Glance

| Operation | Typical cost | Covered in |
|-----------|--------------|------------|
| Read or write by index | O(1) | this file |
| Visit every element | O(n) | [traversal.md](traversal.md) |
| Add or remove at the end | O(1) amortized | [insertion-and-deletion.md](insertion-and-deletion.md) |
| Add or remove at the front or middle | O(n) | [insertion-and-deletion.md](insertion-and-deletion.md) |
| Search an unsorted array | O(n) | [traversal.md](traversal.md) |
| Search a sorted array | O(log n) | binary search, in [what-are-algorithms.md](../introduction-to-data-structures-and-algorithms/what-are-algorithms.md) |

## Common Mistakes

- **Off-by-one errors** — an array of length `n` has valid indices `0` through `n - 1`; index `n` is
  one past the end.
- **Treating `append` as always cheap** — it is amortized O(1); an individual append that triggers a
  resize costs O(n).
- **Confusing length with capacity** — length is how many elements are stored; capacity is how many
  slots are allocated. They differ in every dynamic array.
- **Assuming negative indexes mean the same thing everywhere** — Python counts from the end; in
  JavaScript `items[-1]` is simply `undefined`.
- **Building a 2D grid with repeated references** — `[[0] * 3] * 3` creates *one* inner list
  referenced three times:

```python
grid = [[0] * 3] * 3
grid[0][0] = 1
print(grid)              # [[1, 0, 0], [1, 0, 0], [1, 0, 0]]  — every row changed

grid = [[0] * 3 for _ in range(3)]
grid[0][0] = 1
print(grid)              # [[1, 0, 0], [0, 0, 0], [0, 0, 0]]  — three separate rows
```

## ➡️ Next

Continue to [traversal.md](traversal.md) to see the most basic array operation — visiting every
element — and the mistakes that commonly go with it.
