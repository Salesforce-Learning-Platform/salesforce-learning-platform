# Session-Based Authentication

## The Problem: HTTP Doesn't Remember Anything

Recall [REST's rest-principles.md](../rest-api-design/rest-principles.md)'s coverage of
statelessness: each HTTP request is independent, carrying no memory of any previous one. Without
some mechanism to bridge that gap, a server would have no way to know that a request arriving right
after a successful login is coming from the same, now-authenticated user.

## How Session-Based Authentication Bridges the Gap

```
1. User logs in with correct credentials (per password-hashing.md).
2. Server creates a SESSION — a record, stored server-side, saying
   "session abc123 belongs to user Alice."
3. Server sends the client a cookie containing just the session ID
   (abc123), not any actual user data.
4. Every subsequent request automatically includes that cookie.
5. Server looks up abc123 in its session store to identify the user.
```

**Session-based authentication** keeps the actual authentication state on the **server**, indexed
by a session ID the client holds in a cookie. The cookie itself carries almost no information —
just enough to look the real session data up.

## Setting the Cookie in Express

```js
app.post("/login", async (req, res) => {
  // ... verify credentials via bcrypt.compare, per password-hashing.md
  req.session.userId = user.id; // a session middleware (e.g. express-session)
                                  // handles persisting this server-side
  res.json({ message: "Logged in" });
});
```

A session middleware (commonly `express-session`) manages creating the session record, generating
the session ID, and setting/reading the cookie automatically — a route handler typically just
assigns data onto `req.session`.

## Cookie Security Attributes

```
Set-Cookie: sessionId=abc123; HttpOnly; Secure; SameSite=Strict
```

| Attribute | Protects against |
|---|---|
| `HttpOnly` | Cross-site scripting (XSS) — the cookie is invisible to JavaScript running on the page, so injected malicious script can't steal it |
| `Secure` | Man-in-the-middle attacks — the cookie is only ever sent over HTTPS, never plain HTTP |
| `SameSite=Strict`/`Lax` | Cross-site request forgery (CSRF) — restricts whether the cookie is sent along with requests originating from other sites |

A session cookie holding real authentication power should set **all three** — this is genuinely
non-negotiable for a production authentication cookie, not an optional hardening step.

## The Real Tradeoff vs. Token-Based Auth (Covered Next)

| | Sessions | JWT (next file) |
|---|---|---|
| Where the state lives | Server (a session store) | Entirely inside the token itself |
| Scaling across multiple servers | Needs a shared session store (e.g., Redis) | Naturally stateless — any server can verify it |
| Revoking access immediately | Trivial — delete the session record | Genuinely hard — a valid, unexpired token can't be "un-issued" |

Sessions keep the server in full, immediate control (revoking access is as simple as deleting a
record) at the cost of needing shared server-side storage to scale across multiple server
instances — precisely the tradeoff [jwt.md](jwt.md) approaches from the opposite direction.

## Common Mistakes

- Omitting `HttpOnly`, `Secure`, or `SameSite` on an authentication cookie, leaving it exposed to
  exactly the attack each attribute exists to prevent.
- Storing sessions only in a single server's memory in a multi-server deployment — a user's session
  would only exist on whichever server happened to handle their login, breaking authentication the
  moment a later request lands on a different server.
- Storing sensitive user data directly in the cookie itself, rather than just a session ID pointing
  at server-side data — defeating the purpose of keeping sensitive state off the client.

## Next

Continue to [jwt.md](jwt.md) to see the alternative, stateless approach to authentication.
