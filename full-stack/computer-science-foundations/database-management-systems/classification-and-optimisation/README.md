# 🧭 Database Classification and Optimisation

## 📚 Overview

There are many kinds of database, and a database of any kind is only as fast as the way it finds data. This module closes the Database Management Systems section with both ideas: how databases are **classified**, by data model, workload, storage layout, deployment, and distribution, and how they are **made fast**, with indexes, query plans, and the choices an optimizer makes. It works at the level of concepts, checked with small experiments, and links to the practical SQL, MongoDB, and system design lessons elsewhere in this repository instead of repeating them.

It starts by storing one small bookshop in five data models (relational, key-value, document, wide-column, and graph) and counting what each must read to answer the same questions, then compares row and column storage and looks at consistency across copies. It next builds a **B+ tree**, measures the real B-trees inside SQLite, and introduces log-structured merge-trees. It ends with **query optimization**: reading plans, knowing which queries can use an index, seeing why a scan can beat an index, comparing join algorithms and join orders, and avoiding two common sources of wasted work. The code was run on CPython 3.9 on a Mac (macOS, Apple silicon) with SQLite 3.54, and the toy stores, the tree, and the algorithms were checked against independent references on random data.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Describe a database along several independent axes: data model, workload, storage layout, deployment, distribution, and consistency.
- Explain what relational, key-value, document, wide-column, and graph databases make easy and hard, and why labels such as NoSQL do not settle what a product can do.
- Explain the CAP theorem, eventual consistency, and read and write quorums, and where their guarantees stop.
- Explain how B+ trees work, how clustered, secondary, and covering indexes differ, and how LSM trees trade read cost for cheaper writes.
- Read a query plan, and predict which conditions can use a multi-column index.
- Explain why an optimizer may ignore an index, how the main join algorithms work, and why join order matters.

## 📋 Prerequisites

- [Introduction to DBMS](../introduction-to-dbms/README.md), especially the data model families in [data-modeling.md](../introduction-to-dbms/data-modeling.md).
- [The Relational Model](../the-relational-model/README.md): tables, keys, and joins.
- Helpful: [indexes.md](../../../backend/sql-fundamentals/indexes.md) for the practical side of indexing, and [Hashing](../../../data-structures-and-algorithms/hashing/README.md) and [Binary Search Trees](../../../data-structures-and-algorithms/binary-search-trees/README.md) for the data structures behind it.
- Basic Python reading ability: classes, dictionaries, generators, and the `sqlite3` module at an introductory level.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [database-classification.md](database-classification.md) | The axes of classification, five data models compared on the same data, row against column storage, CAP, eventual consistency, quorums, and blurring labels |
| [indexing-theory.md](indexing-theory.md) | Why indexes save page reads, a working B+ tree, SQLite's real B-trees, clustered and secondary indexes, other index types, and LSM trees |
| [query-optimisation.md](query-optimisation.md) | Query plans, multi-column and expression indexes, statistics, when a scan beats an index, join algorithms and join order, keyset pagination, N+1 queries, and a tuning routine |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** [query-optimisation.md](query-optimisation.md) if you write queries for a real application: which conditions can use an index, and why a scan can win, explain most everyday performance surprises. For interviews, make sure you can explain the B+ tree in [indexing-theory.md](indexing-theory.md) and compare the data models in [database-classification.md](database-classification.md).

**Skim** the B+ tree and LSM code if you only need the ideas, but run the page-read model in [query-optimisation.md](query-optimisation.md) with a different cache size: it shows quickly what changes the balance between an index and a scan.

## 🧠 Knowledge Check

<details>
<summary>A table has an index on (country, city, name). Which of these can use it to search: (a) country = 'X' AND city = 'Y', (b) city = 'Y' alone, (c) country &gt; 'M' AND city = 'Y'?</summary>

**(a)** uses both columns: equality on the leading columns narrows the search twice. **(b)** cannot search from the left, because the first column has no condition; SQLite scans the table, unless `ANALYZE` has shown that `country` has few distinct values, when it may use a **skip-scan** that searches each country in turn. **(c)** uses only the range on `country`: after a range, the next column no longer narrows the part of the index that is searched. If queries by city alone matter, add an index that starts with `city`. See [query-optimisation.md](query-optimisation.md).

</details>

<details>
<summary>A report reads 20% of the rows of a large table. It runs faster after its secondary index is dropped. How can that be?</summary>

Reading rows through a secondary index jumps between table pages in index order. When many rows match, the same pages are read again and again once they have left the cache, while a **full scan** reads every page exactly once, in order. In the page model of [query-optimisation.md](query-optimisation.md), with 20% of rows matching, reading row by row through the index cost 19,101 page reads against 2,000 for a scan. Optimizers weigh this with statistics (PostgreSQL's documented example uses a sequential scan for 7,000 of 10,000 rows), but their estimates can be wrong. A **covering** index, or reading the matching pages in physical order, changes the balance.

</details>

## 📚 References

- [Wikipedia: NoSQL](https://en.wikipedia.org/wiki/NoSQL), [Key–value database](https://en.wikipedia.org/wiki/Key%E2%80%93value_database), [Document-oriented database](https://en.wikipedia.org/wiki/Document-oriented_database), [Wide-column store](https://en.wikipedia.org/wiki/Wide-column_store), [Graph database](https://en.wikipedia.org/wiki/Graph_database), [Data orientation](https://en.wikipedia.org/wiki/Data_orientation), [OLTP](https://en.wikipedia.org/wiki/Online_transaction_processing), [OLAP](https://en.wikipedia.org/wiki/Online_analytical_processing), [CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem), [Eventual consistency](https://en.wikipedia.org/wiki/Eventual_consistency), and [NewSQL](https://en.wikipedia.org/wiki/NewSQL).
- [Wikipedia: B-tree](https://en.wikipedia.org/wiki/B-tree), [B+ tree](https://en.wikipedia.org/wiki/B%2B_tree), [Database index](https://en.wikipedia.org/wiki/Database_index), [Log-structured merge-tree](https://en.wikipedia.org/wiki/Log-structured_merge-tree), [Query optimization](https://en.wikipedia.org/wiki/Query_optimization), [Nested loop join](https://en.wikipedia.org/wiki/Nested_loop_join), [Hash join](https://en.wikipedia.org/wiki/Hash_join), and [Sort-merge join](https://en.wikipedia.org/wiki/Sort-merge_join).
- SQLite documentation: [Query Planning](https://www.sqlite.org/queryplanner.html), [The Query Optimizer](https://www.sqlite.org/optoverview.html), [EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html), [Database File Format](https://www.sqlite.org/fileformat2.html), [Indexes On Expressions](https://www.sqlite.org/expridx.html), and [Appropriate Uses For SQLite](https://www.sqlite.org/whentouse.html).
- PostgreSQL documentation: [Index Types](https://www.postgresql.org/docs/current/indexes-types.html), [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html), and [Planner/Optimizer](https://www.postgresql.org/docs/current/planner-optimizer.html).
- [MongoDB: Transactions](https://www.mongodb.com/docs/manual/core/transactions/), [DynamoDB: Transactions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transactions.html), [Cassandra: Data modeling](https://cassandra.apache.org/doc/latest/cassandra/developing/data-modeling/intro.html), and [Neo4j: Graph database concepts](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/).
- [GeeksforGeeks: Types of NoSQL Databases](https://www.geeksforgeeks.org/nosql/types-of-nosql-databases/), [Indexing in Databases](https://www.geeksforgeeks.org/dbms/indexing-in-databases-set-1/), [Introduction of B+ Tree](https://www.geeksforgeeks.org/dbms/introduction-of-b-tree/), [Query Optimization](https://www.geeksforgeeks.org/dbms/query-optimization-in-relational-algebra/), and [Join Algorithms](https://www.geeksforgeeks.org/dbms/join-algorithms-in-database/): overviews and practice questions.

## ➡️ Continue Your Learning Path

This is the last module of the [Database Management Systems section](../README.md). Put it into practice with [SQL Fundamentals](../../../backend/sql-fundamentals/README.md) and [MongoDB Fundamentals](../../../backend/mongodb-fundamentals/README.md), and see how databases scale across servers in [Communication and Data Layer](../../../system-design/high-level-design/communication-and-data-layer/README.md).
