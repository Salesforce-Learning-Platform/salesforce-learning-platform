# 📏 Shortest Job First (SJF) Scheduling

## Put the Short Jobs First

If a scheduler knew how long each ready job would run, it could do better than first come, first served: serve the shortest job first. This policy is called **shortest job next** (SJN), **shortest job first** (SJF), or **shortest process next**, and it chooses the waiting process with the smallest execution time. It is a non-preemptive algorithm, and its preemptive variant is **shortest remaining time first** (SRTF): whenever a new job arrives with less work than the running job has left, the running job is interrupted and the newcomer takes the CPU ([Wikipedia: Shortest job next](https://en.wikipedia.org/wiki/Shortest_job_next); [Wikipedia: Shortest remaining time](https://en.wikipedia.org/wiki/Shortest_remaining_time)). The idea is the same as at a supermarket with an express lane: the customer with one item should not wait behind a full trolley, and the trolley customer loses little by waiting for a handful of single items.

This file shows the effect, explains why the policy is optimal in one precise sense and checks that claim exhaustively, demonstrates its famous flaw (long jobs can starve), and then faces the practical problem that a real kernel does not know how long a job will run. It uses the toolkit introduced in [cpu-scheduling-basics.md](cpu-scheduling-basics.md), repeated here so that the file runs on its own. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon); the simulations are deterministic.

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

fcfs = lambda job, remaining, waited: (job.arrival,)                 # earliest arrival first
sjf = lambda job, remaining, waited: (job.burst, job.arrival)        # smallest burst first; never interrupted
srtf = lambda job, remaining, waited: (remaining, job.arrival)       # smallest remaining time; re-decided at every tick

def summary(label, jobs, timeline):
    result = metrics(jobs, timeline)
    mean = lambda field: sum(row[field] for row in result.values()) / len(result)
    print(f"{label:<28} {mean('turnaround'):>10.2f} {mean('waiting'):>8.2f} {mean('response'):>9.2f} {switches(timeline):>9}")

HEADER = f"{'policy':<28} {'turnaround':>10} {'waiting':>8} {'response':>9} {'switches':>9}"
```

## 🏁 Same Jobs, Shorter Waits

Four jobs, all available at time 0, with bursts of 6, 8, 7, and 3 ticks. In FCFS they run in the order listed; in SJF the 3-tick job goes first, then the 6, the 7, and the 8:

```python
jobs = [Job("P1", 0, 6), Job("P2", 0, 8), Job("P3", 0, 7), Job("P4", 0, 3)]
print(HEADER)
summary("first come, first served", jobs, schedule(jobs, fcfs))
summary("shortest job first", jobs, schedule(jobs, sjf))
print()
report(jobs, schedule(jobs, sjf))
```

```text
policy                       turnaround  waiting  response  switches
first come, first served          16.25    10.25     10.25         3
shortest job first                13.00     7.00      7.00         3

 job arrival burst finish turnaround waiting response
  P1       0     6      9          9       3        3
  P2       0     8     24         24      16       16
  P3       0     7     16         16       9        9
  P4       0     3      3          3       0        0
                 average      13.00    7.00     7.00
CPU busy 24 of 24 ticks (100%) | throughput 0.167 jobs per tick | switches between jobs: 3
order: P4 0-3 | P1 3-9 | P3 9-16 | P2 16-24
```

SJF cut the average waiting time from 10.25 ticks to 7. The work done and the finish time of the last job (24 ticks) are the same; what changed is how the waiting was shared out. The three short jobs finish early and the long one finishes last, instead of an unlucky short job waiting behind a long one.

## 🏆 Why It Is Optimal

When all the jobs are available at the same time, no order of execution has a lower average waiting time than shortest-first, and the reason is a simple exchange argument. Take any schedule in which a longer job *a* runs immediately before a shorter job *b*. If they swap places, the shorter job now waits *a* ticks less, and the longer job waits *b* ticks more; every other job is unaffected, because the two together still occupy the same stretch of time. The change in total waiting is *b − a*, which is negative. So any order that has a longer job directly before a shorter one can be improved, and the only order with no such pair is the one sorted from shortest to longest. Wikipedia states the same property: SJN minimizes the average time processes wait until their execution is complete ([Wikipedia: Shortest job next](https://en.wikipedia.org/wiki/Shortest_job_next)).

An argument is easy to get wrong, so the next block tests it by brute force. For 500 random workloads of between two and seven jobs, it tries *every possible order* of the jobs and checks that none beats the sorted order:

```python
import random
from itertools import permutations

def average_waiting(order):
    """Average waiting time when jobs that all arrive at time 0 run in this order of burst lengths."""
    waited = elapsed = 0
    for burst in order:
        waited += elapsed                           # this job waited for everything that ran before it
        elapsed += burst
    return waited / len(order)

rng = random.Random(3)
for _ in range(500):
    bursts = [rng.randint(1, 20) for _ in range(rng.randint(2, 7))]
    best_of_all_orders = min(average_waiting(order) for order in permutations(bursts))
    assert average_waiting(sorted(bursts)) == best_of_all_orders
print("sorted order matched the best of all possible orders in 500 random workloads")
```

```text
sorted order matched the best of all possible orders in 500 random workloads
```

## 🔁 With Arrivals: SJF Versus SRTF

When jobs arrive over time, a non-preemptive scheduler can make a choice it later regrets: it starts a long job, and a short job arrives a moment later and must wait. Preemption removes the regret. The four jobs below arrive at times 0, 1, 2, and 3. Under SJF, P1 (8 ticks) starts at once and nothing can stop it. Under SRTF, P2 arrives at time 1 needing 4 ticks while P1 has 7 left, and takes over:

```python
jobs = [Job("P1", 0, 8), Job("P2", 1, 4), Job("P3", 2, 9), Job("P4", 3, 5)]
print(HEADER)
summary("first come, first served", jobs, schedule(jobs, fcfs))
summary("shortest job first", jobs, schedule(jobs, sjf))
summary("shortest remaining time", jobs, schedule(jobs, srtf, preemptive=True))
print()
report(jobs, schedule(jobs, srtf, preemptive=True))
```

```text
policy                       turnaround  waiting  response  switches
first come, first served          15.25     8.75      8.75         3
shortest job first                14.25     7.75      7.75         3
shortest remaining time           13.00     6.50      4.25         4

 job arrival burst finish turnaround waiting response
  P1       0     8     17         17       9        0
  P2       1     4      5          4       0        0
  P3       2     9     26         24      15       15
  P4       3     5     10          7       2        2
                 average      13.00    6.50     4.25
CPU busy 26 of 26 ticks (100%) | throughput 0.154 jobs per tick | switches between jobs: 4
order: P1 0-1 | P2 1-5 | P4 5-10 | P1 10-17 | P3 17-26
```

Preemption brought the average waiting time down again, from 7.75 to 6.5, and the average response time from 7.75 to 4.25: the long first job now waits so that the short ones do not. The Gantt chart shows how, with P1 split into two pieces around P2 and P4, and the policy used one more switch than SJF did. A classic result, proved by Linus Schrage in 1968, is that shortest remaining processing time minimizes the mean completion time of the jobs among *all* schedules that may interrupt jobs ([Schrage, *Operations Research* 16(3), 1968](https://econpapers.repec.org/RePEc:inm:oropre:v:16:y:1968:i:3:p:687-690)); and since the waiting time is the completion time minus the arrival time and the burst, it minimizes the average waiting time as well. The tests at the end of this section confirmed it on random workloads: SRTF's average waiting time was never higher than that of FCFS or of non-preemptive SJF.

## 🥶 Starvation

The price of favouring short jobs is paid by long ones. If shorter jobs keep arriving, a long job may never be chosen: it **starves**. Wikipedia lists this as the main drawback of both SJN and SRT: long processes may be held off indefinitely if short processes are continually added ([Wikipedia: Shortest remaining time](https://en.wikipedia.org/wiki/Shortest_remaining_time)). To see it, give the CPU a stream of 2-tick jobs arriving every 2 ticks, so that a new short job is always ready the moment the previous one ends, and add one long job of 10 ticks in the middle. The last row uses a policy that avoids the trap: **highest response ratio next** (HRRN), which prefers the job with the highest value of (waiting time + burst) / burst, so that a job's priority rises the longer it waits ([Wikipedia: Highest response ratio next](https://en.wikipedia.org/wiki/Highest_response_ratio_next)):

```python
hrrn = lambda job, remaining, waited: (-(waited + job.burst) / job.burst, job.arrival)

jobs = [Job("short0", 0, 2), Job("long", 1, 10)] + [Job(f"short{i}", 2 * i, 2) for i in range(1, 31)]
print(f"{'policy':<28} {'long job starts':>15} {'long job ends':>13} {'avg wait of the shorts':>22}")
for label, key, preemptive in (("first come, first served", fcfs, False), ("shortest job first", sjf, False),
                               ("shortest remaining time", srtf, True), ("highest response ratio next", hrrn, False)):
    timeline = schedule(jobs, key, preemptive)
    result = metrics(jobs, timeline)
    shorts = [result[job.name]["waiting"] for job in jobs if job.name.startswith("short")]
    print(f"{label:<28} {result['long']['response'] + 1:>15} {result['long']['finish']:>13} {sum(shorts) / len(shorts):>22.2f}")
```

```text
policy                       long job starts long job ends avg wait of the shorts
first come, first served                   2            12                   9.68
shortest job first                        62            72                   0.00
shortest remaining time                   62            72                   0.00
highest response ratio next                2            12                   9.68
```

Under SJF and SRTF the 10-tick job waits until time 62, when the stream of short jobs finally ends; the short jobs themselves never wait at all. Under FCFS the long job runs as soon as the CPU is free (time 2), and every short job in the stream behind it waits, 9.68 ticks on average. HRRN lands on the FCFS result here: the long job's ratio rises as it waits and wins at its first opportunity, which shows both the strength and the cost of **aging**: it guarantees that a long job gets its turn, at the price of delaying the short jobs that arrive meanwhile. [priority-scheduling.md](priority-scheduling.md) returns to aging in general.

## 🔮 The Crystal-Ball Problem

SJF has a practical problem that no experiment can fix: it needs to know each job's length in advance, and a kernel does not. Wikipedia notes that the total execution time of a job must be known before it runs, that it can be estimated, for example with a weighted average of earlier execution times, and that SJN is therefore used mainly in specialized environments where accurate estimates exist ([Wikipedia: Shortest job next](https://en.wikipedia.org/wiki/Shortest_job_next)). For CPU scheduling the useful quantity is the *next CPU burst* of a process, and a standard way to guess it is **exponential averaging**: the new guess blends the burst that has just been measured with the previous guess,

*guess*<sub>next</sub> = α × *burst*<sub>just measured</sub> + (1 − α) × *guess*<sub>previous</sub>

where α between 0 and 1 says how much weight the most recent burst gets. With α = 0 history alone decides; with α = 1 only the last burst counts. The first block below follows the guesses for a process whose bursts jump from about 5 to 13, and the second compares several values of α on a longer, noisy series whose typical burst jumps from about 5 to about 20 halfway through:

```python
def predict(bursts, alpha, first_guess):
    """The sequence of guesses: first_guess, then one new guess after every measured burst."""
    guesses = [first_guess]
    for measured in bursts:
        guesses.append(alpha * measured + (1 - alpha) * guesses[-1])
    return guesses

observed = [6, 4, 6, 4, 13, 13, 13, 13]
print("measured bursts:", observed)
print("guesses, alpha = 0.5:", predict(observed, 0.5, 10))

rng = random.Random(8)
series = [max(1, round(rng.gauss(5, 1.5))) for _ in range(60)] + [max(1, round(rng.gauss(20, 3))) for _ in range(60)]
for alpha in (0.1, 0.3, 0.5, 0.7, 0.9):
    guesses = predict(series, alpha, series[0])
    error = sum(abs(guess - actual) for guess, actual in zip(guesses, series)) / len(series)
    print(f"alpha {alpha}: average error of the guesses {error:.2f} ticks")
```

```text
measured bursts: [6, 4, 6, 4, 13, 13, 13, 13]
guesses, alpha = 0.5: [10, 8.0, 6.0, 6.0, 5.0, 9.0, 11.0, 12.0, 12.5]
alpha 0.1: average error of the guesses 2.57 ticks
alpha 0.3: average error of the guesses 2.20 ticks
alpha 0.5: average error of the guesses 2.26 ticks
alpha 0.7: average error of the guesses 2.38 ticks
alpha 0.9: average error of the guesses 2.53 ticks
```

In the first sequence the guesses start at 10, settle around 6 while the bursts are 6 and 4, and then climb towards 13 as the bursts change, lagging a little behind the truth. In the comparison, no extreme is best: a small α reacts too slowly to the change of behaviour, a large α chases every random wobble, and a middle value (0.3 in this run) gives the smallest average error. Predicting bursts this way is what real systems do in spirit, and the idea survives in schedulers that favour processes with short recent bursts, such as interactive programs. A **multilevel feedback queue** can approximate shortest-job-first without any prediction at all, by observing how long jobs actually run and lowering the priority of those that run long ([Wikipedia: Shortest job next](https://en.wikipedia.org/wiki/Shortest_job_next)); it is the last topic of [priority-scheduling.md](priority-scheduling.md).

## ✅ Checking the Implementation

The simulation engine was also tested on 3,000 random workloads, with arrivals, idle gaps and tied burst lengths. For SJF, whenever the CPU became free, the job chosen had the smallest burst among the jobs that had arrived, and no job was ever interrupted. For SRTF, at every single tick the running job had the least remaining time among the ready jobs. And in every workload, the average waiting time under SRTF was no higher than under SJF or FCFS.

## Common Misconceptions

- **"SJF is the best algorithm."** It is optimal for one measure (average waiting time) under one assumption (known burst lengths). It can starve long jobs, and the assumption almost never holds in practice.
- **"SJF only works when all jobs arrive together."** It works with arrivals, but then the non-preemptive version is no longer optimal, which is why the preemptive SRTF exists.
- **"A shorter average wait means every job is better off."** The average hides who pays. In the starvation experiment, the shorts waited nothing while the long job waited 61 ticks.
- **"The scheduler can read a process's burst length from the program."** The kernel sees only what has already happened; the future length of a burst has to be guessed from the past.

## ➡️ Next

Continue to [round-robin.md](round-robin.md): a policy that needs no predictions at all. It simply gives every ready job a short turn, in rotation, and then asks what the right length for a turn is.
