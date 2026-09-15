# ✨ Improving UX in AI-Driven Applications

## Beyond Just Showing Text as It Arrives

A raw, working stream of text is the starting point, not the finished experience. Real AI products
add several deliberate UX layers on top of the mechanics from the previous two files — each solving
a specific, recognizable problem with a naive streaming implementation.

## Loading and Thinking Indicators

```
Request sent → [connection open, but no text_delta events yet] →
first text_delta arrives

This gap can be a full second or more, especially for a request
that also involves a tool call before any text is generated.
```

The moment between sending a request and the very first `text_delta` still needs *some* visual
feedback — a typing indicator, a subtle pulsing state — so the interface never looks frozen or
broken during that initial gap, however brief it usually is.

## Letting the User Stop Generation Mid-Stream

```js
const controller = new AbortController();

async function startStream(conversation) {
  return client.messages.stream(
    { model: "claude-opus-5", max_tokens: 1024, messages: conversation },
    { signal: controller.signal },
  );
}

function stopGeneration() {
  controller.abort(); // the user clicked "Stop"
}
```

A response the user no longer wants to wait for — because it's already clearly not what they
needed, or they want to rephrase — should be interruptible. Wiring a visible "Stop" control to an
`AbortController` (or the SDK's equivalent cancellation mechanism) gives the user real control over
a request that's still in progress, rather than forcing them to wait it out.

## Handling a Stream That Errors Mid-Way

```
event: error
data: {"type": "error", "error": {"type": "overloaded_error", "message": "..."}}
```

A stream can fail partway through — a genuine `error` event, a dropped connection — after some text
has already rendered. The interface needs a deliberate answer for this partial-failure case: does
it keep the partial text visible with an inline "generation interrupted" notice, or discard it and
show a clean retry prompt? Silently leaving a truncated, unexplained response on screen is the one
option to actively avoid.

## Disabling Input While a Response Streams

```jsx
<textarea disabled={isStreaming} placeholder={isStreaming ? "Waiting for response..." : "Ask anything..."} />
```

Allowing a new message to be sent while a previous response is still streaming invites a confusing,
out-of-order conversation. Disabling (or clearly queuing) new input until the current stream
finishes — or is explicitly stopped — keeps the conversation's turn-taking predictable for the
user.

## Showing Tool Calls as They Happen

```
"Looking up your order..." ← shown while a tool_use block is
                               being assembled, before its result
                               comes back
```

For a request that involves [a real tool call](../function-calling-tool-calling/), showing a
lightweight status message during the gap between the tool being invoked and its result coming back
(these gaps can be noticeably longer than pure text generation) keeps the interface transparent
about what's actually happening, rather than looking stalled.

## Common Mistakes

- Providing no feedback at all during the gap before the first token arrives, making the interface
  look broken rather than merely working.
- Building a chat input that silently allows a second message to be sent mid-stream, producing a
  confusing, overlapping conversation.
- Discarding a partially-streamed response entirely on error without at least acknowledging to the
  user that something was interrupted.

## ➡️ Next

Continue to
[separating-ui-responses-from-system-readable-outputs.md](separating-ui-responses-from-system-readable-outputs.md)
to see why the text shown to a user and the data a system needs to act on are often two genuinely
different things.
