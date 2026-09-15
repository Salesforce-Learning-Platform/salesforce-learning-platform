# ⚠️ Common CORS Misconfigurations

## Misconfigured CORS: Weakening a Protection Into a Vulnerability

[understanding-cors.md](understanding-cors.md) established CORS as a deliberate, narrow relaxation
of the browser's same-origin policy. A *misconfigured* CORS setup does the opposite of what it's
meant to — it can turn a legitimate protection into a genuine hole, letting a malicious site's
JavaScript read data and act on behalf of a victim it should never have access to.

## Mistake 1: The Wildcard + Credentials Combination

```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
```

```
Per MDN's own documentation, browsers ACTIVELY REJECT this exact
combination - it's not merely bad practice, it's a configuration
the browser itself refuses to honor, specifically because it
would let ANY origin make fully authenticated, cookie-carrying
requests.
```

This is a genuinely important, protective browser behavior — the specification itself forbids
`*` combined with credentials, precisely because it would defeat the entire purpose of requiring
credentialed requests to specify a genuine, deliberate origin.

## Mistake 2: Dynamically Reflecting the Request's Own Origin

```js
// VULNERABLE - blindly trusts and echoes back WHATEVER origin
// sent the request
app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", req.headers.origin);
  res.header("Access-Control-Allow-Credentials", "true");
  next();
});
```

```
This code technically AVOIDS the literal "*" + credentials
combination the browser rejects - but achieves the EXACT SAME
effect: it grants EVERY origin credentialed access, one at a
time, defeating the entire purpose of CORS.
```

This is a genuinely common, real-world mistake — it looks superficially like a properly-scoped CORS
configuration (a specific origin, not a wildcard), but functionally grants unrestricted access to
literally any site that sends a request, since the server simply echoes back whatever `Origin`
header it received without ever actually checking it against a real allowlist.

## The Fix: an Explicit, Validated Allowlist

```js
const allowedOrigins = ["https://myapp.com", "https://admin.myapp.com"];

app.use((req, res, next) => {
  const origin = req.headers.origin;
  if (allowedOrigins.includes(origin)) {
    res.header("Access-Control-Allow-Origin", origin);
    res.header("Access-Control-Allow-Credentials", "true");
  }
  next();
});
```

This is the actual, correct fix: an explicit list of genuinely trusted origins, checked before ever
echoing anything back — this directly applies
[least privilege](../the-security-mindset/security-principles.md), earlier in this domain, granting
cross-origin, credentialed access only to the specific origins that genuinely need it.

## Mistake 3: Overly Permissive `Access-Control-Allow-Headers`

```http
Access-Control-Allow-Headers: *
```

An overly broad allowed-headers configuration, while less immediately severe than the credentials
issue, still widens the effective attack surface unnecessarily — per
[attack-surface.md](../the-security-mindset/attack-surface.md)'s principle from earlier in this
domain, allowing only the specific headers a legitimate cross-origin client genuinely needs is the
more disciplined, correct approach.

## Verifying a Real CORS Configuration

```
1. Confirm Access-Control-Allow-Origin is NEVER "*" for any
   endpoint that also sets Access-Control-Allow-Credentials
2. Confirm the origin-checking logic uses a REAL allowlist, not a
   blind echo of the request's own Origin header
3. Confirm Access-Control-Allow-Headers/Methods list only what's
   genuinely needed, not a blanket wildcard
```

## Common Mistakes

- Dynamically reflecting the request's `Origin` header back unconditionally, functionally
  equivalent to a wildcard for credentialed requests despite appearing more specific.
- Assuming CORS misconfiguration is "just" a development annoyance to work around quickly, rather
  than a genuine security boundary worth configuring correctly and deliberately.
- Testing CORS configuration only from the application's own legitimate frontend, never verifying
  that a genuinely untrusted origin is actually, correctly rejected.

## ➡️ Next

Continue to [https-and-tls.md](https-and-tls.md) to see the transport-layer security protecting
every request this module has covered, in practice.
