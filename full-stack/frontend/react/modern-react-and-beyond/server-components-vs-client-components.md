# 🖥️ Server Components vs. Client Components

## A React-Level Concept, Not a Next.js-Only One

This is genuinely a **React** architectural model — React itself, not just Next.js, now
distinguishes between components that run on the server and components that run in the browser.
[Next.js's own rendering-strategies module](../../nextjs/rendering-strategies/server-components.md)
already covers this in full depth, specifically as Next.js implements and uses it; this file exists
only to frame it as the broader React 19 concept it actually is, without repeating that existing
coverage.

## The New Mental Model, in One Sentence

Every component in a React app using this model is, by default, a **Server Component** — rendered
once, on the server, with zero JavaScript shipped to the browser for it — unless explicitly marked
otherwise, at which point it becomes a **Client Component**, rendered (and re-rendered) in the
browser exactly like every component covered throughout the rest of the
[React domain](../../react/) up to this point.

## Why This Is a Genuine Shift, Not Just New Syntax

```jsx
// Every component covered before this module: ALWAYS a Client Component,
// running in the browser, capable of useState/useEffect/event handlers

// The new model: components are Server Components BY DEFAULT — no
// useState, no useEffect, no event handlers — unless marked "use client"
```

Everything taught from [Introduction to React](../introduction-to-react/) through
[React Hooks](../react-hooks/) describes what's now specifically called a **Client Component** —
which remains exactly as capable and correct as before. What's new is the *default* shifting: a
component doesn't automatically get that full client-side capability (state, effects, event
handlers) unless it explicitly opts in.

## Why This Matters, Conceptually

A Server Component never ships its own JavaScript to the browser at all — its output is just the
rendered result, sent as part of the page. This directly improves initial load performance (per
[frontend-performance-fundamentals](../../performance/frontend-performance-fundamentals/)'s
broader coverage of what actually makes a page feel fast) for any part of the UI that doesn't
genuinely need client-side interactivity — a static description, a server-rendered list of
data — without needing a completely separate framework or approach for that content.

## Common Mistakes

- Assuming this is a Next.js-specific feature rather than a React-level architectural shift that
  Next.js happens to be the most common framework implementing — the underlying concept belongs to
  React itself.
- Trying to use `useState` or an event handler inside a component that hasn't opted into being a
  Client Component — per
  [Next.js's own coverage](../../nextjs/rendering-strategies/client-components.md), this needs the
  explicit `"use client"` directive.
- Assuming every component needs to become a Client Component out of habit — many real components
  (a static footer, a server-rendered list) are genuinely better off staying Server Components,
  gaining the performance benefit for free.

## ➡️ Next

Continue to [actions-and-form-handling.md](actions-and-form-handling.md) to see React 19's other
major new pattern, built to work naturally alongside this Server/Client model.
