# 🖥️ Operating Systems

## 📚 Overview

An operating system shares one computer among many programs. It decides which program runs on the processor and for how long, which memory each program may use, where data lives on the disk, and what every program is allowed to touch. This section builds that picture one module at a time. It starts with what an operating system is and how programs talk to it, follows a program from creation to exit, shows how memory is divided and the processor is scheduled, examines how programs that share data go wrong (and how to stop them), and ends with the file system that keeps data alive between runs.

Every module follows the same pattern. Its README gives an overview, learning objectives, prerequisites, a table of lessons, advice on what to deep-dive and what to skim, knowledge-check questions with answers, and references. The lessons then explain one idea at a time with runnable Python experiments, small simulators, and measurements, and each ends by clearing up common misconceptions. Every code example was run on CPython 3.9 on a Mac (macOS, Apple silicon); results that depend on the machine are labelled, and the lessons say where something is specific to macOS or Linux.

## 🧭 The Learning Path

Work through the modules in this order. The last column lists the earlier modules that each one relies on, so you can also jump in where you need to.

| # | Module | The question it answers | Builds on |
|---|--------|-------------------------|-----------|
| 1 | [Introduction to Operating Systems](introduction-to-operating-systems/README.md) | What does an operating system do, how do programs ask it for services, and how is a kernel built? | Basic Python and a working terminal ([Preparing Your Machine](../../frontend/foundations/preparing-your-machine/README.md)) |
| 2 | [Processes and Threads](processes-and-threads/README.md) | What does the kernel know about a running program, and how do processes and threads differ? | Introduction |
| 3 | [Memory Management](memory-management/README.md) | How is memory divided among programs, translated, and protected? | Introduction, Processes and Threads |
| 4 | [CPU Scheduling](cpu-scheduling/README.md) | Which ready program runs next, and for how long? | Introduction, Processes and Threads |
| 5 | [Deadlocks and Concurrency](deadlocks-and-concurrency/README.md) | What goes wrong when threads share data, and how do locks, semaphores, and lock ordering fix it? | Processes and Threads, CPU Scheduling |
| 6 | [File Systems](file-systems/README.md) | How do names lead to data on a disk, how is space allocated, and who may access it? | Introduction, Processes and Threads, Memory Management, Deadlocks and Concurrency |
| 7 | Virtual Memory (in preparation) | How can a program use more memory than the machine has? | Memory Management |

## 🧠 How to Study This Section

1. Read the module README first: its objectives, prerequisites, and deep-dive/skim guide tell you where to spend your time.
2. Run the code yourself and change it. Many experiments are small simulators, so you can change the workload and watch the results change.
3. Answer the knowledge-check questions before you open the answers.
4. Use the references (articles, manual pages, free textbook chapters, and practice-question pages) for a second view of each topic.

## 📚 References

- [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/): a free online textbook; the modules link to the chapters that match their topics.
- [Wikipedia: Operating system](https://en.wikipedia.org/wiki/Operating_system): an overview of the whole subject.

## ➡️ Start Here

Begin with [Introduction to Operating Systems](introduction-to-operating-systems/README.md). If you already know what an operating system does, start with [Processes and Threads](processes-and-threads/README.md), and come back to the introduction for system calls and kernel and user mode if a later lesson relies on them.
