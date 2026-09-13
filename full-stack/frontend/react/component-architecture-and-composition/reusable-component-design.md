# Reusable Component Design

## Designing the Prop Interface First

Before writing a component's implementation, it's worth deliberately designing its **prop
interface** — exactly what it accepts and what each prop means — the same discipline as designing
a function's signature (see [Functions](../../javascript/functions/)) before writing its body.
A well-designed interface is what actually determines whether a component is pleasant or painful
to reuse later.

## Pattern: Sensible Defaults, Minimal Required Props

```jsx
interface ButtonProps {
  label: string;                       // required — no reasonable default
  variant?: "primary" | "secondary";     // optional, sensible default
  onClick?: () => void;                    // optional — a button can exist without one
}

function Button({ label, variant = "primary", onClick }: ButtonProps) {
  return <button className={variant} onClick={onClick}>{label}</button>;
}
```

Requiring only what a component genuinely cannot function without, and providing sensible
defaults (see
[parameters-and-return-values.md](../../javascript/functions/parameters-and-return-values.md))
for everything else, keeps the common case simple (`<Button label="Save" />`) while still allowing
full customization when actually needed.

## Pattern: Composition for Genuinely Unpredictable Content

As established in [component-composition.md](component-composition.md), reach for `children` (or
named JSX-element props) rather than adding more configuration props once a component's content
becomes genuinely variable — a `Card` shouldn't need a `hasIcon`/`iconType`/`iconSize` trio of
props if it could simply accept an icon as a child instead.

## Pattern: Let the Consumer Own Behavior, Not Just Data

```jsx
// Less flexible — SearchBox owns the entire search behavior
function SearchBox({ onSearch }) {
  const [query, setQuery] = useState("");
  return <input value={query} onChange={e => { setQuery(e.target.value); onSearch(e.target.value); }} />;
}

// More flexible — the consumer decides what actually happens on change
function SearchBox({ value, onChange }) {
  return <input value={value} onChange={e => onChange(e.target.value)} />;
}
```

The second version is a **controlled component** (see
[controlled-and-uncontrolled-components.md](controlled-and-uncontrolled-components.md)) from the
consuming side — `SearchBox` itself has no opinion about what happens when the value changes
(debouncing, triggering a search immediately, validating), leaving that entirely to whoever uses
it. This tends to produce more genuinely reusable components than baking in one specific behavior.

## Naming Conventions Matter for Reusability

Consistent, predictable prop names across a codebase (`onClick` not `handleClick` or `click`,
`children` not `content`, `className` not `class`) reduce the cognitive cost of learning each new
component — a reader who already knows React's own conventions can guess correctly at an
unfamiliar component's interface, rather than needing to check its source every time.

## Common Mistakes

- Designing a component's props reactively, adding a new prop every time a new use case appears,
  rather than anticipating a small number of genuinely reusable dimensions upfront.
- Baking specific behavior (a particular validation rule, a specific side effect) into a component
  that would be more broadly useful if that decision were left to the consumer.
- Diverging from established naming conventions (`onClick`, `children`, `className`) for no real
  reason, making a component's interface less predictable to someone already familiar with React.

## Module Summary

Across this module: prop drilling — passing data through components that don't use it — is a real
architectural problem composition solves by letting content flow through `children` instead (see
[component-composition.md](component-composition.md)); `children` is just a regular prop value,
renderable, conditional, and not restricted to a special data type (see
[children-prop.md](children-prop.md)); controlled components put React state in charge of an
input's value, while uncontrolled components leave it to the DOM — mixing the two on one input
triggers React's own warning (see
[controlled-and-uncontrolled-components.md](controlled-and-uncontrolled-components.md)); and
deliberately designing a component's prop interface — minimal required props, sensible defaults,
composition over configuration, and consistent naming — is what determines whether it's genuinely
pleasant to reuse.
