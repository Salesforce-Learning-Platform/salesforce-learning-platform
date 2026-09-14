# The React Profiler

## Measure Before You Optimize

This is the single most important idea in this module, and arguably in this entire domain:
**every optimization technique covered so far (`memo`, `useMemo`, `useCallback`, code splitting)
has a real cost, and is only worth applying to a genuine, measured problem.** Applying them
reflexively — as flagged repeatedly across
[usememo.md](../react-hooks/usememo.md),
[usecallback.md](../react-hooks/usecallback.md), and
[memoization.md](memoization.md) — adds complexity and overhead for often negligible or
nonexistent benefit. The React Profiler, part of React Developer Tools (a browser extension), is
how you find out whether a specific component is actually a problem before reaching for any of
these techniques.

## Using the Profiler Tab

1. Install the React Developer Tools browser extension.
2. Open your browser's DevTools (see
   [browser-devtools-essentials.md](../../foundations/preparing-your-machine/browser-devtools-essentials.md))
   and select the "Profiler" tab it adds.
3. Click "Record," interact with your app (click the button that's suspected to cause slow
   re-renders), then stop recording.
4. Review the resulting flame graph — it shows exactly which components rendered, how long each
   took, and *why* each one rendered (props changed, state changed, a parent re-rendered, etc.).

## What to Actually Look For

- **Components that took a genuinely long time to render** — these are candidates for `memo`,
  `useMemo`, or code splitting, in that order of likely relevance.
- **Components that rendered for no apparent reason** — often a parent re-rendering unnecessarily,
  or an unmemoized function/object prop defeating a `memo` wrapper that was already applied (see
  [memoization.md](memoization.md)'s reference-equality gotcha).
- **Whether a "slow" interaction is actually a rendering problem at all** — a slow network request
  (covered in [server-state-and-api-integration](../server-state-and-api-integration/)) can *look*
  like a rendering performance problem from the user's perspective, but no amount of `memo` fixes a
  genuinely slow API call.

## The Programmatic `<Profiler>` Component

```jsx
import { Profiler } from "react";

function onRenderCallback(id, phase, actualDuration) {
  console.log(`${id} (${phase}) took ${actualDuration}ms`);
}

<Profiler id="AnalyticsChart" onRender={onRenderCallback}>
  <AnalyticsChart data={chartData} />
</Profiler>
```

For programmatic, ongoing measurement (rather than a manual DevTools recording session), React
also exposes a `<Profiler>` component that reports timing data via a callback — useful for
tracking a specific, known-important component's render performance over time, including in
production monitoring.

## A Practical Workflow

1. Notice (or hear a genuine user report of) a slow interaction.
2. Profile it — don't guess which component is actually slow.
3. Identify the specific, measured cause (an expensive re-render, an unnecessary one, a slow
   network request, a large bundle).
4. Apply the *specific* technique that addresses that measured cause — `memo`/`useMemo` for
   expensive re-renders, `useCallback` to fix a defeated `memo`, code splitting for bundle size,
   or looking at the network/server side for a slow request.
5. Profile again to confirm the change actually helped.

## Common Mistakes

- Applying `memo`/`useMemo`/`useCallback` speculatively across a codebase without ever profiling,
  based on a guess about what "might" be slow.
- Assuming every slow-feeling interaction is a React rendering problem, when it might be a slow
  network request or a genuinely expensive synchronous JavaScript computation unrelated to
  rendering at all.
- Optimizing once and never re-profiling to confirm the change actually had the intended effect —
  a "fix" that doesn't move the measured number wasn't actually a fix.

## Module Summary

Across this module: `memo` skips a component's re-render when its props are shallowly unchanged,
but is easily defeated by unmemoized function/object props (see [memoization.md](memoization.md));
`lazy`/`Suspense` split an application's JavaScript into separate, on-demand chunks (see
[code-splitting.md](code-splitting.md)); route-based code splitting and lazy-loading heavy
conditional UI are the highest-value places to apply it in practice (see
[lazy-loading.md](lazy-loading.md)); and every technique in this module should be applied only in
response to a genuinely measured problem, found using the React Profiler — never speculatively.
