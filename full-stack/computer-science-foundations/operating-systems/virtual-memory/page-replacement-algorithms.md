# 🔁 Page Replacement Algorithms

## Choosing a Victim

When a page fault needs a frame and none is free, the system must pick a **victim** to give up. If the victim has been modified, it must be written out before the frame can be reused, so a page that is merely read is cheaper to drop than one that was written. Most processors help by keeping two bits in each page table entry: the **access** (referenced) bit, set when the page is read or written, and the **dirty** bit, set when it is written ([Wikipedia: Page replacement algorithm](https://en.wikipedia.org/wiki/Page_replacement_algorithm)). A replacement policy can be **local**, choosing among the pages of the faulting process, or **global**, choosing among all pages in memory (the same article).

Policies are compared on a **reference string**, the sequence of page numbers a program touches, by counting the faults that each causes with a given number of frames. The lessons' simulators do exactly that. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon); every result in this file is deterministic.

## 🧪 Four Algorithms in Code

- **FIFO** (first in, first out) evicts the page that has been in memory the longest. It is simple and cheap, performs poorly in practice, and is rarely used unchanged.
- **LRU** (least recently used) evicts the page that has gone unused for the longest time, on the idea that recently used pages are likely to be used again soon. Keeping exact order on every access is expensive for a real system.
- **Clock** (second chance) is FIFO with a second chance: the frames form a circle with a hand. When a victim is needed, a page whose referenced bit is set is spared once, its bit cleared, and the hand moves on; the first page found with a clear bit is replaced.
- **OPT** (the optimal algorithm) evicts the page whose next use is farthest in the future. No real system can use it, because it needs to know the future; it is the yardstick that others are measured against.

These descriptions follow the Wikipedia article above. The textbook reference string below is a classic example:

```python
from collections import OrderedDict, deque

def fifo(refs, frames):
    memory, order, faults = set(), deque(), 0
    for page in refs:
        if page not in memory:
            faults += 1
            if len(memory) == frames:
                memory.remove(order.popleft())           # the page that came in first
            memory.add(page)
            order.append(page)
    return faults

def lru(refs, frames):
    memory, faults = OrderedDict(), 0                    # oldest use first
    for page in refs:
        if page in memory:
            memory.move_to_end(page)
        else:
            faults += 1
            if len(memory) == frames:
                memory.popitem(last=False)               # the page unused for longest
            memory[page] = None
    return faults

def clock(refs, frames):
    slots, referenced, where, hand, faults = [None] * frames, [False] * frames, {}, 0, 0
    for page in refs:
        if page in where:
            referenced[where[page]] = True               # the hardware sets the referenced bit
            continue
        faults += 1
        while slots[hand] is not None and referenced[hand]:
            referenced[hand] = False                     # a second chance
            hand = (hand + 1) % frames
        if slots[hand] is not None:
            del where[slots[hand]]
        slots[hand], where[page], referenced[hand] = page, hand, True
        hand = (hand + 1) % frames
    return faults

def optimal(refs, frames):
    next_use = [None] * len(refs)                        # next_use[i]: when is refs[i] used again?
    later = {}
    for i in range(len(refs) - 1, -1, -1):
        next_use[i] = later.get(refs[i], float("inf"))
        later[refs[i]] = i
    memory, faults = {}, 0                               # page -> time of its next use
    for i, page in enumerate(refs):
        if page not in memory:
            faults += 1
            if len(memory) == frames:
                del memory[max(memory, key=memory.get)]  # used again farthest in the future
        memory[page] = next_use[i]
    return faults

POLICIES = {"FIFO": fifo, "LRU": lru, "Clock": clock, "OPT": optimal}

def table(refs, frame_counts, policies=POLICIES):
    print("frames |" + "".join(f" {name:>8} |" for name in policies))
    for frames in frame_counts:
        print(f"{frames:>6} |" + "".join(f" {policy(refs, frames):>8,} |" for policy in policies.values()))

TEXTBOOK = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
table(TEXTBOOK, (3, 4))
```

```text
frames |     FIFO |      LRU |    Clock |      OPT |
     3 |       15 |       12 |       14 |        9 |
     4 |       10 |        8 |        9 |        8 |
```

With three frames, OPT needs only 9 faults; LRU needs 12; Clock, an approximation of LRU, needs 14; and FIFO needs 15. More frames help every algorithm here, which seems obvious, but it is not always true.

Real systems approximate LRU in cheaper ways. **NRU** (not recently used) clears the referenced bits at every clock interval and prefers to evict pages that have not been referenced or modified. **NFU** (not frequently used) counts, per page, the intervals in which it was referenced, but it remembers old popularity too long; **aging** fixes that by shifting each counter to the right before adding the new referenced bit at the left, so that recent references count for more. **Random** replacement picks any page, which avoids all bookkeeping; the Wikipedia article reports that it usually does better than FIFO, and better than LRU for looping reference patterns, although LRU generally performs better in practice.

## 🔄 Belady's Anomaly

One might expect that giving a program more frames can only reduce its faults. It was believed so until **Bélády's anomaly** was demonstrated: for FIFO there are reference strings on which *more* frames cause *more* faults ([Wikipedia: Bélády's anomaly](https://en.wikipedia.org/wiki/B%C3%A9l%C3%A1dy%27s_anomaly)):

```python
BELADY = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
table(BELADY, (3, 4))
```

```text
frames |     FIFO |      LRU |    Clock |      OPT |
     3 |        9 |       10 |        9 |        7 |
     4 |       10 |        8 |       10 |        6 |
```

FIFO faults 9 times with three frames and 10 times with four, and Clock, which behaves like FIFO when every referenced bit is set, does the same on this string. The anomaly can be very large: Bélády and co-authors built reference strings on which FIFO faulted nearly twice as often with the bigger memory, and in 2010 Fornai and Iványi showed that there is no limit to the ratio (the same article). LRU and OPT never show it, because they have the **stack property**: the pages held with *N* frames are always included among the pages held with *N* + 1 frames, so a hit with *N* frames is also a hit with *N* + 1, and more memory can never hurt; FIFO and random replacement do not have this property ([OSTEP: Beyond Physical Memory: Policies](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-beyondphys-policy.pdf)). For LRU it is easy to see why: with *N* frames, memory holds exactly the *N* most recently used pages.

## 🏁 No Policy Is Best

Which policy wins depends on the pattern of references. Two additions make that visible: **MRU** (evict the *most* recently used page) and a **two-list** policy. In the two-list policy a new page enters an *inactive* list, and only a second access promotes it to an *active* list, which is kept no larger than half of the memory; victims come from the inactive list. It is a simplified relative of what Linux does: its page cache keeps an **active** set and an **inactive** set, each in LRU order, where a page that is accessed repeatedly moves to the active set and only pages that leave the inactive set are paged out ([Wikipedia: Page replacement algorithm](https://en.wikipedia.org/wiki/Page_replacement_algorithm)). The same article describes **2Q**, which has the same two-queue idea, and **ARC**, which is particularly resistant to sequential scans. The two workloads are a loop over five pages, and a small hot set interrupted by one-off scans:

```python
import random

def mru(refs, frames):
    memory, faults = OrderedDict(), 0
    for page in refs:
        if page in memory:
            memory.move_to_end(page)
        else:
            faults += 1
            if len(memory) == frames:
                memory.popitem(last=True)                # the page used most recently
            memory[page] = None
    return faults

def two_list(refs, frames):
    active, inactive, faults = OrderedDict(), OrderedDict(), 0
    for page in refs:
        if page in active:
            active.move_to_end(page)
            continue
        if page in inactive:
            del inactive[page]                           # a second access: promote the page
            active[page] = None
        else:
            faults += 1
            if len(active) + len(inactive) == frames:
                (inactive if inactive else active).popitem(last=False)
            inactive[page] = None                        # new pages are on probation
        while len(active) > frames // 2:                 # keep the active list the smaller part
            demoted, _ = active.popitem(last=False)
            inactive[demoted] = None
    return faults

loop = list(range(5)) * 20                               # five pages, round and round

def hot_and_scan(rounds=20, hot=30, hot_refs=600, scan=100, seed=1):
    """A small hot set used again and again, interrupted by scans over pages that are never needed again."""
    rng = random.Random(seed)
    refs, next_cold_page = [], 1000
    for _ in range(rounds):
        refs += [rng.randrange(hot) for _ in range(hot_refs)]
        refs += range(next_cold_page, next_cold_page + scan)
        next_cold_page += scan
    return refs

everyone = {**POLICIES, "MRU": mru, "two-list": two_list}
print("a loop over 5 pages with 4 frames (100 references)")
table(loop, (4,), everyone)
print("\na hot set of 30 pages, interrupted by scans, with 64 frames (14,000 references)")
table(hot_and_scan(), (64,), everyone)
```

```text
a loop over 5 pages with 4 frames (100 references)
frames |     FIFO |      LRU |    Clock |      OPT |      MRU | two-list |
     4 |      100 |      100 |      100 |       28 |       28 |      100 |

a hot set of 30 pages, interrupted by scans, with 64 frames (14,000 references)
frames |     FIFO |      LRU |    Clock |      OPT |      MRU | two-list |
    64 |    2,600 |    2,600 |    2,600 |    2,030 |    4,896 |    2,030 |
```

In the loop, which is one page larger than memory, FIFO, LRU, Clock, and the two-list policy fault on **every** reference: they always throw out the page that the loop needs next. MRU, absurd as it sounds, matches the optimum. In the second workload it is the other way round: MRU is the worst, and each scan pushes the whole hot set out of the FIFO, LRU, and Clock memories, so after every scan the hot pages fault again. The two-list policy keeps them on its active list, out of reach of the scan, and matches OPT. Newer Linux kernels also offer a **multi-generational LRU**, an alternative implementation that optimizes page reclaim and improves performance under memory pressure ([Linux kernel documentation: Multi-Gen LRU](https://docs.kernel.org/admin-guide/mm/multigen_lru.html)).

## 🌋 Thrashing and the Working Set

When memory is overcommitted, a system can fall into **thrashing**: it spends so much of its time moving pages in and out that little useful work happens, and performance degrades or collapses ([Wikipedia: Thrashing](https://en.wikipedia.org/wiki/Thrashing_(computer_science))). The key idea is the **working set**: in Peter Denning's definition of 1968, the pages that a process has referenced during a recent interval of its execution, which approximates what it is about to need ([Wikipedia: Working set](https://en.wikipedia.org/wiki/Working_set)). Thrashing occurs when there is not enough memory to hold the working sets of all the active programs ([Wikipedia: Virtual memory](https://en.wikipedia.org/wiki/Virtual_memory)).

The simulation below shows the effect of putting more processes into a fixed amount of memory. There is one CPU and one paging disk; each process has its own LRU set of frames (local replacement); a reference that hits takes one unit of CPU time, a fault sends the process to the disk, where faults are served one at a time, each taking 200 units, and the CPU runs another ready process meanwhile (with a time slice of 50 references). Each process keeps a **working set of 8 pages**, which it changes after a random interval of 2,000 to 6,000 references. There are 64 frames in total:

```python
import heapq

def locality_refs(seed, working_set=8, phase=4000, pages=1000):
    """An endless reference string with locality: each phase uses a small random working set."""
    rng = random.Random(seed)
    while True:
        current = rng.sample(range(pages), working_set)
        for _ in range(rng.randint(phase // 2, phase * 3 // 2)):     # phases vary in length, so processes drift apart
            yield rng.choice(current)

def simulate(processes, total_frames, fault_cost=200, horizon=1_000_000, quantum=50):
    """One CPU, one paging disk, local LRU replacement. Returns the CPU utilization and the fault rate."""
    frames = total_frames // processes
    memory = [OrderedDict() for _ in range(processes)]
    streams = [locality_refs(seed) for seed in range(processes)]
    wanted = [next(stream) for stream in streams]               # the next reference of each process
    ready, waiting = deque(range(processes)), []                # waiting: a heap of (time the page arrives, process)
    time = busy = faults = disk_free = 0
    while time < horizon:
        if not ready:                                           # every process waits for the disk: the CPU is idle
            arrives, process = heapq.heappop(waiting)
            time = max(time, arrives)
            ready.append(process)
        while waiting and waiting[0][0] <= time:
            ready.append(heapq.heappop(waiting)[1])
        process = ready.popleft()
        used = 0
        while time < horizon:
            if used == quantum:                                 # time slice over: go to the back of the queue
                ready.append(process)
                break
            page = wanted[process]
            if page in memory[process]:
                memory[process].move_to_end(page)
                time += 1
                busy += 1
                used += 1
                wanted[process] = next(streams[process])
                while waiting and waiting[0][0] <= time:
                    ready.append(heapq.heappop(waiting)[1])
            else:                                               # a fault: queue for the disk and give up the CPU
                faults += 1
                if len(memory[process]) == frames:
                    memory[process].popitem(last=False)
                memory[process][page] = None
                disk_free = max(disk_free, time) + fault_cost
                heapq.heappush(waiting, (disk_free, process))
                break
    return {"frames each": frames, "cpu": busy / time, "faults per 1000 references": 1000 * faults / max(busy, 1),
            "busy": busy, "faults": faults, "time": time}

for processes in range(1, 17):
    result = simulate(processes, 64)
    bar = "#" * round(40 * result["cpu"])
    print(f"{processes:>2} running, {result['frames each']:>2} frames each: CPU {result['cpu']:>6.1%}   "
          f"faults/1000 refs {result['faults per 1000 references']:>6.1f}  {bar}")
```

```text
 1 running, 64 frames each: CPU  73.1%   faults/1000 refs    1.8  #############################
 2 running, 32 frames each: CPU  89.7%   faults/1000 refs    2.0  ####################################
 3 running, 21 frames each: CPU  96.9%   faults/1000 refs    2.0  #######################################
 4 running, 16 frames each: CPU  97.4%   faults/1000 refs    2.0  #######################################
 5 running, 12 frames each: CPU  98.8%   faults/1000 refs    2.1  ########################################
 6 running, 10 frames each: CPU  98.6%   faults/1000 refs    2.1  #######################################
 7 running,  9 frames each: CPU  98.8%   faults/1000 refs    2.1  ########################################
 8 running,  8 frames each: CPU  98.8%   faults/1000 refs    2.1  ########################################
 9 running,  7 frames each: CPU   4.0%   faults/1000 refs  126.2  ##
10 running,  6 frames each: CPU   2.0%   faults/1000 refs  248.6  #
11 running,  5 frames each: CPU   1.3%   faults/1000 refs  371.7  #
12 running,  5 frames each: CPU   1.3%   faults/1000 refs  371.5  #
13 running,  4 frames each: CPU   1.0%   faults/1000 refs  495.0  
14 running,  4 frames each: CPU   1.0%   faults/1000 refs  496.1  
15 running,  4 frames each: CPU   1.0%   faults/1000 refs  496.0  
16 running,  4 frames each: CPU   1.0%   faults/1000 refs  495.7  
```

The curve is the classic picture of thrashing. With one process the CPU is idle whenever that process waits for the disk, and 73% of the time is useful work. Adding processes hides the waits behind one another, and the CPU reaches about 99% with five to eight processes. At **nine** processes each gets only 7 frames, fewer than its working set of 8, and utilization falls off a cliff: the fault rate jumps from about 2 to about 126 per thousand references, which is what theory predicts, because with 7 frames holding a random working set of 8 pages, one reference in eight asks for the missing page. The disk now serves faults all the time, and the CPU waits for it. The model is deliberately simple (one disk, a fixed fault cost, equal shares of memory), but the shape is the real one: past the point where the working sets stop fitting, adding load makes things much worse.

The remedies follow from the cause. Add memory; make programs' working sets smaller; or run **fewer processes at once**, by suspending some and swapping out their entire working sets ([Wikipedia: Virtual memory](https://en.wikipedia.org/wiki/Virtual_memory)). This idea is called **admission control**: it is sometimes better to do less work well than to try to do everything at once badly. Some versions of Linux instead run an **out-of-memory killer** that picks a memory-hungry process and ends it when memory is oversubscribed ([OSTEP: Beyond Physical Memory: Policies](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-beyondphys-policy.pdf)).

## ✅ Checking the Code

Each piece of code was compared with an independent reference. The six simulators (FIFO, LRU, Clock, OPT, MRU, and the two-list policy) agreed with deliberately naive versions written with plain lists (Clock against the queue form of second chance) on 20,000 random reference strings. No policy ever beat OPT, and OPT equalled the minimum over every possible choice of victims, found by exhaustive search, on 3,000 short strings. On the random strings, LRU and OPT never faulted more with one frame more, while FIFO, Clock, and the two-list policy sometimes did, and LRU's memory with *N* frames was always contained in its memory with *N* + 1. With random references over 8 pages, LRU's miss ratio with *F* frames was within 0.01 of (8 − *F*)/8. For the thrashing simulator, in 20 combinations of process count, fault cost, and time slice, its fault count matched the LRU fault count of the references that each process executed (allowing one pending fault per process), its CPU time equalled the number of references executed, and with a single process the total time equalled the references plus the faults times the fault cost. The fault counts of the experiments in the other two lessons were the same in five repeated runs.

## Common Misconceptions

- **"More memory always means fewer page faults."** It does for LRU and OPT, but FIFO and Clock can fault more with more frames.
- **"LRU is optimal."** It approximates OPT well when references have locality, but on a loop one page larger than memory it faults on every reference, where OPT does not.
- **"The optimal algorithm can be used if it is implemented well."** It needs to know the future; it exists to measure the others.
- **"A thrashing system needs more processes to keep the CPU busy."** Low utilization caused by paging gets worse with every extra process.
- **"The victim is always written back to disk."** A clean page can simply be dropped, because its contents exist elsewhere; only modified pages need writing.

## ➡️ Next

This completes the Virtual Memory module and the Operating Systems section: the kernel and its modes, processes and threads, memory, scheduling, concurrency, files, and the virtual memory that ties memory and disk together. Return to the [section index](../README.md) to review the path or to revisit a module. Then continue to the [Database Management Systems section](../../database-management-systems/README.md).
