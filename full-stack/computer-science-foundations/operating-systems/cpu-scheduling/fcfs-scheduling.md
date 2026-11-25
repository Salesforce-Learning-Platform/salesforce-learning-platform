# 🚶 First-Come, First-Served (FCFS) Scheduling

## The Simplest Policy: A Queue

**First-come, first-served** (FCFS), also called **first in, first out** (FIFO), is the simplest scheduling algorithm there is: the ready processes wait in a queue in the order in which they arrived, and the CPU serves them one at a time from the front ([Wikipedia: Scheduling (computing)](https://en.wikipedia.org/wiki/Scheduling_(computing))). It is **non-preemptive**: once a process has the CPU, it keeps it until it finishes (or, in a real system, until it blocks for I/O). It is the policy of a queue at a shop counter, and for the same reasons it feels fair and has the same problem: a customer with a full trolley holds up everyone behind them who is buying a single item.

This file implements FCFS in two ways, measures how much the *order of arrival* changes the averages, and then measures the problem FCFS is known for, the **convoy effect**. It uses the toolkit introduced in [cpu-scheduling-basics.md](cpu-scheduling-basics.md), repeated here so that the file runs on its own. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon); the simulations are deterministic.

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

fcfs = lambda job, remaining, waited: (job.arrival,)        # the key: whoever arrived first runs first
```

## 🧮 Two Implementations, One Policy

With the toolkit, FCFS is a one-line key. The textbook picture is even simpler, an actual queue of jobs, served from the front, and the two must always produce the same timeline. The block below writes the queue version and checks the two against each other on 1,000 random workloads (random arrivals, bursts of 1 to 20 ticks, and ties that are resolved by the order in the list):

```python
import random
from collections import deque

def fcfs_with_a_queue(jobs):
    """The textbook picture: jobs join a FIFO queue when they arrive, and the CPU serves them one after another."""
    queue = deque(sorted(jobs, key=lambda job: job.arrival))        # sorting is stable: ties keep the order of the list
    timeline, now = [], 0
    while queue:
        job = queue.popleft()
        timeline += [None] * max(0, job.arrival - now)              # the CPU idles until the next job arrives
        now = max(now, job.arrival)
        timeline += [job.name] * job.burst
        now += job.burst
    return timeline

rng = random.Random(1)
for _ in range(1000):
    jobs = [Job(f"J{i}", rng.randint(0, 30), rng.randint(1, 20)) for i in range(rng.randint(1, 8))]
    assert fcfs_with_a_queue(jobs) == schedule(jobs, fcfs)
print("the queue and the key-based engine agree on 1,000 random workloads")
```

```text
the queue and the key-based engine agree on 1,000 random workloads
```

## 🔀 The Order of Arrival Is Everything

FCFS has no say in the order: the arrival order decides, and the averages depend heavily on it. The classic illustration has three jobs that all arrive at time 0, one long job (24 ticks) and two short ones (3 ticks each). First, the long job happens to be first in line:

```python
jobs = [Job("P1", 0, 24), Job("P2", 0, 3), Job("P3", 0, 3)]
long_first = report(jobs, schedule(jobs, fcfs))
```

```text
 job arrival burst finish turnaround waiting response
  P1       0    24     24         24       0        0
  P2       0     3     27         27      24       24
  P3       0     3     30         30      27       27
                 average      27.00   17.00    17.00
CPU busy 30 of 30 ticks (100%) | throughput 0.100 jobs per tick | switches between jobs: 2
order: P1 0-24 | P2 24-27 | P3 27-30
```

Now the same three jobs, with the long one at the back of the queue:

```python
jobs = [Job("P2", 0, 3), Job("P3", 0, 3), Job("P1", 0, 24)]
long_last = report(jobs, schedule(jobs, fcfs))
print(f"average waiting time: {long_first['waiting']:.2f} with the long job first, {long_last['waiting']:.2f} with the long job last")
```

```text
 job arrival burst finish turnaround waiting response
  P2       0     3      3          3       0        0
  P3       0     3      6          6       3        3
  P1       0    24     30         30       6        6
                 average      13.00    3.00     3.00
CPU busy 30 of 30 ticks (100%) | throughput 0.100 jobs per tick | switches between jobs: 2
order: P2 0-3 | P3 3-6 | P1 6-30
average waiting time: 17.00 with the long job first, 3.00 with the long job last
```

The jobs, their lengths, and the policy are identical; only the arrival order changed, and the average waiting time fell from 17 ticks to 3, and the average turnaround from 27 to 13. The total work is the same (30 ticks), so the last job finishes at tick 30 either way; what changed is how long the *short* jobs waited. Everything FCFS does well or badly follows from this.

## 🚛 The Convoy Effect

The same effect on a larger scale is called the **convoy effect**: a number of short processes queue up behind one long one, like cars stuck behind a slow lorry on a single-lane road, and the turnaround, waiting, and response times of all of them are high ([Wikipedia: Scheduling (computing)](https://en.wikipedia.org/wiki/Scheduling_(computing))). The experiment below isolates it. A long job arrives first, followed by five short jobs of 2 ticks each, arriving one tick apart; the long job's length is varied from 5 ticks to 400:

```python
print(f"{'long job (ticks)':>16} | {'avg wait of the 5 short jobs':>28} | {'avg wait of all 6 jobs':>22}")
for long_burst in (5, 20, 50, 100, 400):
    jobs = [Job("long", 0, long_burst)] + [Job(f"s{i}", i, 2) for i in range(1, 6)]
    result = metrics(jobs, schedule(jobs, fcfs))
    short = [result[f"s{i}"]["waiting"] for i in range(1, 6)]
    everyone = [row["waiting"] for row in result.values()]
    print(f"{long_burst:>16} | {sum(short) / 5:>28.1f} | {sum(everyone) / 6:>22.1f}")
```

```text
long job (ticks) | avg wait of the 5 short jobs | avg wait of all 6 jobs
               5 |                          6.0 |                    5.0
              20 |                         21.0 |                   17.5
              50 |                         51.0 |                   42.5
             100 |                        101.0 |                   84.2
             400 |                        401.0 |                  334.2
```

Each short job needs only 2 ticks of CPU, yet its average wait is the long job's length plus one: the shorts wait for the long job and then for each other, so the cost of the long job is paid five times over. When the long job is 400 ticks, a 2-tick job waits about 400. In a real system the effect is worse than this CPU-only picture suggests, because of the way processes alternate between computing and I/O. A CPU-bound process holds the CPU for a long burst while the I/O-bound processes wait behind it, so the disks and network sit idle; each I/O-bound process then gets the CPU only for the instant it needs to start its next I/O operation, and queues up behind the CPU-bound process again. The result is low utilization of the I/O devices as well as slow responses, which is why the convoy effect is the standard objection to FCFS.

## ✅ What FCFS Does Well

- **It is trivial to implement and cheap to run.** A queue needs no search and no measurement of the jobs: adding and removing at the ends take constant time.
- **It never starves a job.** A job's waiting time is bounded by the work of the jobs ahead of it, so every job runs eventually. (The bound was checked on random workloads: a job never waited longer than the combined bursts of the jobs that arrived before it.)
- **It is fair in the simplest sense.** Jobs are served in the order they asked.
- **It switches as rarely as possible.** A job that never leaves the CPU until it is done causes no preemption, and so no switching overhead beyond one switch per job.

## ⚠️ What It Does Badly

- **The averages depend on luck.** As the three-job example showed, the arrival order alone can multiply the average wait.
- **It is poor for interactive use.** A short interactive job may wait behind a long computation, so response times are high and unpredictable.
- **It cannot meet deadlines.** Nothing in the policy notices that one job is more urgent than another; the lack of prioritization makes it hard to meet deadlines.

## 🏭 FCFS in Real Systems

FCFS is rarely the whole scheduler of a general-purpose system, but it is a building block in several. In Linux, the real-time policy `SCHED_FIFO` is a simple algorithm that does no time slicing: a thread runs until it blocks, yields, or is preempted by a higher-priority thread, and threads with the same priority wait in a first-in, first-out list ([Linux man page: `sched(7)`](https://man7.org/linux/man-pages/man7/sched.7.html)). FIFO queues also order work in many places that are not CPU scheduling at all: a pool of worker threads takes tasks from a FIFO queue ([Wikipedia: Scheduling (computing)](https://en.wikipedia.org/wiki/Scheduling_(computing))), and printers and network devices commonly serve requests in the order they arrive. Policies that do better on average waiting time must know or guess how long jobs will run, which is the idea behind [shortest-job-first.md](shortest-job-first.md).

## Common Misconceptions

- **"FCFS is the fairest policy because it is first come, first served."** It treats the order of arrival equally, but a short job that arrives just behind a long one is treated much worse than one that arrives just ahead of it. Fair in order does not mean fair in outcome.
- **"FCFS gives the same average waiting time whatever the order."** The experiment above showed 17 ticks against 3 for the same jobs; the order of arrival changes the average.
- **"FCFS wastes the CPU."** Not at all: the CPU is busy whenever any job is ready. What it wastes is the *waiting time of short jobs*, and (in a real system with I/O) the time the I/O devices are idle.
- **"A convoy needs many long jobs."** One long job in front of many short ones is enough.

## ➡️ Next

Continue to [shortest-job-first.md](shortest-job-first.md): if the scheduler knew how long each job would run, it could put the short ones first and shrink the waiting times, and that idea can be proved optimal, at the price of one serious practical problem.
