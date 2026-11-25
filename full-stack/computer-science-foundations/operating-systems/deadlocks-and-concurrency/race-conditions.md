# 🏁 Race Conditions

## When Timing Decides the Answer

A **race condition** is a situation in which the behaviour of a system depends on the sequence or timing of events that nobody controls, so that some of the possible behaviours are wrong ([Wikipedia: Race condition](https://en.wikipedia.org/wiki/Race_condition)). The name is older than software: it was already in use in 1954, for circuits in which signals racing along different paths could produce a glitch. In concurrent programs the race is between threads that touch the same data; the operations on shared state have to be done in **critical sections** that exclude one another, and failure to obey this rule can corrupt the shared state (the same article). A related term is the **data race**, in which one thread may access a memory location while another is writing to it in a dangerous way. Not everyone uses the two terms as synonyms: timing-dependent behaviour is possible even in a program whose every memory access is atomic and which therefore has no data race (the same article). This file concentrates on the common software case.

Race conditions have done real harm. Concurrent programming errors, which are race conditions, were among the flaws of the Therac-25 radiation therapy machine, which gave some patients doses up to 250 times higher than intended in the 1980s ([Wikipedia: Therac-25](https://en.wikipedia.org/wiki/Therac-25)). A race condition in the energy management software used by FirstEnergy stalled the control-room alarm system for over an hour in the events that led to the North American blackout of 2003, one link in a long chain of failures ([Wikipedia: Northeast blackout of 2003](https://en.wikipedia.org/wiki/Northeast_blackout_of_2003)). What makes such bugs so dangerous is that they are **nondeterministic**: the result depends on the relative timing of the threads, so the bug can vanish when the program is run in a debugger or with extra logging, the kind of bug that is nicknamed a *Heisenbug* (the same article). This file demonstrates a race three ways: by examining every possible schedule, by forcing real threads to collide, and by letting them race unaided. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon).

## ➕ The Lost Update

The standard example is two threads that each add 1 to a shared counter that starts at 0. Each thread performs three steps: read the counter into a private variable, add 1 to that private copy, and write the result back. The expected final value is 2. If thread B reads before thread A has written, though, B starts from the old value, and one increment disappears:

| Step | Thread A | Thread B | Counter |
|------|----------|----------|---------|
| 1 | read (sees 0) | | 0 |
| 2 | | read (sees 0) | 0 |
| 3 | add 1 (has 1) | | 0 |
| 4 | | add 1 (has 1) | 0 |
| 5 | write 1 | | 1 |
| 6 | | write 1 | 1 |

Both threads did exactly what their code says, and yet the final value is 1, not 2. This is a **lost update**, the signature failure of a race on a read-modify-write sequence. How likely it is depends on how many of the possible schedules go wrong, and a short program can count them all.

## 🔬 Trying Every Schedule

Because a thread's steps are fixed and only their interleaving varies, it is possible to *enumerate* all the schedules mechanically. The function below does so for any small set of thread programs. A thread program is a list of atomic steps (read a shared variable into a private register, compute on registers, write a shared variable, and, in later files, acquire and release locks). The explorer tries every order in which the threads' steps can be taken, and reports how many schedules end in each final state, how many end in a deadlock, and how many distinct situations it passed through. It counts schedules without listing them by recording, for each situation, how many schedules lead to it:

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

The next block describes the two incrementing threads as programs and explores them:

```python
increment = [("read", "counter", "r"), ("local", "r", lambda registers: registers["r"] + 1), ("write", "counter", lambda registers: registers["r"])]

def show(outcomes, deadlocks):
    total = sum(outcomes.values()) + sum(deadlocks.values())
    for memory, count in sorted(outcomes.items()):
        print(f"  final {dict(memory)}: {count} of {total} schedules")
    for situation, count in deadlocks.items():
        print(f"  DEADLOCK {situation}: {count} of {total} schedules")

outcomes, deadlocks, states = explore({"A": increment, "B": increment}, {"counter": 0})
print("two threads, no protection:")
show(outcomes, deadlocks)
```

```text
two threads, no protection:
  final {'counter': 1}: 18 of 20 schedules
  final {'counter': 2}: 2 of 20 schedules
```

Of the 20 possible schedules, only 2 give the right answer, the two in which one thread finishes completely before the other starts; the other 18 lose an update. (Real schedules are not equally likely, which is why a real program usually gets lucky, and why the bug seems rare.) With three threads the odds are worse still:

```python
outcomes, deadlocks, states = explore({name: increment for name in "ABC"}, {"counter": 0})
print("three threads, no protection:")
show(outcomes, deadlocks)
```

```text
three threads, no protection:
  final {'counter': 1}: 1404 of 1680 schedules
  final {'counter': 2}: 270 of 1680 schedules
  final {'counter': 3}: 6 of 1680 schedules
```

Only 6 of 1,680 schedules end with the expected 3. The correctness of the program depends on the thread scheduler never choosing the other 99.6% of the schedules, which is not something a program can rely on.

## 🧵 Real Threads: Forcing the Collision

The explorer is a model. Real threads exhibit the same behaviour, but in a normal run it is a matter of luck whether the unlucky timing occurs. To reproduce a race *reliably*, a test can force the unlucky timing with a synchronization device, here a `threading.Barrier`, which makes each thread wait until all the others have reached it. First the lost update, with the barrier placed between the read and the write so that both threads read before either writes:

```python
import threading

def forced_lost_update():
    shared = {"value": 0}
    both_have_read = threading.Barrier(2)

    def worker():
        seen = shared["value"]                      # read
        both_have_read.wait()                       # wait until the other thread has read as well
        shared["value"] = seen + 1                  # write a result based on the value read earlier

    threads = [threading.Thread(target=worker) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return shared["value"]

print("two increments, forced to overlap, five runs:", [forced_lost_update() for _ in range(5)])
```

```text
two increments, forced to overlap, five runs: [1, 1, 1, 1, 1]
```

The result is 1 every time. The second pattern is the **check-then-act** race, in which a decision is made on information that is no longer true by the time it is used. A bank account holds 100, and two threads each try to withdraw 80. Each first checks that the balance covers the withdrawal and only then subtracts it; the barrier makes both checks happen before either subtraction:

```python
def forced_overdraft():
    account = {"balance": 100}
    both_have_checked = threading.Barrier(2)

    def withdraw(amount):
        if account["balance"] >= amount:            # check: is there enough money?
            both_have_checked.wait()                # the other thread checks before either one acts
            account["balance"] -= amount            # act: take the money

    threads = [threading.Thread(target=withdraw, args=(80,)) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return account["balance"]

print("two withdrawals of 80 from a balance of 100 leave:", forced_overdraft())
```

```text
two withdrawals of 80 from a balance of 100 leave: -60
```

Each thread saw 100 and was entitled to 80, but together they took 160 and left the account at −60. Each check was correct when made; it was the gap between check and action that was fatal.

## 🎲 Letting Them Race Unaided

Finally, no barrier at all: four threads each add 1 to a shared global counter a quarter of a million times, so the correct total is 1,000,000. Each run below starts a fresh set of threads:

```python
import sys

counter = 0

def bump(times):
    global counter
    for _ in range(times):
        counter += 1                                # an unprotected read-modify-write

def unprotected_run(threads=4, times=250_000):
    global counter
    counter = 0
    workers = [threading.Thread(target=bump, args=(times,)) for _ in range(threads)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
    return counter

print("the interpreter's thread-switch interval:", sys.getswitchinterval(), "seconds")
print("four threads, 250,000 increments each (correct total 1,000,000):")
for result in [unprotected_run() for _ in range(8)]:
    print(f"  {result:>9,}  ({1_000_000 - result:,} increments lost)")
```

One run on the test machine printed:

```
the interpreter's thread-switch interval: 0.005 seconds
four threads, 250,000 increments each (correct total 1,000,000):
    713,901  (286,099 increments lost)
    541,842  (458,158 increments lost)
    508,950  (491,050 increments lost)
    765,111  (234,889 increments lost)
    730,544  (269,456 increments lost)
    690,403  (309,597 increments lost)
    692,347  (307,653 increments lost)
    770,952  (229,048 increments lost)
```

On the Mac used for this module, the totals in a typical set of eight runs were all over the place: some runs lost hundreds of thousands of increments, and some, by luck, lost none. This is the nature of a race: the interpreter may switch threads every few milliseconds (the interval printed above), and whenever the switch lands between the load and the store of `counter`, an increment is lost. The figures differ from run to run, from machine to machine, and between Python versions, so the numbers matter less than the fact that the program has no single answer.

## 🛠️ What To Do About Races

The remedies correspond to the three approaches in [understanding-concurrency.md](understanding-concurrency.md):

- **Make the critical section mutually exclusive.** Only one thread at a time may perform the read-modify-write, which is what a lock does ([mutex-and-semaphores.md](mutex-and-semaphores.md)). The lock must cover the whole sequence, including the check of a check-then-act.
- **Use an operation that is atomic by construction**, such as the atomic increment or compare-and-swap instruction that hardware provides, or a data structure designed for concurrent use.
- **Do not share mutable data**: send messages through a queue, give each thread its own copy and combine the results at the end, or use immutable data.
- **Use tools.** Static analysis tools can flag suspicious code without running it, and dynamic analysis tools such as ThreadSanitizer and Helgrind watch a running program for conflicting accesses ([Wikipedia: Race condition](https://en.wikipedia.org/wiki/Race_condition)). They find races that testing may miss, but they only report the schedules that actually ran.

## ✅ Checking the Explorer

The explorer was checked against an independent method: a plain recursive enumeration of every schedule, written separately and without any merging of situations, on 1,029 random small programs: 629 mixing reads, computations, writes, and lock sections, and 400 built from nested lock acquisitions, in all of which 149 could deadlock. For each program, the number of schedules ending in every final state, and in every deadlock, was identical.

## Common Misconceptions

- **"A race condition only matters when the machine has several cores."** A single core can interleave threads at any instruction boundary, so races occur on one core too.
- **"My code works, so there is no race."** Races are rare in testing because the dangerous window is short. The unprotected counter above sometimes returns the right answer.
- **"Using `+=` or `append` makes it atomic."** A single source line can be several machine or bytecode steps, as the disassembly in [understanding-concurrency.md](understanding-concurrency.md) showed.
- **"Adding a `sleep` or a print fixes the bug."** It only changes the timing, and may hide the bug, which is what makes races Heisenbugs.
- **"Races are only about counters."** Any check-then-act sequence is exposed: testing whether a file exists before creating it, checking a balance before withdrawing, checking a cache before filling it.

## ➡️ Next

Continue to [mutex-and-semaphores.md](mutex-and-semaphores.md): the tools that make a critical section exclusive, a lock for one thread at a time and a semaphore for a limited number, with the same explorer to prove that the race is gone.
