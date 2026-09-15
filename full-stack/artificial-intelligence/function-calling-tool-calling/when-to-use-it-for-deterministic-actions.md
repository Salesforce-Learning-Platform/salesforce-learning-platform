# ⚙️ When to Use It for Deterministic Actions

## The Core Rule: Determinism Belongs in Code

```
"What's 4,839,201 × 88,432?"  → a calculator TOOL, not the model's
                                  own arithmetic

"Cancel order #48213"          → a real cancelOrder() function TOOL,
                                  never text the model merely CLAIMS
                                  to have done

"Summarize this support
 ticket"                        → the model's own generation — no
                                  tool needed at all
```

An LLM is fundamentally a probabilistic text generator (per
[deterministic-vs-probabilistic-outputs.md](../how-llms-actually-work/deterministic-vs-probabilistic-outputs.md)).
For anything that must be **exactly correct, every single time** — arithmetic, a database write, an
API call with real consequences — the actual operation belongs in ordinary, deterministic code,
triggered *through* a tool call rather than attempted directly by the model's own generation.

## A Concrete Test: "Could This Be Wrong and Still Look Right?"

```
Model does arithmetic directly in text     → can produce a
                                              confident-looking WRONG
                                              number

Model calls a `calculate` tool that runs
real code                                   → the number is either
                                              exactly right, or the
                                              tool call itself fails
                                              loudly
```

A wrong number generated directly in text is a genuinely dangerous failure mode — it looks
identical to a correct one. Routing the actual computation through a real function eliminates this
specific risk entirely: the tool either returns the mathematically correct answer, or it doesn't
return one at all.

## Real, Consequential Actions Always Go Through a Tool

```python
tools = [{
    "name": "cancel_order",
    "description": "Cancel a customer's order by order ID. This is irreversible.",
    "input_schema": {
        "type": "object",
        "properties": {"order_id": {"type": "string"}},
        "required": ["order_id"],
    },
}]
```

An action with a real, sometimes irreversible effect — canceling an order, sending an email,
charging a card — should **never** be something the model merely narrates having done in plain
text. It must always be a genuine tool call, executed by real application code that can enforce
its own checks (authorization, confirmation, logging) independent of anything the model says.

## When a Tool Call Isn't Needed at All

```
Summarizing a document, drafting an email, answering a general
knowledge question, brainstorming ideas
→ no external action or lookup needed — plain generation is
  correct and appropriate here
```

Not every request needs a tool. Reaching for tool calling on a task that's really just generation
adds unnecessary latency (an extra round trip) and complexity for no real benefit — the deciding
question is always whether the task genuinely needs a real action or a piece of real, current
information the model doesn't already have.

## A Simple Decision Framework

```
Does this need EXACT correctness (math, exact data)?        → tool
Does this have a REAL, external effect (write, send, charge)? → tool
Does this need CURRENT information the model can't know?     → tool
None of the above?                                            → plain generation
```

Running through these questions for a given feature is usually enough to decide whether tool
calling is the right mechanism, before writing a single tool definition.

## Common Mistakes

- Letting the model perform exact arithmetic or generate exact structured data (like an ID or a
  price) directly in text when a deterministic tool call would guarantee correctness instead.
- Reaching for a tool call on a purely generative task that never needed one, adding latency and
  complexity without any real benefit.
- Building a tool for a real, consequential action but skipping the application-level checks
  (authorization, confirmation) that real code should always enforce independently of the model.

## ➡️ Next

Continue to [hybrid-logic-ai-and-code.md](hybrid-logic-ai-and-code.md) to see how deterministic
tool calls and the model's own reasoning combine in a single, realistic feature.
