# 🎲 Sampling Basics: Temperature and Randomness Control

## An LLM Doesn't Pick One "Correct" Next Token

At each step, an LLM computes a **probability distribution** over every possible next
[token](what-are-tokens-and-why-everything-becomes-tokens.md) — not a single, definite answer. The
word "the" might have a 40% probability of coming next, "a" might have 15%, and so on across
thousands of possible tokens. **Sampling** is the process of actually picking one token from that
distribution to generate — and *how* that pick happens is directly controllable.

## Temperature — Controlling How "Safe" or "Adventurous" That Pick Is

```
LOW temperature (e.g. 0):   almost always pick the single highest-
                             probability token — conservative,
                             consistent, predictable output

HIGH temperature (e.g. 1+): genuinely more willing to pick a lower-
                             probability token — more varied,
                             creative, sometimes surprising output
```

**Temperature** is the parameter controlling exactly this: how much randomness is applied when
sampling from that probability distribution. A low temperature sticks closely to the most probable,
"safe" phrasing every time; a higher temperature deliberately allows rarer, less predictable word
choices through — genuinely useful for creative writing, and genuinely undesirable for a task that
needs consistent, predictable structure (like generating valid JSON, covered later in this domain).

## Choosing Temperature for a Real Task

```
LOW temperature: extracting structured data, answering a factual
question, generating code — tasks where consistency and
predictability matter far more than variety

HIGH temperature: creative writing, brainstorming, generating varied
example content — tasks where genuine variety is the actual goal
```

There's no single universally "correct" temperature — the right value depends entirely on what the
task actually needs. A task that must reliably produce the same kind of structured, predictable
output every time should use a low temperature; a task that genuinely benefits from creative
variation should use a higher one.

## Common Mistakes

- Using a high temperature for a task that needs consistent, structured output (like data
  extraction or generating valid code), producing unpredictable, sometimes broken results.
- Using a very low temperature for genuinely creative work and being disappointed by repetitive,
  formulaic output — some randomness is often exactly what creative variety requires.
- Assuming temperature 0 guarantees the model always outputs the literal single best-known answer
  in some absolute sense — it means "almost always pick the highest-probability token," not "the
  output is now provably correct."

## ➡️ Next

Continue to
[why-hallucination-happens-it-predicts-it-doesnt-know.md](why-hallucination-happens-it-predicts-it-doesnt-know.md)
to see the direct, structural consequence of this prediction-based process.
