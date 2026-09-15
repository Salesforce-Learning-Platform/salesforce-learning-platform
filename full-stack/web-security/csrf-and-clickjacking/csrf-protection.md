# 🎫 CSRF Protection Techniques

## The Synchronizer Token Pattern: Anti-CSRF Tokens

```
1. The SERVER generates an unpredictable, random token, and
   embeds it in the page (a hidden form field, or made available
   to client-side JS)
2. Every STATE-CHANGING request must include this token
3. The SERVER validates the token matches what it issued -
   requests missing a VALID token are REJECTED
```

This is the core, widely-used defense against CSRF, directly per MDN's own documentation: since an
attacker's malicious page has no way to read or predict this token (it can't access the bank's own
page to extract it, due to the browser's same-origin policy), any forged request the attacker's page
submits will be missing a valid token and gets rejected.

## Implementing an Anti-CSRF Token in a Form

```html
<form action="/transfer" method="POST">
  <input type="hidden" name="csrf_token" value="a1b2c3d4-unpredictable-value" />
  <input type="text" name="recipient" />
  <input type="text" name="amount" />
  <button type="submit">Transfer</button>
</form>
```

```js
app.post("/transfer", (req, res) => {
  if (req.body.csrf_token !== req.session.csrfToken) {
    return res.status(403).json({ error: "Invalid CSRF token" });
  }
  // proceed with the transfer
});
```

The attacker's hidden form (from [understanding-csrf.md](understanding-csrf.md)'s example) has no
way to include this token, since it can only be read from the legitimate page itself — a page the
attacker's own site has no access to.

## For JavaScript/API Requests: a Custom Header

```js
fetch("/transfer", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "X-CSRF-Token": csrfToken,
  },
  body: JSON.stringify({ recipient: "joe", amount: "100" }),
});
```

A plain HTML `<form>` submission can't set custom headers — only genuine JavaScript running on the
*legitimate* page can. Requiring a custom header (like `X-CSRF-Token`) for state-changing API
requests is itself a real defense: an attacker's hidden-form-based CSRF attack physically cannot
include a custom header at all.

## `SameSite` Cookies: a Complementary, Browser-Level Defense

```
Set-Cookie: sessionId=abc123; SameSite=Strict; Secure; HttpOnly
```

```
SameSite=Strict → the cookie is NEVER sent on a cross-site
                   request, INCLUDING the attacker's forged form
                   submission - the browser itself refuses to
                   include it
```

This is a genuinely powerful, complementary defense enforced directly by the browser rather than
the application's own code — [cookie-security.md](../cookies-cors-and-transport-security/cookie-security.md),
later in this domain, covers `SameSite` and the other cookie security attributes in full depth.

## A Practical Defense-in-Depth Checklist

```
☐ Anti-CSRF tokens on every state-changing form/request
☐ Custom headers (or JSON content-type) required for API
  requests, since forms can't set these
☐ SameSite=Strict (or Lax) on session cookies
☐ NEVER use GET requests for state-changing actions (GET requests
  can be triggered even more easily, via a simple <img> tag)
```

Directly applying the same [defense-in-depth principle](../the-security-mindset/security-principles.md)
already established earlier in this domain — no single one of these defenses is treated as
individually, completely sufficient; together, they close the gap from multiple independent angles.

## Common Mistakes

- Implementing anti-CSRF tokens for form submissions but forgetting to require them for equivalent
  JSON/API endpoints performing the same state-changing actions.
- Using a `GET` request for any action that changes server state, which can be triggered even more
  trivially than a POST (a plain `<img src="...">` tag is enough).
- Relying on `SameSite` cookies alone without anti-CSRF tokens, missing the flexibility tokens
  provide for legitimate cross-site use cases that `SameSite=Strict` alone would also block.

## ➡️ Next

Continue to [understanding-clickjacking.md](understanding-clickjacking.md) to see a related attack
that also exploits a victim's authenticated session, through an entirely different mechanism.
