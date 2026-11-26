# 🗄️ Introduction to DBMS

## 📚 Overview

Almost every application keeps data that must survive restarts, be shared, and stay correct while it changes. This module is about the software that makes that possible, the **database management system (DBMS)**, and about the first step of building a database: deciding what to store and how it is related. It comes before the study of the relational model itself, so it assumes no knowledge of databases.

It starts by watching plain files fail: the same fact stored twice and disagreeing, bad data accepted without complaint, two writers losing an update, a crash that makes money disappear, and every new question needing a new program, each with a short experiment, followed by what a database does instead, including a demonstration that a half-written database file is restored byte for byte after a crash. It then explains **data modeling**: the conceptual, logical, and physical stages of design, the external, conceptual, and internal levels of a running database, data independence (demonstrated with a view and with indexes), and the main families of data models. It ends with the **entity-relationship model**: entities, attributes, relationships, cardinality, participation, and weak entities, a diagram of a university, the rules that turn a diagram into tables and constraints, and an exhaustive check that those constraints accept exactly what each kind of relationship allows. Every example uses **SQLite**, which ships with Python, so nothing needs to be installed; the code was run on CPython 3.9 on a Mac (macOS, Apple silicon) with SQLite 3.54.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain what goes wrong when shared, changing data lives in plain files (update anomalies, unchecked data, lost updates, partial updates, and one-off query code), and what a database provides instead.
- Distinguish a database, a DBMS, and a database system, list the services of a DBMS, and judge when a plain file is enough.
- Describe the conceptual, logical, and physical stages of data modeling and the external, conceptual, and internal levels of a database, and demonstrate logical and physical data independence.
- Compare the main families of data models in outline.
- Draw an entity-relationship model with entities, attributes of different kinds, relationships, cardinality, participation, and weak entities, in crow's foot notation.
- Turn an ER model into relational tables, using primary keys, foreign keys, `UNIQUE`, `NOT NULL`, and cascading deletes, and say what such constraints cannot express.

## 📋 Prerequisites

- Basic Python reading ability: functions, loops, dictionaries, and the standard library.
- Helpful, not required: [Introduction to Relational Databases](../../../backend/sql-fundamentals/introduction-to-relational-databases.md) for a first practical look at tables and SQL.
- Helpful for the first lesson: the [File Systems](../../operating-systems/file-systems/README.md) module (the write-and-rename pattern) and the race conditions of [Deadlocks and Concurrency](../../operating-systems/deadlocks-and-concurrency/README.md).
- No earlier knowledge of databases or modeling is assumed.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [why-databases-exist.md](why-databases-exist.md) | What goes wrong with plain files (redundancy, bad data, lost updates, crashes, ad hoc queries), shown by experiments and solved with SQLite, what a DBMS is, and when a file is enough |
| [data-modeling.md](data-modeling.md) | Stages of data modeling, the three levels of a database, logical and physical data independence, families of data models, and a practical order of work |
| [entity-relationship-model.md](entity-relationship-model.md) | Entities, attributes, relationships, cardinality, participation, weak entities, crow's foot notation, mapping a diagram to tables, and an exhaustive check of the mapping constraints |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [entity-relationship-model.md](entity-relationship-model.md) if you are preparing for exams or design interviews: drawing a model from a description and turning it into tables is the classic exercise, and the cardinality and participation rules decide whether the answer is right. [why-databases-exist.md](why-databases-exist.md) is worth running line by line if you have never seen why transactions and constraints matter.

**Skim** [data-modeling.md](data-modeling.md) if you have designed schemas before, but do not skip the difference between the stages of design and the levels of a running database, which is easy to confuse.

## 🧠 Knowledge Check

<details>
<summary>A program keeps account balances in one file per account and moves money by rewriting one file and then the other. Name two different failures this design allows, and what a database does about each.</summary>

A crash between the two writes loses or creates money: a database groups both changes into a **transaction** that happens completely or not at all, and recovers an interrupted transaction from its journal when it is next opened. Two transfers running at the same time can both read an old balance and overwrite each other's result, a **lost update**: the database coordinates the writers (SQLite, for example, lets one writer proceed at a time while the others queue). A third answer is bad data, such as a negative balance, which a database can refuse with a `CHECK` constraint that holds for every program that writes to it. [why-databases-exist.md](why-databases-exist.md) demonstrates all three.

</details>

<details>
<summary>A library lends copies of books to members. A member can borrow many copies over time, a copy can be lent to only one member at a time, and the library records when each loan starts and ends. How would you model this, and how can a database enforce the "one member at a time" rule?</summary>

Lending is a **many-to-many** relationship between *member* and *book copy* over time, and it has attributes (the loan and return dates), so it becomes an entity of its own, **Loan**, with a foreign key to the member and one to the copy. "A copy is lent to one member at a time" does not mean one loan per copy for ever; it means at most one **open** loan per copy. A plain `UNIQUE (copy_id)` would be wrong, but a unique index that covers only open loans does the job, for example `CREATE UNIQUE INDEX one_open_loan_per_copy ON loan (copy_id) WHERE returned_on IS NULL` ([SQLite: partial indexes](https://www.sqlite.org/partialindex.html)): a second open loan for the same copy is rejected, and a new one is accepted after the return.

</details>

## 📚 References

- [Wikipedia: Database](https://en.wikipedia.org/wiki/Database), [Database model](https://en.wikipedia.org/wiki/Database_model), [Data modeling](https://en.wikipedia.org/wiki/Data_modeling), [Three-schema approach](https://en.wikipedia.org/wiki/Three-schema_approach), [Data independence](https://en.wikipedia.org/wiki/Data_independence), [Entity-relationship model](https://en.wikipedia.org/wiki/Entity%E2%80%93relationship_model), and [Associative entity](https://en.wikipedia.org/wiki/Associative_entity).
- Peter Chen, "The Entity-Relationship Model: Toward a Unified View of Data", *ACM Transactions on Database Systems*, 1976: the paper that introduced the ER model.
- SQLite documentation: [Atomic commit](https://www.sqlite.org/atomiccommit.html), [File locking and concurrency](https://www.sqlite.org/lockingv3.html), [Foreign key support](https://www.sqlite.org/foreignkeys.html), [EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html), [Appropriate uses](https://www.sqlite.org/whentouse.html), [SQL features that are not implemented](https://www.sqlite.org/omitted.html), and [Partial indexes](https://www.sqlite.org/partialindex.html).
- [Python docs: `sqlite3`](https://docs.python.org/3/library/sqlite3.html) and the [Mermaid entity-relationship diagram syntax](https://mermaid.js.org/syntax/entityRelationshipDiagram.html).
- [GeeksforGeeks: Difference between File System and DBMS](https://www.geeksforgeeks.org/dbms/difference-between-file-system-and-dbms/), [Physical and Logical Data Independence](https://www.geeksforgeeks.org/dbms/physical-and-logical-data-independence/), [Introduction of ER Model](https://www.geeksforgeeks.org/dbms/introduction-of-er-model/), [Weak Entity Set in ER Diagrams](https://www.geeksforgeeks.org/dbms/weak-entity-set-in-er-diagrams/), and [Mapping from ER Model to Relational Model](https://www.geeksforgeeks.org/dbms/mapping-from-er-model-to-relational-model/): overviews and practice questions.

## ➡️ Continue Your Learning Path

Continue to [The Relational Model](../the-relational-model/README.md), the next module of this section: the tables that the entity-relationship model produced are relations, and the next module studies their keys, their integrity rules, and the operations that combine them, building on the practical [SQL Fundamentals](../../../backend/sql-fundamentals/README.md) lessons.
