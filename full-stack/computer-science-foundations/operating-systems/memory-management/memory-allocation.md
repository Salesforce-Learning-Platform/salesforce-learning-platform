# 🧱 Memory Allocation

## Handing Out Contiguous Memory

The simplest way to share RAM among programs is to give each one a single contiguous block, described by the base and limit registers of [memory-management-basics.md](memory-management-basics.md). The oldest schemes did exactly that. A system might give all of memory except a small part reserved for the operating system to one program at a time, as MS-DOS did, or divide memory into **partitions**, each holding one job ([Wikipedia: Memory management (operating systems)](https://en.wikipedia.org/wiki/Memory_management_(operating_systems))). Partitions come in two kinds:

- **Fixed (static) partitions** are set up at boot time or by an operator. Every job receives a whole partition, so a small job in a large partition wastes the unused rest of it. That wasted space is *inside* the allocated block, and is called **internal fragmentation**.
- **Variable (dynamic) partitions** are created to fit each job exactly. Nothing is wasted inside a block, but as jobs finish and leave, the free memory is chopped into separate **holes**, and a new job needs one hole big enough for all of it. When the free memory is split into pieces too small to use even though their total would be enough, the waste is *between* the blocks, and is called **external fragmentation** ([Wikipedia: Fragmentation (computing)](https://en.wikipedia.org/wiki/Fragmentation_(computing))).

Modern systems have two layers of allocation, and each can fragment: the kernel hands out memory in pages, and inside a process an allocator such as `malloc` divides the pages among the program's objects (the same article). This file studies the allocation problem in its pure form, a row of memory handed out in variable-sized contiguous blocks, because every allocator at either layer faces it. All code was run on CPython 3.9 on a Mac; the simulations are deterministic (fixed random seeds), so on the same Python version you should see the same figures.

## 🧮 A Row of Memory in Code

To compare allocation strategies, the class below models a row of memory as numbered units. The free space is a list of **holes**, kept sorted by address, and the allocated blocks are a dictionary. Four **placement policies** decide which hole serves a request:

| Policy | Rule | Cost of the search |
|--------|------|--------------------|
| **First fit** | Take the first hole, from the start of memory, that is big enough | Stops early |
| **Next fit** | Like first fit, but resume the search where the previous allocation ended | Stops early; spreads allocations around memory |
| **Best fit** | Take the smallest hole that is big enough | Must look at every hole |
| **Worst fit** | Take the largest hole | Must look at every hole |

(The policies are heuristics for what is, in general, a hard packing problem; Wikipedia's article on fragmentation describes all four ([Wikipedia: Fragmentation (computing)](https://en.wikipedia.org/wiki/Fragmentation_(computing))).) The class also merges neighbouring holes when a block is freed, can **compact** memory by sliding every block to one end, and can check its own bookkeeping:

```python
import copy
import random

class Memory:
    """A row of `size` units. Free space is a list of holes (start, length), sorted by address and never touching."""

    def __init__(self, size):
        self.size = size
        self.holes = [(0, size)]
        self.blocks = {}                            # start address -> length, for the allocated blocks
        self.rover = 0                              # where the next-fit policy resumes its search
        self.examined = 0                           # how many holes the searches have looked at so far

    def allocate(self, length, policy):
        """Return the start address of a new block of `length` units, or None if no single hole is big enough."""
        order = list(range(len(self.holes)))
        if policy == "next":                        # next fit: start at the first hole after the previous allocation, wrapping around
            first = next((i for i, (start, _) in enumerate(self.holes) if start >= self.rover), 0)
            order = order[first:] + order[:first]
        chosen = None
        for i in order:
            self.examined += 1
            size = self.holes[i][1]
            if size < length:
                continue
            if policy in ("first", "next"):         # take the first hole that is big enough
                chosen = i
                break
            if chosen is None or (policy == "best" and size < self.holes[chosen][1]) or (policy == "worst" and size > self.holes[chosen][1]):
                chosen = i                          # best fit keeps the smallest big-enough hole, worst fit the largest
        if chosen is None:
            return None
        start, size = self.holes[chosen]
        if size == length:
            del self.holes[chosen]
        else:
            self.holes[chosen] = (start + length, size - length)    # the block takes the front of the hole
        self.blocks[start] = length
        self.rover = start + length
        return start

    def free(self, start):
        """Release a block and merge the new hole with any hole that touches it."""
        length = self.blocks.pop(start)
        merged = []
        for hole_start, hole_length in sorted(self.holes + [(start, length)]):
            if merged and merged[-1][0] + merged[-1][1] == hole_start:
                merged[-1] = (merged[-1][0], merged[-1][1] + hole_length)
            else:
                merged.append((hole_start, hole_length))
        self.holes = merged

    def compact(self):
        """Slide every block towards address 0, joining all holes into one. Returns how many units were copied."""
        copied, position, moved_blocks = 0, 0, {}
        for start in sorted(self.blocks):
            length = self.blocks[start]
            if start != position:
                copied += length                    # this block has to be copied to its new place
            moved_blocks[position] = length
            position += length
        self.blocks = moved_blocks
        self.holes = [(position, self.size - position)] if position < self.size else []
        self.rover = 0
        return copied

    def free_total(self):
        return sum(length for _, length in self.holes)

    def largest_hole(self):
        return max((length for _, length in self.holes), default=0)

    def check(self):
        """Raise an error unless the holes and blocks tile the memory exactly, with no touching holes."""
        spans = sorted([(s, l, "hole") for s, l in self.holes] + [(s, l, "block") for s, l in self.blocks.items()])
        position = 0
        for start, length, kind in spans:
            assert start == position and length > 0, "gap, overlap, or empty piece"
            position = start + length
        assert position == self.size
        assert all(a[0] + a[1] < b[0] for a, b in zip(self.holes, self.holes[1:])), "two holes touch"
```

Now a small, readable scenario. Seven blocks fill a 200-unit memory, and then three of them (A, C, and E) are freed, leaving three holes:

```python
memory = Memory(200)
where = {}
for name, size in (("A", 30), ("B", 15), ("C", 50), ("D", 10), ("E", 25), ("F", 40), ("G", 30)):
    where[name] = memory.allocate(size, "first")
for name in ("A", "C", "E"):
    memory.free(where[name])
print("holes (start, length):", memory.holes, "| free in total:", memory.free_total(), "| largest hole:", memory.largest_hole())

for policy in ("first", "best", "worst"):
    trial = copy.deepcopy(memory)
    start = trial.allocate(20, policy)
    print(f"{policy:>5} fit places a 20-unit request at {start:>3}; holes afterwards: {trial.holes}")
```

```text
holes (start, length): [(0, 30), (45, 50), (105, 25)] | free in total: 105 | largest hole: 50
first fit places a 20-unit request at   0; holes afterwards: [(20, 10), (45, 50), (105, 25)]
 best fit places a 20-unit request at 105; holes afterwards: [(0, 30), (45, 50), (125, 5)]
worst fit places a 20-unit request at  45; holes afterwards: [(0, 30), (65, 30), (105, 25)]
```

The same request, three different answers. First fit used the first hole it met and left a leftover of 10 units. Best fit searched everything and chose the snuggest hole, the 25-unit one, leaving a sliver of only 5 units. Worst fit took the 50-unit hole, on the theory that what remains (30 units) is big enough to be useful. Which of these is "best" depends on what requests arrive next, which no allocator can know; the experiments below measure it.

## 🕳️ External Fragmentation, and Compaction

There are 105 free units in the scenario above, yet no single hole is larger than 50, so a request for 60 units cannot be satisfied: the memory is *fragmented*. One cure is **compaction**: move all the allocated blocks to one end so that the holes merge into a single big one. It works only if blocks can be moved, which is exactly what the base register of [memory-management-basics.md](memory-management-basics.md) provides (relocatable partitions can be compacted; [Wikipedia: Memory management (operating systems)](https://en.wikipedia.org/wiki/Memory_management_(operating_systems))), and it is not free, because every block that moves must be copied:

```python
print("a request for 60 units, with", memory.free_total(), "free in total ->", memory.allocate(60, "first"))
copied = memory.compact()
print("compaction copied", copied, "units; holes are now", memory.holes)
print("the same request for 60 units now ->", memory.allocate(60, "first"))
memory.check()
```

```text
a request for 60 units, with 105 free in total -> None
compaction copied 95 units; holes are now [(95, 105)]
the same request for 60 units now -> 95
```

Compaction rescued the request, at the price of copying 95 units of data, nearly everything in memory. On a real machine that would be 95 *megabytes* or more of copying while the affected programs wait, which is why general-purpose systems avoid depending on it. [paging.md](paging.md) shows the cleverer way out: break memory into fixed-size pieces so that no hole is ever too small to reuse.

## 🧪 Which Policy Fragments Least?

One worked example cannot rank the policies. The next experiment runs each one on the same long sequences of random requests. Memory has 10,000 units; each request asks for between 20 and 400 units; and to keep the memory under steady pressure, the program frees a randomly chosen block whenever memory is fuller than a target, and otherwise makes a new request. Each policy runs the same 30 random sequences of 1,500 requests, at two levels of fullness. A request **fails** when no single hole is big enough. In this experiment the free memory in total is always larger than any request, so every failure is caused by fragmentation alone, and the program asserts that. The *external fragmentation* column is the share of free memory that is not in the largest hole (0% would mean all free space is in one piece):

```python
def run(policy, seed, requests=1500, size=10_000, target=0.8):
    rng = random.Random(seed)
    memory, live = Memory(size), []
    failed = frag_sum = holes_per_block = samples = 0
    for _ in range(requests):
        while live and size - memory.free_total() > target * size:    # too full: some program finishes and frees its block
            memory.free(live.pop(rng.randrange(len(live))))
        length = rng.randint(20, 400)
        start = memory.allocate(length, policy)
        if start is None:
            assert memory.free_total() >= length                      # the request failed although enough memory was free
            failed += 1
        else:
            live.append(start)
        frag_sum += 1 - memory.largest_hole() / memory.free_total()
        holes_per_block += len(memory.holes) / max(1, len(memory.blocks))
        samples += 1
    memory.check()
    return failed, frag_sum, holes_per_block, samples, memory.examined

for target in (0.6, 0.8):
    print(f"memory kept about {target:.0%} full (30 runs of 1,500 requests per policy)")
    print(f"{'policy':>7} | {'requests failed':>15} | {'external fragmentation':>22} | {'holes per block':>15} | {'holes examined per request':>26}")
    for policy in ("first", "next", "best", "worst"):
        totals = [0, 0.0, 0.0, 0, 0]
        for seed in range(30):
            for i, value in enumerate(run(policy, seed, target=target)):
                totals[i] += value
        failed, frag_sum, holes_per_block, samples, examined = totals
        print(f"{policy:>7} | {failed / samples:>15.1%} | {frag_sum / samples:>22.1%} | {holes_per_block / samples:>15.2f} | {examined / samples:>26.1f}")
```

```text
memory kept about 60% full (30 runs of 1,500 requests per policy)
 policy | requests failed | external fragmentation | holes per block | holes examined per request
  first |            0.0% |                  44.6% |            0.50 |                        7.6
   next |            0.0% |                  75.6% |            0.51 |                        1.8
   best |            0.0% |                  39.8% |            0.49 |                       14.5
  worst |            0.9% |                  85.3% |            0.51 |                       15.0
memory kept about 80% full (30 runs of 1,500 requests per policy)
 policy | requests failed | external fragmentation | holes per block | holes examined per request
  first |           13.6% |                  78.8% |            0.49 |                       12.2
   next |           22.6% |                  82.7% |            0.49 |                        9.8
   best |            3.1% |                  69.5% |            0.48 |                       19.1
  worst |           60.7% |                  90.3% |            0.47 |                       34.7
```

Several things stand out. When memory is only 60% full, almost nothing fails, but when it is 80% full the choice of policy matters a great deal: best fit refuses far fewer requests than first fit, next fit does worse than first fit, and worst fit fails most of the time. Worst fit's theory (leave a big leftover) does not survive contact with a steady stream of mixed-size requests: it keeps carving the biggest holes into middling ones, so big requests soon find nothing. Best fit pays for its success in search effort (every hole examined, as the last column shows), while next fit examines the fewest holes when memory is lightly loaded, but scatters allocations and fragments the memory more. These results come from one kind of workload; other request patterns can change the ranking, which is why real allocators measure rather than assume. The `Memory` class itself was checked on 1,200 random sequences of allocations, frees, and compactions (with all four policies): the holes and blocks always tiled the memory exactly, no two holes ever touched, and each policy always chose the hole its rule names.

The *holes per block* column shows a regularity that is easy to miss: for every policy the number of holes settles at about half the number of allocated blocks (between 0.47 and 0.51 in both tables). This is the **fifty percent rule**, a classic result from Knuth's analysis of first fit; later work revisited it and found conditions under which the ratio departs from one half ([Springer: The fifty percent rule revisited](https://link.springer.com/article/10.1007/BF01932770)). It means that fragmentation is not an accident of unlucky workloads but something that dynamic allocation produces by itself: for every two blocks in memory, expect about one hole.

## 🧩 Internal Fragmentation: Rounding Up

The opposite waste appears whenever the allocator hands out units bigger than the request. Two rules are common: round up to a whole number of fixed-size units (a page of 4 KiB, say) or to the next power of two. The block below measures what each wastes, averaged over 100,000 random request sizes, once for small requests (up to 4 KiB) and once for large ones (up to 1 MiB):

```python
def waste(sizes, round_up):
    granted = [round_up(size) for size in sizes]
    return 1 - sum(sizes) / sum(granted)

def to_pages(size, page=4096):
    return -(-size // page) * page                  # round up to a multiple of the page size

def to_power_of_two(size):
    return 1 << (size - 1).bit_length()             # round up to the next power of two

rng = random.Random(3)
for label, largest in (("small requests, 1 byte to 4 KiB", 4096), ("large requests, 1 byte to 1 MiB", 1 << 20)):
    sizes = [rng.randint(1, largest) for _ in range(100_000)]
    print(f"{label}: rounding to 4 KiB pages wastes {waste(sizes, to_pages):.1%}, rounding to a power of two wastes {waste(sizes, to_power_of_two):.1%}")
```

```text
small requests, 1 byte to 4 KiB: rounding to 4 KiB pages wastes 50.0%, rounding to a power of two wastes 25.0%
large requests, 1 byte to 1 MiB: rounding to 4 KiB pages wastes 0.4%, rounding to a power of two wastes 24.9%
```

Rounding to a fixed unit wastes about half a unit per request on average, which is ruinous for requests much smaller than the unit and negligible for large ones. Rounding to a power of two wastes the same fraction, about a quarter, whether the sizes are small or large (as long as they are spread evenly over their range). Every scheme that hands out blocks in fixed or standard sizes trades the external fragmentation of the previous section for this internal waste.

## 👯 The Buddy System

The **buddy system** is a compromise that keeps splitting and merging simple. Memory is a block whose size is a power of two. To serve a request, the allocator rounds it up to a power of two (a block of *order n* has 2<sup>n</sup> units) and finds a free block of that order; if there is none, it takes a bigger free block and splits it in half, repeatedly, until it has the right size. Each half of a split is the other's **buddy**. When a block is freed and its buddy is also free, the two merge back into one bigger block, again and again. Splitting and merging are cheap because a block's buddy is found by flipping a single bit of its address ([Wikipedia: Buddy memory allocation](https://en.wikipedia.org/wiki/Buddy_memory_allocation)):

```python
class Buddy:
    """A buddy allocator over 2**top units. A block of order n has 2**n units."""

    def __init__(self, top):
        self.top = top
        self.free = {order: set() for order in range(top + 1)}
        self.free[top].add(0)                       # at the start there is one free block: all of memory
        self.allocated = {}                         # address -> order

    def allocate(self, size):
        order = max(0, (size - 1).bit_length())     # the smallest order whose block can hold `size` units
        for found in range(order, self.top + 1):    # look for the smallest free block that is big enough
            if self.free[found]:
                address = min(self.free[found])
                self.free[found].remove(address)
                while found > order:                # split: keep the lower half, put the upper half (the buddy) on the free list
                    found -= 1
                    self.free[found].add(address + (1 << found))
                self.allocated[address] = order
                return address
        return None

    def release(self, address):
        order = self.allocated.pop(address)
        while order < self.top:
            buddy = address ^ (1 << order)          # the buddy differs from this block only in bit number `order`
            if buddy not in self.free[order]:
                break
            self.free[order].remove(buddy)          # merge with the free buddy into one block of the next order
            address = min(address, buddy)
            order += 1
        self.free[order].add(address)

def free_lists(buddy):
    return {order: sorted(addresses) for order, addresses in buddy.free.items() if addresses}

buddy = Buddy(6)                                    # 2**6 = 64 units
print("start:", free_lists(buddy))
placed = {}
for name, size in (("A", 10), ("B", 5), ("C", 20), ("D", 3)):
    placed[name] = buddy.allocate(size)
    print(f"allocate {name} ({size:>2} units) -> address {placed[name]:>2}, a block of {1 << buddy.allocated[placed[name]]:>2} | free blocks by order: {free_lists(buddy)}")
for name in ("B", "D", "A", "C"):
    buddy.release(placed[name])
    print(f"release  {name}                          | free blocks by order: {free_lists(buddy)}")
```

```text
start: {6: [0]}
allocate A (10 units) -> address  0, a block of 16 | free blocks by order: {4: [16], 5: [32]}
allocate B ( 5 units) -> address 16, a block of  8 | free blocks by order: {3: [24], 5: [32]}
allocate C (20 units) -> address 32, a block of 32 | free blocks by order: {3: [24]}
allocate D ( 3 units) -> address 24, a block of  4 | free blocks by order: {2: [28]}
release  B                          | free blocks by order: {2: [28], 3: [16]}
release  D                          | free blocks by order: {4: [16]}
release  A                          | free blocks by order: {5: [0]}
release  C                          | free blocks by order: {6: [0]}
```

Follow the free lists. Allocating A (10 units) rounds up to 16 and splits the 64-unit block twice, leaving a free 16-unit buddy at address 16 and a free 32-unit buddy at 32. Requests B, C, and D are carved from those. Then the releases run the splits backwards: when D (at address 24) is released, its buddy at 28 is free, so they merge into an 8-unit block, whose buddy at 16 (the released B) is also free, giving a 16-unit block; releasing A and C finishes the job, and the free list is a single 64-unit block again. Every request wasted some space to rounding (10 units took 16), which is the price of fast merging. The allocator was stress-tested with 400 random sequences of allocations and releases: after every operation the free and allocated blocks tiled the memory exactly, every block sat at an address that is a multiple of its size, no two free buddies were left unmerged, and releasing everything restored the single 64-unit block.

Linux uses a buddy allocator for physical page frames: its page allocator keeps a per-processor cache of pages and falls back to the buddy allocator for the rest ([Linux kernel documentation: Physical Memory](https://docs.kernel.org/mm/physical_memory.html)). The kernel's own tools show it at work: the file `/proc/buddyinfo` lists, for each memory zone, how many free blocks exist at each order, which the documentation describes as a useful tool for diagnosing external fragmentation ([Linux kernel documentation: The /proc filesystem](https://docs.kernel.org/filesystems/proc.html)). On Linux you can look at it yourself:

```bash
cat /proc/buddyinfo
```

Each column counts free blocks of one order, from the smallest on the left; many small blocks and no large ones is external fragmentation.

## 🏠 Allocators Inside Programs

Everything above also applies one level up. A program does not ask the kernel for memory every time it creates an object; that would be far too slow. The kernel gives it large regions of pages, and a user-space allocator (`malloc` in C, the object allocator in Python) subdivides them. CPython, for example, serves objects of 512 bytes or less from its own small-object allocator, which takes larger regions called *arenas* from the operating system and carves them into blocks, and falls back to the general allocator for bigger requests ([Python docs: Memory Management](https://docs.python.org/3/c-api/memory.html)). Inside the kernel itself, objects of a fixed type that are created and destroyed constantly are often handled by a **slab allocator**, which keeps freed objects ready for reuse by the next request of the same type and thereby reduces fragmentation ([Wikipedia: Slab allocation](https://en.wikipedia.org/wiki/Slab_allocation)). So a memory request in a Python program passes through several layers, each with its own free lists and its own fragmentation.

## Common Misconceptions

- **"If the total free memory is large enough, the request will succeed."** Only if the free memory is in one piece. External fragmentation is exactly the case where enough memory exists in total but not in one block, as the 60-unit request showed.
- **"Best fit is the best policy."** It did fail least in the experiment, but it examines every hole, and the results depend on the workload; first fit is often nearly as good and searches less.
- **"Fragmentation is a sign of a buggy allocator."** Every allocator that hands out variable-sized blocks produces holes. The fifty percent rule shows that roughly one hole per two blocks appears even in a correct allocator.
- **"Compaction solves fragmentation."** It works but copies data, needs relocation hardware, and stops the programs being moved, so it is used sparingly.
- **"Wasted memory is always unallocated memory."** Internal fragmentation is wasted memory that *is* allocated: it is inside a block, where nobody else can use it.

## ➡️ Next

Continue to [paging.md](paging.md): the approach that removes external fragmentation altogether by dividing memory into equal pages and letting a process's pages be scattered anywhere, at the price of a translation step on every access that the hardware must make fast.
