# 🖥️ Progressive Rendering in User Interfaces

## From Raw Deltas to Updated Pixels

[streaming-tokens-from-the-model.md](streaming-tokens-from-the-model.md) covered *receiving* text
fragments. Progressive rendering is the other half: taking each fragment as it arrives and updating
what the user actually sees, continuously, rather than waiting to render anything until the whole
response is complete.

## A Minimal React Pattern

```jsx
function StreamingReply({ conversation }) {
  const [text, setText] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function run() {
      const stream = await startStream(conversation);
      for await (const event of stream) {
        if (cancelled) break;
        if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
          setText((prev) => prev + event.delta.text);
        }
      }
    }

    run();
    return () => { cancelled = true; };
  }, [conversation]);

  return <div className="reply">{text}</div>;
}
```

Each incoming `text_delta` triggers a state update, and React re-renders the growing string —
exactly the "typing" effect familiar from most modern AI chat interfaces. The `cancelled` flag
matters here specifically: if the component unmounts (the user navigates away) before the stream
finishes, this stops further state updates on an unmounted component.

## Why This Genuinely Changes Perceived Performance

```
Time to first paint:
  Non-streaming → same as total generation time (e.g. 4 seconds)
  Streaming     → time to the FIRST fragment (often well under 1 second)
```

This is the concrete, measurable benefit: the user perceives the application as responsive almost
immediately, even though the *total* time until the very last word is roughly the same either way.
This directly parallels
[Core Web Vitals](../../frontend/performance/frontend-performance-fundamentals/core-web-vitals.md)'s
distinction between total load time and perceived responsiveness — streaming is the AI-specific
version of optimizing for the metric users actually feel.

## Auto-Scrolling as Content Grows

```js
useEffect(() => {
  containerRef.current?.scrollTo({ top: containerRef.current.scrollHeight });
}, [text]);
```

A growing block of streamed text that overflows its container needs to keep the newest content
visible — but only while the user hasn't manually scrolled up to read something earlier. A common,
correct pattern is auto-scrolling only when the user is already at (or near) the bottom, so it
never yanks the view away from something they deliberately scrolled up to reread.

## Rendering Markdown Incrementally

```
Partial markdown mid-stream: "Here's a **bold cl"
                                          └─ an unclosed ** —
                                             naive markdown parsing
                                             can render this oddly
```

Streamed text is, by definition, incomplete at every point until the very last fragment — a
markdown parser applied to a partial string can occasionally misrender an unclosed formatting
marker. A common, practical mitigation is rendering the raw accumulated text plainly during
streaming, then re-parsing the complete text as proper markdown once the stream finishes (`message_
stop`).

## Common Mistakes

- Re-rendering the entire message list on every single delta instead of only the one message
  that's actively streaming, causing unnecessary work on every fragment.
- Auto-scrolling unconditionally, yanking the view away from content the user had deliberately
  scrolled up to reread.
- Applying a strict markdown/HTML parser to partial, mid-stream text and letting an unclosed tag or
  marker visually break the rendered output.

## ➡️ Next

Continue to
[improving-ux-in-ai-driven-applications.md](improving-ux-in-ai-driven-applications.md) for the
broader set of UX patterns a genuinely well-built streaming interface needs beyond the raw text
itself.
