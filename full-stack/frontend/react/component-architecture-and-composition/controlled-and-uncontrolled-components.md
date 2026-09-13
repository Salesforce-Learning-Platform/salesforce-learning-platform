# Controlled and Uncontrolled Components

## The Core Question: Who Owns the Value?

For a form input, the actual displayed value has to live *somewhere* — either in the DOM element
itself (the browser's native behavior, from
[input-types-and-attributes.md](../../html/html-forms-and-user-input/input-types-and-attributes.md)),
or in React state, with React explicitly telling the DOM what to display on every render.

## Uncontrolled Components — The DOM Owns It

```jsx
function UncontrolledInput() {
  const inputRef = useRef(null);

  function handleSubmit() {
    console.log(inputRef.current.value); // read the DOM's current value only when needed
  }

  return <input ref={inputRef} defaultValue="Initial" />;
}
```

An **uncontrolled** input behaves like a plain HTML input — the browser manages keystrokes and the
current value internally; React only reads that value when it actually needs it (typically via a
`ref`, covered in the React Hooks module), rather than tracking every keystroke.

## Controlled Components — React State Owns It

```jsx
function ControlledInput() {
  const [value, setValue] = useState("");

  return (
    <input
      value={value}
      onChange={(e) => setValue(e.target.value)}
    />
  );
}
```

A **controlled** input's displayed value is fully driven by React state: `value` sets exactly
what's shown, and `onChange` updates that state on every keystroke, which then re-renders the
input with the new value — React state is the single source of truth for what's displayed,
matching the "UI as a function of state" model from
[what-is-react.md](../../react/introduction-to-react/what-is-react.md).

## Choosing Between Them

| | Uncontrolled | Controlled |
|---|---|---|
| Source of truth | The DOM itself | React state |
| Read the value | On demand (e.g., on submit), via a ref | Always available in state, on every render |
| Live validation/formatting as the user types | Harder — requires reading the DOM manually | Natural — the state update itself can validate/transform |
| Simpler for | A single, simple field read once, on submit | Anything needing to react to every keystroke |

Controlled components are the more common default in real applications, specifically because most
forms need *some* per-keystroke behavior (validation feedback, character counting, conditionally
enabling a submit button) — uncontrolled inputs remain a reasonable, simpler choice for a form
that's genuinely just read once at submission time.

## The Warning: Don't Switch Between the Two

```jsx
const [value, setValue] = useState(); // starts as undefined!
<input value={value} onChange={e => setValue(e.target.value)} />
// React warning: "component is changing an uncontrolled input to be controlled"
```

If `value` starts as `undefined`, React initially treats the input as uncontrolled (no `value`
prop meaningfully provided); the moment `setValue` provides an actual string, it becomes
controlled — React explicitly warns about this switch, since an input flip-flopping between the
two models mid-lifecycle produces unpredictable behavior. The fix: always initialize controlled
state to a defined value (`useState("")`, not `useState()`).

## Common Mistakes

- Initializing controlled state as `undefined` instead of an empty string, triggering React's
  controlled/uncontrolled warning the first time the user types.
- Using an uncontrolled input where live, per-keystroke validation or formatting was actually
  needed — this requires directly reading and manipulating the DOM, working against React's model
  rather than with it.
- Mixing both approaches on the same input (providing both `value` and `defaultValue`), which is
  contradictory and unsupported.

## Next

Continue to [reusable-component-design.md](reusable-component-design.md) for concrete patterns
that combine composition and prop design covered throughout this module.
