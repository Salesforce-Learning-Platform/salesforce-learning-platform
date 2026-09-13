# What Is React?

## A Library for Building UI from Components

React is a JavaScript library (not a full framework — it handles UI rendering specifically, with
routing, data fetching, and other concerns typically added via other libraries or a framework like
Next.js) for building user interfaces as a tree of **components**: independent, reusable pieces of
UI, each responsible for its own piece of the interface.

```jsx
function Greeting({ name }) {
  return <h1>Hello, {name}</h1>;
}
```

This is a component — a JavaScript function that returns a description of UI, written in **JSX**
(covered in its own dedicated file in the next module), which looks like HTML embedded directly in
JavaScript.

## The Core Mental Model: UI as a Function of State

The single most important idea in React, everything else in this domain builds on: **the UI you
see is a direct function of the current state**. Rather than writing imperative
instructions ("find this element, change its text, add this class" — the
[dom-manipulation](../../javascript/dom-manipulation/) approach), you describe what the UI
*should look like* for any given state, and React takes responsibility for figuring out how to
update the actual DOM to match whenever that state changes.

```text
        state                    UI
   ┌───────────┐           ┌──────────────┐
   │ count: 0   │  ─────▶  │ "Count: 0"    │
   └───────────┘           └──────────────┘
         │ state changes
         ▼
   ┌───────────┐           ┌──────────────┐
   │ count: 1   │  ─────▶  │ "Count: 1"    │
   └───────────┘           └──────────────┘
```

You never write code that says "change the text from 0 to 1" — you write a component that says
"render the current count," and React handles updating the DOM whenever that count actually
changes. This is the **declarative** approach (describing the desired result) as opposed to the
**imperative** approach (describing the exact steps to get there).

## Components Compose

```jsx
function App() {
  return (
    <div>
      <Greeting name="Ada" />
      <Greeting name="Grace" />
    </div>
  );
}
```

Components can be nested inside other components, each managing its own piece of logic and UI —
an entire application is, structurally, one large tree of components, mirroring the DOM tree
concept from [dom-introduction.md](../../javascript/dom-manipulation/dom-introduction.md), but
composed from reusable, application-defined building blocks rather than raw HTML elements alone.

## Common Mistakes

- Assuming React directly manipulates elements the way
  [dom-manipulation](../../javascript/dom-manipulation/) covers — React abstracts that away
  almost entirely; you describe *what* the UI should look like, and directly manipulating the DOM
  yourself alongside React is actively discouraged, since it can conflict with React's own updates.
- Treating React as a complete framework that includes routing and data fetching out of the box —
  it's specifically a UI-rendering library; those other concerns are handled by additional
  libraries, or by a framework like Next.js built on top of React.
- Thinking in terms of "steps to update the page" rather than "what should this component render
  given its current state" — the mental shift to declarative thinking is the actual learning curve
  in React, more than any specific syntax.

## Next

Continue to [why-react.md](why-react.md) for the concrete problems this model solves.
