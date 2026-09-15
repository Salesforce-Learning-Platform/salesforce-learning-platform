# 🖥️ Server-Side Attacks

## 📚 Overview

This module covers attacks that target the server itself, beyond authentication specifically: SSRF
(tricking a server into making unintended, trusted requests), path traversal (escaping an intended
directory), file upload risks (untrusted content reaching the filesystem), and the broader secure
server configuration discipline that limits damage even when a specific defense fails.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain SSRF, grounded in the real 2019 Capital One breach, and prevent it with allowlisting.
- Prevent path traversal by validating a fully resolved path, not the raw input string.
- Validate uploaded file content via magic bytes rather than trusting client-supplied metadata.
- Apply server-hardening practices (least-privilege process users, minimal exposed surface,
  careful error handling) as defense-in-depth.

## 📋 Prerequisites

- [The Security Mindset](../the-security-mindset/) — this module applies its attack-surface and least-privilege principles directly.
- [Handling Files with Express](../../backend/handling-files-with-express/) — the implementation-level upload handling this module's security coverage builds on.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [server-side-request-forgery-ssrf.md](server-side-request-forgery-ssrf.md) | The 2019 Capital One breach, the mechanism, and allowlist-based prevention |
| [path-traversal.md](path-traversal.md) | `../` escaping an intended directory, verified against OWASP's own guidance |
| [file-upload-security.md](file-upload-security.md) | Magic-byte validation, renaming uploads, and never trusting `Content-Type` |
| [secure-server-configuration.md](secure-server-configuration.md) | Least-privilege process users, minimal surface, patching discipline; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if your application makes server-side requests to user-supplied URLs, serves files by
path, or accepts file uploads — each is a genuine, common risk surface this module directly
addresses.

**Skim** if none of those patterns apply to your current work — but read
[secure-server-configuration.md](secure-server-configuration.md) regardless, since its hardening
practices apply broadly to any deployed server.

## 🧠 Knowledge Check

<details>
<summary>Why was the SSRF vulnerability in the 2019 Capital One breach so severe, beyond simply fetching an unintended URL?</summary>

The malicious request originated from the server itself, carrying that server's own network-level
trust — reaching AWS's internal metadata service (169.254.169.254), which is only reachable from
inside that specific server, never from the public internet. This handed the attacker genuine, live
IAM credentials, turning a request-forgery bug into full cloud credential theft.

</details>

<details>
<summary>Why is checking a file's "magic bytes" a stronger defense than checking its extension or claimed Content-Type?</summary>

Both the filename extension and the `Content-Type` header are supplied by the client and trivially
spoofable — an attacker can claim any value they want. A file's magic bytes (its actual leading byte
sequence) reflect its genuine, real content regardless of what label the client attached, making
this the only one of the three checks that can't be bypassed by simply lying in the request.

</details>

## 📚 References

- [Wiz - What Is SSRF?](https://www.wiz.io/academy/application-security/server-side-request-forgery) and coverage of the 2019 Capital One breach — real-world SSRF context
- [OWASP Community - Path Traversal](https://community.owasp.org/attacks/Path_Traversal) — official documentation for path traversal mechanics and prevention
- [OWASP Cheat Sheet Series - File Upload](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html) — official, layered file upload security guidance

## ➡️ Continue Your Learning Path

Continue to [Security in Practice](../security-in-practice/) to bring every module in this domain
together into a practical, pre-ship security checklist.
