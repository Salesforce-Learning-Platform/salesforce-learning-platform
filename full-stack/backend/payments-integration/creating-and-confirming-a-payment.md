# 💰 Creating and Confirming a Payment

## Creating a Payment Intent, Server-Side

```js
import Stripe from "stripe";
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

app.post("/checkout", requireAuth, async (req, res) => {
  const order = await getOrder(req.body.orderId);
  const amount = calculateTotal(order.items); // per anatomy-of-a-payment-flow.md — server-computed

  const paymentIntent = await stripe.paymentIntents.create({
    amount: Math.round(amount * 100), // Stripe expects the SMALLEST currency unit (cents)
    currency: "usd",
    metadata: { orderId: order.id }, // tag the payment with YOUR OWN order reference
  });

  res.json({ clientSecret: paymentIntent.client_secret });
});
```

Creating a payment intent asks the gateway to prepare for a payment of a specific, server-computed
amount. Stripe's own recommendation is to create it as soon as the real amount is known (when
checkout begins), and to **reuse the same intent** if checkout is interrupted and resumed, rather
than creating a new one each time. The `metadata` field attaches the application's own order
reference — making it possible to look the real order back up once a webhook event arrives later.

## The `client_secret` — What the Client Actually Receives

```js
// The client NEVER receives the secret API key. It receives only
// this specific payment's client_secret, scoped to THIS transaction.
res.json({ clientSecret: paymentIntent.client_secret });
```

The **client secret** is a value scoped specifically to this one payment intent — it lets the
client complete *this* payment, and nothing else. Stripe's own guidance is explicit: never log it,
embed it in a URL, or expose it to anyone other than the actual customer completing this specific
checkout — and the page handling it must use HTTPS.

## Confirming the Payment — the Client's Responsibility

```js
// Client-side (using Stripe.js — not covered in depth here, since
// this module focuses on the SERVER-side integration)
const { error } = await stripe.confirmCardPayment(clientSecret, {
  payment_method: { card: cardElement },
});
```

**Confirmation** — actually submitting the customer's real payment details — happens client-side,
using the gateway's own client-side library (Stripe.js), never by sending raw card details to the
application's own server at all. This is a deliberate security boundary: the application's backend
never touches raw card numbers directly, which both simplifies compliance and dramatically reduces
what a server-side vulnerability could ever expose.

## Never Trust the Client's Own "It Succeeded" Signal

```js
// AFTER stripe.confirmCardPayment() resolves without an error, the
// client-side code KNOWS the confirmation attempt didn't immediately
// fail — but this is NOT the same as the server having verified the
// payment actually, finally succeeded.
```

Even after the client-side confirmation call resolves successfully, the *server* still has no
independently-verified confirmation that the payment genuinely succeeded — the browser could close,
the network could drop, or (in a genuinely malicious scenario) a client could simply lie about the
outcome. This is exactly why
[handling-webhooks-securely.md](handling-webhooks-securely.md)'s webhook-based confirmation is the
only trustworthy signal for actually marking an order as paid.

## Common Mistakes

- Sending raw card details to the application's own backend instead of letting the client-side
  library handle confirmation directly — this both violates payment industry compliance
  requirements and unnecessarily exposes sensitive data to the server.
- Marking an order "paid" immediately after the client-side confirmation call resolves, rather than
  waiting for a verified webhook.
- Forgetting to convert a dollar amount into the smallest currency unit (cents) the gateway
  actually expects, causing a payment for 100x too much or too little.

## ➡️ Next

Continue to [handling-webhooks-securely.md](handling-webhooks-securely.md) to receive the actual,
trustworthy confirmation of what happened.
