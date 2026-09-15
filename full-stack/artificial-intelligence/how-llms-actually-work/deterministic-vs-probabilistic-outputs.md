# 🎯 Deterministic vs. Probabilistic Outputs

## Traditional Software Is Deterministic

```js
function add(a, b) {
  return a + b;
}
add(2, 3); // ALWAYS 5. Every single time. Guaranteed.
```

Every function covered throughout the [Backend domain](../../backend/) is genuinely
**deterministic**: the exact same input always produces the exact same output, every single time,
with no exceptions. This is a foundational assumption most software engineering already relies on —
tests that assert an exact expected value, caching (per
[Caching — Local and Redis](../../backend/caching-local-and-redis/)) that assumes a repeated
request can safely reuse a prior result.

## An LLM Is Fundamentally Probabilistic

Recall [sampling-basics-temperature-and-randomness-control.md](sampling-basics-temperature-and-randomness-control.md):
an LLM doesn't compute one guaranteed correct output — it samples from a probability distribution
over possible next tokens. This means the **same prompt can genuinely produce a different response
each time it's sent**, especially at a non-zero temperature.

## Even Temperature 0 Isn't a Full Guarantee

```
"Users may encounter non-determinism in APIs. Even with temperature
set to 0, the results will not be fully deterministic and identical
inputs may produce different outputs across API calls."
```

This is worth internalizing precisely: setting temperature to 0 (per
[sampling-basics-temperature-and-randomness-control.md](sampling-basics-temperature-and-randomness-control.md))
makes output far more consistent, strongly favoring the single highest-probability token at each
step — but real-world API behavior across major providers still doesn't guarantee full,
bit-for-bit determinism, for reasons related to how computation is actually distributed and
executed at scale, not just the temperature setting alone.

## Why This Genuinely Changes How You Build With LLMs

```js
// A traditional function — safe to write a test asserting an EXACT
// output value
expect(add(2, 3)).toBe(5);

// An LLM call — asserting an EXACT output value is fundamentally
// the wrong approach; test for STRUCTURE, PRESENCE, or a range of
// acceptable behavior instead
expect(response).toMatch(/\$\d+\.\d{2}/); // looks like a price, not an EXACT string
```

Building reliably on top of something probabilistic requires a real shift in approach: instead of
asserting an exact expected output (as ordinary [unit tests](../../backend/backend-testing/) would),
testing and validating an LLM-powered feature means checking for the right **structure**, the right
**shape**, or membership in an acceptable range of outputs — a concept
[Evaluating AI Systems](../evaluating-ai-systems/), later in this domain, covers in full depth.

## Common Mistakes

- Assuming temperature 0 provides the same absolute, bit-for-bit guarantee as a traditional
  deterministic function — it makes output far more consistent, but real APIs don't promise full
  determinism even then.
- Writing a test for an LLM-powered feature that asserts an exact, literal output string, the same
  way a traditional unit test would — this breaks unpredictably even when the feature is genuinely
  working correctly.
- Building application logic that assumes an LLM call will always return the identical structure
  on every call, without validating the actual response — a concern
  [Schema Validation with Zod](../schema-validation-with-zod/), later in this domain, directly
  addresses.

## Module Summary

Across this module: **tokens** are the actual unit an LLM processes text as, roughly but not
exactly corresponding to words, directly tied to real cost and limits (see
[what-are-tokens-and-why-everything-becomes-tokens.md](what-are-tokens-and-why-everything-becomes-tokens.md));
the **context window** is the model's working memory for a specific conversation, a genuinely
different and much smaller thing than its total trained knowledge (see
[what-is-a-context-window-and-why-prompts-get-cut.md](what-is-a-context-window-and-why-prompts-get-cut.md));
**temperature** controls how much randomness is applied when sampling the next token, chosen
deliberately based on whether a task needs consistency or creative variety (see
[sampling-basics-temperature-and-randomness-control.md](sampling-basics-temperature-and-randomness-control.md));
**hallucination** is a direct, structural consequence of prediction-based generation having no
built-in fact-verification mechanism, mitigated (not eliminated) by real, specific techniques (see
[why-hallucination-happens-it-predicts-it-doesnt-know.md](why-hallucination-happens-it-predicts-it-doesnt-know.md));
and an LLM's fundamentally **probabilistic** nature — even at temperature 0 — means building and
testing on top of one genuinely requires a different approach than traditional, deterministic
software.
