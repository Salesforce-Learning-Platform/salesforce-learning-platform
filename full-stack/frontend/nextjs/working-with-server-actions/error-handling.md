# Error Handling with `useActionState`

## The Problem: Forms Need Feedback

A plain `<form action={addReview}>` (from
[forms-and-server-actions.md](forms-and-server-actions.md)) submits and runs the action, but gives
the user no feedback — no loading indicator while it's in flight, and no way to show a validation
error message (like the "rating and comment are required" error from
[data-mutations.md](data-mutations.md)) back in the UI.

## `useActionState`

```tsx
"use client";
import { useActionState } from "react";
import { addReview } from "@/app/lib/actions";

const initialState = { error: null };

async function addReviewAction(prevState: typeof initialState, formData: FormData) {
  try {
    await addReview(formData);
    return { error: null };
  } catch (error) {
    return { error: (error as Error).message };
  }
}

export default function ReviewForm() {
  const [state, formAction, pending] = useActionState(addReviewAction, initialState);

  return (
    <form action={formAction}>
      <input type="number" name="rating" min="1" max="5" />
      <textarea name="comment" />
      {state.error && <p role="alert">{state.error}</p>}
      <button type="submit" disabled={pending}>
        {pending ? "Submitting..." : "Submit Review"}
      </button>
    </form>
  );
}
```

`useActionState(action, initialState)` wraps a Server Action, returning three things: the current
`state` (whatever the action's most recent call returned), a `formAction` to actually pass to the
form, and a `pending` boolean — directly the same loading/error state modeling from
[loading-and-error-states.md](../../react/server-state-and-api-integration/loading-and-error-states.md),
purpose-built here for form-driven Server Actions specifically.

## Returning Structured State Instead of Throwing

Notice the wrapping function catches the action's error and *returns* a plain object describing
it, rather than letting the error propagate as an uncaught exception. This is a deliberate pattern
— `useActionState` is designed around the action returning its result (success or failure) as
data, which the form can then read from `state` and render accordingly, rather than around
catching exceptions in the traditional
[try/catch](../../javascript/error-handling-and-debugging/try-catch-finally.md) sense at the UI
layer.

## Accessible Error Display

```tsx
{state.error && <p role="alert">{state.error}</p>}
```

This reuses the exact `role="alert"` pattern from
[form-validation.md](../../react/advanced-forms-and-validation/form-validation.md) — ensuring a
screen reader announces the error message as soon as it appears, whether the error came from
client-side validation (covered in the React domain) or, as here, from server-side validation
inside a Server Action.

## Common Mistakes

- Using a plain `<form action={addReview}>` with no `useActionState` for a form that genuinely
  needs to show validation errors or a pending indicator, leaving the user with no feedback at all.
- Letting an action's error propagate as an uncaught exception rather than catching it and
  returning structured state `useActionState` can actually display.
- Forgetting `disabled={pending}` on the submit button, allowing a user to submit the same form
  multiple times while a previous submission is still in flight.

## Module Summary

Across this module: a Server Action is a server-only function invokable directly from client code,
but it's a genuine network-reachable endpoint — authorization and validation must be checked
inside it regardless of which UI element happens to call it (see
[introduction-to-server-actions.md](introduction-to-server-actions.md)); wiring a Server Action
directly to a form's `action` prop removes manual `fetch`/`preventDefault` boilerplate and provides
genuine progressive enhancement (see [forms-and-server-actions.md](forms-and-server-actions.md));
a complete mutation checks authorization, then validates, then mutates — in that order — exactly
like a well-built Route Handler (see [data-mutations.md](data-mutations.md));
`revalidatePath`/`revalidateTag`, called *before* any `redirect`, keep cached pages in sync with a
mutation's actual effect (see [revalidation.md](revalidation.md)); and `useActionState` provides
the pending/error state a form-driven Server Action needs to give real user feedback.

This completes the Next.js domain (OPS-093 through OPS-097).
