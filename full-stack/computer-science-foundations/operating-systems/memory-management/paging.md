# 📄 Paging

## Fixed-Size Pieces Instead of Variable Blocks

[memory-allocation.md](memory-allocation.md) ended with a problem: when blocks of different sizes come and go, memory fills up with holes that are too small to use, and the cure, compaction, is expensive. **Paging** removes the problem by removing the variable sizes. Physical memory is divided into equal-sized pieces called **frames**, and each process's logical address space is divided into pieces of the same size called **pages**. The MMU maps pages to frames, any page can sit in any frame, and the process still sees one contiguous range of addresses ([Wikipedia: Memory management (operating systems)](https://en.wikipedia.org/wiki/Memory_management_(operating_systems))). A page is the smallest unit the operating system manages in a virtual-memory system, and a frame is the physical block into which a page is placed ([Wikipedia: Page (computer memory)](https://en.wikipedia.org/wiki/Page_(computer_memory))).

Because every frame is the same size, *any* free frame can hold *any* page, so external fragmentation cannot happen: there are no holes that are too small. The remaining waste is **internal**: a process rarely needs an exact number of pages, so its last page is usually partly empty. The price of the arrangement is that every memory access now needs a translation from page to frame, and the rest of this file is about how to make that translation correct, small, and fast. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon); the simulations are deterministic, and the machine-dependent values are labelled.

## ✂️ Splitting an Address

Page sizes are powers of two, which makes the arithmetic trivial. With a page size of 4,096 bytes (2<sup>12</sup>), the low 12 bits of a logical address are the **offset** within the page, and the remaining high bits are the **page number**. Translation replaces the page number with a frame number and keeps the offset unchanged, because a page and a frame are the same size. The mapping lives in the process's **page table**, a data structure the operating system keeps for each process, in which each mapping is a **page table entry** (PTE) ([Wikipedia: Page table](https://en.wikipedia.org/wiki/Page_table)). Besides the frame number, an entry holds control bits, such as a *present* bit that says whether the page is in physical memory and a *dirty* bit that records whether it has been modified (the same article). The simulation below implements the lookup, adding a *writable* bit to show protection:

```python
import random
from collections import OrderedDict

class PageFault(Exception):
    pass

class PageTable:
    """One process's mapping from page numbers to frame numbers."""

    def __init__(self, page_size):
        assert page_size & (page_size - 1) == 0, "page sizes are powers of two"
        self.page_size = page_size
        self.offset_bits = page_size.bit_length() - 1
        self.entries = {}                           # page number -> (frame number, writable)

    def map(self, page, frame, writable=True):
        self.entries[page] = (frame, writable)

    def translate(self, virtual_address, write=False):
        page = virtual_address >> self.offset_bits                    # the high bits select the page ...
        offset = virtual_address & (self.page_size - 1)               # ... the low bits are the position inside it
        if page not in self.entries:
            raise PageFault(f"page {page} is not mapped (virtual address {virtual_address:#x})")
        frame, writable = self.entries[page]
        if write and not writable:
            raise PageFault(f"page {page} is read-only (virtual address {virtual_address:#x})")
        return (frame << self.offset_bits) | offset                   # the frame replaces the page; the offset is kept

table = PageTable(4096)
for page, frame in {0: 7, 1: 2, 2: 9, 3: 4}.items():
    table.map(page, frame, writable=(page != 0))    # page 0 holds code, so it is read-only
for virtual in (0x0000, 0x0ABC, 0x1000, 0x2FFF, 0x3123):
    physical = table.translate(virtual)
    print(f"virtual {virtual:#06x} -> page {virtual >> 12}, offset {virtual & 0xFFF:#05x} -> frame {physical >> 12} -> physical {physical:#07x}")
for virtual, write in ((0x4000, False), (0x0010, True)):
    try:
        table.translate(virtual, write)
    except PageFault as fault:
        print("fault:", fault)
```

```text
virtual 0x0000 -> page 0, offset 0x000 -> frame 7 -> physical 0x07000
virtual 0x0abc -> page 0, offset 0xabc -> frame 7 -> physical 0x07abc
virtual 0x1000 -> page 1, offset 0x000 -> frame 2 -> physical 0x02000
virtual 0x2fff -> page 2, offset 0xfff -> frame 9 -> physical 0x09fff
virtual 0x3123 -> page 3, offset 0x123 -> frame 4 -> physical 0x04123
fault: page 4 is not mapped (virtual address 0x4000)
fault: page 0 is read-only (virtual address 0x10)
```

The process sees pages 0 to 3 laid out one after another, but they sit in frames 7, 2, 9, and 4, scattered through physical memory; the offsets (`0xabc`, `0xfff`, `0x123`) pass through unchanged. Two accesses fail, for different reasons: page 4 has no entry (the address is not part of the process's memory at all), and a *write* to page 0 is refused because the page is read-only. On a real machine both raise a hardware exception that the kernel handles, and for an invalid access it normally sends the process a segmentation-fault signal ([Wikipedia: Page table](https://en.wikipedia.org/wiki/Page_table)). The same table can serve for sharing: if two processes' tables map one of their pages to the same frame, the processes share that memory, which is how one copy of a library's code is used by many programs, and how `fork` can start a child without copying (the copy-on-write idea of [what-is-a-process.md](../processes-and-threads/what-is-a-process.md): shared frames are marked read-only, and the first write triggers a fault that gives the writer a private copy).

When the kernel switches from one process to another, it also switches the page table in use, which is part of the memory-management information stored in each process's control block ([context-switching.md](../processes-and-threads/context-switching.md)).

## 🌳 How Big Is a Page Table? Multi-Level Tables

A flat table has one entry for every page of the address space, whether or not the process uses it. Current x86-64 processors use 48 bits of each virtual address, which gives a 256 TiB address space ([Wikipedia: x86-64](https://en.wikipedia.org/wiki/X86-64)). With 4 KiB pages that is 2<sup>36</sup> pages, and at 8 bytes per entry a flat table would take 512 GiB, per process, to describe a program that may use a few dozen megabytes. The solution is to build the table as a **tree**: a few small tables that each cover a block of virtual memory, linked together by a master table, with lower-level tables created only when the process actually uses the addresses they cover ([Wikipedia: Page table](https://en.wikipedia.org/wiki/Page_table)). In x86-64 there are four levels, and a full hierarchy for the whole 48-bit space would take a little more than 512 GiB, which is why none is ever built in full ([Wikipedia: x86-64](https://en.wikipedia.org/wiki/X86-64)).

The code below builds a four-level table, with 9 bits of the address indexing each level (so each table has 512 entries of 8 bytes, exactly one 4 KiB page), and maps a realistic sparse process: 2 MiB of program code near the bottom of the address space, a 64 MiB heap, and an 8 MiB stack near the top:

```python
class MultiLevelPageTable:
    """A tree of tables: each level is indexed by 9 bits of the page number, as in x86-64."""

    def __init__(self, level_bits=(9, 9, 9, 9), page_bits=12):
        self.level_bits, self.page_bits = level_bits, page_bits
        self.root = {}
        self.tables = 1                             # the top-level table exists from the start

    def _indexes(self, virtual_address):
        page_number = virtual_address >> self.page_bits
        indexes = []
        for bits in reversed(self.level_bits):      # peel off the lowest bits first: they index the lowest level
            indexes.append(page_number & ((1 << bits) - 1))
            page_number >>= bits
        return list(reversed(indexes))

    def map(self, virtual_address, frame):
        *upper, last = self._indexes(virtual_address)
        node = self.root
        for index in upper:
            if index not in node:
                node[index] = {}
                self.tables += 1                    # a new lower-level table must be allocated
            node = node[index]
        node[last] = frame

    def translate(self, virtual_address):
        *upper, last = self._indexes(virtual_address)
        node = self.root
        for index in upper:
            if index not in node:
                raise PageFault(f"no table covers address {virtual_address:#x}")
            node = node[index]
        if last not in node:
            raise PageFault(f"page not mapped at address {virtual_address:#x}")
        return (node[last] << self.page_bits) | (virtual_address & ((1 << self.page_bits) - 1))

process = MultiLevelPageTable()
regions = {"program code, 2 MiB": (0x0000_0000_0040_0000, 2 << 20),
           "heap, 64 MiB": (0x0000_0000_1000_0000, 64 << 20),
           "stack, 8 MiB": (0x0000_7FFF_FF80_0000, 8 << 20)}
frame = 0
for name, (start, length) in regions.items():
    for address in range(start, start + length, 4096):
        process.map(address, frame)
        frame += 1
print(f"pages mapped: {frame:,} ({frame * 4 // 1024} MiB) | table pages needed: {process.tables} ({process.tables * 4} KiB)")
flat_entries = 1 << 36
print(f"a flat table for the same 48-bit address space: {flat_entries:,} entries x 8 bytes = {flat_entries * 8 // 2**30} GiB")
print("a page inside the heap translates to frame", process.translate(0x0000_0000_1000_2345) >> 12)
try:
    process.translate(0x0000_0000_4000_0000)         # an address in the unused middle of the address space
except PageFault as fault:
    print("fault:", fault)
```

```text
pages mapped: 18,944 (74 MiB) | table pages needed: 42 (168 KiB)
a flat table for the same 48-bit address space: 68,719,476,736 entries x 8 bytes = 512 GiB
a page inside the heap translates to frame 514
fault: no table covers address 0x40000000
```

The process uses 74 MiB through nearly 19,000 pages, and describing it takes 42 small tables (168 KiB) instead of 512 GiB. The empty middle of the address space costs nothing: no table exists for it, and an access there fails at the first missing level. The price is time: finding a mapping now means following one pointer per level, four memory accesses for a four-level table, before the access to the data itself. That cost would make everything several times slower if it had to be paid on every access, which brings us to the hardware that avoids it.

The simulators in this file were checked against independent references: `PageTable` against ordinary arithmetic (frame number times page size plus offset) on 5,000 random addresses and page sizes, with faults exactly where expected; the multi-level table against a plain dictionary on 10,000 random mappings, with unmapped pages faulting; and the TLB simulation against a straightforward list-based least-recently-used cache on 300 random traces. In every case they agreed.

## ⚡ The TLB: Making Translation Fast

The MMU keeps a small, very fast cache of recently used translations, the **translation lookaside buffer** (TLB). On every access the TLB is searched first. A **TLB hit** supplies the frame immediately; a **TLB miss** forces a **page walk** through the page table, and the result is stored in the TLB so that the next access to the same page hits ([Wikipedia: Page table](https://en.wikipedia.org/wiki/Page_table)). The TLB is small (the first-level data TLB of Intel's Nehalem processors, for example, holds 64 entries for 4 KiB pages, according to [Wikipedia: Translation lookaside buffer](https://en.wikipedia.org/wiki/Translation_lookaside_buffer)), so what matters is the **hit rate**, and that depends on locality, the property measured in [memory-management-basics.md](memory-management-basics.md).

The simulation below runs three address traces through a 16-entry TLB with least-recently-used replacement: a scan through a 4 MiB array 8 bytes at a time, a loop that revisits the same 8 pages, and random reads over 1,000 pages. It then computes the **effective access time** with illustrative figures that are not measurements: 1 ns to consult the TLB, 100 ns per memory access, and a four-level walk (four extra memory accesses) on each miss:

```python
def tlb_hit_rate(trace, entries, page_bits=12):
    tlb = OrderedDict()                             # least recently used entry first
    hits = 0
    for address in trace:
        page = address >> page_bits
        if page in tlb:
            hits += 1
            tlb.move_to_end(page)
        else:
            tlb[page] = True
            if len(tlb) > entries:
                tlb.popitem(last=False)             # evict the least recently used translation
    return hits / len(trace)

rng = random.Random(11)
traces = {
    "scan a 4 MiB array, 8 bytes at a time": list(range(0, 4 << 20, 8)),
    "loop over the same 8 pages again and again": [(i % 8) * 4096 + 100 for i in range(100_000)],
    "random reads over 1,000 pages": [rng.randrange(1000) * 4096 for _ in range(100_000)],
}
tlb_ns, memory_ns, walk_levels = 1, 100, 4
for name, trace in traces.items():
    hit = tlb_hit_rate(trace, entries=16)
    effective = tlb_ns + memory_ns + (1 - hit) * walk_levels * memory_ns
    print(f"{name:<45} hit rate {hit:7.2%} | effective access time {effective:6.1f} ns")
```

```text
scan a 4 MiB array, 8 bytes at a time         hit rate  99.80% | effective access time  101.8 ns
loop over the same 8 pages again and again    hit rate  99.99% | effective access time  101.0 ns
random reads over 1,000 pages                 hit rate   1.54% | effective access time  494.8 ns
```

When the access pattern has locality, nearly every translation comes from the TLB, and the cost of paging is only 1% to 2% (101 to 102 ns instead of 100 ns). The scan misses only once per page, because the 512 accesses within a 4 KiB page all share one translation; the loop fits entirely in the TLB. Random access over more pages than the TLB holds misses almost every time, and each access then costs nearly five times as much. This is the same effect as the shuffled-list experiment in [memory-management-basics.md](memory-management-basics.md), seen from the translation side, and it is why larger pages (which let the same number of TLB entries cover more memory) are attractive for programs with huge working sets.

## 📏 How Big Should a Page Be?

Page size is a trade-off with three sides ([Wikipedia: Page (computer memory)](https://en.wikipedia.org/wiki/Page_(computer_memory))). Smaller pages mean more pages and so a larger page table. Larger pages mean more wasted space in each process's last page (internal fragmentation), but let a TLB of a given size cover more memory, and make disk transfers more efficient. A simple model captures the first two forces. For a process of size *s* with *e* bytes per table entry, the table costs *s·e/p* for pages of size *p*, and the waste in the last page averages *p/2*; the total is smallest when *p* is near the square root of *2·s·e*. The table evaluates the model for a 100 MiB process with 8-byte entries:

```python
def human(n):
    for unit in ("B", "KiB", "MiB", "GiB"):
        if n < 1024 or unit == "GiB":
            return f"{n:,.0f} {unit}" if n == int(n) else f"{n:,.1f} {unit}"
        n /= 1024

process_size, entry_size = 100 * 2**20, 8
rows = []
for exponent in range(10, 22):                      # page sizes from 1 KiB to 2 MiB
    page = 2 ** exponent
    pages = -(-process_size // page)
    table = pages * entry_size
    waste = page / 2
    rows.append((page, pages, table, waste, table + waste))
cheapest = min(rows, key=lambda row: row[4])
print(f"{'page size':>9} | {'pages':>8} | {'page table':>10} | {'average waste':>13} | {'total overhead':>14}")
for page, pages, table, waste, total in rows:
    print(f"{human(page):>9} | {pages:>8,} | {human(table):>10} | {human(waste):>13} | {human(total):>14}" + ("  <- smallest" if (page, pages, table, waste, total) == cheapest else ""))
print(f"the formula's best page size: {human((2 * process_size * entry_size) ** 0.5)}")
```

```text
page size |    pages | page table | average waste | total overhead
    1 KiB |  102,400 |    800 KiB |         512 B |      800.5 KiB
    2 KiB |   51,200 |    400 KiB |         1 KiB |        401 KiB
    4 KiB |   25,600 |    200 KiB |         2 KiB |        202 KiB
    8 KiB |   12,800 |    100 KiB |         4 KiB |        104 KiB
   16 KiB |    6,400 |     50 KiB |         8 KiB |         58 KiB
   32 KiB |    3,200 |     25 KiB |        16 KiB |         41 KiB  <- smallest
   64 KiB |    1,600 |   12.5 KiB |        32 KiB |       44.5 KiB
  128 KiB |      800 |    6.2 KiB |        64 KiB |       70.2 KiB
  256 KiB |      400 |    3.1 KiB |       128 KiB |      131.1 KiB
  512 KiB |      200 |    1.6 KiB |       256 KiB |      257.6 KiB
    1 MiB |      100 |      800 B |       512 KiB |      512.8 KiB
    2 MiB |       50 |      400 B |         1 MiB |        1.0 MiB
the formula's best page size: 40 KiB
```

Tiny pages drown the process in table entries; huge ones waste memory in the last page, and the total is lowest in between, near the figure the formula predicts. Real systems do not choose one size for everything: processors typically support a standard small page (4 KiB on most PCs, 16 KiB on Apple silicon, as the next lines show) plus a few much larger ones, called *huge pages* on Linux, *superpages* on FreeBSD, and *large pages* on Windows, for programs with large, dense memory use ([Wikipedia: Page (computer memory)](https://en.wikipedia.org/wiki/Page_(computer_memory))). Programs can ask the system for the page size in effect:

```python
import mmap
import os

print("page size from sysconf:", os.sysconf("SC_PAGE_SIZE"), "bytes | from the mmap module:", mmap.PAGESIZE, "bytes")
```

One run on the test machine printed:

```
page size from sysconf: 16384 bytes | from the mmap module: 16384 bytes
```

On a Unix-like system the command `getconf PAGESIZE` reports the same number from a shell. Even a one-byte allocation made directly from the operating system, for example with `mmap`, takes a whole page of the process's address space: the system call works in whole pages, and every page that contains any part of a requested range is mapped or unmapped together ([Linux man page: `mmap(2)`](https://man7.org/linux/man-pages/man2/mmap.2.html)).

## Common Misconceptions

- **"Paging eliminates fragmentation."** It eliminates *external* fragmentation. Internal fragmentation remains: on average half a page per allocation, as the page-size model shows.
- **"One page table serves the whole machine."** Each process has its own, which is what gives each its own address space; the kernel switches tables when it switches processes.
- **"Address translation costs one extra memory access."** Without a TLB, a four-level table costs four extra accesses; the TLB makes that cost vanish only when the program has locality.
- **"A page and a frame are the same thing."** A page is a block of *virtual* addresses; a frame is a block of *physical* memory. The page table connects them, and the two are the same size.
- **"Bigger pages are always better."** They shrink tables and improve TLB reach but waste memory and make sharing and protection coarser; that is why systems offer several sizes.

## ➡️ Next

Continue to [segmentation.md](segmentation.md): the other classic scheme, which divides a process into logical segments of different sizes (code, data, stack), each with its own base, limit, and permissions, and which explains where the name of the segmentation fault comes from.
