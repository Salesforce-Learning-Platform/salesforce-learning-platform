# JSON Web Tokens (JWT)

## A Stateless Alternative to Sessions

[sessions.md](sessions.md) kept authentication state on the server, with the client holding only a
reference (a session ID) to it. A **JWT (JSON Web Token)** inverts this: it holds the actual
authentication data itself, cryptographically signed, requiring **no server-side storage at all**
to verify.

## The Three Parts

```
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiI0MiJ9.4Y7Xk...
└─── HEADER ─────┘ └────── PAYLOAD ──────┘ └ SIGNATURE ┘
```

A JWT is three Base64URL-encoded parts, separated by dots:

- **Header**: which algorithm was used to sign the token (e.g., `HS256`).
- **Payload**: the actual claims — data about the user, like `userId` — plus standard fields like
  an expiration time.
- **Signature**: computed by signing the header and payload together with a secret key, known only
  to the server.

## What the Signature Actually Guarantees

```js
import jwt from "jsonwebtoken";

const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET, { expiresIn: "1h" });
```

The signature lets the server later **verify** that a token wasn't tampered with — if even one
character of the payload changes, re-computing the signature with the secret produces a completely
different result, so a forged or modified token is immediately detectable. This is the entire
mechanism that makes a JWT trustworthy without needing to look anything up in a database.

## The Payload Is NOT Encrypted — Only Signed

```js
// Anyone can decode and READ a JWT's payload — signing prevents
// tampering, it does NOT prevent reading
const payload = JSON.parse(atob(token.split(".")[1]));
console.log(payload); // { userId: "42", iat: ..., exp: ... } — fully readable
```

This is the single most important, frequently misunderstood fact about JWTs: **signing is not
encryption**. Anyone holding a JWT — including the end user themselves, or anyone intercepting it —
can trivially decode and read its payload. A JWT should **never** contain sensitive data (a
password, a credit card number) in its payload; it should only contain data that's safe for the
holder of the token to see.

## Issuing and Verifying a Token in Express

```js
app.post("/login", async (req, res) => {
  // ... verify credentials via bcrypt.compare
  const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET, { expiresIn: "1h" });
  res.json({ token });
});
```

```js
// The client sends the token back in an Authorization header on later requests:
// Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...

function verifyToken(req, res, next) {
  const token = req.headers.authorization?.split(" ")[1];
  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET);
    next();
  } catch {
    res.status(401).json({ error: "Invalid or expired token" });
  }
}
```

`jwt.verify()` re-checks the signature against the server's secret — if it's valid, the payload can
be trusted as genuinely issued by this server and unmodified since. No database lookup is needed at
all to establish this, which is JWT's core scalability advantage over sessions.

## The Real Cost: Revocation Is Genuinely Hard

```
A session can be revoked instantly — delete the record, and the
session ID immediately stops working.

A JWT, once issued, remains cryptographically valid until it EXPIRES,
regardless of what the server "wants" — there's no built-in way to
invalidate one early.
```

This is JWT's central tradeoff against sessions: a stolen or compromised JWT stays usable until its
`expiresIn` naturally elapses, since the server has no record of having issued it to revoke in the
first place. Real systems mitigate this with deliberately **short** expiration times, often paired
with a separate, revocable refresh-token mechanism — a more advanced pattern beyond this module's
scope, but essential to know exists for anyone building production authentication.

## Common Mistakes

- Putting sensitive data (a password, private personal information) directly into a JWT's payload,
  assuming signing keeps it hidden — it doesn't; only tampering is prevented, not reading.
- Using an overly long expiration time on a JWT with no revocation strategy at all, leaving a large
  window during which a stolen token remains fully usable.
- Storing the JWT secret directly in source code instead of an environment variable (per
  [environment-variables.md](../nodejs-core-concepts/environment-variables.md)) — anyone with the
  secret can forge arbitrary valid tokens.

## Next

Continue to [protecting-routes.md](protecting-routes.md) to apply either authentication mechanism
consistently across an Express application's routes.
