# 📐 Output Formatting Instructions: Making Responses Predictable

## Tell the Model What TO Do, Not What Not to Do

```
LESS EFFECTIVE: "Do not use markdown in your response"

MORE EFFECTIVE: "Your response should be composed of smoothly
flowing prose paragraphs."
```

This is a genuinely counterintuitive but well-documented, real finding: a **positive** instruction
(describing the format actually wanted) is consistently more reliable than a **negative** one
(describing only what to avoid). Telling a model what to actively produce gives it a clear target;
telling it only what *not* to do leaves the actual desired alternative unspecified.

## Using Explicit Format Indicators

```
"Write the prose sections of your response inside
<response> tags."
```

Wrapping a request for a specific output section in explicit tags — the same technique
[few-shot-examples-to-force-pattern-learning.md](few-shot-examples-to-force-pattern-learning.md)
used to distinguish examples from instructions — works just as well for marking exactly where a
specific kind of content should appear, making the expected structure genuinely explicit rather
than implied.

## Matching Your Prompt's Own Style to the Desired Output

If a prompt itself is written in heavy markdown (bullet points, bold text, headers), the response
is more likely to mirror that same style back — this is a real, practical lever: removing markdown
from the prompt itself, when a markdown-free response is genuinely wanted, can reduce the amount of
markdown the model produces in return, since the prompt's own style acts as an implicit signal.

## Writing Detailed Formatting Guidance for a Specific Need

```
When writing reports or long-form content, write in clear, flowing
prose using complete paragraphs and sentences. Reserve markdown
primarily for `inline code`, code blocks, and simple headings.
Avoid **bold** and *italics*. Do NOT use bullet points or numbered
lists unless presenting genuinely discrete items, or the reader
explicitly requests a list.
```

For a genuinely specific, recurring formatting need (an application that always needs prose, never
bullet-point-heavy output, for instance), a detailed, explicit formatting instruction — stated once,
consistently, as part of the system prompt — is far more reliable than hoping the model infers the
right style from context each time.

## A Real Caveat: Don't Over-Correct

Formatting preferences can shift between model versions — a block of instructions specifically
written to suppress excessive markdown for one model generation might unnecessarily suppress
structure a *newer* model generation would have gotten right without it. Formatting instructions,
like any prompt, benefit from being periodically revisited rather than treated as a permanent,
set-once configuration.

## Common Mistakes

- Relying primarily on negative instructions ("don't do X") instead of positive ones ("do Y"),
  producing less reliable, more inconsistent formatting results.
- Writing detailed, prescriptive formatting instructions once and never revisiting them, even as
  the underlying model (and its own default formatting tendencies) changes over time.
- Forgetting that the prompt's own formatting style itself sends an implicit signal — a heavily
  markdown-formatted prompt nudges toward a heavily markdown-formatted response, even without
  explicit instruction either way.

## Module Summary

Across this module: **clear, explicit instructions**, tested against the "golden rule" of a
context-free colleague's understanding, are the foundation every other technique builds on (see
[writing-clear-instructions.md](writing-clear-instructions.md)); **few-shot examples** — relevant,
diverse, and structurally distinguished from instructions — reliably steer output format and tone
through demonstration rather than description alone (see
[few-shot-examples-to-force-pattern-learning.md](few-shot-examples-to-force-pattern-learning.md));
**chain-of-thought prompting**, a general, provider-agnostic technique distinct from a model's
dedicated thinking capability, improves accuracy on genuinely multi-step reasoning tasks (see
[chain-of-thought-high-level-awareness.md](chain-of-thought-high-level-awareness.md)); and
**controlling output format** works best through positive instructions, explicit tags, and matching
the prompt's own style to the desired result, rather than relying on negative instructions alone.
