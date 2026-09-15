# 🎣 CSRF and Clickjacking

## 📚 Overview

[Cross-Site Scripting](../cross-site-scripting-xss/) injected code into a page. This module covers
two genuinely different attacks that exploit a victim's authenticated session *without* any code
injection at all: CSRF, which forges an entire request using a victim's automatically-included
session cookie, and clickjacking, which tricks a victim's genuine click onto a hidden, legitimate
element.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain why an authenticated session cookie alone doesn't prove genuine user intent.
- Implement anti-CSRF tokens (the synchronizer token pattern) and complementary defenses
  (`SameSite` cookies, custom headers).
- Explain how clickjacking misdirects a real click via an invisible, overlaid iframe.
- Configure `X-Frame-Options` and CSP's `frame-ancestors` to prevent a page from being embedded at
  all.

## 📋 Prerequisites

- [Cross-Site Scripting (XSS)](../cross-site-scripting-xss/) — this module contrasts CSRF/clickjacking's mechanism against XSS's code-injection approach.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [understanding-csrf.md](understanding-csrf.md) | How a forged request exploits an automatically-included session cookie |
| [csrf-protection.md](csrf-protection.md) | Anti-CSRF tokens, custom headers, and `SameSite` cookies |
| [understanding-clickjacking.md](understanding-clickjacking.md) | An invisible, overlaid iframe misdirecting a victim's genuine click |
| [preventing-clickjacking.md](preventing-clickjacking.md) | `X-Frame-Options` and CSP's `frame-ancestors`; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you build any application with state-changing forms or API endpoints relying on
cookie-based session authentication — both attacks in this module directly target that exact
pattern.

**Skim** if your application uses only token-based authentication sent via a custom header (never
automatically included by the browser) — CSRF specifically becomes much less of a concern, though
clickjacking protection still applies.

## 🧠 Knowledge Check

<details>
<summary>Why doesn't a valid session cookie on a request prove the user genuinely intended that specific action?</summary>

A browser automatically includes cookies with every request to a given domain, regardless of which
page actually initiated that request. This means an attacker's page can cause a victim's browser to
send a fully authenticated request to a target site the victim never intended to interact with —
the cookie proves *which session* is active, not that the *user* deliberately triggered the action.

</details>

<details>
<summary>Why does clickjacking require the victim to make a genuine, real click, unlike CSRF?</summary>

Clickjacking works by overlaying an invisible, legitimate element (like a real transfer-confirmation
button) directly on top of a decoy the victim sees and intends to click. The victim's click is
completely real and deliberate — it's simply landing on a different, hidden element than the one
they believe they're interacting with, rather than the request being forged without any interaction
at all.

</details>

## 📚 References

- [MDN - Cross-Site Request Forgery (CSRF)](https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/CSRF) — official documentation for the CSRF attack and its defenses
- [MDN - X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options) — official documentation for frame protection headers

## ➡️ Continue Your Learning Path

Continue to [Cookies, CORS, and Transport Security](../cookies-cors-and-transport-security/) to see
the `SameSite` cookie attribute and other browser-enforced security mechanisms in full depth.
