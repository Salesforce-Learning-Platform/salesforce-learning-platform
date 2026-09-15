# 📤 File Upload Security

## User-Supplied Content Reaching the Server's Filesystem

[path-traversal.md](path-traversal.md) covered untrusted *paths*. File uploads introduce a related
but genuinely distinct risk: untrusted *content*, potentially executable content, being written
directly to the server's own filesystem — this directly extends
[Handling Files with Express](../../backend/handling-files-with-express/), covered from the
implementation side earlier in this repository's Backend domain.

## Why the Client-Supplied `Content-Type` Can Never Be Trusted

```js
// VULNERABLE - trusts whatever content-type the CLIENT claims
if (req.file.mimetype === "image/png") {
  saveFile(req.file);
}
```

```
An attacker can trivially SET the Content-Type header to
"image/png" while uploading an ACTUAL, executable script file -
the header is simply a claim the CLIENT makes, entirely under the
attacker's own control.
```

Per OWASP's own File Upload Cheat Sheet, this is a genuinely important, easy-to-miss point: the
`Content-Type` a client sends is not a genuine, trustworthy signal of a file's actual content — it's
just a label the request happens to include, which an attacker controls just as freely as any other
request header.

## The Real Fix: Validate the Actual File Content ("Magic Bytes")

```js
import { fileTypeFromBuffer } from "file-type";

const type = await fileTypeFromBuffer(req.file.buffer);
if (!type || !["image/png", "image/jpeg"].includes(type.mime)) {
  return res.status(400).json({ error: "Invalid file type" });
}
```

Real file formats begin with a specific, known byte sequence (a "magic number") — a genuine PNG
file always starts with the same specific bytes, regardless of what its filename or claimed
`Content-Type` says. Checking the file's *actual* content this way, rather than trusting any
client-supplied label, is the OWASP-recommended, structurally sound validation approach.

## Never Store Uploads Inside the Web Root, With Their Original Names

```
An uploaded file named "malicious.php", saved with its ORIGINAL
name inside a directory the web server SERVES directly:
  → if the server ever executes files from that directory, this
    becomes DIRECT remote code execution
```

```js
const crypto = require("node:crypto");
const safeFilename = crypto.randomUUID() + path.extname(originalName).toLowerCase();
```

Per OWASP's own layered guidance: renaming every uploaded file to a random, generated identifier
(never trusting the original filename) and storing uploads *outside* any directory the web server
would ever directly execute code from — both independently close off this specific, severe outcome.

## A Complete, Layered Upload Validation Strategy

```
☐ ALLOWLIST accepted file types (never a denylist)
☐ Validate ACTUAL content (magic bytes), never just the extension
  or claimed Content-Type
☐ Enforce a strict size limit, SERVER-side
☐ RENAME every file to a random, generated identifier
☐ Store uploads OUTSIDE the web root / any directly-executable
  directory
```

This directly applies [defense in depth](../the-security-mindset/security-principles.md), earlier
in this domain — no single one of these controls is treated as sufficient alone; together, they
close this risk from several independent, complementary angles.

## Common Mistakes

- Trusting a client-supplied `Content-Type` or file extension as genuine proof of a file's actual
  content.
- Storing uploaded files with their original, attacker-controlled filenames inside a directory the
  web server could ever directly execute.
- Validating file type only at initial upload time, with no size limit enforced server-side,
  leaving the endpoint open to resource-exhaustion abuse regardless of file-type correctness.

## ➡️ Next

Continue to
[secure-server-configuration.md](secure-server-configuration.md) to bring every server-side attack
in this module together into one deliberate, hardened configuration checklist.
