# 🔍 Accessing Uploaded Files

## What `req.file` Actually Contains

```js
app.post("/avatar", upload.single("avatar"), (req, res) => {
  console.log(req.file);
  /*
  {
    fieldname: 'avatar',
    originalname: 'photo.jpg',
    mimetype: 'image/jpeg',
    size: 204800,
    buffer: <Buffer ...>,   // present with memory storage
    path: 'uploads/...',     // present with disk storage
  }
  */
});
```

`req.file` (populated by `upload.single()`) carries real metadata about the upload: its original
filename, its declared MIME type, its size in bytes, and either a `buffer` (memory storage) or a
`path` (disk storage), per [memory-vs-disk-storage.md](memory-vs-disk-storage.md).

## Never Trust `mimetype` or `originalname` Blindly

```js
// A malicious client can freely set BOTH of these to anything at all —
// they're just values the client claims, not verified facts
console.log(req.file.mimetype);     // client-declared, not verified
console.log(req.file.originalname); // client-declared, not verified
```

`mimetype` and `originalname` are both values the *client* declares in the request — nothing
verifies they're actually accurate. A file named `"photo.jpg"` with `mimetype: "image/jpeg"` could
genuinely contain anything at all; a client can set both fields to whatever it wants. This is
directly the same "never trust client input" principle from
[request-validation.md](../rest-api-design/request-validation.md), applied specifically to file
uploads.

## Validating Uploads With Multer's `fileFilter` and `limits`

```js
const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 5 * 1024 * 1024 }, // 5 MB
  fileFilter: (req, file, cb) => {
    if (!file.mimetype.startsWith("image/")) {
      return cb(new Error("Only image files are allowed"));
    }
    cb(null, true);
  },
});
```

`limits.fileSize` caps how large an accepted file can be — rejecting anything larger before it
consumes significant memory or disk space, directly addressing
[memory-vs-disk-storage.md](memory-vs-disk-storage.md)'s risk of an oversized upload. `fileFilter`
runs before a file is fully accepted, letting the server reject an upload based on its declared
type — a first line of defense, not a complete guarantee (since, again, that declared type is
client-supplied and not independently verified).

## Handling a Multer Error

```js
app.post("/avatar", (req, res, next) => {
  upload.single("avatar")(req, res, (err) => {
    if (err) return res.status(422).json({ error: err.message });
    res.json({ message: "Uploaded" });
  });
});
```

A rejected upload (from `fileFilter`, an exceeded size limit, or a missing file) surfaces as an
error passed to Multer's own callback — handled here directly, or forwarded to
[Express's centralized error handling](../expressjs-fundamentals/error-handling.md) for a
consistent response shape across the whole application.

## Common Mistakes

- Trusting `req.file.mimetype` as a guarantee of a file's real content — it's a client-supplied
  claim, not a verified fact; genuinely verifying file content requires inspecting the actual file
  data itself, beyond this module's scope.
- Skipping `limits.fileSize` entirely, leaving an upload endpoint exposed to an intentionally
  oversized file.
- Not handling the error Multer produces when `fileFilter` rejects a file, leaving the client with
  an unhelpful, generic server error instead of a clear, specific rejection reason.

## ➡️ Next

Continue to [cloud-media-storage.md](cloud-media-storage.md) to see where an accepted, validated
upload should actually end up in a real production application.
