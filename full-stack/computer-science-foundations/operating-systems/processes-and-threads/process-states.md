# 🚦 Process States

## A Process Is Not Always Running

On a typical laptop there are hundreds of processes and a handful of CPU cores, so at any instant almost every process is *not* executing. Some are waiting for their turn; others are waiting for something to happen, such as a key press, a disk read, or a network packet. To manage this crowd, the kernel records a **state** for each process (in its process control block, described in [what-is-a-process.md](what-is-a-process.md)) and moves the process between states as events occur. The exact states vary from system to system, and a kernel may not label them as such, but the following model is a useful abstraction for understanding every one of them ([Wikipedia: Process state](https://en.wikipedia.org/wiki/Process_state)).

All code in this file was run on CPython 3.9 on a Mac (macOS, Apple silicon); the process-listing commands work the same way on Linux.

## 🗺️ The Five-State Model

```
                      dispatched (chosen by the scheduler)
              ┌───────────────────────────────────────────────┐
              │                                               ▼
   NEW ──► READY ◄──── preempted (its time slice ended) ──── RUNNING ───► TERMINATED
admitted     ▲                                                  │         exits
             │                                                  │ must wait for I/O
             │                  the I/O or event finishes       ▼ or for an event
             └──────────────────────────────────────────── WAITING
```

| State | Meaning | Where the process sits |
|-------|---------|------------------------|
| **New** | The process has just been created and is not yet admitted to compete for the CPU. On most desktops admission is automatic; a real-time system may delay it to avoid overloading itself | Being set up by the kernel |
| **Ready** | It could run right now and is only waiting for a CPU | The **ready queue** (also called the run queue) |
| **Running** | Its instructions are executing on a CPU core. At most one process per core is in this state | On a core |
| **Waiting** (also called **Blocked**) | It cannot continue until something outside it happens: an I/O operation completes, input arrives, a lock becomes available | A queue for that device or event |
| **Terminated** | It has finished (or been killed), but the kernel still holds its exit status until the parent collects it, which is the zombie of [what-is-a-process.md](what-is-a-process.md) | The process table |

Some books use "waiting" for what is called *ready* here, because a ready process is waiting for the CPU. In this module **Ready** always means "could run now" and **Waiting** or **Blocked** means "needs an event first".

### The Six Transitions

| Transition | What causes it | Who decides |
|------------|----------------|-------------|
| New → Ready | The kernel finishes creating the process and admits it | The kernel |
| Ready → Running | The CPU is free and this process is chosen: it is **dispatched** | The **scheduler** |
| Running → Ready | A timer interrupt ends its time slice, or a more important process becomes ready: it is **preempted** | The scheduler |
| Running → Waiting | It asks for something that is not available yet, such as a disk read or `time.sleep` | The process itself, through a system call |
| Waiting → Ready | The awaited I/O completes or the event occurs, typically signalled by an interrupt | The kernel |
| Running → Terminated | It calls `exit`, finishes, or is killed | The process or the kernel |

Notice what is missing. A waiting process never goes straight to running: when its event arrives it becomes *ready* and must wait its turn like every other ready process. And a ready process cannot start itself: only the scheduler can dispatch it. The rules for *which* ready process to choose are the subject of the [CPU Scheduling module](../cpu-scheduling/README.md) of this section.

## 👀 Seeing the States on Your Own Machine

The `ps` command prints each process's state as a letter. The codes differ a little between systems: macOS documents `R` (runnable), `S` (sleeping for less than about 20 seconds), `I` (idle, sleeping for longer than that), `T` (stopped), `U` (uninterruptible wait), and `Z` (zombie); Linux documents `R` (running or runnable), `S` (interruptible sleep), `D` (uninterruptible sleep, usually I/O), `T` (stopped by a job-control signal), `t` (stopped by a debugger), and `Z` (defunct, terminated but not reaped by its parent) ([Linux man page: `ps(1)`](https://man7.org/linux/man-pages/man1/ps.1.html)).

| Textbook state | `ps` letter |
|----------------|-------------|
| Ready or Running | `R`: `ps` does not distinguish between them, because both are "on the run queue" |
| Waiting | `S` (or `I` on macOS): an ordinary wait that a signal can interrupt; `D` (Linux) or `U` (macOS): a wait that cannot be interrupted, usually inside an I/O operation |
| Terminated, not yet collected | `Z` |
| (an extra state) Stopped | `T`: paused by a signal such as `SIGSTOP` (job control, or a debugger) and resumed later by `SIGCONT` |

The next block starts three child processes (one computing in a loop, one sleeping, one that is frozen with `SIGSTOP`) and a fourth that has ended without being waited for, then asks `ps` for each state:

```python
import os
import signal
import subprocess
import sys
import time

def ps_state(pid):
    return subprocess.run(["ps", "-o", "stat=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()[:1]

def wait_for_state(pid, wanted, timeout=3.0):
    deadline = time.time() + timeout
    while time.time() < deadline and ps_state(pid) != wanted:
        time.sleep(0.05)
    return ps_state(pid)

def start(program):
    process = subprocess.Popen([sys.executable, "-c", "print('up', flush=True)\n" + program], stdout=subprocess.PIPE, text=True)
    process.stdout.readline()                       # wait until the interpreter is really running
    return process

busy = start("while True: pass")
sleeper = start("import time; time.sleep(30)")
stopped = start("import time; time.sleep(30)")
os.kill(stopped.pid, signal.SIGSTOP)                # freeze it, as a debugger or Ctrl-Z would
zombie = os.fork()
if zombie == 0:
    os._exit(0)                                     # ends at once; nobody waits for it yet

print("computing in a loop     ->", wait_for_state(busy.pid, "R"), "(runnable)")
print("inside time.sleep       ->", wait_for_state(sleeper.pid, "S"), "(sleeping)")
print("frozen with SIGSTOP     ->", wait_for_state(stopped.pid, "T"), "(stopped)")
print("ended, not yet waited   ->", wait_for_state(zombie, "Z"), "(zombie)")

os.waitpid(zombie, 0)
for process in (busy, sleeper, stopped):
    process.kill()
    process.wait()
    process.stdout.close()
```

```text
computing in a loop     -> R (runnable)
inside time.sleep       -> S (sleeping)
frozen with SIGSTOP     -> T (stopped)
ended, not yet waited   -> Z (zombie)
```

The sleeping process is not consuming the CPU: as shown in [kernel-and-user-mode.md](../introduction-to-operating-systems/kernel-and-user-mode.md), a blocked process is simply not scheduled until the awaited event wakes it. The busy process is the opposite: it is always runnable, so it is either running or waiting in the ready queue, and `ps` cannot tell which.

## 🧪 A Process-State Simulator

To watch processes move through the model, here is a small simulator of one CPU with several processes. Each process is described by a script of alternating CPU bursts and I/O bursts, measured in ticks. The CPU serves the ready queue in order, giving each process a time slice (`quantum`) of at most 2 ticks, which is the **round-robin** policy studied later in this section. I/O devices work independently of the CPU, so any number of processes can wait for I/O at once. The simulator checks every move against the table of legal transitions, so an illegal change would raise an error:

```python
from collections import deque
from enum import Enum

class State(Enum):
    NEW = "new"
    READY = "ready"
    RUNNING = "running"
    WAITING = "waiting"
    TERMINATED = "done"

LEGAL = {                                           # every allowed transition, and what causes it
    (State.NEW, State.READY): "admitted",
    (State.READY, State.RUNNING): "dispatched by the scheduler",
    (State.RUNNING, State.READY): "preempted: its time slice ended",
    (State.RUNNING, State.WAITING): "starts waiting for I/O",
    (State.WAITING, State.READY): "its I/O finished",
    (State.RUNNING, State.TERMINATED): "exits",
}

def simulate(scripts, quantum):
    """scripts maps a process name to a list of ("cpu", ticks) and ("io", ticks) bursts.
    Returns (history, transitions): history[t][name] is the state during tick t;
    transitions lists (tick, name, old state, new state) in the order they happened."""
    bursts = {name: deque([kind, length] for kind, length in script) for name, script in scripts.items()}
    state = {name: State.NEW for name in scripts}
    ready, running, slice_left = deque(), None, 0
    history, transitions = [], []

    def move(name, new_state):
        assert (state[name], new_state) in LEGAL, (name, state[name], new_state)
        transitions.append((len(history), name, state[name], new_state))
        state[name] = new_state

    for name in scripts:                            # every process is admitted at time 0
        move(name, State.READY)
        ready.append(name)

    while any(current is not State.TERMINATED for current in state.values()):
        if running is None and ready:               # the CPU is free: dispatch the head of the ready queue
            running = ready.popleft()
            move(running, State.RUNNING)
            slice_left = quantum
        history.append(dict(state))                 # record who is in which state during this tick

        if running is not None:                     # the running process uses the CPU for one tick
            bursts[running][0][1] -= 1
            slice_left -= 1
        io_finished = []
        for name, current in state.items():         # the devices serve every waiting process for one tick
            if current is State.WAITING:
                bursts[name][0][1] -= 1
                if bursts[name][0][1] == 0:
                    io_finished.append(name)

        if running is not None:                     # what happens to the running process after this tick?
            if bursts[running][0][1] == 0:          # it finished a CPU burst: exit, or wait for the next I/O
                bursts[running].popleft()
                move(running, State.WAITING if bursts[running] else State.TERMINATED)
                running = None
            elif slice_left == 0:                   # its time slice is used up: back to the ready queue
                move(running, State.READY)
                ready.append(running)
                running = None
        for name in io_finished:                    # finished I/O wakes the process up, as ready (never as running)
            bursts[name].popleft()
            move(name, State.READY)
            ready.append(name)

    history.append(dict(state))                     # the final snapshot: everything terminated
    return history, transitions

scripts = {
    "A": [("cpu", 3), ("io", 2), ("cpu", 1)],
    "B": [("cpu", 2), ("io", 3), ("cpu", 2)],
    "C": [("cpu", 4)],
}
history, transitions = simulate(scripts, quantum=2)

print("tick | " + " | ".join(f"{name:^7}" for name in scripts))
for tick, row in enumerate(history):
    print(f"{tick:>4} | " + " | ".join(f"{row[name].value:^7}" for name in scripts))
```

```text
tick |    A    |    B    |    C   
   0 | running |  ready  |  ready 
   1 | running |  ready  |  ready 
   2 |  ready  | running |  ready 
   3 |  ready  | running |  ready 
   4 |  ready  | waiting | running
   5 |  ready  | waiting | running
   6 | running | waiting |  ready 
   7 | waiting |  ready  | running
   8 | waiting |  ready  | running
   9 |  ready  | running |  done  
  10 |  ready  | running |  done  
  11 | running |  done   |  done  
  12 |  done   |  done   |  done  
```

Read the table column by column to follow one process, and row by row to see the whole machine. In every row at most one process is `running`, which is the single-CPU rule. Process A, for example, runs for two ticks, is preempted when its slice ends (it was not finished), waits in the ready queue while B and C take their turns, runs again for the last tick of its first CPU burst, spends two ticks `waiting` for I/O while C is computing, returns to `ready`, waits while B uses its slice, runs its final tick, and is `done`. The simulator also recorded every transition with its cause; the sequence of states of each process is:

```python
for name in scripts:
    path = [State.NEW] + [new for _, who, _, new in transitions if who == name]
    print(f"{name}: " + " -> ".join(state.value for state in path))

print()
for tick, name, old, new in transitions[:8]:
    print(f"tick {tick:>2}: {name} {old.value} -> {new.value}  ({LEGAL[(old, new)]})")
```

```text
A: new -> ready -> running -> ready -> running -> waiting -> ready -> running -> done
B: new -> ready -> running -> waiting -> ready -> running -> done
C: new -> ready -> running -> ready -> running -> done

tick  0: A new -> ready  (admitted)
tick  0: B new -> ready  (admitted)
tick  0: C new -> ready  (admitted)
tick  0: A ready -> running  (dispatched by the scheduler)
tick  2: A running -> ready  (preempted: its time slice ended)
tick  2: B ready -> running  (dispatched by the scheduler)
tick  4: B running -> waiting  (starts waiting for I/O)
tick  4: C ready -> running  (dispatched by the scheduler)
```

The benefit of having several processes shows in the totals. While A and B were waiting for their I/O, C was computing, so the CPU was busy in every tick:

```python
finished_at = len(history) - 1
busy_ticks = sum(1 for row in history if State.RUNNING in row.values())
one_at_a_time = sum(length for script in scripts.values() for _, length in script)
print("ticks until every process was done:        ", finished_at)
print("ticks in which the CPU was running someone:", busy_ticks)
print("the same work done one process at a time:  ", one_at_a_time, "ticks (every I/O wait leaves the CPU idle)")
```

```text
ticks until every process was done:         12
ticks in which the CPU was running someone: 12
the same work done one process at a time:   17 ticks (every I/O wait leaves the CPU idle)
```

That gap, 12 ticks against 17, is the reason multiprogramming exists: a process waiting for I/O costs the CPU nothing, so the kernel runs someone else instead. The simulator was also checked against 5,000 random scripts (up to five processes, random bursts, and random time slices): no more than one process was ever running in a tick, every process ran for exactly as many ticks as its CPU bursts require and waited for exactly as many as its I/O bursts, no time slice was longer than the quantum, the CPU was never idle while a process was ready, and every process eventually terminated.

## 🧩 Beyond Five States

Real kernels refine the model:

- **Swapped-out states.** On systems with virtual memory, a ready or waiting process can be moved out of main memory to disk to free space, giving "swapped out and ready" and "swapped out and waiting" states ([Wikipedia: Process state](https://en.wikipedia.org/wiki/Process_state)). The [Memory Management](../memory-management/README.md) and [Virtual Memory](../virtual-memory/README.md) modules of this section explain the mechanism.
- **Stopped.** Job control (Ctrl-Z in a shell) and debuggers freeze a process with a signal; it is neither ready nor waiting for an event but parked until it is resumed, which is why `ps` has its own `T` letter.
- **Uninterruptible waits.** A process in the middle of certain I/O operations cannot be woken by a signal until the operation finishes, which is what `D` (Linux) and `U` (macOS) mean. A process stuck in such a wait, for example on a failing disk or network file system, may stay in it, immune to signals, until the device responds.
- **Threads have the same states.** The kernel schedules threads, so each thread is individually ready, running, or waiting. A process as a whole is waiting only when all its threads are.

## Common Misconceptions

- **"A process that is not running is stopped or frozen."** In a multiprogrammed system, most processes at any moment are *ready* or *waiting*, and are perfectly healthy. "Stopped" is a separate state that has to be requested.
- **"Waiting and ready are the same thing."** A ready process needs only the CPU; a waiting process needs an event first and cannot use the CPU even if one is free.
- **"`R` in `ps` means the process is executing at this instant."** It means *runnable*: running or in the ready queue. On a busy machine many processes show `R`, and only as many as there are cores are actually executing.
- **"A waiting process wastes CPU time."** It uses none; the kernel does not schedule it until its event arrives.
- **"When I/O finishes, the process resumes immediately."** It becomes ready and must wait for the scheduler to dispatch it (state `waiting` → `ready` → `running`, never straight to running).

## ➡️ Next

Continue to [context-switching.md](context-switching.md): the Running → Ready and Running → Waiting transitions mean the CPU must stop one process and start another, which is the job of the context switch, and which has a cost of its own.
