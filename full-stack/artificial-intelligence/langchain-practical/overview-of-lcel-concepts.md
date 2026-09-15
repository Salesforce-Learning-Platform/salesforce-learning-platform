# ⛓️ Overview of LCEL Concepts

## Formalizing What's Already Been Used

Every prior file in this module used the `|` operator informally —
[building-chains-and-prompt-templates.md](building-chains-and-prompt-templates.md)'s
`prompt | llm | StrOutputParser()` is the clearest example. This file explains exactly what makes
that syntax work: **LCEL**, the **LangChain Expression Language**.

## `Runnable` — the Shared Interface Behind the `|` Operator

```
EVERY LangChain component that can appear in a chain - prompts,
models, parsers, retrievers, even a custom function - implements
the SAME interface: .invoke(), .stream(), .batch()

This shared interface is called a RUNNABLE.
```

The `|` operator works specifically because both sides are `Runnable`s — Python's `__or__` method
is overloaded so that `a | b` produces a new `Runnable` (a `RunnableSequence`) that calls `a`, then
passes its output as `b`'s input. This is the entire mechanism behind the chains built throughout
this module — no special parsing, just an ordinary Python operator overload applied consistently
across every component type.

## Every Runnable Gets Streaming and Batching for Free

```python
chain = prompt | llm | StrOutputParser()

for chunk in chain.stream({"document_type": "ticket", "sentence_count": "2", "content": "..."}):
    print(chunk, end="", flush=True)  # the SAME streaming concept from Streaming AI Responses

results = chain.batch([
    {"document_type": "ticket", "sentence_count": "2", "content": text_1},
    {"document_type": "ticket", "sentence_count": "2", "content": text_2},
])
```

Because every component in a chain shares the `Runnable` interface, `.stream()` — the same
underlying idea as [Streaming AI Responses](../streaming-responses/), now applied across an entire
composed chain rather than a single model call — and `.batch()` (running the same chain across many
inputs) work automatically, without any extra code specific to streaming or batching.

## `RunnableParallel` — Running Steps Concurrently

```python
from langchain_core.runnables import RunnableParallel

parallel_chain = RunnableParallel(
    summary=summary_chain,
    sentiment=sentiment_chain,
)
result = parallel_chain.invoke({"content": ticket_text})
# result == {"summary": "...", "sentiment": "negative"}
```

`RunnableParallel` runs multiple chains concurrently against the same input and combines their
results into one dictionary — this is LCEL's direct expression of the **parallelization** pattern
already introduced in
[Agent Design Patterns](../agent-design-patterns/), specifically the "sectioning" variant: independent
subtasks, run simultaneously, then combined.

## `RunnableLambda` — Dropping Into Plain Python

```python
from langchain_core.runnables import RunnableLambda

def clean_input(data):
    return {**data, "content": data["content"].strip()}

chain = RunnableLambda(clean_input) | prompt | llm
```

`RunnableLambda` wraps an ordinary Python function so it can participate in a chain like any other
component — genuinely useful for a small transformation step (cleaning input, reshaping a
dictionary) that doesn't need its own dedicated LangChain class.

## Why LCEL's Design Choice Matters in Practice

```
A HAND-WRITTEN pipeline: streaming, batching, and async support
  each need to be implemented separately for every new chain

An LCEL chain: gets streaming, batching, AND async support
  automatically, just from composing Runnables with `|`
```

This is the actual, practical payoff of LCEL's design: the uniform `Runnable` interface means a
capability like streaming doesn't need to be re-implemented for every new chain — it comes for free
from the interface every component already implements.

## Common Mistakes

- Writing a custom Python function that isn't wrapped in `RunnableLambda` and trying to `|` it
  directly into a chain, which fails since it doesn't implement the `Runnable` interface.
- Reaching for `RunnableParallel` for steps that actually depend on each other's output, when they
  need to run sequentially (a plain `|` chain) instead.
- Assuming LCEL's chain composition replaces the need for the validation and error-handling
  discipline from earlier in this domain — a chain composes steps together, it doesn't add
  [Zod-equivalent](../schema-validation-with-zod/) validation or retry logic on its own.

## Module Summary

Across this module: **LangChain** is a framework built on top of provider APIs (like Anthropic's),
providing reusable abstractions for patterns this domain already covered from first principles (see
[introduction-to-langchain.md](introduction-to-langchain.md)); **chains and prompt templates**
combine a `ChatPromptTemplate`, a chat model, and an output parser into a reusable, composable unit
using the `|` operator (see
[building-chains-and-prompt-templates.md](building-chains-and-prompt-templates.md)); **tools and
memory** use `@tool` and `bind_tools()` (LangChain's wrapper around the same `tool_use`/`tool_result`
contract) plus `RunnableWithMessageHistory` for persistent, session-based conversation history (see
[using-tools-and-memory-modules.md](using-tools-and-memory-modules.md)); **agents**, via
`create_agent`, are LangChain's own tested implementation of the exact agentic loop from
Understanding AI Agents — "Agent = Model + Harness" (see
[working-with-agents.md](working-with-agents.md)); and **LCEL** — the `Runnable` interface behind
the `|` operator — is what gives every chain, regardless of what it composes, streaming, batching,
and parallel execution for free.
