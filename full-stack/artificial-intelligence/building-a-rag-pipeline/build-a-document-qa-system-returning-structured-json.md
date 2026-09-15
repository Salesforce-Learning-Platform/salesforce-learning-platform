# 📋 Build a Document Q&A System Returning Structured JSON

## The Complete Capstone

This file combines nearly every technique covered in this domain so far into one realistic,
production-shaped feature: a document Q&A system that retrieves relevant context (per
[the-rag-workflow.md](the-rag-workflow.md)) and returns a **structured, validated** answer — not
just plain text — including a confidence level and the specific sources used.

## Step 1: The Target Schema

```js
import { z } from "zod";

const QaResponseSchema = z.object({
  answer: z.string().min(1),
  confidence: z.enum(["high", "medium", "low"]),
  sources: z.array(z.object({
    documentId: z.string(),
    excerpt: z.string(),
  })).min(0), // can be empty if the answer wasn't found in the context
  answerFoundInContext: z.boolean(),
});
```

This schema — built with the patterns from
[Defining a Validation Schema Using Zod](../schema-validation-with-zod/defining-a-validation-schema-using-zod.md)
— captures exactly what a real document Q&A feature needs: the answer itself, a confidence signal
a UI can display, which specific sources backed the answer (for a "cited from" link), and an
explicit flag for whether the context actually contained the answer at all.

## Step 2: Retrieval (Stages 1–2 of the RAG Workflow)

```python
query_embedding = vo.embed([question], model="voyage-4", input_type="query").embeddings[0]
results = index.query(vector=query_embedding, top_k=5, include_metadata=True)
```

Exactly as covered in [the-rag-workflow.md](the-rag-workflow.md) and
[Integrating Vector Databases](../integrating-vector-databases/) — retrieve the most relevant
chunks, using a slightly larger `top_k` here since the model will need enough candidate context to
both answer accurately *and* cite specific sources correctly.

## Step 3: Generation With Native JSON Mode

```python
context_blocks = "\n\n".join(
    f"[Document: {m['id']}]\n{m['metadata']['text']}" for m in results["matches"]
)

response = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": f"""Answer the question using ONLY the context below. Cite the
specific document(s) your answer came from. If the context doesn't
contain the answer, set answerFoundInContext to false.

Context:
{context_blocks}

Question: {question}""",
    }],
    output_config={
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "answer": {"type": "string"},
                    "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                    "sources": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "documentId": {"type": "string"},
                                "excerpt": {"type": "string"},
                            },
                            "required": ["documentId", "excerpt"],
                            "additionalProperties": False,
                        },
                    },
                    "answerFoundInContext": {"type": "boolean"},
                },
                "required": ["answer", "confidence", "sources", "answerFoundInContext"],
                "additionalProperties": False,
            },
        }
    },
)
```

This applies
[using-model-supported-json-mode-for-structured-outputs.md](../generating-json-responses-from-llms/using-model-supported-json-mode-for-structured-outputs.md)
directly — guaranteeing the response's shape, so `sources` is always a real array and `confidence`
is always one of the three declared values, never an unexpected shape the frontend has to guard
against.

## Step 4: Validate Before Trusting It

```js
const parsed = QaResponseSchema.safeParse(JSON.parse(response.content[0].text));

if (!parsed.success) {
  logAiInteraction({ context: "document-qa", success: false, failureReason: "schema_mismatch" });
  return { ok: false };
}

return { ok: true, data: parsed.data };
```

Exactly per [Schema Validation with Zod](../schema-validation-with-zod/) and
[Error Handling in AI Applications](../error-handling-in-ai-applications/) — even a schema-
constrained response still gets validated before the application trusts it, and a failure is
logged with the same structured discipline as any other AI interaction in the application.

## Step 5: The Complete Endpoint

```js
app.post("/qa", requireAuth, async (req, res) => {
  const { question } = req.body;

  const result = await documentQa(question); // Steps 2-4, wrapped together

  if (!result.ok) {
    return res.status(502).json({ error: "Unable to generate an answer right now." });
  }

  if (!result.data.answerFoundInContext) {
    return res.status(200).json({ ...result.data, notice: "Answer not found in available documents." });
  }

  res.status(200).json(result.data);
});
```

This is the full, realistic shape of a production RAG feature — retrieval, schema-constrained
generation, validation, and a deliberate response for the "not found in context" case, all wired
together into one ordinary REST endpoint (per
[REST API Design](../../backend/rest-api-design/)).

## Common Mistakes

- Returning a plain-text answer with citations embedded in prose instead of a structured `sources`
  array, making the citations unusable for a real UI feature like a "view source" link.
- Treating `answerFoundInContext: false` as an error condition rather than a valid, expected
  response the application should handle gracefully and communicate honestly to the user.
- Skipping Zod validation on the schema-constrained response because native JSON mode "already
  guarantees" correctness — the shape guarantee doesn't cover every business rule, exactly as
  [verifying-ai-responses-against-a-schema.md](../schema-validation-with-zod/verifying-ai-responses-against-a-schema.md)
  established.

## Module Summary

Across this module: **the RAG workflow** — query, retrieve, inject, answer — grounds a model's
response in an application's own real, current data by combining embeddings and vector search with
generation, with an explicit "use only this context" instruction being the key to genuine grounding
(see [the-rag-workflow.md](the-rag-workflow.md)); and **a complete document Q&A system** combines
this domain's full toolkit — retrieval, native JSON mode, Zod validation, and structured error
handling — into one production-shaped feature that returns not just an answer, but a confidence
level, cited sources, and an honest signal for when the answer genuinely wasn't found.
