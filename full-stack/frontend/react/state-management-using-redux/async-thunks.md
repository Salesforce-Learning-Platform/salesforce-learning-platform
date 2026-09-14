# Async Thunks

## The Problem: Reducers Must Be Pure

[redux-fundamentals.md](redux-fundamentals.md) established that reducers must be pure functions —
no side effects, which explicitly rules out making an API call (like submitting the cart at
checkout) directly inside one. But real applications obviously need to perform async operations in
response to user actions.

## `createAsyncThunk`

```js
import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

const checkout = createAsyncThunk("cart/checkout", async (cartItems) => {
  const response = await fetch("/api/orders", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ items: cartItems }),
  });
  if (!response.ok) throw new Error(`Checkout failed: ${response.status}`);
  return response.json(); // becomes the action's payload on success
});
```

This directly reuses the Fetch API patterns from
[fetch-api.md](../../javascript/asynchronous-programming-and-modules/fetch-api.md), including the
`response.ok` check — `createAsyncThunk` wraps an async function and automatically dispatches
three actions across its lifecycle: `pending` (when it starts), `fulfilled` (on success, with the
returned value as payload), and `rejected` (if it throws).

## Handling the Three Lifecycle States in a Slice

```js
const cartSlice = createSlice({
  name: "cart",
  initialState: { items: [], checkoutStatus: "idle", error: null },
  reducers: {
    addItem(state, action) { state.items.push(action.payload); },
  },
  extraReducers(builder) {
    builder
      .addCase(checkout.pending, (state) => {
        state.checkoutStatus = "loading";
      })
      .addCase(checkout.fulfilled, (state) => {
        state.checkoutStatus = "succeeded";
        state.items = []; // clear the cart on successful checkout
      })
      .addCase(checkout.rejected, (state, action) => {
        state.checkoutStatus = "failed";
        state.error = action.error.message;
      });
  },
});
```

This is the same three-state pattern (loading/success/error) from
[loading-and-error-states.md](../server-state-and-api-integration/loading-and-error-states.md),
now expressed as part of the Redux store rather than local component state — appropriate
specifically because checkout status is genuinely global, application-wide state that multiple
components (a checkout button, an order confirmation page) might need to react to.

## Dispatching the Thunk from a Component

```jsx
function CheckoutButton() {
  const items = useSelector(state => state.cart.items);
  const status = useSelector(state => state.cart.checkoutStatus);
  const dispatch = useDispatch();

  return (
    <button onClick={() => dispatch(checkout(items))} disabled={status === "loading"}>
      {status === "loading" ? "Processing..." : "Checkout"}
    </button>
  );
}
```

Dispatching a thunk (`checkout(items)`) looks identical to dispatching a plain action — Redux
Toolkit's thunk middleware handles the actual async execution and the three lifecycle
dispatches transparently underneath.

## Common Mistakes

- Attempting to make an API call directly inside a plain reducer function, violating the
  pure-function requirement — async logic always belongs in a thunk.
- Forgetting to handle all three thunk lifecycle states (`pending`/`fulfilled`/`rejected`) in
  `extraReducers`, leaving the UI with no way to show a loading indicator or a failure message.
- Storing genuinely server-owned, cacheable data (an order history) in Redux via thunks, when
  React Query (from [react-query.md](../server-state-and-api-integration/react-query.md)) already
  solves caching, deduplication, and refetching for exactly that category of data more directly.

## Module Summary

Across this module: Redux enforces a single store, read-only state, and pure-function reducers,
buying real guarantees like time-travel debugging in exchange for real strictness (see
[redux-fundamentals.md](redux-fundamentals.md)); actions describe what happened, reducers are pure
functions computing new state, and the store ties them together (see
[actions-reducers-and-store.md](actions-reducers-and-store.md)); Redux Toolkit's `createSlice`
generates the same pattern with dramatically less boilerplate, using Immer to make mutation-looking
syntax safely produce immutable updates (see [redux-toolkit.md](redux-toolkit.md)); and
`createAsyncThunk` handles asynchronous operations correctly within Redux's synchronous reducer
model, dispatching pending/fulfilled/rejected actions automatically.
