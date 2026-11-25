# 🧩 Understanding Concurrency

## Many Things in Progress at Once

A web server handles thousands of clients, a phone app keeps its screen responsive while it downloads, a database answers many queries over the same tables, and the operating system itself runs hundreds of activities on a handful of cores. All of these are **concurrent**: several computations are in progress during overlapping periods of time, instead of strictly one after another ([Wikipedia: Concurrent computing](https://en.wikipedia.org/wiki/Concurrent_computing)). The word is often confused with **parallelism**, which means executing at the same instant on several processing units. The two are independent: a program may exhibit parallelism only, concurrency only, both, or neither (the same article), and several tasks taking turns on a single core are concurrent without being parallel. Everything in this module applies to concurrency in general, because the problems arise whenever activities overlap in time and touch the same things, whether or not they ever literally run at the same instant.

The previous modules supplied the machinery: processes and threads ([what-is-a-thread.md](../processes-and-threads/what-is-a-thread.md)), a scheduler that switches among them at moments the program does not control ([round-robin.md](../cpu-scheduling/round-robin.md)), and memory that threads of one process *share* ([paging.md](../memory-management/paging.md)). This module is about the price of that sharing. This file builds the intuition: why concurrent programs are hard to get right, what an "atomic" step is, and the main ways programs cope. The next files study the first problem, [race conditions](race-conditions.md); its cure, [mutexes and semaphores](mutex-and-semaphores.md); the new problem the cure creates, [deadlock](deadlocks.md); and how to [prevent it](deadlock-prevention.md). All code was run on CPython 3.9 on a Mac (macOS, Apple silicon); where output depends on timing, the text says so.

## 🔀 Interleavings: The Scheduler Chooses the Order

When two threads run, each executes its own steps in order, but the *combination* is up to the scheduler: it may run thread A's next step, or B's, at any moment, and the choice can differ from run to run. Every way of merging the two sequences, while keeping the order inside each, is a possible **interleaving**. For two threads with two steps each, there are six:

```python
from math import comb

def interleavings(first, second):
    """Every way of merging two sequences of steps while keeping the order inside each sequence."""
    if not first:
        yield list(second)
    elif not second:
        yield list(first)
    else:
        for rest in interleavings(first[1:], second):
            yield [first[0]] + rest
        for rest in interleavings(first, second[1:]):
            yield [second[0]] + rest

orders = list(interleavings(["a1", "a2"], ["b1", "b2"]))
for order in orders:
    print(" ".join(order))
assert len(orders) == comb(4, 2)
```

```text
a1 a2 b1 b2
a1 b1 a2 b2
a1 b1 b2 a2
b1 a1 a2 b2
b1 a1 b2 a2
b1 b2 a1 a2
```

Each line is a schedule that the operating system might produce. A correct program must behave correctly in *all* of them, and not merely in the one that happened during testing. The number of schedules grows explosively: two threads with *n* steps each have C(2*n*, *n*) possible interleavings.

```python
print(f"{'steps in each thread':>20} | {'possible interleavings':>26}")
for steps in (2, 3, 5, 10, 20, 50):
    print(f"{steps:>20} | {comb(2 * steps, steps):>26,}")
```

```text
steps in each thread |     possible interleavings
                   2 |                          6
                   3 |                         20
                   5 |                        252
                  10 |                    184,756
                  20 |            137,846,528,820
                  50 | 100,891,344,545,564,193,334,812,497,256
```

Two threads with just 20 steps each already have more than 100 billion interleavings. Real programs have thousands of steps, more than two threads, and a scheduler that depends on timing, load, and the hardware, so testing can sample only a tiny fraction of the schedules. That is why concurrency bugs are rare, hard to reproduce, and often disappear when you add a print statement, and why this module leans on *reasoning* and on tools that explore the schedules systematically (the next files build one).

## ⚛️ Atomicity: One Line of Code Is Not One Step

A step is **atomic** if no other thread can ever observe it half-done: it either has not happened or has completely happened. Hardware makes some single machine operations atomic, but a line of source code is usually many operations. In Python, `counter += 1` looks like one step, but the bytecode shows otherwise:

```python
import dis

counter = 0

def bump():
    global counter
    counter += 1

dis.dis(bump)
```

One run on the test machine printed:

```
  7           0 LOAD_GLOBAL              0 (counter)
              2 LOAD_CONST               1 (1)
              4 INPLACE_ADD
              6 STORE_GLOBAL             0 (counter)
              8 LOAD_CONST               0 (None)
             10 RETURN_VALUE
```

The statement is four separate instructions: fetch the current value of `counter` (`LOAD_GLOBAL`), load the constant 1, add (`INPLACE_ADD`), and store the result back (`STORE_GLOBAL`). The interpreter's lock ([what-is-a-thread.md](../processes-and-threads/what-is-a-thread.md)) keeps each of these simple instructions whole, but it can pass from one thread to another *between* instructions. If another thread changes `counter` after this thread has loaded it, this thread will store a result computed from a stale value, and the other thread's update is lost. Every read-modify-write sequence (increment a counter, append to a list and update its length, check a condition and then act on it) has the same shape: the middle of it is not protected unless the program does something about it. The exact bytecode differs between Python versions, but the structure does not.

## 🤝 Three Ways to Share Work

Programs avoid the dangers of overlapping access in three broad ways:

| Approach | Idea | Python tools | Price |
|----------|------|--------------|-------|
| **Shared memory with locks** | Threads read and write the same data, and take turns inside critical sections | `threading.Lock`, `Semaphore`, `Condition` | Easy to get wrong; locks can cause deadlock |
| **Message passing** | Threads share nothing; they send each other messages through a channel that handles the synchronization | `queue.Queue`, `multiprocessing` pipes and queues | Copying messages; needs a protocol |
| **No shared mutable data** | Data is immutable, or each thread owns its own copy and results are combined at the end | Tuples, `frozenset`, per-thread data, `ProcessPoolExecutor` | Not every problem fits |

The Python documentation describes the queue module as implementing multi-producer, multi-consumer queues that are useful when information must be exchanged safely between threads, with all the required locking built in ([Python docs: `queue`](https://docs.python.org/3/library/queue.html)). The next block uses that: three producer threads put the numbers 1 to 100 on a queue, and two consumer threads take them off and add them up, with no lock in the program itself:

```python
import queue
import threading

work = queue.Queue()
results = queue.Queue()

def producer(first, last):
    for number in range(first, last + 1):
        work.put(number)

def consumer():
    total = 0
    while True:
        number = work.get()
        if number is None:                          # a marker meaning "no more work"
            break
        total += number
    results.put(total)

producers = [threading.Thread(target=producer, args=(1, 100)) for _ in range(3)]
consumers = [threading.Thread(target=consumer) for _ in range(2)]
for thread in producers + consumers:
    thread.start()
for thread in producers:
    thread.join()
for _ in consumers:
    work.put(None)                                  # one marker for each consumer
for thread in consumers:
    thread.join()
print("sum of everything produced:", 3 * sum(range(1, 101)), "| sum of everything consumed:", results.get() + results.get())
```

```text
sum of everything produced: 15150 | sum of everything consumed: 15150
```

However the scheduler interleaved the five threads, nothing was lost or counted twice, because the only shared object was the queue, and the queue guards itself. Message passing does not remove the need to think (the consumers still had to be told when to stop), but it moves the hard part into one well-tested component.

## ⚠️ What Can Go Wrong

Four classic failures belong to this subject; the rest of the module takes them in turn:

| Problem | What happens | Studied in |
|---------|--------------|------------|
| **Race condition** | The result depends on the timing of the threads, and some timings give wrong answers ([Wikipedia: Race condition](https://en.wikipedia.org/wiki/Race_condition)) | [race-conditions.md](race-conditions.md) |
| **Deadlock** | Each member of a group waits for another member of the group, so none can proceed ([Wikipedia: Deadlock](https://en.wikipedia.org/wiki/Deadlock_(computer_science))) | [deadlocks.md](deadlocks.md), [deadlock-prevention.md](deadlock-prevention.md) |
| **Livelock** | Like deadlock, but the states of the processes keep changing without any of them making progress (the same article) | [deadlocks.md](deadlocks.md) |
| **Starvation** | A process is perpetually denied the resources it needs, for example by a scheduling or mutual exclusion algorithm that keeps favouring others ([Wikipedia: Resource starvation](https://en.wikipedia.org/wiki/Resource_starvation)) | [priority-scheduling.md](../cpu-scheduling/priority-scheduling.md), [deadlocks.md](deadlocks.md) |

## 🧠 A Mindset for Concurrent Code

- **Assume the worst interleaving.** Any step may be followed by any other thread's step. Ask what is true *between* two lines.
- **Name the shared mutable state.** Bugs live only where two threads can touch the same data and at least one changes it. The less of it there is, the less there is to get wrong.
- **State the invariant.** "The balance equals deposits minus withdrawals" or "the buffer holds at most N items" are the facts that critical sections must preserve.
- **Prefer higher-level tools.** Queues, thread pools, and immutable data are easier to reason about than hand-made locking.
- **Do not trust testing alone.** A concurrent program that passes a thousand runs may still contain a schedule that fails.

## Common Misconceptions

- **"Concurrency means things happen at the same time."** Concurrency means overlapping *periods*; parallelism is the simultaneous kind. A single core can run a concurrent program by interleaving.
- **"The GIL makes Python threads safe."** The lock keeps each bytecode instruction intact, not sequences of them. A read-modify-write such as `counter += 1` can still lose updates, as the next file shows by experiment.
- **"If it passed the tests, it is correct."** Concurrency bugs depend on timing and may show up once in a million runs.
- **"A race condition is the same as a bug in the logic."** The logic can be perfectly right for any single thread and still fail when two of them overlap.
- **"More threads always mean a faster program."** Extra threads also add contention, switching cost, and new ways to be wrong.

## ➡️ Next

Continue to [race-conditions.md](race-conditions.md): the first and most common concurrency bug, demonstrated deterministically (by enumerating every schedule), with real threads that are forced to collide, and in an unforced experiment where the answer changes from run to run.
