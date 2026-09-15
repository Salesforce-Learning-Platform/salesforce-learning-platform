# 🎟️ Session Attacks

## The Equivalent Risks for Cookie-Based Sessions

[jwt-security.md](jwt-security.md) covered token-based authentication attacks. Traditional,
cookie-based session authentication has its own, related attack patterns — **session fixation** and
**session hijacking** — both targeting the session identifier itself rather than any cryptographic
weakness.

## Session Hijacking: Stealing an Existing, Valid Session

```
An attacker OBTAINS a victim's ALREADY-VALID session identifier -
via XSS (per Cross-Site Scripting, earlier in this domain), a
network eavesdropper on an unencrypted connection, or simply
finding it exposed somewhere (a log file, a URL parameter).
```

```
With that stolen session ID, the attacker's OWN browser is now
treated as the VICTIM by the server - no password, no login
required at all, just presenting a valid, stolen identifier.
```

This is exactly why [secure-cookie-attributes.md](../cookies-cors-and-transport-security/secure-cookie-attributes.md)'s
`HttpOnly` (blocking XSS-based theft) and `Secure` (blocking network interception) attributes,
covered earlier in this domain, matter so directly — they close the two most common actual
mechanisms by which a session identifier gets stolen in the first place.

## Session Fixation: Forcing a KNOWN Session ID

```
1. Attacker visits the target site THEMSELVES, obtaining a
   VALID (but not yet authenticated) session ID: "sess-abc123"
2. Attacker tricks the VICTIM into using THAT SAME session ID
   (e.g. via a crafted link: https://myapp.com/login?sessionId=sess-abc123)
3. Victim LOGS IN, using the session ID the attacker ALREADY KNOWS
4. The attacker's OWN browser, still holding "sess-abc123", is
   now AUTHENTICATED AS THE VICTIM too
```

This is a genuinely distinct mechanism from hijacking — the attacker never actually steals anything
mid-session; they pre-establish a *known* session identifier and trick the victim into
authenticating under it, effectively sharing their own session with the victim without ever needing
to intercept anything.

## The Fix: Regenerate the Session ID on Login

```js
app.post("/login", async (req, res) => {
  const user = await authenticateUser(req.body);
  req.session.regenerate((err) => {      // ISSUE A NEW session ID
    req.session.userId = user.id;
    res.redirect("/dashboard");
  });
});
```

This is the direct, structural fix for session fixation: **regenerating** the session identifier at
the exact moment of successful login means any session ID an attacker pre-established (per the
fixation attack above) is simply discarded and replaced — the attacker's pre-known ID never actually
becomes the victim's real, authenticated session ID at all.

## Detecting Anomalous Session Use

```
A session SUDDENLY used from a genuinely different IP address,
geographic location, or device/browser fingerprint than its
recent, normal pattern is a real, practical signal worth flagging
or requiring re-authentication for.
```

This is a genuinely useful, defense-in-depth layer beyond the structural fixes above — even a
successfully stolen session identifier becomes harder to exploit undetected when its actual usage
pattern is being monitored for anomalies.

## Common Mistakes

- Never regenerating the session ID at login, leaving an application genuinely vulnerable to session
  fixation even with otherwise strong authentication.
- Accepting a session ID supplied via a URL parameter (rather than only a cookie), which makes
  fixation trivially easy to set up via a simple, shareable link.
- Relying solely on session-identifier secrecy with no anomaly detection, missing a real, practical
  layer that can catch a theft even after it's already occurred.

## ➡️ Next

Continue to [brute-force-attacks.md](brute-force-attacks.md) to see attacks that target the
authentication *process* itself, rather than an already-established session.
