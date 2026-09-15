# 📤 Handling Files with Express

## Purpose

Every request body covered so far — from
[REST API Design](../rest-api-design/) through [Authentication](../authentication-and-authorization/) —
has been JSON. A real application inevitably needs to accept an actual **file** — a profile photo,
a product image, a document — which arrives as `multipart/form-data`, a genuinely different request
format Express doesn't parse on its own.

## 🎯 Learning Objectives

- Explain why file uploads need dedicated middleware, unlike a JSON body.
- Use Multer to handle single and multiple file uploads.
- Choose between memory storage and disk storage, and explain the real tradeoff.
- Access an uploaded file's data via `req.file`/`req.files`.
- Explain why a real application typically uploads to a cloud media service rather than storing
  files directly on its own server.

## 📋 Prerequisites

- [Express.js Fundamentals](../expressjs-fundamentals/) — specifically
  [middleware.md](../expressjs-fundamentals/middleware.md), since Multer is used as Express
  middleware throughout this module.

## 📂 Files in This Module

| File | Covers |
|---|---|
| [understanding-multer.md](understanding-multer.md) | What Multer is, and why file uploads need dedicated middleware |
| [uploading-files-with-multer.md](uploading-files-with-multer.md) | `upload.single()`, `upload.array()`, and `upload.fields()` |
| [memory-vs-disk-storage.md](memory-vs-disk-storage.md) | The real tradeoff between Multer's two storage engines |
| [accessing-uploaded-files.md](accessing-uploaded-files.md) | `req.file`/`req.files`, and validating an upload before trusting it |
| [cloud-media-storage.md](cloud-media-storage.md) | Uploading to a service like Cloudinary instead of the server's own disk |

## 🔍 When to Deep-Dive vs. Skim

Deep-dive [memory-vs-disk-storage.md](memory-vs-disk-storage.md) — choosing the wrong storage
engine for a given situation is a genuine, sometimes serious production mistake (an out-of-memory
crash from a large upload, or a lost file after a server restart), not just a minor configuration
detail.

## ✅ Quick Knowledge Check

<details>
<summary>Can req.body alone tell you anything about a file uploaded in the same form submission?</summary>

No — `req.body` only ever contains the form's plain text fields. A file's data and metadata are
populated by Multer specifically onto `req.file` (or `req.files`), a genuinely separate mechanism
from the JSON/urlencoded body parsing covered in
[request-response-objects.md](../expressjs-fundamentals/request-response-objects.md). See
[accessing-uploaded-files.md](accessing-uploaded-files.md).

</details>

<details>
<summary>Should a production application store user-uploaded images directly on its own server's disk long-term?</summary>

Generally no — a dedicated cloud media service handles storage, scaling, and content delivery far
better than a single application server, and storing files on the server's own disk creates real
problems (lost files on redeploy, no CDN, limited storage) that a cloud service is specifically
built to avoid. See [cloud-media-storage.md](cloud-media-storage.md).

</details>

## 📚 References

- Multer, [GitHub repository](https://github.com/expressjs/multer)
- Cloudinary, [Node.js Quick Start](https://cloudinary.com/documentation/node_quickstart)

## ➡️ Continue Your Learning Path

Continue to the [API Documentation and Developer Experience module](../api-documentation-and-developer-experience/)
to properly document the endpoints — including file-upload ones — built throughout this domain.
