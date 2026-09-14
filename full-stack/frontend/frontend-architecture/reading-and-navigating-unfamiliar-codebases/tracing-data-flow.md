# Tracing Data Flow

## Start From What You Can See, Work Backward

```jsx
// CartSummary.jsx — the rendered output you're looking at
function CartSummary({ total }) {
  return <p>Total: ${total.toFixed(2)}</p>;
}
```

If a number on the screen is wrong, the instinct is often to stare at the component rendering it —
but that component only displays whatever value it was handed. The actual bug is frequently
upstream. The reliable technique is to work **backward**: find where this component gets its
`total` prop, then where *that* value came from, continuing until you reach the actual source of
the data — the real place worth investigating.

## Following Props Upward Through the Component Tree

```jsx
// CartPage.jsx
function CartPage() {
  const { items } = useCart();
  const total = items.reduce((sum, item) => sum + item.price * item.qty, 0);

  return <CartSummary total={total} />;
}
```

One step back, `total` isn't a raw prop — it's *derived* from `items`, which itself comes from a
`useCart()` hook. The bug might not be in this file at all: it might be in how `items` is computed
inside `useCart`, or in the price/quantity data those items were given in the first place. Each
step backward either confirms a value is being computed correctly here (so the bug must be further
upstream) or reveals exactly where it goes wrong.

## Following State Into Its Source: Context, a Store, or a Server Response

```jsx
// useCart.js
export function useCart() {
  const { items } = useContext(CartContext);
  return { items };
}
```

Continuing backward, `items` comes from
[React Context](../../react/global-state-management/context-api.md) — meaning the actual source is
wherever that context's value is set: a
[Redux store](../../react/state-management-using-redux/redux-fundamentals.md), or, further still,
a [server-state fetch](../../react/server-state-and-api-integration/) that populated it from an
API response in the first place. The bug could genuinely be several layers away from the component
where it was first noticed — an incorrect price in the API response itself would explain a wrong
total without any of the rendering or calculation logic being at fault at all.

## Using Search as a Shortcut, Not a Replacement

```
grep -r "useCart" src/
```

A text search for a hook's or variable's name across the codebase is a legitimate way to jump
directly to every place a piece of state is used or set — but it's a *shortcut* for the manual
backward-tracing process above, not a replacement for actually understanding what each usage does.
Blindly editing the first match a search returns, without tracing how it connects to what you
actually saw on screen, risks fixing the wrong thing.

## Common Mistakes

- Assuming the component that renders a wrong value is where the bug lives, without checking
  whether the value it received was already wrong before it got there.
- Stopping the backward trace too early — at the first prop, without continuing to that prop's own
  source — and missing that the real issue is several layers further upstream.
- Using a global text search to jump straight to a change without first understanding, through
  tracing, whether that specific usage is actually the one responsible for the bug.

## Next

Continue to [debugging-existing-code.md](debugging-existing-code.md) to verify a data-flow
hypothesis concretely, using the browser's own debugging tools instead of guesswork.
