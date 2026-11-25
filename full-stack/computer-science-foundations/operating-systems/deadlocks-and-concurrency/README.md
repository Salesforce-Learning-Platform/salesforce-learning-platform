# 🔒 Deadlocks and Concurrency

## 📚 Overview

The previous modules made it possible to run many activities at once: processes and threads, a scheduler to share the CPU among them, and memory that threads of one process share. This module is about the price of that sharing. When several threads touch the same data, the result can depend on the exact order in which the scheduler happens to interleave their steps, and a bug that appears in one schedule out of a million will, sooner or later, appear in production. The rest of the module is a tour of that problem and its solutions: the failure (**race conditions**), the cure (**mutexes and semaphores**), the new failure the cure creates (**deadlock**), and the ways of living with it (**prevention, avoidance, and detection**).

The module starts with the basic ideas: concurrency versus parallelism, why the number of possible interleavings explodes, why one line of source code is not one atomic step, and the three broad ways of cooperating (shared memory with locks, message passing, and not sharing). It then examines **race conditions** both exhaustively and on real threads, with a small tool that tries *every* schedule of a set of thread programs, and with lost updates and overdrawn bank accounts reproduced on purpose. It introduces **locks, semaphores, and the bounded buffer**, measures what a lock costs and what spinning wastes, and shows why a lock in the wrong place protects nothing. It explains **deadlock** through the four Coffman conditions, a wait-for graph, and the dining philosophers, and distinguishes it from livelock and starvation. And it closes with **prevention** (lock ordering and try-both locking), **avoidance** (the banker's algorithm), and **detection and recovery**. Every code example was run on CPython 3.9 on a Mac (macOS, Apple silicon); timing-dependent results are labelled, the model checkers and algorithms are deterministic, and each was tested against an independent exhaustive method on thousands of random inputs.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Distinguish concurrency from parallelism, explain why the number of thread interleavings grows explosively, and explain why a statement such as `counter += 1` is not atomic.
- Define a race condition, reproduce a lost update and a check-then-act race, and explain why such bugs are nondeterministic and hard to find.
- Use a mutex to protect a whole critical section (and show that a lock around only part of it protects nothing), and explain mutual exclusion, progress, and bounded waiting.
- Use counting and binary semaphores to limit concurrency, to signal between threads, and to build a bounded buffer, and explain how mutexes and semaphores differ.
- State the four Coffman conditions for deadlock, find a deadlock by exhaustive search, recognise it as a cycle in a wait-for graph, and distinguish it from livelock and starvation.
- Prevent deadlock by removing a condition (especially by imposing a global lock order), avoid it with the banker's algorithm, and detect and recover from it.
- Choose a practical strategy for a real program, a database, or an operating system.

## 📋 Prerequisites

- [Processes and Threads](../processes-and-threads/README.md): especially [what-is-a-thread.md](../processes-and-threads/what-is-a-thread.md), the shared state of threads, and the interpreter lock in CPython.
- [CPU Scheduling](../cpu-scheduling/README.md): the scheduler that creates the interleavings, and the idea of priorities.
- Basic Python reading ability: classes, closures, the `threading` module at an introductory level, and the standard library.
- No earlier knowledge of synchronization is assumed.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [understanding-concurrency.md](understanding-concurrency.md) | Concurrency versus parallelism, interleavings and how many there are, atomicity and the bytecode of `counter += 1`, the three ways to share work, and the failure modes |
| [race-conditions.md](race-conditions.md) | The lost update and check-then-act races, a schedule explorer that tries every interleaving, forced and natural races on real threads, and how to fix and detect them |
| [mutex-and-semaphores.md](mutex-and-semaphores.md) | Critical sections, locks and what they cost, spinning versus blocking, reentrant locks, counting and binary semaphores, the bounded buffer, and priority inversion |
| [deadlocks.md](deadlocks.md) | The Coffman conditions, finding a deadlock by exhaustive search, wait-for graphs and cycle detection, the dining philosophers, livelock and starvation, and deadlocks in real systems |
| [deadlock-prevention.md](deadlock-prevention.md) | Prevention by removing a condition (lock ordering, try-both locking), avoidance with the banker's algorithm, detection and recovery, and practical guidance |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [race-conditions.md](race-conditions.md) and [deadlocks.md](deadlocks.md) first if you are preparing for interviews: the lost update, the four Coffman conditions, and the dining philosophers are the standard questions, and running the explorer yourself, changing the programs and watching the counts change, is the quickest way to understand why a "rare" bug is certain to occur in production. [mutex-and-semaphores.md](mutex-and-semaphores.md) is the one to master for writing concurrent code.

**Skim** [understanding-concurrency.md](understanding-concurrency.md) if you have written multithreaded code before, but run its interleaving count and bytecode listing; and skim the banker's-algorithm part of [deadlock-prevention.md](deadlock-prevention.md) unless you are studying for an exam, since real systems seldom use avoidance, while lock ordering and timeouts are used everywhere.

## 🧠 Knowledge Check

<details>
<summary>Two threads each run `counter += 1` a thousand times on a shared counter without any synchronization, and the program sometimes prints less than 2,000. Why, and how do you fix it?</summary>

`counter += 1` is a read-modify-write sequence of several steps (load the value, add 1, store the result), and the scheduler can switch threads between any two of them. If thread B loads the counter after thread A has loaded it but before A has stored its result, both compute from the same old value, and one of the two increments is lost: a **race condition**. The result depends on the interleaving, so it varies from run to run (in the experiment in [race-conditions.md](race-conditions.md), four threads got totals from about half of the correct value up to the correct value). The fix is **mutual exclusion**: put the entire read-modify-write inside a critical section guarded by a lock (`with lock: counter += 1`), as in [mutex-and-semaphores.md](mutex-and-semaphores.md), where the same experiment returned the exact total every time. Message passing or per-thread counters that are combined at the end also avoid the problem.

</details>

<details>
<summary>Name the four conditions that must hold for a deadlock, and say which one is the easiest to remove in practice and how.</summary>

The four Coffman conditions are **mutual exclusion** (resources are held exclusively), **hold and wait** (a thread holds some resources while waiting for others), **no preemption** (a resource can be released only by its holder), and **circular wait** (a cycle of threads, each waiting for a resource held by the next). Deadlock cannot occur if any one of them is made impossible. The easiest to remove in practice is **circular wait**, by giving every lock a number and requiring all code to acquire locks in increasing order: a thread that is waiting then holds only lower-numbered locks than the one it waits for, so the chain of waits can never come back round on itself. The bank-transfer and dining-philosophers experiments in [deadlocks.md](deadlocks.md) and [deadlock-prevention.md](deadlock-prevention.md) showed deadlocks in a third of the schedules (two threads) or a vanishing fraction of them (five philosophers) with the naive order, and in none with the ordered one.

</details>

## 📚 References

- [Wikipedia: Concurrent computing](https://en.wikipedia.org/wiki/Concurrent_computing), [Race condition](https://en.wikipedia.org/wiki/Race_condition), [Mutual exclusion](https://en.wikipedia.org/wiki/Mutual_exclusion), [Critical section](https://en.wikipedia.org/wiki/Critical_section), [Lock (computer science)](https://en.wikipedia.org/wiki/Lock_(computer_science)), [Semaphore (programming)](https://en.wikipedia.org/wiki/Semaphore_(programming)), [Monitor (synchronization)](https://en.wikipedia.org/wiki/Monitor_(synchronization)), [Producer–consumer problem](https://en.wikipedia.org/wiki/Producer%E2%80%93consumer_problem), [Test-and-set](https://en.wikipedia.org/wiki/Test-and-set), and [Compare-and-swap](https://en.wikipedia.org/wiki/Compare-and-swap): concurrency, races, and synchronization primitives.
- [Wikipedia: Deadlock](https://en.wikipedia.org/wiki/Deadlock_(computer_science)), [Dining philosophers problem](https://en.wikipedia.org/wiki/Dining_philosophers_problem), [Banker's algorithm](https://en.wikipedia.org/wiki/Banker%27s_algorithm), [Resource starvation](https://en.wikipedia.org/wiki/Resource_starvation), [Priority inversion](https://en.wikipedia.org/wiki/Priority_inversion), and [Peterson's algorithm](https://en.wikipedia.org/wiki/Peterson%27s_algorithm): deadlock, its handling, and related failures.
- [Wikipedia: Therac-25](https://en.wikipedia.org/wiki/Therac-25) and [Northeast blackout of 2003](https://en.wikipedia.org/wiki/Northeast_blackout_of_2003): real accidents in which race conditions played a part.
- [Python docs: `threading`](https://docs.python.org/3/library/threading.html), [`queue`](https://docs.python.org/3/library/queue.html), [`faulthandler`](https://docs.python.org/3/library/faulthandler.html), and [`dis`](https://docs.python.org/3/library/dis.html): the tools used in the experiments.
- [PostgreSQL documentation: Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html) (deadlocks in a database) and [Linux kernel documentation: Runtime locking correctness validator](https://docs.kernel.org/locking/lockdep-design.html) (lockdep): deadlock handling in real systems.
- *Operating Systems: Three Easy Pieces*, free chapters: [Concurrency: An Introduction](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-intro.pdf), [Interlude: Thread API](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-api.pdf), [Locks](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-locks.pdf), [Condition Variables](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-cv.pdf), [Semaphores](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-sema.pdf), and [Common Concurrency Problems](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-bugs.pdf).
- [GeeksforGeeks: Process Synchronization](https://www.geeksforgeeks.org/operating-systems/introduction-of-process-synchronization/), [Race Condition Vulnerability](https://www.geeksforgeeks.org/operating-systems/race-condition-vulnerability/), [Semaphores](https://www.geeksforgeeks.org/operating-systems/semaphores-in-process-synchronization/), [Deadlock](https://www.geeksforgeeks.org/operating-systems/introduction-of-deadlock-in-operating-system/), [Banker's Algorithm](https://www.geeksforgeeks.org/operating-systems/bankers-algorithm-in-operating-system-2/), and [Dining Philosopher Solution using Semaphores](https://www.geeksforgeeks.org/operating-systems/dining-philosopher-problem-using-semaphores/): overviews and practice questions.

## ➡️ Continue Your Learning Path

Continue to the File Systems module, the next module in this section: the concurrency tools of this module protect memory and data structures inside a running program, and the file system is where the data that must outlive the program is kept, with its own versions of the same problems (concurrent access, consistency after a crash, and protection).
