# 🖥️ Introduction to Operating Systems

## 📚 Overview

Every program you have ever run depended on an **operating system** — the software that shares the processor, the memory, the disk, and the network among all the programs running at once, hides the awkward details of the hardware behind simple ideas such as files and processes, and keeps programs from interfering with one another. You rarely notice it, but it decides how fast your programs run, what they are allowed to touch, and what happens when one of them crashes.

This module is the foundation for the rest of the Operating Systems section. It explains what an operating system is and what it provides; how programs ask it for services with **system calls**; how the processor's **kernel and user modes** make protection possible, with measurements of what crossing that boundary costs; the **families of operating systems** (batch, time-sharing, real-time, distributed, embedded, mobile), with a simulation of why time-sharing exists and a measurement of why an ordinary desktop OS cannot promise deadlines; and the main **kernel architectures** (monolithic, microkernel, hybrid), with experiments on fault isolation and on the price of message passing. Every code example was run on CPython 3.9 on a Mac (macOS, Apple silicon); where output depends on the machine, the text says so and the same code runs on Linux. The claims about operating-system history and design are checked against the cited sources, and the simulations were verified against accounting identities on thousands of random inputs.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Define an operating system as a resource manager and an abstraction provider, and distinguish the kernel from the operating system as a whole.
- Explain what a system call is, trace its path from a program through a library wrapper and a trap into the kernel and back, and use Python's `os` module to make system calls directly.
- Describe the boot sequence from firmware to the first user process, and find process 1 on your own machine.
- Explain why the CPU has user and kernel modes, which instructions and memory only the kernel may use, and the three ways control enters the kernel: system calls, exceptions, and interrupts.
- Interpret measurements of system-call cost and of user versus system CPU time, and explain why a blocked process uses no CPU.
- Classify operating systems (batch, multiprogramming, time-sharing, real-time, distributed, network, embedded, mobile) and explain the response-time versus throughput trade-off between batch and time-sharing, including the cost of context switches.
- Distinguish monolithic kernels, microkernels, hybrid kernels, and layered designs, and explain how fault isolation trades against communication cost.

## 📋 Prerequisites

- [Preparing Your Machine](../../../frontend/foundations/preparing-your-machine/README.md) — a working terminal and Python installation for running the examples.
- Basic Python reading ability — the examples use functions, loops, dictionaries, and the standard library (`os`, `platform`, `subprocess`, `resource`, `time`).
- No prior knowledge of operating systems is assumed.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [what-is-an-operating-system.md](what-is-an-operating-system.md) | What an OS does, the kernel versus the whole system, system calls from Python, the boot sequence, inspecting your own system, and a short history |
| [kernel-and-user-mode.md](kernel-and-user-mode.md) | Privilege modes and protection rings, the three ways into the kernel, the path of a system call, protection demonstrated, system-call cost measured, and user versus system CPU time |
| [types-of-operating-systems.md](types-of-operating-systems.md) | Batch, multiprogramming, time-sharing, real-time, distributed, network, embedded, and mobile systems; a batch versus time-sharing simulation; sleep latency measured on a quiet and a loaded machine |
| [os-architecture.md](os-architecture.md) | Monolithic, microkernel, hybrid, layered, exokernel, and unikernel designs; virtual machines and containers; a fault-isolation experiment and the cost of message passing measured |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [kernel-and-user-mode.md](kernel-and-user-mode.md) first if you are preparing for interviews or for the later modules in this section: the user/kernel split, system calls, interrupts, and the idea that a blocked process costs nothing are the vocabulary that scheduling, memory management, and concurrency all build on. [os-architecture.md](os-architecture.md) is the usual source of "monolithic versus microkernel" questions.

**Skim** [what-is-an-operating-system.md](what-is-an-operating-system.md) if you already use a command line and know what a kernel is, but run the system-call and `launchd`/`systemd` examples on your own machine. Treat [types-of-operating-systems.md](types-of-operating-systems.md) as a reference table plus a short simulation; read the real-time section if you work with embedded or latency-sensitive systems.

## 🧠 Knowledge Check

<details>
<summary>Why can an ordinary program not simply read from the disk or reprogram a device itself, and what makes that restriction impossible to bypass?</summary>

Instructions that talk to devices, change the memory map, or alter the interrupt controller are **privileged**: the CPU executes them only in **kernel mode**. Ordinary programs run in **user mode**, where such an instruction raises an exception instead of executing. A program that wants to do I/O must make a **system call**, which uses a special trap instruction to switch the CPU into kernel mode and jump to a fixed, kernel-chosen entry point — never to an address the program picks — where the kernel checks the request and its arguments and performs the operation on the program's behalf. Because the mode is recorded in the hardware and the entry point is fixed, user code has no way to run privileged code except through the checks. See [kernel-and-user-mode.md](kernel-and-user-mode.md).

</details>

<details>
<summary>What is the main trade-off between a monolithic kernel and a microkernel?</summary>

A monolithic kernel runs all operating-system services in kernel space and calls them as ordinary functions, which is fast but gives no isolation: a bug in any driver runs with full privilege and can bring down the whole system. A microkernel keeps only the essentials (address spaces, scheduling, message passing) in the kernel and runs file systems, drivers, and protocol stacks as separate user-mode servers, which contains failures and shrinks the trusted code, but every request becomes a message between processes. In the experiment in [os-architecture.md](os-architecture.md), a round trip between two processes cost many times a plain system call — which is why microkernels invest in fast message passing and monolithic and hybrid kernels keep hot paths inside the kernel.

</details>

## 📚 References

- [Wikipedia: Operating system](https://en.wikipedia.org/wiki/Operating_system), [Kernel](https://en.wikipedia.org/wiki/Kernel_(operating_system)), [System call](https://en.wikipedia.org/wiki/System_call), and [History of operating systems](https://en.wikipedia.org/wiki/History_of_operating_systems) — definitions, structure, and history.
- [Wikipedia: Protection ring](https://en.wikipedia.org/wiki/Protection_ring), [User space and kernel space](https://en.wikipedia.org/wiki/User_space_and_kernel_space), [Interrupt](https://en.wikipedia.org/wiki/Interrupt), and [Segmentation fault](https://en.wikipedia.org/wiki/Segmentation_fault) — privilege modes and what happens when a program breaks the rules.
- [Wikipedia: Time-sharing](https://en.wikipedia.org/wiki/Time-sharing), [Computer multitasking](https://en.wikipedia.org/wiki/Computer_multitasking), [Real-time operating system](https://en.wikipedia.org/wiki/Real-time_operating_system), [Distributed operating system](https://en.wikipedia.org/wiki/Distributed_operating_system), and [Network operating system](https://en.wikipedia.org/wiki/Network_operating_system) — the families of operating systems.
- [Wikipedia: Monolithic kernel](https://en.wikipedia.org/wiki/Monolithic_kernel), [Microkernel](https://en.wikipedia.org/wiki/Microkernel), [Hybrid kernel](https://en.wikipedia.org/wiki/Hybrid_kernel), [XNU](https://en.wikipedia.org/wiki/XNU), [Linux kernel](https://en.wikipedia.org/wiki/Linux_kernel), and [OS-level virtualization](https://en.wikipedia.org/wiki/OS-level_virtualization) — kernel architectures and containers.
- [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/) ([introduction chapter](https://pages.cs.wisc.edu/~remzi/OSTEP/intro.pdf)) — a free, widely used textbook that frames the OS around virtualization, concurrency, and persistence.
- [Linux man page: `syscalls(2)`](https://man7.org/linux/man-pages/man2/syscalls.2.html) — the list of Linux system calls.
- [Python docs: `os`](https://docs.python.org/3/library/os.html), [`platform`](https://docs.python.org/3/library/platform.html), [`resource`](https://docs.python.org/3/library/resource.html), and [`subprocess`](https://docs.python.org/3/library/subprocess.html) — the standard-library tools used for the experiments.
- [GeeksforGeeks: Introduction of Operating System](https://www.geeksforgeeks.org/operating-systems/introduction-of-operating-system-set-1/), [Kernel in Operating System](https://www.geeksforgeeks.org/operating-systems/kernel-in-operating-system/), [Types of Operating Systems](https://www.geeksforgeeks.org/operating-systems/types-of-operating-systems/), and [Microkernel](https://www.geeksforgeeks.org/operating-systems/operating-system-microkernel/) — overviews and practice questions.

## ➡️ Continue Your Learning Path

Continue to the Processes and Threads module, the next module in this section, where the focus moves from the operating system as a whole to its central abstraction: what a running program looks like to the kernel, how threads share a process, and how the kernel switches among them.
