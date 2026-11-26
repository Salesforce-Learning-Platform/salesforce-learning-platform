# 📏 Normalisation

## 📚 Overview

A badly designed table stores the same fact many times, and sooner or later the copies disagree. **Normalisation** is the method for finding that redundancy and removing it by splitting tables, without losing information. The practical introduction, with the first three normal forms by example, is [normalization.md](../../../backend/database-design-and-modeling/normalization.md). This module supplies the **theory** behind it, so that you can design and check schemas with reasoning instead of intuition, and know what each step guarantees and what it can cost.

The module starts with **functional dependencies**: what they say, Armstrong's axioms, the closure of a set of attributes, finding candidate keys, and the minimal cover of a set of dependencies. It then states the **normal forms** (1NF, 2NF, 3NF, and Boyce-Codd normal form) in terms of dependencies, tests them with a small program, and normalizes a clinic's appointment table, both as theory and in SQLite, where one update to the wide table leaves a doctor in two rooms. It ends with **decomposition**: what makes a split lossless (and how a lossy one invents rows), the chase test, the synthesis algorithm that builds a dependency-preserving 3NF design, the algorithm that builds a BCNF design, and an example where BCNF can no longer enforce a business rule. The code was run on CPython 3.9 on a Mac (macOS, Apple silicon) with SQLite 3.54, and the algorithms were checked against a definition that does not use them, on thousands of random inputs.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Define functional dependencies, recognise trivial ones, and reason with Armstrong's axioms and their derived rules.
- Compute the closure of a set of attributes, and use it to find all candidate keys and to compute a minimal cover.
- State 1NF, 2NF, 3NF, and BCNF and find which dependency violates each.
- Normalize a realistic table, and show which update anomalies disappear.
- Decide whether a decomposition is lossless, with the two-part criterion or the chase, and explain what a lossy join does to the data.
- Build a 3NF design by synthesis and a BCNF design by decomposition, and weigh BCNF against dependency preservation.

## 📋 Prerequisites

- [The Relational Model](../the-relational-model/README.md): relations, keys, and integrity constraints.
- Helpful: the practical [normalization.md](../../../backend/database-design-and-modeling/normalization.md), which this module explains in depth.
- Basic Python reading ability: functions, sets, loops, and the standard library.
- Comfort with simple set notation (subset, union, difference).

## 📂 Module Contents

| File | Description |
|------|-------------|
| [functional-dependencies.md](functional-dependencies.md) | Functional dependencies, Armstrong's axioms, attribute closure, candidate keys, and minimal covers, on a clinic's appointment table |
| [normal-forms.md](normal-forms.md) | Anomalies, 1NF to BCNF, a program that finds violations, normalizing the clinic in theory and in SQLite, and a 3NF table that is not in BCNF |
| [decomposition.md](decomposition.md) | Lossless and lossy joins, the chase, 3NF synthesis, BCNF decomposition, and the cost of losing a dependency |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [functional-dependencies.md](functional-dependencies.md) and [normal-forms.md](normal-forms.md) if you are preparing for exams or interviews: computing a closure, listing candidate keys, and saying which normal form a table satisfies are the standard questions. Practise them by hand first and check yourself with the code.

**Skim** the chase in [decomposition.md](decomposition.md) if you only need the two-part lossless criterion, but read its last example: it shows why a design that is perfect by one measure can fail to enforce a rule of the business.

## 🧠 Knowledge Check

<details>
<summary>A relation R(A, B, C, D) has the dependencies A → B and B → C. What are its candidate keys, which normal form is it in, and how would you decompose it?</summary>

No dependency determines A or D, so both belong to every key, and the closure of {A, D} is {A, B, C, D}: the only candidate key is **{A, D}**. The dependency A → B has a left side that is only *part* of that key, and B is not prime, so R is **not even in 2NF** (it is only in 1NF). Synthesis from the minimal cover {A → B, B → C} gives the tables **(A, B)** and **(B, C)**; neither contains a key of R, so a table **(A, D)** is added. All three are in BCNF, and the decomposition is lossless and preserves both dependencies. [decomposition.md](decomposition.md) contains the algorithm.

</details>

<details>
<summary>Students take courses with instructors; a student has one instructor per course, and each instructor teaches only one course. Why is the table (student, course, instructor) in 3NF but not in BCNF, and what does splitting it cost?</summary>

The dependencies are {student, course} → instructor and instructor → course, so the candidate keys are {student, course} and {student, instructor}: every attribute is **prime**. For instructor → course the left side is not a superkey, which violates **BCNF**, but the right side is prime, so **3NF** is satisfied. Decomposing into (instructor, course) and (instructor, student) removes the repetition of each instructor's course and is lossless, but no new table holds student, course, and instructor together, so the rule "one instructor per student and course" can no longer be enforced by keys: the tables accept a student with two instructors for the same course. Keeping the 3NF table (and its redundancy), or enforcing the rule with a trigger or application code, are the alternatives.

</details>

## 📚 References

- [Wikipedia: Database normalization](https://en.wikipedia.org/wiki/Database_normalization), [Functional dependency](https://en.wikipedia.org/wiki/Functional_dependency), [Armstrong's axioms](https://en.wikipedia.org/wiki/Armstrong%27s_axioms), and [Canonical cover](https://en.wikipedia.org/wiki/Canonical_cover): dependencies and reasoning about them.
- [Wikipedia: First normal form](https://en.wikipedia.org/wiki/First_normal_form), [Second normal form](https://en.wikipedia.org/wiki/Second_normal_form), [Third normal form](https://en.wikipedia.org/wiki/Third_normal_form), and [Boyce-Codd normal form](https://en.wikipedia.org/wiki/Boyce%E2%80%93Codd_normal_form).
- [Wikipedia: Lossless join decomposition](https://en.wikipedia.org/wiki/Lossless_join_decomposition) and [Chase (algorithm)](https://en.wikipedia.org/wiki/Chase_(algorithm)).
- [GeeksforGeeks: Introduction to Database Normalization](https://www.geeksforgeeks.org/dbms/introduction-of-database-normalization/), [Types of Functional Dependencies](https://www.geeksforgeeks.org/dbms/types-of-functional-dependencies-in-dbms/), [Attribute Closure and Candidate Keys](https://www.geeksforgeeks.org/dbms/finding-attribute-closure-and-candidate-keys-using-functional-dependencies/), [Canonical Cover](https://www.geeksforgeeks.org/dbms/canonical-cover-of-functional-dependencies-in-dbms/), [Boyce-Codd Normal Form](https://www.geeksforgeeks.org/dbms/boyce-codd-normal-form-bcnf/), and [Lossless Decomposition](https://www.geeksforgeeks.org/dbms/lossless-decomposition-in-dbms/): overviews and practice questions.

## ➡️ Continue Your Learning Path

Continue to Transactions and ACID, the next module of this section: a well-designed schema keeps each fact in one place; transactions keep those facts correct while many operations run at once and when something fails in the middle.
