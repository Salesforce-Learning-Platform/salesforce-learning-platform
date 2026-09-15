# 🚨 Alerting

## From "Data Someone Could Check" to "Notified Automatically"

[metrics.md](metrics.md) covered the raw data. Alerting is what turns that data into something
*actionable* — automatically notifying the right people the moment a metric crosses a threshold
that actually matters, rather than relying on someone happening to check a dashboard.

## A Basic Alert Rule

```yaml
# Prometheus alerting rule
groups:
  - name: application-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 10m
        annotations:
          summary: "Error rate above 5% for 10 minutes"
```

This rule fires when the rate of 5xx responses exceeds 5% of total requests, *sustained* for 10
minutes (`for: 10m`) — not on a single momentary spike. This directly echoes
[observability-and-monitoring-basics.md](../../artificial-intelligence/evaluating-ai-systems/observability-and-monitoring-basics.md)'s
earlier guidance, from this repository's AI Engineering domain: an alert should fire on a genuine,
sustained shift, not on every single individual, expected blip.

## Choosing What's Genuinely Worth an Alert

```
ALERT-WORTHY:  error rate sustained above a real threshold; the
               entire application unreachable; a critical
               dependency (database) down

NOT alert-worthy: a single request's transient failure; normal,
               expected fluctuation within a known range
```

This distinction is genuinely important for a real, sustainable on-call practice — over-alerting on
noise trains a team to start ignoring alerts entirely, which is precisely the failure mode that lets
a genuinely serious incident go unnoticed among constant, low-value notifications.

## Alert Severity and Routing

```
CRITICAL → pages someone immediately, even outside business hours
           (the entire application is down)

WARNING  → a less urgent notification (Slack, email) - something
           worth investigating soon, but not an active emergency
```

Not every alert deserves the same urgency — routing critical, genuinely urgent alerts to an
immediate page while sending lower-severity warnings through a less disruptive channel keeps the
most urgent signal from getting lost among less critical ones.

## Runbooks: What to Actually Do When an Alert Fires

```yaml
annotations:
  summary: "Error rate above 5% for 10 minutes"
  runbook: "https://wiki.internal/runbooks/high-error-rate"
```

A genuinely mature alerting setup links each alert to a **runbook** — documented steps for actually
investigating and responding to that specific alert. Without this, an alert firing at 3 AM leaves
whoever's paged to figure out the entire response from scratch, under real time pressure — a
runbook turns that into a known, practiced procedure instead.

## Alert Fatigue: the Real, Practical Risk

```
TOO MANY alerts, too many false positives → the team starts
  ignoring them, or muting the alerting channel entirely →
  a GENUINE incident goes unnoticed among the noise
```

This is a real, well-documented failure mode worth taking seriously: an alerting system's value
depends entirely on alerts actually being trusted and acted on — a system that alerts too
aggressively, on things that don't genuinely matter, actively undermines its own purpose over time.

## Common Mistakes

- Setting an alert threshold so sensitive that normal, expected fluctuation repeatedly triggers it,
  training the team to ignore alerts from that system.
- Alerting on a single momentary spike instead of a sustained condition, generating noise for
  transient blips that resolve themselves.
- Configuring an alert with no accompanying runbook, leaving whoever responds to figure out the
  entire investigation and response process under real, live time pressure.

## Module Summary

Across this module: **observability** is the broader capacity to investigate genuinely unanticipated
problems, built on the three complementary pillars of metrics, logs, and traces — distinct from
monitoring's narrower focus on predefined, known signals (see
[what-is-observability.md](what-is-observability.md)); **application monitoring** uses shallow and
deep health checks, external uptime monitoring, and APM tooling to track whether a running
application is actually healthy, not just technically running (see
[application-monitoring.md](application-monitoring.md)); **metrics** — counters, gauges,
histograms, and summaries, verified against Prometheus's own official concept definitions — track
numerical data over time, with percentile-aware metrics revealing tail latency an average alone
would hide (see [metrics.md](metrics.md)); and **alerting** turns that data into automatic
notification on genuine, sustained problems, with severity-based routing and runbooks turning a
crisis response into a known, practiced procedure rather than a from-scratch investigation.
