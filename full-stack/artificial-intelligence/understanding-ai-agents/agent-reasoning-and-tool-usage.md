# 🔄 Agent = Reasoning + Tool Usage

## The Agentic Loop, Concretely

```python
messages = [{"role": "user", "content": "Find out if order #4821 has shipped, and if not, cancel it."}]

while True:
    response = client.messages.create(
        model="claude-opus-5", max_tokens=1024, tools=tools, messages=messages,
    )
    messages.append({"role": "assistant", "content": response.content})

    if response.stop_reason != "tool_use":
        break  # the model is done — it produced a final answer

    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            result = execute_tool(block.name, block.input)  # your real implementation
            tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})

    messages.append({"role": "user", "content": tool_results})

final_answer = next(b.text for b in response.content if b.type == "text")
```

This `while` loop, keyed on `stop_reason`, is the exact mechanism from Anthropic's own tool-use
documentation — and it's the entire technical definition of "an agent" in this narrow, precise
sense: the model calls a tool, gets a result, decides whether it needs to call another tool or
another one after that, and only stops the loop itself once it has what it needs.

## Walking Through the Example

```
Turn 1: model calls look_up_order(order_id="4821")
        → tool_result: {"status": "processing", "shipped": false}

Turn 2: model REASONS about that result — "not shipped, so I
        should cancel it" — and calls cancel_order(order_id="4821")
        → tool_result: {"success": true}

Turn 3: stop_reason is NOT "tool_use" anymore — the model
        produces a final text answer: "Order #4821 hadn't
        shipped, so I've canceled it."
```

Neither tool call was hard-coded by the application — the model decided, based on the *result* of
the first tool call, whether a second one was even necessary. This is the "reasoning" half of
"reasoning + tool usage": each step's decision depends on what the *previous* step actually
returned, not on a sequence the application predetermined.

## `stop_reason` Values That End the Loop

```
"end_turn"      → the model produced a final answer; done
"max_tokens"    → the response was cut off by a token limit; NOT
                   genuinely done — needs its own handling
"stop_sequence" → a configured stop sequence was hit
"refusal"       → the model declined to continue; NOT genuinely done
"tool_use"      → the ONLY value that means "keep looping"
```

Correctly distinguishing these matters — treating every non-`"tool_use"` stop reason as "the agent
is finished" would silently treat a genuine `max_tokens` truncation or a refusal as a successful
completion, when neither one actually is.

## An Upper Bound on Iterations — Always

```python
MAX_AGENT_ITERATIONS = 10

for iteration in range(MAX_AGENT_ITERATIONS):
    # ... the loop body from above
    if response.stop_reason != "tool_use":
        break
else:
    raise AgentIterationLimitExceeded("Agent did not converge within the iteration limit.")
```

Exactly like [the retry ceilings covered earlier in this domain](../error-handling-in-ai-applications/implementing-retry-mechanisms.md),
an agentic loop needs a firm maximum iteration count. Without one, a model stuck reasoning in
circles — calling the same tool repeatedly without making genuine progress — could loop
indefinitely, at real, accumulating token cost.

## Common Mistakes

- Treating any `stop_reason` other than `"tool_use"` as success, silently mishandling a genuine
  `max_tokens` truncation or `refusal`.
- Running an agentic loop with no maximum iteration count, risking unbounded cost if the model
  never genuinely converges on a final answer.
- Re-implementing this loop from scratch for every new agent feature instead of extracting it into
  one, well-tested, reusable function.

## ➡️ Next

Continue to
[when-to-use-multi-agent-systems-and-when-not-to.md](when-to-use-multi-agent-systems-and-when-not-to.md)
to see when a single agent like this is enough, and when genuinely multiple, coordinating agents
are worth the added complexity.
