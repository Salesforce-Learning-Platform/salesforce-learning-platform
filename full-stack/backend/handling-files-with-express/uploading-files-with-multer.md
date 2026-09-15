# 📎 Uploading Files with Multer

## `upload.single()` — Exactly One File

```js
app.post("/profile", upload.single("avatar"), (req, res) => {
  res.json({ filename: req.file.filename });
});
```

`upload.single(fieldName)` expects exactly one file, submitted under that specific form field name,
populated onto `req.file` (singular) — the pattern already introduced in
[understanding-multer.md](understanding-multer.md).

## `upload.array()` — Multiple Files, Same Field

```js
app.post("/gallery", upload.array("photos", 5), (req, res) => {
  const filenames = req.files.map((file) => file.filename);
  res.json({ uploaded: filenames });
});
```

```html
<input type="file" name="photos" multiple />
```

`upload.array(fieldName, maxCount)` accepts **multiple** files submitted under the same field name
(here, `"photos"`) — useful for something like a product gallery upload, where a user selects
several images from one file input. `maxCount` caps how many files Multer accepts in one request;
exceeding it produces an error rather than silently truncating the list. The result lands on
`req.files` (plural) — an array, iterated with `.map()` exactly like any other array covered
throughout [the JavaScript domain](../../frontend/javascript/).

## `upload.fields()` — Multiple, Differently-Named Fields

```js
app.post(
  "/products",
  upload.fields([
    { name: "mainImage", maxCount: 1 },
    { name: "additionalImages", maxCount: 5 },
  ]),
  (req, res) => {
    console.log(req.files.mainImage);         // an array with one file
    console.log(req.files.additionalImages);  // an array with up to 5 files
  }
);
```

`upload.fields([...])` handles the more complex case: a single request uploading files under
**several different, named fields** at once — a product form with one main image and several
additional images, each field with its own file(s). `req.files` becomes an object keyed by field
name, each value itself an array (even for a field configured with `maxCount: 1`).

## Choosing the Right Method

| Method | Use when |
|---|---|
| `upload.single(name)` | Exactly one file, one field (a profile photo) |
| `upload.array(name, max)` | Several files, all under the same field (a photo gallery) |
| `upload.fields([...])` | Several files under different, distinctly-named fields (a product's main + gallery images) |

## Common Mistakes

- Using `upload.single()` when a form genuinely needs to accept multiple files under the same
  field — it only ever populates `req.file`, ignoring any additional files beyond the first.
- Forgetting `maxCount` on `upload.array()`, unintentionally allowing an unbounded number of files
  in a single request.
- Confusing `req.files` (plural, an array or object, from `array()`/`fields()`) with `req.file`
  (singular, a single object, from `single()`) — mixing these up produces `undefined` where a
  file was expected.

## ➡️ Next

Continue to [memory-vs-disk-storage.md](memory-vs-disk-storage.md) to decide exactly where an
uploaded file's data actually goes once Multer receives it.
