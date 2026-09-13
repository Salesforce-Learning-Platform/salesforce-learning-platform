# Reading Documentation

## Purpose

Every engineer spends a large fraction of their time reading documentation — API references,
library guides, RFCs, error messages, other people's code comments. Reading it efficiently and
correctly is a distinct, learnable skill, not just a byproduct of experience. This module makes
that skill explicit, closing out the Foundations sequence.

## Learning Objectives

- Identify which of the four common documentation types you're reading, and adjust how you read
  accordingly.
- Locate the specific answer you need in a large reference document, without reading it linearly.
- Evaluate whether documentation is current, authoritative, and applicable to your exact version.
- Know when documentation is genuinely wrong or outdated, versus when you've misread it.

## Files in This Module

| File | Covers |
|---|---|
| [types-of-documentation.md](types-of-documentation.md) | Tutorials, how-to guides, reference, and explanation — and why conflating them causes frustration |
| [navigating-and-evaluating-documentation.md](navigating-and-evaluating-documentation.md) | Efficiently finding what you need, and judging whether a source is trustworthy and current |

## When to Deep-Dive vs. Skim

Every learner should read [types-of-documentation.md](types-of-documentation.md) at least once —
recognizing the four types is the single highest-leverage idea in this module and changes how you
approach every technical document afterward. Skim
[navigating-and-evaluating-documentation.md](navigating-and-evaluating-documentation.md) if you
already read documentation daily, but revisit it the next time you catch yourself following advice
from an outdated blog post instead of the current official docs.

## Quick Knowledge Check

<details>
<summary>You want to learn a new library from scratch, step by step. Which documentation type should you look for?</summary>

A tutorial — learning-oriented, guided, hands-on. A reference page (which just lists every
function and parameter) is the wrong tool for this and will feel needlessly overwhelming until you
already have a mental model to hang it on. See
[types-of-documentation.md](types-of-documentation.md).

</details>

<details>
<summary>Why might code copied exactly from a Stack Overflow answer fail against the current version of a library?</summary>

Documentation and community answers age; a library's API can change between major versions.
Checking the version the answer was written against — and comparing it to the official reference
for your installed version — is part of evaluating a source, not just trusting it. See
[navigating-and-evaluating-documentation.md](navigating-and-evaluating-documentation.md).

</details>

## References

- [Diátaxis](https://diataxis.fr/) — the documentation framework this module's four-type model is
  based on
- [Semantic Versioning 2.0.0](https://semver.org/) — the versioning standard referenced when
  evaluating whether documentation matches your installed version

## Continue Your Learning Path

This is the last module in the Foundations sequence. Continue to
[HTML](../../html/semantic-html-and-browser-rendering/) — see the
[Frontend learning path](../../README.md) for the full sequence.
