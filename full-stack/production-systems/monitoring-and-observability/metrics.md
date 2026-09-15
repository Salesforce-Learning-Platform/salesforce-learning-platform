# 📊 Metrics

## Numbers, Tracked Over Time

**Metrics** are the numerical measurements behind
[application-monitoring.md](application-monitoring.md)'s health checks and APM tooling —
[Prometheus](https://prometheus.io/), one of the most widely-used open-source monitoring systems,
defines four core metric types that cover the overwhelming majority of real monitoring needs.

## The Four Core Metric Types

```
COUNTER   → a value that only ever INCREASES (or resets to zero) -
            total requests served, total errors encountered

GAUGE     → a value that goes UP and DOWN freely - current memory
            usage, current number of active connections

HISTOGRAM → observations bucketed into ranges - request duration,
            response size - enables distribution analysis
            (e.g. "what % of requests took under 200ms?")

SUMMARY   → similar to a histogram, but calculates PERCENTILES
            directly (p50, p95, p99) over a sliding time window
```

Choosing the right metric type for a given measurement matters: using a gauge for something that
should only ever increase (like total requests served) loses the guarantee that the value can never
decrease unexpectedly, while using a counter for something that genuinely fluctuates (like memory
usage) simply doesn't fit that value's real behavior.

## A Concrete Example: Instrumenting an Express Endpoint

```js
const requestCounter = new prom.Counter({
  name: "http_requests_total",
  help: "Total number of HTTP requests",
  labelNames: ["method", "route", "status"],
});

const requestDuration = new prom.Histogram({
  name: "http_request_duration_seconds",
  help: "HTTP request duration in seconds",
  labelNames: ["method", "route"],
});

app.use((req, res, next) => {
  const end = requestDuration.startTimer({ method: req.method, route: req.path });
  res.on("finish", () => {
    requestCounter.inc({ method: req.method, route: req.path, status: res.statusCode });
    end();
  });
  next();
});
```

This is real, working instrumentation: every request increments a labeled counter and records its
duration in a histogram — labels (`method`, `route`, `status`) let these metrics later be broken
down and filtered (e.g. "error rate, specifically for `POST /orders`") rather than only viewed as
one undifferentiated total.

## Why Percentiles Matter More Than Averages

```
AVERAGE response time: 120ms  - sounds fine

p99 response time: 4,200ms   - the SLOWEST 1% of requests are
                                genuinely, badly slow, completely
                                hidden by the average
```

This is a genuinely important, easy-to-miss lesson: an average can look perfectly healthy while a
real, meaningful fraction of actual users experience a badly degraded response time — this is
exactly why `histogram`/`summary` metrics, which preserve percentile detail, matter more than a
single average number for understanding real user experience.

## Dashboards: Visualizing Metrics Over Time

```
A dashboard (commonly built with Grafana, paired with Prometheus)
turns raw metric data into VISUAL trends - a graph of error rate
over the last 24 hours is far more immediately useful than
scanning raw numbers.
```

This is the practical, day-to-day interface most engineers actually use — the raw metrics
themselves are the underlying data, but a well-designed dashboard is what makes that data genuinely
usable for spotting trends and anomalies at a glance.

## Common Mistakes

- Using a gauge for a value that should only ever increase (like total requests), losing the
  semantic guarantee a counter would have correctly provided.
- Relying only on average response time, missing a real, significant tail of badly slow requests a
  percentile-aware metric would have surfaced clearly.
- Adding so many labels to a metric that its cardinality explodes (a unique label combination for
  every individual user ID, for instance), which can genuinely degrade a monitoring system's own
  performance.

## ➡️ Next

Continue to [alerts.md](alerts.md) to see how metrics like these actually notify a team when
something goes wrong, rather than only being available for someone to check manually.
