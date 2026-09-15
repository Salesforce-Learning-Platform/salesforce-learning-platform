# 🦜 Introduction to LangChain

## What Problem LangChain Actually Solves

Every technique in this domain so far has been built directly on the Anthropic Messages API — real,
valuable, foundational knowledge. **LangChain** is a framework that sits *on top of* provider APIs
like Anthropic's, providing reusable abstractions for the patterns this domain has already covered
by hand: prompt templates, chains, tool-calling agents, and memory — so a team doesn't have to
rebuild this scaffolding from scratch for every new project.

## Why Learn a Framework After Already Learning the Fundamentals

```
WITHOUT the fundamentals first: LangChain's abstractions (chains,
  agents, memory) feel like magic — useful, but hard to debug when
  something goes wrong

WITH the fundamentals from this domain already understood: every
  LangChain abstraction maps DIRECTLY onto a concept already
  covered — a "chain" is prompt-templating plus a Messages API
  call; an "agent" is the SAME agentic loop from
  Understanding AI Agents, just implemented for you
```

This is exactly why this module comes *after* [Understanding AI Agents](../understanding-ai-agents/)
and [Agent Design Patterns](../agent-design-patterns/) rather than before them — a framework's
abstractions are far easier to use correctly, and to debug when they misbehave, once the underlying
mechanism is already well understood.

## Installing and Connecting to Claude

```bash
pip install -U langchain langchain-anthropic
```

```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-opus-5", max_tokens=1024)
response = llm.invoke("What's the capital of France?")
print(response.content)
```

`langchain-anthropic` is the dedicated integration package connecting LangChain's standard
interfaces to Anthropic's Messages API specifically — this same `ChatAnthropic` object is what
every other file in this module builds on.

## LangChain's Core Building Blocks, at a Glance

```
CHAT MODELS       → a standard interface across providers (this
                     file) — the same code mostly works whether
                     the underlying model is Claude or another
                     provider

PROMPT TEMPLATES   → reusable, parameterized prompt structures
                     (building-chains-and-prompt-templates.md)

CHAINS / LCEL       → composing steps together with the `|`
                     operator (building-chains-and-prompt-
                     templates.md, formalized in
                     overview-of-lcel-concepts.md)

TOOLS & MEMORY      → connecting real functions and conversation
                     history (using-tools-and-memory-modules.md)

AGENTS              → LangChain's own agentic loop implementation
                     (working-with-agents.md)
```

Each of these maps to a concept this domain has already covered from first principles — this
module's job is showing *where* LangChain's abstraction sits relative to what's already
understood, not introducing a genuinely new mental model from scratch.

## When Reaching for LangChain Makes Sense — and When It Doesn't

```
Worth it: a project already using several of LangChain's
  abstractions together (chains + agents + memory), where the
  framework's consistency and ecosystem (integrations, tracing via
  LangSmith) save real, ongoing effort

Not always worth it: a simple, single-purpose feature — a direct
  Messages API call, exactly like everywhere else in this domain,
  can be simpler, more transparent, and easier to debug
```

This mirrors [when-to-use-multi-agent-systems-and-when-not-to.md](../understanding-ai-agents/when-to-use-multi-agent-systems-and-when-not-to.md)'s
"start simple" principle at the tooling level: a framework is worth its added abstraction layer
specifically when a project's actual complexity justifies it, not by default.

## Common Mistakes

- Treating LangChain's abstractions as a replacement for understanding the underlying API mechanics,
  rather than a convenience layer built on top of concepts already learned.
- Reaching for the full framework for a single, simple LLM call where a direct API call would be
  simpler and more transparent.
- Mixing outdated LangChain patterns (from older tutorials) with current ones — the framework has
  evolved significantly, and its own documentation is the authoritative, current source.

## ➡️ Next

Continue to
[building-chains-and-prompt-templates.md](building-chains-and-prompt-templates.md) to see
LangChain's reusable prompt templates and its first composition pattern in action.
