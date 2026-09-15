# 🔒 Handling Webhooks Securely

## Why Webhooks Are the Only Trustworthy Confirmation

Recall [creating-and-confirming-a-payment.md](creating-and-confirming-a-payment.md)'s point: a
client-side "it succeeded" message is never fully trustworthy on its own. A **webhook** is the
payment gateway itself — not the client — pushing a real, server-to-server notification the moment
a payment's actual final state is known: `payment_intent.succeeded`, `payment_intent.payment_failed`,
and similar events. This is the only signal the application's own server should treat as
authoritative for marking an order as genuinely paid.

## Registering a Webhook Endpoint

```js
app.post("/webhooks/stripe", express.raw({ type: "application/json" }), (req, res) => {
  // handled below — note express.raw(), NOT express.json()
});
```

A webhook endpoint is registered with the payment gateway (via its dashboard or API), pointing at a
publicly accessible HTTPS URL. Critically, this specific route needs the **raw**, unparsed request
body — `express.raw()`, not the usual `express.json()` — because signature verification (covered
next) needs the exact original bytes, and any parsing/re-serialization would produce a subtly
different byte sequence that fails verification.

## Verifying the Webhook's Signature — Non-Negotiable

```js
app.post("/webhooks/stripe", express.raw({ type: "application/json" }), (req, res) => {
  const signature = req.headers["stripe-signature"];

  let event;
  try {
    event = stripe.webhooks.constructEvent(
      req.body, // the RAW body, per above
      signature,
      process.env.STRIPE_WEBHOOK_SECRET
    );
  } catch (err) {
    return res.status(400).json({ error: `Webhook signature verification failed` });
  }

  // Only reach here if the signature is genuinely valid
  handleStripeEvent(event);
  res.status(200).json({ received: true });
});
```

Without signature verification, **anyone** could send a fake `POST` request claiming to be a
`payment_intent.succeeded` event — a direct path to fraudulently marking unpaid orders as paid.
Stripe signs every webhook using HMAC-SHA256 and a per-endpoint secret; `stripe.webhooks.
constructEvent()` verifies that signature using the endpoint's own secret, throwing if it doesn't
genuinely match. This check is what makes a webhook endpoint trustworthy at all — skipping it turns
the endpoint into an open door.

## Handling the Verified Event

```js
function handleStripeEvent(event) {
  switch (event.type) {
    case "payment_intent.succeeded": {
      const paymentIntent = event.data.object;
      const orderId = paymentIntent.metadata.orderId; // set during creation, per the prior file
      markOrderAsPaid(orderId);
      break;
    }
    case "payment_intent.payment_failed": {
      const orderId = event.data.object.metadata.orderId;
      markOrderAsFailed(orderId);
      break;
    }
  }
}
```

Only *after* signature verification succeeds does the event's actual content get trusted — reading
back the `orderId` stored in `metadata` during creation (per
[creating-and-confirming-a-payment.md](creating-and-confirming-a-payment.md)) to find and update
the correct order.

## Return a `2xx` Response Quickly, Then Do Complex Work Separately

```js
app.post("/webhooks/stripe", express.raw({ type: "application/json" }), (req, res) => {
  // ... verify signature ...
  res.status(200).json({ received: true }); // respond FAST

  queueForProcessing(event); // do anything slower AFTER responding, not before
});
```

Stripe's own guidance is explicit: return a successful status quickly, before any slow or complex
logic — a webhook endpoint that takes too long to respond risks Stripe treating the delivery as
failed and retrying it, potentially processing the same event multiple times.

## Common Mistakes

- Using `express.json()` instead of `express.raw()` for the webhook route, silently breaking
  signature verification since the raw bytes needed for the signature check no longer match.
- Skipping signature verification "to keep things simple," leaving the endpoint open to anyone
  sending a fabricated event.
- Doing slow, complex work (sending confirmation emails, updating multiple systems) *before*
  responding to the webhook, risking a timeout that causes an unnecessary, duplicate retry.

## ➡️ Next

Continue to
[idempotency-and-duplicate-charges.md](idempotency-and-duplicate-charges.md) to prevent a retried
request from ever charging a customer twice.
