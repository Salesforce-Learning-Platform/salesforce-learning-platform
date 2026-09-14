# Custom Hooks

## The Problem: Sharing Stateful Logic Between Components

Two components might need identical *stateful behavior* — tracking whether a window is scrolled
past a threshold, subscribing to a value in `localStorage` — without necessarily needing identical
UI. Copy-pasting the same `useState`/`useEffect` logic into both components duplicates real logic,
exactly the kind of duplication [Functions](../../javascript/functions/) exists to let you avoid
for ordinary code.

## A Custom Hook Is Just a Function That Uses Other Hooks

```jsx
function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initialValue;
  });

  function updateValue(newValue) {
    setValue(newValue);
    localStorage.setItem(key, JSON.stringify(newValue));
  }

  return [value, updateValue];
}

// Used exactly like useState:
function Settings() {
  const [theme, setTheme] = useLocalStorage("theme", "light");
  return <button onClick={() => setTheme(theme === "light" ? "dark" : "light")}>{theme}</button>;
}
```

`useLocalStorage` is a **custom hook** — an ordinary JavaScript function that happens to call other
hooks (`useState`, here) internally, bundling stateful logic (reading/writing
[localStorage](../../javascript/using-browser-functionalities/local-storage.md), syncing it with
React state) into one reusable, named unit.

## The Naming Convention Is Not Optional

Custom hooks **must** start with `use` — this isn't just a style convention, it's what lets
`eslint-plugin-react-hooks` (from [rules-of-hooks.md](rules-of-hooks.md)) recognize the function as
a hook and correctly enforce the rules of hooks on it. A function that calls hooks internally but
isn't named `useSomething` won't be checked, silently allowing rule violations to slip through
undetected.

## Custom Hooks Don't Share State — They Share Logic

```jsx
function ComponentA() {
  const [theme, setTheme] = useLocalStorage("theme", "light"); // its OWN state
}
function ComponentB() {
  const [theme, setTheme] = useLocalStorage("theme", "light"); // a SEPARATE, independent instance
}
```

Calling the same custom hook from two different components creates two entirely independent state
instances — exactly like calling `useState` twice would (see
[understanding-state.md](../state-and-rerendering-logic/understanding-state.md)). A custom hook
shares the *logic* (the pattern of how state is managed), not the actual state value itself,
between components — for genuinely shared state, Context (covered in the Global State Management
module) is the correct tool.

## Common Mistakes

- Naming a hook-using helper function without the `use` prefix, silently losing
  `eslint-plugin-react-hooks`'s ability to check it for rule violations.
- Assuming two components using the same custom hook share the same underlying state — each call
  creates its own independent instance.
- Extracting a custom hook prematurely for logic used in only one place, adding an unnecessary
  layer of indirection before a genuine pattern of reuse has actually emerged — the same signal
  discussed for components in
  [component-reusability.md](../components-jsx-and-props/component-reusability.md).

## Module Summary

Across this module: hooks must be called unconditionally and only from components or other hooks,
because React tracks them by call order (see [rules-of-hooks.md](rules-of-hooks.md)); `useRef`
persists a value across renders without ever triggering one, making it the right tool for
non-rendering "bookkeeping" values and direct DOM access (see [useref.md](useref.md)); `useMemo`
and `useCallback` memoize a value and a function reference respectively, worth using specifically
for genuinely expensive computations or reference-stability needs like pairing with `memo` (see
[usememo.md](usememo.md) and [usecallback.md](usecallback.md)); and custom hooks let you extract
and share stateful *logic* — though never the state itself — between components, following the
mandatory `use` naming convention.
