# 📂 Path Traversal

## Escaping the Intended Directory

Per OWASP's own definition, path traversal "aims to access files and directories that are stored
outside the web root folder" — by manipulating a file path with `../` sequences, an attacker can
navigate a server's filesystem well beyond wherever the application intended to restrict access.

## The Vulnerable Pattern, and OWASP's Own Example

```php
$template = $_COOKIE['TEMPLATE'];
include("/home/users/phpguru/templates/" . $template);
```

```
Attacker sends: TEMPLATE=../../../../../../../../../etc/passwd

The server concatenates this into:
/home/users/phpguru/templates/../../../../../etc/passwd

Each "../" moves UP one directory level - chained enough times,
this resolves to simply: /etc/passwd
```

The exact same underlying pattern applies directly to a Node.js/Express application:

```js
// VULNERABLE
app.get("/files/:filename", (req, res) => {
  res.sendFile(`/app/uploads/${req.params.filename}`);
});
```

```
Attacker requests: GET /files/../../../../etc/passwd

The server resolves this to a path OUTSIDE the intended
/app/uploads directory entirely.
```

## The Fix: Validate the Resolved Path, Not Just the Input String

```js
const path = require("node:path");

app.get("/files/:filename", (req, res) => {
  const uploadsDir = path.resolve("/app/uploads");
  const requestedPath = path.resolve(uploadsDir, req.params.filename);

  if (!requestedPath.startsWith(uploadsDir)) {
    return res.status(403).json({ error: "Invalid file path" });
  }

  res.sendFile(requestedPath);
});
```

This is the structurally correct fix, directly per OWASP's own guidance — `path.resolve()` fully
normalizes the path (collapsing every `../` sequence), and the check confirms the *final, resolved*
path is genuinely still inside the intended directory, rather than attempting to detect and block
`../` in the raw input string (which is bypassable via URL encoding, double-encoding, or OS-specific
path separators).

## OWASP's Own, Stronger Preference: Avoid User Input for File Paths Entirely

```js
// EVEN BETTER - use an INDEX or ID, never a raw filename, if possible
const TEMPLATES = { 1: "default.html", 2: "compact.html", 3: "dark-mode.html" };

app.get("/template/:id", (req, res) => {
  const filename = TEMPLATES[req.params.id];
  if (!filename) return res.status(404).end();
  res.sendFile(path.resolve("/app/templates", filename));
});
```

Per OWASP's own strongest recommendation, the most robust fix avoids using user-supplied input for
a file path *at all* — mapping a request to a known, fixed set of legitimate options (an ID, an
index) removes the entire attack surface rather than merely validating against it after the fact.

## Common Mistakes

- Attempting to sanitize `../` sequences from the raw input string instead of validating the fully
  resolved, normalized path — an approach genuinely bypassable via encoding tricks.
- Storing genuinely sensitive files (configuration, credentials) inside a directory that's also
  reachable by any file-serving endpoint, even a correctly validated one.
- Trusting a filename supplied by the client for anything beyond display, when an internal ID or
  index would remove the entire risk category.

## ➡️ Next

Continue to
[file-upload-security.md](file-upload-security.md) to see a related, genuinely common risk: what
happens when user-supplied *content*, not just a path, reaches the server's filesystem.
