# 🗃️ Managing Shared State Between Services

## Two Very Different Deployment Shapes

```
IN-PROCESS multi-agent: all agents run as Python function calls
  within ONE application process — state passes as ordinary
  function arguments and return values

MULTI-SERVICE multi-agent: each agent runs as its OWN deployed
  service (separate processes, possibly separate servers) -
  state must be passed over the NETWORK, and persisted somewhere
  both services can reach
```

Every example so far in this domain's agent modules has been the simpler, in-process shape. A real,
larger system sometimes genuinely needs the second shape — separate agents scaled and deployed
independently — and this introduces state-management concerns that don't exist at all in the
simpler case.

## What "Shared State" Actually Means Here

```
- The ORIGINAL user request and its full context
- Each PRIOR stage's output, needed by a LATER stage
- SESSION-level data (a user's identity, a conversation ID) that
  every stage needs, but that no single stage owns
- IN-PROGRESS status - has a given pipeline run's Stage 2 actually
  finished yet?
```

None of this is automatically available to a separate service the way it's automatically available
to a plain Python function call within one process — it all has to be deliberately passed, stored,
or looked up.

## Passing State Directly, for Simple Pipelines

```python
# Service A (researcher) calls Service B (writer) directly,
# passing everything the writer needs in the request body
response = requests.post("https://writer-service/generate", json={
    "research_summary": research_result,
    "original_question": user_question,
    "session_id": session_id,
})
```

For a straightforward, linear pipeline, passing the needed state directly in each service-to-service
request — the same idea as
[REST API Design](../../backend/rest-api-design/)'s ordinary request/response pattern — is often
simple and sufficient. This doesn't need a dedicated state-management layer at all.

## A Shared Store, for More Complex Coordination

```python
# A pipeline run's state lives in a shared store (Redis, a
# database), keyed by a run ID every stage can read and update
def start_pipeline_run(run_id, input_data):
    redis_client.set(f"pipeline:{run_id}:status", "researching")
    redis_client.set(f"pipeline:{run_id}:input", json.dumps(input_data))

def researcher_service(run_id):
    input_data = json.loads(redis_client.get(f"pipeline:{run_id}:input"))
    result = do_research(input_data)
    redis_client.set(f"pipeline:{run_id}:research", json.dumps(result))
    redis_client.set(f"pipeline:{run_id}:status", "writing")
```

For a pipeline with more complex coordination needs — multiple services that don't call each other
directly, a long-running pipeline whose status needs to be queryable independently — a shared,
persistent store (directly applying
[Caching: Local and Redis](../../backend/caching-local-and-redis/)'s patterns, now for
coordination rather than just performance) becomes genuinely necessary.

## The Real Risk: State Drift and Race Conditions

```
Two services both reading and updating the SAME pipeline run's
state, without coordination:
  → a race condition where one service's update is silently lost
    or overwrites another's
```

This is an ordinary distributed-systems problem, not something unique to AI agents — but it's easy
to underestimate specifically because a multi-agent pipeline can feel like "just calling a few
functions" when it's actually a genuinely distributed system with all the usual concurrency
concerns that implies.

## Common Mistakes

- Building a multi-service agent architecture before it's genuinely needed, when an in-process
  pipeline (much simpler, no network state to manage at all) would have worked fine.
- Passing sensitive data (like `session_id`-derived user identity) as plain, unauthenticated request
  fields between services instead of validating it server-side at each hop.
- Never considering what happens if one service in the pipeline crashes mid-run, leaving shared
  state in an inconsistent, half-updated condition.

## ➡️ Next

Continue to
[logging-every-step-of-the-pipeline.md](logging-every-step-of-the-pipeline.md) to see the logging
discipline that makes a distributed, multi-service pipeline like this genuinely operable.
