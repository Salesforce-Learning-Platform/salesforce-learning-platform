# ✅ Forms and Constraint Validation

## Let the Browser Do the First Layer of Validation

[forms-introduction.md](../../html/semantic-html-and-browser-rendering/forms-introduction.md) covers
how HTML forms are structured. This file is about their **JavaScript** side: the **Constraint
Validation API**, which exposes the validity rules you declare in HTML (`required`, `pattern`,
`type="email"`, `min`, `max`, `minlength`) to your code; and **`FormData`**, which reads a form's values.
Using them well gives accessible, native validation with very little script.

## 📋 Declaring the Rules in HTML

```html
<form id="signup" novalidate>
  <input name="email" type="email" required>
  <input name="name" required minlength="3" maxlength="10" pattern="[A-Za-z ]+">
  <input name="age" type="number" min="18" max="99" step="1">
  <button>Sign up</button>
</form>
```

Each attribute defines a constraint the browser checks. The `novalidate` attribute turns off the
browser's automatic error bubbles — per MDN, the API and the `:valid`/`:invalid` pseudo-classes still
work, so you can show your own messages while keeping the native rules.

## 🔍 Reading Validity: `validity`

Every form control has a `validity` object (a `ValidityState`) whose boolean flags say *which*
constraint failed:

| Flag | True when |
|------|-----------|
| `valueMissing` | A `required` field is empty |
| `typeMismatch` | The value is not a valid email or URL for its `type` |
| `patternMismatch` | The value does not match `pattern` |
| `tooShort` / `tooLong` | The value breaks `minlength` / `maxlength` |
| `rangeUnderflow` / `rangeOverflow` | The value is below `min` / above `max` |
| `stepMismatch` / `badInput` | The value does not fit the `step`, or cannot be parsed |
| `customError` | You called `setCustomValidity` with a message |
| `valid` | **No** constraint fails |

Setting values from script and reading each field's flags (run in a real browser):

```js
const email = form.elements.email;
const name = form.elements.name;
const age = form.elements.age;

// email                                  failing flag
email.value = "";            //           valueMissing
email.value = "nope";        //           typeMismatch
email.value = "a@b.co";      //           (valid)

// name
name.value = "Ada1";         //           patternMismatch  (digits don't match [A-Za-z ]+)

// age
age.value = "17";            //           rangeUnderflow
age.value = "30";            //           (valid)
```

And the localized message a browser would show for the bad email:

```js
email.value = "nope";
console.log(email.validationMessage);
// Please include an '@' in the email address. 'nope' is missing an '@'.
```

### A Gotcha: `tooShort` and `tooLong` Follow User Edits

In the same test, setting `name.value = "Al"` from script — shorter than `minlength="3"` — left the
field `valid`. MDN's description of `tooShort` ties it to a value "after having been edited by the user."
Length constraints are therefore **not** a guarantee for values your own code assigns; if you set a
field's value programmatically, validate it yourself.

## 🔧 Methods

| Member | Behavior |
|--------|----------|
| `checkValidity()` | Returns `true`/`false`, and fires an `invalid` event on each failing control |
| `reportValidity()` | Like `checkValidity()`, and also shows the browser's error messages to the user |
| `setCustomValidity(message)` | Marks the control invalid with your own message; pass `""` to clear it |
| `validationMessage` | The current (localized) error text, or `""` if valid |
| `willValidate` | Whether the control participates in validation |

Both `checkValidity` and `reportValidity` exist on individual controls **and** on the whole `<form>`:

```js
name.value = "Ada";
name.setCustomValidity("Name is taken");           // e.g. after a server-side check

console.log(name.validity.valid);                  // false
console.log(name.validity.customError);            // true
console.log(name.validationMessage);               // Name is taken
console.log(form.checkValidity());                 // false — one invalid control invalidates the form

name.setCustomValidity("");                        // clear it, or the field stays invalid forever
console.log(form.checkValidity());                 // true
```

Forgetting to clear a custom message is the most common bug: the control stays `customError`-invalid
even after the user fixes the problem. A typical pattern clears it on every `input` event and sets it
again only when a check fails.

Calling `checkValidity()` on an invalid control fires its `invalid` event once (the test counted exactly
one), which you can listen for to render your own message next to the field.

### Styling

The `:valid` and `:invalid` CSS pseudo-classes reflect the same state. Plain `:invalid` matches
*immediately* — before the user has typed anything — which looks hostile; MDN lists `:user-invalid` and
`:user-valid`, which apply only after the user has interacted.

## 📤 Reading Values: `FormData`

`new FormData(form)` collects the form's current values. It follows the same rules the browser uses
when actually submitting:

```html
<input name="tag" type="checkbox" value="a" checked>
<input name="tag" type="checkbox" value="b">
<input name="tag" type="checkbox" value="c" checked>
<input name="skip" value="disabled-one" disabled>
<select name="plan"><option value="free">Free</option><option value="pro" selected>Pro</option></select>
```

```js
const data = new FormData(form);

console.log([...data.entries()]);
// [ [ 'email', 'a@b.co' ], [ 'name', 'Ada' ], [ 'age', '30' ],
//   [ 'tag', 'a' ], [ 'tag', 'c' ], [ 'plan', 'pro' ] ]

console.log(data.get("tag"));          // a            — the FIRST value
console.log(data.getAll("tag"));       // [ 'a', 'c' ] — every value
console.log(data.has("skip"));         // false        — disabled controls are not included
```

Notice that the unchecked checkbox (`b`) and the disabled input do not appear — only controls that
would actually be submitted do. Every value is a **string** (`age` is `'30'`, not `30`); file inputs
yield `File` objects.

### Converting to an Object — and a Trap

`Object.fromEntries(data)` is the usual shortcut, but plain objects hold one value per key, so repeated
names collapse to the **last** one:

```js
console.log(Object.fromEntries(data));
// { email: 'a@b.co', name: 'Ada', age: '30', tag: 'c', plan: 'pro' }   ← the 'a' tag is gone
```

Use `getAll` for multi-value fields, or keep the entries. To send the values as a URL-encoded body,
pass the `FormData` to `URLSearchParams`, which preserves repeated keys:

```js
console.log(new URLSearchParams(data).toString());
// email=a%40b.co&name=Ada&age=30&tag=a&tag=c&plan=pro
```

### Sending It

Pass a `FormData` straight to `fetch` and the browser sends `multipart/form-data`. **Do not set the
`Content-Type` header yourself** — the browser must add it, because the value includes a generated
boundary:

```js
form.addEventListener("submit", async (event) => {
  event.preventDefault();                              // stop the default page-reloading submit

  if (!form.reportValidity()) return;                  // show native errors and stop if invalid

  const response = await fetch("/api/signup", { method: "POST", body: new FormData(form) });
  if (!response.ok) showError("Sign-up failed.");
});
```

(See [fetch-api.md](../asynchronous-programming-and-modules/fetch-api.md) for `fetch` and
[event-object.md](../events/event-object.md) for `preventDefault`.)

## 🛡️ Client-Side Validation Is Not Security

MDN is blunt about this: client-side validation improves the user experience but is not a security
measure. Anyone can bypass your form — disable JavaScript, edit the HTML in DevTools, or send requests
directly with a tool like `curl`. **The server must validate everything again**, and treat all input as
untrusted. The consequences of skipping that are the subject of the
[Web Security injection module](../../../web-security/injection-attacks/); for structured validation of
incoming data on the server side in this platform, see
[schema validation with Zod](../../../artificial-intelligence/schema-validation-with-zod/).

## 🎤 Interview Angle

- **"How do you validate a form in JavaScript?"** Declare constraints in HTML and use the Constraint
  Validation API — `checkValidity()`/`reportValidity()`, `validity` flags, `setCustomValidity` — in a
  `submit` handler, then validate again on the server.
- **"`checkValidity()` vs. `reportValidity()`?"** Both return a boolean; `reportValidity()` also shows
  the browser's error UI.
- **"Why is client-side validation insufficient?"** It can be bypassed; it only helps the user.
- **"Why does `Object.fromEntries(new FormData(form))` lose checkbox values?"** Repeated field names
  collapse to the last value in an object; use `getAll` or keep the entries.

## Common Mistakes

- **Forgetting `setCustomValidity("")`**, leaving a field permanently invalid.
- **Assuming programmatically set values are checked against `minlength`/`maxlength`.**
- **Treating the browser's validation as a security boundary.**
- **Setting `Content-Type` manually when sending `FormData`.**
- **Flattening a `FormData` to an object and losing repeated fields.**
- **Using `:invalid` styling that shows errors before the user has typed anything.**

## ➡️ Next

Continue to [ajax-and-xmlhttprequest.md](ajax-and-xmlhttprequest.md) to close the module with the
older way of making requests — which you will still meet in existing code.
