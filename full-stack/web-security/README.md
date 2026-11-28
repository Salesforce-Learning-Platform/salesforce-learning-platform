# 🔐 Web Security

## 📚 Overview

These modules explain how web applications are attacked and how to defend them: injection, cross-site scripting, request forgery and clickjacking, cookies and CORS, attacks on authentication, and attacks on the server itself, ending with the habits that put the defenses into practice. No security experience is assumed. Knowing the [backend path](../backend/README.md) helps, because the examples use real endpoints and forms.

## 🧭 The Learning Path

Work through the modules in this order. The last column names the earlier modules each one relies on, so you can also start partway through; links point to modules in other areas.

| # | Module | What it covers | Builds on |
|---|--------|----------------|-----------|
| 1 | [The Security Mindset](the-security-mindset/README.md) | How attackers think, the OWASP Top 10, core principles, and STRIDE threat modeling | No security experience; the [backend path](../backend/README.md) helps |
| 2 | [Injection Attacks](injection-attacks/README.md) | SQL and command injection, and keeping data separate from instructions | The Security Mindset, [Schema Validation with Zod](../artificial-intelligence/schema-validation-with-zod/README.md) |
| 3 | [Cross-Site Scripting (XSS)](cross-site-scripting-xss/README.md) | Reflected, stored, and DOM-based XSS, output escaping, and Content Security Policy | Injection Attacks |
| 4 | [CSRF and Clickjacking](csrf-and-clickjacking/README.md) | Forged requests and hidden-frame clicks, and the defenses against each | Cross-Site Scripting |
| 5 | [Cookies, CORS, and Transport Security](cookies-cors-and-transport-security/README.md) | Cookie attributes, session cookies, CORS, HTTPS, and HSTS | CSRF and Clickjacking, [Domains, DNS, and SSL](../production-systems/domains-dns-and-ssl/README.md) |
| 6 | [Authentication Attacks](authentication-attacks/README.md) | JWT attacks, session hijacking and fixation, password guessing, and password storage | Cookies, CORS, and Transport Security, [Production Authentication Architecture](../backend/production-authentication-architecture/README.md) |
| 7 | [Server-Side Attacks](server-side-attacks/README.md) | Server-side request forgery, path traversal, unsafe uploads, and server hardening | The Security Mindset, [Handling Files with Express](../backend/handling-files-with-express/README.md) |
| 8 | [Security in Practice](security-in-practice/README.md) | Security headers, secrets, dependency scanning, security testing, and a pre-release checklist | All the modules above |

## ➡️ Start Here

Begin with [The Security Mindset](the-security-mindset/README.md). After the last module, the course continues with [System Design](../system-design/README.md).
