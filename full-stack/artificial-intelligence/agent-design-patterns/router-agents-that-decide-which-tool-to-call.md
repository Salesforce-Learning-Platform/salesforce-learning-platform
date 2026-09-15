# 🚦 Router Agents That Decide Which Tool to Call

## Routing, in Anthropic's Own Terms

Anthropic's own guidance describes this pattern plainly: **routing** classifies an incoming input
and directs it to a specialized follow-up handler — a distinct prompt, a distinct tool, sometimes
even a distinct model — chosen specifically for that category of request.

## The Simplest Form: `tool_choice: "auto"` Already Routes

```
Recall from letting-ai-decide-which-function-to-call.md: with
tool_choice: "auto" (the default), the model ITSELF already picks
which of several available tools fits a given request.
```

In its most basic form, [letting-ai-decide-which-function-to-call.md](../function-calling-tool-calling/letting-ai-decide-which-function-to-call.md)
already introduced router-style behavior — a model choosing between `look_up_order`,
`issue_refund`, and `escalate_to_human` based on each tool's description *is* routing, in its
simplest possible shape.

## A Dedicated Router Step, for More Deliberate Control

```python
def route_request(user_message):
    response = client.messages.create(
        model="claude-opus-5", max_tokens=64,
        tools=[{
            "name": "classify_request",
            "strict": True,
            "input_schema": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "enum": ["billing", "technical", "general"]},
                },
                "required": ["category"],
            },
        }],
        tool_choice={"type": "tool", "name": "classify_request"},
        messages=[{"role": "user", "content": user_message}],
    )
    category = next(b.input["category"] for b in response.content if b.type == "tool_use")

    handlers = {
        "billing": handle_billing_request,
        "technical": handle_technical_request,
        "general": handle_general_request,
    }
    return handlers[category](user_message)
```

A dedicated, separate router step — deliberately kept small and cheap (`max_tokens=64`, a narrow,
forced tool call) — is worth building specifically when each category needs a genuinely different,
specialized downstream handler, not just a different tool among several available to one general
agent.

## Cost-Based Routing — a Genuinely Practical Use

```
Simple, common request  → route to a smaller, faster, cheaper model
Complex, unusual request → route to a larger, more capable model
```

One of Anthropic's own concrete examples of this pattern is routing purely on *complexity* rather
than topic — sending straightforward questions to a smaller model and only escalating genuinely
difficult ones to a larger, more expensive model. This directly applies
[cost-awareness-pricing-per-token-and-why-bad-prompts-waste-money.md](../calling-llm-apis-properly/cost-awareness-pricing-per-token-and-why-bad-prompts-waste-money.md)'s
principle at the architecture level, not just the prompt level.

## When a Dedicated Router Beats Plain `tool_choice: "auto"`

```
Plain "auto" tool selection: fine when the DOWNSTREAM handling for
  each category is similar in shape (all tool calls within one
  agent's context)

A DEDICATED router step: worth it when each category needs a
  GENUINELY separate prompt, context, or even a separate model
  entirely — not just a different tool within the same call
```

This mirrors the same judgment call from
[when-to-use-multi-agent-systems-and-when-not-to.md](../understanding-ai-agents/when-to-use-multi-agent-systems-and-when-not-to.md):
a dedicated routing step is added complexity, worth it specifically when the categories genuinely
diverge enough downstream to justify a separate classification step first.

## Common Mistakes

- Building an elaborate, dedicated router for a case where plain `tool_choice: "auto"` selection
  already handles the routing decision perfectly well.
- Using an unnecessarily large, expensive model for the router step itself, when classification is
  usually a simple enough task for a smaller, cheaper model.
- Forgetting a fallback category (like `"general"`) for a request that doesn't cleanly fit any of
  the router's defined categories.

## Module Summary

Across this module: the **planner-executor** pattern (orchestrator-workers) dynamically decomposes
a task into subtasks the application couldn't predetermine, distinguishing it from simple
parallelization (see
[planner-to-executor-workflow.md](planner-to-executor-workflow.md)); the **researcher-writer**
pattern (prompt chaining) separates information-gathering from prose production specifically to
avoid context pollution, with the *shape* of the handoff between stages determining the pattern's
success (see [researcher-to-writer-pattern.md](researcher-to-writer-pattern.md)); the
**critic-refiner loop** (evaluator-optimizer) uses a genuinely separate evaluation call — often with
forced tool use for a structured verdict — to catch problems a self-review would miss, earning its
cost when clear, checkable evaluation criteria exist (see
[critic-to-refiner-loop.md](critic-to-refiner-loop.md)); and **router agents** classify an incoming
request and direct it to specialized handling — a prompt, a tool, or even a different model
entirely — ranging from simple `tool_choice: "auto"` selection to a dedicated classification step
for genuinely divergent downstream needs.
