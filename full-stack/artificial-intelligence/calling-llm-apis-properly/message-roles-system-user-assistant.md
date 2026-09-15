# 🎭 Message Roles: System, User, Assistant

## The `messages` Array — Alternating User and Assistant

```json
[
  { "role": "user", "content": "Hello, Claude" }
]
```

```json
[
  { "role": "user", "content": "Hello there." },
  { "role": "assistant", "content": "Hi, I'm Claude. How can I help you?" },
  { "role": "user", "content": "Can you explain LLMs in plain English?" }
]
```

A request's `messages` array holds the actual conversation — `user` messages represent the
end-user's input, and `assistant` messages represent the model's own prior responses. For a
multi-turn conversation, the array must genuinely **alternate** between the two roles, building up
the real conversation history exactly as it happened.

## `system` Is Not a Message Role — It's Its Own Parameter

```json
{
  "model": "claude-sonnet-5",
  "system": "You are a helpful customer support agent for an e-commerce store. Be concise and friendly.",
  "messages": [
    { "role": "user", "content": "Where is my order?" }
  ]
}
```

This is a genuinely easy mistake to make: the system prompt — instructions establishing the
model's role, tone, or constraints for the entire conversation — is **not** a role placed inside
the `messages` array. It's provided through its own separate, top-level `system` parameter, kept
distinct from the actual back-and-forth conversation.

## Why This Separation Actually Matters

Keeping the system prompt separate from the conversation history means it applies consistently to
every single turn, without needing to be repeated inside every user message, and without risking
it being misinterpreted as something the "user" said. It's the equivalent of a stable configuration
setting for the entire request, not a message exchanged as part of the conversation itself.

## Continuing a Response — Ending With an `assistant` Message

```json
[
  { "role": "user", "content": "What's the Greek name for the Sun? (A) Sol (B) Helios (C) Sun" },
  { "role": "assistant", "content": "The best answer is (" }
]
```

Ending the `messages` array with an `assistant` message (rather than a `user` one) tells the model
to **continue** from exactly that point, rather than starting a fresh response — genuinely useful
for constraining the format of an answer (here, forcing a direct multiple-choice letter to follow).

## Common Mistakes

- Putting system instructions directly inside a `user` message instead of the dedicated `system`
  parameter, mixing configuration with actual conversational content.
- Sending a `messages` array with two consecutive `user` (or two consecutive `assistant`) messages
  without realizing most APIs will simply merge them into a single turn, rather than treating them
  as genuinely separate exchanges.
- Forgetting that the full conversation history needs to be resent with every request — the API
  itself has no memory between separate calls; the application is responsible for maintaining and
  resending that history.

## ➡️ Next

Continue to
[cost-awareness-pricing-per-token-and-why-bad-prompts-waste-money.md](cost-awareness-pricing-per-token-and-why-bad-prompts-waste-money.md)
to see exactly what this conversation structure actually costs.
