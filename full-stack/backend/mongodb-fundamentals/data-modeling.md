# Data Modeling: Embedding vs. Referencing

## The Core Decision SQL Never Really Asks You to Make

In SQL, related data is almost always normalized into separate tables, joined at query time — a
default so strong [SQL's joins.md](../sql-fundamentals/joins.md) treats it as simply how relational
data works. MongoDB genuinely offers a second option: **embedding** related data directly inside a
single document. Choosing between the two — for every relationship in an application — is the
single most consequential MongoDB design decision, and unlike SQL, there's no default that's
correct most of the time.

## Embedding — Related Data Lives Inside the Same Document

```js
{
  _id: ObjectId("..."),
  name: "Alice",
  address: { street: "123 Main St", city: "Springfield" }, // embedded
}
```

**Embedding** nests related data directly within its parent document. Reading a user and their
address back out requires exactly **one** query — no `$lookup`/join needed at all, since the data
was never split apart in the first place.

## Referencing — Related Data Lives in Its Own Collection

```js
// users collection
{ _id: ObjectId("u1"), name: "Alice" }

// orders collection — references the user by ID, doesn't duplicate their data
{ _id: ObjectId("o1"), userId: ObjectId("u1"), total: 79.99 }
```

**Referencing** stores only an ID pointing at a document in another collection — directly
comparable to a SQL foreign key. Reading a user's orders together requires a `$lookup` (per
[aggregation-pipeline.md](aggregation-pipeline.md)) or a separate query, but the user's data is
never duplicated across every order.

## The Actual Decision Rule: Data Accessed Together, Stored Together

MongoDB's own core modeling principle: **data that's typically read together should generally be
stored together.** This translates into concrete guidance:

| Favor **embedding** when | Favor **referencing** when |
|---|---|
| The related data is small and has a bounded size (an address, a set of preferences) | The related data can grow large or unbounded (thousands of reviews on a product) |
| The data is almost always read together with its parent | The related data is often queried independently of its parent |
| The relationship is one-to-one, or one-to-a-few | The relationship is one-to-many-at-scale, or many-to-many |
| Duplication would be minimal or harmless | Duplicating the data would mean expensive, error-prone updates in many places |

## A Concrete Example: Product Reviews

```js
// Embedding — fine for a SMALL, bounded number of reviews shown with the product
{
  name: "Keyboard",
  reviews: [
    { user: "Alice", rating: 5, text: "Great!" },
    { user: "Bob", rating: 4, text: "Good value" },
  ],
}

// Referencing — better once a product could have THOUSANDS of reviews,
// most of which aren't needed every time the product itself is fetched
{ _id: "p1", name: "Keyboard" }               // products collection
{ productId: "p1", user: "Alice", rating: 5 }  // separate reviews collection
```

MongoDB's own documented example is exactly this kind of case: a product page showing only its five
most recent reviews is a strong signal to store *all* reviews in a separate, referenced collection
— they're not consistently accessed together with the product as a whole, and the collection could
grow unbounded over the product's lifetime.

## Common Mistakes

- Embedding a relationship that can grow unbounded (comments on a wildly popular post, reviews on a
  bestselling product) — risking hitting the 16MB document size limit, and making the parent
  document increasingly expensive to load even when most of the embedded data isn't needed.
- Referencing everything by default out of habit from SQL, missing out on embedding's real
  performance benefit (one query instead of a join) for genuinely small, tightly-coupled data.
- Treating the embed-vs-reference choice as permanent and unchangeable — real applications
  sometimes need to migrate a relationship from one approach to the other as actual access patterns
  and data volume become clearer over time.

## Next

Continue to [indexing.md](indexing.md) to see how MongoDB's indexing compares to the SQL concept
already covered.
