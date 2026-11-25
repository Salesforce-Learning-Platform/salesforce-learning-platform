# 🔐 Kernel Mode and User Mode

## Why the CPU Has Two Faces

If every program could execute every instruction, one careless loop could overwrite the operating system's memory, one buggy driver could reprogram the disk controller, and any program could read any other program's data. An operating system can only keep its promises — fair sharing, isolation, permissions — if programs **cannot bypass it**. That guarantee cannot be made by software alone, because software that is trusted to police itself is easily circumvented; it needs help from the processor.

The help is built into the CPU: it runs in (at least) two **privilege modes**.

- **Kernel mode** (also called supervisor, privileged, or "ring 0"): the operating system's core runs here. All instructions are allowed, all memory is reachable, and all devices can be controlled.
- **User mode** ("ring 3" on x86): ordinary programs run here. Certain instructions are forbidden, and memory access is limited to the program's own address space.

A hardware register records the current mode, and the processor checks it on every privileged action. Wikipedia describes these *protection rings* as hierarchical levels of privilege, generally enforced by the CPU architecture. The original Multics system had eight rings, x86 hardware provides four, yet most general-purpose systems use only two of them — ring 0 for the kernel and ring 3 for user programs ([Wikipedia: Protection ring](https://en.wikipedia.org/wiki/Protection_ring)). Other architectures have equivalent user and supervisor modes under different names. All outputs in this file were produced by running the code on CPython 3.9 on a Mac (macOS, Apple silicon); platform-dependent values are labelled.

## 🚫 What Only the Kernel May Do

| Privileged action | Why user programs must not do it |
|-------------------|----------------------------------|
| Talk directly to devices (disk, network card, display) | Two programs driving the same device would corrupt it, and any program could read other users' data from the disk |
| Change the memory map (page tables) | A program could map and read another program's memory, or the kernel's |
| Enable or disable interrupts, set the timer | A program could stop the OS from ever regaining control of the CPU |
| Halt the CPU, reset the machine | One program could shut down everyone's work |
| Change its own privilege mode | It could simply promote itself to kernel mode |

Memory is divided accordingly into **kernel space** — reserved for the privileged kernel, its extensions, and most device drivers — and **user space**, where applications run, typically with one address space per process ([Wikipedia: User space and kernel space](https://en.wikipedia.org/wiki/User_space_and_kernel_space)). The kernel's memory is mapped into every process's address space but is marked inaccessible to user mode, so an attempt to touch it triggers a fault.

## 🧪 Seeing the Protection at Work

Two experiments make the protection visible. First, a program that reads from the forbidden address `0` — a null pointer — is stopped by the hardware and the kernel, not by Python. The experiment runs in a child process so that the crash does not take this document down with it:

```python
import os
import subprocess
import sys

crash = subprocess.run([sys.executable, "-c", "import ctypes; ctypes.string_at(0)"], capture_output=True)
print("child process return code:", crash.returncode, "(a negative value -N means: killed by signal N)")
print("this process is unaffected and still running:", os.getpid() > 0)
```

```text
child process return code: -11 (a negative value -N means: killed by signal N)
this process is unaffected and still running: True
```

The sequence of events is: the CPU executes a load from address 0, finds no valid mapping for it, and raises an **exception** that transfers control to the kernel (in kernel mode); the kernel concludes that the process did something illegal and sends it the **SIGSEGV** signal ("segmentation violation"), which by default terminates it ([Wikipedia: Segmentation fault](https://en.wikipedia.org/wiki/Segmentation_fault)). Signal number 11 is `SIGSEGV` on both Linux and macOS, hence `-11`. The parent process, in a different address space, never notices.

Second, ordinary programs cannot perform privileged operations, even when they ask politely through the proper system call. The kernel checks who is asking:

```python
for candidate in ("/etc/shadow", "/etc/master.passwd"):          # the protected password databases on Linux and macOS
    if os.path.exists(candidate):
        try:
            open(candidate).read()
        except PermissionError as error:
            print("reading a protected file:", error)
        break

try:
    os.setuid(0)                                               # ask to become the superuser (root)
except PermissionError as error:
    print("becoming root:", error)
```

```text
reading a protected file: [Errno 13] Permission denied: '/etc/master.passwd'
becoming root: [Errno 1] Operation not permitted
```

(If these experiments are run as the superuser, they succeed — which is exactly why running everyday programs as root is dangerous.) The permission check happens inside the kernel; it can be trusted because user code cannot bypass it, and user code cannot bypass it because of the hardware modes.

## 🚪 Three Ways Into the Kernel

A user program does not keep running in user mode forever. Control enters the kernel in exactly three ways, and each uses a CPU mechanism that switches to kernel mode and jumps to a **fixed, kernel-chosen entry point** — never an address the program picks:

| Mechanism | Triggered by | Synchronous? | Examples |
|-----------|--------------|--------------|----------|
| **System call** (trap) | The program itself, deliberately | Yes | `read`, `write`, `fork`, `mmap`, `socket` |
| **Exception** (fault) | The program's own instruction going wrong | Yes | Divide by zero, invalid memory address, page fault |
| **Interrupt** | Hardware, independent of the running program | No | Timer tick, keyboard press, disk or network completion |

Wikipedia classifies interrupts as *hardware* interrupts, signalled by devices, and *software* interrupts, raised by instructions ([Wikipedia: Interrupt](https://en.wikipedia.org/wiki/Interrupt)). The **timer interrupt** deserves special mention: the OS programs a hardware timer to fire every few milliseconds, which forces control back into the kernel even if the running program never makes a system call. That is how the OS can **preempt** a program that refuses to yield, and it underlies the CPU scheduling algorithms covered later in this section.

### The Path of a System Call

When a program calls a function such as `write`, the library function is, as Wikipedia notes, usually a normal subroutine call that does not itself switch to kernel mode; it is the trap instruction inside it that transfers control to the kernel ([Wikipedia: System call](https://en.wikipedia.org/wiki/System_call)). In outline:

```
 user mode      program calls write(fd, buffer, n)         (an ordinary function call)
                library wrapper puts the call number and arguments in registers
                library executes the trap instruction  ───────────────┐
                                                                      ▼
 kernel mode                                       CPU switches to kernel mode, jumps to the fixed entry point
                                                   kernel saves the user's registers
                                                   kernel checks the arguments (is the buffer really the caller's memory?)
                                                   kernel looks up the handler in the system call table
                                                   handler does the work (it may block the process, waiting for the device)
                                                   kernel stores the result and executes return-from-trap ─┐
                                                                                                           │
 user mode      library returns the result to the program  ◄───────────────────────────────────────────────┘
```

Two details matter for safety. The kernel **validates every argument**, because the caller is untrusted: a pointer into someone else's memory, a negative length, or a bad file descriptor must produce an error, not a security hole. And the entry point is **fixed**: if programs could jump into the kernel anywhere they liked, they could skip the checks.

## ⏱️ What Does Crossing the Boundary Cost?

Entering the kernel is more expensive than an ordinary function call, because the processor changes mode, the kernel saves and restores state, and the arguments are checked. How much more? The next measurement compares an empty Python function call with a series of system calls, from the cheapest to a typical file operation. Treat the numbers as characteristic of the machine used here, not as universal constants:

```python
import timeit

def nothing():
    pass

devnull = os.open("/dev/null", os.O_WRONLY)
devzero = os.open("/dev/zero", os.O_RDONLY)

def open_and_close():
    fd = os.open("/etc/hosts", os.O_RDONLY)
    os.close(fd)

def nanoseconds(function, number):
    return min(timeit.repeat(function, number=number, repeat=5)) / number * 1e9

measurements = [
    ("an empty Python function call", nothing, 200_000),
    ("os.getpid()", os.getpid, 200_000),
    ("os.getppid()", os.getppid, 200_000),
    ("os.read(1 byte from /dev/zero)", lambda: os.read(devzero, 1), 100_000),
    ("os.write(1 byte to /dev/null)", lambda: os.write(devnull, b"x"), 100_000),
    ("os.stat('/')", lambda: os.stat("/"), 100_000),
    ("open + close a file", open_and_close, 20_000),
]
print(f"{'operation':>32} | {'time':>10}")
for label, function, number in measurements:
    print(f"{label:>32} | {nanoseconds(function, number):7.0f} ns")
```

Output:

```
                       operation |       time
   an empty Python function call |      33 ns
                     os.getpid() |      21 ns
                    os.getppid() |      97 ns
  os.read(1 byte from /dev/zero) |     371 ns
   os.write(1 byte to /dev/null) |     832 ns
                    os.stat('/') |    1147 ns
             open + close a file |    8087 ns
```

Several lessons follow. `os.getpid()` is faster than even an empty Python function, which means it does **not** enter the kernel at all here — the C library on this platform evidently answers it from a cached value — while `os.getppid()` does, and its difference from the empty function call (about 60 nanoseconds in this run) is roughly the price of the mode switch itself on this hardware. The real cost of a system call is mostly **what the kernel does**: a one-byte read or write costs a few hundred nanoseconds, a path lookup (`stat`) about a microsecond, and opening and closing a file about eight microseconds, because the kernel must resolve the path, check permissions, and allocate and free a descriptor. The old advice that "system calls cost thousands of cycles" was shaped by older processors and by calls that perform real I/O; the practical rule that survives is that **a loop issuing millions of tiny system calls is slow, so batch the work** — read a large block instead of a byte at a time.

## 📊 Where Does the CPU Time Go? User Time and System Time

Because the kernel knows which mode each process is in, it can account for the time separately. The `resource` module reports **user CPU time** (spent running the program's own code) and **system CPU time** (spent in the kernel on the program's behalf). Three workloads show the difference: arithmetic with no system calls, a loop of 300,000 `os.stat` calls, and a half-second sleep:

```python
import resource
import time

def cpu_split(work):
    before = resource.getrusage(resource.RUSAGE_SELF)
    start = time.perf_counter()
    work()
    wall = time.perf_counter() - start
    after = resource.getrusage(resource.RUSAGE_SELF)
    return wall, after.ru_utime - before.ru_utime, after.ru_stime - before.ru_stime

def arithmetic():
    total = 0
    for i in range(3_000_000):
        total += i * i

def many_system_calls():
    for _ in range(300_000):
        os.stat("/")

for label, work in (("arithmetic loop", arithmetic), ("300,000 os.stat calls", many_system_calls), ("sleep for 0.5 s", lambda: time.sleep(0.5))):
    wall, user, system = cpu_split(work)
    print(f"{label:>22}: wall {wall:6.3f} s | user CPU {user:6.3f} s | system CPU {system:6.3f} s")
```

Output:

```
       arithmetic loop: wall  0.110 s | user CPU  0.110 s | system CPU  0.000 s
 300,000 os.stat calls: wall  0.333 s | user CPU  0.121 s | system CPU  0.213 s
       sleep for 0.5 s: wall  0.505 s | user CPU  0.000 s | system CPU  0.000 s
```

The arithmetic loop spends essentially all its time in user mode. The `os.stat` loop spends most of its CPU time in the kernel (the rest is the Python interpreter preparing each call). And the sleeping process uses **no CPU time at all** — in either mode — for the whole half second: it is blocked, the kernel does not schedule it, and the processor is free for other programs. That last case is the foundation of multiprogramming: a program waiting for I/O costs nothing, so the CPU can run someone else.

## Common Misconceptions

- **"The OS checks every instruction a program executes."** It does not. Programs run at full hardware speed in user mode; the hardware raises an exception only when the program attempts something forbidden, and the kernel steps in then.
- **"User mode and kernel mode are different processors."** It is the same CPU, switching state many thousands of times per second.
- **"A system call is slow because the kernel is slow."** The mode switch itself is cheap; what makes a system call slow is the work requested (I/O, path lookups, locking) — and making too many of them.
- **"A segmentation fault is Python's (or the language's) fault."** It is the hardware and the kernel stopping a program that touched memory it does not own. A language runtime can only trigger it by bugs in native code (as `ctypes` did here).
- **"Running as root removes the protection."** It removes the *permission checks*; the hardware still isolates the kernel from user mode, which is why even root's programs cannot execute privileged CPU instructions directly.

## ➡️ Next

Continue to [types-of-operating-systems.md](types-of-operating-systems.md): the same ideas — scheduling, protection, resource management — are combined differently for different goals, giving batch, time-sharing, real-time, distributed, embedded, and mobile operating systems.
