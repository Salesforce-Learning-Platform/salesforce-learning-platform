# 🌌 Virtual Memory

## 📚 Overview

Your computer runs hundreds of programs, each of which behaves as if it had a large memory of its own, and together they often use more memory than the machine has. **Virtual memory** is the arrangement that makes this possible: the operating system and the memory management unit translate every address a program uses, so that each process gets a private address space, memory is handed out only when it is touched, pages can be shared or copied lazily, files can be read as if they were memory, and pages that are not needed can be moved out of the way. It also has a price, paid in **page faults**, and a failure mode, **thrashing**, that can make a whole system crawl.

The module starts with what virtual memory gives you, with experiments that show that reserving memory is not using it, that two processes can see different data at the same address, and how shared and private file mappings differ. It then looks closely at the **page fault**: what the kernel does, the difference between minor, major, and invalid faults, how many faults ordinary operations cause (copy-on-write included), and what faults cost, with a calculation of the effective access time. It ends with **page replacement**: FIFO, LRU, Clock, and the optimal algorithm as simulators, Bélády's anomaly and the stack property, workloads on which different policies win or fail, and a simulation of thrashing with its characteristic cliff. Every code example was run on CPython 3.9 on a Mac (macOS, Apple silicon); machine-dependent results are labelled, the simulations are deterministic, and each simulator was checked against an independent reference on thousands of random inputs.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain what virtual memory gives programs and the operating system (isolation, sharing, lazy loading, and the use of more memory than is physically present), and the different states a page can be in.
- Tell reserved memory from resident memory, and explain demand paging, copy-on-write after `fork`, and the difference between shared and private file mappings.
- Describe how a page fault is handled, distinguish minor, major, and invalid faults, and count a process's faults with `getrusage`.
- Calculate the effective access time with page faults, and the highest fault rate that keeps a slowdown within a given limit.
- Simulate FIFO, LRU, Clock, and the optimal algorithm, explain Bélády's anomaly and the stack property, and show why no replacement policy is best on every workload.
- Explain thrashing and working sets, and say which remedies address the cause.

## 📋 Prerequisites

- [Memory Management](../memory-management/README.md), especially [paging.md](../memory-management/paging.md): pages and frames, page tables, and the translation lookaside buffer, which this module builds on.
- [Processes and Threads](../processes-and-threads/README.md): what a process and its address space are, and `fork`.
- [Introduction to Operating Systems](../introduction-to-operating-systems/README.md): system calls and kernel and user mode.
- Basic Python reading ability: functions, classes, dictionaries, and the standard library.
- No earlier knowledge of virtual memory is assumed.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [what-is-virtual-memory.md](what-is-virtual-memory.md) | The illusion and its benefits, the states a page can be in, reserved versus resident memory, the same address in two processes, shared and private file mappings, and what happens when memory runs short |
| [page-faults.md](page-faults.md) | What a page fault is and how it is handled, minor, major, and invalid faults, counting faults for first touches, copy-on-write and file mappings, and effective access time |
| [page-replacement-algorithms.md](page-replacement-algorithms.md) | FIFO, LRU, Clock, OPT, and approximations, Bélády's anomaly and the stack property, workloads that separate the policies (including a two-list policy), and thrashing with the working set |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [page-replacement-algorithms.md](page-replacement-algorithms.md) first if you are preparing for exams or interviews: counting faults for a reference string under FIFO, LRU, and the optimal algorithm, Bélády's anomaly, and thrashing are the standard questions, and running the simulators on your own strings is the fastest way to learn them. [page-faults.md](page-faults.md) has the effective-access-time calculation, another standard question.

**Skim** [what-is-virtual-memory.md](what-is-virtual-memory.md) if you already know how paging works, but run its first experiment, because the difference between reserved and resident memory explains many surprising memory reports.

## 🧠 Knowledge Check

<details>
<summary>A memory access takes 100 ns, and servicing a major page fault takes 8 ms. What fraction of accesses may fault if the average access is to be at most 10% slower than memory?</summary>

With fault rate *p*, the effective access time is (1 − *p*) × 100 ns + *p* × 8,000,000 ns, and it must be at most 110 ns. Solving 100 + *p* × (8,000,000 − 100) ≤ 110 gives *p* ≤ 10 / 7,999,900, about 1.25 × 10⁻⁶: at most about **one fault in 800,000 accesses**. A program with poor locality, or a system short of memory, can easily exceed that, which is why paging to a slow disk is so noticeable. [page-faults.md](page-faults.md) repeats the calculation with 70 ns memory for a hard disk and a solid-state drive.

</details>

<details>
<summary>For the reference string 1 2 3 4 1 2 5 1 2 3 4 5, FIFO faults 9 times with 3 frames and 10 times with 4 frames. What is this called, why can LRU never behave this way, and does it mean that adding memory is a bad idea?</summary>

It is **Bélády's anomaly**: with more frames, FIFO caused more faults. LRU cannot show it because it has the **stack property**: with *N* frames it holds exactly the *N* most recently used pages, which are always among the *N* + 1 most recently used pages that it would hold with one frame more, so every hit with *N* frames is also a hit with *N* + 1. (On this string LRU faults 10 times with 3 frames and 8 times with 4.) The anomaly does not make memory a bad idea: it shows that a poor policy can behave strangely, and when the working sets of the running programs no longer fit, adding memory (or running fewer programs) is exactly what cures thrashing, as [page-replacement-algorithms.md](page-replacement-algorithms.md) shows.

</details>

## 📚 References

- [Wikipedia: Virtual memory](https://en.wikipedia.org/wiki/Virtual_memory), [Demand paging](https://en.wikipedia.org/wiki/Demand_paging), [Page fault](https://en.wikipedia.org/wiki/Page_fault), [Copy-on-write](https://en.wikipedia.org/wiki/Copy-on-write), [Memory-mapped file](https://en.wikipedia.org/wiki/Memory-mapped_file), and [Virtual memory compression](https://en.wikipedia.org/wiki/Virtual_memory_compression): the concepts.
- [Wikipedia: Page replacement algorithm](https://en.wikipedia.org/wiki/Page_replacement_algorithm), [Bélády's anomaly](https://en.wikipedia.org/wiki/B%C3%A9l%C3%A1dy%27s_anomaly), [Thrashing](https://en.wikipedia.org/wiki/Thrashing_(computer_science)), and [Working set](https://en.wikipedia.org/wiki/Working_set): replacement and its failure modes.
- [Linux kernel documentation: Concepts overview](https://docs.kernel.org/admin-guide/mm/concepts.html) and [Multi-Gen LRU](https://docs.kernel.org/admin-guide/mm/multigen_lru.html), and the Linux manual pages [`mmap(2)`](https://man7.org/linux/man-pages/man2/mmap.2.html), [`fork(2)`](https://man7.org/linux/man-pages/man2/fork.2.html), and [`getrusage(2)`](https://man7.org/linux/man-pages/man2/getrusage.2.html): how a real system does it.
- [Python docs: `mmap`](https://docs.python.org/3/library/mmap.html) and [`resource`](https://docs.python.org/3/library/resource.html): the tools used in the experiments.
- *Operating Systems: Three Easy Pieces*, free chapters: [Beyond Physical Memory: Mechanisms](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-beyondphys.pdf), [Beyond Physical Memory: Policies](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-beyondphys-policy.pdf), and [Complete Virtual Memory Systems](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-complete.pdf).
- [GeeksforGeeks: Virtual Memory in Operating System](https://www.geeksforgeeks.org/operating-systems/virtual-memory-in-operating-system/), [Page Fault Handling](https://www.geeksforgeeks.org/computer-organization-architecture/page-fault-handling/), [Page Replacement Algorithms](https://www.geeksforgeeks.org/operating-systems/page-replacement-algorithms-in-operating-systems/), [Belady's Anomaly](https://www.geeksforgeeks.org/operating-systems/beladys-anomaly-in-page-replacement-algorithms/), and [Techniques to Handle Thrashing](https://www.geeksforgeeks.org/operating-systems/techniques-to-handle-thrashing/): overviews and practice questions.

## ➡️ Continue Your Learning Path

This is the last module of the Operating Systems section. Return to the [section index](../README.md) to review the path or revisit a module, and keep the ideas here in mind wherever a program's memory use or speed surprises you: the question to ask is which pages it is touching, and whether they are in memory. Then continue to the [Database Management Systems section](../../database-management-systems/README.md).
