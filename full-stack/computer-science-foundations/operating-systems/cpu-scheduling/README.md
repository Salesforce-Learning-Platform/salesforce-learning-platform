# ⏱️ CPU Scheduling

## 📚 Overview

A computer has far more programs ready to run than it has processor cores, so the operating system must keep choosing which one runs next and for how long. That choice, **CPU scheduling**, decides how fast a typed character appears on screen, how long a job waits behind a long one, whether a background task can slow down the foreground, and whether a time-critical task meets its deadline. There is no single best answer: every policy favours some measure of performance at the expense of another, which is why the field has several classic algorithms and why real kernels combine them.

This module builds the subject from the measurements up. It begins with the vocabulary (the scheduler and the dispatcher, preemptive and cooperative scheduling, and the criteria of **turnaround, waiting, and response time, throughput, and CPU utilization**) and a small simulator that draws Gantt charts and computes every measure, which all later files reuse. It then studies four policies in turn: **first come, first served**, where order alone decides and one long job can hold up many short ones (the convoy effect); **shortest job first** and its preemptive form, which is provably optimal for average waiting time but starves long jobs and needs a crystal ball for burst lengths, with exponential averaging as the usual workaround; **round robin**, which gives everyone a turn and turns the quantum into a trade-off between response time and switching overhead; and **priority scheduling**, with starvation, aging, priority inversion, and the multilevel feedback queue that learns priorities by watching jobs. The last section measures what a priority is worth on a real machine. Every code example was run on CPython 3.9 on a Mac (macOS, Apple silicon); the simulations are deterministic, machine-dependent values are labelled, and every simulator was checked against its defining properties on thousands of random workloads.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Distinguish the scheduler from the dispatcher and the three kinds of scheduler, and explain the difference between preemptive and cooperative scheduling and the four moments at which a scheduling decision can be needed.
- Define turnaround time, waiting time, response time, throughput, and CPU utilization, compute them from a timeline, and read and draw a Gantt chart.
- Simulate first come, first served, explain the convoy effect, and show how the arrival order alone changes the averages.
- Explain why shortest job first minimizes average waiting time, why shortest remaining time first improves on it when jobs arrive over time, how starvation arises, and how exponential averaging predicts the next CPU burst.
- Simulate round robin, explain how the time quantum trades response time against switching overhead, and state the waiting bound that makes it starvation-free.
- Simulate preemptive and non-preemptive priority scheduling, explain starvation, aging, and priority inversion, and describe how a multilevel feedback queue approximates shortest-job-first without knowing job lengths.
- Describe how real systems (Linux's policies, nice values, real-time priorities, and the macOS background class) interpret priorities, and test the effect of a priority on your own machine.

## 📋 Prerequisites

- [Processes and Threads](../processes-and-threads/README.md): especially [process-states.md](../processes-and-threads/process-states.md) (the ready queue and the five states) and [context-switching.md](../processes-and-threads/context-switching.md) (what a switch is and what it costs).
- [Introduction to Operating Systems](../introduction-to-operating-systems/README.md): the timer interrupt that makes preemption possible.
- Basic Python reading ability: classes, dictionaries, sorting with keys, and the standard library.
- No earlier knowledge of scheduling is assumed.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [cpu-scheduling-basics.md](cpu-scheduling-basics.md) | The scheduler and dispatcher, CPU and I/O bursts, preemptive and cooperative scheduling, the scheduling criteria, and the simulator toolkit used by the rest of the module |
| [fcfs-scheduling.md](fcfs-scheduling.md) | First come, first served as a queue, the effect of arrival order, a measurement of the convoy effect, and where FCFS survives in real systems |
| [shortest-job-first.md](shortest-job-first.md) | SJF and SRTF, an exhaustive check of optimality, starvation measured against FCFS and highest response ratio next, and burst prediction by exponential averaging |
| [round-robin.md](round-robin.md) | Time slices in rotation, a simulator with switching cost, the quantum trade-off measured, and the waiting bound |
| [priority-scheduling.md](priority-scheduling.md) | Preemptive and non-preemptive priorities, starvation and aging, priority inversion, a multilevel feedback queue, and an experiment on what nice values and priority classes do on a real machine |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [cpu-scheduling-basics.md](cpu-scheduling-basics.md) and [round-robin.md](round-robin.md) first if you are preparing for exams or interviews: the definitions of turnaround, waiting, and response time, and the Gantt-chart calculations for FCFS, SJF, and round robin, are the standard questions, and the quantum trade-off is the standard discussion. [priority-scheduling.md](priority-scheduling.md) is the one to read for how real systems work.

**Skim** [fcfs-scheduling.md](fcfs-scheduling.md) once you have seen the convoy effect, and run the simulators from [shortest-job-first.md](shortest-job-first.md) if you want to explore the optimality claim yourself: change the workload and watch the averages.

## 🧠 Knowledge Check

<details>
<summary>Three jobs of 24, 3, and 3 ticks all arrive at time 0. Compare the average waiting time under first come, first served (in that order) and under shortest job first, and say why a real scheduler cannot simply always use the better one.</summary>

Under FCFS the jobs wait 0, 24, and 27 ticks, an average of 17. Under SJF the order is 3, 3, 24, so they wait 0, 3, and 6 ticks, an average of 3: the best possible average for these jobs, since no other order beats shortest-first. A real scheduler cannot just use SJF because it needs to know in advance how long each job will run, which a kernel does not; it can only estimate the next CPU burst from the past (for example by exponential averaging), and SJF also starves long jobs if short ones keep arriving. See [fcfs-scheduling.md](fcfs-scheduling.md) and [shortest-job-first.md](shortest-job-first.md).

</details>

<details>
<summary>A round-robin scheduler has a quantum of 4 ms and each switch costs 1 ms. What fraction of the CPU does useful work when every process uses its whole quantum, and what is the effect of raising the quantum to 100 ms?</summary>

Each turn does 4 ms of useful work and then 1 ms of switching, so the useful fraction is 4 / (4 + 1) = 80%. With a quantum of 100 ms it becomes 100 / 101, about 99%, so the overhead nearly vanishes, but a process may now wait up to (*n* − 1) × 100 ms between turns when *n* processes are ready, so ten ready processes could each wait nearly a second, and the scheduler behaves almost like first come, first served for short jobs. The quantum has to be long compared with the switch cost and short compared with the patience of a user; the experiment in [round-robin.md](round-robin.md) measured exactly 80% useful work at a quantum of 4 ticks with a switch cost of 1 tick.

</details>

## 📚 References

- [Wikipedia: Scheduling (computing)](https://en.wikipedia.org/wiki/Scheduling_(computing)), [Shortest job next](https://en.wikipedia.org/wiki/Shortest_job_next), [Shortest remaining time](https://en.wikipedia.org/wiki/Shortest_remaining_time), [Highest response ratio next](https://en.wikipedia.org/wiki/Highest_response_ratio_next), [Round-robin scheduling](https://en.wikipedia.org/wiki/Round-robin_scheduling), [Aging (scheduling)](https://en.wikipedia.org/wiki/Aging_(scheduling)), [Multilevel feedback queue](https://en.wikipedia.org/wiki/Multilevel_feedback_queue), [Priority inversion](https://en.wikipedia.org/wiki/Priority_inversion), and [Preemption (computing)](https://en.wikipedia.org/wiki/Preemption_(computing)): the policies and their properties.
- Linus Schrage, ["A Proof of the Optimality of the Shortest Remaining Processing Time Discipline"](https://econpapers.repec.org/RePEc:inm:oropre:v:16:y:1968:i:3:p:687-690), *Operations Research* 16(3), 1968: the classic optimality result behind SRTF.
- [Linux man page: `sched(7)`](https://man7.org/linux/man-pages/man7/sched.7.html), [`nice(2)`](https://man7.org/linux/man-pages/man2/nice.2.html), and [`setpriority(2)`](https://man7.org/linux/man-pages/man2/setpriority.2.html), and the Linux kernel documentation on the [CFS scheduler](https://docs.kernel.org/scheduler/sched-design-CFS.html), the [EEVDF scheduler](https://docs.kernel.org/scheduler/sched-eevdf.html), and [nice levels](https://docs.kernel.org/scheduler/sched-nice-design.html): how a real kernel schedules.
- [taskpolicy(8)](https://keith.github.io/xcode-man-pages/taskpolicy.8.html): the macOS command used in the priority experiment.
- *Operating Systems: Three Easy Pieces*, free chapters: [Scheduling: Introduction](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf), [Scheduling: The Multi-Level Feedback Queue](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf), and [Scheduling: Proportional Share](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-lottery.pdf).
- [GeeksforGeeks: CPU Scheduling in Operating Systems](https://www.geeksforgeeks.org/operating-systems/cpu-scheduling-in-operating-systems/), [FCFS](https://www.geeksforgeeks.org/dsa/first-come-first-serve-cpu-scheduling-non-preemptive/), [Shortest Job First](https://www.geeksforgeeks.org/operating-systems/shortest-job-first-or-sjf-cpu-scheduling/), [Round Robin](https://www.geeksforgeeks.org/operating-systems/round-robin-scheduling-in-operating-system/), [Priority Scheduling](https://www.geeksforgeeks.org/operating-systems/priority-scheduling-in-operating-system/), and [Multilevel Feedback Queue](https://www.geeksforgeeks.org/operating-systems/multilevel-feedback-queue-scheduling-mlfq-cpu-scheduling/): overviews and practice questions.

## ➡️ Continue Your Learning Path

Continue to the [Deadlocks and Concurrency](../deadlocks-and-concurrency/README.md) module, the next module in this section: once the scheduler can run many processes and threads, they begin to share data and resources, and the interesting new questions are how to keep them from corrupting each other's work (race conditions, mutexes, and semaphores) and from blocking each other forever (deadlocks).
