# 📊 Token Budgeting: Prompt Size, Response Size, Overflow Planning

## The Real Budget Equation

```
context window budget ≥ system prompt tokens
                       + conversation history tokens
                       + current message tokens
                       + max_tokens (the response's own budget)
```

Recall [what-is-a-context-window-and-why-prompts-get-cut.md](../how-llms-actually-work/what-is-a-context-window-and-why-prompts-get-cut.md):
the context window is a **shared** budget across the entire request, including the response the
model is about to generate. A real application needs to actively plan for this total, not just the
size of the message it's currently sending.

## Setting `max_tokens` Deliberately

```json
{
  "model": "claude-sonnet-5",
  "max_tokens": 1024,
  "messages": [{ "role": "user", "content": "Summarize this article in 3 sentences." }]
}
```

`max_tokens` caps how many tokens the response is allowed to generate — set too low, and a genuine,
useful response gets cut off mid-sentence before it's actually finished; set unnecessarily high
"just in case," and (per
[cost-awareness-pricing-per-token-and-why-bad-prompts-waste-money.md](cost-awareness-pricing-per-token-and-why-bad-prompts-waste-money.md))
there's no direct cost penalty for the cap itself, but it does directly affect how much of the
context window's budget is reserved for the response.

## Planning for a Growing Conversation

```js
function estimateTokens(text) {
  return Math.ceil(text.length / 3.5); // Claude's rough characters-per-token average
}

function trimHistoryIfNeeded(history, maxHistoryTokens) {
  let totalTokens = history.reduce((sum, msg) => sum + estimateTokens(msg.content), 0);
  while (totalTokens > maxHistoryTokens && history.length > 2) {
    const removed = history.shift(); // drop the OLDEST messages first
    totalTokens -= estimateTokens(removed.content);
  }
  return history;
}
```

A real, long-running conversation genuinely needs a deliberate strategy for what happens as it
approaches the context window's limit — a common, practical approach trims or summarizes the
**oldest** messages first, preserving the most recent, most relevant context while staying within
budget.

## Planning for Documents Larger Than the Context Window

```
A 500-page document simply CANNOT fit inside even a large context
window at once — the application needs a deliberate strategy:
chunking the document, summarizing sections, or (per RAG, later in
this domain) retrieving only the specifically relevant portions.
```

Some real inputs are simply too large to ever fit in a single request, regardless of context
window size — this is exactly the problem
[Building a RAG Pipeline](../building-a-rag-pipeline/), covered later in this domain, is built to
solve: retrieving only the specifically relevant portion of a much larger document, rather than
attempting to send the entire thing.

## Estimating Tokens Before Sending

Recall [what-are-tokens-and-why-everything-becomes-tokens.md](../how-llms-actually-work/what-are-tokens-and-why-everything-becomes-tokens.md)'s
rough characters-per-token ratio — while an approximation, it's genuinely useful for a quick,
practical estimate of whether a given prompt is likely to fit comfortably within budget, before
actually sending the request and finding out the hard way.

## Common Mistakes

- Setting `max_tokens` far higher than a task genuinely needs "just to be safe," unnecessarily
  reserving context window budget that could otherwise hold more actual conversation history.
- Letting a long-running conversation grow without any trimming strategy at all, eventually hitting
  a hard failure once the context window is genuinely exceeded.
- Assuming any document, regardless of size, can simply be pasted directly into a prompt — some
  inputs genuinely require chunking, summarization, or retrieval instead.

## ➡️ Next

Continue to
[rate-limits-handling-429-backoff-and-retries.md](rate-limits-handling-429-backoff-and-retries.md)
to handle the real, inevitable failure mode of calling any API at genuine production scale.
