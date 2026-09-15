# 🔬 The Critic-Refiner Loop

## Evaluator-Optimizer, Applied

Anthropic's own guidance calls this pattern **evaluator-optimizer**: one LLM call generates a piece
of work, a second, separate LLM call critiques it against explicit criteria, and the first call
revises based on that critique — repeated until the critic is satisfied or an iteration limit is
reached. This directly extends
[implementing-retry-strategies-for-broken-outputs.md](../schema-validation-with-zod/implementing-retry-strategies-for-broken-outputs.md)'s
"retry with feedback" idea from a *schema* validation failure to a genuine *quality* judgment.

## The Loop, Concretely

```python
def critic_refiner_loop(task, max_iterations=3):
    draft = generate_draft(task)

    for i in range(max_iterations):
        critique = critique_draft(task, draft)
        if critique["approved"]:
            return draft
        draft = refine_draft(task, draft, critique["feedback"])

    return draft  # return the best available draft even if not fully approved

def critique_draft(task, draft):
    response = client.messages.create(
        model="claude-opus-5", max_tokens=512,
        tools=[{
            "name": "submit_critique",
            "strict": True,
            "input_schema": {
                "type": "object",
                "properties": {
                    "approved": {"type": "boolean"},
                    "feedback": {"type": "string"},
                },
                "required": ["approved", "feedback"],
            },
        }],
        tool_choice={"type": "tool", "name": "submit_critique"},
        messages=[{"role": "user", "content": f"Task: {task}\n\nDraft:\n{draft}\n\nCritique this draft against the task's requirements."}],
    )
    return next(b.input for b in response.content if b.type == "tool_use")

def refine_draft(task, draft, feedback):
    response = client.messages.create(
        model="claude-opus-5", max_tokens=1024,
        messages=[{"role": "user", "content": f"Task: {task}\n\nPrevious draft:\n{draft}\n\nFeedback: {feedback}\n\nProduce an improved draft."}],
    )
    return response.content[0].text
```

The critic uses [forced tool use](../function-calling-tool-calling/letting-ai-decide-which-function-to-call.md)
(`tool_choice: {"type": "tool", ...}`) specifically to guarantee a structured, parseable verdict —
an `approved` boolean the loop can check programmatically, rather than trying to infer approval from
free-form critique text.

## Why a Separate Critic Call — Not Just "Try Again"

```
A single model asked to "review your own work" tends toward being
LENIENT with itself — it already committed to the reasoning behind
the original draft.

A SEPARATE call, given ONLY the draft and the task's requirements
(no visibility into the original reasoning), can judge it more
objectively — closer to how a fresh reviewer would.
```

This is the actual insight behind treating critique as its own distinct step rather than a vague
instruction to "double-check your answer": a genuinely separate evaluation, especially one with
explicit, well-defined criteria to check against, tends to catch real problems a self-review would
gloss over.

## When Evaluator-Optimizer Is Worth the Extra Cost

```
Good fit: literary translation (capturing nuance genuinely
  benefits from iterative critique), complex research reports,
  code that must meet specific, checkable criteria

Poor fit: a quick factual lookup, or any task where "good enough
  on the first try" is already the actual bar
```

Per Anthropic's own guidance, this pattern earns its cost specifically when there are **clear
evaluation criteria** to check against and **iterative refinement measurably improves** the result
— not simply "for anything that could theoretically be better."

## Common Mistakes

- Letting a single model call both draft and critique its own work in the same context, losing the
  genuine objectivity a separate critic call provides.
- Running the loop with no iteration ceiling, risking indefinite refinement cycles on a task with
  no clean, checkable "done" condition.
- Applying this pattern to tasks with vague, unmeasurable quality criteria, where the critic has no
  real, checkable basis for its "approved" verdict.

## ➡️ Next

Continue to
[router-agents-that-decide-which-tool-to-call.md](router-agents-that-decide-which-tool-to-call.md)
for the final pattern: directing an incoming request to the right specialized handling in the first
place.
