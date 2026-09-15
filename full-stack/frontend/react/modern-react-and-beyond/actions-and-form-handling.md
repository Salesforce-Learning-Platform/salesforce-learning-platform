# 📝 Actions and Form Handling

## The Pattern This Replaces

```jsx
// Before React 19: manual state for every piece of form lifecycle
function UpdateName() {
  const [name, setName] = useState("");
  const [error, setError] = useState(null);
  const [isPending, setIsPending] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setIsPending(true);
    const err = await updateName(name);
    setIsPending(false);
    if (err) { setError(err); return; }
    redirect("/profile");
  }

  return (
    <form onSubmit={handleSubmit}>
      <input value={name} onChange={(e) => setName(e.target.value)} />
      <button disabled={isPending}>Update</button>
      {error && <p>{error}</p>}
    </form>
  );
}
```

Every form covered in [Advanced Forms and Validation](../advanced-forms-and-validation/) follows
this pattern: manual state for the submitted value, manual `isPending` tracking, manual error
state, and a submit handler wiring all three together by hand. This works, and remains completely
valid — Actions exist to remove the *manual bookkeeping* specifically, not to replace form
validation or controlled inputs as concepts.

## An Action — an Async Function Passed to `<form action>`

```jsx
function UpdateName() {
  const [name, setName] = useState("");
  const [error, setError] = useState(null);
  const [isPending, startTransition] = useTransition();

  const submitAction = () => {
    startTransition(async () => {
      const err = await updateName(name);
      if (err) { setError(err); return; }
      redirect("/profile");
    });
  };

  return (
    <div>
      <input value={name} onChange={(e) => setName(e.target.value)} />
      <button onClick={submitAction} disabled={isPending}>Update</button>
      {error && <p>{error}</p>}
    </div>
  );
}
```

An **Action** is simply an async function run inside a **transition** — `useTransition`'s
`isPending` is tracked automatically, and the async function can freely `await` real work without
manually toggling a loading flag before and after. Passing an Action function directly to a
`<form action={...}>` prop goes even further: React automatically resets the form on a successful
submission, and manages pending state without any transition boilerplate at all.

## Form Actions With `formData`

```jsx
async function submitAction(formData) {
  const error = await updateName(formData.get("name"));
  if (error) return error;
  redirect("/profile");
}

<form action={submitAction}>
  <input type="text" name="name" />
  <button type="submit">Update</button>
</form>
```

When an Action is passed directly to a `<form>`'s `action` prop, React calls it with the form's
`FormData` automatically — reading `formData.get("name")` directly, with no `onChange` handler or
controlled `useState` value needed at all for a plain, non-live-validated field. This is a genuine
simplification over [controlled inputs](../advanced-forms-and-validation/) for forms that don't
need to react to every keystroke.

## Common Mistakes

- Assuming Actions eliminate the need for client-side validation entirely — they simplify
  submission handling, not the separate concern of validating input before or during submission.
- Forgetting that a plain `<form action={asyncFunction}>` still needs the function to actually be
  async and to genuinely handle its own errors — React doesn't add error handling on its own.
- Mixing the manual `useState`-per-field pattern with Actions unnecessarily for a form that has no
  need for live, per-keystroke reactivity — `formData.get()` is often simpler for that case.

## ➡️ Next

Continue to
[useactionstate-and-useformstatus.md](useactionstate-and-useformstatus.md) to remove even more of
this boilerplate with two hooks purpose-built for Actions.
