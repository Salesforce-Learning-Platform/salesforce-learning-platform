# 📁 Files, Blobs, and the Clipboard

## Working With Data the User Gives You

Web apps constantly handle data that is not text in a variable: a photo the user picks, a CSV they
drag onto the page, a file the app generates for download, text to copy to the clipboard. The browser
models these with **`Blob`** (immutable raw data), **`File`** (a `Blob` with a name), **`FileReader`**
(the older way to read them), object URLs (a way to point at them), and the **Clipboard API**. For the
byte-level view of buffers see
[typed-arrays-and-binary-data.md](../built-in-objects-and-collections/typed-arrays-and-binary-data.md).

## 📦 `Blob`

A `Blob` is, per MDN, a file-like object of immutable raw data that can be read as text or binary
data, or converted into a stream.

```js
const blob = new Blob(["héllo"], { type: "text/plain" });

console.log(blob.size);                  // 6      — BYTES, not characters ("é" is 2 bytes in UTF-8)
console.log(blob.type);                  // text/plain
console.log(await blob.text());          // héllo
console.log((await blob.arrayBuffer()).byteLength);   // 6
console.log(Array.from(await blob.bytes()));          // [ 104, 195, 169, 108, 108, 111 ]
```

Reading is promise-based: `text()` (decoded as UTF-8), `arrayBuffer()`, `bytes()`, and `stream()`
(a `ReadableStream`, consumable with [`for await`](../advanced-async-patterns/async-iterators-and-for-await.md)).

`slice(start, end)` returns a new `Blob` of a **byte** range — which can cut a multi-byte character in
half:

```js
const sliced = blob.slice(0, 2);          // the bytes for "h" and the FIRST byte of "é"
console.log(sliced.size);                 // 2
console.log(await sliced.text());         // h�   — the broken character decodes to a replacement mark
```

Blobs are the right container for data you build in memory — a generated report, a canvas export, a
JSON file — and for the `body` of a `fetch` upload.

## 🗂️ `File`

A `File` is a `Blob` that also knows its `name` and `lastModified`. You get them from
`<input type="file">` (`input.files`), from drag-and-drop (`event.dataTransfer.files`), or by
constructing one:

```js
const file = new File(["a,b\n1,2"], "data.csv", { type: "text/csv", lastModified: 0 });

console.log(file.name, file.size, file.type);   // data.csv 7 text/csv
console.log(file instanceof Blob);              // true — a File IS a Blob
console.log(await file.text());                 // a,b⏎1,2
```

A selection handler that validates before reading:

```js
input.addEventListener("change", async () => {
  const [file] = input.files;
  if (!file) return;
  if (file.size > 5 * 1024 * 1024) return showError("File is larger than 5 MB.");
  if (!file.type.startsWith("image/")) return showError("Please choose an image.");
  const text = await file.text();               // or arrayBuffer(), or stream() for large files
});
```

`file.type` is typically derived from the file's extension; it is a hint, not proof of the contents,
and a user can rename a file to anything. **Always re-validate uploads on the server.**

## 📖 `FileReader`: The Older, Event-Based Way

Before `Blob` had promise methods, `FileReader` was the way to read a file. It remains common in
existing code. It reads asynchronously and reports through events (`load`, `error`, `progress`):

```js
const text = await new Promise((resolve, reject) => {
  const reader = new FileReader();
  reader.onload = () => resolve(reader.result);
  reader.onerror = () => reject(reader.error);
  reader.readAsText(file);
});
console.log(text);   // a,b⏎1,2
```

Its read methods are `readAsText`, `readAsArrayBuffer`, `readAsDataURL`, and `readAsBinaryString`. The
one `Blob.text()` does not replace is `readAsDataURL`, which yields a `data:` URL with the contents
inlined in Base64:

```js
const dataUrl = await new Promise((resolve) => {
  const reader = new FileReader();
  reader.onload = () => resolve(reader.result);
  reader.readAsDataURL(new Blob(["hi"], { type: "text/plain" }));
});
console.log(dataUrl);   // data:text/plain;base64,aGk=
```

Data URLs are about a third larger than the data and are copied into the page; for showing a large
image, prefer an object URL.

## 🔗 Object URLs: Pointing at In-Memory Data

`URL.createObjectURL(blob)` returns a short `blob:` URL that refers to the data without copying it —
usable as an `<img src>`, a media source, a worker script, or a download link:

```js
const url = URL.createObjectURL(blob);
console.log(url.slice(0, 29));            // blob:https://example.com/b422
console.log(await (await fetch(url)).text());   // héllo — it can be fetched like any URL

URL.revokeObjectURL(url);                 // release it
await fetch(url);                         // TypeError: Failed to fetch — the URL no longer works
```

The browser keeps the data alive for as long as the URL is not revoked, so **call
`revokeObjectURL` when you are done**, or every one you create stays in memory until the page closes.

### Offering a Download

Combine a `Blob`, an object URL, and an anchor with the `download` attribute:

```js
function downloadText(filename, text) {
  const url = URL.createObjectURL(new Blob([text], { type: "text/plain" }));
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;                  // tells the browser to save instead of navigate
  a.click();
  URL.revokeObjectURL(url);
}

downloadText("notes.txt", "Hello from the browser");
```

## 📋 The Clipboard API

`navigator.clipboard` provides asynchronous access to the system clipboard:

| Method | Purpose |
|--------|---------|
| `writeText(text)` | Copy text |
| `readText()` | Read text (an empty string if the clipboard holds none) |
| `write(items)` / `read()` | Copy and read rich data via `ClipboardItem` (images, HTML) |

```js
async function copy(text) {
  try {
    await navigator.clipboard.writeText(text);
    showToast("Copied!");
  } catch (error) {
    showToast("Couldn't copy — please copy manually.");
  }
}

copyButton.addEventListener("click", () => copy(codeBlock.textContent));
```

The API has firm requirements, per MDN:

- **Secure context only** — it exists on HTTPS pages and `localhost`.
- **Writing** needs a recent user action ("transient activation") in all browsers, or a granted
  permission in Chromium.
- **Reading** is more restricted still: it requires user activation plus either a permission prompt
  (Chromium) or a "Paste" prompt (Firefox and Safari).
- **Cross-origin iframes** need the matching Permissions-Policy.

Calling it outside those conditions rejects. In a test where the document was not focused:

```js
await navigator.clipboard.writeText("hello");
// NotAllowedError: Failed to execute 'writeText' on 'Clipboard': Document is not focused.
```

So always `try`/`catch`, call from a click or key handler, and keep a fallback. The old
`document.execCommand("copy")` approach is deprecated; do not build new code on it.

## 🎤 Interview Angle

- **"What is the difference between a `Blob` and a `File`?"** A `File` is a `Blob` with a `name` and
  `lastModified`; files come from user selection or the file system.
- **"How do you read a file's contents in the browser?"** `await file.text()` or `arrayBuffer()`; or
  `FileReader` (event-based) — still needed for `readAsDataURL`.
- **"Why call `URL.revokeObjectURL`?"** An object URL keeps its Blob in memory until revoked.
- **"Why might `navigator.clipboard.writeText` fail?"** It requires a secure context and a user
  gesture or permission, and the document generally has to be focused.

## Common Mistakes

- **Treating `blob.size` as a character count** — it is bytes.
- **Trusting `file.type` or the extension** for security decisions.
- **Reading very large files fully into memory** instead of streaming or slicing them.
- **Never revoking object URLs.**
- **Calling the Clipboard API outside a user action**, or on an insecure origin, with no error handling.
- **Embedding big files as data URLs.**

## ➡️ Next

Continue to [performance-apis.md](performance-apis.md) to measure what your code and your page are
actually doing.
