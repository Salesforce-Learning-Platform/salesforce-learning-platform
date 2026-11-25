# 🏗️ Operating System Architecture

## How Do You Organize a Million Lines of Privileged Code?

The kernel is the most privileged and most trusted software on a computer: everything inside it runs in kernel mode, where one stray pointer can corrupt any memory or any device ([kernel-and-user-mode.md](kernel-and-user-mode.md)). That raises a design question every OS builder faces: **what must run in that privileged mode, and how should the parts be organized and talk to each other?** Putting more inside the kernel makes the common operations fast, because components call each other directly; putting less inside makes the system more robust and more secure, because a failure in one component is contained. Different answers have produced the main kernel architectures.

This file describes them — monolithic, microkernel, hybrid, layered, and the more exotic exokernels and unikernels — and shows where virtual machines and containers fit. Two small experiments make the central trade-off concrete: a crash in a component that lives in the same address space as everything else versus one in its own process, and what it costs to ask a *separate* process for a service instead of making a system call. All outputs were produced by running the code on CPython 3.9 on a Mac (macOS, Apple silicon).

## 🧱 Monolithic Kernels

In a **monolithic kernel** the entire operating system runs in kernel space as one program: the scheduler, memory manager, file systems, network stack, and device drivers all live together and call one another as ordinary functions. Wikipedia defines it as an operating system architecture with the entire operating system running in kernel space, where a set of primitives or system calls implement all operating system services ([Wikipedia: Monolithic kernel](https://en.wikipedia.org/wiki/Monolithic_kernel)).

- **Strengths:** speed and simplicity of interaction. A file system calling the disk driver is a function call, with no message to build and no switch of address space.
- **Weaknesses:** no isolation inside the kernel. A bug in any driver — a device driver is often the least carefully tested code — runs with full privilege and can crash or compromise the whole system. The whole kernel is the trusted base that must be correct.

**Linux** is the best-known monolithic kernel, and it also shows how monoliths cope with their size. Wikipedia notes that the Linux kernel is "both monolithic and modular": architecturally the entire OS runs in kernel space, but the design is modular, because it can be assembled from modules that are loaded and unloaded at run time ([Wikipedia: Linux kernel](https://en.wikipedia.org/wiki/Linux_kernel)). A **loadable kernel module** is an executable library that extends a running kernel — typically with a new device driver or file system — and can be unloaded to free its memory ([Wikipedia: Loadable kernel module](https://en.wikipedia.org/wiki/Loadable_kernel_module)). Modules make a monolith flexible and keep the always-resident part small, but a loaded module still runs in kernel mode with full privilege, so it gains no protection.

## 🪶 Microkernels

A **microkernel** takes the opposite approach: keep in the privileged kernel only what *cannot* be done outside it — typically managing address spaces, scheduling threads, and passing messages between processes — and run everything else as ordinary **user-mode servers**. Components that a monolithic kernel includes, such as device drivers, protocol stacks, and file systems, are typically removed from the microkernel and run in user space ([Wikipedia: Microkernel](https://en.wikipedia.org/wiki/Microkernel)). The pieces cooperate by **sending messages** through the kernel.

```
   Monolithic                                   Microkernel

 ┌──────────────────────────┐        ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐
 │  user programs           │        │ user   │ │ file   │ │ device │ │ network  │   user
 ├──────────────────────────┤        │ prog.  │ │ server │ │ driver │ │ server   │   mode
 │ file system │ drivers │  │        └───┬────┘ └───┬────┘ └───┬────┘ └────┬─────┘
 │ network stack │ memory │ │            │ messages │          │          │
 │ scheduler  ...  (kernel) │        ┌───┴──────────┴──────────┴──────────┴─────┐
 └──────────────────────────┘        │ microkernel: address spaces, threads, IPC│   kernel mode
         all in kernel mode           └──────────────────────────────────────────┘
```

- **Strengths:** **fault isolation** — a crashing driver is just a crashed user process that can be restarted without taking down the kernel; a **small trusted base** — the privileged code is small enough to inspect (Wikipedia gives the MINIX 3 microkernel as having only about 12,000 lines of code); **least privilege** — each server gets only the access it needs; and **flexibility**, since services can be replaced independently.
- **Weaknesses:** **performance cost**. Every request to a service becomes a message, which means copying data and switching address spaces. The first microkernels, notably Mach, "proved to have disappointing performance" (same article), and much later microkernel research went into making message passing fast.
- **Examples:** MINIX 3, QNX, and seL4 are microkernel-based, and many embedded and safety-critical systems use the approach.

## 🧬 Hybrid Kernels

A **hybrid kernel** tries to get the benefits of both: it has a microkernel-like *structure*, but most services still run in kernel space, as in a monolith, to avoid the message-passing overhead ([Wikipedia: Hybrid kernel](https://en.wikipedia.org/wiki/Hybrid_kernel)). The Windows NT kernel is a hybrid kernel — a simple kernel, a hardware abstraction layer, drivers, and a set of services called the Executive, all in kernel mode ([Wikipedia: Windows NT](https://en.wikipedia.org/wiki/Windows_NT)) — and so is **XNU**, the kernel of macOS and iOS, built from the Mach microkernel and a BSD Unix layer running together in one kernel space ([Wikipedia: XNU](https://en.wikipedia.org/wiki/XNU)).

The category is controversial: since a hybrid kernel keeps services in kernel space, it has none of the reliability benefit of a true microkernel, and critics argue that it is just a monolithic kernel with a different structure. Linus Torvalds famously dismissed the term as marketing; the Wikipedia article records this view. The practical point is that real kernels sit on a spectrum rather than in three clean boxes.

The next block asks the OS which kernel it is running on. The answer on the Mac used for this module is `Darwin`, whose kernel is XNU; on Linux the same code reports `Linux`, and on Windows `Windows`:

```python
import platform

kernels = {
    "Darwin": "XNU, a hybrid kernel (Mach and BSD parts together in kernel space)",
    "Linux": "Linux, a monolithic kernel that loads modules at run time",
    "Windows": "the NT kernel, a hybrid kernel",
}
system = platform.system()
print(system, "->", kernels.get(system, "a kernel that is not in this small table"))
print("the kernel's own version string mentions XNU:", "xnu" in platform.version().lower())
```

```text
Darwin -> XNU, a hybrid kernel (Mach and BSD parts together in kernel space)
the kernel's own version string mentions XNU: True
```

## 📚 Layered and Other Designs

Several other organizing ideas appear in the literature:

- **Layered systems.** The design of the THE multiprogramming system, an early example, is significant for its layered structure in which "higher" layers depend on "lower" layers only, so each layer could be built and tested in turn ([Wikipedia: THE multiprogramming system](https://en.wikipedia.org/wiki/THE_multiprogramming_system)). Strict layering is hard to achieve in a full OS, because services depend on one another in cycles, but the idea of clean levels of abstraction pervades operating systems.
- **Exokernels.** An exokernel limits itself to protecting and multiplexing the machine's physical resources — disk blocks, memory pages, processor time — and lets each application decide how to use them, typically through a library that implements the abstractions it wants ([Wikipedia: Exokernel](https://en.wikipedia.org/wiki/Exokernel)). It pushes the "do less in the kernel" idea further than a microkernel does.
- **Unikernels.** A unikernel compiles an application together with just the operating-system pieces it needs into a single specialized image, often run directly on a hypervisor; it cannot be changed after it is built, so a change means building and deploying a new image ([Wikipedia: Unikernel](https://en.wikipedia.org/wiki/Unikernel)).

## 🧰 Virtual Machines and Containers

Two further ideas change what "the OS" means for a program without being kernel architectures themselves:

- A **virtual machine** runs a complete guest operating system, with its own kernel, on virtualized hardware provided by a **hypervisor**. Each guest believes it owns a computer.
- A **container** is an **OS-level virtualization** feature: the one kernel allows multiple isolated user-space instances, which look like separate computers to the programs inside ([Wikipedia: OS-level virtualization](https://en.wikipedia.org/wiki/OS-level_virtualization)). Containers share the host's kernel, which makes them lighter and faster to start than virtual machines, but also means they cannot run a different kernel than the host's.

## ⚖️ Comparing the Architectures

| | Monolithic | Microkernel | Hybrid |
|--|------------|-------------|--------|
| Where most services run | Kernel mode | User mode (servers) | Kernel mode, structured like a microkernel |
| Communication between parts | Function calls | Messages through the kernel | Mostly function calls |
| Speed | Fast | Slower; depends on fast message passing | Fast |
| Fault isolation | Weak: a bad driver can bring down the system | Strong: a failed server can be restarted | Weak, like a monolith |
| Size of the privileged code | Large | Small | Large |
| Examples | Linux, many Unix systems | MINIX 3, QNX, seL4 | Windows NT, XNU (macOS, iOS) |

## 🧪 Experiment 1: Fault Isolation

The robustness argument can be shown directly with processes standing in for address spaces. Imagine a *service* that depends on a *driver* with a fatal bug. A real driver bug would usually end in a segmentation fault ([kernel-and-user-mode.md](kernel-and-user-mode.md) explains how the hardware and the kernel produce one); the experiment has the driver kill itself with the `SIGKILL` signal instead, which ends a process just as instantly and completely but, unlike a genuine segmentation fault, does not make macOS open a crash-report window. In the first program, the driver's code runs inside the service's own process, as in a monolithic kernel; in the second, the driver runs in a separate process that the service supervises, as in a microkernel:

```python
import subprocess
import sys

CRASH = "import os, signal; os.kill(os.getpid(), signal.SIGKILL)"   # a "driver" that suffers a fatal failure and is gone at once

shared_address_space = "print('service: started', flush=True); " + CRASH + "; print('service: finished', flush=True)"
result = subprocess.run([sys.executable, "-c", shared_address_space], capture_output=True, text=True)
print("driver inside the service's own process ->", "exit code", result.returncode, "| output:", result.stdout.split("\n")[:-1])

separate_process = (
    "import subprocess, sys\n"
    "print('service: started', flush=True)\n"
    f"driver = subprocess.run([sys.executable, '-c', {CRASH!r}])\n"
    "print('service: the driver died with code', driver.returncode, '- the service restarts it', flush=True)\n"
    "print('service: finished', flush=True)\n"
)
result = subprocess.run([sys.executable, "-c", separate_process], capture_output=True, text=True)
print("driver in its own process ->", "exit code", result.returncode, "| output:", result.stdout.split("\n")[:-1])
```

```text
driver inside the service's own process -> exit code -9 | output: ['service: started']
driver in its own process -> exit code 0 | output: ['service: started', 'service: the driver died with code -9 - the service restarts it', 'service: finished']
```

When the faulty code shares the service's address space, the whole service dies instantly (exit code -9 means "killed by signal 9") and never reaches its last line. When the faulty code is isolated in its own process, only that process dies; the service sees the exit code, restarts the driver, and finishes normally. That is the reliability argument for microkernels, in miniature: **separate address spaces turn a crash into an event that can be handled**.

## 🧪 Experiment 2: What Does Isolation Cost?

The price is communication. A monolithic kernel calls the file system with a function call; a microkernel must send a message to a file-system *process* and wait for a reply. The next block measures that difference on real hardware. A parent process sends one byte to a child process through a pipe and waits for the child to send it back — a *round trip* of two messages — and the result is compared with a single system call and an ordinary Python function call:

```python
import os
import time

def pipe_round_trip_us(rounds=20_000):
    to_child_r, to_child_w = os.pipe()
    to_parent_r, to_parent_w = os.pipe()
    pid = os.fork()
    if pid == 0:                                                  # the child: echo every byte back
        os.close(to_child_w)
        os.close(to_parent_r)
        try:
            while True:
                data = os.read(to_child_r, 1)
                if not data:
                    break
                os.write(to_parent_w, data)
        finally:
            os._exit(0)
    os.close(to_child_r)
    os.close(to_parent_w)
    start = time.perf_counter()
    for _ in range(rounds):
        os.write(to_child_w, b"x")
        os.read(to_parent_r, 1)
    elapsed = time.perf_counter() - start
    os.close(to_child_w)
    os.close(to_parent_r)
    os.waitpid(pid, 0)
    return elapsed / rounds * 1e6

def microseconds(function, number):
    start = time.perf_counter()
    for _ in range(number):
        function()
    return (time.perf_counter() - start) / number * 1e6

def nothing():
    pass

best_round_trip = min(pipe_round_trip_us() for _ in range(3))
call = microseconds(nothing, 1_000_000)
syscall = microseconds(os.getppid, 1_000_000)
print(f"a Python function call:                        {call:8.3f} us")
print(f"a system call (os.getppid):                    {syscall:8.3f} us")
print(f"a message round trip between two processes:    {best_round_trip:8.3f} us   ({best_round_trip / syscall:,.0f} times the system call)")
```

Output:

```
a Python function call:                           0.034 us
a system call (os.getppid):                       0.103 us
a message round trip between two processes:       5.672 us   (55 times the system call)
```

The round trip includes two messages, two switches between processes, and four system calls, and the interpreter adds overhead of its own, so the exact figure is only a rough guide. Still, it is a large multiple of a plain system call — a plain system call being the price a *monolithic* kernel pays to enter and leave the kernel for an operation — and the gap is why designers of microkernels invest so much in fast message passing, and why monolithic and hybrid kernels keep the hot paths (file access, networking, scheduling) inside the kernel. Both experiments together state the trade-off in one sentence: **moving services out of the kernel buys containment and costs communication**.

## Common Misconceptions

- **"Microkernel is modern, monolithic is outdated."** Both are in heavy use: Linux, the dominant server kernel, is monolithic, while microkernels dominate in embedded and safety-critical systems. The choice is a trade-off, not a generation.
- **"Loadable modules make Linux a microkernel."** Modules are loaded into kernel space and run with full privilege, so they add flexibility but not isolation.
- **"A hybrid kernel has the best of both."** It has the microkernel's structure with the monolith's performance — and the monolith's lack of fault isolation. Whether that is "the best of both" is exactly what is disputed.
- **"A container is a small virtual machine."** A virtual machine has its own kernel; a container shares the host's kernel and is only isolated from other containers by that kernel's features.
- **"The architecture decides the OS's quality."** Implementation quality, testing, and the code of the drivers matter at least as much as the diagram.

## ➡️ Next

Continue to the [Processes and Threads module](../processes-and-threads/README.md), the next module in this section: the kernel's central abstractions, what a running program is from the operating system's point of view, and how the kernel keeps many of them progressing at once.
