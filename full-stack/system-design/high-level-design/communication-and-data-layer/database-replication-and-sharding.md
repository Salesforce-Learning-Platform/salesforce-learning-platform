# 🔀 Database Replication and Sharding

## Two Genuinely Different Scaling Techniques

[sql-vs-nosql-at-scale.md](sql-vs-nosql-at-scale.md) established *which* database type to choose.
This file covers *how* either type actually scales beyond what a single database server can
handle — via two distinct, complementary techniques: replication and sharding.

## Replication: Copying Data Across Multiple Servers

```
PRIMARY (master): handles ALL WRITE operations
REPLICAS (slaves): each holds a COPY of the primary's data,
  synchronized automatically (typically within milliseconds), and
  handle READ operations
```

```
Client WRITE  → always goes to the PRIMARY
Client READ   → can go to ANY replica, DISTRIBUTING read load
                across multiple servers
```

Replication solves a genuinely common real-world pattern: most systems are read-heavy (this is
directly the case for the URL Shortener's redirect traffic, vastly outnumbering creation traffic,
per [capacity-estimation-basics.md](../system-design-foundations/capacity-estimation-basics.md)) —
distributing reads across replicas directly addresses this specific, common bottleneck.

## The Genuine Trade-Off: Replication Lag

```
Changes to the PRIMARY are synchronized to replicas "usually
within milliseconds" - but this is NOT instantaneous. A READ
hitting a replica MILLISECONDS after a write could, genuinely,
return STALE data.
```

This is a direct, concrete preview of
[consistency-vs-performance-tradeoffs.md](consistency-vs-performance-tradeoffs.md), the final file
in this module — replication is a genuinely powerful scaling technique, but it introduces a real,
measurable consistency trade-off that needs to be deliberately considered, not assumed away.

## Sharding: Splitting Data Across Independent Databases

```
Sharding splits a LARGE database into smaller, INDEPENDENT
databases (shards), each holding a SUBSET of the overall data -
directly enabling BOTH read AND write load to be distributed
across multiple servers, unlike replication (which only
distributes reads).
```

```
Shard 1: users A-M
Shard 2: users N-Z
```

Sharding solves a genuinely different problem than replication: when the *total dataset itself* is
too large for even one powerful server to hold, or when *write* volume alone exceeds what one
primary server can handle — sharding distributes the data itself, not merely copies of it.

## The Genuine Complexity Sharding Introduces

```
Applications MUST know which shard to ROUTE a given query to -
and CROSS-SHARD queries (e.g. "find the 10 most recent orders
across ALL users") become genuinely complex and expensive,
since they require querying MULTIPLE shards and combining results.
```

This is a real, practical cost worth weighing deliberately — sharding solves a genuine scaling
problem, but at the cost of meaningfully more application-level complexity for any query that needs
to span multiple shards.

## Combining Both: a Realistic, Real-World Setup

```
Shard 1 → [Primary + 2 Replicas]
Shard 2 → [Primary + 2 Replicas]
Shard 3 → [Primary + 2 Replicas]
```

```
WRITES go to the appropriate SHARD's primary.
READS can be distributed across that SAME shard's replicas.
```

This combined approach — genuinely common in real, large-scale production systems — applies both
techniques together: sharding distributes the overall dataset and write load, while replication
within each shard further distributes read load.

## Common Mistakes

- Reaching for sharding before genuinely exhausting simpler scaling options (a bigger server,
  replication alone), given the real, added application-level complexity it introduces.
- Assuming a replica always has perfectly current data, ignoring genuine replication lag when
  designing a feature that reads from a replica immediately after a related write.
- Choosing a poor sharding key (one that creates genuinely uneven distribution across shards,
  leaving some shards far more loaded than others).

## ➡️ Next

Continue to
[consistency-vs-performance-tradeoffs.md](consistency-vs-performance-tradeoffs.md) to see the
consistency implications this file's replication lag already previewed, covered in full.
