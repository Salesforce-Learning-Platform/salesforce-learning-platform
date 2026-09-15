# 🗄️ Centralized Logging

## The Problem: Logs Scattered Across Many Servers

```
A system running on MULTIPLE servers/containers, each writing
its OWN local log files:

"Investigate why order 4821 failed" → requires manually checking
  logs on potentially SEVERAL different machines, hoping you know
  which ones were actually involved
```

This is the practical problem centralized logging solves: as soon as an application runs on more
than one server or container (which is almost always, per
[Docker Compose](../docker-and-containerization/docker-compose.md) and
[horizontal scaling](../cloud-infrastructure/virtual-machines.md), earlier in this domain), logs
scattered across each individual machine become genuinely impractical to search manually.

## The ELK Stack: A Widely-Used Centralized Logging Solution

```
LOGSTASH      → collects and processes logs from EVERY service,
                normalizing them into a consistent format

ELASTICSEARCH → stores and INDEXES the processed logs, enabling
                fast search across the ENTIRE collection

KIBANA        → the VISUAL interface for searching, filtering,
                and building dashboards from that log data
```

"ELK" (Elasticsearch, Logstash, Kibana) is one of the most widely-used, open-source centralized
logging stacks — every service in a system ships its logs to this central pipeline instead of
writing only to its own local disk, making the entire system's logs searchable from one place.

## Shipping Structured Logs to a Central Store

```
Application → writes STRUCTURED (JSON) logs (per structured-
  logging.md) to stdout →
A log SHIPPER/AGENT on each server/container reads that output
  and forwards it to the central logging system (Logstash, or an
  equivalent) →
Centrally stored, indexed, and SEARCHABLE across every service at
  once
```

This is exactly why [structured-logging.md](structured-logging.md)'s JSON format matters so much in
practice — a centralized system can only meaningfully search and filter on structured fields; plain-
text logs shipped centrally are still just as hard to query precisely, even after being centralized.

## Log Retention: Not Everything Stays Forever

```
Keeping EVERY log entry FOREVER: genuinely expensive at real
  scale, and often unnecessary

A deliberate RETENTION POLICY (e.g. keep detailed logs for 30
  days, aggregated summaries longer) balances actual
  investigative need against real storage cost.
```

This is a genuinely practical operational decision every real logging system needs — indefinite
retention isn't free, and a deliberate policy (how long is genuinely needed for realistic
investigation, versus how long is simply accumulating unused cost) is worth establishing
explicitly rather than defaulting to "keep everything forever" by accident.

## Searching Centralized Logs During an Incident

```
"Find every log entry with requestId=req-a1b2c3, across EVERY
service, in the last hour" - a query a centralized system answers
DIRECTLY, in seconds - the same query against scattered,
per-server local files would take vastly longer, manually.
```

This is the real, practical payoff of everything this module has built toward — the structured
fields and request IDs from [structured-logging.md](structured-logging.md), centrally aggregated,
turn a slow, manual, multi-server investigation into a single, fast, precise query.

## Common Mistakes

- Relying on individual servers' local log files for a multi-service system, making incident
  investigation genuinely slow and manual at real scale.
- Setting no retention policy at all, letting log storage costs grow indefinitely for data that's
  realistically never queried again after a short initial window.
- Centralizing logs without first structuring them properly, missing most of the real query and
  filtering benefit centralization is meant to provide.

## Module Summary

Across this module: **logs** are the discrete, timestamped record of what actually happened —
often the *only* evidence available after a production incident, since a debugger can't be
attached retroactively (see [logging-fundamentals.md](logging-fundamentals.md)); **log levels**
(DEBUG through FATAL) let genuinely important entries be distinguished from routine activity, with
DEBUG-level logging appropriately disabled in production per this domain's environment-management
principles (see [log-levels.md](log-levels.md)); **structured logging** — consistent JSON fields
and shared request IDs across every service — is what turns logs from something a human scans
manually into something a system can precisely query (see
[structured-logging.md](structured-logging.md)); and **centralized logging**, via a stack like ELK,
aggregates every service's structured logs into one searchable place, with a deliberate retention
policy balancing genuine investigative need against real, ongoing storage cost.
