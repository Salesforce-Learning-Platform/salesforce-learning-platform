# 💾 Memory vs. Disk Storage

## Two Genuinely Different Storage Engines

```js
import multer from "multer";

const memoryUpload = multer({ storage: multer.memoryStorage() });
const diskUpload = multer({ storage: multer.diskStorage({
  destination: "uploads/",
  filename: (req, file, cb) => cb(null, `${Date.now()}-${file.originalname}`),
}) });
```

Multer's `dest: "uploads/"` shorthand (from [understanding-multer.md](understanding-multer.md)) is
actually a convenience over its **disk storage** engine. Multer also offers a genuinely different
alternative: **memory storage** — and choosing between them is a real, consequential decision, not
a minor configuration detail.

## Memory Storage — Fast, but Risky at Scale

```js
const upload = multer({ storage: multer.memoryStorage() });

app.post("/avatar", upload.single("avatar"), (req, res) => {
  console.log(req.file.buffer); // the file's raw data, held ENTIRELY in RAM
});
```

With **memory storage**, an uploaded file's data is held as a `Buffer` directly in the server
process's memory — accessible immediately via `req.file.buffer`, with no disk I/O at all. This is
fast, but genuinely dangerous at scale: a large file, or many simultaneous uploads, can exhaust the
server's available memory and crash the entire process — a real production risk, not a theoretical
one.

## Disk Storage — More Control, Persisted to the File System

```js
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, "uploads/"),
  filename: (req, file, cb) => cb(null, `${Date.now()}-${file.originalname}`),
});
const upload = multer({ storage });

app.post("/avatar", upload.single("avatar"), (req, res) => {
  console.log(req.file.path); // where the file actually landed on disk
});
```

**Disk storage** writes each file directly to the server's file system, giving full control over
the destination folder and filename via callback functions — `req.file.path` then points to where
it actually landed. This avoids memory-exhaustion risk entirely, at the cost of needing real disk
space, and (in most production deployments) needing to actually move the file somewhere durable
afterward, since a server's own local disk often isn't reliable long-term storage — covered fully in
[cloud-media-storage.md](cloud-media-storage.md).

## The Real Decision

| | Memory storage | Disk storage |
|---|---|---|
| Speed | Fast — no disk I/O | Slightly slower — real disk writes |
| Risk | Can exhaust RAM with large/many files | No memory risk |
| Best fit | Small files, immediately forwarded elsewhere (e.g., straight to a cloud service) | Larger files, or files that need to persist locally even briefly |

A common, practical real-world pattern: use **memory storage** specifically when a file is
immediately forwarded to a [cloud media service](cloud-media-storage.md) without ever needing to
touch the server's own disk at all — the file exists in memory only briefly, during the upload
request itself.

## Common Mistakes

- Using memory storage for large files or high-volume uploads without any size limit, risking a
  real, production-impacting out-of-memory crash.
- Using disk storage in a deployment environment where the local disk isn't persistent (many modern
  hosting platforms redeploy on a fresh disk each time) and expecting an uploaded file to still be
  there later.
- Not setting a file size limit at all, regardless of storage engine — Multer supports a `limits`
  option specifically to cap upload size, and skipping it leaves the server exposed to an
  intentionally oversized upload.

## ➡️ Next

Continue to [accessing-uploaded-files.md](accessing-uploaded-files.md) to read and validate an
uploaded file's actual data.
