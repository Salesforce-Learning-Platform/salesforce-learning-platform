# ✂️ Segmentation

## Memory in the Programmer's Terms

[paging.md](paging.md) divides memory into equal pieces that have nothing to do with what a program contains: a page boundary may fall in the middle of a function or an array. **Segmentation** takes the opposite view and divides memory along the program's own logical lines. A **segment** is a variable-sized area that corresponds to a natural unit, such as the program's code, a data table, the stack, or a shared library ([Wikipedia: Memory segmentation](https://en.wikipedia.org/wiki/Memory_segmentation)). An address is no longer a single number but a pair, a **segment** and an **offset** inside it, and the hardware translates the pair to a physical address. Each segment has a length and a set of permissions (read, write, execute). A reference is allowed only if the offset is within the segment's length and the kind of access is permitted; otherwise the hardware raises an exception, a segmentation fault being the best-known one (the same article).

Segmentation was invented to let system software isolate processes and their data, in order to make systems that run many processes more reliable (the same article). It is also the only classic memory management technique that does *not* present the program with one linear, contiguous address space; the program, or its compiler, deals in segments ([Wikipedia: Memory management (operating systems)](https://en.wikipedia.org/wiki/Memory_management_(operating_systems))). This file models the hardware, compares it with paging, shows how the two are combined, and traces what survives of segmentation in today's systems. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon); the simulations are deterministic.

## 🧮 The Segment Table

The operating system keeps a **segment table** for each process, with one entry per segment: the **base** (the physical address where the segment starts), the **limit** (its length), and the permissions. It is exactly the base-and-limit scheme of [memory-management-basics.md](memory-management-basics.md), but with one pair per segment instead of one pair per process. The simulation below gives two processes the same program: they share one code segment (the same physical memory, read and execute only) and each has its own data and stack:

```python
class SegmentationFault(Exception):
    pass

class SegmentTable:
    """One process's segments: name -> (base, limit, permissions)."""

    def __init__(self):
        self.segments = {}

    def add(self, name, base, limit, permissions):
        self.segments[name] = (base, limit, permissions)

    def translate(self, segment, offset, access="r"):
        if segment not in self.segments:
            raise SegmentationFault(f"no segment named {segment!r}")
        base, limit, permissions = self.segments[segment]
        if not 0 <= offset < limit:                 # the hardware checks the offset against the segment's length ...
            raise SegmentationFault(f"offset {offset} is outside segment {segment!r} (length {limit})")
        if access not in permissions:               # ... and the kind of access against the segment's permissions
            raise SegmentationFault(f"segment {segment!r} does not allow access {access!r} (permissions {permissions!r})")
        return base + offset

shared_code = (1000, 400, "rx")                     # one copy of the program's code in physical memory
process_a, process_b = SegmentTable(), SegmentTable()
process_a.add("code", *shared_code)
process_a.add("data", 5000, 200, "rw")
process_a.add("stack", 9000, 300, "rw")
process_b.add("code", *shared_code)
process_b.add("data", 7000, 500, "rw")
process_b.add("stack", 12000, 300, "rw")

for label, table, segment, offset, access in (("A", process_a, "code", 10, "x"), ("B", process_b, "code", 10, "x"),
                                              ("A", process_a, "data", 10, "w"), ("B", process_b, "data", 10, "w"),
                                              ("A", process_a, "stack", 299, "r")):
    print(f"process {label}: {segment:>5} offset {offset:>3} ({access}) -> physical {table.translate(segment, offset, access)}")
for label, table, segment, offset, access in (("A", process_a, "code", 10, "w"), ("A", process_a, "data", 200, "r"), ("B", process_b, "heap", 0, "r")):
    try:
        table.translate(segment, offset, access)
    except SegmentationFault as fault:
        print(f"process {label}: fault: {fault}")
```

```text
process A:  code offset  10 (x) -> physical 1010
process B:  code offset  10 (x) -> physical 1010
process A:  data offset  10 (w) -> physical 5010
process B:  data offset  10 (w) -> physical 7010
process A: stack offset 299 (r) -> physical 9299
process A: fault: segment 'code' does not allow access 'w' (permissions 'rx')
process A: fault: offset 200 is outside segment 'data' (length 200)
process B: fault: no segment named 'heap'
```

The first five lines show translation and sharing. Both processes execute the instruction at offset 10 of their code segment, and both reach physical address 1010: one copy of the code serves them both. Their data segments, which both address at offset 10, lead to different places (5010 and 7010). The last three lines show protection. Writing to the code segment is refused, because the segment allows only reading and executing; offset 200 of a segment 200 units long is one past the end; and a segment that does not exist cannot be named. Each check is applied to a *logical* unit, which is segmentation's great strength: a code segment can be made read-only and executable as a whole, and a data segment can be made non-executable, without any page-by-page bookkeeping.

## ⚖️ Segmentation and Paging Compared

| | Segmentation | Paging |
|--|--------------|--------|
| **Unit** | A logical part of the program, of any length | A fixed-size block, unrelated to the program's structure |
| **Visible to the program** | Yes: addresses are (segment, offset) pairs | No: the program sees one linear address space |
| **Fragmentation** | External: variable-sized segments need contiguous holes of the right size | Internal: only the last page of each region is partly empty |
| **Table size** | Small: a few entries per process | Large: an entry per page (multi-level tables keep it manageable) |
| **Protection and sharing** | Natural: a whole code segment or library is shared or protected as one unit | Per page, with the same effect but more bookkeeping |
| **Growing a region** | Needs a larger contiguous hole, or the segment must move | A new page can be added anywhere |

Wikipedia puts the contrast briefly: paged systems break main memory into equal-sized blocks, while segmented systems generally allow blocks of varying size ([Wikipedia: Memory management unit](https://en.wikipedia.org/wiki/Memory_management_unit)). When a segment must be loaded, the system has to find enough contiguous free memory for all of it, so fragmentation results when memory has enough free space in total but not in one place ([Wikipedia: Memory segmentation](https://en.wikipedia.org/wiki/Memory_segmentation)); this is the problem of [memory-allocation.md](memory-allocation.md) all over again.

## 🤝 Segmentation With Paging

Since each scheme has what the other lacks, they can be combined: keep the logical segments for protection and sharing, but build each segment out of pages. The entry for a segment then holds not a base address but the address of a **page table for that segment**, and the segment can grow by adding another page to its table ([Wikipedia: Memory segmentation](https://en.wikipedia.org/wiki/Memory_segmentation)). The hardware of the Multics system, for which the GE-645 computer was designed in 1964, supported segmentation together with paging (the same article). The sketch below models one such paged segment: the check against the segment's length comes first, then the page table of the segment finishes the translation, and the segment grows by one page:

```python
PAGE = 4096

class PagedSegment:
    """A segment of `length` bytes whose memory is a list of frames, one per page, scattered anywhere in RAM."""

    def __init__(self, length, frames):
        self.length, self.frames = length, list(frames)

    def translate(self, offset):
        if not 0 <= offset < self.length:           # the segment's limit is still enforced ...
            raise SegmentationFault(f"offset {offset} is outside the segment (length {self.length})")
        return self.frames[offset // PAGE] * PAGE + offset % PAGE   # ... and the page table places the rest

    def grow(self, extra, new_frames):
        self.length += extra
        self.frames.extend(new_frames)

heap = PagedSegment(10_000, [21, 5, 14])             # 10,000 bytes need three 4 KiB pages
for offset in (0, 4095, 4096, 9999):
    physical = heap.translate(offset)
    print(f"heap offset {offset:>5} -> frame {physical // PAGE:>2}, physical address {physical}")
try:
    heap.translate(10_000)
except SegmentationFault as fault:
    print("fault:", fault)
heap.grow(4_000, [33])                              # one more page, taken from anywhere in physical memory
print("after growing by 4,000 bytes: offset 13999 ->", heap.translate(13_999))
```

```text
heap offset     0 -> frame 21, physical address 86016
heap offset  4095 -> frame 21, physical address 90111
heap offset  4096 -> frame  5, physical address 20480
heap offset  9999 -> frame 14, physical address 59151
fault: offset 10000 is outside the segment (length 10000)
after growing by 4,000 bytes: offset 13999 -> 136879
```

The segment is 10,000 bytes long, yet its three pages live in frames 21, 5, and 14, nowhere near one another, so it needed no contiguous hole; growing it needed only one more frame, from anywhere. The limit check keeps the segment's logical boundary exact (offset 10,000 faults even though the third page has room to spare), which paging alone cannot do. This combination gives the programmer the logical view and the operating system the freedom of fixed-size pieces.

## 🖥️ What Is Left of Segmentation Today

Most of today's systems use a **flat** address space and rely on paging for protection. The 32-bit x86 architecture offered real segmentation, allowing a process up to 16,383 segments of up to 4 GiB each ([Wikipedia: Memory management (operating systems)](https://en.wikipedia.org/wiki/Memory_management_(operating_systems))), but operating systems for it generally set up segments that cover the whole address space and left protection to the paging hardware. The 64-bit x86-64 architecture goes further: in 64-bit mode it does not support segmentation at all. Four of the segment registers (CS, SS, DS, and ES) are forced to base 0 with the maximum limit, while FS and GS keep a usable base address, which operating systems use for special purposes such as **thread-local storage** ([Wikipedia: Memory segmentation](https://en.wikipedia.org/wiki/Memory_segmentation)), the per-thread data of [what-is-a-thread.md](../processes-and-threads/what-is-a-thread.md).

The *idea* of segments survives in software. Executable files are organised into segments that tell the kernel how to map the file into a new process's address space, each with its own protection. On macOS, the `size` command lists them for a program (on Linux, `readelf -lW` shows the equivalent program headers):

```bash
size -m /bin/ls | grep '^Segment'
```

One run on the test machine (macOS, Apple silicon) printed:

```
Segment __PAGEZERO: 4294967296 (zero fill)
Segment __TEXT: 32768
Segment __DATA_CONST: 16384
Segment __DATA: 16384
Segment __LINKEDIT: 32768
```

The `__TEXT` segment holds the program's code and constant data and is read-only, so the kernel can map it once and share it among all the processes running the program; `__DATA` holds the writable data ([Apple: Mach-O executables](https://developer.apple.com/library/archive/documentation/Performance/Conceptual/CodeFootprint/Articles/MachOOverview.html)). The first entry, `__PAGEZERO`, is a segment of 4 GiB (4,294,967,296 bytes) with no file contents and *no access permissions at all*: any access to it causes a page fault, and its purpose is to catch invalid null pointers ([Wikipedia: Mach-O](https://en.wikipedia.org/wiki/Mach-O)). That is the mechanism behind the null-pointer fault described in [kernel-and-user-mode.md](../introduction-to-operating-systems/kernel-and-user-mode.md): address 0 leads into a region the hardware refuses to touch. The name "segmentation fault" goes back to exactly this idea of a program's segments: it refers to violating the program's segmentation, for example by reading outside its address space or writing to a read-only segment. On systems with hardware segmentation the fault comes from the segment checks of this file; on systems that use only paging, an access to an invalid page generally ends as a segmentation fault too, because both are faults raised by the virtual memory system ([Wikipedia: Segmentation fault](https://en.wikipedia.org/wiki/Segmentation_fault)).

## Common Misconceptions

- **"A segmentation fault means the computer uses segmentation."** The name refers to violating a program's segments (its address space, its read-only code). On systems that use only paging, an invalid page access still ends as a segmentation fault: the hardware refused a memory access and the kernel signalled the process.
- **"Segments and pages are rival systems; a computer uses one or the other."** They can be combined, with each segment built from pages, as in the Multics design.
- **"A segment is just a big page."** A segment has a logical meaning (the code, the stack), a length that can be any value, and its own permissions; a page is an arbitrary fixed-size piece.
- **"Segmentation is obsolete and irrelevant."** The hardware mostly is, in 64-bit mode, but the segment ideas (separate regions for code, data, and stack, each with its own permissions, one shared copy of code) are everywhere in executable formats and process layouts, and the register that points at thread-local storage is a segment register.
- **"Segmentation protects better than paging."** Both enforce protection; segmentation expresses it per logical unit and paging per fixed-size piece, which usually ends up equivalent once a segment is a whole number of pages.

## ➡️ Next

This completes the tour of memory management: where memory is divided into pieces (allocation), how pieces are mapped (paging and segmentation), and how the hardware keeps it fast and safe. The [Virtual Memory](../virtual-memory/README.md) module of this section builds directly on paging: if a page table entry can say "not present", the kernel can keep some pages on disk, which lets a process use more memory than the machine has and load a program lazily.
