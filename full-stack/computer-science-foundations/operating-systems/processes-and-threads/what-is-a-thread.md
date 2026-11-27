# 🧵 What Is a Thread?

## Lines of Execution Inside a Process

[what-is-a-process.md](what-is-a-process.md) described the process as the operating system's unit of *ownership*: it owns an address space, open files, and the other resources the kernel tracks. A **thread** is the unit of *execution* inside it. A thread of execution is the smallest stream of instructions that a scheduler can manage on its own, and at the kernel level the division of labour is simple: the process owns the resources, and the thread is what gets scheduled and executed ([Wikipedia: Thread (computing)](https://en.wikipedia.org/wiki/Thread_(computing))).

Think of a process as a kitchen and the threads as cooks working in it at the same moment. The cooks share the stove, the fridge, and the pantry (the memory and the open files), but each cook has their own place in the recipe and their own scratch pad of half-finished work (a program counter, registers, and a stack). Every process has at least one thread, the one that starts running `main`; a process that creates more is **multithreaded**.

```
 One process with three threads

 ┌────────────────────────────────────────────────────────────┐
 │  Shared by every thread                                    │
 │  code · global data · heap · open files · process id       │
 ├──────────────────┬──────────────────┬──────────────────────┤
 │ Thread 1         │ Thread 2         │ Thread 3             │
 │ own stack        │ own stack        │ own stack            │
 │ own registers    │ own registers    │ own registers        │
 │ own thread id    │ own thread id    │ own thread id        │
 └──────────────────┴──────────────────┴──────────────────────┘
```

All code in this file was run on CPython 3.9 on a Mac (macOS, Apple silicon). Timings depend on the machine and are labelled; everything else is the same on Linux.

## 🎯 Why Threads Exist

- **Responsiveness.** One thread can keep a window or a server accepting requests while another does slow work.
- **Overlapping waits.** While one thread waits for a disk, a network, or a person, another can compute. A waiting thread costs no CPU time (as measured in [kernel-and-user-mode.md](../introduction-to-operating-systems/kernel-and-user-mode.md)), so the processor is free for the others.
- **Using several cores.** The kernel can run different threads of one process on different cores at the same time. (In CPython this is limited by the global interpreter lock, covered below.)
- **Cheap sharing.** Threads read and write the same memory, so handing data between them needs no copying and no system call, unlike separate processes ([process-vs-thread.md](process-vs-thread.md)).

## 🔬 Threads in Python

Python's `threading` module creates real operating-system threads. The first experiment starts three worker threads and asks each one for its process id and its **thread id**. A barrier keeps all three alive until every one has reported, so that the operating system cannot reuse a finished thread's id for the next one (the documentation warns that the operating system may reuse a thread id once its thread has ended):

```python
import os
import threading
import time

seen = {}
barrier = threading.Barrier(3)

def report(name):
    seen[name] = (os.getpid(), threading.get_native_id())
    barrier.wait()                                  # keep every worker alive until all have reported

workers = [threading.Thread(target=report, args=(f"worker-{i}",)) for i in range(3)]
for worker in workers:
    worker.start()
for worker in workers:
    worker.join()
seen["main"] = (os.getpid(), threading.get_native_id())

process_ids = {pid for pid, _ in seen.values()}
thread_ids = {tid for _, tid in seen.values()}
print("threads that reported:", len(seen), "| distinct process ids:", len(process_ids), "| distinct thread ids:", len(thread_ids))
print("the shared process id is this process's own:", process_ids == {os.getpid()})
```

```text
threads that reported: 4 | distinct process ids: 1 | distinct thread ids: 4
the shared process id is this process's own: True
```

Four threads (three workers and the main thread) live in one process: they share a single process id but each has its own thread id. The documentation describes a thread's `native_id` as the thread id assigned by the operating-system kernel ([Python docs: `threading`](https://docs.python.org/3/library/threading.html)), which tells us that each `threading.Thread` is a **kernel thread**: the kernel knows about it and schedules it, exactly as it schedules a process's first thread.

## 🤝 What Threads Share and What They Keep Private

| Shared by all threads of a process | Private to each thread |
|------------------------------------|------------------------|
| The program's code | The **stack**: the chain of function calls and every local variable |
| Global and static variables | The **registers**, including the program counter (where this thread is in the code) |
| The heap: objects created while the program runs (in Python, every object) | The thread id |
| Open files and sockets | Thread-local storage, if the program uses it |
| The process id and the address space | |

The rule, as Wikipedia states it, is that the threads of a process share the process's code, its dynamically allocated data, and its global variables, except those declared thread-local ([Wikipedia: Thread (computing)](https://en.wikipedia.org/wiki/Thread_(computing))). The next block makes the difference concrete. Four threads each count to 1,000. Each thread has a *local* counter of its own, and all four add to one *shared* total. The shared total sits behind a lock, because two threads updating the same value at the same moment can lose an update ([race-conditions.md](../deadlocks-and-concurrency/race-conditions.md) in the [Deadlocks and Concurrency](../deadlocks-and-concurrency/README.md) module shows why):

```python
shared = {"total": 0}
lock = threading.Lock()
own_counts = {}

def count_to(n, name):
    own = 0                                         # a local variable: lives on this thread's own stack
    for _ in range(n):
        own += 1
        with lock:                                  # the shared total lives on the heap, so it needs protection
            shared["total"] += 1
    own_counts[name] = own

threads = [threading.Thread(target=count_to, args=(1000, f"t{i}")) for i in range(4)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
print("each thread's own counter:", sorted(own_counts.values()), "| the shared total:", shared["total"])
```

```text
each thread's own counter: [1000, 1000, 1000, 1000] | the shared total: 4000
```

The local counters are independent (each ends at 1,000, none affected by the others), while the shared total is the sum of everyone's work (4,000). Sharing is what makes threads convenient, and also what makes them dangerous: every shared value is something that more than one thread may touch at once.

Sometimes a program wants a variable that *looks* global but is private to each thread, such as a per-request context in a server. That is **thread-local storage**: data that appears global to the program but is kept separately for each thread ([Wikipedia: Thread-local storage](https://en.wikipedia.org/wiki/Thread-local_storage)). Python provides it as `threading.local()`:

```python
local = threading.local()
results = []

def remember(value):
    local.value = value                             # looks like a shared attribute, but each thread has its own copy
    time.sleep(0.01)                                # give the other threads time to set theirs
    results.append(local.value == value)

threads = [threading.Thread(target=remember, args=(i,)) for i in range(5)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
print("every thread still saw its own value:", all(results), "| the main thread has none:", not hasattr(local, "value"))
```

```text
every thread still saw its own value: True | the main thread has none: True
```

## 🧱 Kernel Threads and User Threads

Not every "thread" is something the kernel knows about. Wikipedia distinguishes **kernel threads**, which the operating system schedules, from **user threads**, which a runtime library schedules in user space. User threads may be mapped onto kernel threads in several ways: one-to-one, many-to-one, or many-to-many ([Wikipedia: Thread (computing)](https://en.wikipedia.org/wiki/Thread_(computing))).

| Kind | Who schedules it | Can use several cores at once | Typical example |
|------|------------------|-------------------------------|-----------------|
| **Kernel thread** (one-to-one) | The operating system's scheduler | Yes | A Python `threading.Thread` (it has a kernel-assigned thread id, as shown above) |
| **User-level thread** (many-to-one) | A library or runtime inside one kernel thread | Normally no | Generators and coroutines scheduled by your own code, built in [context-switching.md](context-switching.md) |
| **Hybrid** (many-to-many) | A runtime that spreads many user threads over a few kernel threads | Yes | Language runtimes that multiplex lightweight tasks over a pool of kernel threads |

A **green thread** is a thread scheduled by a language runtime or virtual machine rather than by the operating system, and managed entirely in user space ([Wikipedia: Green thread](https://en.wikipedia.org/wiki/Green_thread)). Because the kernel does not see them, switching between them is far cheaper than a kernel context switch. The price is that a blocking system call made by one of them blocks the kernel thread that they all share, and, as Wikipedia notes, green-thread implementations normally cannot spread work over several processors the way native threads can.

## ⏳ Threads and Waiting

The most common reason to use threads in Python is to overlap *waiting*. The block below waits 0.1 seconds ten times, first one after another, then in ten threads at once. The waiting stands in for a network request, a disk read, or a database query:

```python
def wait_a_tenth():
    time.sleep(0.1)

start = time.perf_counter()
for _ in range(10):
    wait_a_tenth()
one_after_another = time.perf_counter() - start

start = time.perf_counter()
threads = [threading.Thread(target=wait_a_tenth) for _ in range(10)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
together = time.perf_counter() - start
print(f"10 waits of 0.1 s one after another: {one_after_another:.2f} s | in 10 threads: {together:.2f} s")
```

One run on the test machine printed:

```
10 waits of 0.1 s one after another: 1.03 s | in 10 threads: 0.11 s
```

The ten threads finish in about the time of one wait, because each thread spends its time blocked in the kernel and costs no CPU while it does. Creating a new thread for every tiny task is wasteful, though, so programs usually keep a **thread pool**: a fixed set of worker threads that stay alive and take tasks as they arrive, which avoids paying for the creation and destruction of a thread for each short job ([Wikipedia: Thread pool](https://en.wikipedia.org/wiki/Thread_pool)). Python's standard library offers one in `concurrent.futures`:

```python
from concurrent.futures import ThreadPoolExecutor

used = set()

def square_slowly(n):
    used.add(threading.get_ident())
    time.sleep(0.1)                                 # stands in for slow I/O
    return n * n

start = time.perf_counter()
with ThreadPoolExecutor(max_workers=4) as pool:
    answers = list(pool.map(square_slowly, range(8)))
elapsed = time.perf_counter() - start
print("answers, in order:", answers)
print("distinct threads used:", len(used), "| threads left running afterwards:", threading.active_count() - 1)
print(f"8 tasks of 0.1 s on 4 pool threads took {elapsed:.2f} s")
```

One run on the test machine printed:

```
answers, in order: [0, 1, 4, 9, 16, 25, 36, 49]
distinct threads used: 4 | threads left running afterwards: 0
8 tasks of 0.1 s on 4 pool threads took 0.20 s
```

Eight tasks and four threads need two rounds of waiting, so the whole job takes about 0.2 seconds, and the answers still come back in the order of the inputs. When the `with` block ends, the pool's threads are shut down, leaving only the main thread (`threading.active_count()` counts it, hence the subtraction).

## 🔒 The Global Interpreter Lock

There is a catch for programs that compute rather than wait. CPython, the standard Python interpreter, has a **global interpreter lock** (GIL): a lock inside the interpreter that lets only one native thread per process execute its basic operations, such as memory allocation and reference counting, at any moment ([Wikipedia: Global interpreter lock](https://en.wikipedia.org/wiki/Global_interpreter_lock)). The Python documentation spells out the consequence: in CPython only one thread runs Python code at a time, so programs that want to use several cores should turn to `multiprocessing` or `concurrent.futures.ProcessPoolExecutor`, while threads remain a good fit for running several I/O-bound tasks at once ([Python docs: `threading`](https://docs.python.org/3/library/threading.html)).

That sentence matches the experiments: waiting threads overlap, because a blocked thread does not need the lock, but threads that all want to run Python code take turns. [process-vs-thread.md](process-vs-thread.md) measures the difference. Note that this is a property of one implementation, not of threads in general: starting with Python 3.13, CPython offers an optional free-threaded build in which the GIL is disabled ([Python docs: Python support for free threading](https://docs.python.org/3/howto/free-threading-python.html)). The measurements in this module use the standard build, with the GIL.

## Common Misconceptions

- **"More threads always make a program faster."** They help when there is waiting to overlap or idle cores to use, and when the language allows true parallel execution. Threads that all compute in CPython take turns, and every extra thread adds scheduling work.
- **"Python threads are fake."** They are real operating-system threads with kernel-assigned ids. The GIL restricts how many of them run Python code at one instant; it does not make them pretend.
- **"Each thread has its own copy of the global variables."** Globals and the heap are shared. Only the stack (local variables), the registers, and explicit thread-local storage are private.
- **"A thread is a small process."** A thread lives *inside* a process and shares its address space; a process is the container that owns the resources. A crash in one thread can take down the entire process, as [process-vs-thread.md](process-vs-thread.md) demonstrates.
- **"Sharing data between threads is free."** Reading is cheap, but any value that threads *modify* needs coordination with locks or similar tools, and getting that wrong produces bugs that appear only occasionally. The [Deadlocks and Concurrency](../deadlocks-and-concurrency/README.md) module of this section studies them.

## ➡️ Next

Continue to [process-vs-thread.md](process-vs-thread.md): processes and threads side by side, with measurements of what each costs to create, how they communicate, what happens when one of them fails, and which one speeds up work that computes.
