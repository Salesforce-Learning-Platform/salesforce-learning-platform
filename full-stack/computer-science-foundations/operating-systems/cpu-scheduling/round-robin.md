# 🔄 Round Robin Scheduling

## Everyone Gets a Turn

The policies so far either rely on the order of arrival (first come, first served) or on knowing the future (shortest job first). **Round robin** needs neither. It is the policy of a game in which the players take turns around a table: every ready process receives a slice of CPU time, called a **time quantum**, in equal portions and in circular order, with no process favoured over another ([Wikipedia: Round-robin scheduling](https://en.wikipedia.org/wiki/Round-robin_scheduling)). The scheduler keeps the ready processes in a queue. It takes the one at the front, lets it run for at most one quantum, and if the process has not finished by then, interrupts it and puts it at the back of the queue. If the process finishes or has to wait for I/O before its quantum is used up, the scheduler simply moves on to the next process in the queue at once (the same article).

Round robin is therefore **preemptive**, and it depends on the hardware timer interrupt described in [context-switching.md](../processes-and-threads/context-switching.md): the timer fires when the quantum ends, and the kernel gets control back even from a program that never gives it up. It is simple, easy to implement, and starvation-free (the same article). This file implements it, shows how it changes the averages compared with FCFS, and measures the central design question, **how long should the quantum be?** It uses the toolkit introduced in [cpu-scheduling-basics.md](cpu-scheduling-basics.md), repeated here so that the file runs on its own. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon); the simulations are deterministic.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Job:
    name: str
    arrival: int
    burst: int                                      # the CPU time the job needs, in ticks
    priority: int = 0                               # a smaller number means more urgent

def runs(timeline):
    """Merge a per-tick timeline (a job name for each tick, None when the CPU is idle) into (name, start, end) runs."""
    merged = []
    for tick, name in enumerate(timeline):
        if merged and merged[-1][0] == name:
            merged[-1][2] = tick + 1
        else:
            merged.append([name, tick, tick + 1])
    return merged

def gantt(timeline):
    label = lambda name: "idle" if name is None else "switch" if name == "~" else name      # "~" marks time lost switching
    return " | ".join(f"{label(name)} {start}-{end}" for name, start, end in runs(timeline))

def switches(timeline):
    """How many times the CPU went from one job to a different one, without going idle in between."""
    count, last = 0, None
    for name in timeline:
        if name is None:
            last = None                             # the CPU went idle: the next job starts afresh
        elif name != "~":
            count += last is not None and name != last
            last = name
    return count

def metrics(jobs, timeline):
    """Per job: finish time, turnaround (finish - arrival), waiting (turnaround - burst), response (first run - arrival)."""
    result = {}
    for job in jobs:
        ticks = [tick for tick, name in enumerate(timeline) if name == job.name]
        assert len(ticks) == job.burst, f"{job.name} ran {len(ticks)} ticks but needs {job.burst}"
        assert ticks[0] >= job.arrival, f"{job.name} ran before it arrived"
        finish = ticks[-1] + 1
        result[job.name] = dict(finish=finish, turnaround=finish - job.arrival, waiting=finish - job.arrival - job.burst, response=ticks[0] - job.arrival)
    return result

def report(jobs, timeline):
    result = metrics(jobs, timeline)
    print(f"{'job':>4} {'arrival':>7} {'burst':>5} {'finish':>6} {'turnaround':>10} {'waiting':>7} {'response':>8}")
    for job in jobs:
        m = result[job.name]
        print(f"{job.name:>4} {job.arrival:>7} {job.burst:>5} {m['finish']:>6} {m['turnaround']:>10} {m['waiting']:>7} {m['response']:>8}")
    average = {field: sum(m[field] for m in result.values()) / len(jobs) for field in ("turnaround", "waiting", "response")}
    print(f"{'average':>24} {average['turnaround']:>10.2f} {average['waiting']:>7.2f} {average['response']:>8.2f}")
    busy = sum(1 for name in timeline if name and name != "~")
    print(f"CPU busy {busy} of {len(timeline)} ticks ({busy / len(timeline):.0%}) | throughput {len(jobs) / len(timeline):.3f} jobs per tick | switches between jobs: {switches(timeline)}")
    print("order:", gantt(timeline))
    return average

def schedule(jobs, key, preemptive=False):
    """Run one CPU tick by tick. Among the ready jobs, the one with the smallest key(job, remaining, waited) runs.
    A non-preemptive policy keeps its choice until the job finishes; a preemptive one chooses again at every tick."""
    remaining = {job.name: job.burst for job in jobs}
    timeline, current, now = [], None, 0
    while any(remaining.values()):
        ready = [job for job in jobs if job.arrival <= now and remaining[job.name] > 0]
        if not ready:
            timeline.append(None)                   # nothing has arrived yet: the CPU idles
            now += 1
            continue
        if preemptive or current is None or remaining[current.name] == 0:
            current = min(ready, key=lambda job: key(job, remaining[job.name], now - job.arrival - (job.burst - remaining[job.name])))
        timeline.append(current.name)
        remaining[current.name] -= 1
        now += 1
    return timeline

fcfs = lambda job, remaining, waited: (job.arrival,)             # earliest arrival first (used for comparison)
```

## 🧮 The Simulator

Round robin does not fit the "smallest key wins" engine of the toolkit, because the answer depends on the order of a queue, so it gets its own function. Two conventions need a decision. First, a job that arrives *during* another job's turn (or exactly when the turn ends) joins the ready queue before the interrupted job goes to the back. Second, switching from one job to a different one can cost time: `switch_cost` ticks, shown as `~` in the timeline, during which no job runs (switching to the *same* job again, when it is the only one left, costs nothing):

```python
from collections import deque

def round_robin(jobs, quantum, switch_cost=0):
    """Give each ready job a turn of at most `quantum` ticks, in rotation. Ticks lost to switching are marked "~"."""
    remaining = {job.name: job.burst for job in jobs}
    not_arrived = sorted(jobs, key=lambda job: job.arrival)          # sorting is stable: ties keep the order of the list
    ready, timeline, now, previous = deque(), [], 0, None

    def admit():                                                     # move every job that has arrived into the ready queue
        while not_arrived and not_arrived[0].arrival <= now:
            ready.append(not_arrived.pop(0).name)

    admit()
    while ready or not_arrived:
        if not ready:                                                # nothing to run: idle until the next arrival
            timeline.append(None)
            previous = None                                          # after idling, no switch from a job is needed
            now += 1
            admit()
            continue
        name = ready.popleft()
        if switch_cost and previous not in (None, name):             # the dispatcher needs time to switch to a different job
            timeline += ["~"] * switch_cost
            now += switch_cost
            admit()
        for _ in range(min(quantum, remaining[name])):
            timeline.append(name)
            remaining[name] -= 1
            now += 1
            admit()                                                  # jobs arriving during the turn queue up first ...
        if remaining[name]:
            ready.append(name)                                       # ... and the preempted job goes behind them
        previous = name
    return timeline
```

## 🏁 A First Example

Take the classic three jobs again: a 24-tick job and two 3-tick jobs, all arriving at time 0, and a quantum of 4 ticks. Under FCFS the two short jobs waited 24 and 27 ticks. Under round robin the long job is interrupted after 4 ticks, and the short ones each get a turn:

```python
jobs = [Job("P1", 0, 24), Job("P2", 0, 3), Job("P3", 0, 3)]
report(jobs, round_robin(jobs, quantum=4))
```

```text
 job arrival burst finish turnaround waiting response
  P1       0    24     30         30       6        0
  P2       0     3      7          7       4        4
  P3       0     3     10         10       7        7
                 average      15.67    5.67     3.67
CPU busy 30 of 30 ticks (100%) | throughput 0.100 jobs per tick | switches between jobs: 3
order: P1 0-4 | P2 4-7 | P3 7-10 | P1 10-30
```

The average waiting time dropped from 17 ticks under FCFS to 5.67, and the average response time from 17 to 3.67: P2 and P3 finish at ticks 7 and 10 instead of 27 and 30. The long job is the one that pays: it finishes at tick 30 as before, but it has had to wait for the others, 6 ticks in total. (In the Gantt chart, its last run, `P1 10-30`, is a single line because after the others finish, P1 is alone in the queue and keeps getting its turn again; no switching is needed.)

The same policy with a quantum of 1 tick gives the picture that makes round robin easy to remember. Three identical jobs of 4 ticks each take turns, one tick at a time:

```python
jobs = [Job("A", 0, 4), Job("B", 0, 4), Job("C", 0, 4)]
print("".join(name or "." for name in round_robin(jobs, quantum=1)))
```

```text
ABCABCABCABC
```

## ⚖️ How Long Should a Quantum Be?

The quantum is the one tunable setting of round robin, and both extremes are bad:

- If the quantum is **very long** (longer than any job), no job is ever interrupted, and round robin turns into FCFS, with its long waits for short jobs.
- If the quantum is **very short**, every job gets its turn almost at once, which is wonderful for response time, but the system spends more and more of its time switching and less on useful work.

The experiment below measures both effects on five jobs that all arrive at time 0 (bursts of 10, 4, 2, 7, and 12 ticks, 35 ticks of work in total). For each quantum it shows the three averages and the number of switches when switching is free, then repeats the run with a switch cost of 1 tick to show how much of the elapsed time goes on useful work. The last row has a quantum of 100, longer than any job, which makes it identical to FCFS (the code checks that):

```python
jobs = [Job("P1", 0, 10), Job("P2", 0, 4), Job("P3", 0, 2), Job("P4", 0, 7), Job("P5", 0, 12)]
total_work = sum(job.burst for job in jobs)
print(f"{'quantum':>7} | {'avg response':>12} | {'avg waiting':>11} | {'avg turnaround':>14} | {'switches':>8} | {'time taken (cost 1)':>19} | {'useful work':>11}")
for quantum in (1, 2, 3, 4, 6, 8, 12, 100):
    timeline = round_robin(jobs, quantum)
    result = metrics(jobs, timeline)
    mean = lambda field: sum(row[field] for row in result.values()) / len(result)
    with_cost = round_robin(jobs, quantum, switch_cost=1)
    print(f"{quantum:>7} | {mean('response'):>12.2f} | {mean('waiting'):>11.2f} | {mean('turnaround'):>14.2f} | {switches(timeline):>8} | {len(with_cost):>19} | {total_work / len(with_cost):>11.0%}")
assert round_robin(jobs, 100) == schedule(jobs, fcfs)
```

```text
quantum | avg response | avg waiting | avg turnaround | switches | time taken (cost 1) | useful work
      1 |         2.00 |       16.40 |          23.40 |       32 |                  67 |         52%
      2 |         4.00 |       15.60 |          22.60 |       16 |                  51 |         69%
      3 |         5.60 |       17.20 |          24.20 |       13 |                  48 |         73%
      4 |         7.20 |       14.80 |          21.80 |        9 |                  44 |         80%
      6 |         9.20 |       15.80 |          22.80 |        7 |                  42 |         83%
      8 |        11.00 |       15.60 |          22.60 |        6 |                  41 |         85%
     12 |        12.60 |       12.60 |          19.60 |        4 |                  39 |         90%
    100 |        12.60 |       12.60 |          19.60 |        4 |                  39 |         90%
```

Four lessons can be read from the table:

1. **Response time grows steadily with the quantum**, from 2 ticks (quantum 1) to 12.6 (FCFS). This is the whole point of round robin: every job is served promptly, whatever the length of the jobs ahead of it.
2. **Waiting and turnaround time do not improve; they get worse than FCFS** for this workload (between 21.8 and 24.2 ticks of turnaround for quanta from 1 to 8, against 19.6 for FCFS), and they do not change smoothly with the quantum, because the question is which jobs happen to finish within their turn. Round robin buys fairness and response time and pays with longer total completion times for the long jobs.
3. **Switching is not free.** With a cost of one tick per switch, a quantum of 1 spends nearly half its time switching (52% useful work); at a quantum of 12 or more, 90% of the time is useful. This is the trade-off of [context-switching.md](../processes-and-threads/context-switching.md) seen from the scheduler's side: a quantum much longer than the cost of a switch makes the overhead small.
4. **The quantum should be chosen between the two extremes**: long enough that switching is a small fraction of each turn, short enough that a short job or an interactive user never waits long. How long is "long enough" depends on the real cost of a switch on the machine, which is why kernels tune it.

On this Mac, when two CPU-bound processes per core were competing (the experiment in [context-switching.md](../processes-and-threads/context-switching.md)), the kernel interrupted a running process between about 500 and 850 times a second, which means a slice of roughly one to two milliseconds: the scale of numbers real quanta have, though a modern scheduler decides it dynamically.

## 🔒 What Round Robin Guarantees

With *n* jobs in the ready queue and a quantum *q*, a job waits at most (*n* − 1) × *q* ticks (plus any switching time) between one turn and the next, so it can never starve, and the first response of a job that arrived with *n* − 1 others ahead of it is bounded by the same figure. As the quantum shrinks towards zero, round robin approaches **processor sharing**, the ideal in which *n* ready jobs each progress at 1/*n* of the CPU's speed. That ideal is exactly what Linux's default scheduler models: the kernel documentation says that about 80% of the design of CFS can be summed up as modelling an "ideal, precise multi-tasking CPU" on real hardware, one in which each of *n* tasks runs at 1/*n* of the speed ([Linux kernel documentation: CFS Scheduler](https://docs.kernel.org/scheduler/sched-design-CFS.html)), and adds that CFS is now making room for a successor, EEVDF, which has its own page in the same documentation. Real kernels therefore refine round robin more than they replace it.

## 🏭 Round Robin in Real Systems

Linux offers round robin explicitly as a real-time policy, `SCHED_RR`, described in its manual page as a simple enhancement of the first-in-first-out policy in which each thread may run only for a maximum time quantum; when the quantum is used up, the thread goes to the end of the list for its priority ([Linux man page: `sched(7)`](https://man7.org/linux/man-pages/man7/sched.7.html)). General-purpose schedulers use the same idea in a more flexible form: instead of a fixed slice, they compute how long each task should run so that every runnable task gets its fair share. Within a *single priority level*, a round-robin rotation is also the usual way to treat equal jobs equally, which is how it combines with the priority scheduling of [priority-scheduling.md](priority-scheduling.md).

## ✅ Checking the Implementation

The simulator was tested on 3,000 random workloads (random arrivals, bursts, quanta from 1 to 8, and switch costs of 0, 1, and 2). In every one, every job ran exactly its burst, none ran before it arrived, and the CPU was never idle (or switching) while a job was waiting; no job ran for more than one quantum at a stretch unless it was the only job left, and a job never waited more than (*n* − 1) × *q* ticks, plus *n* switches, between its turns; switching ticks occurred only between two different jobs; and with a quantum at least as long as the longest job, the timeline was identical to FCFS.

## Common Misconceptions

- **"Round robin is fair, so everyone is better off than under FCFS."** Everyone gets *service* promptly, but the completion time of the long jobs gets worse, and the average turnaround can be higher than FCFS, as the table shows.
- **"A shorter quantum is always better because it responds faster."** Response improves, but the time lost to switching grows; with a switch cost of 1 tick, a quantum of 1 wasted nearly half the CPU.
- **"The quantum is the same as the time between context switches."** A job that blocks or finishes early causes a switch before its quantum ends, so switches can be more frequent than quanta.
- **"Round robin ignores priorities, so it cannot be used in a real system."** It is used inside priority levels, and as the explicit `SCHED_RR` real-time policy.

## ➡️ Next

Continue to [priority-scheduling.md](priority-scheduling.md): what to do when some jobs matter more than others, and the new problem that creates, jobs that never get to run.
