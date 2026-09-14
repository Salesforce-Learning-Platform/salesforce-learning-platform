# Redux Toolkit

## The Same Cart, With `createSlice`

Compare directly against [actions-reducers-and-store.md](actions-reducers-and-store.md):

```js
import { createSlice, configureStore } from "@reduxjs/toolkit";

const cartSlice = createSlice({
  name: "cart",
  initialState: { items: [] },
  reducers: {
    addItem(state, action) {
      state.items.push(action.payload); // looks like mutation — see below
    },
    removeItem(state, action) {
      state.items = state.items.filter(item => item.id !== action.payload.id);
    },
  },
});

export const { addItem, removeItem } = cartSlice.actions; // action creators, generated automatically
const store = configureStore({ reducer: { cart: cartSlice.reducer } });
```

`createSlice` generates the action type strings, action creator functions, and the reducer all
from one definition — replacing the hand-written `switch` statement, action object literals, and
manual `createStore` setup from
[actions-reducers-and-store.md](actions-reducers-and-store.md) entirely.

## Why `state.items.push(...)` Is Actually Safe Here

This looks like it violates the "never mutate state" rule from
[redux-fundamentals.md](redux-fundamentals.md) — but Redux Toolkit's `createSlice` uses a library
called **Immer** internally, which lets you write code that *looks* like direct mutation, while
actually producing a correctly immutable update behind the scenes. This is a deliberate design
choice specifically to make the common case (updating a nested piece of state) far less verbose
than manually spreading every level, without sacrificing the actual immutability guarantee Redux
depends on.

## Using It in React — Identical to Plain Redux

```jsx
import { useSelector, useDispatch } from "react-redux";
import { addItem, removeItem } from "./cartSlice";

function CartSummary() {
  const items = useSelector(state => state.cart.items);
  const dispatch = useDispatch();

  return (
    <div>
      <p>{items.length} items in cart</p>
      <button onClick={() => dispatch(addItem({ id: "sku-2", name: "Mouse", price: 29 }))}>
        Add Mouse
      </button>
    </div>
  );
}
```

`useSelector`/`useDispatch` work identically regardless of whether the store was built with plain
Redux or Redux Toolkit — Redux Toolkit changes *how the store and reducers are defined*, not how
components interact with them.

## Why Redux Toolkit Is Now the Standard

Redux's own official documentation recommends Redux Toolkit as "the standard way to write Redux
logic" specifically because it eliminates the most error-prone, boilerplate-heavy parts of plain
Redux (manually keeping action type strings, action creators, and reducer cases in sync) while
still enforcing the exact same underlying principles from
[redux-fundamentals.md](redux-fundamentals.md) — new Redux code should default to Redux Toolkit
rather than the hand-written pattern from the previous file, which remains valuable to understand
but isn't how new Redux code is typically written today.

## Common Mistakes

- Writing plain Redux (hand-rolled action types, switch-statement reducers) for new code, missing
  the boilerplate reduction Redux Toolkit provides with no loss of correctness.
- Assuming the `push`/direct-mutation-looking syntax inside a `createSlice` reducer is unsafe —
  it's specifically safe *because* of Immer, and only inside a `createSlice` reducer; the same code
  outside that context would be a genuine, harmful mutation.
- Forgetting to export and use the auto-generated action creators (`cartSlice.actions.addItem`),
  instead trying to hand-construct action objects that no longer match what `createSlice` expects.

## Next

Continue to [async-thunks.md](async-thunks.md) to handle an actual API call — like completing
checkout — within this strictly synchronous reducer model.
