# 🗺️ The Planner-Executor Workflow

## Named Patterns, Not Ad Hoc Designs

[Understanding AI Agents](../understanding-ai-agents/) established the basic agentic loop and when
it's actually justified. This module covers recurring, *named* patterns built on top of that loop —
Anthropic's own engineering guidance documents several of these directly, under the umbrella term
**orchestrator-workers** for the planner-executor shape specifically.

## The Core Idea

```
PLANNER  → a central LLM call that breaks a task into a set of
           subtasks — it does NOT do the actual work itself

EXECUTOR(S) → separate LLM call(s) (or tool calls) that each
           carry out ONE subtask, using the plan as input
```

Splitting "figure out what needs to happen" from "actually do each thing" into two distinct roles
is the core of this pattern. The planner's entire job is decomposition and delegation; it never
directly produces the final work itself.

## A Concrete Example

```python
def plan_task(user_request):
    response = client.messages.create(
        model="claude-opus-5", max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Break this task into a numbered list of concrete subtasks: {user_request}",
        }],
    )
    return parse_subtasks(response.content[0].text)  # e.g. ["Research X", "Research Y", "Summarize"]

def execute_subtask(subtask, tools):
    return client.messages.create(
        model="claude-opus-5", max_tokens=1024, tools=tools,
        messages=[{"role": "user", "content": subtask}],
    )

def planner_executor(user_request, tools):
    subtasks = plan_task(user_request)
    results = [execute_subtask(task, tools) for task in subtasks]
    return synthesize_final_answer(results)  # a final LLM call combining everything
```

The planner produces a list of subtasks *without knowing in advance* exactly how each one will be
carried out — this is the key distinction from a fixed workflow (per
[agent-vs-single-llm-call.md](../understanding-ai-agents/agent-vs-single-llm-call.md)): the actual
decomposition itself is decided by the model, based on the specific request, rather than hard-coded
by the application.

## Why This Differs From Simple Parallelization

```
PARALLELIZATION: the application ALREADY KNOWS the fixed set of
                  subtasks in advance (e.g. "always run these 3
                  checks")

ORCHESTRATOR-WORKERS (planner-executor): the SET of subtasks is
                  itself determined dynamically, per request, by
                  the planner
```

This distinction, directly from Anthropic's own guidance, matters for choosing the right pattern:
if the subtasks are genuinely fixed and known ahead of time, plain parallelization (running them
concurrently) is simpler and doesn't need a dedicated planning step at all.

## When This Pattern Earns Its Complexity

```
Good fit: "Research this topic from multiple angles and write a
  report" — the SPECIFIC angles worth researching can't be known
  until the planner reasons about the actual topic

Poor fit: "Always check spelling, then grammar, then tone" — this
  is a KNOWN, FIXED set of steps; plain sequential chaining is
  simpler and doesn't need dynamic planning at all
```

Reaching for a planner step specifically when the actual subtasks genuinely can't be predetermined
is what justifies this pattern's added complexity over a simpler, fixed sequence.

## Common Mistakes

- Using a planner-executor split for a task whose subtasks are actually fixed and known in advance,
  adding unnecessary planning overhead.
- Letting the planner produce subtasks with no validation, then blindly executing whatever it
  generated even if a subtask is malformed or nonsensical.
- Forgetting a final synthesis step, leaving the application with several disconnected executor
  results instead of one coherent final answer.

## ➡️ Next

Continue to
[researcher-to-writer-pattern.md](researcher-to-writer-pattern.md) to see a specific, very common
application of a related, sequential handoff pattern.
