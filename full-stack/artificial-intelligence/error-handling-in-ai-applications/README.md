# 🩺 Error Handling in AI Applications

## 📚 Overview

Several earlier modules each introduced their own piece of error handling — validation retries in
[Schema Validation with Zod](../schema-validation-with-zod/), rate-limit backoff in
[Calling LLM APIs Properly](../calling-llm-apis-properly/), mid-stream errors in
[Streaming AI Responses](../streaming-responses/). This module brings those pieces together into
one coherent, application-wide error-handling strategy, and fills in the remaining gaps: malformed
JSON recovery, timeouts, a unified retry layer, and the logging discipline that makes AI failures —
often non-reproducible by nature — genuinely diagnosable after the fact.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Build a pipeline that safely parses and recovers from malformed AI JSON output.
- Handle timeouts and partial/mid-stream failures, preferring streaming for long-running requests.
- Combine the SDK's built-in infrastructure retries with application-level retry logic for
  validation failures, behind a single, firm attempt ceiling.
- Design a structured, consistent AI request/response logging discipline that turns rare,
  hard-to-reproduce failures into an actionable signal.

## 📋 Prerequisites

- [Schema Validation with Zod](../schema-validation-with-zod/) — this module's retry and validation-failure handling builds directly on it.
- [Calling LLM APIs Properly](../calling-llm-apis-properly/) — familiarity with rate-limit backoff, extended here to the broader infrastructure-failure category.
- [Streaming AI Responses](../streaming-responses/) — mid-stream error handling builds on this module's UX patterns.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [handling-invalid-or-malformed-json-responses.md](handling-invalid-or-malformed-json-responses.md) | Safe parsing, recovering from common wrapping artifacts, distinguishing failure types |
| [managing-partial-responses-and-timeouts.md](managing-partial-responses-and-timeouts.md) | Timeouts, mid-stream errors, and why streaming is safer for long requests |
| [implementing-retry-mechanisms.md](implementing-retry-mechanisms.md) | Combining SDK-level and application-level retries behind a firm ceiling |
| [logging-ai-requests-and-responses-for-debugging.md](logging-ai-requests-and-responses-for-debugging.md) | Structured, consistent logging that makes AI failures diagnosable |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you're building or operating a production AI feature — this module is the
capstone that ties every other error-handling concept in this domain into one coherent strategy.

**Skim** if you've already internalized the individual pieces from Schema Validation with Zod,
Calling LLM APIs Properly, and Streaming AI Responses — this module's core value is in how they
combine, more than any single new technique.

## 🧠 Knowledge Check

<details>
<summary>Why might an application still need its own retry logic even though the official SDKs already retry transient failures automatically?</summary>

The SDK's automatic retries cover infrastructure-level failures (connection errors, rate limits,
5xx server errors). A validation failure — a response that arrived successfully but doesn't match
the expected schema — is a structurally different problem the SDK has no way to detect, so it
always needs application-level retry handling, ideally feeding the specific validation errors back
into the next prompt.

</details>

<details>
<summary>Why does an AI request/response log need a different discipline than a typical application error log?</summary>

An AI failure is often not reproducible — a model's probabilistic nature means the exact same
prompt can succeed most of the time and fail only occasionally. A thorough, structured log (with a
request ID, a clear failure-category taxonomy, and careful handling of sensitive content) may be
the only record of a failure that never happens again, making it far more valuable here than for a
typical, reliably-reproducible application bug.

</details>

## 📚 References

- [Anthropic - Claude API Errors](https://platform.claude.com/docs/en/api/errors) — official documentation for HTTP error codes, error shapes, request IDs, and SDK retry behavior
- [Anthropic - Streaming Messages: Error Events](https://platform.claude.com/docs/en/build-with-claude/streaming#error-events) — the shape of a mid-stream error
- [W3Schools - JSON Introduction](https://www.w3schools.com/js/js_json_intro.asp) — a refresher on JSON parsing and common syntax pitfalls

## ➡️ Continue Your Learning Path

Continue to [Understanding Embeddings](../understanding-embeddings/) to move from generation-based
AI techniques into the retrieval-based foundations used for search, RAG, and semantic matching.
