# 🐛 Debugging Difficulty Across Agents

## "Which Agent Actually Caused This?"

A single agent producing a wrong final answer has exactly one place to look: that agent's own
reasoning and tool calls. A multi-agent pipeline producing a wrong final answer could have gone
wrong at *any* stage — the researcher gathered incomplete information, the writer misrepresented
correct information, or the critic approved a flawed draft it should have caught. Genuinely
diagnosing which stage is actually responsible is the core added debugging cost of this
architecture.

## A Concrete Failure Scenario

```
Final report contains a factual error about "Company X's 2024
revenue."

Was it:
1. The RESEARCHER's fault — it retrieved outdated or wrong data?
2. The WRITER's fault — it correctly received good data, but
   misrepresented it while writing?
3. The CRITIC's fault — it reviewed the draft and approved it
   anyway, missing the error?
```

Without visibility into each stage's *individual* input and output — not just the final result —
this question is genuinely unanswerable. This is exactly why
[logging-every-step-of-the-pipeline.md](logging-every-step-of-the-pipeline.md), later in this
module, is not optional infrastructure for a multi-agent system — it's the only way to actually
answer this question when it inevitably comes up.

## Non-Determinism Compounds Across Stages

```
A SINGLE model call is already probabilistic (per
deterministic-vs-probabilistic-outputs.md) — the SAME prompt can
occasionally produce a different result.

A pipeline of THREE such calls compounds this: even if each
individual stage is only "occasionally" wrong, the END-TO-END
pipeline's overall failure rate is higher than any single stage's
own rate.
```

This compounding effect is a genuine, easy-to-overlook cost specific to multi-stage systems: a
pipeline with three stages, each individually correct 95% of the time, has a meaningfully lower
end-to-end success rate than 95% — closer to 0.95³ ≈ 86%, if the stages' errors are independent.
This is exactly why [evaluating-retrieval-quality.md](../evaluating-ai-systems/evaluating-retrieval-quality.md)'s
evaluation-set discipline matters even more for a multi-stage pipeline than a single call.

## Reproducing a Failure Is Harder, Too

```
A single agent's failure: re-run the SAME prompt, likely
reproduce something close to the original behavior

A multi-agent pipeline's failure: EACH stage's output feeds the
next, so reproducing the exact failure means reproducing the
EXACT sequence of intermediate outputs — much harder when each
stage is independently probabilistic
```

Debugging a multi-agent pipeline often means working from **logged, captured intermediate outputs**
from the actual failed run, rather than trying to reproduce the failure fresh — a real production
incident's exact intermediate research summary or draft is often the only reliable way to understand
what actually went wrong.

## A Practical Debugging Discipline

```python
def run_pipeline_with_trace(input_data):
    trace = {"input": input_data, "stages": []}

    research = research_agent(input_data)
    trace["stages"].append({"stage": "researcher", "output": research})

    draft = writer_agent(research)
    trace["stages"].append({"stage": "writer", "output": draft})

    critique = critic_agent(draft)
    trace["stages"].append({"stage": "critic", "output": critique})

    return draft, trace  # the trace is what makes a later failure genuinely debuggable
```

Capturing every stage's actual input and output into one linked `trace` object — the same idea as
[Observability and Monitoring Basics](../evaluating-ai-systems/observability-and-monitoring-basics.md)'s
request tracing, applied specifically across agent boundaries — is what turns "the pipeline
produced a wrong answer" into "Stage 2 misrepresented Stage 1's correct data," a genuinely
actionable finding.

## Common Mistakes

- Only logging a pipeline's final output, discarding the intermediate stage results that are
  actually needed to diagnose which stage caused a given failure.
- Assuming a multi-stage pipeline is more reliable than a single agent simply because each
  individual stage is more focused — the compounding failure-rate effect can make the opposite true.
- Trying to reproduce a production failure by re-running the pipeline fresh instead of working from
  the actual logged intermediate outputs of the failed run.

## ➡️ Next

Continue to
[managing-shared-state-between-services.md](managing-shared-state-between-services.md) to see a
third architectural concern: how data actually flows and persists across multiple, separate agent
services.
