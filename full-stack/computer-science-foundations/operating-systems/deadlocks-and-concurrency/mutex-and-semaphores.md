# 🔐 Mutexes and Semaphores

## Taking Turns Inside a Critical Section

[race-conditions.md](race-conditions.md) showed what happens when threads overlap inside a read-modify-write sequence. The cure is to let only one thread at a time execute such a sequence. The stretch of code that needs this protection is a **critical section**, and the requirement that no two threads be inside it together is **mutual exclusion**. The requirement was first identified and solved by Edsger Dijkstra in a 1965 paper, usually credited as the beginning of the study of concurrent algorithms ([Wikipedia: Mutual exclusion](https://en.wikipedia.org/wiki/Mutual_exclusion)). A good solution to the critical-section problem meets three criteria: **mutual exclusion** (never two threads inside at once), **progress** (a thread outside the critical section cannot stop others from entering), and **bounded waiting** (a thread that wants in gets in after a limited wait, so it cannot starve) ([Wikipedia: Peterson's algorithm](https://en.wikipedia.org/wiki/Peterson%27s_algorithm)).

The standard tool is the **lock**, also called a **mutex** (short for mutual exclusion): a synchronization primitive that prevents state from being modified or accessed by several threads of execution at once ([Wikipedia: Lock (computer science)](https://en.wikipedia.org/wiki/Lock_(computer_science))). A second tool, the **semaphore**, generalizes the idea from "one at a time" to "at most *n* at a time" and doubles as a signalling device. This file builds both, measures what they cost, and checks that they do their job. It uses the schedule explorer from [race-conditions.md](race-conditions.md), repeated here so that the file runs on its own. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon).

```python
from collections import Counter

# A program for each thread is a list of atomic steps. A step is one of:
#   ("read", variable, register)     copy a shared variable into one of the thread's private registers
#   ("local", register, function)    set a private register to function(registers); no other thread can see or affect it
#   ("write", variable, function)    store function(registers) into a shared variable
#   ("acquire", lock)                take a lock, or wait if another thread holds it
#   ("release", lock)                give a lock back
# Registers are private to a thread; shared variables and locks are visible to all.

def explore(programs, shared):
    """Try every possible interleaving of the threads' steps and report how they end.
    Returns (outcomes, deadlocks, states): how many schedules end in each final value of the shared variables,
    how many schedules end stuck in a deadlock, and how many distinct situations were reached on the way."""
    names = list(programs)
    freeze = lambda mapping: tuple(sorted(mapping.items()))
    start = (freeze(shared), (0,) * len(names), (freeze({}),) * len(names), freeze({}))
    paths = Counter({start: 1})                     # how many different schedules lead to each situation
    layer, outcomes, deadlocks, states = {start}, Counter(), Counter(), 1
    while layer:                                    # every step moves one thread forward, so situations form layers
        following = set()
        for situation in layer:
            memory, counters, registers, locks = situation
            moves = []
            for i, name in enumerate(names):
                if counters[i] == len(programs[name]):
                    continue                        # this thread has finished
                step = programs[name][counters[i]]
                new_memory, new_registers, new_locks = dict(memory), dict(registers[i]), dict(locks)
                if step[0] == "read":
                    new_registers[step[2]] = new_memory[step[1]]
                elif step[0] == "local":
                    new_registers[step[1]] = step[2](new_registers)
                elif step[0] == "write":
                    new_memory[step[1]] = step[2](new_registers)
                elif step[0] == "acquire":
                    if step[1] in new_locks:
                        continue                    # the lock is taken: this thread is blocked and cannot move now
                    new_locks[step[1]] = name
                elif step[0] == "release":
                    del new_locks[step[1]]
                moves.append((freeze(new_memory), counters[:i] + (counters[i] + 1,) + counters[i + 1:],
                              registers[:i] + (freeze(new_registers),) + registers[i + 1:], freeze(new_locks)))
            if not moves:                           # nobody can move: either everyone finished, or the threads are deadlocked
                finished = all(counters[i] == len(programs[name]) for i, name in enumerate(names))
                (outcomes if finished else deadlocks)[memory if finished else (counters, locks)] += paths[situation]
            for move in moves:
                paths[move] += paths[situation]
                following.add(move)
        states += len(following)
        layer = following
    return outcomes, deadlocks, states
```

## 🔒 The Mutex

A thread **acquires** the lock before entering the critical section and **releases** it on the way out; a thread that finds the lock taken waits until it is free. In Python the lock is `threading.Lock`, and the `with` statement guarantees the release even if the critical section raises an exception. The explorer can first show the effect on the two incrementing threads of the previous file, with the lock around the *whole* read-modify-write. Then it shows a lock in the wrong place, where the read happens outside it:

```python
increment = [("read", "counter", "r"), ("local", "r", lambda registers: registers["r"] + 1), ("write", "counter", lambda registers: registers["r"])]

def show(outcomes, deadlocks):
    total = sum(outcomes.values()) + sum(deadlocks.values())
    for memory, count in sorted(outcomes.items()):
        print(f"  final {dict(memory)}: {count} of {total} schedules")
    for situation, count in deadlocks.items():
        print(f"  DEADLOCK {situation}: {count} of {total} schedules")

whole = [("acquire", "L")] + increment + [("release", "L")]
print("the lock covers the read, the addition and the write:")
outcomes, deadlocks, states = explore({"A": whole, "B": whole}, {"counter": 0})
show(outcomes, deadlocks)

misplaced = increment[:1] + [("acquire", "L")] + increment[1:] + [("release", "L")]
print("the read is outside the lock:")
outcomes, deadlocks, states = explore({"A": misplaced, "B": misplaced}, {"counter": 0})
show(outcomes, deadlocks)
```

```text
the lock covers the read, the addition and the write:
  final {'counter': 2}: 2 of 2 schedules
the read is outside the lock:
  final {'counter': 1}: 8 of 12 schedules
  final {'counter': 2}: 4 of 12 schedules
```

With the lock around everything, the bad interleavings are gone: only two schedules exist at all (A's whole section and then B's, or the reverse), and both end with 2. The lock *removed* schedules, which is precisely its job. With the read outside, a thread can still read a stale value before the other thread's write, and 8 of the 12 schedules lose an update: **the critical section must contain the entire sequence whose parts must not be separated**, not merely the final write. Real threads behave the same way. This block runs the unprotected experiment of the previous file again, but with the lock, four times:

```python
import threading
import time

counter = 0
lock = threading.Lock()

def bump_locked(times):
    global counter
    for _ in range(times):
        with lock:                                  # only one thread at a time may be inside this block
            counter += 1

def locked_run(threads=4, times=250_000):
    global counter
    counter = 0
    workers = [threading.Thread(target=bump_locked, args=(times,)) for _ in range(threads)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
    return counter

print("four threads, 250,000 increments each, with a lock:", [locked_run() for _ in range(4)])
```

```text
four threads, 250,000 increments each, with a lock: [1000000, 1000000, 1000000, 1000000]
```

Every run gives exactly 1,000,000, where the unprotected runs gave anything from half that upwards. The same rule covers the **check-then-act** race: the lock has to include the check as well as the action. The next block runs the bank-account example of the previous file, with two withdrawals of 80 from a balance of 100, 500 times with the check and the subtraction inside one critical section, and then once more with a *misplaced* lock that protects only the subtraction while the barrier forces both checks to happen first:

```python
def withdraw_trial():
    account = {"balance": 100}
    guard = threading.Lock()
    results = []

    def withdraw(amount):
        with guard:                                 # the check and the action form one critical section
            if account["balance"] >= amount:
                account["balance"] -= amount
                results.append("paid")
            else:
                results.append("refused")

    threads = [threading.Thread(target=withdraw, args=(80,)) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return account["balance"], sorted(results)

print("500 trials with the whole check-and-withdraw protected:", {str(withdraw_trial()) for _ in range(500)})

def misplaced_overdraft():
    account = {"balance": 100}
    guard = threading.Lock()
    both_have_checked = threading.Barrier(2)

    def withdraw(amount):
        if account["balance"] >= amount:            # the check is outside the lock ...
            both_have_checked.wait()
            with guard:                             # ... only the subtraction is inside it
                account["balance"] -= amount

    threads = [threading.Thread(target=withdraw, args=(80,)) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return account["balance"]

print("the lock around the subtraction only:", misplaced_overdraft())
```

```text
500 trials with the whole check-and-withdraw protected: {"(20, ['paid', 'refused'])"}
the lock around the subtraction only: -60
```

All 500 correct trials give the same outcome (one withdrawal paid, one refused, 20 left), whichever thread happens to go first; the misplaced lock still overdraws the account to −60.

## 💰 What Does a Lock Cost?

Mutual exclusion is not free. The first measurement times one million increments in a single thread with and without the lock, so that there is no contention at all, and the second times the four-thread experiment above with and without the lock:

```python
def nanoseconds_per_increment(use_lock, times=1_000_000):
    global counter
    counter = 0
    start = time.perf_counter()
    if use_lock:
        for _ in range(times):
            with lock:
                counter += 1
    else:
        for _ in range(times):
            counter += 1
    return (time.perf_counter() - start) / times * 1e9

def bump_plain(times):
    global counter
    for _ in range(times):
        counter += 1

def four_thread_seconds(target):
    workers = [threading.Thread(target=target, args=(250_000,)) for _ in range(4)]
    start = time.perf_counter()
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
    return time.perf_counter() - start

print(f"one thread, per increment: {min(nanoseconds_per_increment(False) for _ in range(3)):.0f} ns without a lock, {min(nanoseconds_per_increment(True) for _ in range(3)):.0f} ns with a lock")
print(f"four threads, 1,000,000 increments: {min(four_thread_seconds(bump_plain) for _ in range(3)):.3f} s without a lock (and wrong answers), {min(four_thread_seconds(bump_locked) for _ in range(3)):.3f} s with a lock")
```

One run on the test machine printed:

```
one thread, per increment: 32 ns without a lock, 128 ns with a lock
four threads, 1,000,000 increments: 0.032 s without a lock (and wrong answers), 0.124 s with a lock
```

Even with no competition, taking and releasing the lock made each increment about four times slower; four threads sharing one lock take correspondingly longer, and they spend that time in queues rather than in computation. Locks are cheap compared with a mistake, but they are not free, so critical sections should be as short as correctness allows (never include slow operations such as network or disk waits, which would make every other thread wait for them too).

## ⏳ Spinning or Sleeping

How should a thread wait for a lock? A **spinlock** keeps trying in a loop, "spinning" until the lock becomes available. This is efficient if threads are blocked for only a short time, because it avoids the overhead of the operating system rescheduling the thread, but it is inefficient if the lock is held for a long time ([Wikipedia: Lock (computer science)](https://en.wikipedia.org/wiki/Lock_(computer_science))). A **blocking** lock puts the waiting thread to sleep, in the waiting state of [process-states.md](../processes-and-threads/process-states.md), and the kernel wakes it when the lock is released. Locks of both kinds depend on hardware support for **atomic** instructions such as **test-and-set**, which writes a flag to a memory location and returns the old value as one uninterruptible operation ([Wikipedia: Test-and-set](https://en.wikipedia.org/wiki/Test-and-set)), and **compare-and-swap**, which changes a memory location only if it still holds an expected value ([Wikipedia: Compare-and-swap](https://en.wikipedia.org/wiki/Compare-and-swap)). Python's `acquire(False)` is a non-blocking attempt, the equivalent of one test-and-set, so a spinlock can be written with it. The experiment below makes a second thread wait half a second for a lock, once by spinning and once by blocking, and measures the CPU time that thread consumes:

```python
def cpu_seconds_while_waiting(spin):
    held = threading.Lock()
    held.acquire()                                  # the lock is held by this (main) thread for half a second
    used = {}

    def waiter():
        before = time.thread_time()                 # the CPU time of this thread alone
        if spin:
            while not held.acquire(False):          # try again and again without sleeping
                pass
        else:
            held.acquire()                          # sleep inside the kernel until the lock is released
        used["cpu"] = time.thread_time() - before
        held.release()

    thread = threading.Thread(target=waiter)
    thread.start()
    time.sleep(0.5)
    held.release()
    thread.join()
    return used["cpu"]

print(f"CPU time used by a thread waiting 0.5 s: {cpu_seconds_while_waiting(True):.2f} s when spinning, {cpu_seconds_while_waiting(False):.2f} s when blocking")
```

One run on the test machine printed:

```
CPU time used by a thread waiting 0.5 s: 0.53 s when spinning, 0.00 s when blocking
```

The spinning thread burned a full half second of processor time to do nothing, as much as a computing thread would; the blocking thread used essentially none, because a waiting thread is simply not scheduled (the measurement of [kernel-and-user-mode.md](../introduction-to-operating-systems/kernel-and-user-mode.md) again). General-purpose locks therefore block, or spin only briefly before blocking, and spinlocks are used where the wait is known to be very short, such as inside an operating-system kernel.

## 🔁 Who Owns the Lock?

Python's plain `Lock` is, in the words of its documentation, not owned by a particular thread when locked, so even the thread that took it cannot take it again: it would wait for itself, a one-thread deadlock. A **reentrant lock**, `RLock`, remembers its owning thread and a recursion level, so the same thread may acquire it several times and must release it as many times ([Python docs: `threading`](https://docs.python.org/3/library/threading.html)). That matters when a function that holds a lock calls another function that takes the same lock. A timeout lets the experiment show the difference safely, instead of hanging:

```python
plain = threading.Lock()
plain.acquire()
print("the same thread takes a plain Lock a second time (waiting up to 0.2 s):", plain.acquire(timeout=0.2))

reentrant = threading.RLock()
reentrant.acquire()
print("the same thread takes an RLock a second time:", reentrant.acquire(timeout=0.2))
```

```text
the same thread takes a plain Lock a second time (waiting up to 0.2 s): False
the same thread takes an RLock a second time: True
```

## 🎟️ Semaphores

A **semaphore** is a synchronization device that controls access to a shared resource by several threads at once, allowing a predetermined number of them into a critical section. It can be pictured as a count of how many units of a resource are available, with operations to adjust the count safely and to wait until a unit becomes available. The concept was invented by Edsger Dijkstra in 1962 or 1963, while he and his team were developing the THE multiprogramming system. A semaphore that allows any count is a **counting semaphore**, and one restricted to 0 and 1 is a **binary semaphore**, usable as a lock ([Wikipedia: Semaphore (programming)](https://en.wikipedia.org/wiki/Semaphore_(programming))). Dijkstra's operations were named P (wait) and V (signal); Python calls them `acquire` and `release`: `acquire` decrements the counter, or blocks if it is zero, and `release` increments it, waking a waiter ([Python docs: `threading`](https://docs.python.org/3/library/threading.html)). Wikipedia adds a caution: semaphores help prevent race conditions but do not guarantee their absence ([Wikipedia: Semaphore (programming)](https://en.wikipedia.org/wiki/Semaphore_(programming))).

**Limiting concurrency.** Ten workers each need a scarce resource for 50 milliseconds, and only three may use it at once (a database connection pool, say). A semaphore with a count of 3 enforces that, and a counter protected by a lock records how many workers were inside at the same time:

```python
def semaphore_demo(permits=3, workers=10):
    gate = threading.Semaphore(permits)
    inside, peak, guard = [0], [0], threading.Lock()

    def worker():
        with gate:                                  # blocks when `permits` workers are already inside
            with guard:
                inside[0] += 1
                peak[0] = max(peak[0], inside[0])
            time.sleep(0.05)                        # use the scarce resource
            with guard:
                inside[0] -= 1

    threads = [threading.Thread(target=worker) for _ in range(workers)]
    start = time.perf_counter()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return peak[0], time.perf_counter() - start

peak, seconds = semaphore_demo()
print(f"most workers ever inside at once: {peak} (never more than 3: {peak <= 3})")
print(f"10 workers of 0.05 s with 3 permits took {seconds:.2f} s, about {-(-10 // 3)} rounds of 0.05 s")
```

One run on the test machine printed:

```
most workers ever inside at once: 3 (never more than 3: True)
10 workers of 0.05 s with 3 permits took 0.24 s, about 4 rounds of 0.05 s
```

**Signalling.** A semaphore that starts at 0 turns the roles around: a thread that calls `acquire` must wait until another thread calls `release`, so the release acts as a signal that something has happened. The thread that uses the data below is started *first*, yet it cannot proceed until the thread that prepares the data has said it is ready:

```python
events = []
data_ready = threading.Semaphore(0)

def prepare():
    events.append("A: preparing the data")
    time.sleep(0.05)
    events.append("A: data ready")
    data_ready.release()                            # signal: one unit of "ready" is now available

def use():
    data_ready.acquire()                            # wait for the signal
    events.append("B: using the data")

user, preparer = threading.Thread(target=use), threading.Thread(target=prepare)
user.start()
preparer.start()
preparer.join()
user.join()
print(events)
```

```text
['A: preparing the data', 'A: data ready', 'B: using the data']
```

This is the difference in spirit between the two tools. A **mutex** protects a critical section and belongs to the thread that took it, which is the one that should release it. A **semaphore** has no owner, so any thread may release it; that makes it a counter of resources and a means of signalling. `BoundedSemaphore` is a variant that raises an error if it is released more often than it was acquired, which usually reveals a bug ([Python docs: `threading`](https://docs.python.org/3/library/threading.html)).

## 🍽️ The Bounded Buffer

A classic problem puts the tools together: **producers** make items and put them in a buffer of fixed size, and **consumers** take them out. A producer must wait when the buffer is full, a consumer must wait when it is empty, and the buffer itself must not be corrupted by simultaneous access. This is the producer–consumer problem, also called the bounded-buffer problem, described by Dijkstra since 1965, and its first solution used two counting semaphores ([Wikipedia: Producer–consumer problem](https://en.wikipedia.org/wiki/Producer%E2%80%93consumer_problem)). One semaphore counts the free slots (producers wait on it), the other counts the filled slots (consumers wait on it), and a lock protects the list:

```python
class BoundedBuffer:
    def __init__(self, capacity):
        self.items = []
        self.free_slots = threading.Semaphore(capacity)     # how many more items may be added
        self.used_slots = threading.Semaphore(0)            # how many items are waiting to be taken
        self.lock = threading.Lock()                        # protects the list itself
        self.peak = 0

    def put(self, item):
        self.free_slots.acquire()                           # wait until there is room
        with self.lock:
            self.items.append(item)
            self.peak = max(self.peak, len(self.items))
        self.used_slots.release()                           # tell a consumer there is something to take

    def get(self):
        self.used_slots.acquire()                           # wait until there is something to take
        with self.lock:
            item = self.items.pop(0)
        self.free_slots.release()                           # tell a producer there is room
        return item

def buffer_trial(capacity=4, producers=3, per_producer=200, consumers=2):
    buffer = BoundedBuffer(capacity)
    taken, guard = [], threading.Lock()
    share = producers * per_producer // consumers

    def produce(number):
        for sequence in range(per_producer):
            buffer.put((number, sequence))

    def consume():
        mine = [buffer.get() for _ in range(share)]
        with guard:
            taken.extend(mine)

    threads = [threading.Thread(target=produce, args=(number,)) for number in range(producers)]
    threads += [threading.Thread(target=consume) for _ in range(consumers)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    expected = sorted((number, sequence) for number in range(producers) for sequence in range(per_producer))
    return sorted(taken) == expected, buffer.peak <= capacity, len(buffer.items) == 0

print("3 producers x 200 items, 2 consumers, a buffer of 4 slots; (every item exactly once, never over capacity, left empty):")
for trial in range(3):
    print("  trial", trial + 1, buffer_trial())
```

```text
3 producers x 200 items, 2 consumers, a buffer of 4 slots; (every item exactly once, never over capacity, left empty):
  trial 1 (True, True, True)
  trial 2 (True, True, True)
  trial 3 (True, True, True)
```

Six hundred items passed through a buffer that could hold only four, and every one arrived exactly once. Nobody checked the buffer's fullness by hand: the semaphores did the waiting. In everyday Python you would not write this yourself: `queue.Queue(maxsize=4)` is exactly this structure, with the locking built in ([Python docs: `queue`](https://docs.python.org/3/library/queue.html)). A **monitor**, a lock together with one or more *condition variables* on which threads can wait for a state change and be woken when it happens ([Wikipedia: Monitor (synchronization)](https://en.wikipedia.org/wiki/Monitor_(synchronization))), is the more general tool for the same problem; in Python it is `threading.Condition`.

## 🔃 Locks Meet Priorities

Locks interact with the priority scheduling of [priority-scheduling.md](../cpu-scheduling/priority-scheduling.md) in one notorious way. If a low-priority task holds a lock that a high-priority task needs, and a medium-priority task preempts the low-priority one, the high-priority task is held up indirectly by a task of lower priority than itself: the priorities are *inverted*. There is no foolproof way to predict the situation, but there are well-known remedies. With **priority inheritance**, a low-priority task that holds a resource needed by a waiting higher-priority task temporarily takes on the priority of the highest-priority waiter while it uses the resource, so medium-priority tasks cannot preempt it, and it drops back when it releases the lock. With the **priority ceiling protocol**, the lock itself carries a high priority that is given to whichever task holds it. Simple embedded systems often disable interrupts around critical sections, which leaves only two priorities, preemptible and not, so that inversion cannot occur, provided the critical sections stay very short ([Wikipedia: Priority inversion](https://en.wikipedia.org/wiki/Priority_inversion)). The problem is not an academic one: it was one of the troubles of the Mars Pathfinder lander in 1997. If you build a system with several priority levels and locks shared among them, ask what happens when a lock holder is preempted.

## 🧭 Choosing and Using the Tools

| Need | Tool | Note |
|------|------|------|
| Only one thread at a time may run a section of code | `Lock`, with `with` | Keep the section short and never block inside it |
| The same thread may need the lock again | `RLock` | Owned by a thread; released as many times as acquired |
| At most *n* threads may use a resource | `Semaphore(n)` | `BoundedSemaphore(n)` also catches extra releases |
| One thread must wait for another to finish or signal | `Semaphore(0)`, `Event`, `Condition` | The signal has no owner |
| Hand data from threads to threads | `queue.Queue` | Locking is built in |
| Wait for a *condition* about shared state | `Condition` (a lock plus waiting) | A monitor |

Habits that prevent most lock bugs: always use `with` (so a lock cannot be left held after an error); protect the *whole* invariant, as the misplaced-lock experiments showed; keep critical sections short; do not call unknown code or slow operations while holding a lock; and take several locks in one agreed order, which is the subject of [deadlocks.md](deadlocks.md). The first problem that locks cannot solve alone is already visible in the table: when threads hold one lock and wait for another, they can end up waiting for each other for ever.

## ✅ Checking the Code

The bounded buffer was run on 200 random configurations (capacities from 1 to 6, one to four producers and consumers, and different item counts) and in every case each item came out exactly once, the buffer never exceeded its capacity, and it ended empty. The semaphore demonstration was run on 25 random combinations of 1 to 5 permits and 3 to 15 workers: the number of workers inside at once never exceeded the permits, and always reached them when there were at least as many workers as permits. The locked counter gave the full total in every one of 200 runs of random thread counts.

## Common Misconceptions

- **"A lock makes my code thread-safe."** Only if it covers every access to the shared data and the whole sequence that must be indivisible. The lock around only the write, or only the subtraction, protected nothing.
- **"A semaphore and a mutex are the same."** A binary semaphore can act as a lock, but a semaphore has no owner and counts, which makes it a signalling and resource-counting tool; a mutex expresses ownership of a critical section.
- **"Spinning is faster, so spinlocks are better."** Spinning avoids a sleep and wake-up but burns CPU for the whole wait; it pays only when the wait is shorter than a trip through the scheduler.
- **"Locks fix races for free."** They cost time on every use (about four times slower per increment in the single-thread measurement), and they create the possibility of deadlock.
- **"If I never release the lock, nothing bad happens."** Every other thread that needs it will wait for ever; use `with` so that a release always happens.

## ➡️ Next

Continue to [deadlocks.md](deadlocks.md): what goes wrong when threads hold locks and wait for each other, the four conditions that make it possible, and an explorer that can find the fatal schedule.
