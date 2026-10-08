# 🔗 URL and History APIs

## Stop Building URLs With String Concatenation

URLs look like simple strings, which tempts people to build them with `+` and template literals — and to
parse them with `split("?")`. Both approaches break on special characters, relative paths, and
encoding. The browser (and Node.js) provide a proper **`URL`** class and **`URLSearchParams`**, and a
**History API** for changing the address bar without reloading the page. Together they are the
foundation of every client-side router.

## 🧩 The `URL` Class

```js
const url = new URL("https://user@example.com:8080/a/b/c.html?x=1&y=two&x=3#section");

console.log(url.origin);     // https://example.com:8080
console.log(url.protocol);   // https:
console.log(url.host);       // example.com:8080
console.log(url.hostname);   // example.com
console.log(url.port);       // 8080
console.log(url.pathname);   // /a/b/c.html
console.log(url.search);     // ?x=1&y=two&x=3
console.log(url.hash);       // #section
```

### Resolving Relative URLs

Give `URL` a base and it resolves relative references the way a browser would:

```js
console.log(new URL("../x?k=v", "https://example.com/a/b/c").href);   // https://example.com/a/x?k=v
console.log(new URL("/root", "https://example.com/a/b/c").href);      // https://example.com/root
```

### Validating Input

The constructor throws for anything that is not a valid URL. `URL.canParse()` answers the same question
with a boolean (check MDN's compatibility table for older environments):

```js
console.log(URL.canParse("https://example.com"));                 // true
console.log(URL.canParse("not a url"));                           // false
console.log(URL.canParse("/path", "https://example.com"));        // true

new URL("not a url");
// TypeError: Failed to construct 'URL': Invalid URL    (Chrome's wording; Node.js says "Invalid URL")
```

## 🔎 `URLSearchParams`: The Query String as a Collection

`url.searchParams` is a live `URLSearchParams`: editing it updates `url.search`.

```js
const url = new URL("https://example.com/a?x=1&y=two&x=3");

console.log(url.searchParams.get("x"));      // 1       — the FIRST value
console.log(url.searchParams.getAll("x"));   // [ '1', '3' ]
console.log(url.searchParams.has("y"));      // true

url.searchParams.set("x", "9");              // replaces every x with one x=9
url.searchParams.append("q", "a b&c");       // adds a pair, encoding it for you
url.searchParams.delete("y");

console.log(url.search);                      // ?x=9&q=a+b%26c
console.log([...new URLSearchParams("a=1&b=2&a=3")]);   // [ [ 'a', '1' ], [ 'b', '2' ], [ 'a', '3' ] ]
```

Repeated keys are preserved in order; `get` returns the first and `getAll` returns every value.

### Encoding: `+` vs. `%20`

`URLSearchParams` serializes a space as `+`; `encodeURIComponent` uses `%20`. Both are valid in a
query string, but they are not interchangeable everywhere:

```js
console.log(new URLSearchParams({ q: "a b&c", plus: "1+1" }).toString());
// q=a+b%26c&plus=1%2B1

console.log(encodeURIComponent("a b&c"));                      // a%20b%26c
console.log(encodeURI("https://example.com/a b?q=1&r=é"));     // https://example.com/a%20b?q=1&r=%C3%A9
```

`encodeURI` encodes a *whole URL* and leaves its structural characters (`?`, `&`, `/`) alone;
`encodeURIComponent` encodes a *single piece* and escapes those characters. Use `URLSearchParams` (or
`encodeURIComponent` per value) for query values, never `encodeURI`.

MDN warns about one trap in the other direction: parsing a *string* treats a literal `+` as a space.
Build instances with `append()` or an object rather than interpolating strings:

```js
console.log(new URLSearchParams("q=1+1").get("q"));   // "1 1" — the + was read as a space
```

Building URLs with the API instead of concatenation also removes a class of bugs where unescaped user
input changes the meaning of a URL — see the injection material in
[Injection Attacks](../../../web-security/injection-attacks/).

## 🧭 `location`: The Current URL

`window.location` exposes the current page's URL with the same properties (`pathname`, `search`,
`hash`, …). Assigning to `location.href` or calling `location.assign(url)` **navigates** (loading a new
page); `location.replace(url)` navigates without leaving a history entry; `location.reload()` reloads.
Changing only `location.hash` scrolls and adds a history entry without reloading.

## 📚 The History API

For single-page apps, navigating by full page loads is too slow and loses state. The **History API**
lets script change the URL and the history stack *without* loading a page. The core methods:

| Method | Effect |
|--------|--------|
| `history.pushState(state, "", url)` | Adds a new history entry and updates the address bar |
| `history.replaceState(state, "", url)` | Replaces the current entry instead of adding one |
| `history.back()` / `forward()` / `go(n)` | Moves through the stack |
| `history.state` | The state object of the current entry |
| `popstate` event | Fired when the user (or script) moves through history |

The second argument is a legacy "title" that browsers ignore; pass `""`.

A recorded sequence in a real browser, on an `https://example.com` page:

```js
history.pushState({ step: 1 }, "", "/step-1");
history.pushState({ step: 2 }, "", "/step-2?mode=x");

console.log(location.pathname + location.search);   // /step-2?mode=x
console.log(history.state);                          // { step: 2 }
// history.length grew by 2

addEventListener("popstate", (event) => {
  console.log(event.state, location.pathname);
});

history.back();      // { step: 1 }  /step-1
history.back();      // null         /      — the original entry had no state
history.forward();   // { step: 1 }  /step-1

history.replaceState({ replaced: true }, "", "/replaced");
console.log(location.pathname, history.state);       // /replaced { replaced: true }
```

Three details that trip people up:

- **`pushState` does not fire `popstate`.** The event fires only when the user navigates (Back, Forward)
  or you call `back()`/`forward()`/`go()`. A router must update its own view after calling `pushState`.
  The test confirmed: pushing state fired no event.
- **The URL must be same-origin.** Pushing a cross-origin URL throws a `SecurityError`:

```js
history.pushState({}, "", "https://example.org/other");
// SecurityError: A history state object with URL 'https://example.org/other' cannot be created in a
//                document with origin 'https://example.com' …
```

- **Reloading a pushed URL asks the server for it.** After `pushState(..., "/step-1")`, refreshing
  requests `/step-1` from the server, which must serve the app for that path — which is why single-page
  apps need a server fallback to `index.html`.

### A Minimal Router Skeleton

```js
function navigate(path) {
  history.pushState({ path }, "", path);
  render(path);                                   // push does NOT trigger popstate, so render here
}

addEventListener("popstate", () => render(location.pathname));   // Back/Forward

document.addEventListener("click", (event) => {
  const link = event.target.closest("a[data-link]");
  if (link) {
    event.preventDefault();                       // stop the full page load
    navigate(link.getAttribute("href"));
  }
});
```

This uses event delegation ([event-delegation.md](../events/event-delegation.md)) so dynamically added
links work. Frameworks such as React Router and the Next.js router are built on exactly this pattern.

## 🎤 Interview Angle

- **"How do you read query parameters?"** `new URL(location.href).searchParams`, or
  `new URLSearchParams(location.search)`, then `.get(name)`.
- **"`encodeURI` vs. `encodeURIComponent`?"** `encodeURI` encodes a full URL and keeps its structural
  characters; `encodeURIComponent` encodes one component and escapes them.
- **"Does `pushState` trigger `popstate`?"** No — `popstate` fires on back/forward navigation only.
- **"How does a single-page app change the URL without reloading?"** With the History API
  (`pushState`/`replaceState`) plus rendering its own view, and listening for `popstate`.
- **"Why do SPAs need server configuration?"** A reload of a client-side route requests that path from
  the server, which must return the app shell.

## Common Mistakes

- **Concatenating query strings by hand**, leaving values unencoded.
- **Using `encodeURI` for query values.**
- **Expecting `pushState` to render anything** or to fire `popstate`.
- **Pushing cross-origin URLs** (a `SecurityError`).
- **Forgetting that `searchParams.get` returns only the first of repeated keys.**
- **Reading a `+` in a parsed string as a plus sign** — it is decoded as a space.

## ➡️ Next

Continue to [files-blobs-and-clipboard.md](files-blobs-and-clipboard.md) to work with user-selected
files, in-memory binary data, and copy-and-paste.
