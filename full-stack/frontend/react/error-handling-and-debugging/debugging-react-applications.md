# Debugging React Applications

## React Developer Tools

Beyond the general browser DevTools from
[browser-devtools-essentials.md](../../foundations/preparing-your-machine/browser-devtools-essentials.md),
the React Developer Tools browser extension adds two React-specific panels:

- **Components**: shows the actual component tree (as opposed to the raw DOM tree), with each
  component's current props and state inspectable directly — letting you confirm exactly what
  data a component actually received and is currently holding, without adding a single
  `console.log`.
- **Profiler**: covered in depth in
  [react-profiler.md](../performance-optimization-in-react/react-profiler.md), for measuring
  render performance.

## Inspecting Props and State Directly

Selecting any component in the Components panel shows its current props and state values live —
this is frequently faster than the `console.log`-driven approach from
[debugging-techniques.md](../../javascript/error-handling-and-debugging/debugging-techniques.md),
since you can inspect a component's actual current values at any point, without predicting in
advance what to log.

## A Systematic Approach for a React-Specific Bug

1. **Reproduce it reliably.** The same discipline from
   [debugging-techniques.md](../../javascript/error-handling-and-debugging/debugging-techniques.md)
   applies here first.
2. **Check the Components panel**: is the component receiving the props you expect? Is its state
   what you expect at the point the bug occurs?
3. **Check the Network panel** if the bug involves data — is the actual API response what the
   component assumes? (Directly the
   [fetch-api.md](../../javascript/asynchronous-programming-and-modules/fetch-api.md) `response.ok`
   discipline — confirm the request even succeeded before assuming the component's logic is wrong.)
4. **Set a breakpoint** in the Sources panel at the exact point the bug manifests, and step through
   from there — the same breakpoint discipline from
   [debugging-techniques.md](../../javascript/error-handling-and-debugging/debugging-techniques.md),
   now informed by what the Components panel already told you about props/state.
5. **Check the console for React's own warnings** — many bugs (a missing `key`, a dependency array
   issue) are explicitly flagged by React itself before they cause a visible problem, per
   [common-react-errors.md](common-react-errors.md).

## A Concrete Example

A product's price displaying as `undefined` on a product page:

1. Reproduce it — confirm which specific product triggers it.
2. Components panel: select the `ProductPrice` component — is `price` actually present in its
   props? If not, the bug is upstream (the parent isn't passing it, or the API response is missing
   it).
3. Network panel: check the actual `/api/products/:id` response — does it genuinely include a
   `price` field for this product?
4. If the API response has the price but the component doesn't, the bug is in how the parent
   destructures or passes the prop — a breakpoint in that parent component narrows it down further.

This traces the exact path data travels (API → parent component → child prop) rather than
guessing, isolating which specific link in that chain is actually broken.

## Common Mistakes

- Debugging a data-related bug by reading component code alone, without checking the Network panel
  to confirm what the API actually returned.
- Not using the Components panel to directly inspect current props/state, instead adding temporary
  `console.log` statements for information already visible directly in React DevTools.
- Fixing the first plausible-looking cause found without confirming (via the panel or a breakpoint)
  that it's actually the *real* cause — a "fix" for the wrong cause often just moves the bug rather
  than resolving it.

## Module Summary

Across this module: several React error messages have specific, recognizable causes and fixes —
unmounted-component updates, too-many-re-renders, invalid children, missing keys, and exhaustive-deps
warnings (see [common-react-errors.md](common-react-errors.md)); error boundaries catch rendering
errors and show a fallback UI, but explicitly not errors in event handlers, async code, or
server-side rendering (see [react-error-boundaries.md](react-error-boundaries.md)); and React
Developer Tools' Components panel lets you inspect actual live props and state directly, forming
the basis of a systematic, evidence-based debugging workflow rather than guessing at a cause.

This completes the React domain. Continue to
[Getting Started with Next.js](../../nextjs/getting-started-with-nextjs/), or see the
[Frontend learning path](../../README.md) for the full sequence.
