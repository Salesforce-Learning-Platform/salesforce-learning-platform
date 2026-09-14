# Rules of Hooks

## The Two Rules

**1. Only call hooks at the top level.** Never inside conditions, loops, or nested functions.

```jsx
// WRONG
function Component({ shouldTrack }) {
  if (shouldTrack) {
    const [count, setCount] = useState(0); // conditional hook call
  }
}

// CORRECT
function Component({ shouldTrack }) {
  const [count, setCount] = useState(0); // always called, unconditionally
  if (shouldTrack) {
    // use `count` conditionally instead — the hook call itself stays unconditional
  }
}
```

**2. Only call hooks from React function components or custom hooks.** Never from a regular
JavaScript function or a class component.

## Why These Rules Actually Exist

This isn't an arbitrary style preference — it follows directly from *how* React implements hooks
internally. React tracks each component's hooks by the **order they're called in** during a
render, not by name or any other identifier:

```jsx
function Component() {
  const [a, setA] = useState(1);  // React internally: "hook #1"
  const [b, setB] = useState(2);   // React internally: "hook #2"
  useEffect(() => {...});            // React internally: "hook #3"
}
```

On every re-render, React expects to see hooks called in this exact same order, matching each call
to its previously stored state by position. If a hook is called conditionally, the order can shift
between renders — imagine `shouldTrack` being `true` on one render (making the conditional
`useState` "hook #1") and `false` on the next (skipping it entirely, so the *next* hook becomes
"hook #1" instead) — React would then incorrectly match a completely different hook's stored state
to the wrong call, corrupting component state in a way that's genuinely confusing to debug.

## Enforcing the Rules Automatically

```bash
npm install --save-dev eslint-plugin-react-hooks
```

The `eslint-plugin-react-hooks` package (referenced directly in React's own documentation)
statically analyzes code and flags rule violations before they ever run — since a violation's
actual symptom (subtly wrong state) can appear only intermittently and be genuinely hard to
diagnose after the fact, catching it at lint time is far more reliable than debugging it once it
manifests.

## Common Mistakes

- Calling a hook inside an `if`, a loop, or after an early `return` — all of these can change how
  many times, or in what order, hooks are called between renders.
- Calling a hook from a plain helper function called by a component, rather than from the
  component (or a properly-named custom hook, covered in
  [custom-hooks.md](custom-hooks.md)) directly.
- Not installing `eslint-plugin-react-hooks`, missing automatic detection of violations that can
  otherwise go unnoticed until they cause a confusing bug.

## Next

Continue to [useref.md](useref.md) for a hook whose defining feature is that it does *not*
trigger a re-render.
