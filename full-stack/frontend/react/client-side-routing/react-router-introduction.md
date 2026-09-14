# React Router: Introduction

## Why Client-Side Routing Exists

As covered in [react-project-structure.md](../introduction-to-react/react-project-structure.md), a
React single-page application has exactly one real HTML file — `index.html`, with an empty
`<div id="root">`. Without any additional tooling, there's no way for a URL like
`/products/42` to correspond to anything, since the server only ever serves that one file.
**Client-side routing** solves this: a library (React Router) intercepts navigation, updates the
URL, and renders the matching component — all in the browser, without asking the server for a new
page.

## Installing React Router

```bash
npm install react-router
```

## The Core Idea: Intercepting Navigation

```jsx
import { BrowserRouter } from "react-router";

function App() {
  return (
    <BrowserRouter>
      {/* routes go here */}
    </BrowserRouter>
  );
}
```

`BrowserRouter` uses the browser's History API to change the URL shown in the address bar and
respond to back/forward navigation, **without** triggering an actual new request to the server —
this is the mechanism that makes React Router's `<Link>` (covered next) behave completely
differently from a plain `<a href>` from
[links-and-navigation-flow.md](../../html/semantic-html-and-browser-rendering/links-and-navigation-flow.md),
which would otherwise cause a full page reload.

## Server-Side Considerations

Because the server still only knows about `index.html`, a production deployment needs to be
configured to serve `index.html` for *any* route the client-side router might handle (commonly
called a "catch-all" or "fallback" rewrite rule) — otherwise, directly visiting
`https://example.com/products/42` (or refreshing the page while on it) would hit the server
directly and get a genuine 404, since the server has no idea `/products/42` is meant to be handled
by client-side JavaScript. This exact problem is one of the things frameworks like Next.js
(covered in its own domain) solve automatically.

## Common Mistakes

- Forgetting the server-side fallback configuration, causing a direct visit or refresh on any
  route other than `/` to produce a genuine `404` in production, even though the same route works
  fine when navigated to via a `<Link>` from within the app.
- Using a plain `<a href="/products">` instead of React Router's `<Link>` (covered next) for
  in-app navigation, causing an unnecessary full page reload.
- Assuming client-side routing eliminates the need to think about URLs at all — routes should
  still be meaningful, bookmarkable, and shareable, exactly as they would be for a traditional
  multi-page site.

## Next

Continue to [routes-and-navigation.md](routes-and-navigation.md) to actually define routes and
navigate between them.
