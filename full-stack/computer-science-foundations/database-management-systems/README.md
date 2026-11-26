# 🗄️ Database Management Systems

## 📚 Overview

Databases sit under almost every application. This section explains the ideas that make them trustworthy and usable: why they exist, how data is modeled, what the relational model is, how to design tables without redundancy, how transactions keep data correct when things run at once or fail, and how databases are classified and made fast. It concentrates on concepts, checked with small experiments in SQLite, and links to the practical database lessons elsewhere in this repository instead of repeating them.

## 🧭 The Learning Path

| # | Module | The question it answers | Builds on |
|---|--------|-------------------------|-----------|
| 1 | [Introduction to DBMS](introduction-to-dbms/README.md) | Why do databases exist, and how does an entity-relationship model become tables? | Basic Python |
| 2 | [The Relational Model](the-relational-model/README.md) | What are relations, keys, and joins, and where does SQL depart from the model? | Introduction to DBMS |
| 3 | Normalisation (in preparation) | How are tables split so that facts are stored once? | The Relational Model |
| 4 | Transactions and ACID (in preparation) | What does a transaction guarantee, and what can go wrong when transactions overlap? | The Relational Model |
| 5 | Database Classification and Optimisation (in preparation) | Which kinds of database exist, and how are queries made fast? | The earlier modules |

## 🔗 Practical Material Elsewhere in the Repository

- [SQL Fundamentals](../../backend/sql-fundamentals/README.md): writing queries against a relational database.
- [Database Design and Modeling](../../backend/database-design-and-modeling/README.md): design principles, relationships, normalization, schema design, and SQL versus NoSQL.
- [MongoDB Fundamentals](../../backend/mongodb-fundamentals/README.md): a document database in practice.

## ➡️ Start Here

Begin with [Introduction to DBMS](introduction-to-dbms/README.md).
