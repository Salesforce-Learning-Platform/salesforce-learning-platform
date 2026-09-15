# 📝 Writing Clear Instructions

## Think of the Model as a Brilliant, but Genuinely New, Employee

An LLM has no inherited context about your specific norms, conventions, or unstated assumptions —
it only knows what's actually in the prompt. Anthropic's own guidance frames this precisely: treat
the model like a brilliant but brand-new employee, who lacks any context on your team's workflows.
The more precisely you explain what you actually want, the better the result — vagueness isn't
filled in with the "right" assumption; it's filled in with *some* plausible assumption, which may
not match what you actually meant.

## The Golden Rule: Would a Colleague With No Context Understand This?

```
Show your exact prompt to a colleague who has minimal context on
the task, and ask them to follow it. If THEY would be confused
about exactly what's being asked, the model will be too.
```

This is a genuinely practical, concrete test — not an abstract principle. A prompt that assumes
unstated context, uses ambiguous phrasing, or leaves the actual desired output format unclear will
produce inconsistent, unpredictable results, for exactly the same reason a human given the same
vague instructions would produce inconsistent results.

## A Concrete Before/After

```
LESS EFFECTIVE: "Create an analytics dashboard"

MORE EFFECTIVE: "Create an analytics dashboard. Include as many
relevant features and interactions as possible. Go beyond the
basics to create a fully-featured implementation."
```

The "less effective" version leaves the actual scope, depth, and expected feature set entirely
unstated — the model has to guess what "an analytics dashboard" concretely means to you. The "more
effective" version removes that guesswork by stating the actual expectation directly.

## Be Specific About Format and Order

Two concrete techniques that consistently help:

- **State the desired output format and constraints explicitly** — don't leave the model to guess
  whether you want a paragraph, a table, or a specific structure (covered fully in
  [output-formatting-instructions-making-responses-predictable.md](output-formatting-instructions-making-responses-predictable.md)).
- **Use numbered steps or bullet points when order or completeness genuinely matters** — if a task
  has several distinct steps that must happen in sequence, say so explicitly rather than describing
  them in one continuous paragraph.

## Adding Context (the "Why") Genuinely Helps

```
LESS EFFECTIVE: "NEVER use ellipses"

MORE EFFECTIVE: "Your response will be read aloud by a text-to-
speech engine, so never use ellipses since the engine won't know
how to pronounce them."
```

Explaining the actual *reason* behind an instruction — not just the instruction itself — lets a
model generalize correctly to related situations it wasn't explicitly told about, rather than
following the rule mechanically without understanding why it exists.

## Common Mistakes

- Writing a prompt that assumes shared context the model was never actually given, producing a
  response based on a different, plausible-but-wrong interpretation.
- Describing a desired outcome vaguely ("make it good") instead of stating concrete, checkable
  expectations.
- Omitting the reasoning behind a constraint, losing the model's ability to apply that same
  reasoning correctly to a related situation not explicitly covered.

## ➡️ Next

Continue to
[few-shot-examples-to-force-pattern-learning.md](few-shot-examples-to-force-pattern-learning.md)
to steer output even more reliably — by showing, not just telling.
