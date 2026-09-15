# 💳 Payments Integration

## Purpose

Every backend module so far has managed the application's own data. This module covers something
genuinely different: integrating with an **external, real-money payment gateway** — where
correctness isn't just about a clean API, but about handling asynchronous confirmation, security,
and failure modes where getting it wrong has real financial consequences.

## 🎯 Learning Objectives

- Explain the real anatomy of a payment flow: creating an order, confirming payment, and capturing
  it.
- Create and confirm a payment using a real payment gateway's server-side API.
- Explain why webhooks — not just the client's confirmation — are essential for a genuinely
  reliable payment flow.
- Verify a webhook's signature correctly, and explain why this is non-negotiable.
- Apply idempotency to prevent duplicate charges.

## 📋 Prerequisites

- [REST API Design](../rest-api-design/) and
  [Database Design and Modeling](../database-design-and-modeling/) — this module persists order
  and payment state using patterns already covered there.

## 📂 Files in This Module

| File | Covers |
|---|---|
| [anatomy-of-a-payment-flow.md](anatomy-of-a-payment-flow.md) | Orders, payment intents, confirmation, and capture — the real shape of a payment |
| [creating-and-confirming-a-payment.md](creating-and-confirming-a-payment.md) | The server-side flow: creating a payment, passing a client secret, confirming |
| [handling-webhooks-securely.md](handling-webhooks-securely.md) | Why webhooks matter, and verifying a webhook's signature correctly |
| [idempotency-and-duplicate-charges.md](idempotency-and-duplicate-charges.md) | Preventing a retried request from charging a customer twice |

## 🔍 When to Deep-Dive vs. Skim

Deep-dive [handling-webhooks-securely.md](handling-webhooks-securely.md) — an unverified webhook
endpoint is a genuine, serious security hole (anyone could fake a "payment succeeded" event), and
precisely understanding signature verification is non-negotiable for handling real payments safely.

## ✅ Quick Knowledge Check

<details>
<summary>Is it safe to mark an order as "paid" purely because the client-side checkout page said the payment succeeded?</summary>

No — a client-side success message can be spoofed, or the browser could close before truly
confirming. The server should only trust a **verified webhook event** from the payment gateway
itself as the authoritative signal that a payment actually succeeded. See
[handling-webhooks-securely.md](handling-webhooks-securely.md).

</details>

<details>
<summary>If a client's payment request times out and retries, could the customer be charged twice?</summary>

Without an idempotency key, yes — this is a genuine, real risk. Providing a stable idempotency key
per checkout attempt lets the payment gateway recognize a retried request as the same one, safely
returning the original result instead of creating a second charge. See
[idempotency-and-duplicate-charges.md](idempotency-and-duplicate-charges.md).

</details>

## 📚 References

- Stripe, [The Payment Intents API](https://docs.stripe.com/payments/payment-intents)
- Stripe, [Receive Stripe events in your webhook endpoint](https://docs.stripe.com/webhooks)

## ➡️ Continue Your Learning Path

Continue to the [Backend Testing module](../backend-testing/) to properly test the payment flow
and every other endpoint built throughout this domain.
