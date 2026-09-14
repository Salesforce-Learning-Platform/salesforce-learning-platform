# Complex Form Patterns

## Multi-Step Forms

A checkout flow is rarely one single form — shipping address, then payment details, then a final
review step, each shown one at a time:

```jsx
function CheckoutFlow() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({});

  function handleNext(stepData) {
    setFormData(prev => ({ ...prev, ...stepData })); // merge this step's data in
    setStep(prev => prev + 1);
  }

  if (step === 1) return <ShippingStep onNext={handleNext} />;
  if (step === 2) return <PaymentStep onNext={handleNext} />;
  if (step === 3) return <ReviewStep formData={formData} onSubmit={submitOrder} />;
}
```

The key architectural decision: state lives in the **parent** (`CheckoutFlow`), not in each
individual step — this is "lifting state up," directly applying the composition and shared-state
reasoning from
[component-composition.md](../component-architecture-and-composition/component-composition.md).
Each step component only needs to know about its own fields and calls `onNext` with its piece of
the data; the parent is responsible for merging everything together and tracking which step is
currently active.

## Dynamic Field Arrays

A real order form might let a user add multiple line items — a genuinely dynamic number of
repeated field groups:

```jsx
function OrderItemsForm() {
  const [items, setItems] = useState([{ product: "", quantity: 1 }]);

  function addItem() {
    setItems(prev => [...prev, { product: "", quantity: 1 }]);
  }

  function updateItem(index, field, value) {
    setItems(prev => prev.map((item, i) =>
      i === index ? { ...item, [field]: value } : item
    ));
  }

  function removeItem(index) {
    setItems(prev => prev.filter((_, i) => i !== index));
  }

  return (
    <>
      {items.map((item, index) => (
        <div key={index}>
          <input
            value={item.product}
            onChange={e => updateItem(index, "product", e.target.value)}
          />
          <button type="button" onClick={() => removeItem(index)}>Remove</button>
        </div>
      ))}
      <button type="button" onClick={addItem}>Add Item</button>
    </>
  );
}
```

This is directly built from the non-mutating array method discipline in
[array-methods.md](../../javascript/arrays-and-objects/array-methods.md) — `map` to update one
item immutably, `filter` to remove one, spread to add one — never mutating the `items` array
directly, exactly the state-update discipline from
[usestate.md](../state-and-rerendering-logic/usestate.md).

## React Hook Form's `useFieldArray` for the Same Pattern

```jsx
import { useForm, useFieldArray } from "react-hook-form";

function OrderItemsForm() {
  const { control, register } = useForm({ defaultValues: { items: [{ product: "", quantity: 1 }] } });
  const { fields, append, remove } = useFieldArray({ control, name: "items" });

  return (
    <>
      {fields.map((field, index) => (
        <div key={field.id}>
          <input {...register(`items.${index}.product`)} />
          <button type="button" onClick={() => remove(index)}>Remove</button>
        </div>
      ))}
      <button type="button" onClick={() => append({ product: "", quantity: 1 })}>Add Item</button>
    </>
  );
}
```

`useFieldArray` handles exactly the same add/update/remove logic as the hand-built version above,
integrated with React Hook Form's validation and submission handling — the same "library reduces
boilerplate" tradeoff from [react-hook-form.md](react-hook-form.md), applied to this specific,
more complex pattern.

## Common Mistakes

- Managing multi-step form state inside each individual step component instead of lifting it to a
  shared parent, losing data when navigating between steps.
- Mutating the items array directly (`items[index].product = value`) instead of using `map` to
  produce a new array, silently breaking React's change detection.
- Using the array index as the sole persistent identifier for a dynamic field array in a way that
  breaks when items are reordered or removed from the middle — React Hook Form's `field.id`
  (a stable, library-generated key) exists specifically to avoid this class of bug.

## Module Summary

Across this module: multi-field controlled forms are managed with one state object and one generic
change handler (see [controlled-forms.md](controlled-forms.md)); client-side validation improves
UX but never replaces mandatory server-side validation (see [form-validation.md](form-validation.md));
React Hook Form reduces both boilerplate and unnecessary re-renders for forms of real complexity
(see [react-hook-form.md](react-hook-form.md)); and multi-step forms and dynamic field arrays are
handled by lifting state to a shared parent and using non-mutating array operations, whether built
by hand or via React Hook Form's `useFieldArray`.
