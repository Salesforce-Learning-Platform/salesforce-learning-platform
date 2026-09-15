# 📦 Understanding Multer

## Why a File Upload Isn't Just Another JSON Body

```
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary...

------WebKitFormBoundary...
Content-Disposition: form-data; name="avatar"; filename="photo.jpg"
Content-Type: image/jpeg

[raw binary image data]
------WebKitFormBoundary...
Content-Disposition: form-data; name="username"

alice
------WebKitFormBoundary...
```

A form submitting a file uses `multipart/form-data`, a genuinely different request encoding than
the JSON bodies parsed by `express.json()` throughout every prior module — it interleaves plain
text fields and raw binary file data together, separated by boundary markers. Express's built-in
body parsers don't understand this format at all; a dedicated tool is needed specifically to parse
it.

## What Multer Actually Is

**Multer** is Express middleware — following exactly the same `(req, res, next)` pattern from
[middleware.md](../expressjs-fundamentals/middleware.md) — built specifically to parse
`multipart/form-data` requests, separating a request's plain text fields (populated onto the usual
`req.body`) from its uploaded file data (populated onto a new `req.file`/`req.files`, covered fully
in [accessing-uploaded-files.md](accessing-uploaded-files.md)).

## Installing and Wiring It In

```bash
npm install multer
```

```js
import multer from "multer";
const upload = multer({ dest: "uploads/" });

app.post("/profile", upload.single("avatar"), (req, res) => {
  console.log(req.file); // the uploaded file's info
  console.log(req.body); // any other plain text fields
  res.json({ message: "Upload complete" });
});
```

`multer({ dest: "uploads/" })` configures a Multer instance; `upload.single("avatar")` is then
passed as route-specific middleware (per
[middleware.md](../expressjs-fundamentals/middleware.md)'s coverage of per-route middleware),
telling Multer to expect exactly one file, submitted under the form field named `"avatar"`.

## The Client Side Needs `enctype="multipart/form-data"` Too

```html
<form action="/profile" method="POST" enctype="multipart/form-data">
  <input type="file" name="avatar" />
  <button type="submit">Upload</button>
</form>
```

A plain HTML form defaults to a different encoding entirely — without `enctype="multipart/form-
data"` explicitly set, a file input's actual file data never gets sent correctly, regardless of
whether Multer is configured correctly on the server.

## Common Mistakes

- Forgetting `enctype="multipart/form-data"` on the client's `<form>` tag — Multer has nothing
  correctly-formatted to parse without it, even if the server-side setup is otherwise correct.
- Using `express.json()` alone and expecting it to somehow also parse an uploaded file — it's built
  specifically for JSON bodies and has no knowledge of `multipart/form-data` at all.
- Mismatching the field name passed to `upload.single("avatar")` against the actual `name`
  attribute on the HTML file input — Multer looks for that exact field name.

## ➡️ Next

Continue to [uploading-files-with-multer.md](uploading-files-with-multer.md) to handle more than
just a single file.
