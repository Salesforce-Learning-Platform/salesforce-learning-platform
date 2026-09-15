# 💸 Cost Awareness: Pricing Per Token

## Billed Per Token, Input and Output Separately

Recall [what-are-tokens-and-why-everything-becomes-tokens.md](../how-llms-actually-work/what-are-tokens-and-why-everything-becomes-tokens.md):
tokens are the actual unit an LLM processes. API pricing is built directly on that same unit —
**input tokens** (everything sent: the system prompt, conversation history, the current message)
and **output tokens** (what the model generates) are typically priced separately, and often at
different rates, since generating new text is generally more computationally expensive than
processing existing text.

## Every Resent Piece of Conversation History Costs Again

```
Turn 1: system prompt (500 tokens) + user message (50 tokens) → billed for 550 input tokens
Turn 2: system prompt (500) + turn 1's user+assistant messages (200) + new message (50)
        → billed for 750 input tokens — the SAME system prompt, paid for AGAIN
```

Recall [message-roles-system-user-assistant.md](message-roles-system-user-assistant.md)'s point:
the full conversation history has to be resent with every request, since the API itself has no
memory between calls. This means a long, growing conversation costs progressively **more** per
turn — not because each individual message is expensive, but because the entire accumulated history
gets billed again on every single request.

## How a Poorly-Designed Prompt Directly Wastes Real Money

```
BLOATED system prompt: 3,000 tokens of verbose, repetitive
instructions — paid for on EVERY SINGLE request, forever

CONCISE, well-edited system prompt: 400 tokens — the same
effective instructions, at a fraction of the recurring cost
```

Unlike a one-time inefficiency in traditional code, an unnecessarily long or poorly-written system
prompt is a **recurring** cost — paid again on every single request that includes it, for the
entire lifetime of the application. A genuinely well-edited, concise prompt isn't just better
practice; it's directly, measurably cheaper to run at real scale.

## Unnecessary Context Is Also Wasted Money

Sending an entire large document when only a small, relevant portion is actually needed wastes
real input-token cost on every request — directly connecting to
[what-is-a-context-window-and-why-prompts-get-cut.md](../how-llms-actually-work/what-is-a-context-window-and-why-prompts-get-cut.md)'s
point that more context sent isn't free, just because the context window is technically large
enough to hold it.

## Setting `max_tokens` Deliberately

A generous, unconstrained maximum output length doesn't inherently cost more on its own (output is
billed for what's actually generated, not the cap) — but a runaway or unexpectedly long response
still costs real money for every token it actually produces, which is exactly why monitoring real
usage, not just theoretical limits, matters for genuine cost control.

## Common Mistakes

- Treating a verbose, unedited system prompt as a one-time cost, rather than recognizing it's paid
  for again on every single request.
- Sending an entire large document as context when only a small, specifically relevant portion is
  actually needed for the task at hand.
- Never actually monitoring real token usage in production, discovering unexpectedly high costs
  only after they've already accumulated.

## ➡️ Next

Continue to
[token-budgeting-prompt-size-response-size-and-overflow-planning.md](token-budgeting-prompt-size-response-size-and-overflow-planning.md)
to plan deliberately for both cost and the context window's hard limit.
