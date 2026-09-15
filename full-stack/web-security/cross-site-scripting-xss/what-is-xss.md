# 🎭 What Is XSS?

## Injection, Targeting the Browser Instead of a Server

[Injection Attacks](../injection-attacks/), the previous module, covered untrusted input reaching a
server-side interpreter (a database, a shell). **Cross-Site Scripting (XSS)** is the same
fundamental pattern — untrusted input executed as instructions rather than treated as inert data —
but targeting a genuinely different interpreter: the *victim's own browser*.

## The Core Mechanism

```
An application takes untrusted input and renders it into a page's
HTML WITHOUT properly escaping it - if that input contains a
<script> tag (or another way to execute JavaScript), the BROWSER
executes it as genuine, real code, running with the SAME
privileges as the actual website's own legitimate JavaScript.
```

```html
<!-- A comment field rendering user input directly, unescaped -->
<div class="comment">Great post! <script>steal(document.cookie)</script></div>
```

If this comment is ever rendered into a page without escaping, the browser doesn't display the
`<script>` tag as text — it *executes* it, exactly as if it were part of the site's own legitimate
code.

## Why This Is Genuinely Severe

```
XSS-injected JavaScript runs with the SAME origin, and therefore
the SAME privileges, as the site's own real code - it can:
  - read cookies and session tokens (enabling session hijacking)
  - make authenticated requests AS the logged-in victim
  - modify the page's content the victim sees, arbitrarily
  - capture keystrokes, form submissions, anything on the page
```

This is the real severity of XSS: it isn't merely "displaying unwanted text" — the injected code
runs with full access to everything the legitimate page's own JavaScript can do, including reading
authentication tokens and performing actions *as the actual logged-in user*.

## Three Types, Covered in This Module

```
REFLECTED XSS  → the malicious script comes back in an IMMEDIATE
                  server response (covered in reflected-xss.md)

STORED XSS     → the malicious script is PERSISTED on the server
                  (a database, a comment) and served to EVERY
                  future visitor (covered in stored-xss.md)

DOM-BASED XSS  → the vulnerability exists entirely CLIENT-SIDE,
                  with no server involvement at all (covered in
                  dom-based-xss.md)
```

Each type shares the identical underlying root cause — unescaped, attacker-controlled content
reaching the browser's rendering or script-execution engine — but differs in exactly *where* that
untrusted content actually originates and travels through.

## Common Mistakes

- Assuming XSS is a "minor" issue because it "just" displays unexpected content, missing that
  injected JavaScript has full access to cookies, session tokens, and the ability to act as the
  logged-in user.
- Believing a site is safe from XSS "because we don't store user-generated content," missing that
  reflected and DOM-based XSS require no persistent storage at all.
- Confusing XSS with CSRF (covered in the next module) — XSS executes attacker code in the victim's
  browser; CSRF tricks the victim's browser into making an unwanted, authenticated request.

## ➡️ Next

Continue to [reflected-xss.md](reflected-xss.md) to see the first, and often easiest to
demonstrate, XSS variant in concrete detail.
