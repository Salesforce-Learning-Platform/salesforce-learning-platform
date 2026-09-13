# Types of Documentation

## Why This Distinction Matters

A huge amount of documentation frustration comes from using the wrong *type* of document for the
question you actually have — reading a reference page top-to-bottom like a tutorial, or hunting
through a tutorial for the one parameter detail that only lives in the reference. The
[Diátaxis](https://diataxis.fr/) framework names four distinct types, each answering a genuinely
different kind of question.

## The Four Types

| Type | Answers | Example |
|---|---|---|
| **Tutorial** | "Teach me, step by step" | "Getting Started with React" walkthrough |
| **How-to guide** | "How do I accomplish this specific task?" | "How to add authentication to your app" |
| **Reference** | "What exactly does this do?" | A complete list of every function, its parameters, and return values |
| **Explanation** | "Why does this work this way?" | An article on why React re-renders when state changes |

```text
                Practical                          Theoretical
              ┌──────────────────┬──────────────────┐
   Learning   │     Tutorial      │    Explanation    │
              ├──────────────────┼──────────────────┤
   Working    │   How-to guide    │     Reference     │
              └──────────────────┴──────────────────┘
```

## Matching the Type to Your Actual Need

- **New to a topic entirely?** Look for a **tutorial** — you want guided hands-on steps, not a
  wall of every possible option.
- **Know roughly what you want, need the exact steps for one task?** Look for a **how-to guide** —
  focused, task-oriented, assumes you already have the basics.
- **Need to confirm an exact parameter, return type, or edge-case behavior?** Go straight to the
  **reference** — don't read it linearly; jump directly to the relevant entry.
- **Confused about *why* something behaves the way it does, beyond just how to use it?** Look for
  an **explanation** or conceptual guide — this is what most of this platform's own learning
  content is.

## Recognizing Well-Organized Documentation

Mature documentation (MDN, most major frameworks' official docs) is often explicitly organized
along these lines — separate "Guides," "Tutorial," and "API Reference" sections. Recognizing this
structure lets you jump directly to the right section instead of searching the whole site for
something that's actually just one click away in the correct category.

## Common Mistakes

- Reading an entire API reference top-to-bottom when you only needed one function's exact
  signature — reference docs are meant to be searched, not read linearly.
- Following a tutorial's exact steps and getting stuck when your situation differs slightly,
  instead of switching to a how-to guide or reference once you're past the pure-learning stage.
- Treating a conceptual explanation as if it were a precise reference for exact syntax — it's
  optimized for understanding *why*, and may simplify or omit exact detail on purpose.

## Next

Continue to
[navigating-and-evaluating-documentation.md](navigating-and-evaluating-documentation.md) to build
the skill of finding the right document quickly and judging whether to trust what it says.
