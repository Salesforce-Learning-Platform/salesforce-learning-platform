# 📟 Application Monitoring

## What Actually Gets Watched, Day to Day

[what-is-observability.md](what-is-observability.md) covered the broader philosophy. Application
monitoring is the concrete, practical layer built on top of it: specific, ongoing checks that tell
a team whether a running application is currently healthy.

## Health Checks: The Most Basic Form of Monitoring

```js
app.get("/health", (req, res) => {
  res.status(200).json({ status: "ok", timestamp: new Date().toISOString() });
});
```

A health check endpoint is exactly what it sounds like — a simple, fast endpoint a monitoring
system polls regularly. This directly parallels
[Docker Compose](../docker-and-containerization/docker-compose.md)'s `healthcheck` directive,
earlier in this domain — the same underlying idea, now checked continuously by an external
monitoring system rather than only once, at container startup.

## Deep Health Checks: Verifying Real Dependencies

```js
app.get("/health", async (req, res) => {
  try {
    await db.query("SELECT 1");         // is the database actually reachable?
    await redis.ping();                  // is the cache actually reachable?
    res.status(200).json({ status: "ok" });
  } catch (err) {
    res.status(503).json({ status: "unhealthy", reason: err.message });
  }
});
```

A "deep" health check verifies the application's actual dependencies, not just that the process
itself is running — a server can be technically "up" while its database connection is silently
broken, and a shallow health check would never catch this. This is a genuinely important
distinction: monitoring should verify what actually matters for the application to function, not
just that a process exists.

## Uptime Monitoring: Checking From the Outside

```
An EXTERNAL monitoring service pings https://myapp.com/health
every 60 seconds, from OUTSIDE the application's own
infrastructure - catching failures a purely internal check might
miss (DNS misconfiguration, a firewall rule blocking traffic, the
ENTIRE server being unreachable).
```

Internal monitoring (the application checking its own dependencies) and external uptime monitoring
(a separate service checking reachability from outside) catch genuinely different failure classes —
relying on only one leaves real gaps the other would have caught.

## Application Performance Monitoring (APM)

```
APM tools track, PER REQUEST:
  - response time
  - which specific code path/database query was slow
  - error rates broken down by endpoint
```

Beyond simple up/down health checks, APM tooling provides the detailed, per-request visibility that
turns "the app feels slow" into an actual, specific, actionable finding — directly the same
diagnostic value the tracing concept from
[what-is-observability.md](what-is-observability.md) provides, applied specifically to performance.

## Common Mistakes

- Implementing only a shallow health check (`res.send("ok")` unconditionally) that can never
  actually fail, providing false confidence about an application's true health.
- Relying only on internal application monitoring with no external uptime checks, missing failures
  that occur entirely outside the application's own ability to observe.
- Monitoring only whether the application is "up," with no visibility into performance — response
  time degradation is often a genuine, early warning sign of a larger problem developing.

## ➡️ Next

Continue to [metrics.md](metrics.md) to see the specific, numerical data application monitoring
actually tracks over time.
