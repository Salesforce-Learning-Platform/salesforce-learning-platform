# 🧵 Processes and Threads

## 📚 Overview

The process is the operating system's central idea. Every program you run becomes one or more **processes**, each with its own memory, open files, and place in the code, and inside each process run one or more **threads**, the units the kernel actually schedules onto CPU cores. Understanding the difference, and the cost of each, is what lets you answer practical questions: why a web browser starts a separate process for each site, why a database server forks a process for each connection, why four Python threads can be no faster than one, and what a computer is doing when it appears to run hundreds of programs on a handful of cores.

This module follows a process from birth to exit and then widens to the threads inside it. It explains what a **process** is and what the kernel records about it (the process control block and the address space); how Unix-style systems create one with `fork` and `exec`, and how a process ends, including zombies and orphans; what a **thread** is, what threads share and what they keep private, and the **global interpreter lock** in CPython; a side-by-side comparison of processes and threads, measured for creation cost, communication cost, CPU-bound work, and failure scope; the **five-state model** of a process, with a simulator that checks every transition; and **context switching**, with the kernel's own switch counters, the cost of a switch, and a cooperative scheduler built from generators. Every code example was run on CPython 3.9 on a Mac (macOS, Apple silicon); the examples that use `fork` need Linux or macOS, and where output depends on the machine the text says so. The claims about operating-system design are checked against the cited sources, and the process-state simulator was verified against its invariants on thousands of random scripts.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Distinguish a program from a process, and describe what the kernel stores about each process in its process control block and what an address space contains.
- Create and run processes with `fork`, `exec`, and `wait`; explain copy-on-write, why `exec` keeps the process id, and how zombie and orphan processes arise and are cleaned up.
- Define a thread, list what threads of one process share and what each keeps private, and tell kernel threads from user-level (green) threads.
- Explain what the global interpreter lock does in CPython, why it matters for CPU-bound code but not for waiting, and when to use threads, processes, or lightweight tasks.
- Compare processes and threads using measurements of creation cost, communication cost, parallel speed-up, and what happens when something fails, and apply that comparison to real systems such as PostgreSQL, Chromium, and Apache.
- Describe the five process states and the six legal transitions, read the state letters printed by `ps`, and explain why a waiting process becomes ready, never running, when its event arrives.
- Explain what a context switch saves and restores, tell voluntary from involuntary switches (and a mode switch from a context switch), and reason about the cost of switching and the trade-off in choosing a time slice.

## 📋 Prerequisites

- [Introduction to Operating Systems](../introduction-to-operating-systems/README.md): system calls, kernel and user mode, and the idea that a blocked process uses no CPU.
- [Preparing Your Machine](../../../frontend/foundations/preparing-your-machine/README.md): a working terminal and Python installation for running the examples.
- Basic Python reading ability: functions, loops, dictionaries, and the standard library (`os`, `threading`, `subprocess`, `time`).
- No earlier knowledge of concurrency is assumed.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [what-is-a-process.md](what-is-a-process.md) | Program versus process, the process control block, the address space, `fork`, `exec`, and `wait` demonstrated from Python, zombies, orphans, and the process tree |
| [what-is-a-thread.md](what-is-a-thread.md) | Threads inside a process, what is shared and what is private, thread-local storage, kernel versus user threads, overlapping waits, thread pools, and the global interpreter lock |
| [process-vs-thread.md](process-vs-thread.md) | A comparison table and five measured experiments: shared versus separate memory, creation cost, communication cost, CPU-bound work, and crash scope; how PostgreSQL, Chromium, and Apache choose; a decision guide |
| [process-states.md](process-states.md) | The five-state model and its six transitions, reading `ps` state codes on a live system, and a process-state simulator that checks every move |
| [context-switching.md](context-switching.md) | What a context switch saves, what triggers one, voluntary and involuntary switches counted from Python, the direct and indirect cost, user-level switching with generators, and the time-slice trade-off |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [process-vs-thread.md](process-vs-thread.md) first if you are preparing for interviews or designing a concurrent system: the comparison table, the global interpreter lock, and the question of when to use which tool come up constantly, and the experiments show the numbers behind the folklore. [process-states.md](process-states.md) is the usual source of exam questions about the five-state model and the legal transitions.

**Skim** [what-is-a-process.md](what-is-a-process.md) if you already know `fork` and `exec` from a systems course, but run its zombie and orphan examples on your own machine. Treat [context-switching.md](context-switching.md) as the bridge to the CPU Scheduling module: read the counting experiment and the time-slice table, and skim the rest unless you care about the cost of switching in detail.

## 🧠 Knowledge Check

<details>
<summary>A Python program starts four threads that each run the same long, purely computational loop, and it finishes no faster than one thread doing all four jobs. Why, and what would you change?</summary>

CPython has a **global interpreter lock**: only one thread per process can run Python code at any instant, so four computing threads simply take turns on one core, and the extra threads add scheduling work without adding speed. In the measurements in [process-vs-thread.md](process-vs-thread.md), four threads took as long as running the four jobs one after another, while four processes, each with its own interpreter and its own lock, finished in little more than the time of a single job. To speed up CPU-bound work, use processes (`multiprocessing` or `concurrent.futures.ProcessPoolExecutor`). Threads remain the right tool when the tasks mostly *wait* (network, disk, database), because a waiting thread releases the lock and the waits overlap, as shown in [what-is-a-thread.md](what-is-a-thread.md).

</details>

<details>
<summary>A process is waiting for a disk read, and the read completes. Which state does the process enter, and why is it not running at once?</summary>

It enters the **ready** state. A finished I/O operation (typically signalled by an interrupt) only tells the kernel that the event the process was waiting for has happened, so the process becomes eligible to run; it still has to wait in the ready queue for the scheduler to dispatch it, because only the scheduler moves a process from ready to running, and a core may be busy with another process. The path is therefore waiting → ready → running, never waiting → running directly, as the transition table and the simulator in [process-states.md](process-states.md) show. In that file's timeline, for example, process B becomes ready at tick 7 when its I/O finishes, but is not dispatched until tick 9.

</details>

## 📚 References

- [Wikipedia: Process (computing)](https://en.wikipedia.org/wiki/Process_(computing)), [Process control block](https://en.wikipedia.org/wiki/Process_control_block), [Process state](https://en.wikipedia.org/wiki/Process_state), [Zombie process](https://en.wikipedia.org/wiki/Zombie_process), and [Orphan process](https://en.wikipedia.org/wiki/Orphan_process): what a process is, how the kernel tracks it, and how it ends.
- [Wikipedia: fork (system call)](https://en.wikipedia.org/wiki/Fork_(system_call)), [exec (system call)](https://en.wikipedia.org/wiki/Exec_(system_call)), and [Copy-on-write](https://en.wikipedia.org/wiki/Copy-on-write): creating processes on Unix-like systems.
- [Wikipedia: Thread (computing)](https://en.wikipedia.org/wiki/Thread_(computing)), [Green thread](https://en.wikipedia.org/wiki/Green_thread), [Coroutine](https://en.wikipedia.org/wiki/Coroutine), [Thread-local storage](https://en.wikipedia.org/wiki/Thread-local_storage), [Thread pool](https://en.wikipedia.org/wiki/Thread_pool), and [Global interpreter lock](https://en.wikipedia.org/wiki/Global_interpreter_lock): threads and the models for implementing them.
- [Wikipedia: Context switch](https://en.wikipedia.org/wiki/Context_switch), [Preemption (computing)](https://en.wikipedia.org/wiki/Preemption_(computing)), and [Translation lookaside buffer](https://en.wikipedia.org/wiki/Translation_lookaside_buffer): what a switch involves and what it costs.
- [Python docs: `os.fork`](https://docs.python.org/3/library/os.html#os.fork), [`threading`](https://docs.python.org/3/library/threading.html), [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html), [`concurrent.futures`](https://docs.python.org/3/library/concurrent.futures.html), [`resource`](https://docs.python.org/3/library/resource.html), [`subprocess`](https://docs.python.org/3/library/subprocess.html), and [Python support for free threading](https://docs.python.org/3/howto/free-threading-python.html): the standard-library tools used in the experiments.
- Linux manual pages: [`ps(1)`](https://man7.org/linux/man-pages/man1/ps.1.html) (process state codes), [`fork(2)`](https://man7.org/linux/man-pages/man2/fork.2.html), [`execve(2)`](https://man7.org/linux/man-pages/man2/execve.2.html), [`wait(2)`](https://man7.org/linux/man-pages/man2/wait.2.html), and [`getrusage(2)`](https://man7.org/linux/man-pages/man2/getrusage.2.html) (context-switch counters).
- Real systems: [PostgreSQL: How Connections Are Established](https://www.postgresql.org/docs/current/connect-estab.html), [Chromium: Multi-process Architecture](https://www.chromium.org/developers/design-documents/multi-process-architecture/), [Apache HTTP Server: Multi-Processing Modules](https://httpd.apache.org/docs/2.4/mpm.html), and [Microsoft: CreateProcessA](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa).
- *Operating Systems: Three Easy Pieces*, free chapters: [The Abstraction: The Process](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-intro.pdf), [Interlude: Process API](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-api.pdf), [Mechanism: Limited Direct Execution](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-mechanisms.pdf) (context switches), and [Concurrency: An Introduction](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-intro.pdf) (threads).
- [GeeksforGeeks: Introduction of Process Management](https://www.geeksforgeeks.org/operating-systems/introduction-of-process-management/), [Process vs Thread](https://www.geeksforgeeks.org/operating-systems/difference-between-process-and-thread/), [States of a Process in Operating Systems](https://www.geeksforgeeks.org/operating-systems/states-of-a-process-in-operating-systems/), [Context Switching in Operating System](https://www.geeksforgeeks.org/operating-systems/context-switch-in-operating-system/), and [Zombie and Orphan Processes in C](https://www.geeksforgeeks.org/c/zombie-and-orphan-processes-in-c/): overviews and practice questions.

## ➡️ Continue Your Learning Path

Continue to the CPU Scheduling module, the next module in this section: with many processes and threads ready to run, it studies how the kernel decides which one gets the CPU next, and why first-come-first-served, shortest-job-first, round-robin, and priority scheduling suit different goals.
