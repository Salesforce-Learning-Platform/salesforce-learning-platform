# 🧬 Hybrid Logic: AI and Code Working Together

## Neither Pure AI Nor Pure Code

Real, production AI features are rarely "the model does everything" or "code does everything" —
the strongest designs deliberately split responsibility: the model handles **understanding intent
and reasoning about unstructured input**, while ordinary code handles **exact computation, real
actions, and business rules**.

## A Concrete Example: A Customer Support Assistant

```python
tools = [
    {
        "name": "look_up_order",
        "description": "Retrieve order details by order ID.",
        "input_schema": {
            "type": "object",
            "properties": {"order_id": {"type": "string"}},
            "required": ["order_id"],
        },
    },
    {
        "name": "issue_refund",
        "description": "Issue a refund for an order. Requires manager approval for amounts over $100.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"},
                "amount": {"type": "number"},
                "reason": {"type": "string"},
            },
            "required": ["order_id", "amount", "reason"],
        },
    },
]
```

Here, the model's job is purely interpretive: understanding a customer's free-text complaint,
deciding which tool(s) are relevant, and extracting the right arguments. Everything downstream —
whether an amount actually exceeds the $100 threshold, whether the requesting user is actually
authorized, whether the order actually exists — is enforced by real code in `issue_refund`'s
implementation, never by the model's own judgment.

## Business Rules Belong in the Tool's Implementation, Not the Prompt

```js
// AVOID relying on prompt text alone: "Only refund if under $100"
// PREFER enforcing it in the actual function
async function issueRefund({ orderId, amount, reason }, requestingUser) {
  if (amount > 100 && !requestingUser.isManager) {
    throw new ToolExecutionError("Refunds over $100 require manager approval.");
  }
  // ... the real refund logic
}
```

A rule stated only in a prompt is a *suggestion* the model usually follows — but "usually" isn't
good enough for a genuine business rule with real financial consequences. The tool's actual
implementation should enforce the rule in code, so it holds even on the rare occasion the model's
behavior doesn't.

## Passing Context the Model Shouldn't See

```python
# The requesting user's ID comes from YOUR application's session,
# never from the model's tool call arguments
async def handle_tool_call(tool_name, tool_input, current_user):
    if tool_name == "issue_refund":
        return await issue_refund(tool_input, requesting_user=current_user)
```

Some data — the authenticated user's real identity, an internal permission level — should come from
your application's own trusted session state, never from an argument the model fills in. Letting the
model supply its own claim about "who is asking" would let a cleverly-worded prompt potentially
impersonate a different user.

## The Pattern in One Diagram

```
User's free-text request
        │
        ▼
   Model interprets intent, extracts structured tool_use arguments
        │
        ▼
   Your CODE validates, enforces business rules, executes the real
   action (using trusted context the model never controls)
        │
        ▼
   Result sent back as tool_result → model produces the final,
   human-readable reply
```

This hybrid loop — model for interpretation, code for everything that must be exactly correct or
strictly enforced — is the practical shape of nearly every real, production tool-calling feature.

## Common Mistakes

- Relying on prompt instructions alone to enforce a genuine business rule instead of checking it in
  the tool's actual implementation.
- Letting the model supply "who is making this request" as a tool argument instead of using the
  application's own trusted session/auth state.
- Splitting responsibility so the model does too much — for instance, generating a final price
  itself — when that calculation belongs in a deterministic tool instead.

## ➡️ Next

Continue to
[letting-ai-decide-which-function-to-call.md](letting-ai-decide-which-function-to-call.md) to see
how a model actually chooses between multiple available tools, and how to guide that choice.
