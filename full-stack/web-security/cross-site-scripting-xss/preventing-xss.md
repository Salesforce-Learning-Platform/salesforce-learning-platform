# 🛡️ Preventing XSS

## Two Complementary Layers of Defense

Preventing all three XSS variants — [reflected](reflected-xss.md), [stored](stored-xss.md), and
[DOM-based](dom-based-xss.md) — relies on two genuinely complementary defenses: **output escaping**
(the primary, structural fix) and **Content Security Policy** (a powerful defense-in-depth layer on
top of it).

## Output Escaping: The Structural Fix

```js
function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

res.send(`<div class="comment">${escapeHtml(userComment)}</div>`);   // SAFE
```

Escaping converts characters with special HTML meaning (`<`, `>`, `&`) into their literal, inert
text equivalents (`&lt;`, `&gt;`, `&amp;`) — a `<script>` tag becomes the harmless, visible text
`&lt;script&gt;` rather than an executable element. This is directly the same "structural
separation of data and instructions" principle already established in
[preventing-injection-attacks.md](../injection-attacks/preventing-injection-attacks.md), applied
here to HTML rendering specifically.

## Modern Frameworks Escape by Default

```jsx
// React escapes {userComment} automatically - SAFE by default
<div className="comment">{userComment}</div>
```

This is a genuinely significant, practical benefit already implicit throughout this repository's
Frontend domain — React, Vue, and similar frameworks escape interpolated content by default,
meaning ordinary, idiomatic use of these frameworks is already safe from XSS in the overwhelming
majority of cases, *unless* an explicit raw-HTML escape hatch is deliberately used (per
[dom-based-xss.md](dom-based-xss.md)).

## Content Security Policy: Defense in Depth

```
Content-Security-Policy: script-src 'self' 'nonce-a1b2c3d4'; object-src 'none'; base-uri 'none'
```

Per MDN's own documentation, CSP is a browser-enforced HTTP header that restricts which resources a
page is allowed to load and execute — it disables inline `<script>` tags and event handlers by
default, blocks `eval()`, and only permits scripts matching an explicit allowlist (here, the same
origin, plus scripts carrying a matching cryptographic nonce).

## Why CSP Matters Even With Correct Output Escaping

```
CSP provides GENUINE defense in depth: even if output escaping
somehow FAILS (a missed edge case, a bug, a new code path added
later without proper escaping), a correctly configured CSP can
STILL block the injected script from actually executing.
```

This is exactly the same defense-in-depth reasoning already established in
[preventing-injection-attacks.md](../injection-attacks/preventing-injection-attacks.md) — CSP is
not a substitute for correct output escaping, but a genuinely independent second layer that can
still prevent real harm if the first layer's protection somehow fails.

## A Complete Prevention Checklist

```
☐ Escape all user-controlled content before rendering it as HTML
  (or rely on a framework that does this by default)
☐ Use textContent instead of innerHTML wherever actual HTML
  rendering isn't genuinely needed
☐ Avoid raw-HTML escape hatches (dangerouslySetInnerHTML, v-html)
  for anything derived from user input
☐ Configure a strict Content Security Policy as an additional,
  independent layer of defense
```

## Common Mistakes

- Relying on CSP alone without correct output escaping, treating a defense-in-depth layer as though
  it were the primary, sufficient fix.
- Assuming a modern frontend framework's default escaping makes an application fully immune to XSS,
  missing that its own raw-HTML escape hatches can still reintroduce the exact same risk.
- Configuring a CSP so permissively (`script-src *`, allowing inline scripts) that it provides
  little to no genuine additional protection beyond output escaping.

## Module Summary

Across this module: **XSS** applies the same injection pattern already established in this domain's
previous module, targeting the victim's browser instead of a server-side interpreter, with injected
code running at the full privilege of the legitimate site (see
[what-is-xss.md](what-is-xss.md)); **reflected XSS** requires a victim to click a specifically
crafted, malicious link, with the payload never stored anywhere (see
[reflected-xss.md](reflected-xss.md)); **stored XSS** is generally more severe, since a single
successful injection can silently compromise every future visitor to an affected page, with no
further action needed from the attacker (see [stored-xss.md](stored-xss.md)); **DOM-based XSS**
lives entirely in client-side JavaScript, where server-side validation can never help, following a
source-to-sink pattern that `textContent` structurally defeats (see
[dom-based-xss.md](dom-based-xss.md)); and **prevention** combines output escaping (the structural
fix, provided by default in modern frameworks) with Content Security Policy (verified against MDN's
official documentation) as a genuinely independent, defense-in-depth second layer.
