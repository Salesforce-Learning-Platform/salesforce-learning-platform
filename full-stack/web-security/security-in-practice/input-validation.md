# ✅ Input Validation

## The Principle That's Appeared Throughout This Entire Domain

Nearly every module in this domain has touched this same underlying idea from a different angle —
[Injection Attacks](../injection-attacks/preventing-injection-attacks.md)'s structural separation,
[XSS](../cross-site-scripting-xss/preventing-xss.md)'s output escaping,
[SSRF](../server-side-attacks/server-side-request-forgery-ssrf.md)'s allowlisting,
[path traversal](../server-side-attacks/path-traversal.md)'s resolved-path validation. This file
names the unifying principle directly: **never trust data crossing a trust boundary until it's been
genuinely validated.**

## Validating at the Boundary, With a Real Schema

```js
import { z } from "zod";

const CreateOrderSchema = z.object({
  productId: z.string().uuid(),
  quantity: z.number().int().min(1).max(100),
  shippingAddress: z.string().min(10).max(500),
});

app.post("/orders", (req, res) => {
  const result = CreateOrderSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(400).json({ error: "Invalid request", details: result.error.issues });
  }
  // result.data is now genuinely validated - safe to use
});
```

This is directly the same [Zod validation pattern](../../artificial-intelligence/schema-validation-with-zod/defining-a-validation-schema-using-zod.md)
already established in this repository's AI Engineering domain for validating AI-generated data —
applied here to its original, more familiar use: validating data arriving from an actual HTTP
request, exactly the pattern this repository's own
[REST API Design](../../backend/rest-api-design/request-validation.md) module covers from the
implementation side.

## Allowlist Validation, Not Denylist Filtering

```
DENYLIST (block known-bad patterns): "reject input containing
  <script>, or ../, or ; " - INCOMPLETE by nature, since it can
  only block patterns someone THOUGHT to anticipate.

ALLOWLIST (accept only known-good patterns): "accept ONLY a valid
  UUID," "accept ONLY these specific enum values" - structurally
  cannot be bypassed by an unanticipated variant, since anything
  not explicitly matching the allowed shape is simply rejected.
```

This is the exact same principle already applied specifically to
[SSRF](../server-side-attacks/server-side-request-forgery-ssrf.md)'s host validation earlier in
this domain, now stated as a general rule: an allowlist is structurally more robust than a denylist
for nearly every validation scenario, because it doesn't depend on anticipating every possible
malicious variant in advance.

## Validating Every Trust Boundary, Not Just the Obvious One

```
- Request BODY (per the example above)
- URL/query PARAMETERS
- HTTP HEADERS (a client can set ANY header value)
- File UPLOADS (per File Upload Security, earlier in this
  domain — content, not just metadata)
- Data from THIRD-PARTY APIs (still external, still untrusted,
  even though it didn't come from your OWN application's users)
```

This last point is genuinely easy to overlook: data from a third-party API is still crossing a
trust boundary into the application — it deserves the same validation discipline as data from a
user's own request, not an implicit pass simply because it originated from another "trusted"
service.

## Common Mistakes

- Validating only the request body while trusting headers, query parameters, or third-party API
  responses without the same scrutiny.
- Relying on a denylist of known-bad patterns instead of an allowlist of known-good ones, leaving
  the validation incomplete against any pattern not specifically anticipated.
- Validating on the client side only, forgetting that a client-side check can always be bypassed by
  sending a request directly to the API, skipping the frontend entirely.

## ➡️ Next

Continue to [security-testing.md](security-testing.md) to see how these defenses are actually
verified to be working, rather than simply assumed to be correct.
