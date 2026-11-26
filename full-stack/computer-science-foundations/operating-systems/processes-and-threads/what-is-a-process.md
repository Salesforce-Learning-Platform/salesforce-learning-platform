# 🧬 What Is a Process?

## A Recipe and a Cook

A **program** is a file: a list of instructions and some starting data, sitting on a disk and doing nothing. A **process** is that program *being executed*. Wikipedia describes it as an instance of a computer program that is being executed, by one thread or by several ([Wikipedia: Process (computing)](https://en.wikipedia.org/wiki/Process_(computing))). The usual picture is a recipe and a cook: one recipe can be cooked in several kitchens at the same time, each cook has their own ingredients and their own place in the steps, and the recipe itself never changes. In the same way, one program file can be running as many processes at once, and each process has its own memory, its own position in the code, and its own open files.

The process is the operating system's central abstraction. The kernel creates processes, gives them resources, decides which one runs next, keeps them from interfering with each other, and cleans up after them. Scheduling, memory management, and deadlocks, the other modules of this section, are all different views of how the kernel manages processes. This file explains what a process is made of, how Unix-style systems create and end one, and what you can observe about it from Python. Every code example was run on CPython 3.9 on a Mac (macOS, Apple silicon); the examples use the Unix calls `fork`, `exec`, and `wait`, which exist on Linux and macOS but not on Windows. Where an output depends on the machine, the text says so.

## 👥 One Program, Many Processes

Two copies of the same program, started at the same moment, are two different processes. The next block starts two sleeping Python interpreters and asks the `ps` command which program file each one is running:

```python
import os
import subprocess
import sys

def program_of(pid):
    return subprocess.run(["ps", "-o", "comm=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()

code = "import time; print('started', flush=True); time.sleep(5)"
sleepers = [subprocess.Popen([sys.executable, "-c", code], stdout=subprocess.PIPE, text=True) for _ in range(2)]
for process in sleepers:
    process.stdout.readline()                       # wait until the interpreter has really started
programs = [program_of(process.pid) for process in sleepers]
print("two live processes with different ids:", sleepers[0].pid != sleepers[1].pid)
print("running the same program file:", programs[0] == programs[1] and programs[0] != "")
for process in sleepers:
    process.kill()
    process.wait()
    process.stdout.close()
```

```text
two live processes with different ids: True
running the same program file: True
```

The block waits for each interpreter to print a line before asking `ps`, because on some systems `python3` is a small launcher that first executes the real interpreter; until that second `exec` has happened (a call explained below), `ps` may still report the launcher.

Each process is identified by a number, the **process identifier** (PID), which the kernel hands out when the process is created. The PID is the handle used by `ps`, `kill`, and every other tool that talks about a particular process.

## 🧾 What the Kernel Remembers About a Process

Because many processes share one CPU, the kernel must be able to stop a process and later resume it exactly where it left off. It keeps a record for each one: the **process control block** (PCB), also called a *process descriptor*, which Wikipedia describes as a data structure the operating system uses to store all the information about a process. The kernel creates it when the process is created, keeps all the PCBs in a *process table*, and holds them in memory that ordinary programs cannot touch ([Wikipedia: Process control block](https://en.wikipedia.org/wiki/Process_control_block)). Details differ between systems, but the contents fall into a few groups:

| What the kernel tracks | Examples | A window from Python |
|------------------------|----------|----------------------|
| **Identity** | Process id, parent's process id, owner (user and group ids) | `os.getpid()`, `os.getppid()`, `os.getuid()` |
| **State and CPU context** | Process state, program counter, registers, stack pointer | Not visible to the process itself; the kernel saves them while the process is not running |
| **Scheduling information** | Priority, CPU time used, the queue the process waits in | `os.nice(0)`, `resource.getrusage()` |
| **Memory map** | Page tables, the layout of the address space, memory limits | `resource.getrlimit(resource.RLIMIT_STACK)` |
| **Open resources** | Open files and sockets (the *descriptor table*), current directory, environment | `os.listdir("/dev/fd")`, `os.getcwd()`, `os.environ` |
| **Accounting** | CPU time and other usage counters | `resource.getrusage()` |

The descriptor table is easy to watch. Every file a process opens takes one entry in it, and closing the file frees the entry (the listing of `/dev/fd` shows one name per open descriptor on both macOS and Linux):

```python
def descriptor_count():
    return len(os.listdir("/dev/fd"))

before = descriptor_count()
handles = [open("/etc/hosts") for _ in range(3)]
after = descriptor_count()
print("opening 3 files added", after - before, "entries to this process's descriptor table")
for handle in handles:
    handle.close()
print("closing them removed", after - descriptor_count())
```

```text
opening 3 files added 3 entries to this process's descriptor table
closing them removed 3
```

This is also why a program that forgets to close files eventually fails with "too many open files": the descriptor table, like every part of the PCB, has a limit.

## 🗺️ The Address Space

Every process gets its own **address space**: the range of memory addresses it believes it can use. A typical layout looks like this (the exact arrangement differs between operating systems and processors):

```
 high addresses   ┌─────────────────────────────┐
                  │ stack      (grows downward) │   function calls, local variables
                  │             ↓               │
                  │                             │
                  │             ↑               │
                  │ heap       (grows upward)   │   memory requested while running
                  ├─────────────────────────────┤
                  │ data                        │   global and static variables
                  ├─────────────────────────────┤
 low addresses    │ code (text)                 │   the program's instructions
                  └─────────────────────────────┘
```

The addresses are **virtual**: the hardware and the kernel translate them to real memory using the page tables recorded in the PCB, so the same virtual address in two processes can refer to different physical memory. That translation is what makes isolation possible (a process cannot even *name* another process's memory), and it is the subject of the [Memory Management](../memory-management/README.md) and [Virtual Memory](../virtual-memory/README.md) modules later in this section. The next experiment shows it directly, once `fork` has been introduced.

## 🍴 Creating a Process: fork, exec, and wait

Unix-style systems create processes with two separate calls:

1. **`fork()`** makes a new process that is a near-copy of the caller. Both processes continue from the point of the call, as if both had just called it, and each can look at the return value to find out which one it is: in the new **child** process the return value is zero (which is not a valid process id), while the **parent** receives the child's process id ([Wikipedia: fork (system call)](https://en.wikipedia.org/wiki/Fork_(system_call))).
2. **`exec()`** replaces the program running in the calling process with a different program. A successful call never returns, because the code that made it no longer exists ([Wikipedia: exec (system call)](https://en.wikipedia.org/wiki/Exec_(system_call))).

A third call, **`wait()`**, lets the parent sleep until a child ends and collect its **exit status**. The next block uses `fork` and `wait`, plus a pipe (a one-way channel between processes) through which the child reports back. It needs Python 3.9 or newer for `os.waitstatus_to_exitcode`:

```python
data = ["original"]
read_end, write_end = os.pipe()
pid = os.fork()
if pid == 0:
    # this branch runs only in the child: fork() returned 0 here
    data[0] = "changed by the child"
    os.write(write_end, f"{id(data)}|{data[0]}".encode())
    os._exit(7)                                     # end the child at once, with exit status 7
# this line runs only in the parent: fork() returned the child's process id
_, status = os.waitpid(pid, 0)                      # sleep until the child ends, then collect its status
child_address, child_view = os.read(read_end, 200).decode().split("|")
print("child's exit status:", os.waitstatus_to_exitcode(status))
print("same virtual address in both processes:", str(id(data)) == child_address)
print("parent's list:", data[0], "| child's list:", child_view)
```

```text
child's exit status: 7
same virtual address in both processes: True
parent's list: original | child's list: changed by the child
```

Three ideas are visible. The child ended with the status it chose, and the parent collected it. The list lives at the *same* virtual address in both processes (in CPython, `id()` is the object's address in memory), yet the child's change is invisible to the parent: the two address spaces are separate even though the addresses look identical. And no memory was copied just to make that true. A modern `fork` uses **copy-on-write**: the two processes initially point at the same physical pages, and a page is copied only when one of them writes to it ([Wikipedia: fork (system call)](https://en.wikipedia.org/wiki/Fork_(system_call))), which is why forking even a large process is fast.

On its own, `fork` only makes more copies of the same program. To run a *different* program, the child calls `exec`. The following block does exactly what a shell does when it runs a command whose output is redirected: it forks, rearranges the child's file descriptors with `dup2` so that standard output (descriptor 1) leads into the pipe, and only then replaces the child's program with a new one, here a shell that prints its own process id:

```python
read_end, write_end = os.pipe()
pid = os.fork()
if pid == 0:
    os.dup2(write_end, 1)                           # the child's standard output now leads into the pipe
    os.close(read_end)
    os.close(write_end)
    os.execv("/bin/sh", ["sh", "-c", "echo $$"])    # replace the child's program; never returns on success
    os._exit(127)                                   # reached only if exec failed
os.close(write_end)
printed = os.read(read_end, 100).decode().strip()
os.close(read_end)
_, status = os.waitpid(pid, 0)
print("the new program ran inside the same process:", printed == str(pid), "| exit code:", os.waitstatus_to_exitcode(status))
```

```text
the new program ran inside the same process: True | exit code: 0
```

The new program reported the process id that `fork` had returned to the parent: `exec` changed *what* the process runs, not *which process* it is. Its PID, its parent, and its open descriptors (including the redirected one) all survived, which is the reason Unix splits creation into two steps. Wikipedia describes the same pattern: to run a different program, a process first forks a copy of itself, the copy makes whatever changes to its environment the new program needs, and then it calls `exec` to overlay itself with that program ([Wikipedia: fork (system call)](https://en.wikipedia.org/wiki/Fork_(system_call))). Everything between the two calls, such as redirecting output or changing the current directory, is how shells build pipes and redirection. Python's `subprocess` module wraps this whole sequence in one friendly call, which is what the earlier blocks in this file used. Windows takes a different route: it has no `fork`, and a single call, `CreateProcess`, creates a new process and its primary thread ([Microsoft: CreateProcessA](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa)), which is why Python's `os.fork` is documented as available only on POSIX systems ([Python docs: `os.fork`](https://docs.python.org/3/library/os.html#os.fork)).

One warning from those documents is worth repeating. On macOS, `os.fork` is documented as unsafe when mixed with higher-level system APIs, and mixing `fork` with threads has never been safe on POSIX platforms: only the calling thread exists in the child, so a lock held by another thread at that moment stays locked forever. The examples in this module call `fork` from single-threaded programs and use only plain system calls; for everyday work, use `subprocess` (to run another program) or `multiprocessing` (to run Python functions in other processes).

## 🪦 How a Process Ends: Exit Status, Zombies, and Orphans

A process ends when it calls `exit` (or when a signal kills it). The kernel then releases its memory and open files, but it keeps a small record, the exit status, until the parent asks for it with `wait`. A child that has ended but has not yet been waited for is called a **zombie** (or *defunct*) process: it has completed execution but still has an entry in the process table, because the entry is what lets the parent read the exit status; once the parent has read it, the entry is removed ([Wikipedia: Zombie process](https://en.wikipedia.org/wiki/Zombie_process)). A zombie uses no CPU and almost no memory, but it holds on to its process id, and a parent that never waits leaks one process-table entry per child.

The `ps` command shows the state of each process as a short code, and `Z` means zombie. Here the child exits immediately while the parent is still busy:

```python
import time

def state_of(pid):
    return subprocess.run(["ps", "-o", "stat=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()

child = os.fork()
if child == 0:
    os._exit(0)                                     # the child finishes at once
time.sleep(0.2)                                     # the parent is busy and has not called wait yet
print("child ended, parent has not waited -> state:", state_of(child)[:1])
os.waitpid(child, 0)
print("after the parent waited -> state:", repr(state_of(child)))
```

```text
child ended, parent has not waited -> state: Z
after the parent waited -> state: ''
```

The opposite case is an **orphan**: a process whose parent has ended while it keeps running. A Unix-like system never leaves a process without a parent; the kernel immediately hands the orphan to a system process, an operation called *re-parenting* ([Wikipedia: Orphan process](https://en.wikipedia.org/wiki/Orphan_process)). The block below creates a middle process that starts a grandchild and exits at once; the grandchild waits until its original parent is gone and reports who its parent is now:

```python
read_end, write_end = os.pipe()
if os.fork() == 0:                                  # the middle process: starts a grandchild, then exits at once
    middle_pid = os.getpid()
    if os.fork() == 0:                              # the grandchild: wait until the middle process is gone
        while os.getppid() == middle_pid:
            time.sleep(0.01)
        os.write(write_end, str(os.getppid()).encode())
        os._exit(0)
    os._exit(0)
os.close(write_end)
os.wait()                                           # collect the middle process; the grandchild is now an orphan
new_parent = int(os.read(read_end, 20))
os.close(read_end)
print("the orphan was adopted by process 1:", new_parent == 1)
```

```text
the orphan was adopted by process 1: True
```

Process 1 is the first user-space process started by the kernel (`launchd` on this Mac, as seen in [what-is-an-operating-system.md](../introduction-to-operating-systems/what-is-an-operating-system.md)). On macOS the adopter is process 1; some Linux systems choose another system process instead, because the exact adopter is implementation-defined.

## 🌳 The Process Tree

Because every process except the first has a parent, the processes on a machine form a **tree**: a shell is a child of a terminal, the programs you start are children of the shell, and everything leads back to process 1. Following the parent links from the current process proves it:

```python
def parent_of(pid):
    return int(subprocess.run(["ps", "-o", "ppid=", "-p", str(pid)], capture_output=True, text=True).stdout)

chain = [os.getpid()]
while chain[-1] > 1:
    chain.append(parent_of(chain[-1]))
print("this process has at least one ancestor:", len(chain) >= 2, "| the chain ends at process 1:", chain[-1] == 1)
```

```text
this process has at least one ancestor: True | the chain ends at process 1: True
```

To see the whole tree on your own machine, list every process with its parent:

```bash
ps -A -o pid,ppid,stat,comm
```

## Common Misconceptions

- **"A program and a process are the same thing."** A program is a passive file; a process is an executing instance with its own state. One program can be several processes, and one process can run several programs over its life (through `exec`).
- **"`fork` copies all of the parent's memory immediately."** Modern systems copy a page only when one of the two processes writes to it, which is why `fork` is cheap even for big processes.
- **"After `exec` the process is a new process."** It keeps its process id, parent, and open descriptors; only the program and the address space it runs are replaced.
- **"A zombie is a process that is still running."** It has finished. What remains is a table entry holding the exit status until the parent collects it; killing a zombie does nothing, and the fix is for the parent to call `wait` (or for the parent to end, after which the system process that adopts the zombie collects it). The `kill` command has no effect on a zombie, because there is nothing left to kill ([Wikipedia: Zombie process](https://en.wikipedia.org/wiki/Zombie_process)).
- **"If a parent process ends, its children end too."** On Unix they continue as orphans and are adopted by a system process, as the experiment above showed. (A terminal closing can send its programs a hangup signal, but that is a separate mechanism.)

## ➡️ Next

Continue to [what-is-a-thread.md](what-is-a-thread.md): a process is the unit that owns resources, but it is not the unit the kernel schedules. Threads are the lines of execution inside a process, and they change what is shared and what is private.
