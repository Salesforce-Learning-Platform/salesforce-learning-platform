# 🌌 What Is Virtual Memory?

## The Illusion

Every running program behaves as if it had a large, private, contiguous memory all to itself, starting wherever it likes, while many other programs share the same limited RAM. **Virtual memory** is what makes that possible: the operating system, using hardware and software together, maps the **virtual addresses** a program uses to **physical addresses** in main memory. The memory management unit (MMU) translates them automatically, and the system can extend the illusion with disk storage, so that the virtual address spaces can hold more than the physical memory does ([Wikipedia: Virtual memory](https://en.wikipedia.org/wiki/Virtual_memory)). This frees programs from managing a shared memory, lets processes share memory such as libraries, improves security because processes are isolated from one another, and lets a system use conceptually more memory than it physically has (the same article).

The mechanics of translation, pages and frames, page tables, and the translation lookaside buffer, are the subject of [paging.md](../memory-management/paging.md) in the [Memory Management](../memory-management/README.md) module. This module builds on them: this file looks at what virtual memory gives you, [page-faults.md](page-faults.md) at the event that makes it work, and [page-replacement-algorithms.md](page-replacement-algorithms.md) at what happens when memory runs short. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon); numbers that depend on the machine are labelled.

## 🗺️ Where Can a Page Be?

The page table records, for each page of a process, whether the page is in physical memory. If it is, the entry says where; if it is not, an access raises a **page fault**, and the operating system takes over ([Wikipedia: Virtual memory](https://en.wikipedia.org/wiki/Virtual_memory)). The "not there" case covers very different situations:

| State of the page | What happens when the program touches it |
|-------------------|------------------------------------------|
| In physical memory, and mapped | the access simply proceeds |
| Part of the address space, never touched, and backed by no file (**anonymous** memory) | the kernel provides a page filled with zeros |
| Backed by a file, and not mapped in yet | the kernel finds it in its cache of file pages, or reads it from the file |
| Paged out to swap, or compressed | the kernel brings the contents back |
| Not part of the address space at all | the access is invalid, and the process normally receives a segmentation fault |

Bringing pages in only when they are touched is called **demand paging**: the operating system copies a page into physical memory only when an attempt is made to access it and it is not already there, so a process starts with few of its pages in memory and faults them in as it needs them, a form of lazy loading ([Wikipedia: Demand paging](https://en.wikipedia.org/wiki/Demand_paging)). The three experiments below show the consequences.

## 🧮 Reserving Memory Is Not Using It

The first experiment asks the operating system for a gigabyte of anonymous memory with `mmap`, writes one byte into 4,000 of its pages, and watches two numbers that `ps` reports for the process: the **virtual size** (`vsz`), the size of the address space, and the **resident set size** (`rss`), the physical memory that the process is using:

```python
import mmap
import os
import subprocess

PAGE = os.sysconf("SC_PAGE_SIZE")                # 16 KiB on Apple silicon, usually 4 KiB on x86-64 Linux
MIB = 1024 * 1024

def sizes_mib():
    """Virtual size and resident set size of this process, in MiB (ps reports KiB)."""
    out = subprocess.run(["ps", "-o", "vsz=,rss=", "-p", str(os.getpid())], capture_output=True, text=True, check=True).stdout.split()
    return int(out[0]) / 1024, int(out[1]) / 1024

before = sizes_mib()
region = mmap.mmap(-1, 1024 * MIB)               # 1 GiB that no file backs
reserved = sizes_mib()
for page in range(4000):
    region[page * PAGE] = 1                      # write one byte into each of 4,000 different pages
touched = sizes_mib()
region.close()

print(f"page size: {PAGE:,} bytes")
print(f"{'(change since the start)':<27}{'virtual size':>15}{'resident size':>16}")
for label, (virtual, resident) in (("after reserving 1 GiB", reserved), ("after touching 4,000 pages", touched)):
    print(f"{label:<27}{virtual - before[0]:>+11.0f} MiB{resident - before[1]:>+12.1f} MiB")
```

One run on the test machine printed:

```
page size: 16,384 bytes
(change since the start)      virtual size   resident size
after reserving 1 GiB            +1024 MiB        +0.0 MiB
after touching 4,000 pages       +1024 MiB       +62.5 MiB
```

Reserving the gigabyte enlarged the address space by a gigabyte but did not increase the memory in use at all. Touching 4,000 pages added exactly 4,000 × 16 KiB = 62.5 MiB of resident memory: physical memory is given out **page by page, when the page is first touched**. That is why a program's virtual size says little about how much memory it uses, and why allocating a large buffer is cheap until you write to it.

## 🪞 The Same Address, a Different Memory

Virtual addresses belong to a process. After `fork`, parent and child have the same layout, so a buffer lies at the same virtual address in both, but a write by one is not seen by the other. Linux implements `fork` with **copy-on-write** pages: parent and child share the physical pages until one of them writes, so the cost of `fork` is mainly that of copying the parent's page tables ([`fork(2)`](https://man7.org/linux/man-pages/man2/fork.2.html), [Wikipedia: Copy-on-write](https://en.wikipedia.org/wiki/Copy-on-write)):

```python
import ctypes
import struct

def address_of(buffer):
    """The virtual address at which the first byte of `buffer` lies in this process."""
    return ctypes.addressof(ctypes.c_char.from_buffer(buffer))

data = mmap.mmap(-1, PAGE, flags=mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS)
data[0] = 1
address = address_of(data)

read_end, write_end = os.pipe()
child = os.fork()
if child == 0:                                   # in the child process
    data[0] = 99                                 # change "its" memory
    os.write(write_end, struct.pack("?i", address_of(data) == address, data[0]))
    os._exit(0)                                  # leave at once, without running the parent's clean-up
os.waitpid(child, 0)
same_address, child_value = struct.unpack("?i", os.read(read_end, 8))
os.close(read_end)
os.close(write_end)
print("the buffer is at the same virtual address in the child:", same_address)
print("the child sees", child_value, "| the parent still sees", data[0])
data.close()
```

```text
the buffer is at the same virtual address in the child: True
the child sees 99 | the parent still sees 1
```

The two processes use the same address, yet the child sees 99 and the parent 1. The address is only a name inside one address space; each process has its own page table, which maps that name to a physical page. Copying happened only for the page that was written ([page-faults.md](page-faults.md) counts the faults). The processes also cannot reach each other's memory by guessing addresses, because an address of one process means nothing in the other: this is the isolation that [processes-and-threads](../processes-and-threads/README.md) relies on.

## 📄 Files as Memory

Virtual memory can also back a region with a **file**: with `mmap`, the file's contents appear in memory, and pages are brought in from the file as they are touched ([Wikipedia: Memory-mapped file](https://en.wikipedia.org/wiki/Memory-mapped_file)). The mapping can be **shared**, so that writes are visible to other processes mapping the same file and are carried through to the file, or **private**, a copy-on-write view whose changes are neither visible to others nor carried through to the file ([`mmap(2)`](https://man7.org/linux/man-pages/man2/mmap.2.html)):

```python
import tempfile

with tempfile.TemporaryDirectory() as workshop:
    path = os.path.join(workshop, "notes.txt")
    with open(path, "wb") as handle:
        handle.write(b"hello, world\n")
    with open(path, "r+b") as handle:
        shared = mmap.mmap(handle.fileno(), 0, flags=mmap.MAP_SHARED)      # the whole file, appearing in memory
        print("the mapping reads:                      ", shared[:12])
        shared[:5] = b"HELLO"                                              # an ordinary write to memory ...
        shared.flush()
        with open(path, "rb") as other:
            print("read() after writing through it (shared):", other.read(12))      # ... changed the file

        private = mmap.mmap(handle.fileno(), 0, flags=mmap.MAP_PRIVATE)    # a copy-on-write view of the same file
        private[:5] = b"MINE!"
        print("the private mapping reads:              ", private[:12])
        with open(path, "rb") as other:
            print("read() after writing through it (private):", other.read(12))
        shared.close()
        private.close()
```

```text
the mapping reads:                       b'hello, world'
read() after writing through it (shared): b'HELLO, world'
the private mapping reads:               b'MINE!, world'
read() after writing through it (private): b'HELLO, world'
```

A write to the shared mapping changed the file without any `write` call; a write to the private mapping stayed in that mapping. Operating systems use exactly this machinery to load programs and libraries: the file pages can be shared between the processes that map them, and a process that modifies one gets its own copy.

## 💾 When Memory Runs Short

When free memory runs low, the system takes pages back, a job Linux calls **reclaim**. Reclaimable pages are mainly the **page cache** (cached file contents) and anonymous memory: cached file pages that have not been changed can be dropped, because the data exists on disk, while a modified anonymous page must be written to swap before its memory is reused ([Linux kernel documentation: Concepts overview](https://docs.kernel.org/admin-guide/mm/concepts.html)). Many systems also **compress** pages instead of, or before, writing them out: a page that would have been paged out is compressed and kept in RAM, or written out in compressed form, and is marked inaccessible so that an access triggers a page fault that decompresses it; Linux's `zswap` and `zram` are implementations ([Wikipedia: Virtual memory compression](https://en.wikipedia.org/wiki/Virtual_memory_compression)). Some memory is never paged out at all: pinned (or wired) pages, for example those that the page-fault handler itself needs ([Wikipedia: Virtual memory](https://en.wikipedia.org/wiki/Virtual_memory)). When the pages that the running programs are actively using no longer fit, the system can spend most of its time moving pages in and out, which is called **thrashing** and is measured in [page-replacement-algorithms.md](page-replacement-algorithms.md).

## Common Misconceptions

- **"Virtual memory is the same thing as swap space."** Virtual memory is the whole arrangement of translating each process's addresses; swap is only one of the places where a page that is not in memory can be.
- **"Allocating memory uses up RAM."** Reserving address space uses almost none; physical pages are given out as they are first touched.
- **"`fork` copies the whole memory of the parent."** With copy-on-write, a page is copied when one of the two processes writes to it.
- **"Two processes that use the same address see the same data."** Each has its own address space; the same number can refer to different physical pages.
- **"A memory-mapped file always writes your changes to disk."** Only a shared mapping does; changes through a private mapping stay private.

## ➡️ Next

Continue to [page-faults.md](page-faults.md): what actually happens when a program touches a page that is not there, how many faults ordinary operations cause, and what they cost.
