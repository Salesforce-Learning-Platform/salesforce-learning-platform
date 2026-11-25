# 🧠 Memory Management

## 📚 Overview

Every running program needs memory, memory is finite, and the programs sharing a computer cannot be trusted to stay out of each other's way. **Memory management** is the part of the operating system, together with a piece of hardware called the memory management unit, that solves this: it decides who gets which memory, lets each program use its own addresses while the hardware maps them to real RAM, and refuses every access that a program has no right to make. Almost every performance and reliability question about memory, from why a program is mysteriously slow when it walks through data in the wrong order to what a segmentation fault actually is, comes back to the ideas in this module.

The module starts with what memory management is for: its five jobs, the memory hierarchy and the locality of reference that makes it work (with a measurement showing the same arithmetic running about ten times slower in a bad access order), logical versus physical addresses, and the base-and-limit hardware that makes relocation and protection possible. It then follows the history of how memory is divided up: **contiguous allocation** and its placement policies (first, next, best, and worst fit, compared on thousands of simulated requests), internal and external fragmentation, compaction, and the buddy system that Linux uses for physical pages; **paging**, which removes external fragmentation, with a page-table simulator, multi-level tables that describe a sparse address space in kilobytes instead of hundreds of gigabytes, a TLB simulator, and the page-size trade-off; and **segmentation**, which divides memory along the program's own lines, and how it is combined with paging and what is left of it in today's processors. Every code example was run on CPython 3.9 on a Mac (macOS, Apple silicon); the simulations are deterministic, machine-dependent values are labelled, and the allocators and translation tables were checked against independent reference implementations on thousands of random inputs.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- List the jobs of a memory manager (allocation, address translation, protection, sharing, and extending memory beyond RAM) and distinguish logical from physical addresses.
- Describe the memory hierarchy, explain locality of reference, and predict how the order of memory accesses changes the speed of a program.
- Explain how base-and-limit hardware translates and protects addresses, and why it makes relocation cheap.
- Compare the first-fit, next-fit, best-fit, and worst-fit placement policies, and explain external fragmentation, internal fragmentation, compaction, and the fifty percent rule.
- Describe how the buddy system splits and merges blocks, and where it is used.
- Split a virtual address into page number and offset, translate it through a page table, and explain page faults and protection bits.
- Calculate the size of a flat page table, explain how multi-level tables shrink it for sparse address spaces, and describe the translation lookaside buffer, hit rate, and effective access time.
- Explain the trade-offs in choosing a page size.
- Describe segmentation (segment and offset, base, limit, and permissions), compare it with paging, explain segmentation with paging, and say what remains of segmentation in modern systems, including the origin of the name "segmentation fault".

## 📋 Prerequisites

- [Introduction to Operating Systems](../introduction-to-operating-systems/README.md): the kernel, user and kernel mode, and system calls.
- [Processes and Threads](../processes-and-threads/README.md): especially what a process and its address space are, which this module explains how the hardware provides.
- Basic Python reading ability: classes, dictionaries, loops, and the standard library.
- Comfort with powers of two and, ideally, hexadecimal numbers and bit shifts; the paging file uses them throughout.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [memory-management-basics.md](memory-management-basics.md) | The five jobs of a memory manager, the memory hierarchy and a locality-of-reference experiment, logical and physical addresses, a base-and-limit simulator, and virtual versus resident size |
| [memory-allocation.md](memory-allocation.md) | Partitions, holes, and the four placement policies compared on simulated workloads, external and internal fragmentation, compaction, the buddy system, and allocators inside programs |
| [paging.md](paging.md) | Pages and frames, address translation with a page-table simulator, multi-level page tables, the TLB with hit rates and effective access time, and the page-size trade-off |
| [segmentation.md](segmentation.md) | Segments with base, limit, and permissions, sharing and protection, comparison with paging, segmentation combined with paging, and segments in modern systems |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [paging.md](paging.md) first if you are preparing for interviews or for the Virtual Memory module: splitting an address into page number and offset, the size of a page table, and the TLB with its effective access time are the standard exam and interview questions, and everything in virtual memory builds on them. [memory-allocation.md](memory-allocation.md) is the place to look for fragmentation, the placement policies, and the buddy system.

**Skim** [segmentation.md](segmentation.md) if you only need the exam-level contrast with paging (read its comparison table), and treat [memory-management-basics.md](memory-management-basics.md) as the foundation to read once, with its locality experiment worth running on your own machine, because the size of the effect surprises most people.

## 🧠 Knowledge Check

<details>
<summary>A 200-unit memory has 105 units free in total, split into holes of 30, 50, and 25 units, and a request for 60 units fails. What is this problem called, and what are two ways to deal with it?</summary>

It is **external fragmentation**: enough memory is free in total, but not in one contiguous piece. One cure is **compaction**: slide the allocated blocks together so that the holes merge into one, which works because the base register of each moved process can simply be updated, but it costs a copy of every block that moves (95 units in the example in [memory-allocation.md](memory-allocation.md)). The other is to stop requiring contiguous memory: **paging** divides memory into equal frames so that any free frame can hold any page, which removes external fragmentation entirely and leaves only internal fragmentation in each process's last page ([paging.md](paging.md)). A placement policy that fragments less, such as best fit in the experiment, reduces the problem but cannot remove it.

</details>

<details>
<summary>With 4 KiB pages, a process executes a load from virtual address 0x2FFF, and its page table maps page 2 to frame 9. What physical address does the hardware access, and what does the TLB do for the next access to the same page?</summary>

A 4 KiB page has a 12-bit offset, so the low 12 bits of the address, `0xFFF`, are the offset and the remaining bits, `0x2`, are the page number. The page table maps page 2 to frame 9, so the physical address is frame 9 followed by the same offset: `0x9FFF` (the worked example in [paging.md](paging.md) translates `0x2fff` to `0x09fff` the same way). The MMU stores the translation (page 2 → frame 9) in the **TLB**, so the next access to any address in that page finds it there (a TLB hit) and skips the walk through the page table, which in a four-level table would cost four extra memory accesses.

</details>

## 📚 References

- [Wikipedia: Memory management (operating systems)](https://en.wikipedia.org/wiki/Memory_management_(operating_systems)), [Memory management unit](https://en.wikipedia.org/wiki/Memory_management_unit), [Memory hierarchy](https://en.wikipedia.org/wiki/Memory_hierarchy), and [Locality of reference](https://en.wikipedia.org/wiki/Locality_of_reference): what memory management is, the hardware behind it, and why access order matters.
- [Wikipedia: Fragmentation (computing)](https://en.wikipedia.org/wiki/Fragmentation_(computing)), [Buddy memory allocation](https://en.wikipedia.org/wiki/Buddy_memory_allocation), and [Slab allocation](https://en.wikipedia.org/wiki/Slab_allocation), plus the paper [The fifty percent rule revisited](https://link.springer.com/article/10.1007/BF01932770) (BIT Numerical Mathematics): allocation strategies and fragmentation.
- [Wikipedia: Page (computer memory)](https://en.wikipedia.org/wiki/Page_(computer_memory)), [Page table](https://en.wikipedia.org/wiki/Page_table), [Translation lookaside buffer](https://en.wikipedia.org/wiki/Translation_lookaside_buffer), and [x86-64](https://en.wikipedia.org/wiki/X86-64): paging, page tables, the TLB, and a real four-level design.
- [Wikipedia: Memory segmentation](https://en.wikipedia.org/wiki/Memory_segmentation), [Segmentation fault](https://en.wikipedia.org/wiki/Segmentation_fault), and [Mach-O](https://en.wikipedia.org/wiki/Mach-O), with [Apple's overview of Mach-O executables](https://developer.apple.com/library/archive/documentation/Performance/Conceptual/CodeFootprint/Articles/MachOOverview.html): segmentation, segmentation faults, and the segments of a real executable.
- [Linux kernel documentation: Physical Memory](https://docs.kernel.org/mm/physical_memory.html) and [The /proc filesystem](https://docs.kernel.org/filesystems/proc.html) (`/proc/buddyinfo`), and the Linux manual page [`mmap(2)`](https://man7.org/linux/man-pages/man2/mmap.2.html): how a real kernel allocates and maps memory.
- [Python docs: Memory Management (C API)](https://docs.python.org/3/c-api/memory.html), [`mmap`](https://docs.python.org/3/library/mmap.html), and [`os.sysconf`](https://docs.python.org/3/library/os.html#os.sysconf): Python's allocator and the tools used in the experiments.
- *Operating Systems: Three Easy Pieces*, free chapters: [The Abstraction: Address Spaces](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-intro.pdf), [Mechanism: Address Translation](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-mechanism.pdf), [Segmentation](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-segmentation.pdf), [Free-Space Management](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-freespace.pdf), [Paging: Introduction](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-paging.pdf), [Paging: Faster Translations (TLBs)](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-tlbs.pdf), and [Paging: Smaller Tables](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-smalltables.pdf).
- [GeeksforGeeks: Memory Management in Operating System](https://www.geeksforgeeks.org/operating-systems/memory-management-in-operating-system/), [Partition Allocation Methods](https://www.geeksforgeeks.org/operating-systems/partition-allocation-methods-in-memory-management/), [Buddy System](https://www.geeksforgeeks.org/operating-systems/buddy-system-memory-allocation-technique/), [Paging](https://www.geeksforgeeks.org/operating-systems/paging-in-operating-system/), [Multilevel Paging](https://www.geeksforgeeks.org/operating-systems/multilevel-paging-in-operating-system/), [TLB in Paging](https://www.geeksforgeeks.org/operating-systems/translation-lookaside-buffer-tlb-in-paging/), [Segmentation](https://www.geeksforgeeks.org/operating-systems/segmentation-in-operating-system/), and [Paging vs. Segmentation](https://www.geeksforgeeks.org/operating-systems/difference-between-paging-and-segmentation/): overviews and practice questions.

## ➡️ Continue Your Learning Path

Continue to the [CPU Scheduling module](../cpu-scheduling/README.md), the next module in this section: with memory divided and protected, the kernel still has to decide which ready process gets the processor next, and why first-come-first-served, shortest-job-first, round-robin, and priority scheduling suit different goals. The Virtual Memory module then returns to paging to show how page tables let a process use more memory than the machine has.
