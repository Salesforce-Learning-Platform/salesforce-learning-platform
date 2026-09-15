# 🤖 Agent vs. a Single LLM Call

## Everything So Far Has Been a Single Call

Every technique covered up to this point in this domain — even a
[tool call](../function-calling-tool-calling/), even a [RAG pipeline](../building-a-rag-pipeline/) —
has been, fundamentally, **one request, one response**: the application decides what to do next.
An **agent** is a genuinely different shape: the model itself decides what to do next, repeatedly,
without the application dictating each individual step in advance.

## Workflows vs. Agents — Anthropic's Own Distinction

```
WORKFLOW → LLMs and tools orchestrated through PREDEFINED code
           paths — the application decides the sequence of steps
           in advance

AGENT     → the LLM DYNAMICALLY directs its own process and tool
           usage — the model itself decides what to do next, and
           when it's actually done
```

This is a real, important distinction from Anthropic's own engineering guidance on building
effective agents: a workflow is still code-driven, even if an LLM call is one of its steps. An
agent hands genuine control over the *sequence* of actions to the model itself.

## A Concrete Comparison

```python
# WORKFLOW — the code decides the fixed sequence
def process_support_ticket(ticket):
    category = classify(ticket)          # step 1, always runs
    if category == "refund":
        return handle_refund(ticket)      # step 2a, code-decided branch
    return escalate_to_human(ticket)      # step 2b, code-decided branch

# AGENT — the MODEL decides what to do, and in what order
response = client.messages.create(
    model="claude-opus-5", max_tokens=1024,
    tools=[classify_tool, refund_tool, escalate_tool, look_up_order_tool],
    messages=[{"role": "user", "content": ticket.text}],
)
# The model itself decides: look up the order first? classify first?
# call multiple tools? ask a clarifying question instead? — none of
# this sequence is fixed by the application code.
```

The workflow version is entirely predictable — the same category always leads to the same code
path. The agent version gives the model genuine latitude over which tools to call, in what order,
and how many times, based on its own reasoning about the specific ticket in front of it.

## Why This Distinction Matters for Real Design Decisions

```
Workflow strengths: predictable, easy to test exhaustively, cheaper
  (fewer, more targeted LLM calls), easy to reason about failure
  modes

Agent strengths: handles genuinely open-ended, unpredictable
  problems where the right sequence of steps can't be known in
  advance
```

Neither shape is universally "better" — they solve different problems. A workflow is the right
choice whenever the actual steps genuinely are predictable and fixed; an agent earns its added
complexity and cost specifically when the problem's shape is too open-ended for a fixed sequence to
handle well. [when-to-use-multi-agent-systems-and-when-not-to.md](when-to-use-multi-agent-systems-and-when-not-to.md),
later in this module, returns to this trade-off in more depth.

## Common Mistakes

- Calling any feature that uses an LLM at all "an agent," blurring the genuinely useful distinction
  between a fixed workflow and a model directing its own steps.
- Reaching for an agent's added complexity and cost for a task that's actually entirely predictable
  and would be simpler, cheaper, and more testable as a plain workflow.
- Assuming an agent is always "smarter" than a workflow — a well-designed workflow often
  outperforms an agent on exactly the kind of task it was built for.

## ➡️ Next

Continue to
[agent-reasoning-and-tool-usage.md](agent-reasoning-and-tool-usage.md) to see the actual mechanism
— the agentic loop — that lets a model direct its own steps like this.
