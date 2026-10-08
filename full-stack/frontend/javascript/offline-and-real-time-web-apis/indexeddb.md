# 🗄️ IndexedDB

## A Real Database in the Browser

[local-storage.md](../using-browser-functionalities/local-storage.md) ended with a pointer: for large
or structured data, `localStorage` is the wrong tool and **IndexedDB** is the right one. `localStorage`
is synchronous (it blocks the page while it reads or writes), stores only strings, and is small.
IndexedDB is **asynchronous**, stores almost any JavaScript value, supports **indexes** for querying,
and groups operations into **transactions**. It is what offline-capable apps use for their local data.

## 🧱 The Model

Per MDN's guide, an IndexedDB database holds **object stores** (the analog of tables), each containing
records addressed by a **key**:

| Concept | Meaning |
|---------|---------|
| **Database** | A named, versioned container, scoped to your origin |
| **Object store** | A collection of records; keyed by a `keyPath` (a property of the value) or an auto-incrementing key |
| **Index** | A secondary lookup on another property (optionally `unique`) |
| **Transaction** | A group of operations that succeed or fail together |
| **Request** | Every operation returns an `IDBRequest` that reports success or error through events |

Data is bound to the origin that created it, so other origins cannot read it.

## 🪄 Promise Helpers

IndexedDB predates promises and uses `onsuccess`/`onerror` events. Three tiny helpers make it pleasant
to use with `async`/`await` (the popular [`idb`](https://github.com/jakearchibald/idb) library, described
as "IndexedDB, but with promises," does this and more):

```js
const request = (req) => new Promise((resolve, reject) => {
  req.onsuccess = () => resolve(req.result);
  req.onerror = () => reject(req.error);
});

const done = (tx) => new Promise((resolve, reject) => {
  tx.oncomplete = () => resolve();
  tx.onerror = () => reject(tx.error);
  tx.onabort = () => reject(tx.error ?? new Error("transaction aborted"));
});

function openDb(name, version, upgrade) {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(name, version);
    req.onupgradeneeded = (event) => upgrade(req.result, event.oldVersion, req.transaction);
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
    req.onblocked = () => reject(new Error("blocked by another open connection"));
  });
}
```

## 🏗️ Creating the Database and Its Schema

`indexedDB.open(name, version)` opens the database, creating it if needed. When the requested version is
**higher** than the stored one, the `upgradeneeded` event fires — and, per MDN, that is the **only**
place you can create or delete object stores and indexes.

```js
const db = await openDb("demo", 1, (db, oldVersion) => {
  console.log(`upgrade from v${oldVersion}`);                 // upgrade from v0  (a brand-new database)

  const notes = db.createObjectStore("notes", { keyPath: "id", autoIncrement: true });
  notes.createIndex("byTag", "tag");
  notes.createIndex("byEmail", "email", { unique: true });
});

console.log(db.name, db.version, [...db.objectStoreNames]);   // demo 1 [ 'notes' ]
```

## ✍️ Writing

All reads and writes happen inside a **transaction**, created with `db.transaction(stores, mode)`. The
mode is `"readonly"` (the default) or `"readwrite"`.

```js
const tx = db.transaction("notes", "readwrite");
const store = tx.objectStore("notes");

const ids = await Promise.all([
  request(store.add({ title: "Buy milk",   tag: "home", email: "a@x.com", created: new Date(0) })),
  request(store.add({ title: "Write docs", tag: "work", email: "b@x.com", created: new Date(86400000) })),
  request(store.add({ title: "Call mom",   tag: "home", email: "c@x.com", created: new Date(172800000) })),
]);
await done(tx);                       // wait for the transaction to COMMIT, not just the requests

console.log(ids);                     // [ 1, 2, 3 ] — auto-incremented keys
```

`add` fails if the key already exists; `put` inserts or replaces. Awaiting `done(tx)` — the
transaction's `complete` event — is what tells you the data is durably stored.

## 🔍 Reading and Querying

```js
const tx = db.transaction("notes");
const store = tx.objectStore("notes");

console.log((await request(store.get(2))).title);                        // Write docs
console.log(await request(store.count()));                               // 3
console.log((await request(store.index("byTag").getAll("home"))).map((n) => n.title));
// [ 'Buy milk', 'Call mom' ]                                            — query by an index
console.log(await request(store.get(999)));                              // undefined — a miss is not an error
```

A **cursor** walks records in key order (ascending by default, or `"prev"` for descending); a **key range**
narrows a query:

```js
const titles = [];
await new Promise((resolve) => {
  const cursorRequest = store.openCursor(null, "prev");
  cursorRequest.onsuccess = () => {
    const cursor = cursorRequest.result;
    if (cursor) { titles.push(`${cursor.key}:${cursor.value.title}`); cursor.continue(); }
    else resolve();
  };
});
console.log(titles);   // [ '3:Call mom', '2:Write docs', '1:Buy milk' ]

// all notes created on or after day 1, using an index on `created` (added in the upgrade below)
store.index("byCreated").getAll(IDBKeyRange.lowerBound(new Date(86400000)));
```

## 📦 What You Can Store

Values are copied with the **structured clone algorithm** — the same one used by `postMessage` and
`structuredClone` (see [copying-objects-shallow-vs-deep.md](../objects-in-depth/copying-objects-shallow-vs-deep.md)).
So rich types survive the round trip, but functions do not:

```js
await request(store.put({ title: "binary", email: "bin@x.com", data: new Uint8Array([1, 2, 3]),
                          blob: new Blob(["hi"]), set: new Set([1]) }));
// reading it back: data is a Uint8Array, blob is a Blob, set is a Set

store.put({ title: "fn", email: "fn@x.com", handler() {} });
// DataCloneError — functions cannot be stored
```

`Date` objects also come back as real `Date`s (confirmed in testing), unlike a JSON round trip. Storing
`Blob`s is a common way to cache images and files for offline use
([files-blobs-and-clipboard.md](../browser-apis-in-depth/files-blobs-and-clipboard.md)).

## 🔒 Transactions: Atomic, Auto-Committing, and Easy to Misuse

A transaction **commits automatically** when it has no pending requests and control returns to the event
loop. Two consequences follow, both verified in a browser.

**1. An error aborts the whole transaction.** A write that violates a constraint — here a duplicate value
in the `unique` email index — fails with a `ConstraintError`; per MDN, an unhandled request error
bubbles up and aborts the transaction, rolling back everything in it:

```js
const tx = db.transaction("notes", "readwrite");
const dupe = tx.objectStore("notes").add({ title: "dupe", tag: "x", email: "a@x.com" });
dupe.onerror = () => console.log(dupe.error.name);        // ConstraintError
await done(tx).catch(() => console.log("aborted"));       // aborted — the count is still 3
```

You can also roll back deliberately with `tx.abort()`; after it, nothing the transaction wrote remains
(the count stayed at 3 in testing).

**2. Don't wait on anything *except* IndexedDB inside a transaction.** If you `await` a timer, a
`fetch`, or any other non-IndexedDB promise, the transaction has no pending requests, commits, and your
next write throws:

```js
const tx = db.transaction("notes", "readwrite");
const store = tx.objectStore("notes");

await new Promise((resolve) => setTimeout(resolve, 20));  // the transaction auto-commits here
store.put({ title: "too late" });
// TransactionInactiveError: Failed to execute 'put' on 'IDBObjectStore': The transaction has finished.
```

The rule of thumb: do your network calls and computation **first**, then open a short transaction and
do only IndexedDB work inside it. (Awaiting the promises that wrap IndexedDB requests, as in the helpers
above, is fine — it keeps the transaction alive.)

## 🔄 Changing the Schema: Versions and Migrations

To add an index or store, bump the version; the `upgradeneeded` handler runs with the old version number
so you can migrate step by step. The upgrade gets its own `versionchange` transaction (the third argument
of the helper):

```js
db.close();                                               // close old connections first
const db2 = await openDb("demo", 2, (db, oldVersion, upgradeTx) => {
  console.log(`upgrade from v${oldVersion}`);             // upgrade from v1
  upgradeTx.objectStore("notes").createIndex("byCreated", "created");   // existing records are indexed
  db.createObjectStore("settings", { keyPath: "key" });
});

console.log(db2.version, [...db2.objectStoreNames]);      // 2 [ 'notes', 'settings' ]
```

Existing data is kept. If another tab still holds the old version open, the upgrade is **blocked** until
it closes its connection — real apps listen for `versionchange` on their connection and close it.
`indexedDB.databases()` lists the databases for the origin (name and version).

## 📏 Quotas and Persistence

Browser storage is limited. MDN's quota guide explains that quotas apply per origin and are **shared**
by IndexedDB, the Cache API, and the Origin Private File System. Data is **best-effort** by default —
the browser may evict it under storage pressure (least-recently-used origins first, and all of an
origin's data together). Two APIs help:

```js
const { usage, quota } = await navigator.storage.estimate();   // estimates, not exact values
console.log(typeof usage, typeof quota, quota > usage);         // number number true

console.log(await navigator.storage.persisted());               // false — best-effort by default
// await navigator.storage.persist();                           // request storage exempt from pressure eviction
```

Writes that exceed the quota fail with a `QuotaExceededError`, so wrap large writes in `try`/`catch`.
Always keep the server as the source of truth for anything the user cannot afford to lose.

## 🆚 `localStorage` vs. IndexedDB

| | `localStorage` | IndexedDB |
|---|----------------|-----------|
| API | Synchronous (blocks the page) | Asynchronous (events / promises) |
| Values | Strings only | Structured-cloneable values: objects, `Date`, `Blob`, typed arrays, … |
| Querying | By key only | By key, indexes, ranges, cursors |
| Size | A few megabytes | Large, subject to the shared origin quota |
| Transactions | None | Yes, atomic |
| Typical use | Small preferences | Offline data, caches of API results, files |

## 🛡️ Security Note

IndexedDB is readable by *any* script running on your origin — including injected code from an XSS
vulnerability ([Cross-Site Scripting](../../../web-security/cross-site-scripting-xss/)). Never store
passwords or long-lived secrets there; treat it as a cache of data the user is already allowed to see.

## 🎤 Interview Angle

- **"`localStorage` vs. IndexedDB?"** `localStorage` is a small, synchronous, string-only key-value
  store; IndexedDB is an asynchronous, transactional, indexed object database for large structured data.
- **"Where can you create object stores?"** Only inside the `upgradeneeded` handler of an `open()` call
  with a higher version.
- **"Why did my IndexedDB write throw `TransactionInactiveError`?"** The transaction auto-committed
  because you awaited a non-IndexedDB promise before using it.
- **"What happens if one request in a transaction fails?"** If the error is not handled, the whole
  transaction aborts and rolls back.

## Common Mistakes

- **Awaiting `fetch` or timers inside a transaction.**
- **Creating stores or indexes outside `upgradeneeded`.**
- **Treating the request's `onsuccess` as "saved"** — wait for the transaction's `complete`.
- **Forgetting that old tabs can block an upgrade.**
- **Assuming stored data is permanent** — it is best-effort unless persistence is granted.
- **Storing secrets in it.**

## ➡️ Next

Continue to [service-workers-and-the-cache-api.md](service-workers-and-the-cache-api.md) to cache the
app itself — HTML, scripts, and API responses — so it keeps working offline.
