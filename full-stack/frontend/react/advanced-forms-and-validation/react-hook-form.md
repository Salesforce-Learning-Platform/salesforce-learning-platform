# React Hook Form

## The Problem It Solves

The hand-built approach from
[controlled-forms.md](controlled-forms.md)/[form-validation.md](form-validation.md) works, but has
a real, measurable cost as a form grows: every keystroke in a controlled input triggers a
re-render of the *entire* form component (per
[how-rerendering-works.md](../state-and-rerendering-logic/how-rerendering-works.md)), even though
only one field's display actually needs to update. On a checkout form with a dozen fields, this
adds up. **React Hook Form** manages form state largely outside React's own re-render cycle,
minimizing this cost while also cutting the boilerplate from writing `useState`, `handleChange`,
and manual validation logic by hand.

## The Same Shipping Form, with React Hook Form

```jsx
import { useForm } from "react-hook-form";

function ShippingForm() {
  const { register, handleSubmit, formState: { errors } } = useForm();

  function onSubmit(data) {
    submitOrder(data); // `data` is the complete form values object
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("fullName", { required: "Full name is required" })} />
      {errors.fullName && <span role="alert">{errors.fullName.message}</span>}

      <input {...register("zipCode", {
        pattern: { value: /^\d{5}$/, message: "Enter a valid 5-digit ZIP code" }
      })} />
      {errors.zipCode && <span role="alert">{errors.zipCode.message}</span>}

      <button type="submit">Place Order</button>
    </form>
  );
}
```

`register("fullName", { required: "..." })` replaces the manual `value`/`onChange` wiring from
[controlled-forms.md](controlled-forms.md) — it returns exactly the props (`name`, `onChange`,
`ref`, etc.) needed to connect that input to the form's internal, largely-uncontrolled state
tracking, spread directly onto the `<input>` via the spread operator (see
[parameters-and-return-values.md](../../javascript/functions/parameters-and-return-values.md)).
`handleSubmit(onSubmit)` wraps your submit logic, automatically running all registered validation
rules first and only calling `onSubmit` if the form is actually valid.

## Validation Rules, Directly in `register`

The second argument to `register` accepts the same validation concepts covered in
[form-validation.md](form-validation.md) — `required`, `pattern`, `minLength`, custom validator
functions — declared once per field, with error messages managed automatically in `formState.errors`
rather than a manually-maintained `errors` state object.

## Schema Validation Libraries

For more complex validation logic, React Hook Form integrates with schema-validation libraries
like Zod or Yup — defining a form's entire shape and validation rules in one schema object, rather
than scattering rules across each individual `register` call. This becomes genuinely valuable once
a form's validation rules involve cross-field dependencies (like confirming two password fields
match).

## When Hand-Rolling Is Still Reasonable

For a genuinely simple form (a newsletter signup with one email field), the hand-built approach
from the previous two files remains perfectly reasonable — reaching for a library adds a
dependency and an API to learn, worthwhile specifically once a form's field count and validation
complexity actually justify it.

## Common Mistakes

- Manually managing `useState` for a form's values alongside React Hook Form, duplicating what the
  library already does internally — `register` and `watch` (for reading current values when
  needed) replace that entirely.
- Forgetting to spread `register`'s return value (`{...register("fullName")}`) onto the actual
  input element, which silently disconnects the field from the form's tracking.
- Reaching for React Hook Form (or any library) for a single-field form where the added dependency
  and API surface aren't actually justified by the form's complexity.

## Next

Continue to
[complex-form-patterns.md](complex-form-patterns.md) for genuinely complex, real-world form
structures: multi-step forms and dynamic field arrays.
