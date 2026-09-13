# Input Types and Attributes

## Why the `type` Attribute Matters

`<input>` is a single element that behaves completely differently depending on its `type`
attribute — each type gets its own browser UI, mobile keyboard, and built-in validation behavior,
all without any extra code.

## Common Input Types

| Type | Use for | What you get for free |
|---|---|---|
| `text` | Generic short text | Nothing beyond a plain text box |
| `email` | Email addresses | Mobile email keyboard, basic format validation |
| `password` | Passwords | Characters masked visually |
| `tel` | Phone numbers | Mobile numeric/phone keyboard (no format validation — phone formats vary too much globally) |
| `url` | Web addresses | Basic URL format validation |
| `number` | Numeric values | Numeric keyboard, stepper UI, `min`/`max`/`step` support |
| `date`, `time`, `datetime-local` | Dates and times | A native date/time picker UI |
| `checkbox` | Independent on/off choices | Multiple can be selected at once |
| `radio` | One choice from a set | Grouped by shared `name`; only one selectable |
| `search` | Search boxes | Often a native "clear" affordance |
| `file` | File uploads | A native file picker |

## Attributes That Configure Behavior

| Attribute | Effect |
|---|---|
| `placeholder` | Grey hint text shown when empty — not a replacement for `<label>` |
| `required` | Field must have a value before the form submits (see [html-validation-and-constraints.md](html-validation-and-constraints.md)) |
| `disabled` | Field is inert and its value is not submitted at all |
| `readonly` | Field's value is submitted but cannot be edited |
| `min`, `max`, `step` | Bounds and increments for numeric/date types |
| `pattern` | A regular expression the value must match |
| `autocomplete` | Hints the browser about what kind of data this is, enabling autofill (`autocomplete="email"`, `"tel"`, etc.) |

## Checkboxes vs. Radio Buttons

This pair is worth being precise about: checkboxes represent independent boolean choices (any
number can be checked); radio buttons sharing the same `name` represent a single choice among
mutually exclusive options (checking one automatically unchecks the others in that group). Using a
checkbox where the choices are actually mutually exclusive misleads both the user and any code
reading the submitted values.

```html
<!-- Independent choices -->
<input type="checkbox" name="notifications" value="email"> Email
<input type="checkbox" name="notifications" value="sms"> SMS

<!-- Mutually exclusive choices -->
<input type="radio" name="plan" value="free"> Free
<input type="radio" name="plan" value="pro"> Pro
```

## Common Mistakes

- Using `type="text"` for everything, missing the free mobile keyboard and validation behavior
  that a more specific type provides.
- Using `disabled` when `readonly` was actually intended — a `disabled` field's value is not
  included when the form submits at all, which silently drops data if that wasn't the goal.
- Reaching for `pattern` with a fragile, overly strict regular expression (a common failure:
  rejecting valid international phone numbers or email addresses) instead of a more permissive
  format check paired with server-side validation.

## Next

Continue to
[html-validation-and-constraints.md](html-validation-and-constraints.md) to see exactly how
`required`, `pattern`, and related attributes are enforced — and their real limits.
