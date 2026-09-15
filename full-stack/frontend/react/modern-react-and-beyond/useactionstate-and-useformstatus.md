# 🪝 useActionState and useFormStatus

## `useActionState` — Wrapping an Action With Its Result

```jsx
function ChangeName() {
  const [error, submitAction, isPending] = useActionState(
    async (previousState, formData) => {
      const err = await updateName(formData.get("name"));
      if (err) return err;
      redirect("/profile");
      return null;
    },
    null // initial state
  );

  return (
    <form action={submitAction}>
      <input type="text" name="name" />
      <button type="submit" disabled={isPending}>Update</button>
      {error && <p>{error}</p>}
    </form>
  );
}
```

`useActionState(actionFn, initialState)` wraps an [Action](actions-and-form-handling.md) and
returns three things: the **current state** (whatever the action function last returned — here, an
error message or `null`), a **wrapped action** to pass directly to `<form action={...}>`, and
`isPending`. This is a direct, meaningful reduction of
[actions-and-form-handling.md](actions-and-form-handling.md)'s already-simpler pattern: no separate
`useState` for the error, and no manual `useTransition` — `useActionState` manages both together.

## The `previousState` Argument

```jsx
async (previousState, formData) => {
  // previousState is whatever this same function returned last time
}
```

The action function passed to `useActionState` always receives the **previous state** as its first
argument (React automatically threads it through between submissions) — genuinely useful for a form
that needs to know something about its last submission attempt, like an incrementing retry count,
without needing separate state to track it.

## `useFormStatus` — Reading Form Status From a Child, Without Prop Drilling

```jsx
// A reusable submit button component, usable inside ANY form
import { useFormStatus } from "react-dom";

function SubmitButton({ children }) {
  const { pending } = useFormStatus();
  return <button type="submit" disabled={pending}>{children}</button>;
}
```

```jsx
<form action={submitAction}>
  <input type="text" name="name" />
  <SubmitButton>Update</SubmitButton>
</form>
```

`useFormStatus()` reads the pending status of the **nearest parent `<form>`**, from *inside* a
child component — without that pending state needing to be passed down as a prop at all. This
directly solves the same [prop drilling problem](../component-architecture-and-composition/)
already covered for general component state, specifically for form status: a reusable
`SubmitButton` component, usable inside any form anywhere in the app, can know whether its parent
form is currently submitting without the parent ever needing to pass that information down
explicitly.

## Choosing Between the Two

| | `useActionState` | `useFormStatus` |
|---|---|---|
| Called from | The component that *owns* the form and its Action | Any *child* component nested inside a `<form>` |
| Provides | The action's result state, the wrapped action, and pending | Only the parent form's pending status |
| Typical use | The form's own top-level component | A reusable submit button or status indicator |

## Common Mistakes

- Calling `useFormStatus()` outside of a component that's actually nested inside a `<form>` — it
  has nothing to read from and won't reflect any real form's status.
- Forgetting that the action function passed to `useActionState` must return the *new* state on
  every call — returning nothing (or accidentally returning `undefined`) loses whatever the UI was
  meant to display.
- Recreating `useFormStatus`'s job manually by threading a `isSubmitting` prop down through several
  component layers, when `useFormStatus` reads it directly with no prop drilling at all.

## ➡️ Next

Continue to
[optimistic-ui-with-useoptimistic.md](optimistic-ui-with-useoptimistic.md) to make a form feel
instant, even while its Action is still genuinely in flight.
