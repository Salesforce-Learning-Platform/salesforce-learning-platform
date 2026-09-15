# 🧬 Anatomy of a Payment Flow

## Not a Single Request — a Real, Multi-Step Process

```
1. Customer reaches checkout with a real order amount
2. Server creates a PAYMENT INTENT for that exact amount
3. Client CONFIRMS the payment (entering card details, or an
   equivalent payment method)
4. The payment gateway processes it — possibly requiring
   additional authentication (per SCA regulations)
5. The gateway sends a WEBHOOK to the server confirming the
   final outcome (succeeded or failed)
6. The server updates the order's status based on that webhook —
   NOT based on what the client claimed happened
```

Unlike every prior REST endpoint in this domain (a single request, a single response), a real
payment is a genuine multi-step process spanning the server, the client, the payment gateway, and
(often) the customer's bank — with the final, authoritative outcome arriving **asynchronously**,
after the original request has already completed.

## Why "Order," "Payment," and "Capture" Are Genuinely Different Concepts

- **Order** — the application's own record of what's being purchased and for how much (per
  [Database Design and Modeling](../database-design-and-modeling/)'s modeling principles) —
  exists entirely within the application's own database.
- **Payment (Intent)** — the payment gateway's own record of an attempt to collect a specific
  amount — created on the gateway's servers, tracked through its own lifecycle
  (`requires_payment_method` → `requires_confirmation` → `processing` → `succeeded`/`failed`).
- **Capture** — actually collecting the authorized funds. Some flows separate **authorization**
  (confirming funds are available and reserved) from **capture** (actually collecting them) — useful
  when a business needs to confirm something else (like inventory availability) before actually
  charging the customer.

## Why the Payment Amount Belongs on the Server, Never the Client

```js
// DANGEROUS — trusting a client-supplied amount directly
app.post("/checkout", (req, res) => {
  createPaymentIntent(req.body.amount); // a malicious client could send ANY amount
});

// CORRECT — the server computes the real amount from its own trusted data
app.post("/checkout", async (req, res) => {
  const order = await getOrder(req.body.orderId);
  const amount = calculateTotal(order.items); // computed server-side, from trusted data
  createPaymentIntent(amount);
});
```

This is exactly [request-validation.md](../rest-api-design/request-validation.md)'s "never trust
client input" principle, applied at maximum stakes: the actual amount charged must always be
computed by the server from its own trusted order data, never accepted directly from whatever the
client happens to send.

## Common Mistakes

- Trusting a client-supplied payment amount directly, opening the door to a customer paying far
  less than the real order total.
- Treating a payment as a single, atomic request/response, rather than the genuinely multi-step,
  partially-asynchronous process it actually is.
- Confusing authorization (funds reserved) with capture (funds actually collected) — some
  integrations genuinely separate the two steps, and conflating them can lead to charging (or
  failing to charge) a customer at the wrong moment.

## ➡️ Next

Continue to
[creating-and-confirming-a-payment.md](creating-and-confirming-a-payment.md) to implement this
flow concretely, server-side.
