# 🤖 Working with Agents

## `create_agent` — LangChain's Own Agentic Loop

```python
from langchain.agents import create_agent

agent = create_agent(
    model="anthropic:claude-opus-5",
    tools=[get_weather, look_up_order],
    system_prompt="You are a helpful customer support assistant.",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Has order #4821 shipped yet?"}]}
)
print(result["messages"][-1].content)  # the agent's final answer
```

`create_agent` is LangChain's own implementation of exactly the agentic loop covered in
[agent-reasoning-and-tool-usage.md](../understanding-ai-agents/agent-reasoning-and-tool-usage.md) —
LangChain's own documentation states this plainly: **"An agent is a model calling tools in a loop
until a given task is complete."** Every mechanic from that earlier module — call a tool, get a
result, decide whether to call another, stop once done — is what `create_agent` handles internally.

## "Agent = Model + Harness"

```
MODEL   → the underlying LLM (here, Claude, via the
          "anthropic:claude-opus-5" provider-prefixed string)

HARNESS → the loop itself, plus configurable middleware:
          guardrails, retries, routing, custom tool policies
```

LangChain's own framing of this is useful: an agent is the model plus a **harness** — the
surrounding orchestration logic. This harness is exactly what
[agent-reasoning-and-tool-usage.md](../understanding-ai-agents/agent-reasoning-and-tool-usage.md)'s
hand-written `while` loop, `stop_reason` handling, and iteration ceiling amounted to — `create_agent`
provides a tested, configurable version of that same harness instead of writing it by hand each
time.

## Reading the Full Conversation, Not Just the Final Answer

```python
for message in result["messages"]:
    print(type(message).__name__, "-", message.content)
# HumanMessage - Has order #4821 shipped yet?
# AIMessage - (tool call to look_up_order)
# ToolMessage - {"status": "processing", "shipped": false}
# AIMessage - Order #4821 hasn't shipped yet.
```

`result["messages"]` is append-only — it contains the entire conversation, including every
intermediate tool call and result, not just the final text answer. This is genuinely useful for
debugging: the exact same visibility this domain's earlier
[logging-ai-requests-and-responses-for-debugging.md](../error-handling-in-ai-applications/logging-ai-requests-and-responses-for-debugging.md)
established the value of, available directly from the agent's own return value.

## Persisting State Across Turns With a Checkpointer

```python
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="anthropic:claude-opus-5", tools=[get_weather, look_up_order],
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": "conversation-42"}}
result = agent.invoke({"messages": [{"role": "user", "content": "Has order #4821 shipped?"}]}, config=config)
# a LATER call with the SAME thread_id continues the same conversation
followup = agent.invoke({"messages": [{"role": "user", "content": "And what about #4822?"}]}, config=config)
```

A `checkpointer`, combined with a `thread_id` (the same `session_id` idea from
[using-tools-and-memory-modules.md](using-tools-and-memory-modules.md)'s memory pattern), lets an
agent's conversation persist across multiple separate `invoke()` calls — essential for any real,
multi-turn agent feature rather than a single, one-shot request.

## Why This Replaced the Older `AgentExecutor` Pattern

```
OLDER pattern (AgentExecutor): a less flexible, harder-to-extend
  agent implementation

CURRENT pattern (create_agent): a composable, middleware-based
  architecture supporting fault tolerance, custom state, and
  human-in-the-loop steering
```

Worth knowing explicitly since LangChain has evolved significantly: `create_agent` is the current,
actively maintained pattern — a tutorial or codebase still using `AgentExecutor` or
`initialize_agent` is working from an older, superseded API.

## Common Mistakes

- Following an outdated tutorial using `AgentExecutor`/`initialize_agent` instead of the current
  `create_agent` API — the framework moves quickly enough that this happens often.
- Omitting a `checkpointer` and `thread_id` for a feature that actually needs multi-turn
  conversation continuity, then wondering why the agent "forgets" prior turns.
- Treating `create_agent`'s harness as removing the need for the iteration-ceiling and
  error-handling discipline from [Understanding AI Agents](../understanding-ai-agents/) and
  [Error Handling in AI Applications](../error-handling-in-ai-applications/) — the harness
  implements this, but production configuration and monitoring are still the application's
  responsibility.

## ➡️ Next

Continue to [overview-of-lcel-concepts.md](overview-of-lcel-concepts.md) to formalize the `|`
operator mechanism used informally throughout this module.
