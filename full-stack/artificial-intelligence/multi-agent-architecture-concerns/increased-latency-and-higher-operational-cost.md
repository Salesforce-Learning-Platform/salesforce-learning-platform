# 💸 Increased Latency and Higher Operational Cost

## The Costs Named, Not Just Mentioned

[when-to-use-multi-agent-systems-and-when-not-to.md](../understanding-ai-agents/when-to-use-multi-agent-systems-and-when-not-to.md)
listed cost, latency, and complexity as real trade-offs of a multi-agent architecture. This module
examines each of these in genuine depth — starting with the two most immediately measurable:
latency and operational cost.

## Latency: Every Agent Boundary Is a Round Trip

```
A SINGLE agent handling "research and write a report":
  N tool calls + 1 final generation ≈ N+1 round trips

TWO SEPARATE agents (researcher, then writer):
  N tool calls (researcher) + 1 research summary generation +
  1 writer generation + the LATENCY of handing off between them
  ≈ N+2 round trips, PLUS coordination overhead
```

Each agent boundary in a multi-agent system adds at least one more full model round trip beyond
what a single agent doing the same work would need — and in a genuinely sequential pipeline (like
[the researcher-writer pattern](../agent-design-patterns/researcher-to-writer-pattern.md)), these
round trips can't overlap; the writer literally cannot start until the researcher finishes.

## Operational Cost: More Tokens, Not Fewer

```
Splitting a task into 3 agents doesn't reduce the TOTAL work — it
usually INCREASES total token usage, because:

1. Each agent's own system prompt/instructions are sent again,
   every time, on top of the shared task context
2. A "clean handoff" summary (per researcher-to-writer-pattern.md)
   is ADDITIONAL generated content, not a reduction
3. Any critic/evaluator step (per critic-to-refiner-loop.md) is
   ENTIRELY additional generation on top of the original work
```

This is a genuinely common, easy-to-underestimate cost: splitting one task into multiple
specialized agents virtually always increases the *total* number of tokens processed across the
whole system, even though each individual agent's context stays smaller and more focused. Applying
[cost-awareness-pricing-per-token-and-why-bad-prompts-waste-money.md](../calling-llm-apis-properly/cost-awareness-pricing-per-token-and-why-bad-prompts-waste-money.md)'s
per-token pricing lens across an entire multi-agent pipeline (not just one call) is essential before
committing to this architecture.

## Measuring Before Committing

```python
def measure_pipeline_cost(pipeline_fn, test_inputs):
    total_tokens = 0
    total_latency_ms = 0
    for input_data in test_inputs:
        start = time.time()
        result = pipeline_fn(input_data)
        total_latency_ms += (time.time() - start) * 1000
        total_tokens += sum(usage.input_tokens + usage.output_tokens for usage in result.usage_log)
    return {
        "avg_tokens_per_request": total_tokens / len(test_inputs),
        "avg_latency_ms": total_latency_ms / len(test_inputs),
    }
```

Directly per
[observability-and-monitoring-basics.md](../evaluating-ai-systems/observability-and-monitoring-basics.md)'s
core metrics, measuring a multi-agent pipeline's actual token usage and latency against a
single-agent alternative — with real, representative test inputs — turns "multi-agent feels more
thorough" into an actual, comparable number before committing to the added architecture.

## When the Cost Is Genuinely Worth Paying

```
Worth it: a task where a single agent's quality is MEASURABLY
  worse — not just theoretically — and the improvement justifies
  the added cost and latency

Not worth it: "it feels more sophisticated" or "it might be better"
  without an actual measurement backing that intuition
```

This directly echoes Anthropic's own "add complexity only when it demonstrably improves outcomes"
guidance from [Understanding AI Agents](../understanding-ai-agents/) — cost and latency are the
concrete, measurable price of that added complexity, and they should be weighed against an equally
concrete, measured quality improvement.

## Common Mistakes

- Assuming a multi-agent split automatically reduces cost because each individual agent's context is
  smaller, ignoring that the *total* tokens across the whole pipeline usually go up.
- Never actually measuring a multi-agent pipeline's real latency and cost against a simpler
  alternative before committing to the architecture in production.
- Treating latency as acceptable "because the task is thorough" without considering whether a user
  waiting on the response actually needs that level of thoroughness for every request.

## ➡️ Next

Continue to
[debugging-difficulty-across-agents.md](debugging-difficulty-across-agents.md) to see the second
major cost: how much harder a multi-agent system is to diagnose when something goes wrong.
