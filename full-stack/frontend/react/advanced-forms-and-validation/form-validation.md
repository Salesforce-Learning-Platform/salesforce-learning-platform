# Form Validation

## Validation on Submit

Continuing the checkout shipping form from [controlled-forms.md](controlled-forms.md):

```jsx
function validate(formData) {
  const errors = {};
  if (!formData.fullName.trim()) errors.fullName = "Full name is required";
  if (!formData.zipCode.match(/^\d{5}$/)) errors.zipCode = "Enter a valid 5-digit ZIP code";
  return errors;
}

function handleSubmit(event) {
  event.preventDefault();
  const validationErrors = validate(formData);
  if (Object.keys(validationErrors).length > 0) {
    setErrors(validationErrors);
    return; // stop — don't submit an invalid form
  }
  submitOrder(formData);
}
```

This directly reuses the regular-expression pattern-matching from
[regular-expressions.md](../../javascript/additional-javascript-topics/regular-expressions.md),
applied to a realistic ZIP code check.

## Displaying Errors Accessibly

```jsx
<label htmlFor="zipCode">ZIP Code</label>
<input
  id="zipCode"
  name="zipCode"
  value={formData.zipCode}
  onChange={handleChange}
  aria-describedby={errors.zipCode ? "zipCode-error" : undefined}
  aria-invalid={!!errors.zipCode}
/>
{errors.zipCode && <span id="zipCode-error" role="alert">{errors.zipCode}</span>}
```

This directly applies
[accessible-form-patterns.md](../../html/html-forms-and-user-input/accessible-form-patterns.md):
`aria-describedby` programmatically links the error message to its field, and `role="alert"`
ensures a screen reader announces the new error message as soon as it appears.

## Validating on Blur vs. on Every Keystroke

```jsx
function handleBlur(event) {
  const { name } = event.target;
  const fieldErrors = validate(formData);
  setErrors(prev => ({ ...prev, [name]: fieldErrors[name] }));
}
```

Validating on every keystroke (`onChange`) can feel intrusive — showing "required" the instant a
user starts typing a field they haven't finished yet. Validating `onBlur` (when the user leaves a
field) is a more common, less jarring pattern for initial validation, often combined with
immediate `onChange` re-validation *after* an error has already been shown, so the error clears as
soon as it's actually fixed.

## Remember: This Is Still Only a UX Layer

Exactly as flagged in
[html-validation-and-constraints.md](../../html/html-forms-and-user-input/html-validation-and-constraints.md)
and reiterated in this module's README: no amount of client-side validation — HTML attributes or
custom JavaScript logic — replaces server-side validation. A request to place an order can always
be sent directly to the server's API, bypassing this entire validation function. The server must
independently validate the same ZIP code format, full name presence, and everything else, treating
the client exactly as untrustworthy as
[frontend-and-backend-responsibilities.md](../../foundations/client-server-architecture/frontend-and-backend-responsibilities.md)
describes.

## Common Mistakes

- Validating aggressively on every keystroke from the very first character typed, producing a
  jarring experience where every field starts in an error state.
- Displaying an error message visually without `aria-describedby`/`role="alert"`, leaving screen
  reader users unaware a validation error even occurred.
- Treating passing client-side validation as proof the data reaching the server will be valid —
  it's a UX convenience only, never a security or data-integrity guarantee.

## Next

Continue to [react-hook-form.md](react-hook-form.md) to see how a dedicated library reduces the
boilerplate in what's been built by hand so far.
