# ☁️ Cloud Media Storage

## Why a Server's Own Disk Isn't a Good Long-Term Home for Uploads

Storing user-uploaded files directly on the application server's own disk (per
[memory-vs-disk-storage.md](memory-vs-disk-storage.md)'s disk storage option) has real, practical
problems at production scale: many modern hosting platforms redeploy onto a **fresh disk** on every
deploy, silently losing anything stored there; a single server has no built-in content delivery
network, meaning every image request is served slowly and directly from that one server; and
scaling to multiple server instances (per
[Backend Architecture](../backend-architecture/)'s broader scalability concerns) means a file
uploaded to one instance isn't automatically available from another.

## Uploading to Cloudinary as a Concrete Example

```js
import { v2 as cloudinary } from "cloudinary";

cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET,
});

app.post("/avatar", upload.single("avatar"), async (req, res) => {
  const result = await cloudinary.uploader.upload(req.file.path, {
    folder: "avatars",
  });
  res.json({ url: result.secure_url });
});
```

**Cloudinary** (one real, concrete example of a dedicated media storage/delivery service) receives
the file and returns a `secure_url` — a permanent, CDN-backed URL the application stores (in its
own database, per [Database Design and Modeling](../database-design-and-modeling/)) and uses
whenever that image needs to be displayed, rather than ever serving the raw file from the
application server itself again.

## What a Dedicated Media Service Actually Provides

- **Durable, purpose-built storage** — files persist independently of the application server's own
  disk or deploy lifecycle.
- **A real CDN** — images are served from edge locations close to the actual viewer, directly
  connecting to [asset-loading-strategy.md](../../frontend/performance/frontend-performance-fundamentals/asset-loading-strategy.md)'s
  broader performance concerns, without the application backend needing to build that
  infrastructure itself.
- **On-the-fly transformations** — resizing, cropping, and format conversion available directly via
  URL parameters, with no need to pre-generate every size variant of an image manually.

## The Realistic Full Flow

```
1. Client uploads a file → Express + Multer (memory storage, per
   memory-vs-disk-storage.md — no need to touch the server's own disk
   at all before forwarding it)
2. Server forwards the file's buffer to Cloudinary
3. Cloudinary returns a permanent, CDN-backed URL
4. Server stores that URL in its own database, associated with the
   relevant record (a user's profile, a product)
```

This is exactly why memory storage (rather than disk storage) is often the right choice
specifically for uploads immediately forwarded to a cloud service: the file only ever needs to
exist briefly, in memory, during the single request that hands it off.

## Common Mistakes

- Storing uploaded files on the application server's own disk in production, then being surprised
  when they disappear after a routine redeploy.
- Serving user-uploaded images directly from the application server instead of through a real CDN,
  missing out on the load-time performance benefit a dedicated media service already provides.
- Forgetting to store the returned URL (from Cloudinary or an equivalent service) in the
  application's own database — the file exists in the cloud service, but the application has no
  way to find it again without that reference saved somewhere.

## Module Summary

Across this module: file uploads arrive as **`multipart/form-data`**, a genuinely different
encoding than JSON, requiring dedicated middleware to parse (see
[understanding-multer.md](understanding-multer.md)); **Multer**'s `single()`/`array()`/`fields()`
methods handle one file, several files under one field, or several files under distinctly named
fields respectively (see [uploading-files-with-multer.md](uploading-files-with-multer.md)); the
choice between **memory and disk storage** is a real production tradeoff between speed/memory risk
and disk persistence (see [memory-vs-disk-storage.md](memory-vs-disk-storage.md)); an uploaded
file's metadata (`mimetype`, `originalname`) is client-supplied and must never be trusted blindly,
with `fileFilter` and `limits` providing real, enforceable validation (see
[accessing-uploaded-files.md](accessing-uploaded-files.md)); and a real production application
typically forwards accepted uploads to a **dedicated cloud media service**, storing only the
resulting URL, rather than keeping files on the application server's own disk long-term.
