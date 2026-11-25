# 🖥️ What Is an Operating System?

## The Software Between Programs and Hardware

When you open a file, type in a window, or run two programs at once, you rely on a layer of software that you rarely see: the **operating system** (OS). Wikipedia's definition is a good starting point: an operating system is system software that manages computer hardware and software resources and provides common services for computer programs ([Wikipedia: Operating system](https://en.wikipedia.org/wiki/Operating_system)). Without one, every program would have to know how to drive the disk controller, share the processor politely with every other program, and keep its memory from colliding with theirs.

An OS plays two complementary roles:

1. **Resource manager.** The computer has a limited supply of CPU time, memory, storage, network bandwidth, and devices, and many programs want them at once. The OS decides who gets what and when, keeps programs from interfering with each other, and keeps accounts of the use.
2. **Abstraction provider.** Raw hardware is awkward: a disk is a numbered array of blocks, a network card is a set of registers, memory is a flat range of addresses. The OS hides these details behind simpler, uniform ideas — **files**, **processes**, **sockets**, **virtual memory** — so programmers can write `open`, `read`, and `send` without knowing which device is underneath.

This file introduces what an operating system is, what it does, how programs ask it for services, and how a computer gets from power-on to a running OS. Every code example was run on CPython 3.9 on a Mac (macOS, Apple silicon); output that depends on the machine is labelled as such, and the same code runs unchanged on Linux. The next files look at the **kernel** and its privileged mode ([kernel-and-user-mode.md](kernel-and-user-mode.md)), the **kinds of OS** ([types-of-operating-systems.md](types-of-operating-systems.md)), and how kernels are **structured** ([os-architecture.md](os-architecture.md)).

## 🧱 Where the OS Sits

```
┌──────────────────────────────────────────────────┐
│  Users                                           │
├──────────────────────────────────────────────────┤
│  Applications   (browser, editor, your Python)   │
├──────────────────────────────────────────────────┤
│  System programs and libraries  (shell, libc)    │
├══════════════════════════════════════════════════┤  ← system call interface
│  Kernel   (processes, memory, files, devices)    │
├──────────────────────────────────────────────────┤
│  Hardware (CPU, RAM, disk, network, displays)    │
└──────────────────────────────────────────────────┘
```

The word "operating system" is used for two slightly different things. The **kernel** is the core program that runs with full hardware privileges and does the resource management. The **operating system** in the everyday sense also includes the system programs around it — shells, file utilities, libraries, a graphical interface. *Linux*, strictly, is a kernel; a Linux distribution adds the surrounding software to make a complete OS. This is why one kernel can underlie many different-looking systems, and why "the OS" in a product description may mean either.

## 🧰 What an Operating System Does

| Responsibility | What the OS provides | Typical abstraction |
|----------------|----------------------|---------------------|
| **Process management** | Creating, scheduling, and ending running programs; letting many share the CPU | Process, thread |
| **Memory management** | Giving each program its own address space; allocating and protecting RAM; using disk to extend it | Virtual memory |
| **Storage and file systems** | Naming, storing, retrieving, and protecting data on disks | Files and directories |
| **Device management** | Controlling hardware through drivers; handling interrupts and buffering | Device files, drivers |
| **Networking** | Moving data between machines; hiding the network hardware | Sockets |
| **Protection and security** | Isolating programs and users from one another; checking permissions | Users, permissions, privilege modes |
| **User interface** | Letting people start and control programs | Shell, windows, icons |
| **Accounting and monitoring** | Measuring resource use per process and per user | Counters, logs |

The [Processes and Threads](../processes-and-threads/README.md), CPU Scheduling, Memory Management, Virtual Memory, File Systems, and Deadlocks and Concurrency modules in this section take these responsibilities one at a time. The rest of this file shows the most important idea that connects them: how an ordinary program asks the OS for help.

## 🔌 System Calls: How Programs Ask for Service

Programs run in a restricted environment where they cannot touch the disk, the network, or other programs' memory directly. To do anything beyond computing on their own data, they make a **system call** — a controlled request to the kernel, such as "open this file", "read these bytes", "create a new process", or "send this data". The kernel checks the request, performs it on the program's behalf, and returns a result ([Wikipedia: System call](https://en.wikipedia.org/wiki/System_call)). The next file explains the hardware mechanism that makes this safe.

High-level languages hide system calls inside friendly functions. Python's `os` module exposes many of them almost directly: `os.open` is a thin wrapper over the `open` system call, `os.write` over `write`, `os.close` over `close`. Here is a file written and read back using only those wrappers, and the same bytes read through Python's ordinary file object:

```python
import os
import tempfile

with tempfile.TemporaryDirectory() as folder:
    path = os.path.join(folder, "demo.txt")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT)               # open: ask the kernel for a file descriptor
    written = os.write(fd, b"hello, kernel\n")                  # write: the kernel reports how many bytes it took
    os.close(fd)                                                # close: hand the descriptor back
    print("descriptor is a small integer above 2:", 3 <= fd < 100, "| wrote", written, "bytes")
    with open(path, "rb") as handle:                            # the high-level way; it makes the same calls underneath
        print(handle.read())
```

```text
descriptor is a small integer above 2: True | wrote 14 bytes
b'hello, kernel\n'
```

Several OS ideas are visible in those few lines. The kernel returns a small integer, a **file descriptor**, as a handle for the open file; the program never sees the disk's layout. The call reports how many bytes it accepted, because a system call may do less than asked. And every call can fail — with a missing directory, a permission error, or a full disk — which is why the OS reports errors through return codes that Python turns into exceptions.

Python's `os.getpid()` is no different from the C library's `getpid()` — Python is a thin layer over the C library, which is a thin layer over the system call. The check below calls the C library directly through `ctypes` and gets the same answer:

```python
import ctypes
import ctypes.util

libc = ctypes.CDLL(ctypes.util.find_library("c"))
print(libc.getpid() == os.getpid())                            # True
```

## 🥾 From Power-On to a Running System

A computer cannot load an operating system from disk until it has software that knows how to read a disk. The chain that solves this is the **boot process**:

1. **Firmware** (BIOS or UEFI on PCs, the boot ROM on phones and Apple silicon) runs first, from non-volatile memory. It tests and initializes basic hardware.
2. The firmware loads a **bootloader** from storage — a small program that knows where the kernel lives and how to load it.
3. The bootloader loads the **kernel** into memory and starts it. The kernel initializes its own data structures, detects devices, sets up memory management, and mounts the root file system.
4. The kernel starts the **first user-space process**, known as process ID 1 (`init`, `systemd`, or `launchd`, depending on the system). Every other process descends from it.
5. That first process starts **services** (network, logging, login screens), and finally a user session.

Step 4 can be seen directly. Process ID 1 is the ancestor of all user processes; on the Mac used for this module it is `launchd`, while on many Linux systems it is `systemd`:

```python
import subprocess

first_process = subprocess.run(["ps", "-p", "1", "-o", "comm="], capture_output=True, text=True).stdout.strip()
print("process 1 on this machine:", first_process)
```

```text
process 1 on this machine: /sbin/launchd
```

## 🔎 What Does *Your* System Look Like?

Python can ask the OS about itself. The values below describe the machine used to build this module (a Mac with Apple silicon); on yours they will differ, which is exactly the point — the same program learns what it is running on by asking the OS:

```python
import platform
import sys

print("OS:", platform.system())
print("hardware:", platform.machine(), "| logical CPUs:", os.cpu_count(), "| memory page size:", os.sysconf("SC_PAGE_SIZE"), "bytes")
print("os.name:", os.name, "| sys.platform:", sys.platform)
```

```text
OS: Darwin
hardware: arm64 | logical CPUs: 11 | memory page size: 16384 bytes
os.name: posix | sys.platform: darwin
```

`platform.system()` returns `Darwin` here: the name of the open-source core of macOS, which is built around the XNU kernel (see [os-architecture.md](os-architecture.md)). On Linux it returns `Linux`, and on Windows `Windows`. The **page size** (16 KB on Apple silicon, commonly 4 KB on x86 PCs) is a unit the memory manager works in, as the Memory Management and Virtual Memory modules explain.

## 🕰️ A Short History: Why OSes Look the Way They Do

Each stage in the history of operating systems answered a specific waste or frustration of the one before it:

| Era | Problem | Idea | Example |
|-----|---------|------|---------|
| Mid-1950s | An expensive computer sat idle while operators loaded jobs by hand | **Batch processing**: queue jobs and run them one after another automatically | GM-NAA I/O, 1956 — described by Wikipedia as the first operating system used for real work |
| 1960s | During disk or tape I/O, the CPU sat idle; users waited hours for results | **Multiprogramming** and **time-sharing**: keep several jobs in memory, switch among them, and let many users share the machine interactively | CTSS, a time-sharing system whose prototype was tested in 1961 |
| Mid-1960s | Shared machines needed protection between users | **Privilege levels** and protected memory | Multics, which introduced ringed privilege levels |
| Late 1960s and after | Operating systems were written for one machine and thrown away | **Portable, simple, Unix-style design** in a high-level language | Unix (preemptive multitasking in 1969), whose descendants and imitators include Linux, BSD, and macOS |
| 1980s onward | Computers became personal and cheap | Single-user, then multitasking, graphical systems | Desktop systems of every kind |
| 2000s onward | Phones, servers by the thousand, virtual machines | Mobile OSes, virtualization, containers | Android, iOS, cloud platforms |

(GM-NAA I/O, CTSS, Multics, and Unix dates are from Wikipedia's articles on the [history of operating systems](https://en.wikipedia.org/wiki/History_of_operating_systems), [time-sharing](https://en.wikipedia.org/wiki/Time-sharing), and [computer multitasking](https://en.wikipedia.org/wiki/Computer_multitasking).)

The pattern is that **the OS grows features to keep expensive resources busy and to keep users from harming each other**. Almost every concept in this section — scheduling, memory protection, virtual memory, file permissions — exists because of one of those two pressures.

## Common Misconceptions

- **"The OS is the same as the user interface."** The graphical desktop or the command line is one program among many; the OS's core work (scheduling, memory, files, devices) is invisible.
- **"Linux is an operating system like Windows."** Strictly, Linux is a kernel; a complete system adds libraries, utilities, and an interface. In everyday speech, "Linux" often means the whole distribution.
- **"Programs talk to the hardware directly."** Ordinary programs never do; they make system calls, and only the kernel touches devices.
- **"Python (or any language) runs without an OS."** The interpreter itself is a program that relies on the OS for memory, files, threads, and time.
- **"A system call is just a function call."** It looks like one in code, but it crosses a protection boundary into privileged code, which has real consequences for cost and safety ([kernel-and-user-mode.md](kernel-and-user-mode.md)).

## ➡️ Next

Continue to [kernel-and-user-mode.md](kernel-and-user-mode.md): the hardware feature that lets the kernel protect itself and every program from one another, how a system call crosses that boundary, and what crossing it costs.
