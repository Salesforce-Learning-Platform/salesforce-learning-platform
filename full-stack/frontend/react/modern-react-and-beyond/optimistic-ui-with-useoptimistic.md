# ⚡ Optimistic UI with useOptimistic

## The Problem: Waiting for a Round Trip Feels Slow

```jsx
// Without optimistic UI: the name doesn't visibly change until the
// server genuinely confirms the update — a real, felt delay
async function submitAction(formData) {
  const newName = formData.get("name");
  const updatedName = await updateName(newName); // waits for the network
  setCurrentName(updatedName);
}
```

Even a fast server round trip is genuinely perceptible to a user — clicking "Save" and watching
nothing change for a few hundred milliseconds feels sluggish, even when the request is guaranteed
to succeed almost every time.

## Showing the Assumed Result Immediately

```jsx
function ChangeName({ currentName, onUpdateName }) {
  const [optimisticName, setOptimisticName] = useOptimistic(currentName);

  const submitAction = async (formData) => {
    const newName = formData.get("name");
    setOptimisticName(newName); // shown IMMEDIATELY, before the request resolves
    const updatedName = await updateName(newName); // the real, awaited request
    onUpdateName(updatedName);
  };

  return (
    <form action={submitAction}>
      <p>Your name is: {optimisticName}</p>
      <input type="text" name="name" disabled={currentName !== optimisticName} />
    </form>
  );
}
```

`useOptimistic(realValue)` returns the current value to display, plus a function to set a
temporary, "optimistic" value shown **immediately** — before the real async request has actually
resolved. Once the real request finishes and the underlying `currentName` prop updates, React
automatically reconciles `optimisticName` back to the real, confirmed value.

## What Happens If the Request Actually Fails

If `updateName` above throws or the surrounding logic doesn't update `currentName` to match, React
reverts the optimistic value back to the last real value once the action finishes — so a genuine
failure needs its own explicit handling (showing an error, per
[actions-and-form-handling.md](actions-and-form-handling.md)) rather than assuming the optimistic
update alone is sufficient.

## When Optimistic UI Is the Right Choice

```
GOOD FIT:   liking a post, marking a todo complete, sending a chat
            message — actions that succeed the vast majority of the
            time, where an instant visual response matters

POOR FIT:   submitting a payment, placing an order — actions where
            showing a false "success" before genuine confirmation
            could mislead the user about something consequential
```

Optimistic UI is a deliberate tradeoff: instant perceived responsiveness, in exchange for
occasionally showing something that later needs correcting if the real request fails. This tradeoff
is excellent for low-stakes, usually-successful actions, and a poor fit for anything where a false
positive result could genuinely mislead the user about something important.

## Common Mistakes

- Using `useOptimistic` for a high-stakes action (a payment, an irreversible deletion) where
  showing a premature "success" before real confirmation could genuinely mislead the user.
- Forgetting to handle the real failure case at all, assuming the optimistic value reverting
  automatically is sufficient user feedback on its own — an explicit error message is still needed.
- Confusing `useOptimistic`'s temporary value with genuine, persisted state — it's specifically
  for the visual gap between an action starting and its real result arriving, not a replacement for
  actual state management.

## ➡️ Next

Continue to [the-use-hook.md](the-use-hook.md) to see the hook that makes reading a promise
directly during render — the mechanism Suspense and optimistic UI both build on — actually possible.
