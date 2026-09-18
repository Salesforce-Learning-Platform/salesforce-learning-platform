# 🌍 Real-World System Design Problems

## 📚 Overview

This final module of the High-Level Design domain applies every concept covered across
[System Design Foundations](../system-design-foundations/),
[Communication and Data Layer](../communication-and-data-layer/),
[Core Infrastructure](../core-infrastructure/), and
[Advanced Distributed Systems Concepts](../advanced-distributed-systems/) to three complete,
structured, interview-style worked examples: a URL Shortener (concluding the running example used
throughout this domain), a Rate Limiter, and a Notification System.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Apply the complete four-step design process to a real, end-to-end system.
- Explain why distributed rate limiting requires shared, centralized state rather than local,
  per-instance counters.
- Design a message-queue-based fan-out architecture for large-scale broadcast delivery.
- Apply idempotency to prevent duplicate side effects when a distributed system's components fail
  and retry.

## 📋 Prerequisites

- Every prior module in the High-Level Design domain — this module applies all of them together, without introducing new concepts.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [designing-a-url-shortener.md](designing-a-url-shortener.md) | The complete, concluded running example: requirements through a deep-dive on the redirect path |
| [designing-a-rate-limiter.md](designing-a-rate-limiter.md) | Why distributed rate limiting needs shared state, and the fail-open-vs-closed trade-off |
| [designing-a-notification-system.md](designing-a-notification-system.md) | Message-queue fan-out, per-channel independence, and idempotent delivery; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** regardless of how much of this domain you've already covered — this module is where
every prior concept gets applied together, which is where real, practical understanding actually
solidifies.

**Skim** only if you've already worked through complete, realistic HLD problems end-to-end
elsewhere — but the notification system's idempotency coverage is worth a look even then, since
it's a commonly underestimated real-world concern.

## 🧠 Knowledge Check

<details>
<summary>Why does a naive, single-instance rate limiter implementation fail once real traffic is distributed across multiple load-balanced servers?</summary>

Each server instance would maintain its own, entirely separate in-memory count — a client could
receive a full allowance of requests from every instance independently, effectively multiplying the
real limit by the number of instances. A shared, centralized store (like Redis) that every instance
reads and writes ensures one true, consistent limit is enforced across the whole distributed system.

</details>

<details>
<summary>Why does the notification system need idempotency checks specifically, given its "at least once" delivery requirement?</summary>

"At least once" delivery means a message might genuinely be redelivered — for instance, if a worker
crashes after sending a notification but before marking it as sent. Without an idempotency check
(verifying a notification ID hasn't already been processed before sending), this redelivery would
cause the same notification to be sent to the user a second time.

</details>

## 📚 References

- Every reference already verified throughout this domain's prior modules — this module applies that content directly rather than introducing new external sources, consistent with the closing module of the Low-Level Design domain.

## ➡️ Continue Your Learning Path

This is the final module of the High-Level Design domain, and completes the System Design domain's
Low-Level and High-Level Design coverage. Continue to Data Structures and Algorithms to build the
problem-solving foundations that complement this domain's architectural thinking.
