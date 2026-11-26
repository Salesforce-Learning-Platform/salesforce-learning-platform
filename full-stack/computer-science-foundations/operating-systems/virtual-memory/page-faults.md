# ⚡ Page Faults

## What Happens When a Page Is Not There

A **page fault** is an exception that the memory management unit raises when a process accesses a memory page without the necessary preparation: a mapping has to be added to the process's address space, and the contents of the page may also have to be loaded, for example from disk. The MMU detects the fault, but the operating system's kernel handles it, either by making the page accessible in physical memory or by denying an illegal access ([Wikipedia: Page fault](https://en.wikipedia.org/wiki/Page_fault)). A fault is therefore not an error by itself: valid faults are common, and they are how virtual memory does its work. There are three kinds (the same article):

- A **minor** (soft) fault: the page's contents are already in memory (for example because another program has brought a shared page in), so the kernel only has to update the page table; nothing is read from disk.
- A **major** (hard) fault: the contents are not in memory and must be loaded from disk. The kernel must first find a frame, a free one or, when memory is scarce, one that holds another page, whose contents must be written out first if they have been modified.
- An **invalid** fault: the address is not part of the process's address space (a null pointer is the usual example, because the page at address 0 is deliberately not mapped). The kernel passes a segmentation fault to the process, which usually terminates it.

What the kernel does for a fault that is not invalid:

1. The MMU cannot complete the translation, or the access breaks the page's permissions, so it raises an exception and the CPU enters the kernel.
2. The kernel checks its records of the process's memory regions: is the address part of the address space, and is this kind of access allowed? If not, the process receives a signal (an invalid fault).
3. If it is allowed, the kernel finds the contents of the page: a page of zeros, a page already in its file cache, or data in a file or in swap.
4. It takes a free frame. If none is free, a [replacement algorithm](page-replacement-algorithms.md) chooses a page to give up, writing it out first if it has been modified.
5. If data has to come from disk, the process waits and the CPU runs something else.
6. The kernel updates the page table, and the faulting instruction runs again, this time successfully.

All code was run on CPython 3.9 on a Mac (macOS, Apple silicon); the counts and times below depend on the machine and are labelled.

## 🔢 Counting Faults

The kernel counts a process's faults: `getrusage` reports `ru_minflt`, the faults handled without any disk activity, and `ru_majflt`, the faults that needed it ([`getrusage(2)`](https://man7.org/linux/man-pages/man2/getrusage.2.html)). The next block writes to 4,000 pages of a fresh anonymous region and then writes to them again, and does the same for reading first and writing afterwards:

```python
import mmap
import os
import resource
import time

PAGE = os.sysconf("SC_PAGE_SIZE")

def fault_counts():
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return usage.ru_minflt, usage.ru_majflt              # handled without I/O, and with I/O

def touch(region, pages, write=True):
    """Touch one byte in each of `pages` pages; return (minor faults, major faults, microseconds per page, sum read)."""
    minor, major = fault_counts()
    total = 0
    start = time.perf_counter()
    for page in range(pages):
        if write:
            region[page * PAGE] = 1
        else:
            total += region[page * PAGE]
    elapsed = time.perf_counter() - start
    after_minor, after_major = fault_counts()
    return after_minor - minor, after_major - major, elapsed / pages * 1e6, total

PAGES = 4000
def report(label, result):
    minor, major, microseconds, total = result
    print(f"{label:<22} minor faults {minor:>5,}   major {major}   {microseconds:5.2f} microseconds per page")

region = mmap.mmap(-1, PAGES * PAGE)
report("first write", touch(region, PAGES))
report("second write", touch(region, PAGES))
region.close()

region = mmap.mmap(-1, PAGES * PAGE)
first_read = touch(region, PAGES, write=False)
report("first read", first_read)
report("write after the read", touch(region, PAGES))
print("sum of the bytes in the first read:", first_read[3])
region.close()
```

One run on the test machine printed:

```
first write            minor faults 4,000   major 0    0.72 microseconds per page
second write           minor faults     0   major 0    0.04 microseconds per page
first read             minor faults 4,000   major 0    0.66 microseconds per page
write after the read   minor faults     0   major 0    0.07 microseconds per page
sum of the bytes in the first read: 0
```

The first pass faulted once for every page and the second not at all: after the first touch the page is mapped, and the program reads and writes it at memory speed. The difference in time per page is the cost of the faults (the Python loop itself accounts for most of the time of a pass with no faults). Reading a fresh page faults too, and what it reads is **zero** (the sum is 0): anonymous memory starts out zero-filled, so no process ever sees another's leftovers. On this Mac the write that followed the read caused no further fault. On Linux the behaviour is different: for anonymous memory, a first *read* maps a special shared page filled with zeros, and a real page is allocated only when the program *writes* ([Linux kernel documentation: Concepts overview](https://docs.kernel.org/admin-guide/mm/concepts.html)), so read-then-write costs two faults per page there.

## 🪞 Copy-on-Write Faults

[what-is-virtual-memory.md](what-is-virtual-memory.md) showed that a child's write does not change the parent's memory. The faults show how: a page is copied when it is first written. The parent writes 2,000 pages, and then forks; the child reads them all, writes to 500 of them, and writes to the same 500 again:

```python
import struct

PARENT_PAGES = 2000
region = mmap.mmap(-1, PARENT_PAGES * PAGE, flags=mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS)
touch(region, PARENT_PAGES)                                 # the parent now has 2,000 written pages

read_end, write_end = os.pipe()
child = os.fork()
if child == 0:
    reading = touch(region, PARENT_PAGES, write=False)[0]
    writing = touch(region, 500)[0]                         # the first write to 500 pages
    rewriting = touch(region, 500)[0]                       # the same 500 once more
    os.write(write_end, struct.pack("iii", reading, writing, rewriting))
    os._exit(0)
os.waitpid(child, 0)
reading, writing, rewriting = struct.unpack("iii", os.read(read_end, 12))
os.close(read_end)
os.close(write_end)
print(f"child reads all {PARENT_PAGES:,} pages:   {reading:>5,} faults")
print(f"child writes 500 of them:     {writing:>5,} faults")
print(f"child writes them again:      {rewriting:>5,} faults")
region.close()
```

One run on the test machine printed:

```
child reads all 2,000 pages:   2,041 faults
child writes 500 of them:       500 faults
child writes them again:          0 faults
```

The first write to each of the 500 pages cost one fault, in which the kernel made a private copy; the second write cost nothing. The reads are interesting: on this Mac the child also took about one minor fault for each page that it only read, which suggests that the child's mappings are set up as it touches them. Linux copies the parent's page tables during `fork` ([`fork(2)`](https://man7.org/linux/man-pages/man2/fork.2.html)), so a child there can read the parent's resident pages without faulting. Either way, the parent's data was never copied for pages the child did not write.

## 📄 Faults on a File Mapping

Pages of a mapped file also arrive by faulting. The next block writes a file of 1,000 pages, maps it, and reads one byte of each page twice. Because the file has just been written, its contents are still in the operating system's file cache, so the faults are minor:

```python
import tempfile

with tempfile.TemporaryDirectory() as workshop:
    path = os.path.join(workshop, "data.bin")
    with open(path, "wb") as handle:
        handle.write(os.urandom(1000 * PAGE))
    with open(path, "rb") as handle:
        view = mmap.mmap(handle.fileno(), 0, prot=mmap.PROT_READ)
        report("file, first read", touch(view, 1000, write=False))
        report("file, second read", touch(view, 1000, write=False))
        view.close()
```

One run on the test machine printed:

```
file, first read       minor faults 1,000   major 0    0.54 microseconds per page
file, second read      minor faults     0   major 0    0.05 microseconds per page
```

If the file's pages had not been cached, the same first read would have caused major faults, with a disk read each (or one read for several pages, because systems read ahead). That case is not reproduced here, since forcing data out of the cache needs administrator rights.

## 💰 What a Fault Costs

A minor fault costs a trip into the kernel and some bookkeeping. A major fault waits for a disk. The difference matters because memory is so fast: the [Wikipedia article on page faults](https://en.wikipedia.org/wiki/Page_fault) gives about 8 ms to service a page from a hard disk, a 30 microsecond read for a fast solid-state drive, and memory accesses of well under a microsecond (70 ns in its solid-state example). The **effective access time** with a fault rate *p* is (1 − *p*) × memory time + *p* × fault time:

```python
def effective_access_ns(p, memory_ns, fault_ns):
    """The average time of a memory access when a fraction p of the accesses fault."""
    return (1 - p) * memory_ns + p * fault_ns

MEMORY_NS = 70
DEVICES = {"hard disk (8 ms)": 8_000_000, "solid-state drive (30 us)": 30_000}
print(f"{'faults per access':>17} | " + " | ".join(f"{name:>26}" for name in DEVICES))
for p in (0, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3):
    cells = [f"{effective_access_ns(p, MEMORY_NS, fault):>10,.0f} ns ({effective_access_ns(p, MEMORY_NS, fault) / MEMORY_NS:>7.1f}x)"
             for fault in DEVICES.values()]
    print(f"{p:>17.0e} | " + " | ".join(f"{cell:>26}" for cell in cells))
for name, fault_ns in DEVICES.items():
    limit = 0.10 * MEMORY_NS / (fault_ns - MEMORY_NS)        # the largest fault rate with at most a 10% slowdown
    print(f"{name}: for a slowdown of at most 10%, fewer than 1 fault in {1 / limit:,.0f} accesses")
```

```text
faults per access |           hard disk (8 ms) |  solid-state drive (30 us)
            0e+00 |           70 ns (    1.0x) |           70 ns (    1.0x)
            1e-07 |           71 ns (    1.0x) |           70 ns (    1.0x)
            1e-06 |           78 ns (    1.1x) |           70 ns (    1.0x)
            1e-05 |          150 ns (    2.1x) |           70 ns (    1.0x)
            1e-04 |          870 ns (   12.4x) |           73 ns (    1.0x)
            1e-03 |        8,070 ns (  115.3x) |          100 ns (    1.4x)
hard disk (8 ms): for a slowdown of at most 10%, fewer than 1 fault in 1,142,847 accesses
solid-state drive (30 us): for a slowdown of at most 10%, fewer than 1 fault in 4,276 accesses
```

With a hard disk, one fault in a thousand accesses makes the average access more than a hundred times slower, and keeping the slowdown within 10% needs fewer than one major fault in about 1.1 million accesses; the solid-state drive is more forgiving but still needs fewer than one in about 4,300. This is why programs with good **locality** ([memory-management-basics.md](../memory-management/memory-management-basics.md)) run well and why a system that is short of memory can slow to a crawl.

## 🚫 When the Access Is Invalid

When the fault is invalid, UNIX-like systems report it to the program with a signal such as `SIGSEGV`, and unless the program handles it, the default action usually ends the process ([Wikipedia: Page fault](https://en.wikipedia.org/wiki/Page_fault)). This lesson does not trigger one: it would crash the interpreter and leave crash reports behind. You can watch the kernel's side of the check safely, though: a system call that is *given* a bad address fails with the error `EFAULT` instead of crashing anything, as the experiment in [kernel-and-user-mode.md](../introduction-to-operating-systems/kernel-and-user-mode.md) shows.

## 🧰 Making Faults Cheaper or Fewer

- **Locality.** Walking through memory in order touches fewer pages at a time than jumping around, so fewer faults (and TLB misses) happen for the same work.
- **Read-ahead and prefaulting.** Kernels read nearby file pages before they are asked for. On Linux, `MAP_POPULATE` asks `mmap` to populate the page tables immediately, which for a file mapping also reads ahead, so the program does not stop for faults later ([`mmap(2)`](https://man7.org/linux/man-pages/man2/mmap.2.html)).
- **Keeping the actively used pages in memory.** This is what replacement algorithms and the idea of the working set, in the next lesson, are about.

## Common Misconceptions

- **"A page fault means something went wrong."** Most faults are valid and routine; only an invalid fault is an error.
- **"Every page fault reads the disk."** A minor fault involves no disk access at all.
- **"Fresh memory contains random leftovers."** Anonymous memory given to a process starts out filled with zeros (the experiment read a sum of 0).
- **"`fork` is expensive because it copies all of memory."** Pages are copied one at a time, when written to; the cost is moved to the later faults.

## ➡️ Next

Continue to [page-replacement-algorithms.md](page-replacement-algorithms.md): when a fault needs a frame and none is free, which page should go?
