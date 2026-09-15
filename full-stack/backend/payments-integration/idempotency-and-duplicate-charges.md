# 🔁 Idempotency and Duplicate Charges

## The Real Risk: a Network Timeout Doesn't Mean "It Failed"

```
Client sends: "charge this customer $79.99"
             ↓
Request reaches the server and genuinely succeeds — the charge happens
             ↓
The RESPONSE gets lost on the way back (a network blip, a timeout)
             ↓
The client, seeing no response, assumes it failed and RETRIES
             ↓
Without protection: the customer is now charged TWICE for one order
```

This is a genuine, real-world risk, not a theoretical edge case: a request can fully succeed on the
server while its response never makes it back to the client — the client has no way to distinguish
"it failed" from "it succeeded, but I didn't hear back," and a naive retry can create a second,
unintended charge.

## Idempotency Keys — Making a Retry Provably Safe

```js
const idempotencyKey = `order-${order.id}-checkout`;

const paymentIntent = await stripe.paymentIntents.create(
  {
    amount: Math.round(amount * 100),
    currency: "usd",
    metadata: { orderId: order.id },
  },
  { idempotencyKey } // Stripe recognizes this SAME key on a retry
);
```

An **idempotency key** is a value the client (or server) generates once, per genuine attempt, and
sends along with the request. If the exact same key is sent again — say, because the original
response was lost and the client retried — the payment gateway recognizes it as the *same* attempt
and simply returns the original result, **without processing the charge a second time**.

## Choosing a Stable, Deterministic Key

```js
// GOOD — the same key every time this specific order's checkout is retried
const idempotencyKey = `order-${order.id}-checkout`;

// WRONG — a new random key every attempt defeats the entire purpose
const idempotencyKey = crypto.randomUUID();
```

The key must be **stable** across genuine retries of the same logical operation — generating a
fresh random key on every attempt (even a retry of the exact same checkout) completely defeats
idempotency's purpose, since the gateway would then see each "retry" as a brand-new, distinct
request.

## Idempotency Isn't Only for Payment Gateways

```js
// The exact same underlying idea, applied to the application's OWN API
app.post("/orders", async (req, res) => {
  const existing = await Order.findOne({ idempotencyKey: req.headers["idempotency-key"] });
  if (existing) return res.status(200).json(existing); // return the SAME result, don't recreate

  const order = await Order.create({ ...req.body, idempotencyKey: req.headers["idempotency-key"] });
  res.status(201).json(order);
});
```

This same principle applies directly to the application's *own* API, not just calls to Stripe — a
`POST /orders` endpoint can accept and store its own idempotency key, checking for an existing
record with that key before creating a new one, protecting against exactly the same
retry-creates-a-duplicate risk for the application's own order-creation logic.

## Common Mistakes

- Generating a new, random idempotency key on every retry attempt instead of a stable one, which
  provides no actual protection at all.
- Assuming idempotency is only relevant to payment gateway API calls — the same retry-duplication
  risk applies to any endpoint whose response might be lost even after the underlying operation
  succeeded.
- Relying solely on client-side "don't double-click the button" UI prevention instead of genuine,
  server-enforced idempotency — a UI-only safeguard doesn't protect against a real network-level
  retry.

## Module Summary

Across this module: a real **payment flow** spans multiple asynchronous steps — order, payment
intent, confirmation, capture — with the payment amount always computed server-side from trusted
data, never accepted from the client (see
[anatomy-of-a-payment-flow.md](anatomy-of-a-payment-flow.md)); **creating and confirming a
payment** splits responsibility between the server (creating the intent, computing the amount) and
the client (confirming with the gateway's own library, keeping raw card data off the application's
server entirely) (see
[creating-and-confirming-a-payment.md](creating-and-confirming-a-payment.md)); **webhooks**,
verified through signature checking with the raw request body, are the only trustworthy source of
truth for a payment's final outcome — never the client's own claim (see
[handling-webhooks-securely.md](handling-webhooks-securely.md)); and **idempotency keys** make a
retried request provably safe, preventing a lost response from ever resulting in a customer being
charged twice.
