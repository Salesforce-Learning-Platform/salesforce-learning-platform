# 📦 What Are Data Structures?

## A New Domain, Focused on the Building Blocks Underneath Everything

Every domain in this repository so far has used data structures constantly — an array of comments,
a hash map of session data, a tree of UI components — without ever stopping to examine *why* a
particular structure was chosen, or what alternatives existed. This domain does exactly that: a
genuine, ground-up look at the data structures and algorithms underlying software built throughout
this entire repository.

## The Core Definition

```
A DATA STRUCTURE is a specific way of ORGANIZING data in memory so
it can be accessed and modified EFFICIENTLY, for a GIVEN set of
operations.
```

The key phrase is "for a given set of operations" — no single data structure is universally best;
each one makes deliberate trade-offs, genuinely faster at some operations and genuinely slower at
others.

## A Concrete Illustration: Storing a List of Usernames

```python
# An ARRAY: usernames stored in contiguous memory, in order
usernames = ["alice", "bob", "carol", "dave"]

# A SET: usernames stored for fast MEMBERSHIP checking, unordered
usernames_set = {"alice", "bob", "carol", "dave"}
```

```
Checking "is 'carol' in this list?" with the ARRAY: potentially
CHECK EVERY element, one by one, until found (or not).

The SAME check with the SET: a near-instant, DIRECT lookup,
regardless of how many usernames exist.
```

This is a genuinely concrete illustration of the core lesson: the *exact same data* ("a list of
usernames"), organized two different ways, has genuinely different performance characteristics for
the exact same operation — this performance difference is precisely what
[Time and Space Complexity](../time-and-space-complexity/), the next module in this domain, gives a
precise, formal way to actually measure.

## Data Structures Already Used Throughout This Repository

```
ARRAY   → JavaScript's own Array, Python's list - already used
          constantly throughout this repository's Frontend and
          Backend domains

HASH MAP → JavaScript's Object/Map, Python's dict - directly
          underlying every key-value lookup already covered,
          including Redis's own core data model (per Caching:
          Local and Redis, earlier in this repository)

TREE     → the DOM itself (per this repository's Frontend domain),
          a file system's directory structure, a database index
```

Recognizing that these structures were already in constant, everyday use throughout this
repository — just without their formal names and trade-offs being examined explicitly — is a
genuinely useful realization at the start of this domain.

## Two Fundamental Categories

```
LINEAR structures    → elements arranged in SEQUENCE (arrays,
                        linked lists, stacks, queues)

NON-LINEAR structures → elements arranged in HIERARCHICAL or
                        NETWORKED relationships (trees, graphs,
                        heaps)
```

This domain's own module sequence follows roughly this progression — starting with linear
structures (this module through Stacks and Queues), then moving to non-linear ones (Trees, Graphs,
Heaps) later in the domain.

## Why This Matters, Even With High-Level Languages Handling the Details

```
Modern languages provide BUILT-IN data structures (Python's list,
dict; JavaScript's Array, Map) - but choosing WHICH one to use for
a given problem, and understanding WHY one choice performs
dramatically better than another at real scale, remains a
genuinely essential skill.
```

## Common Mistakes

- Reaching for the same, familiar data structure (usually an array) for every problem, regardless
  of what operations the actual use case genuinely needs to perform efficiently.
- Assuming a language's built-in data structures are all equally fast for every operation, when
  each one is deliberately optimized for specific access patterns.
- Treating data structure choice as a minor implementation detail rather than a decision with real,
  measurable performance consequences at scale.

## ➡️ Next

Continue to [what-are-algorithms.md](what-are-algorithms.md) to see the other essential half of
this domain: the actual procedures that operate on these structures.
