# 📈 Observability and Monitoring Basics

## From a One-Time Evaluation to Ongoing Visibility

[evaluating-retrieval-quality.md](evaluating-retrieval-quality.md)'s evaluation set answers "is this
system good right now?" Observability answers a related but different, ongoing question: "is this
system *still* behaving well in production, and can I tell exactly what happened when it wasn't?"

## The Core Metrics Worth Tracking

```
LATENCY     → how long a request takes (p50, p95, p99 — not just
              the average, which hides slow outliers)
COST        → token usage and $ spent, per request and aggregated
ERROR RATE  → the failure-category taxonomy from
              logging-ai-requests-and-responses-for-debugging.md,
              tracked and graphed over time, not just logged
QUALITY     → confidence scores, retrieval precision/recall
              (from this module's own earlier files), tracked as
              a trend rather than a one-off check
```

These four categories — directly building on
[logging-ai-requests-and-responses-for-debugging.md](../error-handling-in-ai-applications/logging-ai-requests-and-responses-for-debugging.md)'s
structured logging discipline — turn individual log lines into aggregate, trackable signals a team
can actually monitor and alert on.

## Tracing: Following One Request End-to-End

```
A single user question, in a RAG system, involves MULTIPLE steps:
  1. Embed the query
  2. Query the vector database
  3. Build the prompt
  4. Call the model
  5. Validate the structured response

A TRACE captures all five steps, with their individual timings and
outcomes, as ONE linked unit — not five disconnected log lines.
```

Tracing is what makes a complex, multi-step AI feature actually debuggable: instead of trying to
manually correlate five separate log entries by approximate timestamp, a trace shows the entire
request's full path — including which specific step was slow, or which step actually failed — as
one coherent unit.

## Dedicated LLM Observability Tools

```
Purpose-built platforms — Langfuse (open-source, self-hostable) and
LangSmith (from the LangChain team) among the best-known — provide
tracing, cost/latency dashboards, and prompt-level analytics
SPECIFICALLY designed around LLM application concepts (token usage,
prompt/completion pairs, evaluation scores).
```

Rather than building this tracing and dashboarding infrastructure from scratch, dedicated LLM
observability platforms exist precisely because generic application-monitoring tools weren't
designed around LLM-specific concepts like token counts, prompt versions, and model-quality scores
— they're worth evaluating before building custom tooling for anything beyond a small prototype.

## Alerting on the Signals That Actually Matter

```
Alert-WORTHY:  error rate crosses 5% over 10 minutes; p95 latency
               doubles; average confidence score drops sharply
NOT necessarily alert-worthy: a single request's failure — that's
               noise an alerting threshold should be tuned to ignore
```

An alert should fire on a genuine, sustained shift in a tracked metric — not on every single
individual failure, which (per
[never-trust-ai-output-without-validation.md](../schema-validation-with-zod/never-trust-ai-output-without-validation.md)'s
framing of AI output as inherently probabilistic) is an expected, occasional occurrence rather than
an emergency on its own.

## Common Mistakes

- Tracking only the average latency, hiding a meaningful fraction of genuinely slow requests behind
  a healthy-looking mean.
- Logging each step of a multi-step AI feature separately with no way to correlate them into one
  coherent trace of a single request.
- Setting alert thresholds so sensitive that individual, expected failures trigger constant noise,
  training the team to ignore alerts entirely.

## Module Summary

Across this module: **hallucination detection** uses grounding checks against retrieved context
(especially tractable for RAG systems) and self-consistency sampling, since no single technique
guarantees catching every fabrication (see
[detecting-hallucinations.md](detecting-hallucinations.md)); **confidence scores** are most
reliable when combining self-reported model confidence with independent signals like retrieval
similarity and consistency checks, always displayed in a way that actually changes what the user
sees (see [assigning-confidence-scores.md](assigning-confidence-scores.md)); **retrieval quality**
is measured separately from answer quality using precision@k, recall@k, and MRR against a real,
maintained evaluation set (see
[evaluating-retrieval-quality.md](evaluating-retrieval-quality.md)); and **observability** —
latency, cost, error rate, and quality metrics, tied together through request-level tracing, often
via a dedicated LLM observability platform — turns a one-time evaluation into ongoing, actionable
visibility into a system's real production behavior.
