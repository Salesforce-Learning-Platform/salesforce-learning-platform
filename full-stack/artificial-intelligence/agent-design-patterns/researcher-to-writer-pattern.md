# ✍️ The Researcher-Writer Pattern

## A Specific, Very Common Sequential Handoff

Where [planner-to-executor-workflow.md](planner-to-executor-workflow.md) covered dynamic
decomposition into multiple parallel subtasks, the researcher-writer pattern is a simpler, sequential
case — Anthropic's own guidance calls this general shape **prompt chaining**: one LLM call's output
becomes the next call's input, in a fixed sequence of stages.

## The Two Roles

```
RESEARCHER → gathers raw, relevant information (via retrieval,
             tool calls, or both) — its output is dense, messy,
             comprehensive, and NOT meant for a human to read
             directly

WRITER     → takes that gathered information and produces
             polished, well-organized, human-readable prose —
             it does NOT gather any new information itself
```

Separating these two roles directly addresses the "context pollution" problem introduced in
[when-to-use-multi-agent-systems-and-when-not-to.md](../understanding-ai-agents/when-to-use-multi-agent-systems-and-when-not-to.md):
a single agent trying to do both jobs at once ends up with a context full of raw search results and
intermediate notes by the time it needs to focus purely on prose quality.

## A Concrete Implementation

```python
def research_agent(topic, tools):
    """Gathers information; returns a structured summary, not prose."""
    response = client.messages.create(
        model="claude-opus-5", max_tokens=2048, tools=tools,
        messages=[{
            "role": "user",
            "content": f"Research '{topic}'. Return a structured list of key "
                       f"facts, each with its source. Do not write prose.",
        }],
    )
    return response.content[-1].text  # the final research summary

def writer_agent(topic, research_summary):
    """Takes a clean summary; produces polished, final prose."""
    response = client.messages.create(
        model="claude-opus-5", max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Using ONLY these researched facts, write a clear, "
                       f"well-organized report on '{topic}':\n\n{research_summary}",
        }],
    )
    return response.content[0].text

def researcher_writer(topic, tools):
    summary = research_agent(topic, tools)
    return writer_agent(topic, summary)
```

Notice the writer's prompt applies the same [RAG-style](../building-a-rag-pipeline/the-rag-workflow.md)
"using ONLY these facts" grounding instruction — the writer is deliberately constrained to the
researcher's findings, rather than free to introduce its own, potentially ungrounded claims.

## Why the Handoff Format Matters

```
BAD handoff: the researcher's raw tool outputs and internal
  reasoning passed directly to the writer — noisy, hard to write
  clean prose from

GOOD handoff: a clean, structured summary — key facts with
  sources — specifically designed to be exactly what the writer
  actually needs
```

The quality of this pattern depends heavily on the *shape* of what gets handed off between the two
roles — a well-designed research agent doesn't just dump everything it found, it deliberately
produces output shaped for what the writer needs next.

## When This Pattern Is (and Isn't) Worth It

```
Worth it: a genuinely long or complex report where researching
  and writing are distinct enough skills that separating them
  measurably improves quality

Not worth it: a short, simple factual answer where a single agent
  (or even a single LLM call) handles both perfectly well
```

Per [when-to-use-multi-agent-systems-and-when-not-to.md](../understanding-ai-agents/when-to-use-multi-agent-systems-and-when-not-to.md)'s
"start simple" principle, this two-stage split earns its added cost and latency specifically for
tasks substantial enough that context pollution would genuinely be a problem in a single agent.

## Common Mistakes

- Handing off raw, unstructured research output instead of a clean, purpose-built summary,
  defeating the whole point of separating the two roles.
- Letting the writer introduce facts beyond what the researcher actually found, losing the
  grounding this pattern is meant to provide.
- Using this two-stage pattern for a task simple enough that a single agent would have handled
  perfectly well at lower cost and latency.

## ➡️ Next

Continue to [critic-to-refiner-loop.md](critic-to-refiner-loop.md) to see a pattern for iteratively
improving a single piece of output, rather than producing it once.
