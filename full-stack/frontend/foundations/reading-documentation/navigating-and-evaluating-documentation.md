# Navigating and Evaluating Documentation

## Finding What You Need Without Reading Everything

- **Use in-page search (`Ctrl`/`Cmd`+`F`) aggressively** on reference pages — most documentation
  sites are structured so the term you're looking for appears as a heading or a parameter name.
- **Check the table of contents or sidebar first.** Well-structured docs mirror the four-type
  organization from [types-of-documentation.md](types-of-documentation.md); knowing which type you
  want tells you which part of the sidebar to open.
- **Read function/method signatures before prose.** In reference documentation, the signature
  (name, parameters, return type) usually answers the question faster than the paragraph
  describing it.
- **Use the site's actual search**, not just a general web search — official documentation search
  is usually scoped correctly and versioned, where a general search often surfaces outdated
  third-party content first.

## Evaluating Whether to Trust What You're Reading

Not all documentation is equally current or authoritative, and mixing sources without checking
this is a common source of subtly broken code:

| Question | Why it matters |
|---|---|
| **Is this official, or a third-party summary?** | Official docs are maintained alongside the actual software; third-party posts can silently go stale |
| **Does the version match what I have installed?** | An API can change across major versions — see [Semantic Versioning](https://semver.org/), where a major-version bump signals exactly this kind of breaking change |
| **When was this last updated?** | A tutorial from several years ago may predate significant changes to the tool it covers |
| **Does it match what the reference documentation says?** | A blog post or forum answer that contradicts the current official reference should lose, not win, when they disagree |

## A Practical Workflow

1. Identify what type of question you have (learning, task, exact detail, or "why") — see
   [types-of-documentation.md](types-of-documentation.md).
2. Go to the official documentation for the exact tool/library and version you're using.
3. Use the sidebar/search to jump directly to the relevant section rather than reading linearly.
4. If official docs don't fully answer it, use community sources (Stack Overflow, GitHub issues)
   — but verify any code or claim against the official reference before trusting it, especially if
   the community answer is old.

## When Documentation Is Actually Wrong

Documentation can genuinely be outdated, incomplete, or incorrect — this isn't rare, particularly
for fast-moving libraries or auto-generated reference pages that lag behind code changes. Signs
worth taking seriously:

- The documented behavior doesn't match what you observe when you actually run the code.
- Multiple official sources (release notes, migration guides, the changelog) contradict the page
  you're reading.
- The page itself is marked deprecated, or references a version far older than the one you have.

The fix is the same discipline used everywhere else in this platform: don't take a single source's
claim as certain when it's easy to verify directly — run the code, check the changelog, or check
an adjacent official page before concluding the documentation (or your understanding of it) is
wrong.

## Common Mistakes

- Assuming documentation is permanently correct simply because it's official — it can lag behind
  the actual current release, especially for a library between versions.
- Trusting a highly-upvoted but old community answer over current official documentation without
  checking dates or version applicability.
- Giving up on official docs after one confusing read, rather than switching to a different
  documentation type (a tutorial instead of a reference, or vice versa) that better answers the
  actual question.

## Module Summary

Across this module: documentation comes in four genuinely different types — tutorial, how-to,
reference, explanation — and matching the type to your actual question is the fastest path to an
answer (see [types-of-documentation.md](types-of-documentation.md)); and finding information
efficiently plus evaluating whether a source is current and authoritative (checking versions,
official status, and recency) protects you from silently following outdated or incorrect guidance.

This closes the Foundations sequence — see the
[Foundations learning path](../README.md) for what you've covered, and the
[Frontend learning path](../../README.md) for what comes next.
