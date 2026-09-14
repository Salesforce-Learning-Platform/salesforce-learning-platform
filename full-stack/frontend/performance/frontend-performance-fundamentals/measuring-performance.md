# Measuring Performance

## Why Measure Before Optimizing

Every technique in [asset-loading-strategy.md](asset-loading-strategy.md) is only worth applying
where it actually matters. Guessing which resource is slow wastes effort and can even make things
worse (e.g., over-using `preload`, per that file's Common Mistakes). Measuring first turns
performance work from guesswork into evidence.

## Lighthouse — A Lab Report

Lighthouse (built into Chrome DevTools, under the "Lighthouse" panel) runs a single, controlled
page load and produces a report scoring Performance, Accessibility, Best Practices, and SEO,
including a full breakdown of Core Web Vitals for that one run plus specific, actionable
suggestions (e.g., "Serve images in next-gen formats," "Eliminate render-blocking resources").

This is **lab data** — one simulated run, under controlled network/CPU conditions — which makes it
excellent for quickly finding concrete issues to fix, but it's not the same as real users' actual
experience, which varies by device, network, and location. Treat a Lighthouse score as a diagnostic
starting point, not the final word on real-world performance (that's what the 75th-percentile
field-data threshold described in [core-web-vitals.md](core-web-vitals.md) is for).

## The DevTools Performance Panel — Diagnosing Runtime Behavior

The Performance panel records what the page actually does while running — not just loading, but
also scrolling, clicking, and any JavaScript executing in response. After clicking Record and
interacting with the page:

- The **FPS chart** shows frame rate over time; red bars mark frames that dropped below a smooth
  60 FPS.
- The **flame chart** shows exactly which function calls ran, when, and for how long, on the main
  thread — the tool for finding *which specific piece of code* caused a slow interaction.
- Clicking into a long task in the flame chart traces directly back to the source file and line
  number responsible.

This is the right tool specifically for diagnosing a poor INP score: recording a real interaction
(a click, a form submission) and finding exactly which function occupied the main thread long
enough to delay the next paint.

## A Practical Workflow

1. Run Lighthouse for a quick, broad diagnostic pass and a Core Web Vitals snapshot.
2. For a specific slow interaction (a laggy click, a janky scroll), record it with the Performance
   panel and read the flame chart to find the exact blocking function.
3. Fix the specific issue found — an unoptimized image, a missing `loading="lazy"`, an
   expensive synchronous function — using the techniques from
   [asset-loading-strategy.md](asset-loading-strategy.md).
4. Re-measure to confirm the fix actually moved the number, rather than assuming it did.

## Common Mistakes

- Treating a single Lighthouse run as definitive, rather than one lab sample — running it multiple
  times, and ideally validating against real field data, gives a much more trustworthy picture.
- Using the Performance panel to look at page *load*, when it's built for observing runtime
  interaction behavior — Lighthouse (or the Network panel) is the better tool for load-time
  analysis.
- Applying a fix without re-measuring afterward — an optimization that seems obviously correct can
  fail to move the actual number, or even regress a different metric.

## Module Summary

Across this module: the three **Core Web Vitals** — LCP (loading), INP (interactivity), and CLS
(visual stability) — give a framework-agnostic, standardized vocabulary for "is this page fast,"
each with defined good/poor thresholds measured against real users at the 75th percentile (see
[core-web-vitals.md](core-web-vitals.md)); concrete **asset loading strategies** —
`loading="lazy"`, `async`/`defer` for scripts, and `preload`/`prefetch` — directly target those
metrics by controlling exactly when and how the browser fetches and executes resources (see
[asset-loading-strategy.md](asset-loading-strategy.md)); and Lighthouse plus the DevTools
Performance panel are the concrete tools for measuring, diagnosing, and verifying performance
work, so that every optimization is evidence-driven rather than guessed.
