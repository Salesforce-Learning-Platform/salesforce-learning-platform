# 🧯 Handling Invalid or Mismatched Responses

## Detecting Failure Is Only Half the Job

[verifying-ai-responses-against-a-schema.md](verifying-ai-responses-against-a-schema.md) covered
*detecting* a validation failure. What an application actually **does** with that failure is an
equally important, separate decision — and it should never be "nothing," which is what happens by
default if the failure branch is left unhandled or silently ignored.

## Option 1: Return a Clear, Honest Error

```js
app.post("/profile/analyze", requireAuth, async (req, res) => {
  const raw = await callLlmForAnalysis(req.user.profile);
  const result = verifyAiResponse(ProfileAnalysisSchema, raw, { context: "profile-analysis" });

  if (!result.ok) {
    return res.status(502).json({
      error: "Analysis service returned an unexpected response. Please try again.",
    });
  }

  res.status(201).json(result.data);
});
```

A `502 Bad Gateway` honestly reflects what happened — an upstream service (the model provider)
returned something the application couldn't use — rather than disguising it as a `500` that implies
a bug in the application's own code. This is often the simplest, most honest option, and it should
usually be the default when a retry (per the next file) isn't worth attempting.

## Option 2: Fall Back to a Safe Default

```js
function getSentimentWithFallback(raw) {
  const result = SentimentSchema.safeParse(raw);
  return result.success ? result.data.sentiment : "neutral"; // safe, sensible default
}
```

For lower-stakes data — a sentiment label used only for a UI badge, not a decision with real
consequences — silently substituting a safe, sensible default can be the right call. This is
appropriate specifically when the data is genuinely low-stakes; falling back silently on something
like a payment amount or an access-control decision would hide a real, consequential problem.

## Option 3: Escalate for Human Review

```js
async function handleValidationFailure(rawResponse, schema, context) {
  await FailedAiResponse.create({
    context,
    rawResponse: JSON.stringify(rawResponse),
    timestamp: new Date(),
  });
  // a scheduled job or dashboard surfaces these for a human to review later
}
```

For content that's expensive to regenerate or unusually high-stakes, persisting the failure for
later human review — rather than either erroring immediately or guessing at a fallback — keeps a
record instead of losing the failure entirely, and gives a real person the chance to look at what
actually went wrong.

## Choosing Between the Three

```
Return an error   → default choice; most requests, most stakes
Fall back safely  → low-stakes data where a sensible default beats
                     no data at all
Escalate to human → high-stakes, expensive-to-regenerate content
                     where losing the failure would be a real problem
```

These aren't mutually exclusive — a real system might return an error to the client immediately
*while also* logging the failure for later review. The one option to avoid entirely is doing
nothing: neither erroring, falling back, nor logging, which loses the failure without a trace.

## Never Silently Coerce Invalid Data Into "Good Enough"

```js
// NEVER do this
const score = typeof raw.score === "number" ? raw.score : 0; // guessing, not validating
```

Manually coercing or guessing at a value the schema rejected defeats the entire purpose of
validating in the first place — it lets invalid data through anyway, just with an extra step that
looks like safety without actually providing it.

## Common Mistakes

- Leaving the failure branch of a validation check empty or unhandled, silently losing the failure.
- Falling back to a default value for data where the fallback itself could cause real harm (a
  financial figure, an access decision) rather than genuinely low-stakes display data.
- Returning a generic `500` for every validation failure, hiding the fact that the actual root
  cause was an unreliable upstream AI response rather than a bug in the application's own logic.

## ➡️ Next

Continue to
[implementing-retry-strategies-for-broken-outputs.md](implementing-retry-strategies-for-broken-outputs.md)
to see when — and how — retrying the generation itself is the better option.
