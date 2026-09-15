# 🔀 Separating UI Responses from System-Readable Outputs

## Two Different Audiences for One AI Response

An AI feature often needs to serve two genuinely different consumers from a single generation: a
**human**, reading a natural-language reply, and **the application itself**, which may need a
piece of structured data extracted from that same interaction — a category, a decision, a value to
store. Conflating these two needs into one plain-text stream causes real problems.

## The Naive Approach — and Why It Breaks Down

```
"Sure! Based on your answers, I'd rate your compatibility as an
 82/100. Here's why: ..."
```

If an application needs the `82` programmatically — say, to store it, or to trigger some logic
above a certain threshold — parsing it back out of a friendly, conversational sentence is fragile:
a slightly different phrasing, and the number becomes hard to reliably extract at all.

## Two Genuinely Better Patterns

**Pattern 1 — a trailing structured block, clearly delimited:**

```
Sure! Based on your answers, I'd rate your compatibility as pretty
strong — you both value communication and shared humor highly.

<!--RESULT:{"score": 82, "matchingFactors": ["communication", "humor"]}-->
```

The human-readable text streams normally; a clearly delimited structured block (an HTML comment, a
unique marker) follows it, extracted separately once the stream completes and parsed with
[the validation discipline from Schema Validation with Zod](../schema-validation-with-zod/) before
being used.

**Pattern 2 — two separate requests entirely:**

```
Request 1 (streamed to the user): "Explain your compatibility
  analysis in a friendly way."

Request 2 (not streamed, native JSON mode): generate ONLY the
  {score, matchingFactors} structured data
```

For cases where the two outputs genuinely don't need to be generated together, making two separate
requests — one purely for the human-facing text (streamed), one purely for the structured data
(using [native JSON mode](../generating-json-responses-from-llms/using-model-supported-json-mode-for-structured-outputs.md),
not streamed) — is simpler and more reliable than trying to interleave both into a single response.

## Why Streaming and Strict JSON Mode Don't Mix Well

```
Streaming's whole POINT: show partial, incomplete content as it
arrives

Strict JSON's whole POINT: the response is only valid once it's
COMPLETE and well-formed

→ a "streamed JSON object" is, by definition, invalid JSON at
  every point except the very last chunk
```

This is the core tension this file exists to resolve: streaming is fundamentally about showing
*incomplete* content progressively, while structured, schema-validated data is only meaningful once
it's *complete*. The two patterns above sidestep this tension rather than trying to stream
partially-valid JSON and parse it incrementally, which is both harder to implement correctly and
fragile in practice.

## Common Mistakes

- Streaming a single JSON object directly to the UI and trying to parse it incrementally — partial
  JSON is invalid JSON, and this approach breaks in exactly the cases it needs to be reliable.
- Parsing a human-facing sentence with a regex to extract a number or category the application
  actually needs, instead of requesting that data in a clearly separated, structured form.
- Forgetting to apply the same validation discipline from
  [Schema Validation with Zod](../schema-validation-with-zod/) to a structured block just because it
  arrived alongside a streamed response instead of a direct JSON-mode request.

## ➡️ Next

Continue to
[combining-streaming-with-structured-data.md](combining-streaming-with-structured-data.md) to put
both patterns from this file into a complete, working example.
