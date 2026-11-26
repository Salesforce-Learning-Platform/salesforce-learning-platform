# 🧠 Memory Management Basics

## Why Memory Needs a Manager

Main memory (RAM) is a long row of numbered bytes, and every running program needs some of it: its code, its variables, its stack, the data it is working on. A computer runs many programs at once, each of which was written without knowing about the others, and RAM is finite, while the programs together may want more than there is. Someone has to decide who gets which bytes, keep programs out of each other's memory, and take the memory back when a program ends. That someone is the **memory management** function of the operating system: it keeps track of the state of every memory location (allocated or free), decides which processes receive memory, when, and how much, and updates its records when memory is released ([Wikipedia: Memory management (operating systems)](https://en.wikipedia.org/wiki/Memory_management_(operating_systems))).

It helps to separate two layers that share the name. The operating system hands out memory to *processes*. Inside each process, the program (or its language runtime, such as Python's) then decides how to use what it was given, carving it up among its own objects; that second layer is *application* memory management. This module is about the first layer, the kernel's, and about the hardware that makes it possible. Every code example was run on CPython 3.9 on a Mac (macOS, Apple silicon); where output depends on the machine, the text says so, and the code runs unchanged on Linux.

## 🧾 The Five Jobs of a Memory Manager

| Job | What it means | Where this module covers it |
|-----|---------------|-----------------------------|
| **Allocation** | Choose which free memory to give a process, and take it back when the process releases it or ends | [memory-allocation.md](memory-allocation.md) |
| **Address translation (relocation)** | Let a program use its own addresses while the hardware maps them to wherever the program really sits in RAM | This file, then [paging.md](paging.md) and [segmentation.md](segmentation.md) |
| **Protection** | Stop a process from reading or writing memory that is not its own, and the kernel's memory from being touched at all | This file, [paging.md](paging.md), [segmentation.md](segmentation.md) |
| **Sharing** | Let processes deliberately use the same physical memory, for example one copy of a library's code | [paging.md](paging.md), [segmentation.md](segmentation.md) |
| **Using more than fits** | Keep the parts of a program that are not needed right now out of RAM | The [Virtual Memory](../virtual-memory/README.md) module |

## 🪜 The Memory Hierarchy

Fast memory is small and expensive; large memory is slow and cheap. Computers resolve this by stacking several kinds, each level typically smaller and faster than the one below it. The memory hierarchy separates storage by response time, from the processor's registers and caches, through main memory, down to disks and other mass storage ([Wikipedia: Memory hierarchy](https://en.wikipedia.org/wiki/Memory_hierarchy)):

| Level | Role | Size | Speed |
|-------|------|------|-------|
| **Registers** | The values the processor is working with right now | Bytes to kilobytes | Fastest |
| **Caches** | Copies of recently used memory, kept close to the processor | Kilobytes to megabytes | Very fast |
| **Main memory (RAM)** | What running programs live in | Gigabytes | Fast, but far slower than a cache |
| **Disk or flash storage** | Files, and the overflow of RAM | Hundreds of gigabytes and more | Much slower still |

The system works because programs are predictable. **Locality of reference** is the tendency of a processor to use the same memory locations repeatedly over a short time (temporal locality) and to use locations close to ones it just used (spatial locality), with the traversal of an array as the typical case ([Wikipedia: Locality of reference](https://en.wikipedia.org/wiki/Locality_of_reference)). Caches, prefetching, and, as later files show, the operating system's own paging policies all bet on it. The next experiment shows how much the bet is worth. It adds up the same four million numbers twice: once visiting the list positions in order, once in a shuffled order, so that exactly the same work is done and only the order of the memory accesses differs:

```python
import random
import time

N = 4_000_000
data = list(range(N))
in_order = list(range(N))
shuffled = in_order[:]
random.Random(1).shuffle(shuffled)

def walk(order):
    start = time.perf_counter()
    total = sum(map(data.__getitem__, order))
    return time.perf_counter() - start, total

in_order_time, in_order_sum = min(walk(in_order) for _ in range(3))
shuffled_time, shuffled_sum = min(walk(shuffled) for _ in range(3))
print("both orders give the same sum:", in_order_sum == shuffled_sum)
print(f"visiting the items in order:        {in_order_time * 1000:6.0f} ms")
print(f"visiting the items in random order: {shuffled_time * 1000:6.0f} ms  ({shuffled_time / in_order_time:.1f} times slower)")
```

One run on the test machine printed:

```
both orders give the same sum: True
visiting the items in order:            49 ms
visiting the items in random order:    463 ms  (9.5 times slower)
```

The arithmetic and the amount of data are identical; the only change is the order, and it costs several times as much. In order, each access lands next to the previous one, so the cache line that was just fetched already holds the next few items, the hardware can guess what comes next, and the address translations for the page are already at hand. In random order, almost every access lands somewhere new and must travel down the hierarchy towards RAM. Memory is called *random access* because any location takes the same logical effort to name, but that does not make every access equally fast. The practical rule, which reappears throughout this module and in [paging.md](paging.md), is that **keeping related data close together and using it together is faster than scattering it**.

## 🏷️ Logical and Physical Addresses

A program cannot know in advance where in RAM it will be loaded, because that depends on what else is running. If programs used raw physical addresses, two programs written to use the same locations would corrupt each other, and moving a program would break it. So programs use **logical** (or *virtual*) addresses, numbered from zero in the program's own address space (see [what-is-a-process.md](../processes-and-threads/what-is-a-process.md)), and a piece of hardware, the **memory management unit** (MMU), examines every memory reference and translates the logical address to a **physical** address in RAM ([Wikipedia: Memory management unit](https://en.wikipedia.org/wiki/Memory_management_unit)). The operating system sets up the translation; the hardware performs it on every access, which is what makes protection enforceable: an address with no valid translation never reaches RAM.

The simplest scheme, used by early systems and still the clearest way to see the idea, is **base and limit** (also called base and bounds). Two registers describe where the process lives: the **base** is the physical address where its memory begins, and the **limit** is its size. The hardware compares every logical address with the limit, and if the address is in range, adds the base. The simulation below models that hardware for two processes, then moves one:

```python
class ProtectionFault(Exception):
    pass

class BaseLimitMMU:
    """The hardware of the simplest scheme: check a logical address against the limit, then add the base."""
    def __init__(self, base, limit):
        self.base, self.limit = base, limit

    def translate(self, logical):
        if not 0 <= logical < self.limit:
            raise ProtectionFault(f"logical address {logical} is outside this process's memory (0 to {self.limit - 1})")
        return self.base + logical

process_a = BaseLimitMMU(base=40_000, limit=8_000)
process_b = BaseLimitMMU(base=90_000, limit=20_000)
print("logical address 100 in A is physical", process_a.translate(100))
print("logical address 100 in B is physical", process_b.translate(100))
try:
    process_a.translate(8_000)                      # one byte past the end of A's memory
except ProtectionFault as fault:
    print("fault:", fault)
process_a.base = 10_000                             # the OS moves A to another place in RAM; A is not told
print("after the move, logical address 100 in A is physical", process_a.translate(100))
```

```text
logical address 100 in A is physical 40100
logical address 100 in B is physical 90100
fault: logical address 8000 is outside this process's memory (0 to 7999)
after the move, logical address 100 in A is physical 10100
```

Three results matter. Two processes can use the same logical address and reach different physical memory, which is what isolation means. An address outside the limit is refused by the hardware before any memory is touched (on a real machine that is the exception the kernel turns into a fault, as in [kernel-and-user-mode.md](../introduction-to-operating-systems/kernel-and-user-mode.md)). And **relocation is cheap**: to move a process, the kernel copies its memory and changes one register; the program's addresses never change. That ability becomes essential when [memory-allocation.md](memory-allocation.md) discusses compaction.

Base and limit has a weakness: each process must occupy one contiguous block of RAM, and blocks of different sizes coming and going leave the memory full of unusable gaps. Early systems that used base and bounds addressing developed into the two schemes that replace it, segmentation and paging ([Wikipedia: Memory management unit](https://en.wikipedia.org/wiki/Memory_management_unit)): [segmentation.md](segmentation.md) gives each logical part of a program (code, data, stack) its own base and limit, and [paging.md](paging.md) breaks memory into small fixed-size pieces that need not be contiguous at all.

## 🔭 What a Process Sees: Virtual Size and Resident Size

Two numbers describe a process's memory in tools such as `ps`, `top`, and Activity Monitor, and they mean very different things. The **virtual size** is how much address space the process has mapped or reserved. The **resident size** is how much of it is currently held in physical RAM. A fresh child process makes the difference clear, because it can measure itself before and after it writes 200 MiB of data into a block:

```python
import os
import subprocess
import sys

CHILD = '''
import os, subprocess
def sizes():
    vsz, rss = subprocess.run(["ps", "-o", "vsz=,rss=", "-p", str(os.getpid())], capture_output=True, text=True).stdout.split()
    return f"virtual {int(vsz) // 1024:>9,} MiB | resident {int(rss) // 1024:>5,} MiB"
print("at start:               ", sizes())
block = bytearray(b"\\x01") * (200 * 1024 * 1024)       # 200 MiB, every byte written
print("holding 200 MiB of data:", sizes())
'''
print(subprocess.run([sys.executable, "-c", CHILD], capture_output=True, text=True).stdout, end="")

page = os.sysconf("SC_PAGE_SIZE")
pages = os.sysconf("SC_PHYS_PAGES")
print(f"this machine: {pages * page / 2**30:.0f} GiB of RAM, in {pages:,} frames of {page // 1024} KiB")
```

One run on the test machine printed:

```
at start:                virtual   477,288 MiB | resident    15 MiB
holding 200 MiB of data: virtual   477,488 MiB | resident   215 MiB
this machine: 18 GiB of RAM, in 1,179,648 frames of 16 KiB
```

The resident size rose by about 200 MiB, because the data is now really in RAM. The virtual size is a different kind of number: it counts address space, not RAM, and it can be many times larger than the machine's memory, as the figure for the start of the program shows (the exact values depend on the operating system, and macOS in particular reports a very large virtual size; on Linux a small Python process typically reports far less). A large virtual size alone is therefore no sign of trouble; the resident size, together with how much the system is paging, says more about real pressure on RAM. The last line also introduces the unit the kernel manages memory in: RAM is divided into fixed-size **frames** (here 16 KiB on Apple silicon, commonly 4 KiB on x86 PCs), the subject of [paging.md](paging.md).

## 🗺️ Where the Rest of the Module Goes

The file you are reading set the stage. The next three look at how the five jobs are done in practice:

- [memory-allocation.md](memory-allocation.md): how the kernel (and every allocator above it) chooses a block when memory is divided into contiguous pieces, why holes appear, and how first-fit, best-fit, worst-fit, next-fit, and the buddy system compare.
- [paging.md](paging.md): memory divided into small fixed-size pages and frames, page tables, multi-level tables, and the translation cache that makes it fast.
- [segmentation.md](segmentation.md): memory divided along the program's own logical lines, with a base, a limit, and permissions for each part.

## Common Misconceptions

- **"Memory management only means handing out RAM."** Allocation is one of five jobs; address translation, protection, and sharing are just as central, and they are why programs can run safely side by side.
- **"Programs use real RAM addresses."** Programs use logical addresses; the MMU translates each access, so the same logical address in two processes can lead to different physical memory.
- **"RAM is random access, so the order I read it in does not matter."** Any location can be named equally easily, but access time depends on whether the data is already in a cache, as the shuffled-order experiment showed.
- **"A huge virtual size means the program is using huge amounts of memory."** Virtual size counts address space; resident size counts the RAM actually occupied.
- **"The operating system decides how every object in my program is placed."** It supplies pages; deciding where individual objects go inside them is the job of the program's own allocator.

## ➡️ Next

Continue to [memory-allocation.md](memory-allocation.md): when memory is handed out in blocks of different sizes, how does the manager choose, and what happens to the gaps that are left?
