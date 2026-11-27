# 🗂️ Types of Operating Systems

## One Job, Many Goals

Every operating system manages the same resources — CPU, memory, storage, devices — but different machines want different things from them. A bank's overnight settlement run wants to finish as much work as possible; a laptop wants to feel instant when you click; a car's braking controller wants to *never* be late; a phone wants to last all day on a battery. These competing goals have produced several families of operating systems, each making different trade-offs about **throughput**, **responsiveness**, **predictability**, **size**, and **power**.

Operating systems are classified in several overlapping ways — by how they schedule work (batch, multiprogramming, time-sharing), by their timing guarantees (real-time), by how many machines they span (distributed, network), and by the device they live in (embedded, mobile). One real system usually belongs to several categories at once. This file describes each type, simulates the central trade-off between batch and time-sharing systems, and measures why an ordinary desktop OS cannot offer real-time guarantees. All outputs were produced by running the code on CPython 3.9 on a Mac (macOS, Apple silicon).

## 📋 The Main Types at a Glance

| Type | Core idea | Optimizes for | Typical examples |
|------|-----------|---------------|------------------|
| **Batch** | Jobs are collected and run one after another with no user interaction | Throughput, keeping an expensive machine busy | Early mainframes; today's scheduled batch jobs (payroll, reports, data pipelines) |
| **Multiprogramming** | Keep several jobs in memory; when one waits for I/O, run another | CPU utilization | The first step beyond batch ([Wikipedia: Computer multitasking](https://en.wikipedia.org/wiki/Computer_multitasking)) |
| **Time-sharing (multitasking)** | Switch rapidly among jobs so that many users or programs appear to run at once | Responsiveness | Unix and Linux, Windows, macOS |
| **Real-time (RTOS)** | Guarantee that tasks finish by their deadlines | Predictability (bounded latency) | VxWorks, QNX, FreeRTOS |
| **Distributed** | Make many networked computers cooperate as one system | Scale, sharing, fault tolerance | Cluster and cloud operating layers |
| **Network** | Provide services (files, printing, routing) over a network | Sharing resources between machines | Router and switch operating systems; historically, file-server OSes |
| **Embedded** | Run inside a device with a fixed purpose and tight limits | Small size, low power, reliability | Appliance, vehicle, and router firmware |
| **Mobile** | Run on phones and tablets with touch, sensors, and a battery | Energy efficiency, app sandboxing, user experience | Android, iOS |

The categories overlap. Android is a mobile, time-sharing system whose kernel is a monolithic Linux kernel ([Wikipedia: Android](https://en.wikipedia.org/wiki/Android_(operating_system))); iOS is a Unix-like mobile system based on Darwin, the same family as macOS ([Wikipedia: iOS](https://en.wikipedia.org/wiki/IOS)); and QNX, VxWorks, and FreeRTOS are real-time operating systems aimed at embedded systems ([Wikipedia: QNX](https://en.wikipedia.org/wiki/QNX), [VxWorks](https://en.wikipedia.org/wiki/VxWorks), [FreeRTOS](https://en.wikipedia.org/wiki/FreeRTOS)).

## 📦 Batch, Multiprogramming, and Time-Sharing

**Batch processing** runs a job — a program plus its data — from start to finish before beginning the next, with no one at the keyboard. It is the simplest scheme and maximizes the work done per hour, but a short job queued behind a long one waits for the whole thing, and the CPU idles whenever the running job waits for I/O.

**Multiprogramming** attacks the idle CPU: several jobs are kept in memory, and when the running one blocks on I/O, the OS switches to another. Wikipedia notes that in multiprogramming systems a task runs until it must wait for an external event or until the scheduler forcibly swaps it out ([Wikipedia: Computer multitasking](https://en.wikipedia.org/wiki/Computer_multitasking)).

**Time-sharing** goes further: the OS switches among jobs on a fixed **time slice** (a *quantum*), a few milliseconds long, regardless of whether the running job is waiting. Each user or program gets frequent short turns, so each *seems* to have the computer to itself and the system responds quickly to interactive requests. Time-sharing was developed in the early 1960s; CTSS at MIT is a well-known early example ([Wikipedia: Time-sharing](https://en.wikipedia.org/wiki/Time-sharing)).

Time-sharing buys responsiveness at a price: every switch from one job to another costs time (saving one job's state and loading another's), during which no useful work is done. The simulation below makes the trade-off concrete. Four jobs arrive together: one long job needing 100 milliseconds of CPU, and three short interactive ones needing 5 milliseconds each. The batch system runs them to completion in arrival order. The time-sharing system gives each job a slice of at most `quantum` milliseconds in rotation, paying a `switch_cost` each time it changes jobs:

```python
from collections import deque

def run_batch(bursts):
    """Run jobs to completion in arrival order. Return (when each job first ran, when each finished, total time)."""
    clock, first_run, finish = 0, [], []
    for burst in bursts:
        first_run.append(clock)
        clock += burst
        finish.append(clock)
    return first_run, finish, clock

def run_time_sharing(bursts, quantum, switch_cost):
    """Round-robin time slices; every change from one job to another costs switch_cost.
    Return (first run times, finish times, total time, number of switches, timeline of (job, start, end))."""
    n = len(bursts)
    remaining = list(bursts)
    queue = deque(range(n))
    clock, first_run, finish = 0, [None] * n, [None] * n
    previous, switches, timeline = None, 0, []
    while queue:
        job = queue.popleft()
        if previous is not None and previous != job:
            clock += switch_cost                                  # saving one job's state and loading another's
            switches += 1
        if first_run[job] is None:
            first_run[job] = clock
        run = min(quantum, remaining[job])
        timeline.append((job, clock, clock + run))
        clock += run
        remaining[job] -= run
        if remaining[job] == 0:
            finish[job] = clock
        else:
            queue.append(job)                                     # not done: back to the end of the line
        previous = job
    return first_run, finish, clock, switches, timeline

def report(name, first_run, finish, total, switches):
    n = len(first_run)
    print(f"{name:<34} | wait for first turn {sum(first_run) / n:6.2f} | turnaround {sum(finish) / n:6.2f} | short jobs finish at {finish[1:]} | total {total}")

jobs = [100, 5, 5, 5]                                              # milliseconds of CPU: one long job, three short ones
first_run, finish, total = run_batch(jobs)
report("batch: run to completion", first_run, finish, total, 0)
for quantum, cost in ((10, 1), (2, 1), (10, 0)):
    first_run, finish, total, switches, timeline = run_time_sharing(jobs, quantum, cost)
    report(f"time-sharing: quantum {quantum}, switch cost {cost}", first_run, finish, total, switches)
print(run_time_sharing(jobs, 10, 1)[4][:5])
```

```text
batch: run to completion           | wait for first turn  78.75 | turnaround 107.50 | short jobs finish at [105, 110, 115] | total 115
time-sharing: quantum 10, switch cost 1 | wait for first turn  12.75 | turnaround  46.25 | short jobs finish at [16, 22, 28] | total 119
time-sharing: quantum 2, switch cost 1 | wait for first turn   4.50 | turnaround  54.25 | short jobs finish at [28, 30, 32] | total 127
time-sharing: quantum 10, switch cost 0 | wait for first turn  11.25 | turnaround  43.75 | short jobs finish at [15, 20, 25] | total 115
[(0, 0, 10), (1, 11, 16), (2, 17, 22), (3, 23, 28), (0, 29, 39)]
```

Compare the rows:

- **Batch** makes the three short jobs wait for the 100-millisecond job: they do not even *start* until time 100, and the average wait for a first turn is 78.75 ms.
- **Time-sharing with a 10 ms quantum** cuts the average wait to 12.75 ms and lets the short jobs finish at times 16, 22, and 28 instead of 105 to 115. The long job pays only slightly: it finishes at 119 instead of 100 plus the others' time. The total time is 119 rather than 115 — the 4 ms of switching overhead, one per context switch.
- **A tiny quantum of 2 ms** makes first turns come even sooner (4.5 ms) but wastes more time switching (12 switches, total 127), and the *average turnaround gets worse* (54.25 against 46.25), because the short jobs are chopped into more rounds. Choosing the quantum is a real design decision, and [CPU Scheduling](../cpu-scheduling/README.md) ([Round Robin](../cpu-scheduling/round-robin.md)) returns to it.
- **A zero switch cost** (the last row) is an idealization; real switches are never free, which is why the lesson on [context switching](../processes-and-threads/context-switching.md) in the [Processes and Threads](../processes-and-threads/README.md) module measures them.

The same program, with a quantum at least as long as the longest job and no switch cost, gives exactly the batch schedule — the simulation was checked against that equivalence, and against the accounting identity *total time = sum of CPU bursts + switch cost × number of switches*, on thousands of random job mixes:

```python
import random

random.seed(1)
for _ in range(3_000):
    bursts = [random.randint(1, 30) for _ in range(random.randint(1, 6))]
    quantum, cost = random.randint(1, 12), random.randint(0, 3)
    first_run, finish, total, switches, timeline = run_time_sharing(bursts, quantum, cost)
    assert total == sum(bursts) + cost * switches                                      # busy time plus switching time
    assert sum(end - start for _, start, end in timeline) == sum(bursts)               # every burst is executed exactly once
    assert switches == sum(1 for (a, _, _), (b, _, _) in zip(timeline, timeline[1:]) if a != b)
    assert all(done >= burst for done, burst in zip(finish, bursts))
    assert run_time_sharing(bursts, max(bursts), 0)[:3] == run_batch(bursts)           # a huge quantum with free switches is batch
print("time-sharing simulation agrees with its accounting identities and with the batch schedule on 3,000 random job mixes")
```

```text
time-sharing simulation agrees with its accounting identities and with the batch schedule on 3,000 random job mixes
```

## ⏰ Real-Time Operating Systems

A **real-time operating system** is judged not by how fast it is on average but by whether it **meets deadlines**. If a controller must respond to a sensor within 2 milliseconds, a response that is usually fast but occasionally takes 50 is a failure. Wikipedia distinguishes *soft* real-time systems, which usually meet their deadlines, from *hard* real-time systems, which meet them deterministically ([Wikipedia: Real-time operating system](https://en.wikipedia.org/wiki/Real-time_operating_system)). Examples of hard real-time needs include flight and engine controllers, medical devices, and industrial robots; soft real-time needs include video playback and audio mixing.

An RTOS gets its guarantees by keeping every kernel operation **bounded in time** and by using priority-based scheduling in which the most urgent task always runs first. A general-purpose time-sharing OS makes no such promise — it optimizes average behaviour and fairness. The measurement below shows the difference in character. A program asks to be woken after exactly 1 millisecond, 2,000 times, and records how *late* each wake-up was — first on a quiet machine, then while twice as many CPU-hungry processes as there are cores compete for the processors:

```python
import os
import subprocess
import sys
import time

def lateness_ms(requested_ms, samples):
    errors = []
    for _ in range(samples):
        start = time.perf_counter()
        time.sleep(requested_ms / 1000)
        errors.append((time.perf_counter() - start) * 1000 - requested_ms)
    return sorted(errors)

def describe(label, late):
    print(f"{label:>6}: median lateness {late[len(late) // 2]:.3f} ms | 99th percentile {late[int(len(late) * 0.99)]:.3f} ms | worst {late[-1]:.3f} ms")

describe("quiet", lateness_ms(1, 2_000))
burners = [subprocess.Popen([sys.executable, "-c", "while True: pass"]) for _ in range(2 * (os.cpu_count() or 4))]
try:
    time.sleep(0.5)                                    # let the burners get going
    describe("loaded", lateness_ms(1, 2_000))
finally:
    for burner in burners:
        burner.kill()
    for burner in burners:
        burner.wait()
```

Output:

```
 quiet: median lateness 0.272 ms | 99th percentile 0.304 ms | worst 0.581 ms
loaded: median lateness 0.256 ms | 99th percentile 0.368 ms | worst 3.041 ms
```

On a quiet machine every wake-up is a fraction of a millisecond late. Under load the **median barely changes** — the scheduler is good at giving a sleeper a processor quickly — but the **tail grows**: the 99th percentile rises a little and the worst case several-fold (in the run above, from about half a millisecond to about three), because occasionally every processor is busy with someone else's time slice. Another run, a different machine, or a heavier load will give different numbers, and **nothing in the OS promises an upper bound**: when the timer fires, the kernel must still find a CPU for the sleeping program, and interrupts, other programs, and power management all add delay. For a video player that is fine; for an anti-lock braking controller it is not, and that is exactly the gap a real-time operating system fills.

## 🌐 Distributed and Network Operating Systems

A **distributed operating system** presents a collection of independent, networked computers as if they were one system; its pieces run on separate nodes and cooperate to schedule jobs across multiple CPUs ([Wikipedia: Distributed operating system](https://en.wikipedia.org/wiki/Distributed_operating_system)). Users and programs see a single set of resources — files, processes, memory — whose actual location is hidden. True single-system-image operating systems remain rare; most large deployments instead run ordinary operating systems on each machine and add a cluster-management layer on top.

The term **network operating system** has shifted meaning. Historically it described operating systems with networking capabilities that let personal computers join networks and share files and printers; today Wikipedia uses it for the specialized operating system of a network device such as a router, switch, or firewall ([Wikipedia: Network operating system](https://en.wikipedia.org/wiki/Network_operating_system)).

## 📱 Embedded and Mobile Operating Systems

An **embedded operating system** lives inside a device whose function is fixed — a thermostat, a router, a car's engine controller. It is typically small, starts quickly, uses little memory and power, and often has real-time requirements; some embedded devices need no OS at all. A **mobile operating system** is built for phones and tablets: it must conserve the battery (suspending background apps), isolate apps from one another and from the user's data (sandboxing and permission prompts), and manage radios, sensors, and touch input. Both are still operating systems in the sense of the previous files: they use kernel and user modes, schedule processes, manage memory, and provide files.

## Choosing and Comparing

The families answer one question differently: **when two things want the CPU, which one wins, and what does it cost?**

| Goal | Best fit |
|------|----------|
| Process the largest amount of work per hour, no one waiting | Batch |
| Keep an expensive CPU busy during slow I/O | Multiprogramming |
| Let many users or programs feel responsive | Time-sharing |
| Never miss a deadline | Real-time |
| Pool many machines | Distributed |
| Run on a battery with sensors and apps | Mobile |
| Fit in a small, fixed-purpose device | Embedded |

Modern desktop, server, and phone operating systems are all time-sharing at heart, with real-time-style priorities available for tasks such as audio, and with batch behaviour for scheduled jobs.

## Common Misconceptions

- **"Time-sharing is just faster."** It is not faster; total time grows slightly because of switching. It is more *responsive* to short and interactive work.
- **"Real-time means fast."** It means *predictable*: a slow system that always answers within its deadline is real-time; a fast one that occasionally stalls is not.
- **"Each family replaced the previous one."** They coexist: batch jobs run on time-sharing servers, and real-time kernels run inside the devices around you.
- **"Android and iOS are the same kind of thing as Windows."** They are mobile operating systems built on Unix-like kernels (Linux for Android, Darwin for iOS) with different goals around power, sandboxing, and app distribution.

## ➡️ Next

Continue to [os-architecture.md](os-architecture.md): inside the kernel, how a designer decides which services run in privileged mode — one large program (monolithic), a tiny core with services outside (microkernel), or a mixture (hybrid) — and what each choice costs.
