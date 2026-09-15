# 🔭 Monitoring and Observability

## 📚 Overview

[CI/CD Pipelines](../ci-cd-pipelines/) got code deployed reliably. This module covers what happens
next: knowing whether a running, deployed application is actually healthy — through observability's
broader investigative capacity, concrete application monitoring practices, the metrics that quantify
system behavior, and the alerting that turns those metrics into timely, actionable notification.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Distinguish observability from monitoring, and explain the three pillars (metrics, logs, traces).
- Implement shallow and deep health checks, and explain the value of external uptime monitoring.
- Choose the correct metric type (counter, gauge, histogram, summary) for a given measurement.
- Design alert rules that fire on genuine, sustained problems, with appropriate severity routing.

## 📋 Prerequisites

- [CI/CD Pipelines](../ci-cd-pipelines/) — this module assumes an application is already reliably deployed and now needs ongoing health visibility.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [what-is-observability.md](what-is-observability.md) | Monitoring vs. observability, and the three pillars: metrics, logs, traces |
| [application-monitoring.md](application-monitoring.md) | Shallow vs. deep health checks, external uptime monitoring, and APM |
| [metrics.md](metrics.md) | Counter/gauge/histogram/summary, real instrumentation code, and why percentiles beat averages |
| [alerts.md](alerts.md) | Alert rules, severity routing, runbooks, and avoiding alert fatigue; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you'll be operating any application real users depend on — this module's practices
are what actually catch problems before (or as) they affect users, rather than after a complaint.

**Skim** if you're using a platform that already provides built-in monitoring and alerting — the
underlying concepts (what to watch, how to alert well) still transfer directly.

## 🧠 Knowledge Check

<details>
<summary>Why is a shallow health check (<code>res.send("ok")</code> unconditionally) misleading?</summary>

It can never actually fail, since it doesn't verify any of the application's real dependencies (a
database connection, a cache). A server can be technically "up" while a critical dependency is
silently broken — a deep health check that actually queries those dependencies is needed to catch
this.

</details>

<details>
<summary>Why should an alert require a condition to be sustained (e.g. <code>for: 10m</code>) rather than firing on a single momentary spike?</summary>

Firing on every transient blip generates noise for conditions that resolve themselves without any
real intervention needed, training a team to start ignoring alerts — exactly the alert-fatigue
failure mode that lets a genuinely serious, sustained incident go unnoticed among the noise.

</details>

## 📚 References

- [Prometheus - Metric Types](https://prometheus.io/docs/concepts/metric_types/) — official documentation for Counter, Gauge, Histogram, and Summary
- [prom-client (npm)](https://github.com/siimon/prom-client) — the Node.js Prometheus client library used in this module's instrumentation example

## ➡️ Continue Your Learning Path

Continue to [Logging in Production](../logging-in-production/) to see the logs pillar of
observability in full depth.
