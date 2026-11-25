# 🔗 Deadlocks

## Waiting for Each Other for Ever

[mutex-and-semaphores.md](mutex-and-semaphores.md) ended with a warning: locks cure races, but a thread that holds one lock while it waits for another can end up waiting for something that will never happen. A **deadlock** is any situation in which no member of a group of entities can proceed because each is waiting for another member, including possibly itself, to take some action, most commonly to release a lock. In an operating system it appears when a process or thread enters the waiting state because a resource it requested is held by another waiting process, which is in turn waiting for a resource held by yet another waiting process ([Wikipedia: Deadlock](https://en.wikipedia.org/wiki/Deadlock_(computer_science))). The simplest case needs only two threads and two locks: thread A holds lock 1 and wants lock 2, while thread B holds lock 2 and wants lock 1. Neither can move, neither will ever release what it holds, and the program hangs without an error message.

This file shows how a deadlock arises, finds one by exhaustive search, draws its signature (a cycle in a graph of who waits for whom), applies the same tools to the dining philosophers, and distinguishes deadlock from the related failures of livelock and starvation. It uses the schedule explorer from [race-conditions.md](race-conditions.md), repeated here so that the file runs on its own. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon).

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

## 📋 The Four Conditions

A deadlock can arise only if four conditions hold at the same time. They are known as the **Coffman conditions**, after their first description in a 1971 article by Edward G. Coffman Jr. ([Wikipedia: Deadlock](https://en.wikipedia.org/wiki/Deadlock_(computer_science))):

| Condition | Meaning | In the two-lock example |
|-----------|---------|-------------------------|
| **Mutual exclusion** | Each resource can be used by only one thread at a time | A lock can be held by one thread only |
| **Hold and wait** | A thread holds at least one resource while waiting for another | A holds lock 1 while waiting for lock 2 |
| **No preemption** | A resource can be released only by the thread holding it, voluntarily | Nobody can take lock 1 away from A |
| **Circular wait** | A cycle of threads, each waiting for a resource held by the next | A waits for B, and B waits for A |

The same source adds a precision: for resources of which there is only one instance each (such as a lock), the four conditions together are enough to produce a deadlock, but where resources have several instances they show only that deadlock is possible (the same article). The conditions are also the key to defences: remove any one, and deadlock cannot happen, which is the subject of [deadlock-prevention.md](deadlock-prevention.md).

## 🔍 Finding a Deadlock by Exhaustive Search

Describe the two threads as programs for the explorer. Thread A takes lock 1 and then lock 2, and thread B takes them in the opposite order. A small function reports how many of the possible schedules finish and how many end stuck, and names the locks held in a stuck situation. The second run gives both threads the same lock order:

```python
def verdict(programs, shared=None):
    outcomes, deadlocks, states = explore(programs, shared or {})
    finished, stuck = sum(outcomes.values()), sum(deadlocks.values())
    print(f"{finished + stuck:,} schedules: {finished:,} finish, {stuck:,} deadlock ({states} situations explored)")
    for (counters, locks), count in deadlocks.items():
        print(f"  stuck in {count} schedule(s) with:", ", ".join(f"{owner} holding {lock}" for lock, owner in locks))

a_then_b = [("acquire", "L1"), ("acquire", "L2"), ("release", "L2"), ("release", "L1")]
b_then_a = [("acquire", "L2"), ("acquire", "L1"), ("release", "L1"), ("release", "L2")]
print("A takes L1 then L2; B takes L2 then L1:")
verdict({"A": a_then_b, "B": b_then_a})
print("both take L1 then L2:")
verdict({"A": a_then_b, "B": a_then_b})
```

```text
A takes L1 then L2; B takes L2 then L1:
6 schedules: 4 finish, 2 deadlock (19 situations explored)
  stuck in 2 schedule(s) with: A holding L1, B holding L2
both take L1 then L2:
2 schedules: 2 finish, 0 deadlock (16 situations explored)
```

In 2 of the 6 possible schedules, A gets L1 and B gets L2 before either asks for its second lock, and the program is stuck; in the other 4, one thread obtains both of its locks before the other has taken any, and everything finishes without trouble. This is why deadlocks survive testing: most schedules are fine, and the program passes thousands of runs before the fatal interleaving occurs in production. With the same lock order in both threads, no schedule deadlocks; the circle cannot form.

## 🧵 A Real Deadlock, Without the Hang

Real threads can be made to deadlock reliably in the same way, with a barrier that guarantees that both threads hold their first lock before either asks for the second. A genuine deadlock would hang the program for ever, so the second request in this experiment gives up after 0.3 seconds, which also shows what a timeout tells you. A second barrier keeps either thread from releasing its lock until both have finished trying:

```python
import threading

def real_deadlock():
    first, second = threading.Lock(), threading.Lock()
    both_hold_one = threading.Barrier(2)
    both_have_tried = threading.Barrier(2)
    got_second = {}

    def worker(name, mine, other):
        with mine:
            both_hold_one.wait()                        # now each thread holds one lock
            got_second[name] = other.acquire(timeout=0.3)   # a patient thread would wait for ever here
            both_have_tried.wait()                      # neither lets go until both have tried
            if got_second[name]:
                other.release()

    threads = [threading.Thread(target=worker, args=("A", first, second)), threading.Thread(target=worker, args=("B", second, first))]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return dict(sorted(got_second.items()))

print("did each thread get its second lock?", real_deadlock())
```

```text
did each thread get its second lock? {'A': False, 'B': False}
```

Neither thread could get its second lock, so each waited out its timeout. In a program without timeouts, both would still be waiting. (Python's `Lock.acquire` waits for ever by default; the `timeout` argument is the exception, not the rule.)

## 🕸️ The Signature: a Cycle in the Wait-For Graph

A deadlock has a recognizable shape. Draw one node for each thread and an arrow from thread X to thread Y when X is waiting for something that Y holds: this is the **wait-for graph**. For resources that exist in one instance each, the threads are deadlocked exactly when the graph contains a cycle. A thread waits for at most one other thread at a time here, so a cycle can be found by following the arrows from every starting point until one revisits a node. The function below does it, and `wait_for_graph` builds the graph from a stuck situation reported by the explorer: a stuck thread is waiting at an `acquire` of a lock that another thread holds:

```python
def find_cycle(graph):
    """graph maps each waiting thread to the thread it waits for (or None). Returns the threads in a cycle, or None."""
    for start in graph:
        seen, node = [], start
        while node is not None and node not in seen:
            seen.append(node)
            node = graph.get(node)
        if node is not None:                        # we came back to a thread we had already visited: a cycle
            return seen[seen.index(node):]
    return None

def wait_for_graph(programs, counters, locks):
    """For a stuck situation: which thread is each unfinished thread waiting for?"""
    owner = dict(locks)
    graph = {}
    for (name, program), counter in zip(programs.items(), counters):
        if counter < len(program):
            graph[name] = owner[program[counter][1]]    # the step it is stuck on is an acquire of a lock someone holds
    return graph

programs = {"A": a_then_b, "B": b_then_a}
outcomes, deadlocks, states = explore(programs, {})
for counters, locks in deadlocks:
    graph = wait_for_graph(programs, counters, locks)
    print("who waits for whom:", graph, "| cycle:", find_cycle(graph))

print("a chain that ends in a thread that can run:", find_cycle({"A": "B", "B": "C", "C": None}))
print("a cycle with a thread queued behind it:    ", find_cycle({"T": "A", "A": "B", "B": "C", "C": "A"}))
```

```text
who waits for whom: {'A': 'B', 'B': 'A'} | cycle: ['A', 'B']
a chain that ends in a thread that can run: None
a cycle with a thread queued behind it:     ['A', 'B', 'C']
```

The deadlocked situation is the graph with A pointing at B and B pointing at A: a cycle of length two. A chain of waiting threads that ends in one that can still run is not a deadlock, since the front of the chain will eventually finish and release what the others need. A thread queued *behind* a cycle (T above) is not in the cycle, but is stuck all the same, because what it waits for will never come. Operating systems and database systems keep a graph of this kind and look for cycles to detect deadlocks.

## 🍝 The Dining Philosophers

The dining philosophers problem was formulated in 1965 by Edsger Dijkstra as an examination exercise, about computers competing for tape drives, and named by Tony Hoare soon afterwards. Philosophers sit round a table, with one fork between each pair of neighbours; to eat, a philosopher needs both the left and the right fork, and the problem is to design a rule such that every philosopher can go on eating and thinking for ever without anyone starving ([Wikipedia: Dining philosophers problem](https://en.wikipedia.org/wiki/Dining_philosophers_problem)). The obvious rule, "pick up the left fork, then the right", looks harmless, but if every philosopher picks up the left fork at the same time, each holds one fork and waits for the one held by the neighbour: all four Coffman conditions hold. The explorer can examine tables of three, four, and five philosophers. In the *ordered* variant, each philosopher picks up the lower-numbered of their two forks first:

```python
def philosopher(seat, seats, ordered):
    left, right = seat, (seat + 1) % seats
    first, second = (min(left, right), max(left, right)) if ordered else (left, right)
    return [("acquire", f"fork{first}"), ("acquire", f"fork{second}"), ("release", f"fork{second}"), ("release", f"fork{first}")]

print(f"{'philosophers':>12} | {'rule':<22} | {'schedules':>11} | {'deadlocked':>10}")
for seats in (3, 4, 5):
    for ordered in (False, True):
        table = {f"P{seat}": philosopher(seat, seats, ordered) for seat in range(seats)}
        outcomes, deadlocks, states = explore(table, {})
        rule = "lower fork first" if ordered else "left fork, then right"
        print(f"{seats:>12} | {rule:<22} | {sum(outcomes.values()) + sum(deadlocks.values()):>11,} | {sum(deadlocks.values()):>10,}")

table = {f"P{seat}": philosopher(seat, 3, False) for seat in range(3)}
outcomes, deadlocks, states = explore(table, {})
for counters, locks in deadlocks:
    print("with three philosophers and the left-then-right rule, the stuck situation has the cycle", find_cycle(wait_for_graph(table, counters, locks)))
```

```text
philosophers | rule                   |   schedules | deadlocked
           3 | left fork, then right  |         168 |          6
           3 | lower fork first       |         142 |          0
           4 | left fork, then right  |      98,184 |         24
           4 | lower fork first       |      64,000 |          0
           5 | left fork, then right  |  66,468,720 |        120
           5 | lower fork first       |  49,719,072 |          0
with three philosophers and the left-then-right rule, the stuck situation has the cycle ['P0', 'P1', 'P2']
```

With "left fork, then right" there is exactly one stuck situation, the one in which every philosopher holds a left fork, and it can be reached in *n*! different orders (6, 24, and 120 for 3, 4, and 5 philosophers): a vanishing fraction of all the schedules, 0.00018% of them for five philosophers. Yet the search finds it with certainty, and a real table would meet it sooner or later. With the lower-numbered fork always first, no schedule deadlocks, because the circle of waiting cannot close: a philosopher who is waiting holds only forks numbered lower than the one being waited for, so following the chain of waits always leads to higher-numbered forks and can never come back round to the start. This idea, a global order on the locks, is the most practical way to prevent deadlock, and [deadlock-prevention.md](deadlock-prevention.md) uses it on a bank.

## 🔄 Livelock and Starvation

Two relatives of deadlock are worth separating from it. In a **livelock**, the threads are not blocked: their states keep changing in response to one another, yet none makes progress. The term was coined by Edward A. Ashcroft in 1975, in connection with airline booking systems, and a livelock is a special case of resource starvation ([Wikipedia: Deadlock](https://en.wikipedia.org/wiki/Deadlock_(computer_science))). The classic picture is two people meeting in a corridor who both step aside, then both step back, for ever. In code, this is a "polite" thread that gives up what it holds when it cannot get the second lock, and tries again at exactly the same moment as its rival:

```python
def livelock(rounds=5):
    left, right = threading.Lock(), threading.Lock()
    in_step = threading.Barrier(2)                      # keeps the two threads in perfect step, as an unlucky schedule might
    finished = []

    def polite(name, mine, other):
        for attempt in range(rounds):
            mine.acquire()
            in_step.wait()                              # both now hold their first lock
            got_it = other.acquire(blocking=False)      # try for the second lock without waiting
            in_step.wait()
            if got_it:
                finished.append(name)
                other.release()
                mine.release()
                return
            mine.release()                              # polite: give way, then try again at once
            in_step.wait()

    threads = [threading.Thread(target=polite, args=("A", left, right)), threading.Thread(target=polite, args=("B", right, left))]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return finished

print(f"threads that finished after 5 polite rounds: {livelock()}")
```

```text
threads that finished after 5 polite rounds: []
```

Both threads were active in every round (acquiring, trying, releasing), and neither ever finished. It is the retry strategy of the next file, with one ingredient missing: a *random* delay before retrying, which breaks the symmetry. A third failure, **starvation**, is one in which a particular process is perpetually denied the resources it needs, whether because of a flaw in a scheduling or mutual exclusion algorithm or a resource leak ([Wikipedia: Resource starvation](https://en.wikipedia.org/wiki/Resource_starvation)); [priority-scheduling.md](../cpu-scheduling/priority-scheduling.md) showed it together with its cure, aging. In a deadlock *nothing* can move; in a livelock everything moves and nothing progresses; in starvation the system as a whole progresses and one participant never does.

## 🏭 Deadlocks in Real Systems

Most current operating systems cannot prevent deadlocks, and different systems respond to them in different, non-standard ways ([Wikipedia: Deadlock](https://en.wikipedia.org/wiki/Deadlock_(computer_science))). The simplest policy is to **ignore** the problem on the assumption that deadlocks are rare and the damage tolerable: the *ostrich algorithm*, which the same article says MINIX and UNIX used initially. Databases take the opposite approach: they expect deadlocks, detect them, and recover. PostgreSQL's manual states that it automatically detects deadlock situations and resolves them by aborting one of the transactions involved, so that the others can complete, and that the best defence is to make all applications take locks on multiple objects in a consistent order, with retrying of aborted transactions as the fallback ([PostgreSQL documentation: Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html)). The Linux kernel contains a **runtime locking correctness validator**, lockdep, that tracks the dependencies between classes of locks, where a dependency L1 → L2 means that a task tried to take L2 while holding L1, and reports locking patterns that could deadlock, even if no deadlock has happened yet ([Linux kernel documentation: Runtime locking correctness validator](https://docs.kernel.org/locking/lockdep-design.html)). In Python, a hung program can be diagnosed with `faulthandler.dump_traceback_later`, which dumps the tracebacks of all threads after a timeout and shows where each is stuck ([Python docs: `faulthandler`](https://docs.python.org/3/library/faulthandler.html)).

## 🧰 Four Ways to Handle Deadlock

| Strategy | Idea | Cost |
|----------|------|------|
| **Ignore** it | Deadlocks are rare; restart when one happens | Free, until it happens |
| **Detect and recover** | Let deadlocks happen, find the cycle, break it by aborting or rolling back a victim | Needs the graph, and a safe way to undo work |
| **Avoid** it | Grant a request only if the system stays in a state from which everything can still finish (the banker's algorithm) | Needs advance knowledge of the maximum demands |
| **Prevent** it | Make one of the four conditions impossible, for example by ordering the locks | Restricts how resources may be used |

[deadlock-prevention.md](deadlock-prevention.md) takes the last three one at a time.

## ✅ Checking the Code

The cycle finder was compared with an independent method (Floyd's tortoise-and-hare cycle detection, which does not record visited nodes) on 5,000 random waiting graphs of up to 12 threads: both agreed on whether there was a cycle, and the cycle returned was always a genuine cycle of the graph. For the philosophers, the exhaustive search was repeated for two to six seats: in each case the deadlocked schedules numbered exactly *n*! with the left-then-right rule and none with the ordered rule.

## Common Misconceptions

- **"A deadlock means the program crashed."** It means the program is *alive but stuck*: no error, no exception, no CPU use, just threads waiting. That is what makes deadlocks hard to notice.
- **"If it ran fine a thousand times, there is no deadlock."** The fatal interleaving may be one among millions, as the philosophers' count showed.
- **"Deadlock needs many threads."** Two threads and two locks are enough, and one thread is enough for a plain non-reentrant lock taken twice.
- **"A timeout fixes the deadlock."** It turns an eternal hang into an error you must handle, and a careless retry can turn it into a livelock.
- **"Deadlock, livelock, and starvation are the same."** In a deadlock nothing moves, in a livelock everything moves and nothing is achieved, and in starvation everything else makes progress while one participant never does.

## ➡️ Next

Continue to [deadlock-prevention.md](deadlock-prevention.md): how to make deadlock impossible by breaking one of the four conditions, how the banker's algorithm avoids it by never entering an unsafe state, and how detection and recovery work when neither is practical.
