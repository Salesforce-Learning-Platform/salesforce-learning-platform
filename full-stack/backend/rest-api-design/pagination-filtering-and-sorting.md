# Pagination, Filtering, and Sorting

## Why a Collection Endpoint Can't Just Return Everything

```
GET /products
```

Returning every single product in one response works fine with 20 products in a database — and
becomes a real problem with 200,000: a massive response payload, a slow database query, and a
frontend forced to render an unusably long list all at once. Collection endpoints need a
deliberate strategy for returning a manageable slice of the data instead.

## Pagination: Returning One Page at a Time

```
GET /products?page=2&limit=20
```

```json
{
  "data": [ /* 20 products */ ],
  "pagination": {
    "page": 2,
    "limit": 20,
    "totalItems": 347,
    "totalPages": 18
  }
}
```

**Pagination** splits a large collection into pages, with `page` and `limit` (or an equivalent pair
of parameters) as query parameters — recall
[routing.md](../expressjs-fundamentals/routing.md)'s distinction between route parameters (which
resource) and query parameters (options on the request): pagination is squarely the latter, since
it's not identifying a different resource, just a different slice of the same collection. A
well-designed paginated response also includes metadata (`totalItems`, `totalPages`) so the client
knows how many pages exist without needing a separate request.

## An Alternative: Cursor-Based Pagination

```
GET /products?cursor=eyJpZCI6NDJ9&limit=20
```

Page-number pagination (`?page=2`) has a subtle problem: if an item is inserted or deleted between
two requests, page boundaries can shift, causing a client to see a duplicate or skip an item
entirely. **Cursor-based pagination** instead returns an opaque token (`cursor`) pointing at
exactly where the *previous* page ended, avoiding that shifting-boundary problem — commonly
preferred for large, frequently-changing datasets (like a live social media feed), at the cost of
not letting a client jump directly to an arbitrary page number.

## Filtering

```
GET /products?category=electronics&minPrice=50
```

```js
app.get("/products", (req, res) => {
  let results = products;
  if (req.query.category) {
    results = results.filter((p) => p.category === req.query.category);
  }
  if (req.query.minPrice) {
    results = results.filter((p) => p.price >= Number(req.query.minPrice));
  }
  res.json(results);
});
```

**Filtering** narrows a collection down based on field values, expressed as query parameters named
after the fields being filtered on. Each filter parameter should be genuinely optional — a request
with none applies no filtering at all, returning the full (paginated) collection.

## Sorting

```
GET /products?sort=price          (ascending, by default)
GET /products?sort=-price         (descending — a leading "-" is a common convention)
GET /products?sort=-price,name    (multiple sort keys, comma-separated)
```

**Sorting** controls the order results are returned in, via a `sort` query parameter naming the
field(s) to sort by — a leading `-` (or a separate `order=desc` parameter, an equally valid
alternative convention) commonly signals descending order.

## Common Mistakes

- Building a collection endpoint with no pagination at all, working fine in early development with
  a small dataset and becoming a real production performance problem once the data grows.
- Using page-number pagination for a rapidly-changing, large dataset where items are frequently
  inserted or removed, causing users to intermittently see duplicate or skipped items.
- Applying filters as if they were required — a filterable endpoint should work correctly with
  zero filter parameters supplied, returning the full (still paginated) collection.

## Next

Continue to [api-versioning.md](api-versioning.md) to see how an API evolves over time without
breaking the clients already depending on it.
