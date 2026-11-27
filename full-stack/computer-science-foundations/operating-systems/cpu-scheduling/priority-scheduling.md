# 🏅 Priority Scheduling

## Not All Jobs Are Equal

So far every job counted the same. Real systems know better: a mouse click should be handled before a nightly backup, an audio buffer before a disk indexer, and the process that keeps a robot's motors turning before everything else. **Priority scheduling** gives each job a number, its **priority**, and always runs the ready job with the most urgent one; jobs with equal priority are served first come, first served (or in round robin). A scheduler that assigns each task a fixed priority and serves higher priorities first is called a fixed-priority scheduler ([Wikipedia: Aging (scheduling)](https://en.wikipedia.org/wiki/Aging_(scheduling))). Like the other policies it comes in a **non-preemptive** form, which only chooses when the CPU becomes free, and a **preemptive** form, in which a newly ready job with a higher priority takes the CPU from the running one at once.

Numbers need a convention, and conventions differ. This module's simulator treats a **smaller number as more urgent**, as many textbooks do. Linux's real-time policies run the other way: their priorities go from 1 (low) to 99 (high), and every real-time thread outranks every ordinary one, while the *nice* values of ordinary threads go from −20 (most favoured) to +19 (least) ([Linux man page: `sched(7)`](https://man7.org/linux/man-pages/man7/sched.7.html)). Whenever you meet a priority number, check which end is urgent.

This file works through priority scheduling with the toolkit introduced in [cpu-scheduling-basics.md](cpu-scheduling-basics.md), repeated here so that the file runs on its own. It then meets the policy's famous problem, starvation, its standard cure, aging, and finishes with the design that real systems build on, the multilevel feedback queue. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon); the simulations are deterministic.

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

fcfs = lambda job, remaining, waited: (job.arrival,)
srtf = lambda job, remaining, waited: (remaining, job.arrival)
by_priority = lambda job, remaining, waited: (job.priority, job.arrival)     # most urgent first; ties go to the earlier arrival

def summary(label, jobs, timeline):
    result = metrics(jobs, timeline)
    mean = lambda field: sum(row[field] for row in result.values()) / len(result)
    print(f"{label:<28} {mean('turnaround'):>10.2f} {mean('waiting'):>8.2f} {mean('response'):>9.2f} {switches(timeline):>9}")

HEADER = f"{'policy':<28} {'turnaround':>10} {'waiting':>8} {'response':>9} {'switches':>9}"
```

## 🔢 Priorities in Action

Five jobs arrive together, with priorities that have nothing to do with their lengths. Job P2 is the most urgent (priority 1) and P4 the least (priority 5):

```python
jobs = [Job("P1", 0, 10, 3), Job("P2", 0, 1, 1), Job("P3", 0, 2, 4), Job("P4", 0, 1, 5), Job("P5", 0, 5, 2)]
report(jobs, schedule(jobs, by_priority))
```

```text
 job arrival burst finish turnaround waiting response
  P1       0    10     16         16       6        6
  P2       0     1      1          1       0        0
  P3       0     2     18         18      16       16
  P4       0     1     19         19      18       18
  P5       0     5      6          6       1        1
                 average      12.00    8.20     8.20
CPU busy 19 of 19 ticks (100%) | throughput 0.263 jobs per tick | switches between jobs: 4
order: P2 0-1 | P5 1-6 | P1 6-16 | P3 16-18 | P4 18-19
```

The jobs run strictly in priority order (P2, P5, P1, P3, P4), however long they are, and the least urgent jobs wait longest: P4 needs one tick and waits 18. Priority scheduling optimizes *importance*, not any of the averages.

Preemption matters when jobs arrive over time. In the next scenario, P2 and P3 arrive while the lower-priority P1 is running. Without preemption, P1 keeps the CPU; with it, the more urgent arrivals take over at once:

```python
jobs = [Job("P1", 0, 8, 3), Job("P2", 1, 4, 1), Job("P3", 2, 6, 2), Job("P4", 3, 2, 4)]
print(HEADER)
summary("priority, non-preemptive", jobs, schedule(jobs, by_priority, preemptive=False))
summary("priority, preemptive", jobs, schedule(jobs, by_priority, preemptive=True))
print()
report(jobs, schedule(jobs, by_priority, preemptive=True))
```

```text
policy                       turnaround  waiting  response  switches
priority, non-preemptive          13.00     8.00      8.00         3
priority, preemptive              12.00     7.00      4.50         4

 job arrival burst finish turnaround waiting response
  P1       0     8     18         18      10        0
  P2       1     4      5          4       0        0
  P3       2     6     11          9       3        3
  P4       3     2     20         17      15       15
                 average      12.00    7.00     4.50
CPU busy 20 of 20 ticks (100%) | throughput 0.200 jobs per tick | switches between jobs: 4
order: P1 0-1 | P2 1-5 | P3 5-11 | P1 11-18 | P4 18-20
```

With preemption, the most urgent job, P2, starts the moment it arrives (response time 0) and finishes at tick 5, instead of waiting until tick 12; P1 is interrupted after one tick and resumes later. The average response time falls from 8 ticks to 4.5. The cost is the extra switch, and, for P4, which is the least urgent job, a long wait until everyone else is done.

## 🥶 Starvation, and the Cure Called Aging

Priority scheduling inherits a flaw from shortest job first: a steady stream of urgent jobs can keep a low-priority job from ever reaching the CPU, indefinitely blocking it. That is **starvation**. The standard cure is **aging**: gradually raise the priority of a task according to how long it has waited in the ready queue, so that waiting itself eventually makes it urgent enough ([Wikipedia: Aging (scheduling)](https://en.wikipedia.org/wiki/Aging_(scheduling))).

The experiment below uses the same kind of stream as in [shortest-job-first.md](shortest-job-first.md): one low-priority job (priority 9, 5 ticks) arrives early, and then a new high-priority 2-tick job (priority 1) arrives every 2 ticks for 60 ticks, so that an urgent job is always ready. The first row uses static priorities. The other two let a job's effective priority improve by 1 for every 5 (or every 2) ticks it has waited:

```python
def aging(interval):
    """A key function in which every `interval` ticks of waiting make a job one step more urgent."""
    return lambda job, remaining, waited: (job.priority - waited // interval, job.arrival)

stream = [Job("hi0", 0, 2, 1), Job("low", 1, 5, 9)] + [Job(f"hi{i}", 2 * i, 2, 1) for i in range(1, 31)]
print(f"{'policy':<26} {'low job starts':>14} {'low job ends':>12} {'avg wait of the urgent jobs':>27}")
for label, key in (("static priorities", by_priority), ("aging: +1 every 5 ticks", aging(5)), ("aging: +1 every 2 ticks", aging(2))):
    timeline = schedule(stream, key)
    result = metrics(stream, timeline)
    urgent = [result[job.name]["waiting"] for job in stream if job.name != "low"]
    print(f"{label:<26} {result['low']['response'] + 1:>14} {result['low']['finish']:>12} {sum(urgent) / len(urgent):>27.2f}")
```

```text
policy                     low job starts low job ends avg wait of the urgent jobs
static priorities                      62           67                        0.00
aging: +1 every 5 ticks                42           47                        1.61
aging: +1 every 2 ticks                18           23                        3.55
```

With static priorities, the low-priority job does not run until time 62, when the stream of urgent jobs finally ends, although it arrived at time 1; the urgent jobs never wait. Aging bounds the injustice: with a step every 5 ticks the low job starts at time 42, and with a step every 2 ticks at time 18. The price is paid by the urgent jobs, whose average wait rises from 0 to 1.6 and then 3.6 ticks, because once the old job has aged enough it outranks newcomers. How fast priorities age is a policy choice between promptness for the urgent and fairness to the patient.

Real kernels build aging in. The manual page of Linux's default policy, `SCHED_OTHER`, describes a dynamic priority based on the nice value that is *increased for each time quantum the thread is ready to run but denied the CPU*, which is meant to ensure fair progress among all such threads ([Linux man page: `sched(7)`](https://man7.org/linux/man-pages/man7/sched.7.html)).

## 🔃 Priority Inversion

Priorities interact with locks in a way that can turn them upside down. Suppose a low-priority task L holds a lock that a high-priority task H needs, so H must wait for L. If a medium-priority task M becomes ready, it preempts L (it has no need of the lock), L cannot release the lock, and H, the most urgent task of all, is held up indirectly by a task of lower priority: the priorities are *inverted*. The best-known case is the 1997 Mars Pathfinder lander, whose real-time system suffered from exactly this problem ([Wikipedia: Priority inversion](https://en.wikipedia.org/wiki/Priority_inversion)). The remedy, giving the lock holder a temporary boost, belongs to the study of locks and synchronization, and is covered in [mutex-and-semaphores.md](../deadlocks-and-concurrency/mutex-and-semaphores.md) of the [Deadlocks and Concurrency](../deadlocks-and-concurrency/README.md) module.

## 🪜 Priorities That Adjust Themselves: Multilevel Feedback Queues

A fixed priority has to be chosen by someone who knows what the job will do. The **multilevel feedback queue** (MLFQ), first developed by Fernando Corbató in 1962, lets the system *learn* it instead. It keeps several FIFO queues, one per priority level, with longer time quanta at the lower levels. A new job joins the top queue, on the assumption that it will be short; the scheduler always serves the highest non-empty queue; a job that uses up its whole quantum is judged to be long-running and is moved down one level; a job that gives up the CPU early (because it waits for I/O) stays where it is or is promoted. Long jobs therefore sink to the bottom by themselves, short and interactive jobs stay near the top, and a job waiting too long at a low level can be aged upwards ([Wikipedia: Multilevel feedback queue](https://en.wikipedia.org/wiki/Multilevel_feedback_queue)).

The simulator below uses three levels with quanta of 2, 4, and 8 ticks. A job that arrives at a higher level than the one running takes over at once, and a preempted job goes to the back of its own queue. (This model has only CPU bursts, with no I/O, so the rule about staying at a level when a job waits is not exercised.) It runs a long job, a medium job, and three short ones against FCFS, and against shortest remaining time first, which is the ideal that needs to know each job's length in advance:

```python
from collections import deque

def mlfq(jobs, quanta=(2, 4, 8)):
    """Multilevel feedback queue: new jobs start at level 0; using a whole quantum moves a job one level down."""
    remaining = {job.name: job.burst for job in jobs}
    not_arrived = sorted(jobs, key=lambda job: job.arrival)
    queues = [deque() for _ in quanta]
    timeline, now, running = [], 0, None                      # running = (name, level, ticks used in this turn)

    def admit():
        while not_arrived and not_arrived[0].arrival <= now:
            queues[0].append(not_arrived.pop(0).name)         # every new job starts at the top level

    admit()
    while any(remaining.values()):
        top = next((level for level, queue in enumerate(queues) if queue), None)
        if running and top is not None and top < running[1]:  # a more urgent level has a job: preempt
            queues[running[1]].append(running[0])
            running = None
        if running is None:
            if top is None:                                   # nothing is ready: the CPU idles
                timeline.append(None)
                now += 1
                admit()
                continue
            running = (queues[top].popleft(), top, 0)
        name, level, used = running
        timeline.append(name)
        remaining[name] -= 1
        used += 1
        now += 1
        admit()
        if remaining[name] == 0:
            running = None                                    # finished
        elif used == quanta[level]:                           # used its whole quantum: demote it
            queues[min(level + 1, len(quanta) - 1)].append(name)
            running = None
        else:
            running = (name, level, used)
    return timeline

workload = [Job("long", 0, 30), Job("medium", 3, 12), Job("s1", 5, 3), Job("s2", 9, 2), Job("s3", 14, 4)]
shorts = ("s1", "s2", "s3")
print(f"{'policy':<26} {'avg response':>12} {'avg turnaround':>14} {'shorts: avg turnaround':>22} {'long job ends':>13}")
for label, timeline in (("first come, first served", schedule(workload, fcfs)),
                        ("shortest remaining time", schedule(workload, srtf, preemptive=True)),
                        ("multilevel feedback queue", mlfq(workload))):
    result = metrics(workload, timeline)
    mean = lambda field, names: sum(result[name][field] for name in names) / len(names)
    everyone = [job.name for job in workload]
    print(f"{label:<26} {mean('response', everyone):>12.2f} {mean('turnaround', everyone):>14.2f} {mean('turnaround', shorts):>22.2f} {result['long']['finish']:>13}")
print()
print("MLFQ order:", gantt(mlfq(workload)))
```

```text
policy                     avg response avg turnaround shorts: avg turnaround long job ends
first come, first served          26.60          36.80                  38.33            30
shortest remaining time            0.00          16.20                   3.00            51
multilevel feedback queue          0.00          22.60                   9.00            51

MLFQ order: long 0-3 | medium 3-5 | s1 5-7 | long 7-9 | s2 9-11 | medium 11-14 | s3 14-16 | s1 16-17 | long 17-21 | medium 21-25 | s3 25-27 | long 27-35 | medium 35-38 | long 38-51
```

The multilevel feedback queue, which was told nothing about the job lengths, behaves almost like the ideal shortest-remaining-time scheduler: every new job gets the CPU immediately (response time 0), and the three short jobs finish in 9 ticks on average against 3 for the ideal and 38 for FCFS. It pays for this the way SRTF does, by pushing the long job to the end (it finishes at tick 51 instead of 30). The Gantt chart shows how: `long` runs first, but each new arrival lands at a higher level and takes over, while the long job, which keeps using its whole quantum, sinks to the lower levels where it only runs when nothing more urgent is ready. This is why Wikipedia notes that a multilevel feedback queue can approximate shortest job next without needing to know each job's total run time in advance ([Wikipedia: Shortest job next](https://en.wikipedia.org/wiki/Shortest_job_next)). Practical designs add rules to this skeleton: a periodic boost of every job back to the top to prevent starvation, and counting the total CPU time a job has used at a level, so that a program cannot stay at the top by giving up the CPU just before its quantum ends.

## 🖥️ Priorities in Real Systems

Real operating systems layer policies on top of these ideas. Linux, for example, has several: ordinary threads run under `SCHED_OTHER`, whose scheduling is influenced by the nice value, while real-time threads run under `SCHED_FIFO` or `SCHED_RR` (the policy of [round-robin.md](round-robin.md)) at priorities that always outrank ordinary ones, and a deadline policy `SCHED_DEADLINE` exists as well ([Linux man page: `sched(7)`](https://man7.org/linux/man-pages/man7/sched.7.html)). The same manual page explains that the nice value is a hint that the scheduler may interpret as it likes: how strongly it affects the relative scheduling of ordinary processes varies across UNIX systems and across Linux versions. Since Linux 2.6.23 each unit of difference between two nice values changes by a factor of 1.25 how much the scheduler favours one process over the other, so that a process at +19 receives very little CPU when anything else wants it (the same page); the kernel documentation puts the share of a nice +19 task at about 1.5% ([Linux kernel documentation: Nice levels](https://docs.kernel.org/scheduler/sched-nice-design.html)).

You can ask your own machine what a priority is worth. The experiment starts as many busy processes as there are logical CPUs at normal priority and the same number at a lowered priority, so that every core has a rival, lets them all compute for two seconds, and measures the CPU time each group received. The first comparison lowers priority with a nice value of 19. The second, which only runs where the macOS command `taskpolicy` exists, uses the lowest priority class macOS offers, the one `taskpolicy -b` selects by calling `setpriority(2)` with `PRIO_DARWIN_BG` ([taskpolicy(8)](https://keith.github.io/xcode-man-pages/taskpolicy.8.html)):

```python
import os
import resource
import shutil
import subprocess
import sys

WORKER = """
import os, resource, sys, time
os.nice(int(sys.argv[1]))                       # lower this process's priority by that many nice steps
stop = time.time() + float(sys.argv[2])
while time.time() < stop:                       # compute until the time is up
    pass
usage = resource.getrusage(resource.RUSAGE_SELF)
print(usage.ru_utime + usage.ru_stime)          # the CPU seconds this process received
"""

def cpu_received(plan, seconds=2.0):
    """Start one busy process per (command prefix, nice steps) pair at once; return the CPU seconds each one received."""
    processes = [subprocess.Popen(prefix + [sys.executable, "-c", WORKER, str(nice), str(seconds)], stdout=subprocess.PIPE, text=True) for prefix, nice in plan]
    return [float(process.communicate()[0]) for process in processes]

def compare(label, first, second, seconds=2.0):
    cores = os.cpu_count()
    received = cpu_received([first] * cores + [second] * cores, seconds)
    a, b = sum(received[:cores]) / cores, sum(received[cores:]) / cores
    print(f"{label}: first group {a:.2f} s, second group {b:.2f} s of CPU in a {seconds:.0f}-second window ({b / a:.0%} as much)")

compare("nice 0 against nice 19", ([], 0), ([], 19))
if shutil.which("taskpolicy"):                      # a macOS command that runs a program in a lower-priority class
    compare("normal against taskpolicy -b", ([], 0), (["taskpolicy", "-b"], 0))
```

One run on the test machine printed:

```
nice 0 against nice 19: first group 0.91 s, second group 0.95 s of CPU in a 2-second window (104% as much)
normal against taskpolicy -b: first group 1.84 s, second group 0.86 s of CPU in a 2-second window (47% as much)
```

On the Mac used for this module, the nice value made no measurable difference: the group at nice 19 received as much CPU as the group at nice 0, in every run made while preparing this lesson. The lowered *class*, in contrast, cut its group's CPU time to well under the normal group's (between 38% and 49% of it in the runs made while preparing this lesson). The same program on a Linux machine would show something different, because the kernel documentation quoted above says a nice +19 task there gets a small fraction of the CPU when competing with normal tasks. A priority is a request that goes into the scheduler's policy; it is not a promise, and two kernels can answer it very differently. That is the practical reason to know the *principles* of priority scheduling (urgency, preemption, starvation, aging, feedback) and to measure on the system you actually use.

## ✅ Checking the Implementation

The simulators were tested on 3,000 random workloads. For the priority policy, each time a job was chosen it had the most urgent priority among the ready jobs (and, in the preemptive version, at every tick); for aging, the chosen job had the smallest effective priority at every dispatch; and for the multilevel feedback queue, every job ran exactly its burst, no job ran while a job at a higher level was waiting, a job never used more than its level's quantum without being demoted (unless it finished), and the CPU never idled while any job was ready.

## Common Misconceptions

- **"Priority scheduling is the same as shortest job first."** Shortest job first is priority scheduling with the priority defined as the job's length. A general priority can mean anything, such as importance or the amount paid, and need not be related to length.
- **"A higher priority number means a more urgent job."** It depends on the system: in this module and in Linux's nice values a smaller number is more urgent, while Linux's real-time priorities work the other way round.
- **"Setting a low priority always makes a process run much more slowly."** A priority is advice to the scheduler. On the Mac used here, a nice value of 19 had no measurable effect while another mechanism did.
- **"Aging is only a cure for starvation."** It is also a trade: the older job's gain is the newer jobs' delay, as the experiment showed.
- **"Preemption fixes priority problems."** It stops a low-priority job from holding the CPU, but it does nothing about a low-priority job holding a lock that a high-priority job needs (priority inversion).

## ➡️ Next

This completes the CPU Scheduling module: how a scheduler is judged, and four policies that each trade one measure against another. The next module of this section, [Deadlocks and Concurrency](../deadlocks-and-concurrency/README.md), deals with what happens when the processes and threads that the scheduler runs *share* resources, and can block one another for good.
