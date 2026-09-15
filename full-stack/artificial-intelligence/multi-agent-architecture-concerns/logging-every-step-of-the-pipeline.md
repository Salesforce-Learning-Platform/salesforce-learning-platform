# 📋 Logging Every Step of the Pipeline

## The Non-Negotiable Infrastructure for This Architecture

[debugging-difficulty-across-agents.md](debugging-difficulty-across-agents.md) established *why*
per-stage logging matters so much more here than for a single agent. This file covers what
that logging discipline should actually look like for a genuine multi-agent or multi-stage
pipeline — extending
[logging-ai-requests-and-responses-for-debugging.md](../error-handling-in-ai-applications/logging-ai-requests-and-responses-for-debugging.md)'s
per-call discipline to an entire, linked pipeline run.

## A Pipeline-Run ID Ties Everything Together

```python
import uuid

def run_pipeline(input_data):
    pipeline_run_id = str(uuid.uuid4())  # ONE id for the entire run

    research = research_agent(input_data)
    log_stage(pipeline_run_id, "researcher", input_data, research)

    draft = writer_agent(research)
    log_stage(pipeline_run_id, "writer", research, draft)

    return draft, pipeline_run_id
```

Every stage's log entry shares the *same* `pipeline_run_id` — this single id is what lets a later
investigation pull every stage of one specific, failed run back together, exactly like a distributed
trace ties together the individual steps of one request in
[Observability and Monitoring Basics](../evaluating-ai-systems/observability-and-monitoring-basics.md).

## What Each Stage's Log Entry Needs

```python
def log_stage(pipeline_run_id, stage_name, stage_input, stage_output):
    logger.info("pipeline_stage", {
        "pipeline_run_id": pipeline_run_id,
        "stage": stage_name,
        "input_summary": summarize(stage_input),   # not always the FULL input - see below
        "output_summary": summarize(stage_output),
        "duration_ms": ...,
        "token_usage": ...,
        "timestamp": datetime.utcnow().isoformat(),
    })
```

Each entry needs enough detail to answer "what did this specific stage receive, and what did it
produce?" — directly the information [debugging-difficulty-across-agents.md](debugging-difficulty-across-agents.md)
established is otherwise unrecoverable once a pipeline run has finished and its in-memory state is
gone.

## The Same Privacy Discipline, at Pipeline Scale

```
NEVER log, even across a multi-stage pipeline:
  - full raw content containing more PII than needed to diagnose
    a specific failure
  - API keys or session tokens passed between services
```

[logging-ai-requests-and-responses-for-debugging.md](../error-handling-in-ai-applications/logging-ai-requests-and-responses-for-debugging.md)'s
"what NOT to log" guidance applies with even more force here — a multi-stage pipeline logs *more*
individual entries than a single call, and each one is a potential place for sensitive data to leak
into logs if this discipline isn't applied consistently at every single stage.

## Reconstructing a Failed Run

```python
def get_pipeline_trace(pipeline_run_id):
    entries = log_store.query({"pipeline_run_id": pipeline_run_id})
    return sorted(entries, key=lambda e: e["timestamp"])
```

Being able to pull every logged stage for one specific `pipeline_run_id`, in order, is the actual
practical payoff of this discipline: a support engineer or developer investigating a specific
reported failure can reconstruct exactly what happened at each stage of that one run, rather than
guessing from the final output alone.

## Dashboarding Per-Stage Failure Rates

```
Aggregate ACROSS many pipeline runs (not just one):
  "researcher" stage failure rate: 2%
  "writer" stage failure rate:     8%   <- the actual weak link
  "critic" stage failure rate:     1%
```

Beyond debugging one specific incident, aggregating this same per-stage logging across many runs
reveals *which stage* is systematically the weakest link in the pipeline — directly informing where
prompt improvements or schema changes should actually be focused, rather than guessing.

## Common Mistakes

- Logging each stage independently without a shared `pipeline_run_id`, making it impossible to
  reconstruct one specific run's full sequence of stages later.
- Logging full raw content at every stage without the same privacy discipline established for a
  single AI call, multiplying the exposure risk across a multi-stage pipeline.
- Only ever looking at individual failed runs, never aggregating per-stage failure rates to find the
  pipeline's actual systematic weak point.

## ➡️ Next

Continue to
[understanding-that-multi-agent-systems-are-not-always-the-best-solution.md](understanding-that-multi-agent-systems-are-not-always-the-best-solution.md)
to bring every concern from this module together into a final, practical decision framework.
