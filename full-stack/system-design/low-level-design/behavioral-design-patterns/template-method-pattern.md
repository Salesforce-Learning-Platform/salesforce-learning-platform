# 📋 Template Method Pattern

## The Problem: Duplicated Algorithm Structure Across Subclasses

```python
# WITHOUT Template Method - the SAME overall analysis sequence is
# DUPLICATED across every document type, with only small pieces
# genuinely differing
class PDFProcessor:
    def analyze(self):
        self._open_file()
        self._extract_pdf_text()   # PDF-specific
        self._run_analysis()
        self._close_file()

class DOCProcessor:
    def analyze(self):
        self._open_file()
        self._extract_doc_text()   # DOC-specific
        self._run_analysis()
        self._close_file()
```

Per Refactoring.guru's own framing: this is exactly the problem behind a real "data mining
application had three document-processing classes (PDF, DOC, CSV) that shared common analysis logic
but duplicated it across implementations" — the *overall sequence* of steps is genuinely identical
across every case, yet it's fully rewritten in each subclass.

## The Pattern

```python
class DocumentProcessor:
    def analyze(self):   # the TEMPLATE METHOD - defines the FIXED
        self._open_file()    # sequence, never overridden
        self._extract_text()   # a step SUBCLASSES must implement
        self._run_analysis()
        self._close_file()

    def _open_file(self): print("Opening file...")
    def _extract_text(self): raise NotImplementedError   # ABSTRACT step
    def _run_analysis(self): print("Running shared analysis...")
    def _close_file(self): print("Closing file...")

class PDFProcessor(DocumentProcessor):
    def _extract_text(self):
        print("Extracting text from PDF...")   # ONLY this differs

class DOCProcessor(DocumentProcessor):
    def _extract_text(self):
        print("Extracting text from DOC...")
```

The `analyze()` method — the **template method** — defines the fixed overall sequence exactly
*once*, in the base class. Each subclass implements only the specific step that genuinely differs
(`_extract_text()`), while every other step (`_open_file`, `_run_analysis`, `_close_file`) is shared,
written only once.

## Three Kinds of Steps

```
ABSTRACT step  → MUST be implemented by every subclass (like
                 _extract_text above) - no default behavior exists

DEFAULT step    → has a REASONABLE default implementation, but CAN
                 be overridden if a specific subclass needs to

HOOK             → an EMPTY, optional extension point - subclasses
                 may override it, but most won't need to
```

This three-way distinction is genuinely useful for designing a template method thoughtfully —
deciding which steps are truly mandatory, which have sensible defaults, and which are purely
optional extension points shapes how flexible (or rigid) the resulting template actually is.

## A Real, Physical Analogy: Standardized House Construction

```
A house-building plan has a FIXED overall sequence (foundation,
framing, plumbing, roofing) that never changes - but specific
EXTENSION POINTS let an owner customize details (wall color,
fixture style) within that same, fixed overall structure.
```

This is directly Refactoring.guru's own real-world analogy — genuinely capturing the pattern's
essence: a stable, shared skeleton, with specific, well-defined places where variation is
deliberately allowed.

## Template Method vs. Strategy: the Final Distinction in This Domain

```
TEMPLATE METHOD: uses INHERITANCE - the algorithm's skeleton is
  fixed at the CLASS level (static, decided at compile/definition
  time)

STRATEGY: uses COMPOSITION - a DIFFERENT algorithm can be swapped
  in at RUNTIME, dynamically
```

Per Refactoring.guru's own direct comparison — this is the final, important distinction to close out
this module and this entire design-patterns sequence: Template Method fixes an algorithm's *shape*
through inheritance, while [Strategy](strategy-pattern.md) swaps an algorithm's *entire
implementation* through runtime composition.

## Common Mistakes

- Duplicating a shared algorithm's overall sequence across multiple subclasses instead of extracting
  it once into a template method in a shared base class.
- Making every step abstract (forcing every subclass to implement everything) when some steps
  genuinely have a sensible, reusable default.
- Confusing Template Method's compile-time, inheritance-based structure with Strategy's
  runtime-swappable, composition-based one — the two solve related but genuinely different problems.

## Module Summary

Across this module: **Observer** notifies a dynamic, unknown set of subscribers about a publisher's
state changes, the exact pattern underlying event listeners already used throughout this repository
(see [observer-pattern.md](observer-pattern.md)); **Strategy** lets a client swap between
independent, interchangeable algorithms at runtime, directly applying Open-Closed to algorithm
selection (see [strategy-pattern.md](strategy-pattern.md)); **State** lets an object's behavior
change based on its own internal state, with each state genuinely aware of — and able to trigger
transitions to — other states, precisely distinguished from Strategy's mutual independence (see
[state-pattern.md](state-pattern.md)); **Command** turns a request itself into a genuine object,
enabling queuing, logging, and undo/redo in ways a plain method call never could (see
[command-pattern.md](command-pattern.md)); and **Template Method** fixes a shared algorithm's
overall sequence once in a base class, letting subclasses implement only the specific steps that
genuinely differ, distinguished from Strategy by its inheritance-based, compile-time nature (see
[template-method-pattern.md](template-method-pattern.md)) — completing this domain's coverage of
creational, structural, and behavioral design patterns, ahead of applying all of it directly in
[LLD Problem Solving and Machine Coding](../lld-problem-solving-and-machine-coding/), the final
module in this domain.
