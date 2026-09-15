# 📡 Calling LLM APIs Properly

## Purpose

[How LLMs Actually Work](../how-llms-actually-work/) covered the concepts underneath an LLM.
This module covers actually **calling** one in real, production code — structuring a request
correctly, understanding what you're being billed for, and handling the real, inevitable failure
modes (rate limits, timeouts) any API-dependent application eventually hits.

## 🎯 Learning Objectives

- Structure a Messages API request correctly using system, user, and assistant roles.
- Explain what drives real API cost, and why a poorly-written prompt can waste real money.
- Plan for a request/response's token budget, avoiding overflow.
- Handle a `429` rate-limit error correctly, with retries and backoff.

## 📋 Prerequisites

- [How LLMs Actually Work](../how-llms-actually-work/) — this module assumes tokens, context
  windows, and the probabilistic nature of LLM output are already understood.

## 📂 Files in This Module

| File | Covers |
|---|---|
| [message-roles-system-user-assistant.md](message-roles-system-user-assistant.md) | Structuring a request with system, user, and assistant roles |
| [cost-awareness-pricing-per-token-and-why-bad-prompts-waste-money.md](cost-awareness-pricing-per-token-and-why-bad-prompts-waste-money.md) | Per-token pricing, and how a poorly-designed prompt directly costs real money |
| [token-budgeting-prompt-size-response-size-and-overflow-planning.md](token-budgeting-prompt-size-response-size-and-overflow-planning.md) | Planning for prompt size, response size, and context window overflow |
| [rate-limits-handling-429-backoff-and-retries.md](rate-limits-handling-429-backoff-and-retries.md) | Handling `429` errors correctly, with exponential backoff |

## 🔍 When to Deep-Dive vs. Skim

Deep-dive
[rate-limits-handling-429-backoff-and-retries.md](rate-limits-handling-429-backoff-and-retries.md) —
any real application calling an LLM API in production will eventually hit a rate limit, and
handling it correctly (rather than crashing or hammering the API with immediate retries) is a
genuine production-readiness requirement, not an edge case.

## ✅ Quick Knowledge Check

<details>
<summary>Is "system" a message role that goes inside the messages array, alongside "user" and "assistant"?</summary>

Not for the Claude API specifically — the system prompt is provided through its own separate,
top-level `system` parameter, while the `messages` array itself only ever alternates between
`user` and `assistant` roles. See
[message-roles-system-user-assistant.md](message-roles-system-user-assistant.md).

</details>

<details>
<summary>If a request gets a 429 error, is it safe to immediately retry it as fast as possible?</summary>

No — immediately hammering a rate-limited endpoint with retries makes the problem worse. The
correct approach is exponential backoff, honoring the `retry-after` header the API returns, which
tells you exactly how long to actually wait. See
[rate-limits-handling-429-backoff-and-retries.md](rate-limits-handling-429-backoff-and-retries.md).

</details>

## 📚 References

- Anthropic, [Messages API](https://platform.claude.com/docs/en/api/messages)
- Anthropic, [Rate limits](https://platform.claude.com/docs/en/api/rate-limits)
- Anthropic, [Claude API errors](https://platform.claude.com/docs/en/api/errors)

## ➡️ Continue Your Learning Path

Continue to the [Prompt Engineering Fundamentals module](../prompt-engineering-fundamentals/) to
write genuinely effective prompts, not just correctly-structured API requests.
