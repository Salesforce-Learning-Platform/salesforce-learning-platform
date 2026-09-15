# 🎭 Cross-Site Scripting (XSS)

## 📚 Overview

[Injection Attacks](../injection-attacks/) covered untrusted input reaching server-side
interpreters. This module covers the same fundamental pattern applied to a genuinely different
target: the victim's own browser. It covers what XSS actually is and why it's severe, all three
variants (reflected, stored, DOM-based), and the two complementary defenses — output escaping and
Content Security Policy — that prevent it.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain why XSS is severe: injected code runs with the same privileges as the legitimate site.
- Distinguish reflected, stored, and DOM-based XSS by where the vulnerability and payload actually
  live.
- Recognize the source-to-sink pattern behind DOM-based XSS, and use `textContent` over `innerHTML`
  appropriately.
- Configure output escaping and a Content Security Policy as complementary, defense-in-depth
  protections.

## 📋 Prerequisites

- [Injection Attacks](../injection-attacks/) — this module applies the same structural-separation principle established there to HTML rendering specifically.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [what-is-xss.md](what-is-xss.md) | The core mechanism, and why injected code's privileges make it severe |
| [reflected-xss.md](reflected-xss.md) | A crafted URL, echoed back unescaped, requiring a victim's click |
| [stored-xss.md](stored-xss.md) | A persisted payload silently compromising every future visitor |
| [dom-based-xss.md](dom-based-xss.md) | A purely client-side vulnerability server-side validation can't catch |
| [preventing-xss.md](preventing-xss.md) | Output escaping and Content Security Policy together; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you render any user-generated content, work with a framework's raw-HTML escape
hatch, or write client-side JavaScript that reads from the URL — every one of these is a genuine
XSS risk surface.

**Skim** if you exclusively use a modern frontend framework's default rendering with no raw-HTML
escape hatches — but read [dom-based-xss.md](dom-based-xss.md) regardless, since it applies even
then.

## 🧠 Knowledge Check

<details>
<summary>Why is stored XSS generally considered more severe than reflected XSS?</summary>

Reflected XSS requires a specific victim to click a specifically crafted, malicious link — it
compromises one victim per successful click. Stored XSS persists on the server and is served
automatically to every future visitor of the affected page, requiring no action from any individual
victim beyond simply viewing it — a single successful injection can compromise far more users.

</details>

<details>
<summary>Why can server-side input validation never catch DOM-based XSS?</summary>

DOM-based XSS can involve data (like a URL fragment after `#`) that is never sent to the server at
all — it's read and written entirely by client-side JavaScript, in the browser. Since the server
never sees this data, no amount of server-side validation can inspect or block it; the vulnerability
and its fix both live purely in client-side code.

</details>

## 📚 References

- [OWASP Community - Cross-Site Scripting](https://community.owasp.org/attacks/xss) — official source for the reflected/stored/DOM-based XSS distinction
- [MDN - Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP) — official documentation for CSP directives and syntax

## ➡️ Continue Your Learning Path

Continue to [CSRF and Clickjacking](../csrf-and-clickjacking/) to see two attacks that exploit a
victim's authenticated session without ever injecting code into the page at all.
