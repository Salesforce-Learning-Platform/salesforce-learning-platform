# Using AI Tools Effectively

## What AI Coding Assistants Are Good At

Modern AI coding assistants are language models trained on large volumes of text and code. They
are strongest at pattern-completion tasks — producing plausible, often correct code for
well-represented, well-specified problems — and weaker at tasks requiring genuinely novel
reasoning about a specific, unfamiliar codebase's actual behavior, or verified real-world facts
they weren't reliably trained on.

Tasks where they tend to help most:

- **Boilerplate and repetitive code**: generating a component skeleton, a CRUD API's basic
  structure, repetitive test cases following an established pattern.
- **Explaining unfamiliar code or error messages**: a fast first pass at understanding what a
  function does or what a stack trace means, to orient before you dig in yourself.
- **Drafting documentation or comments** for code you've already written and understand.
- **Exploring alternative approaches** to a problem you already understand well enough to evaluate
  the suggestions critically.
- **Learning**: asking a concept to be explained multiple ways, or generating small examples to
  experiment with.

Tasks where they're a poor fit, or actively risky, without heavy verification:

- Anything requiring accurate knowledge of your specific codebase's actual runtime behavior,
  unless the tool has genuinely read that code (rather than guessing from a description).
- Security-sensitive logic (authentication, authorization, payment handling), where a subtly wrong
  suggestion can be a serious vulnerability rather than a visible bug.
- Anything where you cannot yet evaluate whether the output is correct — using an assistant to
  write code in a domain you don't understand at all removes your ability to catch its mistakes.

## Getting Useful Output

The quality of AI-assisted output correlates strongly with the quality and specificity of the
input:

- **Provide real context**: actual error messages, actual relevant code, actual constraints — not
  a vague paraphrase of the problem.
- **Be specific about constraints**: language/framework version, existing patterns in the
  codebase, performance or security requirements.
- **Ask for reasoning, not just code**, when you don't already understand the approach — "explain
  why this works" is often more valuable than the code itself.
- **Iterate in small steps** rather than requesting a large, multi-file change you can't easily
  review in one pass.

## Common Mistakes

- Treating a vague, underspecified prompt's confident-sounding output as reliable simply because
  it's confident and well-formatted — confidence in phrasing is not evidence of correctness.
- Asking for a solution to a problem you don't understand well enough to verify, and shipping
  whatever comes back.
- Pasting an entire unfamiliar file and asking "what's wrong with this" instead of first narrowing
  down what you already know or suspect — a more specific question generally produces a more
  useful answer.

## Next

Continue to
[validating-ai-output-and-engineering-responsibility.md](validating-ai-output-and-engineering-responsibility.md)
to understand why none of this removes the need for your own review.
