# 🚀 Query Optimization

## From SQL to a Plan

SQL says **what** you want, not **how** to get it. The database parses a query, and its **query optimizer** chooses an execution **plan**: which indexes to use, in which order to join the tables, and how to join them. A **cost-based** optimizer estimates the cost of candidate plans from **statistics** about the data and picks the cheapest it found ([Wikipedia: Query optimization](https://en.wikipedia.org/wiki/Query_optimization)). [relational-algebra.md](../the-relational-model/relational-algebra.md) showed why this is possible: different expressions can give the same result with very different amounts of work. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon) with SQLite 3.54. Plan wording and work counts can differ in other versions.

## 🔎 Reading a Plan

In SQLite, `EXPLAIN QUERY PLAN` shows the plan ([SQLite: EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html)):

| Plan text | Meaning |
|-----------|---------|
| `SCAN t` | every row of `t` is visited (possibly in the order of an index) |
| `SEARCH t USING INDEX i (a=?)` | only some rows are visited, found through index `i` |
| `USING COVERING INDEX` | the index has every column needed, so the table is not read |
| `USE TEMP B-TREE FOR ORDER BY` | an extra sorting step builds a temporary B-tree (also used for `GROUP BY` and `DISTINCT`) |

> ⚠️ **When you experiment from Python:** `sqlite3` caches prepared statements, and on this setup (CPython 3.9, SQLite 3.54) a cached `EXPLAIN QUERY PLAN` kept showing the old plan after an index was **dropped**. Change the SQL text, for example by adding a comment, or open a new connection to see the current plan.

For a join, there is one line per nested loop, outer loop first. In PostgreSQL, `EXPLAIN` shows the plan with the planner's estimates, and `EXPLAIN ANALYZE` also **runs the query** to show real row counts and times, so any changes the statement makes really happen ([PostgreSQL: Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)).

## 🧪 Which Queries Can Use an Index?

The table below has 60,000 members, an index on `(country, city, name)`, and an index on `email`. Besides the plan, the code reports a rough measure of work: how often SQLite calls a **progress handler**, which it runs periodically while executing a statement ([SQLite: progress handler](https://www.sqlite.org/c3ref/progress_handler.html)). With the interval set to 1, the number of calls grows with the work done. It is only approximate, and it does **not** count pages read from storage.

```python
import random
import sqlite3

db = sqlite3.connect(":memory:", isolation_level=None)
db.execute("""CREATE TABLE members (id INTEGER PRIMARY KEY, country TEXT NOT NULL, city TEXT NOT NULL,
              name TEXT NOT NULL, email TEXT NOT NULL, joined INTEGER NOT NULL)""")
generator = random.Random(11)
COUNTRIES = ["Brazil", "India", "Japan", "Kenya", "Norway", "Peru"]
people = []
for number in range(60_000):
    country = generator.choice(COUNTRIES)
    people.append((country, f"{country[:2]}-town{generator.randrange(50):02d}", f"name{generator.randrange(100_000):05d}",
                   f"user{number:05d}@example.com", generator.randrange(3650)))
db.executemany("INSERT INTO members (country, city, name, email, joined) VALUES (?, ?, ?, ?, ?)", people)
db.execute("CREATE INDEX members_place ON members (country, city, name)")
db.execute("CREATE INDEX members_email ON members (email)")

def plan(db, sql, parameters=()):
    return "; ".join(row[-1] for row in db.execute("EXPLAIN QUERY PLAN " + sql, parameters))

def work(db, sql, parameters=()):
    """(rows returned, progress-handler calls: a rough measure of the work done)."""
    db.execute(sql, parameters).fetchall()                 # run once first, so it is already compiled
    calls = 0
    def tick():
        nonlocal calls
        calls += 1
    db.set_progress_handler(tick, 1)
    rows = db.execute(sql, parameters).fetchall()
    db.set_progress_handler(None, 0)
    return len(rows), calls

def explain(where, columns="*"):
    sql = f"SELECT {columns} FROM members WHERE {where}"
    rows, calls = work(db, sql)
    print(f"{'' if columns == '*' else 'SELECT ' + columns + ' '}WHERE {where}\n"
          f"    {plan(db, sql)}   [{rows:,} row{'' if rows == 1 else 's'}, work {calls:,}]")

explain("country = 'India'")
explain("country = 'India' AND city = 'In-town07'")
explain("city = 'In-town07'")
explain("country > 'M' AND city = 'No-town07'")
explain("country = 'India' ORDER BY city, name")
explain("country = 'India' ORDER BY joined")
explain("country = 'India' AND name = 'name58535'", columns="city")
```

```text
WHERE country = 'India'
    SEARCH members USING INDEX members_place (country=?)   [9,957 rows, work 99,579]
WHERE country = 'India' AND city = 'In-town07'
    SEARCH members USING INDEX members_place (country=? AND city=?)   [199 rows, work 2,000]
WHERE city = 'In-town07'
    SCAN members   [199 rows, work 181,401]
WHERE country > 'M' AND city = 'No-town07'
    SEARCH members USING INDEX members_place (country>?)   [198 rows, work 82,112]
WHERE country = 'India' ORDER BY city, name
    SEARCH members USING INDEX members_place (country=?)   [9,957 rows, work 99,580]
WHERE country = 'India' ORDER BY joined
    SEARCH members USING INDEX members_place (country=?); USE TEMP B-TREE FOR ORDER BY   [9,957 rows, work 199,153]
SELECT city WHERE country = 'India' AND name = 'name58535'
    SEARCH members USING COVERING INDEX members_place (country=?)   [1 row, work 39,839]
```

The rules behind these plans ([SQLite: The Query Optimizer](https://www.sqlite.org/optoverview.html)):

- An index on several columns is used from the **left**. The leading columns need conditions with `=`, `IN`, or `IS`; the last column used may have a range such as `>` or `<`; and there can be **no gaps**. So `city` alone cannot use `(country, city, name)` here, and after the range on `country`, the condition on `city` no longer narrows the search.
- If the rows come out of the index already in the order that `ORDER BY` asks for, no sorting step is needed. Sorting by `joined` needed one, and about twice the work.
- The last query could be answered from the index alone (a **covering** index), but without a condition on `city`, the `name` condition could not narrow the search, so every Indian entry was still checked.

PostgreSQL's rule is similar: conditions on the leading columns limit how much of the index is read ([PostgreSQL: Multicolumn Indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html)).

A condition can also hide a column from its index:

```python
explain("email = 'user00042@example.com'")
explain("lower(email) = 'user00042@example.com'")
explain("email LIKE 'user0004%'")
explain("email GLOB 'user0004*'")
db.execute("CREATE INDEX members_lower_email ON members (lower(email))")
print("after CREATE INDEX members_lower_email ON members (lower(email)):")
explain("lower(email) = 'user00042@example.com'")
```

```text
WHERE email = 'user00042@example.com'
    SEARCH members USING INDEX members_email (email=?)   [1 row, work 19]
WHERE lower(email) = 'user00042@example.com'
    SCAN members   [1 row, work 240,015]
WHERE email LIKE 'user0004%'
    SCAN members   [10 rows, work 240,078]
WHERE email GLOB 'user0004*'
    SEARCH members USING INDEX members_email (email>? AND email<?)   [10 rows, work 116]
after CREATE INDEX members_lower_email ON members (lower(email)):
WHERE lower(email) = 'user00042@example.com'
    SEARCH members USING INDEX members_lower_email (<expr>=?)   [1 row, work 19]
```

- **A function on the column** (`lower(email)`) hides it from the index on `email`. An **index on the expression** fixes that; SQLite uses it when the query contains the expression exactly as written in the index ([SQLite: Indexes On Expressions](https://www.sqlite.org/expridx.html)).
- **`LIKE` and `GLOB`** can use an index for a fixed prefix only if the index sorts text the way the operator compares it. By default, SQLite's `LIKE` ignores the case of ASCII letters but this index does not, so `LIKE` scanned the table; the case-sensitive `GLOB` searched the index. An index with the `NOCASE` collation would let this `LIKE` use it ([the LIKE optimization](https://www.sqlite.org/optoverview.html#the_like_optimization)).

## 📈 Statistics Change Plans

A plan is only as good as the optimizer's estimates. SQLite's `ANALYZE` command collects statistics into the `sqlite_stat1` table, and they are **not** updated automatically as the data changes, so rerun it after large changes ([SQLite: ANALYZE](https://www.sqlite.org/lang_analyze.html)):

```python
explain("city = 'In-town07'")
db.execute("ANALYZE")
print("after ANALYZE:")
explain("city = 'In-town07'")
print("statistics:", db.execute("SELECT idx, stat FROM sqlite_stat1 WHERE idx = 'members_place'").fetchone())
```

```text
WHERE city = 'In-town07'
    SCAN members   [199 rows, work 181,401]
after ANALYZE:
WHERE city = 'In-town07'
    SEARCH members USING INDEX members_place (ANY(country) AND city=?)   [199 rows, work 2,042]
statistics: ('members_place', '60000 10000 200 1')
```

The statistics say that the index has about 60,000 entries, about 10,000 for each country, 200 for each (country, city) pair, and 1 for each full key ([SQLite: file format](https://www.sqlite.org/fileformat2.html#the_sqlite_stat1_table)). With few distinct countries, SQLite can now use a **skip-scan**: it jumps from one country to the next and searches each for the city, the `ANY(country)` in the plan. SQLite only does this after `ANALYZE` has shown that the first column has many repeated values ([the skip-scan optimization](https://www.sqlite.org/optoverview.html#the_skip_scan_optimization)). PostgreSQL also plans from collected statistics ([PostgreSQL: Statistics Used by the Planner](https://www.postgresql.org/docs/current/planner-stats.html)).

## ⚖️ When an Index Is Not Worth It

The work counter above cannot see page reads, and page reads are where an index can lose. This model stores 100,000 rows, 50 to a page, in an order unrelated to a `score` column, with a secondary index on `score` whose leaves hold 200 entries. A query asks for the rows whose score is below a limit. The model counts the pages read in four ways, with a cache that keeps the 100 most recently used table pages (it ignores the few inner index pages):

```python
from bisect import bisect_left
from collections import OrderedDict

ROWS, PER_PAGE, PER_LEAF, CACHE_PAGES = 100_000, 50, 200, 100
generator = random.Random(9)
scores = [generator.randrange(1_000_000) for _ in range(ROWS)]            # in the table's storage order
by_score = sorted((score, row) for row, score in enumerate(scores))       # the secondary index

def pages_read(requests):
    """Requests that miss a cache of the CACHE_PAGES most recently used pages."""
    cache, misses = OrderedDict(), 0
    for page in requests:
        if page in cache:
            cache.move_to_end(page)
        else:
            misses += 1
            cache[page] = True
            if len(cache) > CACHE_PAGES:
                cache.popitem(last=False)
    return misses

def costs(limit):
    matching = by_score[:bisect_left(by_score, (limit,))]
    leaves = -(-len(matching) // PER_LEAF)                                    # divide, rounding up
    return {"full scan": ROWS // PER_PAGE,
            "index, row by row": leaves + pages_read(row // PER_PAGE for _, row in matching),
            "index, pages in order": leaves + len({row // PER_PAGE for _, row in matching}),
            "if clustered on score": leaves + -(-len(matching) // PER_PAGE)}, len(matching)

print(f"{'rows matching':>14}" + "".join(f"{name:>23}" for name in costs(1)[0]))
for limit in (1_000, 10_000, 50_000, 200_000, 500_000):
    result, count = costs(limit)
    print(f"{count:>8,} {count / ROWS:>5.1%}" + "".join(f"{pages:>23,}" for pages in result.values()))
```

```text
 rows matching              full scan      index, row by row  index, pages in order  if clustered on score
      98  0.1%                  2,000                     99                     99                      3
   1,023  1.0%                  2,000                    976                    800                     27
   4,916  4.9%                  2,000                  4,707                  1,885                    124
  19,965 20.0%                  2,000                 19,101                  2,100                    500
  49,959 50.0%                  2,000                 47,771                  2,250                  1,250
```

With 0.1% of the rows matching, the index needs 99 page reads instead of 2,000, and at 1% it is still ahead. At about 5%, reading row by row costs 4,707 pages, more than twice a full scan: the matches are spread over the whole table, and the small cache drops pages before they are needed again. Collecting the row numbers first and reading each page **once**, in order, avoids that, although from 20% on it reads every table page anyway, plus the index leaves. If the table were stored in `score` order (**clustered**), the index would stay cheaper even with half the rows matching.

PostgreSQL's planner makes this trade-off from its estimates. In the documentation's example on a table of 10,000 rows, it uses a sequential scan when 7,000 rows are expected, but an index when only 100 are; that plan first collects the row locations and then reads the table pages in physical order (a **bitmap heap scan**) ([PostgreSQL: Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)). Its cost settings also treat a random page read as 4 times as expensive as a sequential one by default; the documentation notes that uncached random reads usually cost much more than that, and that the default assumes most are cached ([PostgreSQL: Planner Cost Constants](https://www.postgresql.org/docs/current/runtime-config-query.html#RUNTIME-CONFIG-QUERY-CONSTANTS)). Planners work from estimates, though, so they can choose badly: measure the queries that matter.

## 🔗 Join Algorithms

Three basic algorithms join two tables on equal keys:

- **Nested loop:** compare every row of one table with every row of the other. With an index on the inner table's key, search the index for each outer row instead (an **index nested loop**) ([Wikipedia: Nested loop join](https://en.wikipedia.org/wiki/Nested_loop_join)).
- **Hash join:** build a hash table on one input, then look up each row of the other. It works only for equality conditions ([Wikipedia: Hash join](https://en.wikipedia.org/wiki/Hash_join)).
- **Sort-merge join:** sort both inputs by the key and walk through them together. An input that is already sorted, for example by an index, saves its sort ([Wikipedia: Sort-merge join](https://en.wikipedia.org/wiki/Sort-merge_join)).

PostgreSQL chooses among all three ([PostgreSQL: Planner/Optimizer](https://www.postgresql.org/docs/current/planner-optimizer.html)). SQLite implements joins only as nested loops, but it may build a temporary **automatic index** for one statement, which its documentation calls almost the same thing as a hash join ([SQLite: The Query Optimizer](https://www.sqlite.org/optoverview.html#automatic_query_time_indexes)). The code below joins 5,000 orders, about 5% of them guest orders with no customer (`NULL`), to 500 customers, and checks every result against SQLite:

```python
from collections import defaultdict
from functools import cmp_to_key

generator = random.Random(21)
customers = [(number, f"customer-{number}") for number in range(1, 501)]                 # (id, name)
orders = [(number, None if generator.random() < 0.05 else generator.randrange(1, 501))     # (id, customer_id)
          for number in range(1, 5_001)]

def nested_loop(counts):
    out = []
    for order, key in orders:
        for customer, name in customers:
            counts["pairs compared"] += 1
            if key is not None and key == customer:
                out.append((order, customer, name))
    return out

def index_nested_loop(counts):
    keys = [customer for customer, _ in customers]            # already sorted: stands in for an index
    out = []
    for order, key in orders:
        if key is None:                                       # NULL never equals anything
            continue
        counts["index searches"] += 1
        i = bisect_left(keys, key)
        if i < len(keys) and keys[i] == key:
            out.append((order, key, customers[i][1]))
    return out

def hash_join(counts):
    table = defaultdict(list)
    for customer, name in customers:                          # build on the smaller input
        table[customer].append(name)
        counts["rows hashed"] += 1
    out = []
    for order, key in orders:                                 # probe with the larger one
        if key is not None:
            counts["probes"] += 1
            out += [(order, key, name) for name in table.get(key, [])]
    return out

def sort_merge(counts):
    def compare(a, b):
        counts["sort comparisons"] += 1
        return (a[0] > b[0]) - (a[0] < b[0])
    left = sorted(((key, order) for order, key in orders if key is not None), key=cmp_to_key(compare))
    right = sorted(customers, key=cmp_to_key(compare))
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        counts["merge steps"] += 1
        if left[i][0] < right[j][0]:
            i += 1
        elif left[i][0] > right[j][0]:
            j += 1
        else:                                                 # emit this order, keep the customer for the next
            out.append((left[i][1], right[j][0], right[j][1]))
            i += 1                                            # (customer ids are unique)
    return out

sql = sqlite3.connect(":memory:")
sql.execute("CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT)")
sql.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER)")
sql.executemany("INSERT INTO customers VALUES (?, ?)", customers)
sql.executemany("INSERT INTO orders VALUES (?, ?)", orders)
expected = sorted(sql.execute("SELECT o.id, c.id, c.name FROM orders o JOIN customers c ON c.id = o.customer_id"))
sql.close()

for join in (nested_loop, index_nested_loop, hash_join, sort_merge):
    counts = defaultdict(int)
    result = sorted(join(counts))
    assert result == expected
    print(f"{join.__name__:<18}{len(result):>6,} rows   " + ", ".join(f"{value:,} {what}" for what, value in counts.items()))
```

```text
nested_loop        4,737 rows   2,500,000 pairs compared
index_nested_loop  4,737 rows   4,737 index searches
hash_join          4,737 rows   500 rows hashed, 4,737 probes
sort_merge         4,737 rows   52,216 sort comparisons, 5,236 merge steps
```

All four return the same 4,737 rows; the other orders have no customer. The nested loop compared all 2,500,000 pairs. The index nested loop searched the index once for each order that has a customer, each search taking about log₂ 500, so about 9, steps. The hash join read each input once. The sort-merge join spent most of its effort sorting, mainly the orders, and then merged in 5,236 steps; if both inputs arrived already sorted, for example from indexes, only the merge would remain.

The index nested loop and the merge above rely on customer ids being unique, as a primary key is. When both sides can repeat a key, every row of one group must be paired with every row of the other.

## 🧮 Join Order Matters

With three tables, which two are joined first can change the work enormously. Here the query wants the order lines of customers in one city:

```python
generator = random.Random(31)
shop_customers = {number: f"city{generator.randrange(100):02d}" for number in range(1, 2_001)}   # id -> city
shop_orders = {number: generator.randrange(1, 2_001) for number in range(1, 20_001)}            # id -> customer
shop_lines = [(order, item) for order in shop_orders for item in range(generator.randrange(1, 6))]   # (order, item)

local = {customer for customer, city in shop_customers.items() if city == "city07"}              # filtered first
local_orders = {order for order, customer in shop_orders.items() if customer in local}
result = sum(order in local_orders for order, _ in shop_lines)
plans = {"customers with orders, then lines": len(local_orders) + result,
         "orders with lines, then customers": len(shop_lines) + result,
         "customers with lines, then orders": len(local) * len(shop_lines) + result}   # nothing links them
for name, rows in plans.items():
    print(f"{name:<36}{rows:>12,} rows produced along the way")
print(f"final result: {result:,} lines from {len(local)} customers in city07")

shop = sqlite3.connect(":memory:")
shop.executescript("""
    CREATE TABLE customers (id INTEGER PRIMARY KEY, city TEXT);
    CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER);
    CREATE TABLE lines (order_id INTEGER, item INTEGER);
    CREATE INDEX customers_city ON customers (city);
    CREATE INDEX orders_customer ON orders (customer_id);
    CREATE INDEX lines_order ON lines (order_id);
""")
shop.executemany("INSERT INTO customers VALUES (?, ?)", shop_customers.items())
shop.executemany("INSERT INTO orders VALUES (?, ?)", shop_orders.items())
shop.executemany("INSERT INTO lines VALUES (?, ?)", shop_lines)
query = """SELECT count(*) FROM lines l JOIN orders o ON o.id = l.order_id
           JOIN customers c ON c.id = o.customer_id WHERE c.city = 'city07'"""
assert shop.execute(query).fetchone()[0] == result
print("SQLite's plan, outer loop first:")
for row in shop.execute("EXPLAIN QUERY PLAN " + query):
    print("   ", row[-1])
shop.close()
```

```text
customers with orders, then lines            941 rows produced along the way
orders with lines, then customers         60,468 rows produced along the way
customers with lines, then orders      1,315,491 rows produced along the way
final result: 705 lines from 22 customers in city07
SQLite's plan, outer loop first:
    SEARCH c USING COVERING INDEX customers_city (city=?)
    SEARCH o USING COVERING INDEX orders_customer (customer_id=?)
    SEARCH l USING COVERING INDEX lines_order (order_id=?)
```

All three orders give the same 705 lines, but they produce very different amounts of data along the way. Filtering the customers first and following the join conditions produces 941 rows; joining every order with its lines first produces about 64 times as many; and pairing customers with lines, which no condition links, builds over 1.3 million combinations (a **cross product**). SQLite chose the first order, starting from the index on `city`.

The number of possible orders grows quickly with the number of tables. PostgreSQL normally searches them almost exhaustively, with an approach first used in IBM's System R, and switches to a **genetic** search when a query joins many tables ([PostgreSQL: GEQO](https://www.postgresql.org/docs/current/geqo-intro.html)). SQLite uses an efficient, polynomial-time graph algorithm ([SQLite: The Query Optimizer](https://www.sqlite.org/optoverview.html#joins)).

## 🐢 Two Habits That Waste Work

### Pagination With OFFSET

`LIMIT 10 OFFSET 90000` still steps over 90,000 rows before returning anything. **Keyset pagination** remembers where the last page ended and searches from there:

```python
feed = sqlite3.connect(":memory:", isolation_level=None)
feed.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY, created INTEGER NOT NULL, title TEXT NOT NULL)")
generator = random.Random(41)
feed.executemany("INSERT INTO posts (created, title) VALUES (?, ?)",
                 ((generator.randrange(50_000), f"post {n}") for n in range(100_000)))
feed.execute("CREATE INDEX posts_created ON posts (created, id)")
ORDERED = feed.execute("SELECT created, id FROM posts ORDER BY created, id").fetchall()

by_offset = "SELECT created, id FROM posts ORDER BY created, id LIMIT 10 OFFSET ?"
by_keyset = "SELECT created, id FROM posts WHERE (created, id) > (?, ?) ORDER BY created, id LIMIT 10"
print(f"{'rows before the page':>20}{'work with OFFSET':>18}{'work with keyset':>18}")
for skip in (10, 1_000, 10_000, 90_000):
    last = ORDERED[skip - 1]                                  # the last row of the previous page
    assert feed.execute(by_offset, (skip,)).fetchall() == feed.execute(by_keyset, last).fetchall()
    print(f"{skip:>20,}{work(feed, by_offset, (skip,))[1]:>18,}{work(feed, by_keyset, last)[1]:>18,}")
print("keyset plan:", plan(feed, by_keyset, (0, 0)))
```

```text
rows before the page  work with OFFSET  work with keyset
                  10                91               133
               1,000             2,071               115
              10,000            20,071               112
              90,000           180,071               148
keyset plan: SEARCH posts USING COVERING INDEX posts_created (created>?)
```

The keyset query returns exactly the same pages, and its work stays about the same however deep the page is, while `OFFSET`'s work grows with every row it skips. It needs a **unique** sort key (here `created` then `id`), and it moves to the next or previous page rather than jumping to page 500.

### One Query per Row (N+1)

Loading 100 orders and then running one more query for each order's lines sends 101 statements. A join sends one. This counts them with SQLite's trace callback:

```python
store = sqlite3.connect(":memory:", isolation_level=None)
store.executescript("""
    CREATE TABLE orders (id INTEGER PRIMARY KEY);
    CREATE TABLE lines (order_id INTEGER NOT NULL, product TEXT NOT NULL);
    CREATE INDEX lines_order ON lines (order_id);
""")
store.executemany("INSERT INTO orders VALUES (?)", ((n,) for n in range(1, 101)))
store.executemany("INSERT INTO lines VALUES (?, ?)", ((n, f"product-{n % 7}-{k}") for n in range(1, 101) for k in range(3)))
statements = []
store.set_trace_callback(statements.append)

one_by_one = [(order, product)
              for (order,) in store.execute("SELECT id FROM orders ORDER BY id").fetchall()
              for (product,) in store.execute("SELECT product FROM lines WHERE order_id = ? ORDER BY product", (order,))]
print("one query per order:", len(statements), "statements")
statements.clear()
joined = store.execute("""SELECT o.id, l.product FROM orders o JOIN lines l ON l.order_id = o.id
                          ORDER BY o.id, l.product""").fetchall()
print("one join:           ", len(statements), "statement")
print("same rows:", one_by_one == joined, f"({len(joined)} rows)")
```

```text
one query per order: 101 statements
one join:            1 statement
same rows: True (300 rows)
```

In a client-server database, each statement is usually a separate round trip over the network, so this pattern, often hidden inside object-relational mapping code, adds up quickly.

## 🛠️ A Tuning Routine

1. **Measure** first, and find the queries that are actually slow.
2. **Read the plan** for each, remembering that `EXPLAIN ANALYZE` runs the query.
3. **Change one thing:** add or reshape an index for the real `WHERE`, `JOIN`, and `ORDER BY` clauses; rewrite a condition so that an index can be used; select only the columns you need; or fix a pattern such as N+1.
4. **Measure again**, with data of a realistic size and shape.
5. **Keep statistics current** (`ANALYZE` in SQLite after large changes), and remove indexes that no query uses.

[indexes.md](../../../backend/sql-fundamentals/indexes.md) gives practical advice on choosing indexes, and the [Caching: Local and Redis](../../../backend/caching-local-and-redis/README.md) module covers reusing results instead of repeating the same work.

## ✅ Checking the Code

The whole lesson printed identical plans and work counts in 25 runs, and every plan it prints matched the plan from a new connection at the same stage, which rules out stale cached plans. A separate checker confirmed that indexed queries returned the same rows as a plain Python filter, also after `ANALYZE`; that `LIKE` used a `NOCASE` index; and that the page-read model agreed with a brute-force version. The join algorithms matched a brute-force join on 1,500 random inputs (repeated customer ids only for the nested loop and hash joins), the join-order counts matched fully built intermediate results on 300 random shops, and walking through keyset pages returned every row once, in the same order as `OFFSET` pages.

## Common Misconceptions

- **"The database runs the query the way I wrote it."** The optimizer may reorder joins and choose indexes.
- **"If an index exists, it will be used."** Only if the query's conditions fit it and the optimizer expects it to help.
- **"An index scan is always faster than a full scan."** Not when many rows match and their pages are scattered.
- **"`EXPLAIN ANALYZE` is harmless."** It runs the statement, including any changes it makes.
- **"`OFFSET` is cheap because only ten rows come back."** The skipped rows are still visited.

## ➡️ Next

This completes the Database Classification and Optimisation module, and with it the [Database Management Systems section](../README.md). For practice with real databases, continue with [SQL Fundamentals](../../../backend/sql-fundamentals/README.md) and [Database Design and Modeling](../../../backend/database-design-and-modeling/README.md).
