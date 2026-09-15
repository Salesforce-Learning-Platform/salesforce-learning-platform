# 📝 Logging in Production

## 📚 Overview

[Monitoring and Observability](../monitoring-and-observability/) named logs as one of the three
pillars of observability. This module covers logging in full depth, at the production-
infrastructure level — distinct from [Logging and Monitoring](../../backend/logging-and-monitoring/)'s
coverage of the actual Node.js libraries used to generate logs in application code. It covers why
logs matter, how severity levels organize them, why structure makes them queryable, and how
centralized logging makes a multi-service system's logs searchable from one place.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain why logs are often the only evidence available after a production incident.
- Choose the correct log level (DEBUG through FATAL) for a given situation, and configure levels
  appropriately per environment.
- Write structured (JSON) log entries with consistent field names and shared request IDs.
- Explain how a centralized logging stack (like ELK) aggregates and makes searchable the logs from
  an entire multi-service system.

## 📋 Prerequisites

- [Monitoring and Observability](../monitoring-and-observability/) — this module is the deep-dive on the logs pillar introduced there.
- [Logging and Monitoring](../../backend/logging-and-monitoring/) — the application-code-level Winston/Pino implementation this module's log-level hierarchy builds on.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [logging-fundamentals.md](logging-fundamentals.md) | Why logs matter more in production than in development |
| [log-levels.md](log-levels.md) | DEBUG through FATAL, and configuring the right level per environment |
| [structured-logging.md](structured-logging.md) | JSON logs, consistent field names, and request IDs |
| [centralized-logging.md](centralized-logging.md) | The ELK stack, shipping logs centrally, and retention policy; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you're operating any system running on more than one server or service — this is
exactly the situation where scattered, per-server logs become genuinely impractical to investigate
manually.

**Skim** if you're already comfortable with structured logging from the application-code side (per
[Logging and Monitoring](../../backend/logging-and-monitoring/)) and mainly want the
production-infrastructure perspective on top of that.

## 🧠 Knowledge Check

<details>
<summary>Why are logs often the only evidence available for investigating a production incident, unlike a bug found in local development?</summary>

In local development, a bug can be reproduced by re-running the code with a debugger attached. In
production, the exact moment something went wrong is gone the instant it happens — there's no way
to retroactively attach a debugger. The logs captured at the time are the only record that will
ever exist of what actually occurred.

</details>

<details>
<summary>Why does structured (JSON) logging matter so much more once logs are centralized across multiple services?</summary>

A centralized logging system can only meaningfully search and filter on structured fields — plain-
text logs shipped to a central store are still just as hard to query precisely as they were locally.
Structured fields (and consistent naming across every service) are what actually let a query like
"every error for this user in the last 24 hours" work as a direct, fast query instead of a fragile
text search.

</details>

## 📚 References

- [Logz.io - The Complete Guide to the ELK Stack](https://logz.io/learn/complete-guide-elk-stack/) — a well-known, detailed explanation of Elasticsearch, Logstash, and Kibana

## ➡️ Continue Your Learning Path

This is the final module of the DevOps / Production Systems domain. Continue to
[The Security Mindset](../../web-security/the-security-mindset/) to begin the Web Security domain.
