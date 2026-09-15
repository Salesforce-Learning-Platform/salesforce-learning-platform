# 🧭 Letting AI Decide Which Function to Call

## The Default: `tool_choice: "auto"`

```python
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    tools=[get_weather_tool, look_up_order_tool, issue_refund_tool],
    tool_choice={"type": "auto"},  # this is also the default when omitted
    messages=messages,
)
```

With `tool_choice` set to `"auto"` (the default), the model decides for itself, on every turn,
whether to call a tool at all and — if several are available — **which one** fits the actual
request. It calls a tool when the request maps to that tool's description and the answer isn't
already available in the conversation; it responds directly with plain text otherwise.

## How the Model Actually Chooses Between Tools

```
User: "What's my order status?"
    → maps to look_up_order's description → model calls look_up_order

User: "I'd like a refund for that broken item"
    → maps to issue_refund's description → model calls issue_refund

User: "What's your return policy?"
    → matches NEITHER tool's description → model responds with
      plain text instead
```

This is exactly why each tool's `description` matters so much (as introduced in
[what-is-tool-calling-and-why-it-matters.md](what-is-tool-calling-and-why-it-matters.md)) — with
several tools available at once, a vague or overlapping description is the most common real cause
of the model picking the wrong one, or failing to pick any tool when it should have.

## Forcing a Specific Choice

```python
# Force the model to call a tool (any tool) rather than reply in plain text
tool_choice={"type": "any"}

# Force the model to call ONE SPECIFIC named tool
tool_choice={"type": "tool", "name": "look_up_order"}

# Force the model to NEVER call a tool this turn
tool_choice={"type": "none"}
```

Beyond `"auto"`, `tool_choice` can force stronger guarantees: `"any"` requires *some* tool call,
`{"type": "tool", "name": "..."}` requires that *specific* tool, and `"none"` disables tool calling
entirely for that turn. Reach for a forced choice when a particular part of a flow has a known,
required next step — for instance, immediately after asking the user to confirm a refund amount,
forcing `issue_refund` specifically rather than leaving the choice open again.

## `strict: true` — Guaranteeing the Arguments Match the Schema

```python
tools = [{
    "name": "issue_refund",
    "strict": True,
    "input_schema": { "...": "..." },
}]
```

Just as covered for pure structured extraction in
[basics-of-tool-function-calling.md](../generating-json-responses-from-llms/basics-of-tool-function-calling.md),
`strict: true` applies equally here — guaranteeing the arguments in a real, action-triggering
`tool_use` block always conform exactly to the declared `input_schema`, which matters even more
once the tool call is about to trigger a real, consequential action.

## Handling Ambiguity Instead of Letting the Model Guess

```
User: "What's the weather?" (no location given)
    → Claude Sonnet models MAY guess a plausible default location
      rather than asking for clarification
```

When a required parameter is genuinely missing from the user's request, a model — especially a
smaller or faster one — may sometimes guess a plausible-looking value instead of asking for
clarification, and this behavior isn't guaranteed either way. For any parameter where a wrong guess
would matter (a real order ID, a real amount), the tool's implementation should validate the
argument it actually receives rather than assume the model always asked before guessing.

## Common Mistakes

- Writing overlapping or vague descriptions across multiple tools, causing the model to pick the
  wrong one for an ambiguous request.
- Leaving `tool_choice` as `"auto"` in a flow with a known, required next step, when forcing a
  specific tool would remove the ambiguity entirely.
- Assuming the model will always ask for a missing required parameter instead of guessing — the
  tool's own validation should never depend on that assumption holding.

## Module Summary

Across this module: **tool calling** bridges the gap between a model's text-only generation and the
real actions and lookups an application can perform, through a `tool_use` request and a
`tool_result` reply (see
[what-is-tool-calling-and-why-it-matters.md](what-is-tool-calling-and-why-it-matters.md));
**deterministic actions — exact computation, real and consequential effects** — belong in a real
tool call rather than the model's own generation, while purely generative tasks need no tool at all
(see
[when-to-use-it-for-deterministic-actions.md](when-to-use-it-for-deterministic-actions.md));
**hybrid design** puts intent-understanding in the model and business-rule enforcement in the tool's
actual code, with trusted context like user identity coming from the application's own session, never
from the model (see [hybrid-logic-ai-and-code.md](hybrid-logic-ai-and-code.md)); and **`tool_choice`**
— `"auto"`, `"any"`, a forced specific tool, or `"none"` — combined with clear, non-overlapping
tool descriptions and `strict: true`, governs exactly how and when the model calls a tool at all.
