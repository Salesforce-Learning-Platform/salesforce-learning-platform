# The JavaScript Event Loop

## Purpose

[Asynchronous Programming and Modules](../asynchronous-programming-and-modules/) covered *how* to
write async code. This module explains the mechanism underneath it: how JavaScript — a
single-threaded language — manages to run non-blocking asynchronous operations at all, without
ever running two pieces of JavaScript at the exact same instant.

## Learning Objectives

- Explain the call stack, and why a long-running synchronous function blocks everything else.
- Explain what Web APIs handle on JavaScript's behalf, outside the call stack.
- Explain the callback queue and how the event loop decides what runs next.
- Explain the distinction between microtasks and macrotasks, and predict execution order.

## Prerequisites

[Asynchronous Programming and Modules](../asynchronous-programming-and-modules/).

## Files in This Module

| File | Covers |
|---|---|
| [call-stack.md](call-stack.md) | How JavaScript tracks function execution, and why it's single-threaded |
| [web-apis.md](web-apis.md) | What handles timers, network requests, and DOM events off the call stack |
| [callback-queue.md](callback-queue.md) | How completed async work gets back onto the call stack |
| [microtasks-and-macrotasks.md](microtasks-and-macrotasks.md) | Two separate queues, and why Promises consistently run before `setTimeout` |

## When to Deep-Dive vs. Skim

Deep-dive [microtasks-and-macrotasks.md](microtasks-and-macrotasks.md) — this is the piece that
actually explains puzzling execution-order questions ("why does this Promise log before this
`setTimeout(fn, 0)`") that are otherwise easy to memorize as trivia without understanding.

## Quick Knowledge Check

<details>
<summary>Why does a single infinite loop freeze an entire web page, including its UI?</summary>

JavaScript is single-threaded — one call stack. A function that never returns keeps that one
thread permanently occupied, so nothing else (including UI updates and other JavaScript) can run
until it finishes. See [call-stack.md](call-stack.md).

</details>

<details>
<summary>Between a resolved Promise's `.then()` and a `setTimeout(fn, 0)`, which runs first?</summary>

The Promise's `.then()` callback — microtasks (Promise callbacks) are fully drained before the
event loop processes the next macrotask (`setTimeout` callbacks), regardless of the requested
delay. See [microtasks-and-macrotasks.md](microtasks-and-macrotasks.md).

</details>

## References

- MDN Web Docs, [JavaScript execution model](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Execution_model)

## Continue Your Learning Path

Next: [JavaScript Object-Oriented Programming](../object-oriented-programming/) — see the
[Frontend learning path](../../README.md) for the full sequence.
