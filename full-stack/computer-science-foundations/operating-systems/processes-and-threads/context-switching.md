# 🔀 Context Switching

## Taking Turns on One CPU

A CPU core can run only one stream of instructions at a time, yet a computer appears to run hundreds at once. The trick is to take turns so quickly that every program seems to have the machine to itself. Each change of turn is a **context switch**: the kernel stores the state of the task that was running (a process or a thread) so that it can be resumed later exactly where it stopped, and restores the previously stored state of another task ([Wikipedia: Context switch](https://en.wikipedia.org/wiki/Context_switch)). The task never notices; as far as it can tell, it simply ran without interruption.

The "context" is whatever must survive the break: the CPU registers, the program counter (which instruction comes next), the stack pointer, and the memory-management information that says which address space the task lives in. The kernel keeps it in the task's process control block ([what-is-a-process.md](what-is-a-process.md)), which is why the PCB plays a central role in context switching. All code in this file was run on CPython 3.9 on a Mac (macOS, Apple silicon, 11 logical CPUs); counts and timings depend on the machine and are labelled, and everything else is the same on Linux.

## 🔬 Anatomy of a Switch

```
 Task A running in user mode
      │   a timer interrupt, a system call that must wait, an exit ...
      ▼
 kernel: save A's registers and program counter into A's control block
 kernel: update A's state (running → ready, or running → waiting)
 scheduler: choose the next task from the ready queue (say, B)
 kernel: if B belongs to a different process, switch to B's memory map (page tables)
 kernel: load B's registers and program counter from B's control block
      │   return to user mode
      ▼
 Task B continues from where it was last stopped
```

The scheduler's choice (step three) is the subject of the [CPU Scheduling module](../cpu-scheduling/README.md); this file is about the machinery around it.

## 🔔 What Triggers a Switch

Wikipedia identifies three situations in which a context switch can happen ([Wikipedia: Context switch](https://en.wikipedia.org/wiki/Context_switch)):

| Trigger | What happens | In the state model |
|---------|--------------|--------------------|
| **The task cannot continue**, so it gives up the CPU: it waits for I/O, sleeps, waits for a lock, or finishes | The kernel switches to another ready task. This is a **voluntary** switch | Running → Waiting, or Running → Terminated |
| **Preemption.** On a preemptive system, the scheduler arranges a timer interrupt to fire when a task has used up its time slice, or a more important task becomes ready | The kernel takes the CPU away from a task that was still runnable. This is an **involuntary** switch | Running → Ready |
| **Interrupt handling.** A device signals that it has finished, for example when a disk read completes | The hardware saves a *part* of the context, and the interrupt handler runs in that partial context without scheduling a special process; the interrupted task usually resumes afterwards. The interrupt may also make a waiting task ready, which can lead to a preemption | Waiting → Ready (for the task that was waiting) |

Preemption is exactly the act of interrupting a task temporarily, without its cooperation, with the intention of resuming it later ([Wikipedia: Preemption (computing)](https://en.wikipedia.org/wiki/Preemption_(computing))). It is what keeps one endless loop from freezing a machine. A related point from the same article on context switching: when the CPU changes between user mode and kernel mode, as in an ordinary system call, that **mode switch** is not by itself a context switch, although a context switch may follow.

## 🧪 Counting Switches From Python

The kernel keeps count. `resource.getrusage` reports the number of **voluntary** context switches (the process gave up the CPU before its time slice ended, usually to wait for something) and **involuntary** ones (a higher-priority process became runnable, or the process used up its slice), as defined in the Linux manual page for `getrusage(2)` ([Linux man page: `getrusage(2)`](https://man7.org/linux/man-pages/man2/getrusage.2.html)). The following block runs four workloads and prints both counters for each: a hundred short sleeps, a hundred thousand system calls that never block, a second of computing with no rivals, and a second of computing while twice as many busy processes as there are logical CPUs compete for the cores:

```python
import os
import resource
import subprocess
import sys
import threading
import time
from collections import deque

def switches(work):
    """Run work() and return this process's (voluntary, involuntary) context switches while it ran."""
    before = resource.getrusage(resource.RUSAGE_SELF)
    work()
    after = resource.getrusage(resource.RUSAGE_SELF)
    return after.ru_nvcsw - before.ru_nvcsw, after.ru_nivcsw - before.ru_nivcsw

def sleep_100_times():
    for _ in range(100):
        time.sleep(0.002)                           # blocks in the kernel: the process gives up the CPU

def make_100000_system_calls():
    for _ in range(100_000):
        os.getppid()                                # enters the kernel and returns at once: it never waits

def compute_one_second():
    start = time.perf_counter()
    while time.perf_counter() - start < 1.0:        # never blocks: only the kernel can take the CPU away
        pass

for label, work in (("100 sleeps", sleep_100_times),
                    ("100,000 system calls that do not block", make_100000_system_calls),
                    ("1 s of computing, no rivals", compute_one_second)):
    voluntary, involuntary = switches(work)
    print(f"{label:<42} {voluntary:5d} voluntary {involuntary:5d} involuntary")

rivals = [subprocess.Popen([sys.executable, "-c", "while True: pass"]) for _ in range(2 * os.cpu_count())]
try:
    time.sleep(0.5)                                 # let the rivals start competing
    voluntary, involuntary = switches(compute_one_second)
    print(f"{f'1 s of computing, {len(rivals)} busy rivals':<42} {voluntary:5d} voluntary {involuntary:5d} involuntary")
finally:
    for rival in rivals:
        rival.kill()
        rival.wait()
```

One run on the test machine printed:

```
100 sleeps                                   100 voluntary     0 involuntary
100,000 system calls that do not block         0 voluntary     1 involuntary
1 s of computing, no rivals                    0 voluntary     0 involuntary
1 s of computing, 22 busy rivals               0 voluntary   511 involuntary
```

The counts match the theory. Each of the 100 sleeps is a blocking call, so the process gave up the CPU 100 times: 100 voluntary switches, one per sleep. The 100,000 system calls produce no voluntary switches at all, because a call that returns immediately is only a mode switch; nobody had to wait. The computing loop never blocks either, so it has no voluntary switches. Its involuntary count depends on what else wants the core: when nothing else does, it can be zero or close to it, while in other runs on this Mac, busy with its usual background software, the same loop was taken off the CPU anywhere from dozens to a few hundred times in a second. Rivals change the picture decisively. With twice as many busy processes as logical CPUs, the kernel has to share the cores among all of them, and the count rose to several hundred in every run made while preparing this lesson. The exact figures change from run to run with whatever else the machine is doing; the pattern does not.

## 💰 What Does a Switch Cost?

A switch has **direct** and **indirect** costs. The direct cost is the work of the switch itself: saving and loading registers and memory maps, updating tables, and running the scheduler. The indirect cost comes afterwards. A task that has just been switched in finds the processor's caches filled with the previous task's data, and when the memory map changes, the cache of address translations (the TLB) may be flushed, so every memory reference starts slowly until the caches and the TLB warm up again. Wikipedia describes the translation-cache part of this cost, explains that every memory reference misses until the TLB refills, and notes that what a switch involves depends on the architecture, the operating system, and how many resources the two tasks share: threads of one process share far more than unrelated processes do ([Wikipedia: Context switch](https://en.wikipedia.org/wiki/Context_switch)).

The next block measures round trips in which two tasks hand control back and forth through a pair of pipes, each handing a single byte to the other. Each round trip contains two context switches and four system calls (a write and a read on each side), so a single switch costs well under half of the figure printed. The same ping-pong is run between two threads of one process and between two processes, to see whether sharing the address space matters. For comparison, the last measurement resumes a Python generator, which is a switch between tasks that happens entirely in user space, with no kernel involved:

```python
def pipe_ping_pong_threads_us(rounds=20_000):
    to_worker_r, to_worker_w = os.pipe()
    to_main_r, to_main_w = os.pipe()
    def echo():
        for _ in range(rounds):
            os.write(to_main_w, os.read(to_worker_r, 1))
    worker = threading.Thread(target=echo)
    worker.start()
    start = time.perf_counter()
    for _ in range(rounds):
        os.write(to_worker_w, b"x")
        os.read(to_main_r, 1)
    elapsed = time.perf_counter() - start
    worker.join()
    for descriptor in (to_worker_r, to_worker_w, to_main_r, to_main_w):
        os.close(descriptor)
    return elapsed / rounds * 1e6

def pipe_ping_pong_processes_us(rounds=20_000):
    to_child_r, to_child_w = os.pipe()
    to_parent_r, to_parent_w = os.pipe()
    pid = os.fork()
    if pid == 0:                                    # the child: echo every byte back
        try:
            for _ in range(rounds):
                os.write(to_parent_w, os.read(to_child_r, 1))
        finally:
            os._exit(0)
    start = time.perf_counter()
    for _ in range(rounds):
        os.write(to_child_w, b"x")
        os.read(to_parent_r, 1)
    elapsed = time.perf_counter() - start
    os.waitpid(pid, 0)
    for descriptor in (to_child_r, to_child_w, to_parent_r, to_parent_w):
        os.close(descriptor)
    return elapsed / rounds * 1e6

def forever():
    while True:
        yield                                       # hand control back to whoever resumed this generator

def generator_resume_us(resumes=1_000_000):
    task = forever()
    next(task)                                      # run it up to its first yield
    start = time.perf_counter()
    for _ in range(resumes):
        next(task)                                  # switch into the task and straight back out
    return (time.perf_counter() - start) / resumes * 1e6

def best_of(measure, repeats=3):
    return min(measure() for _ in range(repeats))

print(f"{'a generator resumed with next() (user level)':<48} {best_of(generator_resume_us):7.3f} us")
print(f"{'a pipe round trip between two threads':<48} {best_of(pipe_ping_pong_threads_us):7.3f} us")
print(f"{'a pipe round trip between two processes':<48} {best_of(pipe_ping_pong_processes_us):7.3f} us")
```

One run on the test machine printed:

```
a generator resumed with next() (user level)       0.042 us
a pipe round trip between two threads              6.551 us
a pipe round trip between two processes            5.872 us
```

Two results stand out. First, a switch made by the kernel costs microseconds, while resuming a generator, a user-level switch that saves nothing but the generator's own frame, costs a few hundredths of a microsecond: more than an order of magnitude less, even after allowing for the system calls inside each round trip. That gap is why runtimes with their own lightweight tasks (generators and `async` code in Python, green threads, goroutines in Go) can switch between enormous numbers of tasks cheaply, and why a design that avoids the kernel on its hot path scales better. Wikipedia notes that switching between user-level threads is often very lightweight, and that in the extreme case of Go's goroutines a switch costs little more than a function call ([Wikipedia: Context switch](https://en.wikipedia.org/wiki/Context_switch)). The price is that the kernel cannot see those tasks, so they cannot run on several cores at once unless the runtime also uses several kernel threads, and a blocking call can stall every task that shares a kernel thread.

Second, the two round trips between kernel-scheduled tasks are about the same, even though the textbook says a switch between processes should be dearer than one between threads. On this Mac the difference is not visible, and three things plausibly explain why. Newer CPUs mark each cached address translation with the process it belongs to, so a switch to another process need not flush the TLB, and a task that returns soon may find its entries still valid ([Wikipedia: Translation lookaside buffer](https://en.wikipedia.org/wiki/Translation_lookaside_buffer)). The two tasks in this test touch almost no memory, so there is no cache or TLB warm-up cost to expose. And the thread version also has to pass CPython's interpreter lock back and forth, which adds work of its own. The theoretical advantage of switching between threads is therefore real but is not a number you can count on; the dependable differences between threads and processes are the ones in [process-vs-thread.md](process-vs-thread.md): shared memory, creation cost, and failure scope.

## 🧪 A Context Switch You Can Read: Cooperative Scheduling

A generator is a convenient way to see what a context switch *is*. When a generator yields, Python keeps its local variables and its place in the code; when it is resumed, it continues from that place. That saved frame is the generator's context, and `next()` is the switch. A small scheduler that resumes tasks in turn, putting each at the back of the line when it yields, is a cooperative version of the round-robin policy used by real kernels. The three tasks below each print a line and then give up the CPU voluntarily:

```python
def worker(name, steps):
    for step in range(1, steps + 1):
        print(f"  {name}: step {step} of {steps}")
        yield                                       # give up the CPU: this generator's frame is its saved context

def run(tasks):
    ready = deque(tasks)
    dispatches = 0
    while ready:
        task = ready.popleft()                      # the scheduler picks the task at the front of the line
        dispatches += 1
        try:
            next(task)                              # switch to it; it runs until its next yield
            ready.append(task)                      # it yielded: back of the line
        except StopIteration:
            pass                                    # it finished: it never comes back
    return dispatches

print("order of execution:")
count = run([worker("A", 3), worker("B", 2), worker("C", 3)])
print("dispatches (switches into a task):", count)
print("kernel threads involved:", threading.active_count())
```

```text
order of execution:
  A: step 1 of 3
  B: step 1 of 2
  C: step 1 of 3
  A: step 2 of 3
  B: step 2 of 2
  C: step 2 of 3
  A: step 3 of 3
  C: step 3 of 3
dispatches (switches into a task): 11
kernel threads involved: 1
```

The tasks interleave one step at a time (A, B, C, A, B, C, A, C), B drops out of the rotation when it finishes after two steps, and the eleven dispatches (one more per task than it has steps, to discover that it is finished) all happened inside a single kernel thread, which the last line confirms. The weakness of cooperative scheduling is also visible in the code: a task that never yields would keep the CPU forever, because nothing can take it away. That is the problem the timer interrupt solves in a real kernel, and the reason operating systems use preemption.

## ⚖️ How Long Should a Time Slice Be?

Every preemption costs a switch, so the length of the time slice (the *quantum*) is a trade-off. Short slices make every task get the CPU often, which keeps response times low, but the fixed price of each switch eats a larger share of the time. Long slices waste little on switching, but a task that just became ready may wait a long time for its turn. With a cost per switch of *c* and a slice of *q*, the fraction of time spent on useful work is *q / (q + c)*, and with *n* tasks in the round-robin queue, one that has just become ready may wait up to *(n − 1) × (q + c)* before it runs. The table uses an illustrative switch cost of 0.05 ms, not a measurement, and ten competing tasks:

```python
switch_cost_ms = 0.05                               # an illustrative figure, not a measurement
tasks_in_queue = 10
print(f"{'time slice':>10} | {'time doing useful work':>22} | {'worst wait for a turn':>21}")
for quantum_ms in (0.1, 0.5, 1, 5, 20, 100):
    useful = quantum_ms / (quantum_ms + switch_cost_ms)
    worst_wait = (tasks_in_queue - 1) * (quantum_ms + switch_cost_ms)
    print(f"{quantum_ms:>7} ms | {useful:>22.1%} | {worst_wait:>18.1f} ms")
```

```text
time slice | time doing useful work | worst wait for a turn
    0.1 ms |                  66.7% |                1.4 ms
    0.5 ms |                  90.9% |                5.0 ms
      1 ms |                  95.2% |                9.5 ms
      5 ms |                  99.0% |               45.4 ms
     20 ms |                  99.8% |              180.5 ms
    100 ms |                 100.0% |              900.4 ms
```

No slice length is best for every workload: a desktop that must feel responsive prefers short slices, while a batch machine crunching numbers prefers long ones. The simulation in [types-of-operating-systems.md](../introduction-to-operating-systems/types-of-operating-systems.md) showed the same trade-off with total completion time, and the [CPU Scheduling module](../cpu-scheduling/README.md) of this section builds on it.

## 🧰 Keeping the Cost Under Control

- **Do not run more CPU-bound workers than there are cores.** Extra workers only add preemptions and switches (the rivals in the counting experiment).
- **Avoid designs where tasks constantly hand work back and forth.** Each hand-off is at least two switches. Let workers process batches, and give each worker enough to do before it waits for another.
- **Use lightweight tasks for waiting-heavy work.** Thousands of connections that are mostly idle are better served by an event loop or a small pool of threads than by one kernel thread each.
- **Remember that a blocked task costs nothing while it waits.** It is the *wake-up* that costs, so the number of hand-offs matters more than the number of tasks.

## Common Misconceptions

- **"Every system call is a context switch."** A system call is a mode switch. The experiment above made 100,000 of them without a single voluntary context switch; a switch happens only if the call has to wait, or the timer happens to expire.
- **"A context switch is a tiny cost, so nobody needs to care."** One switch is small, but a program or a server that causes millions of them a second spends a noticeable share of its time on switching and on re-warming caches.
- **"Threads switch for free."** They avoid some of the cost of changing the address space, but they are still scheduled by the kernel, still save and restore registers, and in the measurement above they cost about as much as processes. Only user-level tasks switch cheaply.
- **"The CPU only switches when a program asks it to."** On a preemptive system, the timer interrupt takes the CPU back without asking, which is exactly what the involuntary counts show.
- **"Context switches are a flaw to be eliminated."** They are what makes multitasking possible. The goal is to make them rare enough, and the work between them long enough, that the overhead is negligible.

## ➡️ Next

This completes the tour of processes and threads: what they are, how they differ, which states they pass through, and what it costs to change from one to another. The next module of this section, [CPU Scheduling](../cpu-scheduling/README.md), studies how the kernel chooses *which* ready task receives the CPU at each switch, and why different policies suit different goals.
