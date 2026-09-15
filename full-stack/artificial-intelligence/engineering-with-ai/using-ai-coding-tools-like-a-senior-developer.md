# 👨‍💻 Using AI Coding Tools Like a Senior Developer

## The Tools, Briefly

```
Cursor      → an AI-native code editor (a fork of VS Code) with
              deep, editor-integrated AI code generation and chat
GitHub
Copilot     → an AI pair-programmer available as an extension
              across many editors, focused on inline suggestions
Claude Code → an agentic CLI/IDE tool that can read a codebase,
              plan changes, edit multiple files, run commands, and
              verify its own work
```

These tools differ in shape — inline autocomplete vs. chat vs. a full agentic loop (per
[Understanding AI Agents](../understanding-ai-agents/), the same underlying agentic pattern this
domain has covered from first principles) — but the engineering judgment for using any of them well
is the same, and it comes down to one core idea: **a junior developer accepts suggestions; a senior
developer directs and verifies them.**

## The Senior-Developer Mental Model

```
JUNIOR approach: "The AI wrote it, so it's probably fine" -
  accept, move on, trust by default

SENIOR approach: "I asked for X. Did it actually deliver X,
  correctly, in a way that fits THIS codebase?" - direct, then
  verify, every time
```

This isn't about distrust for its own sake — it's the same discipline
[never-trust-ai-output-without-validation.md](../schema-validation-with-zod/never-trust-ai-output-without-validation.md)
established for AI-generated *data* earlier in this domain, applied here to AI-generated *code*.
Code is just another kind of AI output, and it deserves the same scrutiny before it's trusted.

## Writing a Genuinely Good Prompt for Code Generation

```
WEAK: "Add pagination to this endpoint"

STRONG: "Add cursor-based pagination to the GET /orders endpoint,
matching the pattern already used in GET /products (see
src/routes/products.js). Use the same `limit`/`cursor` query
params, and add a test for the empty-results case."
```

This directly applies [writing-clear-instructions.md](../prompt-engineering-fundamentals/writing-clear-instructions.md)'s
clarity principle to code specifically — pointing to an existing pattern in the actual codebase, per
this repo's own architecture, produces meaningfully more consistent, integrated results than a
vague request the tool has to guess an approach for.

## Giving the Tool Real Context

```
A tool that can only see the CURRENT file will guess at
conventions - naming, error handling, project structure.

A tool that can read the SURROUNDING codebase (an agentic tool
like Claude Code, or a well-configured Cursor session) can match
EXISTING patterns instead of inventing its own.
```

This is a genuinely practical, high-leverage habit: pointing an AI coding tool at a relevant
existing file, or letting an agentic tool actually explore the codebase first, consistently produces
code that looks like it belongs in the project — rather than a stylistically foreign addition that
happens to work.

## Iterating, Not Accepting the First Draft

```
"This is close, but our error responses always include a
`requestId` field - can you match that pattern?" (a SECOND turn,
refining the FIRST output)
```

Directly parallel to
[implementing-retry-strategies-for-broken-outputs.md](../schema-validation-with-zod/implementing-retry-strategies-for-broken-outputs.md)'s
"feed the specific errors back" technique — treating the first generated draft as a starting point
to refine, not a final answer to accept or reject wholesale, consistently produces better results
than either blindly accepting or starting over from scratch.

## Common Mistakes

- Accepting a large, multi-file AI-generated change without reading through it, treating volume of
  output as a proxy for quality.
- Writing vague prompts and then blaming the tool for a generic, poorly-integrated result instead of
  giving it the context and existing patterns to match.
- Never giving specific, targeted feedback on a draft — either accepting it as-is or discarding it
  entirely and starting over.

## ➡️ Next

Continue to
[reviewing-ai-generated-code-when-to-trust-it-and-when-not-to.md](reviewing-ai-generated-code-when-to-trust-it-and-when-not-to.md)
to see the actual review discipline that makes "verify, don't just accept" concrete.
