# Actions, Reducers, and the Store

## Actions: Describing What Happened

```js
const addItem = { type: "cart/addItem", payload: { id: "sku-1", name: "Keyboard", price: 79 } };
const removeItem = { type: "cart/removeItem", payload: { id: "sku-1" } };
```

An **action** is a plain object with a `type` field (a string identifying what happened) and
usually a `payload` (the data needed to actually handle it) — a factual description of an event,
not a direct instruction for how to update state.

## The Reducer: A Pure Function

```js
const initialState = { items: [] };

function cartReducer(state = initialState, action) {
  switch (action.type) {
    case "cart/addItem":
      return { ...state, items: [...state.items, action.payload] }; // new array, new object
    case "cart/removeItem":
      return { ...state, items: state.items.filter(item => item.id !== action.payload.id) };
    default:
      return state; // unrecognized action — return the existing state unchanged
  }
}
```

This directly reuses the non-mutating array patterns from
[array-methods.md](../../javascript/arrays-and-objects/array-methods.md) — spreading to add an
item, `filter` to remove one — exactly the same discipline as an immutable `useState` update,
enforced here as a strict rule rather than a convention. The `default` case matters: an unhandled
action type must return the *existing* state object unchanged, not `undefined` or a new object.

## The Store

```js
import { createStore } from "redux";

const store = createStore(cartReducer);

store.dispatch(addItem); // triggers the reducer, updates the store's state
store.getState();          // { items: [{ id: "sku-1", name: "Keyboard", price: 79 }] }
```

The **store** holds the current state and provides `dispatch` (to send an action through the
reducer) and `getState` (to read the current state) — this is the "single store" principle from
[redux-fundamentals.md](redux-fundamentals.md) made concrete.

## Connecting to React with `react-redux`

```jsx
import { useSelector, useDispatch } from "react-redux";

function CartSummary() {
  const items = useSelector(state => state.items); // read from the store
  const dispatch = useDispatch();

  return (
    <div>
      <p>{items.length} items in cart</p>
      <button onClick={() => dispatch(removeItem)}>Remove last item</button>
    </div>
  );
}
```

`useSelector` reads a specific piece of the store's state (re-rendering the component only when
that specific piece changes — a more granular subscription than Context's all-consumers-re-render
behavior from [context-performance.md](../global-state-management/context-performance.md));
`useDispatch` returns the function used to send actions.

## Common Mistakes

- Mutating `state` directly inside a reducer (`state.items.push(...)`) instead of returning a new
  object — this silently breaks Redux's change-detection, exactly like directly mutating
  `useState`.
- Forgetting the `default` case in a reducer's switch statement, causing it to return `undefined`
  for any action it doesn't explicitly handle.
- Performing a side effect (an API call, a `console.log` with real consequences) directly inside a
  reducer — reducers must remain pure; async logic belongs in a thunk, covered next.

## Next

Continue to [redux-toolkit.md](redux-toolkit.md) to see this exact same cart rebuilt with
dramatically less boilerplate.
