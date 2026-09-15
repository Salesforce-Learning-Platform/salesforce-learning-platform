# 🪟 What Is a Context Window, and Why Prompts Get Cut

## The Model's "Working Memory," Not Its Training Data

The **context window** is the total amount of text — measured in [tokens](what-are-tokens-and-why-everything-becomes-tokens.md) —
a model can actually look back on and reference at once when generating a response. This is
explicitly distinct from the enormous corpus of data a model was originally *trained* on: the
context window is closer to a genuine "working memory," holding only what's actually present in
the current conversation or request, not the model's entire trained knowledge.

## Everything Counts Against the Same Limit

```
context window budget = system prompt tokens
                       + conversation history tokens
                       + the current user message tokens
                       + the model's OWN response tokens
```

A context window isn't just "how long a single message can be" — it's the **total** budget shared
across the entire conversation so far, the current prompt, and the response the model is about to
generate. A long, multi-turn conversation genuinely consumes real context window budget with every
turn, not just the newest message.

## What Happens When It's Exceeded

A request that would exceed the model's context window can't simply be silently ignored — either
the request is rejected outright, or (more commonly, in an application built on top of the API)
older conversation history has to be deliberately trimmed, summarized, or dropped before sending a
new request, since the model genuinely cannot process more tokens than its context window allows.

## Why a Larger Context Window Isn't Simply "Better" in Every Way

```
LARGER context window: can process longer documents, longer
conversations, more retrieved context (per RAG, later in this domain)

But: more tokens sent also means MORE COST (billed per token, per
calling-llm-apis-properly) and can mean SLOWER responses
```

A larger context window genuinely enables handling longer documents and longer conversations
without truncation — but sending more tokens is not free: it costs more (per
[calling-llm-apis-properly](../calling-llm-apis-properly/)'s token-based pricing) and can increase
response latency. A real application deliberately manages what actually goes into the context
window, rather than always sending everything available just because the window is large enough to
technically fit it.

## Why Long Conversations Can Feel Like the Model "Forgets"

Once a conversation's total token count approaches the context window's limit, something has to
give — older messages get trimmed or summarized to make room for new ones. This is exactly why a
very long conversation can start to feel like the model has "forgotten" something discussed much
earlier: that earlier content may have genuinely fallen outside the current context window, not
because the model chose to ignore it.

## Common Mistakes

- Assuming the context window represents the model's total trained knowledge — it's specifically
  the current conversation/request's working memory, a much smaller and entirely different thing.
- Sending an unnecessarily large amount of context "just in case," incurring real, avoidable cost
  and latency for information the current request doesn't actually need.
- Being surprised when a long-running conversation seems to lose track of something discussed much
  earlier — that's very often the context window's real, physical limit, not an unexplained bug.

## ➡️ Next

Continue to
[sampling-basics-temperature-and-randomness-control.md](sampling-basics-temperature-and-randomness-control.md)
to see how a model actually chooses which token to generate next.
