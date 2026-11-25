# ⏱️ CPU Scheduling Basics

## Who Gets the CPU Next?

[process-states.md](../processes-and-threads/process-states.md) ended with a crowd: at any moment a computer has far more processes and threads that are *ready to run* than it has CPU cores, and the kernel must decide, again and again, which of them runs next and for how long. That decision is **CPU scheduling**, and the part of the kernel that makes it is the **scheduler**. Scheduling in general means assigning resources to tasks; for the CPU it is what makes multitasking on a limited number of cores possible, and a scheduler may aim at several goals at once, such as keeping the processor busy, finishing as much work as possible per unit of time, responding quickly to users, and treating every task fairly. Those goals often conflict, so every scheduler is a compromise ([Wikipedia: Scheduling (computing)](https://en.wikipedia.org/wiki/Scheduling_(computing))).

This module studies the classic policies one at a time: [first-come, first-served](fcfs-scheduling.md), [shortest job first](shortest-job-first.md), [round robin](round-robin.md), and [priority scheduling](priority-scheduling.md). This file provides the vocabulary and the measuring tools that all of them share, including a small simulator that the later files reuse. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon); the simulations are deterministic.

## 🔁 Bursts: The Shape of a Process's Life

A running program alternates between two kinds of activity. It *computes* for a while, a **CPU burst**, and then it needs something it cannot get from the CPU, such as a disk read, a network packet, or a keypress, and *waits*: an **I/O wait**, during which the process is in the waiting state and uses no processor time (as measured in [kernel-and-user-mode.md](../introduction-to-operating-systems/kernel-and-user-mode.md)). Then another CPU burst begins, and so on until the process ends. A program that spends most of its time computing, such as a video encoder, is **CPU-bound** and has long bursts; a program that spends most of its time waiting, such as a text editor, is **I/O-bound** and has many very short ones. A good scheduler exploits this shape: while one process waits, the CPU runs another, which is the gain from multiprogramming shown in the simulator of [process-states.md](../processes-and-threads/process-states.md) (12 ticks instead of 17). The policies in this module simplify the picture by treating a job as a single CPU burst of known length; the sections on [shortest job first](shortest-job-first.md) and [priority scheduling](priority-scheduling.md) return to how a real system copes with not knowing it.

## 🧰 The Scheduler, the Dispatcher, and the Ready Queue

Three pieces cooperate. The **ready queue** holds every process that is ready to run (the Ready state of the five-state model). The **scheduler** is the policy: it looks at the ready queue and selects the next process. The **dispatcher** is the mechanism: it is the module that gives control of the CPU to the process the scheduler selected, which means performing the context switch (saving the old context and loading the new one), switching to user mode, and jumping to the right place in the user program. It runs in kernel mode as the result of an interrupt or a system call, and since it runs on every switch, it should be as fast as possible ([Wikipedia: Scheduling (computing)](https://en.wikipedia.org/wiki/Scheduling_(computing)); the switch itself is the subject of [context-switching.md](../processes-and-threads/context-switching.md)).

Operating systems may have up to three kinds of scheduler, named for how often they make decisions: a **long-term** (admission) scheduler that decides which jobs enter the system at all, a **medium-term** scheduler that swaps processes out of memory and back, and the **short-term** (CPU) scheduler that chooses among the ready processes, which runs most often and is the subject of this module (the same article).

## ⏰ When Does the Scheduler Run?

A scheduling decision can be needed at four moments:

| Moment | Example | State change |
|--------|---------|--------------|
| 1. The running process cannot continue | It starts a disk read or sleeps | Running → Waiting |
| 2. The running process is forced to stop | A timer interrupt ends its time slice | Running → Ready |
| 3. A waiting process becomes able to run | Its I/O completes | Waiting → Ready |
| 4. The running process ends | It exits | Running → Terminated |

A scheduler that acts *only* at moments 1 and 4 can never take the CPU away from a process that does not give it up: it is **non-preemptive** (also called **cooperative** or voluntary). A scheduler that also acts at moments 2 and 3 can remove a running process and give the CPU to another one: it is **preemptive**. Wikipedia describes the same two kinds: a preemptive scheduler can force processes off the CPU, while a cooperative one cannot ([Wikipedia: Scheduling (computing)](https://en.wikipedia.org/wiki/Scheduling_(computing))). Preemption needs hardware support (the timer interrupt) and costs context switches, but without it one program stuck in an endless loop would hold the CPU forever. Every desktop and server operating system today is preemptive.

## 📏 How to Judge a Scheduler

Several measurements, each with a precise meaning, say how well a scheduler served a set of jobs. The definitions used in this module, for a job that arrives at some time, needs some amount of CPU time (its **burst**), and finishes at some time, are:

| Measure | Definition | Better when |
|---------|------------|-------------|
| **Turnaround time** | Finish time − arrival time: everything from submission to completion | Smaller |
| **Waiting time** | Turnaround time − burst: the total time the job spent ready but not running | Smaller |
| **Response time** | First time the job runs − arrival time: how long before it gets *any* attention | Smaller |
| **CPU utilization** | The share of time the CPU is busy | Larger |
| **Throughput** | Jobs completed per unit of time | Larger |
| **Fairness** | Whether comparable jobs receive comparable treatment, and none is starved | Judged case by case |

Sources differ in their names for these. What this module calls response time is sometimes called wait time (the time until the first start), and the total ready-queue time is then called something else, so always check which definition a text is using. For an interactive system, response time usually matters most, because it is what a person feels; for a batch system, throughput and turnaround matter more.

## 🧪 A Scheduling Laboratory

Time is counted in whole **ticks**. The toolkit below describes a job (name, arrival time, burst, and a priority that later files use), turns a simulation into a **timeline** (which job ran in each tick, or `None` when the CPU was idle), measures every quantity in the table above from that timeline, and prints a report with a **Gantt chart**, the standard text description of who ran when. The function `schedule` is a small engine for the policies that pick the job with the smallest *key* from the ready jobs; each policy in this module is simply a different key:

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
```

The first scenario has three jobs, with a gap in their arrivals so that the CPU goes idle. The policy is first come, first served: the key is the arrival time, so the job that arrived earliest runs first and keeps the CPU until it finishes:

```python
jobs = [Job("A", 0, 6), Job("B", 2, 4), Job("C", 15, 3)]
timeline = schedule(jobs, lambda job, remaining, waited: (job.arrival,))
average = report(jobs, timeline)
```

```text
 job arrival burst finish turnaround waiting response
   A       0     6      6          6       0        0
   B       2     4     10          8       4        4
   C      15     3     18          3       0        0
                 average       5.67    1.33     1.33
CPU busy 13 of 18 ticks (72%) | throughput 0.167 jobs per tick | switches between jobs: 1
order: A 0-6 | B 6-10 | idle 10-15 | C 15-18
```

Check the numbers against the definitions. Job B arrives at time 2 but the CPU is busy with A until time 6, so B's response time is 4 (first run at 6, minus arrival 2), its finish time is 10, its turnaround time is 8 (10 − 2), and its waiting time is 4 (turnaround 8 minus burst 4). Job C arrives at time 15, after the CPU has been idle from time 10 to 15, so it starts at once and waits for nothing. The CPU was busy for 13 of the 18 ticks, a utilization of 72%, and three jobs finished in 18 ticks, a throughput of about 0.167 jobs per tick. The line `switches between jobs` counts how many times the CPU went directly from one job to a different one (the A-to-B change only; the idle gap before C is not a switch from a job), which becomes important for preemptive policies.

## 🧭 No Policy Wins Everywhere

To see why scheduling has several algorithms and not one, run the same four jobs under three different policies and compare the averages. The jobs arrive at different times, and the three policies are first come, first served (earliest arrival first), shortest job first (the shortest burst among the ready jobs, once started never interrupted), and shortest remaining time first (the same idea, but a newly arrived short job may take over from the running one):

```python
fcfs = lambda job, remaining, waited: (job.arrival,)
sjf = lambda job, remaining, waited: (job.burst, job.arrival)
srtf = lambda job, remaining, waited: (remaining, job.arrival)

workload = [Job("P1", 0, 8), Job("P2", 1, 4), Job("P3", 2, 9), Job("P4", 3, 5)]
print(f"{'policy':<26} {'avg turnaround':>14} {'avg waiting':>11} {'avg response':>12} {'switches':>8}")
for label, key, preemptive in (("first come, first served", fcfs, False),
                               ("shortest job first", sjf, False),
                               ("shortest remaining time", srtf, True)):
    timeline = schedule(workload, key, preemptive)
    result = metrics(workload, timeline)
    mean = lambda field: sum(row[field] for row in result.values()) / len(result)
    print(f"{label:<26} {mean('turnaround'):>14.2f} {mean('waiting'):>11.2f} {mean('response'):>12.2f} {switches(timeline):>8}")
```

```text
policy                     avg turnaround avg waiting avg response switches
first come, first served            15.25        8.75         8.75        3
shortest job first                  14.25        7.75         7.75        3
shortest remaining time             13.00        6.50         4.25        4
```

The ranking is not a tie: favouring short jobs lowers the average waiting and turnaround time, and the preemptive version does best on every average, including response time. But it is not free, because letting a newly arrived job take over adds a switch (4 instead of 3 here), and each switch costs real time on a real machine. It also quietly assumes that the scheduler knows how long each job will run, which a real kernel generally does not. The rest of the module takes each policy apart:

| Policy | Idea | Preemptive? | Main weakness |
|--------|------|-------------|---------------|
| [First come, first served](fcfs-scheduling.md) | Run jobs in order of arrival | No | One long job delays every short job behind it |
| [Shortest job first](shortest-job-first.md) | Run the shortest job next (shortest remaining time first is the preemptive version) | Either | Long jobs can starve, and burst lengths must be predicted |
| [Round robin](round-robin.md) | Give each job a fixed time slice in turn | Yes | A poor slice length wastes time on switching or delays short jobs |
| [Priority scheduling](priority-scheduling.md) | Run the most urgent job first | Either | Low-priority jobs can starve unless priorities age |

Real kernels combine these ideas. They keep several priority levels, time-slice among jobs at the same level, and adjust priorities according to behaviour, which is the subject of the end of [priority-scheduling.md](priority-scheduling.md).

## Common Misconceptions

- **"There is a best scheduling algorithm."** Each one optimizes some measure at the expense of another. The right choice depends on whether the system serves interactive users, batch jobs, or deadlines.
- **"The scheduler and the dispatcher are the same thing."** The scheduler decides which process runs; the dispatcher performs the switch to it. One is policy, the other mechanism.
- **"Waiting time means time spent waiting for I/O."** In scheduling, waiting time is the time a job spends *ready* in the queue, waiting for the CPU. Time blocked on I/O is a different wait.
- **"Preemption is always better."** It improves response time and stops one job from hogging the CPU, but it adds context switches and complicates programs that share data. Some real-time and embedded systems deliberately avoid it.
- **"Higher CPU utilization always means a better scheduler."** A busy CPU doing useless switching is fully utilized. Utilization says nothing about whether the right jobs got the CPU.

## ➡️ Next

Continue to [fcfs-scheduling.md](fcfs-scheduling.md): the simplest policy, why it is fair and simple but can make short jobs wait a very long time, and a measurement of the convoy effect.
