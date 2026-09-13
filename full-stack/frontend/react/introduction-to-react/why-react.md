# Why React?

## The Problem with Manual DOM Updates at Scale

A small, static interaction is straightforward with plain
[dom-manipulation](../../javascript/dom-manipulation/) and
[events](../../javascript/events/): select an element, update it, done. The difficulty grows
sharply once an interface has many interdependent pieces of state — a shopping cart that affects a
total, a header count, and an availability message simultaneously. Manually tracking every place
in the DOM that needs to update whenever any piece of state changes becomes genuinely hard to get
right and keep consistent as an application grows, and small inconsistencies (one place updated,
another forgotten) become a real, recurring source of bugs.

## What React Actually Does About It

React's declarative model (from [what-is-react.md](what-is-react.md)) removes the need to manually
track *which* DOM elements need updating when state changes. You update the state; React
re-runs the relevant components to determine what the UI should now look like, then efficiently
updates only the parts of the actual DOM that changed — a process covered in
[how-rerendering-works.md](../state-and-rerendering-logic/how-rerendering-works.md) in the next
module.

## Component Reusability

```jsx
function Button({ label, onClick }) {
  return <button onClick={onClick}>{label}</button>;
}
```

A component defined once can be reused throughout an application with different data (via props,
covered in the next module) — consistent behavior and appearance without duplicating markup and
event-wiring logic every time a similar UI element is needed.

## A Large, Mature Ecosystem

React's popularity means an extensive ecosystem of libraries for routing, state management, data
fetching, and UI components — several of which are covered in dedicated modules later in this
domain (React Router, Redux, React Query) — reducing how much needs to be built from scratch for
common application needs.

## Being Honest About Tradeoffs

React isn't the only reasonable choice, and it's worth naming its real costs rather than
presenting it as a universal default:

- It adds real complexity (a build step, a component mental model, a learning curve) that a
  genuinely simple, mostly-static page doesn't need — plain HTML/CSS/JavaScript remains the right
  tool for that case.
- Other frameworks (Vue, covered later in this platform, and others) solve overlapping problems
  with different tradeoffs, and are reasonable choices depending on team and project context.
- React's declarative model has to be learned deliberately — it's a genuine shift in thinking, not
  simply "the same DOM manipulation with nicer syntax."

## Common Mistakes

- Reaching for React by default for every project regardless of actual complexity, adding
  unnecessary overhead to a page that a few lines of vanilla JavaScript would handle just as well.
- Treating React as strictly superior to every alternative rather than a tool with genuine,
  specific tradeoffs suited to interfaces with meaningfully complex, interdependent state.
- Learning React's syntax without genuinely internalizing the declarative mental model from
  [what-is-react.md](what-is-react.md) — this produces code that technically works but fights the
  framework's actual design.

## Next

Continue to [setting-up-a-react-project.md](setting-up-a-react-project.md) to create your first
project.
