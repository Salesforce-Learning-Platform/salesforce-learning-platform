# 🚫 Preventing Clickjacking with Frame Protection

## The Direct Fix: Refuse to Be Framed at All

[understanding-clickjacking.md](understanding-clickjacking.md)'s entire attack depends on one
precondition: the target page can be loaded inside an attacker's `<iframe>`. The most direct,
effective defense is simply refusing to allow that at all.

## The `X-Frame-Options` Header

```http
X-Frame-Options: DENY
```

```
DENY        → the page can NEVER be framed, by ANY site,
              including the site's own other pages

SAMEORIGIN  → the page can be framed ONLY by pages on the SAME
              origin - blocks every cross-site framing attempt
```

Per MDN's own documentation, this header instructs the *browser itself* to refuse to render the
page inside a frame at all when the condition isn't met — the protection happens at the browser
level, before the attacker's overlay trick from
[understanding-clickjacking.md](understanding-clickjacking.md) ever has a chance to work.

## Setting It in Express, With Helmet

```js
import helmet from "helmet";

app.use(helmet({
  xFrameOptions: { action: "sameorigin" },
}));
```

[Helmet](../security-in-practice/), covered in full later in this domain, is a widely-used Express
middleware that sets this and several other security headers with sensible defaults — this is a
genuinely common, practical way this specific header actually gets configured in a real Node.js
application.

## The Modern Alternative: CSP's `frame-ancestors`

```http
Content-Security-Policy: frame-ancestors 'self'
```

This directive, part of the same [Content Security Policy](../cross-site-scripting-xss/preventing-xss.md)
mechanism already covered for XSS prevention earlier in this domain, provides finer-grained control
than `X-Frame-Options` — for instance, allowing a page to be framed by a specific *list* of trusted
origins, something `X-Frame-Options` alone cannot express. MDN's own guidance is direct: this is
the currently preferred, more modern approach, though setting both together maximizes compatibility
across a wider range of browsers.

## A Critical Configuration Detail

```html
<!-- This does NOT work - X-Frame-Options MUST be an HTTP header -->
<meta http-equiv="X-Frame-Options" content="deny">
```

This is a genuinely important, easy-to-miss detail directly from MDN's own documentation:
`X-Frame-Options` has no effect when set via an HTML `<meta>` tag — it must be sent as a real HTTP
response header, or the browser silently ignores it entirely, leaving the page just as vulnerable
as if no protection had been configured at all.

## When a Page Genuinely Needs to Be Framed

```
For the RARE, legitimate case where embedding is genuinely
needed (a widget meant to be embedded on partner sites):
  frame-ancestors https://trusted-partner.example.com
```

The default should always be the most restrictive option that still supports genuine, legitimate use
cases — explicitly allowlisting only specific, trusted origins when embedding is truly needed, rather
than leaving framing open to any site by default.

## Common Mistakes

- Setting `X-Frame-Options` via an HTML `<meta>` tag instead of a real HTTP header, silently
  providing zero actual protection.
- Leaving frame protection unconfigured entirely, relying on the (false) assumption that clickjacking
  is too obscure or unlikely to be worth defending against.
- Using an overly permissive `frame-ancestors` policy (or omitting it) for a page with no genuine
  legitimate need to ever be embedded elsewhere.

## Module Summary

Across this module: **CSRF** exploits a victim's authenticated session by tricking their browser
into automatically including valid session credentials on a forged, attacker-initiated request —
verified against MDN's own official CSRF documentation (see
[understanding-csrf.md](understanding-csrf.md)); **CSRF protection** combines anti-CSRF tokens (the
synchronizer token pattern), custom headers for API requests, and `SameSite` cookies as
complementary, defense-in-depth layers (see [csrf-protection.md](csrf-protection.md));
**clickjacking** exploits the same authenticated-session precondition through an entirely different
mechanism — misdirecting a victim's genuine click onto a hidden, legitimately embedded element (see
[understanding-clickjacking.md](understanding-clickjacking.md)); and **frame protection**, via
`X-Frame-Options` and CSP's `frame-ancestors` directive (verified against MDN's official
documentation, including the critical HTTP-header-only requirement), directly prevents the
embedding clickjacking depends on in the first place.
