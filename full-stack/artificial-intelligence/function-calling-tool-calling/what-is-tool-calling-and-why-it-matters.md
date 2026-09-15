# 🔧 What Is Tool Calling and Why It Matters

## From Structured Extraction to Real Action

[Basics of Tool/Function Calling](../generating-json-responses-from-llms/basics-of-tool-function-calling.md),
in the previous module, used the tool-calling mechanism purely to extract structured data — the
"tool" never actually did anything. This module covers the **real, full capability**: an AI model
that can genuinely decide to call a real function in your application, receive its actual result,
and use that result to continue reasoning or respond.

## The Core Problem Tool Calling Solves

```
An LLM, by itself, can only do ONE thing: generate text based on
its training data and the conversation so far.

It CANNOT, on its own:
  - look up today's actual weather
  - check a real database for a real user's actual order status
  - send a real email
  - perform exact arithmetic on large numbers reliably
  - know anything that happened after its training cutoff
```

A model's knowledge is frozen at training time, and its raw output is just text — it has no
built-in way to reach outside itself. Tool calling is the mechanism that bridges this gap: it lets
a model request that *your application* perform a real action or a real lookup, then hands the
result back so the model can use it.

## The Round Trip, Concretely

```python
tools = [{
    "name": "get_weather",
    "description": "Get the current weather for a given location.",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City and state, e.g. San Francisco, CA"}
        },
        "required": ["location"],
    },
}]

response = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in San Francisco?"}],
)
# response.stop_reason == "tool_use"
# response.content contains a tool_use block:
#   { "type": "tool_use", "id": "toolu_01...", "name": "get_weather",
#     "input": { "location": "San Francisco, CA" } }
```

The model doesn't run `get_weather` itself — it can't. Instead it replies with `stop_reason:
"tool_use"` and a `tool_use` content block naming which tool it wants and with what arguments. Your
application code is the one that actually looks up the weather.

```python
weather = look_up_weather("San Francisco, CA")  # your real implementation

messages.append({"role": "assistant", "content": response.content})
messages.append({
    "role": "user",
    "content": [{"type": "tool_result", "tool_use_id": tool_use.id, "content": weather}],
})

followup = client.messages.create(
    model="claude-opus-5", max_tokens=1024, tools=tools, messages=messages,
)
# followup now contains the model's final, text answer, informed by the real result
```

Your code sends the real result back in a `tool_result` block, keyed to the original `tool_use_id`
so the model knows which call it corresponds to. The model then continues, now with real,
up-to-date information it could never have had on its own.

## The Three Pieces That Make This Work

```
1. TOOL DEFINITION   → name, description, input_schema (what the tool
                        does and what arguments it needs)
2. TOOL_USE BLOCK     → the model's request: "call this tool with
                        these arguments"
3. TOOL_RESULT BLOCK  → your application's real answer, sent back so
                        the model can use it
```

The `description` field matters more than it might first appear — the model decides *whether* and
*when* to call a tool almost entirely based on how clearly the description explains what the tool
does and when it's useful, directly applying
[writing-clear-instructions.md](../prompt-engineering-fundamentals/writing-clear-instructions.md)'s
clarity principle to a tool's own definition.

## Client Tools vs. Server Tools

```
CLIENT TOOLS  → you define the schema, YOUR code executes the call
                and returns the tool_result (get_weather above)

SERVER TOOLS  → Anthropic's own infrastructure executes the call
                (e.g. a web search tool) — you receive the result
                directly, with no execution code of your own to write
```

This module focuses on client tools — the pattern used for connecting a model to your own
application's real functions, databases, and APIs.

## Common Mistakes

- Assuming the model actually executes the function itself — it only ever *requests* a call; your
  application code is always the one that runs it.
- Writing a vague or generic tool `description`, leading the model to call the wrong tool, or the
  right tool at the wrong time.
- Forgetting that a `tool_use` response isn't the end of the conversation — the result still needs
  to be sent back for the model to actually use it.

## ➡️ Next

Continue to
[when-to-use-it-for-deterministic-actions.md](when-to-use-it-for-deterministic-actions.md) to see
when reaching for a real tool call is the right choice, and when it isn't.
