# 🛡️ Deadlock Prevention, Avoidance, and Detection

## Three Ways to Deal With a Deadlock That You Cannot Ignore

[deadlocks.md](deadlocks.md) listed four ways to handle deadlock: ignore it, prevent it, avoid it, or detect it and recover. Ignoring is cheap but only suits rare, harmless deadlocks. This file takes the other three in turn. **Prevention** makes deadlock impossible by design, by ensuring that at least one of the four Coffman conditions can never hold. **Avoidance** lets all four conditions exist but refuses any request that could lead the system into a state from which deadlock cannot be escaped. **Detection and recovery** lets deadlocks happen, notices them, and breaks them. Each trades something away: freedom in how resources are used, advance knowledge of what processes will need, or lost work. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon). The first part uses the schedule explorer from [race-conditions.md](race-conditions.md), repeated here so that the file runs on its own.

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

## 🚫 Prevention: Remove One Condition

Deadlock prevention works by preventing one of the four Coffman conditions from occurring ([Wikipedia: Deadlock](https://en.wikipedia.org/wiki/Deadlock_(computer_science))). The options differ greatly in practicality:

| Condition removed | How | Price |
|-------------------|-----|-------|
| **Mutual exclusion** | Make the resource shareable, or serve it indirectly: print jobs go to a queue (spooling) instead of locking the printer; use non-blocking algorithms | Impossible for a resource that must be used exclusively, and even spooled resources can still deadlock |
| **Hold and wait** | Request everything needed at once, or release everything held before asking for more ("all or none") | The needs must be known in advance; resources are held idle for long periods; a process needing a popular resource may starve |
| **No preemption** | If a request cannot be granted at once, release what is held and start again, or let the system take resources away | Taking a resource back usually means rolling work back, which is costly; works only for resources that can be saved and restored |
| **Circular wait** | Number the resources and require every process to request them in increasing order | The order must be known and respected by every piece of code |

(The table summarizes the prevention section of the same Wikipedia article.) The last row is the one used most in practice, because it asks for nothing but discipline.

### Breaking Circular Wait: Lock Ordering

Two threads transfer money between accounts *a* and *b*: one moves 10 from *a* to *b*, the other moves 5 from *b* to *a*. Each transfer locks the account it takes from and then the account it gives to, updates both balances, and unlocks. In the first run, each takes its locks in the order "source, then target", which are opposite for the two threads. In the second, both take the lock of the account with the lower name first, whichever is the source:

```python
def transfer(amount, source, target, ordered):
    first, second = sorted((source, target)) if ordered else (source, target)
    return [("acquire", f"lock_{first}"), ("acquire", f"lock_{second}"),
            ("read", source, "s"), ("local", "s", lambda registers, a=amount: registers["s"] - a), ("write", source, lambda registers: registers["s"]),
            ("read", target, "t"), ("local", "t", lambda registers, a=amount: registers["t"] + a), ("write", target, lambda registers: registers["t"]),
            ("release", f"lock_{second}"), ("release", f"lock_{first}")]

for ordered in (False, True):
    programs = {"T1": transfer(10, "a", "b", ordered), "T2": transfer(5, "b", "a", ordered)}
    outcomes, deadlocks, states = explore(programs, {"a": 100, "b": 100})
    total = sum(outcomes.values()) + sum(deadlocks.values())
    finals = {tuple(dict(memory).items()): count for memory, count in outcomes.items()}
    print(f"{'lowest account first' if ordered else 'source first, then target'}: {sum(deadlocks.values())} of {total} schedules deadlock; the ones that finish end with {finals}")
```

```text
source first, then target: 2 of 6 schedules deadlock; the ones that finish end with {(('a', 95), ('b', 105)): 4}
lowest account first: 0 of 2 schedules deadlock; the ones that finish end with {(('a', 95), ('b', 105)): 2}
```

With the lock order tied to the source and the target, a third of the schedules deadlock (the two threads each take their first lock and wait for the other's). With a global order, no schedule can, and every one ends with the same balances (95 and 105): the money is conserved. The rule scales. Here is the same idea on a bank with five accounts, where eight threads make 2,000 random transfers each, always locking the account with the lower number first, with real locks and no timeouts. If the rule were broken, the program could hang; with it, the run always finishes, and the total money is unchanged:

```python
import random
import threading
import time

def ordered_bank(accounts=5, threads=8, transfers=2000, seed=0):
    balances = [1000] * accounts
    locks = [threading.Lock() for _ in range(accounts)]

    def worker(index):
        rng = random.Random(seed * 100 + index)
        for _ in range(transfers):
            source, target = rng.sample(range(accounts), 2)
            amount = rng.randint(1, 50)
            first, second = sorted((source, target))        # the rule: always lock the lower-numbered account first
            with locks[first]:
                with locks[second]:
                    if balances[source] >= amount:
                        balances[source] -= amount
                        balances[target] += amount

    workers = [threading.Thread(target=worker, args=(index,)) for index in range(threads)]
    for worker_thread in workers:
        worker_thread.start()
    for worker_thread in workers:
        worker_thread.join()
    return sum(balances), min(balances) >= 0

for seed in range(3):
    total, never_negative = ordered_bank(seed=seed)
    print(f"run {seed + 1}: 16,000 transfer attempts finished; total money {total:,} (was 5,000); no balance negative: {never_negative}")
```

```text
run 1: 16,000 transfer attempts finished; total money 5,000 (was 5,000); no balance negative: True
run 2: 16,000 transfer attempts finished; total money 5,000 (was 5,000); no balance negative: True
run 3: 16,000 transfer attempts finished; total money 5,000 (was 5,000); no balance negative: True
```

### Breaking Hold and Wait: Take Both or None

Sometimes no global order is available. Another way is never to *wait* while holding a lock: try to take both locks without blocking, and if either is busy, release anything held, pause, and try again. The pause must be **random**, or two rivals retry in step for ever (the livelock of [deadlocks.md](deadlocks.md)). Here the same bank runs in this style, with no lock ordering at all, and each transfer does a little work (half a millisecond) while it holds both accounts, to make collisions common:

```python
def acquire_both(first, second, rng):
    """Take two locks without ever holding one while waiting for the other. Returns how many times it had to retry."""
    retries = 0
    while True:
        if first.acquire(blocking=False):
            if second.acquire(blocking=False):
                return retries
            first.release()                                 # could not get both: let go of everything
        retries += 1
        time.sleep(rng.uniform(0, 0.001))                   # a random pause breaks the symmetry between rivals

def try_both_bank(accounts=4, threads=8, transfers=40, seed=0):
    balances = [1000] * accounts
    locks = [threading.Lock() for _ in range(accounts)]
    retries = [0] * threads

    def worker(index):
        rng = random.Random(seed * 100 + index)
        for _ in range(transfers):
            source, target = rng.sample(range(accounts), 2)         # no ordering: any pair, in any direction
            amount = rng.randint(1, 50)
            retries[index] += acquire_both(locks[source], locks[target], rng)
            time.sleep(0.0005)                                      # work done while holding both accounts
            if balances[source] >= amount:
                balances[source] -= amount
                balances[target] += amount
            locks[target].release()
            locks[source].release()

    workers = [threading.Thread(target=worker, args=(index,)) for index in range(threads)]
    for worker_thread in workers:
        worker_thread.start()
    for worker_thread in workers:
        worker_thread.join()
    return sum(balances), min(balances) >= 0, sum(retries)

for seed in range(3):
    total, never_negative, retries = try_both_bank(seed=seed)
    print(f"run {seed + 1}: 320 transfer attempts finished; total money {total:,} (was 4,000); no balance negative: {never_negative}; lock attempts that had to be retried: {retries:,}")
```

One run on the test machine printed:

```
run 1: 320 transfer attempts finished; total money 4,000 (was 4,000); no balance negative: True; lock attempts that had to be retried: 1,265
run 2: 320 transfer attempts finished; total money 4,000 (was 4,000); no balance negative: True; lock attempts that had to be retried: 1,421
run 3: 320 transfer attempts finished; total money 4,000 (was 4,000); no balance negative: True; lock attempts that had to be retried: 1,421
```

Every transfer finished and the books balance, without any ordering rule, but the price is visible in the last figure: each transfer attempt needed several tries on average, and the time spent in the pauses is lost. This approach also leans on the same randomness that fixes livelock, which is why it is a pattern rather than a guarantee: with unlucky random numbers a thread could in principle keep losing.

## 🏦 Avoidance: the Banker's Algorithm

Avoidance asks a different question. Instead of forbidding a condition, it examines each request and grants it only if the system will remain in a **safe state**. A state is safe if there is some order in which all the processes can run to completion, each one getting the resources it still needs from what is free plus what the earlier ones have returned. The best-known method is the **banker's algorithm**, developed by Edsger Dijkstra, which tests safety by simulating the allocation of the processes' declared maximum demands before deciding whether a request may proceed. The name comes from a bank that never lends out its money in a way that leaves it unable to satisfy all its customers' needs. The algorithm needs three pieces of information: the **maximum** each process may ever claim (declared in advance), how much each process currently **holds**, and how much is **available**; the remaining **need** of a process is its maximum minus its holdings ([Wikipedia: Banker's algorithm](https://en.wikipedia.org/wiki/Banker%27s_algorithm)). The classic textbook example has five processes and three kinds of resource, A, B, and C, of which the system owns 10, 5, and 7 units:

```python
def safe_sequence(available, maximum, allocated):
    """Return an order in which every process can finish (a 'safe sequence'), or None if the state is unsafe."""
    need = {p: [m - a for m, a in zip(maximum[p], allocated[p])] for p in maximum}
    work, finished, order = list(available), set(), []
    while len(finished) < len(maximum):
        for process in maximum:
            if process not in finished and all(n <= w for n, w in zip(need[process], work)):
                work = [w + a for w, a in zip(work, allocated[process])]      # it finishes and returns everything it held
                finished.add(process)
                order.append(process)
                break
        else:
            return None                                                      # nobody left can finish: the state is unsafe
    return order

def try_request(state, process, amount):
    """Grant `amount` to `process` only if the system stays safe. Returns (new state or None, explanation)."""
    available, maximum, allocated = state
    need = [m - a for m, a in zip(maximum[process], allocated[process])]
    if any(r > n for r, n in zip(amount, need)):
        return None, "refused: it asks for more than the maximum the process declared"
    if any(r > a for r, a in zip(amount, available)):
        return None, "must wait: not enough of the resource is free"
    new_available = [a - r for a, r in zip(available, amount)]
    new_allocated = {p: list(held) for p, held in allocated.items()}
    new_allocated[process] = [a + r for a, r in zip(allocated[process], amount)]
    order = safe_sequence(new_available, maximum, new_allocated)             # pretend to grant it, then test safety
    if order is None:
        return None, "must wait: granting it would leave the system in an unsafe state"
    return (new_available, maximum, new_allocated), f"granted: the system stays safe, for example in the order {order}"

maximum = {"P0": [7, 5, 3], "P1": [3, 2, 2], "P2": [9, 0, 2], "P3": [2, 2, 2], "P4": [4, 3, 3]}
allocated = {"P0": [0, 1, 0], "P1": [2, 0, 0], "P2": [3, 0, 2], "P3": [2, 1, 1], "P4": [0, 0, 2]}
state = ([3, 3, 2], maximum, allocated)
print("the starting state is safe, for example in the order", safe_sequence(*state))
for process, amount in (("P1", [1, 0, 2]), ("P4", [3, 3, 0]), ("P0", [0, 2, 0])):
    new_state, message = try_request(state, process, amount)
    print(f"{process} asks for {amount}: {message}")
    state = new_state or state                                               # a denied request changes nothing
```

```text
the starting state is safe, for example in the order ['P1', 'P3', 'P0', 'P2', 'P4']
P1 asks for [1, 0, 2]: granted: the system stays safe, for example in the order ['P1', 'P3', 'P0', 'P2', 'P4']
P4 asks for [3, 3, 0]: must wait: not enough of the resource is free
P0 asks for [0, 2, 0]: must wait: granting it would leave the system in an unsafe state
```

The starting state is safe: there is an order in which every process can finish. The first request is granted, because afterwards a safe order still exists. The second, from P4, cannot even be tried: the resources it asks for are not all free. The third, from P0, is the instructive one: the resources *are* free, and nothing is wrong yet, but giving them away would leave nobody able to finish, so the banker makes P0 wait. Note what an unsafe state means: not that a deadlock *has* occurred, but that one *could* be unavoidable, depending on what the processes ask for next. The algorithm is conservative: it assumes every process will claim its full declared maximum.

Avoidance is elegant, but it asks for a great deal: every process must declare its maximum needs in advance, the set of processes and resources must be fixed, and each request needs a safety check. General-purpose operating systems rarely meet these conditions, which is why the banker's algorithm is mainly a teaching tool and a model for specialized systems ([Wikipedia: Deadlock](https://en.wikipedia.org/wiki/Deadlock_(computer_science))).

## 🔎 Detection and Recovery

The third approach lets deadlocks happen and deals with them afterwards. Detecting a deadlock that has already occurred is easy in principle, since the operating system knows which resources each process holds and requests ([Wikipedia: Deadlock](https://en.wikipedia.org/wiki/Deadlock_(computer_science))). With one instance of each resource, a cycle in the wait-for graph of [deadlocks.md](deadlocks.md) is enough. With several instances of each resource, a variant of the safety test works: look for any process whose *current request* can be met from what is free; if it exists, assume that it finishes and gives back what it holds, and repeat. Whoever is left over when no more processes can finish is deadlocked. The block below applies it to another standard example, with five processes and the resources A, B, and C; nothing is free at the moment:

```python
def deadlocked(available, allocated, requests):
    """Processes that can never finish, given what is free, what each holds, and what each is waiting for."""
    work, finished = list(available), set()
    progress = True
    while progress:
        progress = False
        for process in allocated:
            if process not in finished and all(r <= w for r, w in zip(requests[process], work)):
                work = [w + a for w, a in zip(work, allocated[process])]      # it could finish, and would return what it holds
                finished.add(process)
                progress = True
    return [process for process in allocated if process not in finished]

holding = {"P0": [0, 1, 0], "P1": [2, 0, 0], "P2": [3, 0, 3], "P3": [2, 1, 1], "P4": [0, 0, 2]}
waiting_for = {"P0": [0, 0, 0], "P1": [2, 0, 2], "P2": [0, 0, 0], "P3": [1, 0, 0], "P4": [0, 0, 2]}
print("deadlocked processes:", deadlocked([0, 0, 0], holding, waiting_for))
waiting_for["P2"] = [0, 0, 1]                                                  # P2 now also asks for one more unit of C
print("after P2 asks for one more unit of C:", deadlocked([0, 0, 0], holding, waiting_for))
```

```text
deadlocked processes: []
after P2 asks for one more unit of C: ['P1', 'P2', 'P3', 'P4']
```

At first nobody is deadlocked: P0 and P2 need nothing more, finish, and return what they hold, which lets P3, then P1 and P4, finish. When P2 asks for one more unit of C, which nothing can supply, it can never finish, and neither can P1, P3, or P4, each of which is waiting for resources that only some member of the group can give. (P0 is unaffected, and finishes.)

Once a deadlock is found, the system must **recover**, and Wikipedia lists the two standard methods. *Process termination* aborts one or more of the processes in the deadlock: all of them, which is certain and fast but throws away their partial work, or one at a time until the deadlock disappears, which needs a new detection after each abort; the choice of victim considers factors such as priority and age. *Resource preemption* takes resources away from some processes and gives them to others until the cycle is broken ([Wikipedia: Deadlock](https://en.wikipedia.org/wiki/Deadlock_(computer_science))). Database systems make this routine: PostgreSQL detects deadlocks automatically and aborts one of the transactions involved, which the application can simply retry ([PostgreSQL documentation: Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html)).

## 🧭 What to Do in Practice

| Situation | Practical approach |
|-----------|--------------------|
| A program that takes several locks | Define one global lock order, document it, and follow it everywhere (the strongest and cheapest rule) |
| Locks whose order cannot be fixed in advance | Try-lock with random back-off, or a timeout that raises an error you handle |
| A database or transactional system | Expect deadlocks: keep transactions short, take locks in a consistent order, and retry when a transaction is aborted |
| A system with known, declared maximum needs | Avoidance (the banker's algorithm) is possible, and worth it only when the cost of a deadlock is high |
| Anything that might hang | Add timeouts and logging, and use diagnostic tools such as `faulthandler` in Python, and the lock validator in the Linux kernel ([Linux kernel documentation: Runtime locking correctness validator](https://docs.kernel.org/locking/lockdep-design.html)) |
| Code that does not need shared mutable state | Avoid the problem: pass messages through queues (see [understanding-concurrency.md](understanding-concurrency.md)) |

## ✅ Checking the Code

The two resource algorithms were compared with exhaustive searches. For `safe_sequence`, 3,000 random states (up to six processes and three resource types) were checked against a search over every possible order of the processes: the algorithm reported a safe state exactly when some order works, and the order it returned always worked. For `deadlocked`, 3,000 random situations were checked against a search over every possible sequence of finishings: the processes it reported were exactly those that can never finish in any sequence. `try_request` never granted a request that left the system unsafe. The ordered bank returned the exact total in 40 random runs, and the try-both bank in 20.

## Common Misconceptions

- **"A safe state is a state with no waiting."** A state is safe if some order lets every process finish; processes may well be waiting in a safe state, and they will be served in that order.
- **"An unsafe state is a deadlock."** It is a state from which deadlock *may* be unavoidable. The banker's algorithm refuses to enter it, even though a deadlock may never actually have happened.
- **"Lock ordering is enough if I only use two locks."** The rule must hold for *every* path through the program: one function that takes the locks in the other order brings the deadlock back.
- **"Retrying immediately is polite and safe."** Without a random delay, rivals can retry in step for ever, which turns a deadlock into a livelock.
- **"Databases do not have deadlocks."** They have them often; they detect and abort one transaction, and applications are expected to retry.

## ➡️ Next

This completes the Deadlocks and Concurrency module: how concurrent activities overlap, how overlapping on shared data goes wrong (races), how locks and semaphores prevent that, and how holding locks can in turn lead to deadlock and what to do about it. The next module of this section, File Systems, turns to a shared resource that every one of these mechanisms protects: the persistent store of files and directories on disk.
