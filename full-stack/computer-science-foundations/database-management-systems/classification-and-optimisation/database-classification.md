# 🗂️ Classifying Databases

## One Label Is Not Enough

"Is it SQL or NoSQL?" is only one of the questions that describe a database. Several are largely independent of each other:

| Question | Typical answers |
|----------|-----------------|
| How is the data modeled? | relational, key-value, document, wide-column, graph |
| What work is it tuned for? | many small transactions (OLTP), or analysis over many rows (OLAP) |
| How is a table laid out in storage? | row by row, or column by column |
| Where does it run? | inside the application's process (**embedded**), or as a separate server (**client-server**) |
| How many machines hold the data? | one, copies on several (**replication**), or different parts on several (**sharding**) |
| What does it promise when copies disagree? | every read sees the latest write, or copies catch up later |

SQLite, the database used in this section, is relational, stores a table row by row, and is **embedded**: it runs inside the program that uses it and aims to provide local storage for individual applications and devices, whereas client-server databases such as PostgreSQL aim to be a shared, central store of data ([SQLite: Appropriate Uses For SQLite](https://www.sqlite.org/whentouse.html)). The data model is the axis that people usually mean, so it comes first. [data-modeling.md](../introduction-to-dbms/data-modeling.md) outlined the families of data models, including older ones. This lesson concentrates on the five that you are most likely to meet today, and then looks at the other axes.

All code was run on CPython 3.9 on a Mac (macOS, Apple silicon).

## 🧱 The Same Data in Five Models

A small bookshop has 40 customers, 30 books, and 200 orders, each with one to three books. The code below stores the same data in a toy version of each model, and each toy store **counts every stored item that a query reads**: a row, a value, a document, a node, or an edge. Index entries are not counted. The counts show what each shape makes cheap or expensive. They are not measurements of any real product.

```python
import json
import random
from collections import defaultdict

generator = random.Random(8)
CUSTOMERS = {number: f"customer-{number}" for number in range(1, 41)}
BOOKS = {number: f"book-{number}" for number in range(1, 31)}
ORDERS = [(order, generator.randrange(1, 41), generator.randrange(1, 366),              # (order, customer, day,
           sorted(generator.sample(range(1, 31), generator.randrange(1, 4))))           #  books in the order)
          for order in range(1, 201)]

def truth(question, argument):
    """The right answers, computed straight from the raw data."""
    if question == "order_view":                          # the customer's name and the titles in one order
        _, customer, _, books = ORDERS[argument - 1]
        return CUSTOMERS[customer], [BOOKS[book] for book in books]
    if question == "history":                             # one customer's orders as (day, order), newest first
        return sorted(((day, order) for order, customer, day, _ in ORDERS if customer == argument), reverse=True)
    return sorted({customer for _, customer, _, books in ORDERS if argument in books})   # "buyers" of a book

class Store:
    """A toy database that counts every stored item a query reads."""
    reads = 0
    def read(self, item):
        self.reads += 1
        return item
```

**Relational** and **key-value** come first. The relational store keeps each fact once and uses indexes to find rows. The key-value store is a dictionary: the database sees only keys and **opaque** values, so it can fetch a value by its key but cannot search inside it ([Wikipedia: Key–value database](https://en.wikipedia.org/wiki/Key%E2%80%93value_database)). In this basic form, anything else that must be found quickly needs a key that the application invented and keeps up to date:

```python
class Relational(Store):
    name = "relational, with indexes"
    def __init__(self):
        self.orders = {order: (customer, day) for order, customer, day, _ in ORDERS}
        self.lines_by_order = {order: [(order, book) for book in books] for order, _, _, books in ORDERS}
        self.lines_by_book, self.orders_by_customer = defaultdict(list), defaultdict(list)
        for order, customer, _, _ in ORDERS:
            self.orders_by_customer[customer].append(order)
            for line in self.lines_by_order[order]:
                self.lines_by_book[line[1]].append(line)
    def order_view(self, order):
        customer, _ = self.read(self.orders[order])
        titles = [self.read(BOOKS[self.read(line)[1]]) for line in self.lines_by_order[order]]
        return self.read(CUSTOMERS[customer]), titles
    def history(self, customer):
        return sorted(((self.read(self.orders[order])[1], order) for order in self.orders_by_customer[customer]),
                      reverse=True)
    def buyers(self, book):
        return sorted({self.read(self.orders[self.read(line)[0]])[0] for line in self.lines_by_book[book]})

class KeyValue(Store):
    name = "key-value"
    def __init__(self):
        self.data, orders_of = {}, defaultdict(list)
        for order, customer, day, books in ORDERS:
            self.data[f"order:{order}"] = json.dumps({"customer": customer, "name": CUSTOMERS[customer], "day": day,
                                                      "books": [[book, BOOKS[book]] for book in books]})
            orders_of[customer].append(order)
        for customer, orders in orders_of.items():                       # a key the application must maintain
            self.data[f"orders-of:{customer}"] = json.dumps(orders)
    def get(self, key):
        return json.loads(self.read(self.data[key])) if key in self.data else []
    def order_view(self, order):
        value = self.get(f"order:{order}")
        return value["name"], [title for _, title in value["books"]]
    def history(self, customer):
        orders = self.get(f"orders-of:{customer}")
        return sorted(((self.get(f"order:{order}")["day"], order) for order in orders), reverse=True)
    def buyers(self, book):                                              # no key answers this: read every order
        found = set()
        for key in [key for key in self.data if key.startswith("order:")]:
            value = self.get(key)
            if any(number == book for number, _ in value["books"]):
                found.add(value["customer"])
        return sorted(found)
```

A **document** database also keeps self-contained records, but it understands their structure, so it can query and index fields inside them ([Wikipedia: Document-oriented database](https://en.wikipedia.org/wiki/Document-oriented_database)). An index on an array field holds one entry per array element, which is how MongoDB's **multikey** indexes work ([MongoDB: Multikey Indexes](https://www.mongodb.com/docs/manual/core/indexes/index-types/index-multikey/)). A **wide-column** store has rows whose columns may differ from row to row and are grouped into column families, and it can be seen as a two-level key-value store; Google's Bigtable is a classic example ([Wikipedia: Wide-column store](https://en.wikipedia.org/wiki/Wide-column_store)). In Apache Cassandra, tables are designed around the queries: joins are not supported, so data is copied into a table for each query pattern, and rows are grouped into partitions by a partition key ([Cassandra: Data modeling](https://cassandra.apache.org/doc/latest/cassandra/developing/data-modeling/intro.html)). A **graph** database stores **nodes** and **relationships** between them, each relationship with a direction and a type, and both can carry properties ([Neo4j: Graph database concepts](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/)):

```python
class Document(Store):
    def __init__(self, index_books=False):
        self.name = "document, plus an index on books" if index_books else "document"
        self.index_books = index_books
        self.orders = {order: {"customer": {"id": customer, "name": CUSTOMERS[customer]}, "day": day,
                               "books": [{"id": book, "title": BOOKS[book]} for book in books]}
                       for order, customer, day, books in ORDERS}
        self.by_customer, self.by_book = defaultdict(list), defaultdict(list)
        for order, document in self.orders.items():
            self.by_customer[document["customer"]["id"]].append(order)
            for book in document["books"]:                               # one index entry per array element
                self.by_book[book["id"]].append(order)
    def order_view(self, order):
        document = self.read(self.orders[order])
        return document["customer"]["name"], [book["title"] for book in document["books"]]
    def history(self, customer):
        return sorted(((self.read(self.orders[order])["day"], order) for order in self.by_customer[customer]),
                      reverse=True)
    def buyers(self, book):
        candidates = self.by_book[book] if self.index_books else self.orders      # no index: every document
        found = set()
        for order in candidates:
            document = self.read(self.orders[order])
            if any(entry["id"] == book for entry in document["books"]):
                found.add(document["customer"]["id"])
        return sorted(found)

class WideColumn(Store):
    name = "wide-column, one table per query"
    def __init__(self):
        views, histories, buyers = defaultdict(dict), defaultdict(dict), defaultdict(dict)
        for order, customer, day, books in ORDERS:                       # every order is written three ways
            histories[customer][(-day, -order)] = (day, order)           # partition = customer, newest row first
            for book in books:
                views[order][book] = (CUSTOMERS[customer], BOOKS[book])  # partition = order
                buyers[book][customer] = customer                        # partition = book
        self.views, self.histories, self.buyers_of = [
            {key: [rows[column] for column in sorted(rows)] for key, rows in table.items()}   # rows kept in order
            for table in (views, histories, buyers)]
    def partition(self, table, key):
        return [self.read(row) for row in table.get(key, [])]
    def order_view(self, order):
        rows = self.partition(self.views, order)
        return rows[0][0], [title for _, title in rows]
    def history(self, customer):
        return self.partition(self.histories, customer)
    def buyers(self, book):
        return self.partition(self.buyers_of, book)

class Graph(Store):
    name = "graph"
    def __init__(self):
        self.nodes, self.out, self.into = {}, defaultdict(list), defaultdict(list)
        self.nodes.update({("customer", number): name for number, name in CUSTOMERS.items()})
        self.nodes.update({("book", number): title for number, title in BOOKS.items()})
        for order, customer, day, books in ORDERS:
            self.nodes["order", order] = day
            self.connect(("customer", customer), ("order", order))       # the PLACED relationship
            for book in books:
                self.connect(("order", order), ("book", book))           # the CONTAINS relationship
    def connect(self, start, end):
        self.out[start].append((start, end))                             # each node refers to its own edges
        self.into[end].append((start, end))
    def node(self, key):
        return self.read(self.nodes[key])
    def follow(self, edges, side):                                       # the nodes at one side of these edges
        return [self.read(edge)[side] for edge in edges]
    def order_view(self, order):
        self.node(("order", order))
        [customer] = self.follow(self.into["order", order], 0)
        books = self.follow(self.out["order", order], 1)
        return self.node(customer), [self.node(book) for book in books]
    def history(self, customer):
        self.node(("customer", customer))
        orders = self.follow(self.out["customer", customer], 1)
        return sorted(((self.node(order), order[1]) for order in orders), reverse=True)
    def buyers(self, book):
        self.node(("book", book))
        orders = self.follow(self.into["book", book], 0)
        return sorted({customer[1] for order in orders for customer in self.follow(self.into[order], 0)})
```

Now every store answers the same three questions, every answer is checked against the raw data, and the reads are counted:

```python
STORES = [Relational(), KeyValue(), Document(), Document(index_books=True), WideColumn(), Graph()]
QUESTIONS = [("order 17", "order_view", 17), ("customer 3's orders", "history", 3), ("buyers of book 5", "buyers", 5)]

print(f"{'items read':<34}" + "".join(f"{label:>21}" for label, _, _ in QUESTIONS))
for store in STORES:
    counts = []
    for _, method, argument in QUESTIONS:
        store.reads = 0
        assert getattr(store, method)(argument) == truth(method, argument)
        counts.append(store.reads)
    print(f"{store.name:<34}" + "".join(f"{count:>21}" for count in counts))
print(f"answers: {len(truth('order_view', 17)[1])} books in order 17, {len(truth('history', 3))} orders by customer 3, "
      f"{len(truth('buyers', 5))} buyers of book 5 (in {sum(5 in books for *_, books in ORDERS)} orders)")
```

```text
items read                                     order 17  customer 3's orders     buyers of book 5
relational, with indexes                              8                    5                   30
key-value                                             1                    6                  200
document                                              1                    5                  200
document, plus an index on books                      1                    5                   15
wide-column, one table per query                      3                    5                   13
graph                                                 9                   11                   31
answers: 3 books in order 17, 5 orders by customer 3, 13 buyers of book 5 (in 15 orders)
```

How to read these numbers:

- **One order:** the key-value and document stores read a single record that holds everything about the order, and the wide-column store reads one small partition. The relational store reads 8 rows (the order, its 3 lines, 3 books, and the customer), because it stores each fact once. The graph store reads 9 nodes and edges.
- **One customer's orders:** the first five stores read 5 or 6 items, since each has a path from a customer to that customer's orders. The key-value store has one only because the application maintains an `orders-of` key. The graph store reads 11 items, counting the edges.
- **Who bought book 5?** Here the shapes differ most. The key-value store and the document store without an index on books read all 200 orders. The index on the array reduces that to the 15 orders that contain the book. The wide-column table built for this question reads 13 rows, one per buyer. The relational store reads 15 order lines and their 15 orders, and the graph store follows 15 edges to orders and 15 more to customers.

The wide-column store is cheap for all three only because the questions were known in advance. It writes `2 × (books in the order) + 1` rows for every order, and a new question would need a new table. The relational store can answer a new question with a new query, at the cost of joins and, often, a new index.

| Model | Shape of the data | A natural fit when | The price |
|-------|-------------------|--------------------|-----------|
| **Relational** | tables joined by keys | questions are varied and not all known in advance, and rules must hold across records | joins, and care with indexes at scale |
| **Key-value** | a dictionary of keys to opaque values | everything is looked up by a known key | other questions need extra keys, maintained by the application |
| **Document** | self-contained, nested records | a record is usually read and written whole, and its fields vary | repeated data inside documents, and joins across documents are less natural |
| **Wide-column** | rows grouped by partition key, sorted inside | huge data sets whose queries are known in advance | one copy of the data per query pattern, written together |
| **Graph** | nodes and typed relationships | questions follow chains of connections | a different query language and model to learn |

## 📊 Rows or Columns: OLTP and OLAP

**OLTP** (online transaction processing) systems run many short operations that each touch little data, such as placing an order. **OLAP** (online analytical processing) answers broad questions over large amounts of data, such as sales by region and month ([Wikipedia: OLTP](https://en.wikipedia.org/wiki/Online_transaction_processing), [OLAP](https://en.wikipedia.org/wiki/Online_analytical_processing)). The storage layout often follows the job: **row-oriented** formats, which keep each row's values together, are more common for OLTP, and **column-oriented** formats, which keep each column's values together, are more common for OLAP ([Wikipedia: Data orientation](https://en.wikipedia.org/wiki/Data_orientation)).

The experiment stores 100,000 sales both ways, as fixed-width binary values in 4,096-byte pages (no value crosses a page boundary), and counts the pages each query must read. It also compresses both layouts with `zlib`:

```python
import struct
import zlib

PAGE_BYTES = 4096
CODES = {"id": "i", "day": "h", "store": "h", "product": "i", "quantity": "h", "cents": "i"}   # i = 4 bytes, h = 2
SALES = 100_000
generator = random.Random(4)
sales = {"id": range(1, SALES + 1), "day": sorted(generator.randrange(365) for _ in range(SALES)),
         "store": [generator.randrange(50) for _ in range(SALES)],
         "product": [generator.randrange(5000) for _ in range(SALES)],
         "quantity": [generator.choice([1, 1, 1, 2, 3]) for _ in range(SALES)],
         "cents": [generator.randrange(100, 100_000) for _ in range(SALES)]}

def pages(item_bytes, items):
    per_page = PAGE_BYTES // item_bytes
    return -(-items // per_page)                                          # divide, rounding up

row_bytes = struct.calcsize("<" + "".join(CODES.values()))                # "<" means no padding
print(f"one row is {row_bytes} bytes: the row layout needs {pages(row_bytes, SALES)} pages")
print(f"{'pages read':<34}{'rows together':>14}{'columns together':>18}")
print(f"{'sum(cents) over every sale':<34}{pages(row_bytes, SALES):>14}{pages(4, SALES):>18}")
print(f"{'all six values of one sale':<34}{1:>14}{len(CODES):>18}")

by_rows = b"".join(struct.pack("<" + "".join(CODES.values()), *row) for row in zip(*(sales[c] for c in CODES)))
by_columns = {c: struct.pack(f"<{SALES}{code}", *sales[c]) for c, code in CODES.items()}
print(f"\ncompressed: {len(zlib.compress(by_rows)):,} bytes row by row, "
      f"{sum(len(zlib.compress(blob)) for blob in by_columns.values()):,} bytes column by column")
for column, blob in by_columns.items():
    print(f"  {column:<9}{len(blob):>8,} -> {len(zlib.compress(blob)):>7,}")
```

```text
one row is 18 bytes: the row layout needs 441 pages
pages read                         rows together  columns together
sum(cents) over every sale                   441                98
all six values of one sale                     1                 6

compressed: 932,563 bytes row by row, 746,335 bytes column by column
  id        400,000 -> 138,363
  day       200,000 ->   1,132
  store     200,000 ->  92,226
  product   400,000 -> 210,860
  quantity  200,000 ->  26,767
  cents     400,000 -> 276,987
```

The sum reads the whole table in the row layout, 441 pages, but only the 98 pages of the `cents` column in the column layout. Fetching one complete sale goes the other way: one page for rows, six for columns. Columns also compressed better here, about 20% smaller in total, because the values within one column are alike: the sorted `day` column shrank to under 1% of its size, and `quantity`, with three distinct values, to about 13%. How much compression helps depends on the data.

> ⚠️ **Wide-column is not column-oriented.** "Column store" originally meant a column-oriented relational database. Wide-column stores such as Bigtable and Cassandra group related columns into column families that are stored together, and are a different idea ([Wikipedia: Wide-column store](https://en.wikipedia.org/wiki/Wide-column_store)).

## 🌐 One Machine or Many

**Replication** keeps copies of the same data on several servers, and **sharding** splits different data across servers. [Database Replication and Sharding](../../../system-design/high-level-design/communication-and-data-layer/database-replication-and-sharding.md) covers both. Copies raise a new question: what does a reader see while they differ?

The **CAP theorem** says that while a network **partition** stops some servers from talking to each other, a replicated data store has to choose between **consistency** (every read returns the most recent write, or an error) and **availability** (every request to a working server gets a response). Without a partition it can offer both. Note that CAP's consistency is not the C in ACID ([Wikipedia: CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem)); [Consistency vs. Performance Tradeoffs](../../../system-design/high-level-design/communication-and-data-layer/consistency-vs-performance-tradeoffs.md) applies it to a design. Systems that favour availability often promise only **eventual consistency**: if no new updates arrive, all copies eventually return the last written value. They are often described as **BASE** (basically available, soft state, eventually consistent), in contrast to ACID ([Wikipedia: Eventual consistency](https://en.wikipedia.org/wiki/Eventual_consistency)).

Some databases let each request choose. With `N` copies, a write can wait until `W` of them confirm it, and a read can ask `R` of them. Cassandra's consistency levels are a version of this rule ([Cassandra: Dynamo](https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html)). The program checks every possible choice of servers:

```python
from itertools import combinations

def every_read_meets_every_write(replicas, write_acks, read_asks):
    return all(set(written) & set(asked)
               for written in combinations(range(replicas), write_acks)
               for asked in combinations(range(replicas), read_asks))

for replicas in (3, 5, 7):
    assert all(every_read_meets_every_write(replicas, w, r) == (w + r > replicas)
               for w in range(1, replicas + 1) for r in range(1, replicas + 1))
print("for N = 3, 5 and 7, the overlap is guaranteed exactly when R + W > N")
print("N = 3     R=1        R=2        R=3")
for w in (1, 2, 3):
    print(f"  W={w}  " + "".join(f"{'overlap' if every_read_meets_every_write(3, w, r) else 'may miss':<11}"
                              for r in (1, 2, 3)).rstrip())
```

```text
for N = 3, 5 and 7, the overlap is guaranteed exactly when R + W > N
N = 3     R=1        R=2        R=3
  W=1  may miss   may miss   overlap
  W=2  may miss   overlap    overlap
  W=3  overlap    overlap    overlap
```

An overlap means that a read reaches at least one copy that holds the latest **acknowledged** write. That alone does not make the data consistent: the reader still has to tell which of the answers is newest, and writes that happen at the same time, or fail part-way, need rules of their own, such as timestamps or vector clocks ([Wikipedia: Eventual consistency](https://en.wikipedia.org/wiki/Eventual_consistency)).

## 🧬 The Lines Are Blurring

A label no longer tells you what a product can do. Check the documentation of the product and version you use:

- In **MongoDB**, an operation on a single document is atomic, and **multi-document transactions** are available, including across replica sets and sharded clusters; the documentation still advises modeling data so that they are rarely needed ([MongoDB: Transactions](https://www.mongodb.com/docs/manual/core/transactions/)).
- **Amazon DynamoDB**, a NoSQL database, offers **ACID transactions** over multiple items, within and across tables ([DynamoDB: Transactions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transactions.html)).
- **PostgreSQL**, a relational database, stores JSON documents in `jsonb` columns and can index the keys and values inside them with GIN indexes ([PostgreSQL: JSON Types](https://www.postgresql.org/docs/current/datatype-json.html)).
- **NewSQL** names relational systems that aim for the scale of NoSQL systems for transaction processing while keeping ACID guarantees ([Wikipedia: NewSQL](https://en.wikipedia.org/wiki/NewSQL)).

Even the word NoSQL, usually read as "not only SQL" or "non-relational", covers very different designs ([Wikipedia: NoSQL](https://en.wikipedia.org/wiki/NoSQL)).

## 🧭 Choosing

Start from the questions the application must answer, not from a product:

1. What are the important reads and writes, and are they all known in advance?
2. Which rules must hold across several records, and therefore need transactions?
3. Is the main work many small transactions or broad analysis?
4. How much data and traffic will there be, and does it need more than one machine?
5. What does the team already know how to run, back up, and monitor?

[SQL vs. NoSQL](../../../backend/database-design-and-modeling/sql-vs-nosql.md) walks through the choice between a relational and a document database, and [SQL vs. NoSQL at Scale](../../../system-design/high-level-design/communication-and-data-layer/sql-vs-nosql-at-scale.md) revisits it for large systems. Using more than one database in one system, each for the data it suits, is common.

## ✅ Checking the Code

On 300 random bookshops, all six stores gave the same answers as a direct computation from the raw data, for every order, customer, and book (315,930 answers), and every count of items read matched a formula for what that shape has to read. The page counts matched packing the values into pages one at a time, both layouts decoded to the same values, and the `R + W > N` rule held in an exhaustive check of every setting with up to 9 copies.

## Common Misconceptions

- **"NoSQL databases have no schema."** The database may not enforce one, but the program still relies on the data having a certain shape.
- **"NoSQL means no transactions."** MongoDB and DynamoDB both offer transactions; the guarantees differ between products, so read them.
- **"Wide-column and column-oriented are the same thing."** They are different designs with similar names.
- **"R + W > N makes a database strongly consistent."** It guarantees that read and write sets overlap, which is only one ingredient.
- **"One database has to do everything."** Many systems use several, each for a part of the data.

## ➡️ Next

Whatever the model, a database stays fast only because it can find data without reading all of it. Continue to [indexing-theory.md](indexing-theory.md) to see how indexes work inside.
