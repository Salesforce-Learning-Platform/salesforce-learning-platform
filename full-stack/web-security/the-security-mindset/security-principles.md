# 🏛️ Core Security Principles

## Timeless Principles Behind Every Specific Defense

The OWASP Top 10 categories from
[understanding-web-security.md](understanding-web-security.md) change over time as the industry's
real, observed risks shift. The principles behind *defending* against them are far more stable —
these four ideas underlie nearly every specific defense this domain's later modules cover.

## Never Trust User Input

```
EVERY piece of data originating outside the application's own
trusted code - form input, URL parameters, HTTP headers, even
data from a THIRD-PARTY API - must be treated as potentially
hostile until validated.
```

This is directly the same principle already established in
[never-trust-ai-output-without-validation.md](../../artificial-intelligence/schema-validation-with-zod/never-trust-ai-output-without-validation.md),
earlier in this repository's AI Engineering domain — data crossing a trust boundary needs validation
regardless of source, whether that source is a user, an AI model, or (as this domain will cover) a
deliberately malicious attacker.

## Least Privilege

```
Every USER, PROCESS, or SERVICE should have ONLY the minimum
access genuinely required to do its job - nothing more.
```

```
A backend service account that can READ and WRITE the orders
table, but has NO permission to drop tables or access unrelated
customer payment data it never actually needs.
```

This principle is what limits the *damage* a single compromised credential or vulnerability can
actually cause — if a specific account is compromised, least privilege ensures the resulting damage
is bounded by what that one account could ever legitimately do, rather than unlimited.

## Defense in Depth

```
A SINGLE security control, no matter how strong, can fail or be
bypassed - MULTIPLE, INDEPENDENT layers of defense mean a single
failure doesn't lead directly to a full compromise.
```

```
Layer 1: input validation (rejects obviously malformed data)
Layer 2: parameterized queries (prevents injection even if
  Layer 1 somehow missed something)
Layer 3: least-privilege database credentials (limits the DAMAGE
  even if Layers 1 and 2 both somehow failed)
```

This is genuinely the opposite of relying on one single, "bulletproof" defense — real security
comes from multiple, independent layers, each catching what the others might miss, so no single
point of failure results in total compromise.

## Fail Securely

```
When something GOES WRONG (an error, an unexpected exception),
the SAFE, secure state should be the DEFAULT outcome - not
accidentally granting broader access as a side effect of a
failure.
```

```js
// INSECURE - a bug here accidentally grants access
function checkAccess(user) {
  try {
    return user.hasPermission("admin");
  } catch (err) {
    return true; // NEVER do this - failure should NEVER default to granting access
  }
}

// SECURE - failure defaults to the safe, restrictive outcome
function checkAccess(user) {
  try {
    return user.hasPermission("admin");
  } catch (err) {
    return false; // an error means access is DENIED, not granted
  }
}
```

This is a genuinely important, concrete principle: an error-handling path should never accidentally
become a path to broader, unintended access — the safe default in any failure case is always to
deny, not to grant.

## Common Mistakes

- Trusting data because it "came from our own frontend" — an attacker can send arbitrary requests
  directly to a backend API, entirely bypassing the frontend's own validation logic.
- Granting broad, convenient permissions "just in case they're needed later" instead of the actual
  minimum required right now, violating least privilege for the sake of convenience.
- Writing error-handling logic that defaults to permissive behavior on failure, turning an
  unrelated bug into an unintended security hole.

## ➡️ Next

Continue to [threat-modeling-basics.md](threat-modeling-basics.md) to see a structured process for
applying these principles to a specific, real application.
