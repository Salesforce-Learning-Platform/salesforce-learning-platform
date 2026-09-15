# 📡 Streaming Tokens from the Model

## The Problem With Waiting

```
NON-STREAMING: send request → ...wait several seconds, nothing
happens on screen... → the ENTIRE response arrives at once

STREAMING: send request → the FIRST words appear almost immediately,
more arrive continuously as the model generates them
```

A response of any real length — a paragraph, an explanation, a generated document — can take
several seconds for a model to fully generate. Waiting in total silence for all of it feels slow
and unresponsive, even when the total generation time is identical. Streaming doesn't make the
model faster; it changes *when* the user sees the words that are already being produced.

## Enabling Streaming: `stream: true`

```python
with client.messages.stream(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain how photosynthesis works."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

The Python and TypeScript SDKs provide a dedicated streaming helper (`stream.text_stream` here)
that yields each new piece of text as it arrives — the simplest way to consume a stream without
handling the underlying event protocol directly.

## What's Actually Happening: Server-Sent Events

```
event: message_start
data: {"type": "message_start", "message": {"content": [], ...}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "Hello"}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "!"}}

event: content_block_stop
data: {"type": "content_block_stop", "index": 0}

event: message_delta
data: {"type": "message_delta", "delta": {"stop_reason": "end_turn"}, "usage": {"output_tokens": 15}}

event: message_stop
data: {"type": "message_stop"}
```

Under the hood, `stream: true` switches the response to Server-Sent Events (SSE): instead of one
big HTTP response body, the connection stays open and sends a sequence of small, named events as
the model generates. `message_start` opens the response, one or more `content_block_delta` events
each carry a `text_delta` fragment, `content_block_stop` closes that block, and `message_stop`
signals the whole response is complete.

## Assembling the Full Text

```js
let fullText = "";
for await (const event of stream) {
  if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
    fullText += event.delta.text;
  }
}
```

Each `text_delta` carries only a fragment — a full response is simply every fragment concatenated
in the order the events arrive. For a raw HTTP integration (not using an SDK's `text_stream`
helper), this accumulation is something the application code has to do itself.

## `ping` Events Are Normal, Not Errors

```
event: ping
data: {"type": "ping"}
```

A stream may include any number of `ping` events interspersed with the real content — these are
harmless keep-alive signals with no data of their own, and application code consuming a raw stream
should simply ignore any event type it doesn't specifically need to handle.

## Common Mistakes

- Assuming streaming makes the model generate faster overall — it changes *when* text appears, not
  the total generation time.
- Building a raw SSE integration that breaks on an unrecognized event type instead of gracefully
  ignoring events it doesn't need (like `ping`, or future event types).
- Forgetting that individual `text_delta` fragments are not guaranteed to align with word or
  sentence boundaries — a fragment can end mid-word.

## ➡️ Next

Continue to
[progressive-rendering-in-user-interfaces.md](progressive-rendering-in-user-interfaces.md) to see
how these incoming fragments actually get displayed to a user in real time.
