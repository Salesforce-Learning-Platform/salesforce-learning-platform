# The Aggregation Pipeline

## A Pipeline of Stages

```js
db.products.aggregate([
  { $match: { category: "electronics" } },
  { $group: { _id: "$category", avgPrice: { $avg: "$price" }, count: { $sum: 1 } } },
  { $sort: { avgPrice: -1 } },
]);
```

The **aggregation pipeline** processes documents through a sequence of **stages**, where each
stage's output becomes the next stage's input — directly comparable to
[SQL's `aggregations.md`](../sql-fundamentals/aggregations.md)'s combination of `WHERE`,
`GROUP BY`, and `ORDER BY`, just expressed as an explicit, ordered array of stages rather than a
single combined statement.

## `$match` — Filtering, Like `WHERE`

```js
{ $match: { category: "electronics" } }
```

`$match` filters documents through to the next stage — functionally identical to
[querying-documents.md](querying-documents.md)'s `find()` filter syntax, and directly analogous to
SQL's `WHERE`. Placing `$match` as early as possible in a pipeline is a meaningful performance
practice: filtering down to fewer documents *before* more expensive stages (like `$group`) run
means those later stages have less data to process.

## `$group` — Aggregating, Like `GROUP BY`

```js
{ $group: { _id: "$category", totalRevenue: { $sum: "$price" }, count: { $sum: 1 } } }
```

`$group` collapses documents sharing the same `_id` expression (here, `$category`) into one
output document per group, computing aggregates (`$sum`, `$avg`, `$max`, `$min` — the same
functions from [SQL's aggregations.md](../sql-fundamentals/aggregations.md)) across each group.
The `$` prefix (`$category`, `$price`) refers to a field's *value* within each document being
processed — a syntax convention used consistently throughout aggregation pipeline stages.

## `$sort` and `$project`

```js
{ $sort: { totalRevenue: -1 } }        // descending, like SQL's ORDER BY ... DESC

{ $project: { name: 1, price: 1, _id: 0 } }  // include name and price, exclude _id
```

`$sort` orders documents, directly parallel to SQL's `ORDER BY`. `$project` reshapes each
document's output — `1` includes a field, `0` excludes it — the aggregation-pipeline equivalent of
choosing specific columns in a SQL `SELECT` rather than using `*`.

## `$lookup` — MongoDB's Version of a `JOIN`

```js
db.orders.aggregate([
  {
    $lookup: {
      from: "products",
      localField: "productId",
      foreignField: "_id",
      as: "productDetails",
    },
  },
]);
```

`$lookup` performs a left-outer-join-style operation against another collection — directly
comparable to [SQL's `LEFT JOIN`](../sql-fundamentals/joins.md). `localField`/`foreignField` name
which fields to match on (paralleling a SQL `JOIN ... ON` condition), and `as` names the new array
field holding the matched documents from the other collection.

## A Realistic Combined Pipeline

```js
db.orders.aggregate([
  { $match: { status: "completed" } },
  { $lookup: { from: "products", localField: "productId", foreignField: "_id", as: "product" } },
  { $group: { _id: "$product.category", totalRevenue: { $sum: "$total" } } },
  { $sort: { totalRevenue: -1 } },
]);
```

This mirrors [SQL's combined aggregation example](../sql-fundamentals/aggregations.md) closely:
filter to completed orders, join in each order's product, group by category to sum revenue, and
sort the result — the same real analytics question, expressed as an explicit pipeline of stages
instead of one SQL statement.

## Common Mistakes

- Placing `$match` late in a pipeline (or omitting it entirely) when it could run first, forcing
  expensive later stages to process far more documents than necessary.
- Forgetting the `$` prefix when referencing a field's value inside a stage (`category` instead of
  `$category`) — without it, MongoDB treats it as a literal string, not a reference to the field.
- Assuming `$lookup` behaves like a SQL `INNER JOIN` by default — it's structurally closer to a
  `LEFT JOIN`, always including the original document even when no match is found in the joined
  collection (with an empty array for `as` in that case).

## Next

Continue to [data-modeling.md](data-modeling.md) to make the single most consequential design
decision in MongoDB: whether to embed or reference related data in the first place.
