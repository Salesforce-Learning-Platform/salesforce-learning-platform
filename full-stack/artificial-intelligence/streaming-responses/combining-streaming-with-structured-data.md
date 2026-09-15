# 🧩 Combining Streaming with Structured Data

## A Third Case: Streaming a Tool Call Itself

[separating-ui-responses-from-system-readable-outputs.md](separating-ui-responses-from-system-readable-outputs.md)
covered keeping human-facing text and structured data apart. There's one more case worth knowing:
[tool calls](../function-calling-tool-calling/) themselves can be streamed too — not as text, but as
an `input_json_delta`, arriving in pieces.

```
event: content_block_start
data: {"type": "content_block_start", "index": 1, "content_block": {"type": "tool_use", "id": "toolu_01...", "name": "issue_refund", "input": {}}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "partial_json": "{\"order_id\": \"48213\", \"amount\": 5"}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "partial_json": "0, \"reason\": \"damaged\"}"}}

event: content_block_stop
data: {"type": "content_block_stop", "index": 1}
```

The `partial_json` fragments are, individually, **not valid JSON on their own** — they're pieces of
a JSON string that only becomes parseable once fully accumulated. This is exactly the tension from
the previous file, in miniature: never attempt to `JSON.parse()` a single fragment.

## Accumulating and Parsing Safely

```js
let partialInput = "";

for await (const event of stream) {
  if (event.type === "content_block_delta" && event.delta.type === "input_json_delta") {
    partialInput += event.delta.partial_json;
  }
  if (event.type === "content_block_stop") {
    const toolInput = JSON.parse(partialInput); // only parse once complete
    // now validate with Zod, per Schema Validation with Zod, before acting on it
  }
}
```

Only after `content_block_stop` — signaling the block is genuinely complete — is `partialInput`
guaranteed to be valid, parseable JSON. This same accumulate-then-parse pattern applies to `text_
delta` fragments too, whenever the accumulated text itself needs to be treated as structured data
rather than displayed directly.

## Why This Still Streams Usefully to the User

```
While the tool's arguments accumulate silently in the background,
the UI can already show:

"Looking up order details..." (a lightweight status message, per
 improving-ux-in-ai-driven-applications.md)

The user perceives continuous progress even though the actual
JSON data isn't usable until it's complete.
```

Even though the structured `input_json_delta` fragments themselves can't be shown or used
incrementally, the *surrounding* UX — a status indicator, any text the model generates alongside the
tool call — can still stream normally, keeping the interface responsive throughout.

## A Complete, Combined Example

```js
async function handleStreamingToolRequest(conversation) {
  let userFacingText = "";
  let toolCalls = {}; // index -> { name, id, partialInput }

  const stream = await client.messages.stream({
    model: "claude-opus-5", max_tokens: 1024, tools, messages: conversation,
  });

  for await (const event of stream) {
    if (event.type === "content_block_start" && event.content_block.type === "tool_use") {
      toolCalls[event.index] = { name: event.content_block.name, id: event.content_block.id, partialInput: "" };
    }
    if (event.type === "content_block_delta") {
      if (event.delta.type === "text_delta") userFacingText += event.delta.text; // → render to UI
      if (event.delta.type === "input_json_delta") toolCalls[event.index].partialInput += event.delta.partial_json;
    }
  }

  for (const call of Object.values(toolCalls)) {
    const args = ToolArgsSchema.safeParse(JSON.parse(call.partialInput)); // validate, per Schema Validation with Zod
    if (args.success) await executeTool(call.name, args.data);
  }
}
```

This combines every piece from this module: streamed text rendered progressively to the user,
streamed tool-call JSON accumulated safely and only parsed once complete, and Zod validation
applied before any real action is taken — the full, production-shaped pattern.

## Common Mistakes

- Attempting to `JSON.parse()` an individual `input_json_delta` fragment instead of accumulating
  every fragment first and parsing only after `content_block_stop`.
- Skipping schema validation on a streamed tool call's arguments just because they arrived via a
  different mechanism than a non-streamed response.
- Forgetting to track `index` correctly when a response contains multiple content blocks (text and
  one or more tool calls) streaming concurrently — deltas for different blocks are interleaved by
  their `index`, not delivered one block fully at a time.

## Module Summary

Across this module: **streaming** delivers a model's response incrementally via Server-Sent Events
(`message_start`, `content_block_delta`, `message_stop`, and others), changing when text appears
without changing total generation time (see
[streaming-tokens-from-the-model.md](streaming-tokens-from-the-model.md));
**progressive rendering** turns incoming fragments into a responsive, continuously updating UI,
with careful handling of auto-scroll and partial markdown (see
[progressive-rendering-in-user-interfaces.md](progressive-rendering-in-user-interfaces.md));
**a genuinely polished streaming UX** needs loading indicators, a way to stop generation early,
graceful mid-stream error handling, and input locking while a response is in flight (see
[improving-ux-in-ai-driven-applications.md](improving-ux-in-ai-driven-applications.md));
**human-facing text and system-readable structured data are best kept separate** — through a
delimited block or a second, dedicated request — rather than parsed back out of conversational
prose (see
[separating-ui-responses-from-system-readable-outputs.md](separating-ui-responses-from-system-readable-outputs.md));
and **streamed tool calls** arrive as `input_json_delta` fragments that must be fully accumulated
before parsing, then validated exactly like any other AI-generated structured data before a real
action is taken.
