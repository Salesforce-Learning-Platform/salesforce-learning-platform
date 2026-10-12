# 📚 Stacks and Queues

## 📚 Overview

A **stack** and a **queue** are collections that restrict where items may be added and removed — and that restriction is exactly what makes them
useful. A stack serves the *most recent* item first (last in, first out) and models function calls, undo history, and nested structure. A queue
serves the *oldest* item first (first in, first out) and models waiting lines, buffers, and scheduling. A **deque** allows both ends. Together they
are the engines of the two basic ways to explore trees and graphs: depth-first search uses a stack, breadth-first search uses a queue.

This module builds stacks and queues several ways, shows why a naïve `list.pop(0)` queue is a performance trap (with measurements), explains how
Python's `collections.deque` is built, and teaches the monotonic stack, a pattern that turns many O(n²) "nearest greater element" problems into
single passes. Every class was tested against a model (a list or `deque`) with tens of thousands of random operations, every algorithm against a brute-force
version on thousands of random inputs, and every benchmark is a real measurement on CPython 3.9.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain LIFO and FIFO behaviour and implement stacks and queues with lists, linked nodes, ring buffers, and pairs of stacks.
- Choose the right Python tool — `list` for stacks, `collections.deque` for queues, `queue.Queue` only for thread-to-thread communication — and explain why.
- Use a stack to match brackets, evaluate and convert arithmetic expressions, and support undo; use a queue for sliding-window counts and breadth-first search.
- Describe how a deque is built, why indexing its middle is slow, and use it for bounded histories and the sliding-window maximum.
- Apply the monotonic-stack pattern to next-greater-element, daily temperatures, stock span, largest rectangle in a histogram, and digit-removal problems, and justify
  their O(n) running time with an amortized argument.

## 📋 Prerequisites

- [Arrays](../arrays/README.md) — lists are the default stack storage, and the cost of shifting explains why `pop(0)` is slow.
- [Linked Lists](../linked-lists/README.md) — linked stacks and queues, and the doubly linked structure underneath `deque`.
- [Time and Space Complexity](../time-and-space-complexity/README.md) — including amortized analysis.
- [Recursion](../recursion/README.md) — the call stack, and replacing recursion with an explicit stack.
- Basic Python reading ability — the examples use Python classes, lists, and `collections.deque`.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [stack-fundamentals.md](stack-fundamentals.md) | LIFO, list and linked-list stacks; bracket matching, postfix evaluation, infix conversion, a min-stack, undo |
| [queue-fundamentals.md](queue-fundamentals.md) | FIFO; why `list.pop(0)` is a trap (measured); linked, ring-buffer, and two-stack queues; hit counting and BFS |
| [deque.md](deque.md) | Both ends in O(1), `maxlen`, the block-linked-list implementation, middle-access cost, the sliding-window maximum |
| [monotonic-stack.md](monotonic-stack.md) | The pattern and six problems with brute-force verification; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [monotonic-stack.md](monotonic-stack.md) and the sliding-window maximum in [deque.md](deque.md) if you are preparing for coding interviews:
"next greater element" and "largest rectangle in a histogram" are famous problems whose O(n) solutions come from the same idea, and being able to
explain the amortized O(n) bound is a frequent follow-up. Also work through the infix-to-postfix and two-stack-queue sections, which are standard
design questions.

**Skim** [stack-fundamentals.md](stack-fundamentals.md) and [queue-fundamentals.md](queue-fundamentals.md) if you already use stacks and queues daily — but read
the measured `pop(0)` comparison, which is the most common avoidable performance bug in Python code that processes queues.

## 🧠 Knowledge Check

<details>
<summary>Why does evaluating <code>10 - 4 - 3</code> with a stack-based infix-to-postfix converter require popping operators of <em>equal</em> precedence, and what goes wrong if you pop only strictly higher precedence?</summary>

Subtraction is left-associative: `10 - 4 - 3` means `(10 - 4) - 3 = 3`. When the second `-` arrives, the first `-` is already on the
operator stack and must be applied **before** the second one, so it must be popped to the output first — which means popping operators of equal
precedence, not just higher. If you pop only strictly higher precedence, the first `-` stays on the stack, and the output becomes `10 4 3 - -`, which
evaluates as `10 - (4 - 3) = 9`: the wrong answer. See [stack-fundamentals.md](stack-fundamentals.md).

</details>

<details>
<summary>The monotonic-stack solution to "next greater element" has a <code>while</code> loop nested inside a <code>for</code> loop. Why is it O(n) rather than O(n²)?</summary>

Each index is pushed onto the stack exactly once and popped at most once. The inner `while` loop only executes when it pops, so over the entire run
it performs at most `n` iterations *in total*, not `n` per outer iteration. The outer loop does `n` iterations plus the inner loop's total of at most `n`
pops, so the whole function does O(n) work. This is the same amortized argument used for sliding windows and for the monotonic deque in the
sliding-window maximum. See [monotonic-stack.md](monotonic-stack.md).

</details>

## 📚 References

- [Python docs: `collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque) — the double-ended queue, `maxlen`, `rotate`, and the complexity notes.
- [Python docs: `queue`](https://docs.python.org/3/library/queue.html) — thread-safe queues, and the tutorial's note on [using lists as queues](https://docs.python.org/3/tutorial/datastructures.html#using-lists-as-queues).
- [Wikipedia: Shunting-yard algorithm](https://en.wikipedia.org/wiki/Shunting_yard_algorithm) and [Reverse Polish notation](https://en.wikipedia.org/wiki/Reverse_Polish_notation) — the expression conversion and evaluation used in the stack file.
- [Wikipedia: Circular buffer](https://en.wikipedia.org/wiki/Circular_buffer) — the ring-buffer queue.
- [W3Schools: DSA Stacks](https://www.w3schools.com/dsa/dsa_data_stacks.php) and [DSA Queues](https://www.w3schools.com/dsa/dsa_data_queues.php) — beginner-friendly illustrated introductions.
- [GeeksforGeeks: Stack Data Structure](https://www.geeksforgeeks.org/dsa/stack-data-structure/), [Queue Data Structure](https://www.geeksforgeeks.org/dsa/queue-data-structure/), and [Monotonic Stack](https://www.geeksforgeeks.org/dsa/introduction-to-monotonic-stack-data-structure-and-algorithm-tutorials/) — overviews and practice problems.

## ➡️ Continue Your Learning Path

Continue to the [Trees](../trees/README.md) module, the next module in this domain, where data is organized hierarchically — and where stacks and queues
become the two engines of traversal: depth-first and breadth-first.
