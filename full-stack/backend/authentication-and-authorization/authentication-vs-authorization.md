# Authentication vs. Authorization

## Two Genuinely Different Questions

**Authentication** answers: "Who is making this request?" **Authorization** answers: "Is this
specific, now-known person allowed to do this specific thing?" These are sequential, dependent
questions — authorization only makes sense *after* authentication has already established who's
asking.

## A Concrete Example

```
1. A user logs in with a username and password.
   → AUTHENTICATION: the server now knows this is genuinely "Alice."

2. Alice tries to delete an order that belongs to a different user, Bob.
   → AUTHORIZATION: the server knows exactly who Alice is, but must
     separately decide whether Alice is ALLOWED to delete Bob's order
     (the answer here should be no).
```

Authentication happens once, establishing identity. Authorization happens on **every** subsequent
action that needs a permission check, using that already-established identity to decide what's
allowed.

## Why the `401`/`403` Distinction Directly Maps to This

Recall [REST's status-codes.md](../rest-api-design/status-codes.md)'s coverage of `401` vs. `403`:

| Status | Question it answers | Example |
|---|---|---|
| `401 Unauthorized` | An **authentication** failure — who even are you? | No login token sent at all, or an invalid/expired one |
| `403 Forbidden` | An **authorization** failure — I know who you are, but no | Alice, correctly authenticated, tries to delete Bob's order |

This is precisely why the distinction matters practically, not just academically — returning the
wrong one of these two codes actively misleads a client about what actually went wrong (whether to
prompt a re-login, or to simply show a "not allowed" message).

## Both Are Needed, Neither Replaces the Other

An API that only checks authentication ("is this a valid, logged-in user?") but never checks
authorization would let any logged-in user do *anything* — delete any other user's data, view any
other user's private information. Real backend security requires both layers, checked separately:
first establish identity, then, for every sensitive action, separately verify that identity is
actually permitted to perform it.

## Where Each Fits in an Express App

```js
app.use(authenticate);              // AUTHENTICATION — runs on every request,
                                     // establishes req.user

app.delete("/orders/:id", authorize("orders:delete"), (req, res) => {
  // AUTHORIZATION — runs only on this specific route, checks whether
  // req.user (already known) is allowed to do THIS specific thing
});
```

This structure — one authentication middleware applied broadly, layered with authorization checks
applied per-route or per-action — is the pattern
[protecting-routes.md](protecting-routes.md) and
[role-based-access-control.md](role-based-access-control.md) build out concretely.

## Common Mistakes

- Using `401` when the real problem is authorization (a logged-in user lacking permission) — the
  correct code there is `403`.
- Checking authentication only, and assuming that's sufficient security — it only confirms who
  someone is, not what they're allowed to do.
- Performing an authorization check using data the client sent directly, rather than the server's
  own already-authenticated `req.user` — a client-supplied "I am an admin" claim can never be
  trusted on its own.

## Next

Continue to [password-hashing.md](password-hashing.md) to see how authentication actually verifies
a password safely, without ever storing it in a readable form.
