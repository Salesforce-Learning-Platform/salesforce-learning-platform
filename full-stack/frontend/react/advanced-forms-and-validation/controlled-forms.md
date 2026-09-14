# Controlled Forms

## Managing Multiple Fields

Extending the single-input pattern from
[controlled-and-uncontrolled-components.md](../component-architecture-and-composition/controlled-and-uncontrolled-components.md)
to a realistic multi-field form — a checkout shipping form:

```jsx
function ShippingForm() {
  const [formData, setFormData] = useState({
    fullName: "",
    address: "",
    city: "",
    zipCode: "",
  });

  function handleChange(event) {
    const { name, value } = event.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  }

  return (
    <form>
      <input name="fullName" value={formData.fullName} onChange={handleChange} />
      <input name="address" value={formData.address} onChange={handleChange} />
      <input name="city" value={formData.city} onChange={handleChange} />
      <input name="zipCode" value={formData.zipCode} onChange={handleChange} />
    </form>
  );
}
```

Rather than a separate `useState` for every single field, one object holds the entire form's
state, with a single `handleChange` reused across every input — each field's `name` attribute
matches the corresponding key in `formData`, letting one generic handler update the correct
property using a computed key (see
[object-methods.md](../../javascript/arrays-and-objects/object-methods.md)'s spread pattern).

## Why `prev => ({ ...prev, [name]: value })`, Specifically

This uses the updater-function form of `setState` from
[usestate.md](../state-and-rerendering-logic/usestate.md) — reading the *latest*
form state (`prev`) rather than a potentially stale value from the current render, exactly the
batching concern from
[batching-state-updates.md](../state-and-rerendering-logic/batching-state-updates.md). Spreading
`prev` and overriding only the changed key preserves every other field's current value untouched —
directly applying the never-mutate-state rule.

## Handling Checkboxes and Selects

```jsx
function handleChange(event) {
  const { name, value, type, checked } = event.target;
  setFormData(prev => ({
    ...prev,
    [name]: type === "checkbox" ? checked : value,
  }));
}
```

A checkbox's relevant property is `checked`, not `value` — this small but important distinction
(covered originally in
[input-types-and-attributes.md](../../html/html-forms-and-user-input/input-types-and-attributes.md))
needs to be handled explicitly in a generic change handler like this one.

## Submitting the Form

```jsx
function handleSubmit(event) {
  event.preventDefault(); // stop the browser's default full-page navigation
  console.log("Submitting:", formData);
  // send formData to the server here, per form-submission-and-data.md
}

<form onSubmit={handleSubmit}>
  {/* fields */}
  <button type="submit">Place Order</button>
</form>
```

This is the same `preventDefault()` pattern from
[event-object.md](../../javascript/events/event-object.md) and
[form-submission-and-data.md](../../html/html-forms-and-user-input/form-submission-and-data.md) —
intercepting the browser's default submission behavior so the form's data can be sent via `fetch`
(see [fetch-api.md](../../javascript/asynchronous-programming-and-modules/fetch-api.md)) under
full JavaScript control instead.

## Common Mistakes

- Creating a separate `useState` per field on a form with many fields, producing repetitive
  handler code instead of one object and one generic handler.
- Forgetting the checkbox `checked`-vs-`value` distinction in a generic change handler, silently
  storing `undefined` for checkbox fields.
- Forgetting `event.preventDefault()` in the submit handler, causing an unwanted full-page reload
  alongside the intended JavaScript-driven submission.

## Next

Continue to [form-validation.md](form-validation.md) to add validation to this shipping form.
