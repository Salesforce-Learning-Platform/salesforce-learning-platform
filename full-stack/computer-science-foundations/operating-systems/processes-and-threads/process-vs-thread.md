# ⚖️ Process vs. Thread

## Two Answers to One Question

A program that wants to do several things at once has two tools, and they answer the question differently. **Processes** give each task its own address space, so the tasks are isolated from one another. **Threads** put the tasks inside one address space, so they share everything. Almost every difference between the two follows from that single choice: isolation costs more to set up and more to communicate across, but contains failures; sharing is cheap and fast, but lets one task's mistake damage all the others.

This file compares them side by side, first in a table and then with five experiments that measure each claim instead of just stating it. Every code example was run on CPython 3.9 on a Mac (macOS, Apple silicon, 11 logical CPUs); timings depend on the machine and are labelled, while the logic is the same on Linux. The examples that use `os.fork` need a Unix-like system, and they are written to run in a single-threaded program, as the warning in [what-is-a-process.md](what-is-a-process.md) advises. The code blocks are cumulative: each one uses the imports and helper functions defined in the blocks before it, so run them in order in one session or script. Timings in Experiment 2 are averages over many calls, and Experiments 3 and 4 report the best of three runs to reduce noise.

## 📋 The Comparison at a Glance

| | Process | Thread |
|--|---------|--------|
| **What it is** | A running program that owns resources | A line of execution inside a process |
| **Address space** | Its own, separated from every other process by the hardware | Shared with the other threads of the process |
| **Created by** | `fork` and `exec`, `subprocess`, `multiprocessing` | `threading.Thread`, `pthread_create` |
| **Cost to create** | Higher: a new address space, descriptor table, and kernel records | Lower: a stack and a small kernel record |
| **Communication** | Needs inter-process communication: pipes, sockets, shared-memory regions, messages | Reads and writes the same memory, coordinated with locks |
| **When one fails** | The others carry on; the parent can read its exit status | A fatal fault ends every thread in the process |
| **Switching between them** | Dearer: a different address space must be loaded | Cheaper: the address space stays the same |
| **Protection** | A real security boundary: different users, sandboxes | None between threads: they have the same rights and see the same memory |

The switching row rests on how a context switch works: the kernel loads the next process's memory map (its page tables) unless the two share memory, and when it does load a different map, the processor's cache of address translations (the *TLB*) may have to be flushed, which slows the memory accesses that follow (how much depends on the hardware); threads of one process share memory, so they can skip that step ([Wikipedia: Context switch](https://en.wikipedia.org/wiki/Context_switch)). [context-switching.md](context-switching.md) examines the switch itself.

## 🧪 Experiment 1: Shared or Separate Memory?

The first experiment changes a variable from a new thread and then from a new process. A thread shares the address space, so its change is visible; a forked child works on its own copy, so its change is not:

```python
import os
import queue
import subprocess
import sys
import threading
import time

counter = [0]

def bump():
    counter[0] += 1

thread = threading.Thread(target=bump)
thread.start()
thread.join()
print("after a thread added 1, this process sees:", counter[0])

pid = os.fork()
if pid == 0:
    bump()                                          # the child changes its own copy of the list
    os._exit(0)
os.waitpid(pid, 0)
print("after a forked child added 1, this process sees:", counter[0])
```

```text
after a thread added 1, this process sees: 1
after a forked child added 1, this process sees: 1
```

The thread's addition is there; the child's is not (the value is still 1, not 2). Isolation is the default between processes, which is why they need explicit channels, such as the pipes in Experiment 3, to exchange anything.

## 🧪 Experiment 2: What Does Creation Cost?

Starting a unit of work has a price, and the two tools differ by orders of magnitude. The next block times four ways of getting something new running and waiting for it to finish: a thread that does nothing, a forked process that exits at once, a forked process that also runs a new program (`true`, which does nothing and exits), and a brand-new Python interpreter:

```python
def make_thread():
    worker = threading.Thread(target=lambda: None)
    worker.start()
    worker.join()

def make_fork():
    pid = os.fork()
    if pid == 0:
        os._exit(0)
    os.waitpid(pid, 0)

def make_program():
    subprocess.run(["true"])

def make_interpreter():
    subprocess.run([sys.executable, "-c", "pass"])

def microseconds_per_call(function, calls):
    start = time.perf_counter()
    for _ in range(calls):
        function()
    return (time.perf_counter() - start) / calls * 1e6

for label, function, calls in (("a new thread (start and join)", make_thread, 2000),
                               ("a new process with fork (fork and wait)", make_fork, 300),
                               ("a new program, fork plus exec (true)", make_program, 200),
                               ("a new Python interpreter", make_interpreter, 30)):
    print(f"{label:<42} {microseconds_per_call(function, calls):9.0f} us")
```

One run on the test machine printed:

```
a new thread (start and join)                     29 us
a new process with fork (fork and wait)          844 us
a new program, fork plus exec (true)            1629 us
a new Python interpreter                       12256 us
```

A thread costs tens of microseconds. A forked process is already a few dozen times dearer, and a process that also loads a new program costs more again; starting a whole new interpreter, which must also initialise Python itself, takes milliseconds. This is why servers keep pools of long-lived workers instead of creating one per request, and why `fork` plus copy-on-write (see [what-is-a-process.md](what-is-a-process.md)) matters so much: it makes the second row far cheaper than building a process from nothing.

## 🧪 Experiment 3: What Does Communication Cost?

Threads have an obvious advantage here, because they can simply read each other's variables. The experiment measures that read, and then the price of *handing control* from one worker to another and back, which is what coordinating real work needs. It compares four things: reading a shared variable; two threads passing a lock back and forth; two threads exchanging a message through `queue.Queue`; and two processes exchanging a byte through a pair of pipes:

```python
def best_of(measure, repeats=3):
    return min(measure() for _ in range(repeats))

shared_value = [42]

def shared_read_us(reads=1_000_000):
    start = time.perf_counter()
    for _ in range(reads):
        shared_value[0]
    return (time.perf_counter() - start) / reads * 1e6

def lock_hand_off_us(rounds=20_000):
    go, back = threading.Lock(), threading.Lock()
    go.acquire()
    back.acquire()
    def echo():
        for _ in range(rounds):
            go.acquire()                            # wait for the main thread's signal
            back.release()                          # answer it
    worker = threading.Thread(target=echo)
    worker.start()
    start = time.perf_counter()
    for _ in range(rounds):
        go.release()
        back.acquire()
    elapsed = time.perf_counter() - start
    worker.join()
    return elapsed / rounds * 1e6

def queue_round_trip_us(rounds=20_000):
    ping, pong = queue.Queue(), queue.Queue()
    def echo():
        for _ in range(rounds):
            pong.put(ping.get())
    worker = threading.Thread(target=echo)
    worker.start()
    start = time.perf_counter()
    for _ in range(rounds):
        ping.put(1)
        pong.get()
    elapsed = time.perf_counter() - start
    worker.join()
    return elapsed / rounds * 1e6

def pipe_round_trip_us(rounds=20_000):
    to_child_r, to_child_w = os.pipe()
    to_parent_r, to_parent_w = os.pipe()
    pid = os.fork()
    if pid == 0:                                    # the child: echo every byte back
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

for label, measure in (("one read of a shared variable (loop included)", shared_read_us),
                       ("two threads hand a lock back and forth", lock_hand_off_us),
                       ("two threads exchange a message (queue.Queue)", queue_round_trip_us),
                       ("two processes exchange a byte (pipes)", pipe_round_trip_us)):
    print(f"{label:<48} {best_of(measure):9.3f} us")
```

One run on the test machine printed:

```
one read of a shared variable (loop included)        0.024 us
two threads hand a lock back and forth               5.109 us
two threads exchange a message (queue.Queue)         9.468 us
two processes exchange a byte (pipes)                6.480 us
```

The result has two parts. Sharing memory is dramatically cheaper than any message: a read of a shared variable takes a few hundredths of a microsecond, hundreds of times less than a round trip. But *waiting for another worker to respond* costs about the same for threads as for processes: the bare lock hand-off is in the same range as the pipe round trip, and `queue.Queue`, which adds Python-level locking on top, is slower still. Whatever the mechanism, the expensive part is putting one worker to sleep and waking another through the kernel's scheduler. The practical lesson is that threads win when they can work on shared data *without* constantly waiting for each other; a design in which threads ping-pong messages gains little over processes and gives up their isolation.

## 🧪 Experiment 4: Work That Computes

Creation and communication costs matter less when the work itself is large. For work that computes rather than waits, the question is whether the extra workers actually run in parallel. The block below runs the same CPU-bound function once; four times in a row; in four threads; and in four separate processes (four Python interpreters started with `subprocess`, each running the identical function). The function's source is kept in one string so that the parent and the workers run exactly the same code:

```python
BURN_SOURCE = """
def burn(n=5_000_000):
    total = 0
    for i in range(n):
        total += i * i
"""
exec(BURN_SOURCE)                                   # defines burn() in this process...
WORKER = BURN_SOURCE + "burn()\n"                   # ...and the same text is what each worker process runs

def timed(function):
    start = time.perf_counter()
    function()
    return time.perf_counter() - start

def four_threads():
    threads = [threading.Thread(target=burn) for _ in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def four_processes():
    workers = [subprocess.Popen([sys.executable, "-c", WORKER]) for _ in range(4)]
    for worker in workers:
        worker.wait()

one = best_of(lambda: timed(burn))
sequential = best_of(lambda: timed(lambda: [burn() for _ in range(4)]))
threads = best_of(lambda: timed(four_threads))
processes = best_of(lambda: timed(four_processes))
print(f"one task:                          {one:5.2f} s")
print(f"four tasks, one after another:     {sequential:5.2f} s")
print(f"four tasks in four threads:        {threads:5.2f} s")
print(f"four tasks in four processes:      {processes:5.2f} s")
```

One run on the test machine printed:

```
one task:                           0.19 s
four tasks, one after another:      0.76 s
four tasks in four threads:         0.76 s
four tasks in four processes:       0.22 s
```

Four threads take as long as running the four tasks one after another: the global interpreter lock lets only one of them execute Python code at a time ([what-is-a-thread.md](what-is-a-thread.md)), so the extra threads add no speed. Four processes finish in not much more than the time of a single task, because each has its own interpreter and its own lock and the kernel can run them on different cores at once (the figure includes starting four interpreters, a cost of about ten milliseconds each, as Experiment 2 showed). That is the advice in the Python documentation, in numbers: for CPU-bound work, use processes. In real code you would not start interpreters by hand; `multiprocessing` and `concurrent.futures.ProcessPoolExecutor` manage the workers, and the `multiprocessing` documentation describes the package as side-stepping the global interpreter lock by using subprocesses instead of threads ([Python docs: `multiprocessing`](https://docs.python.org/3/library/multiprocessing.html)). On macOS and Windows it starts each worker as a fresh interpreter by default (the `spawn` method), because forking is considered unsafe there.

## 🧪 Experiment 5: When Something Goes Wrong

The last experiment compares what a failure takes down with it. Each case runs in its own Python process, so the results can be observed from outside. A real driver or extension crash would typically be a memory fault; the experiment simulates a fatal failure with `os._exit(3)`, which ends a process immediately with exit status 3 and, unlike a genuine segmentation fault, does not make macOS open a crash-report window:

```python
programs = {
    "python exception in a thread": (
        "import threading, time\n"
        "threading.Thread(target=lambda: 1 / 0).start()\n"
        "time.sleep(0.3)\n"
        "print('main thread still alive')\n"),
    "fatal failure in a thread": (
        "import os, threading, time\n"
        "threading.Thread(target=lambda: os._exit(3)).start()\n"
        "time.sleep(0.3)\n"
        "print('main thread still alive')\n"),
    "fatal failure in a child process": (
        "import os\n"
        "if os.fork() == 0:\n"
        "    os._exit(3)\n"
        "_, status = os.wait()\n"
        "print('parent still alive; child exit code', os.waitstatus_to_exitcode(status))\n"),
}
for label, program in programs.items():
    result = subprocess.run([sys.executable, "-c", program], capture_output=True, text=True)
    print(f"{label:<34} -> exit code {result.returncode} | output {result.stdout.splitlines()} | traceback printed: {'Traceback' in result.stderr}")
```

```text
python exception in a thread       -> exit code 0 | output ['main thread still alive'] | traceback printed: True
fatal failure in a thread          -> exit code 3 | output [] | traceback printed: False
fatal failure in a child process   -> exit code 0 | output ['parent still alive; child exit code 3'] | traceback printed: False
```

An ordinary Python exception in a thread ends only that thread: the interpreter prints the traceback and the main thread carries on. A *fatal* failure is different. Anything that ends the process, such as an invalid memory access in native code, an out-of-memory kill, or here `os._exit`, takes every thread with it, because the process is the unit the kernel terminates, and the main thread never gets to print its line. The same failure in a *child process* ends only the child; the parent keeps running and can read the exit code, which is how supervisors detect a dead worker and restart it. This is the same containment argument made for microkernels in [os-architecture.md](../introduction-to-operating-systems/os-architecture.md).

## 🏗️ Real Systems Choose Differently

- **PostgreSQL** uses a "process per user" model: a supervisor process called the postmaster starts a new backend process for every client connection, so a misbehaving session cannot corrupt another's memory ([PostgreSQL documentation: How Connections Are Established](https://www.postgresql.org/docs/current/connect-estab.html)).
- **Chromium** is split into several process types because, as its design document explains, a rendering engine that never crashes, hangs, or has a security hole is nearly impossible to build; isolating pages in separate processes keeps one bad page from taking down the whole browser ([Chromium: Multi-process Architecture](https://www.chromium.org/developers/design-documents/multi-process-architecture/)).
- **Apache HTTP Server** lets the administrator choose: its multi-processing modules include `prefork`, suited to sites that value stability or compatibility with older software, and threaded modules such as `worker` and `event`, suited to sites that need a great deal of scalability ([Apache documentation: Multi-Processing Modules](https://httpd.apache.org/docs/2.4/mpm.html)). The same server software can be configured toward isolation or toward sharing.

## 🧭 Choosing Between Them

| Situation | Better fit | Why |
|-----------|------------|-----|
| Many tasks that mostly wait (network calls, disk, database queries) | Threads, or an event loop | The waits overlap; threads are cheap; CPython releases the interpreter lock while a thread is blocked |
| Heavy computation in CPython | Processes (`multiprocessing`, `ProcessPoolExecutor`) | Each process has its own interpreter and lock, so the cores run in parallel (Experiment 4) |
| Heavy computation in a language without a global lock | Threads | Real parallelism with shared data and cheap creation |
| Untrusted, crash-prone, or security-sensitive code | Processes | The address-space boundary contains crashes and attacks (Experiment 5) |
| Tasks that must share large amounts of changing data | Threads | Sharing is direct, but every shared value that changes needs a lock |
| Mixed needs | Several processes, each with several threads | Isolation between units, sharing within them |

## Common Misconceptions

- **"Threads are always faster than processes."** Threads are cheaper to create and can share data directly, but in CPython they do not speed up computation (Experiment 4), and waiting for another thread costs about as much as waiting for another process (Experiment 3).
- **"Processes cannot share data."** They can, through pipes, sockets, files, and shared-memory regions the kernel sets up; it just has to be arranged explicitly, and it is slower than a plain memory read.
- **"If a Python thread raises an exception, the program dies."** Only that thread ends. What ends *everything* is a fatal fault or an exit of the whole process.
- **"A process is always safer than a thread."** Isolation contains accidents and many attacks, but processes can still share files, ports, and databases, and communicating between them brings its own failure modes.
- **"Use as many workers as possible."** Past the number of cores, extra CPU-bound workers only add scheduling and switching overhead (see [context-switching.md](context-switching.md)).

## ➡️ Next

Continue to [process-states.md](process-states.md): once there are many processes and threads competing for few cores, each one is at any moment running, ready to run, or waiting, and the kernel moves them between those states.
