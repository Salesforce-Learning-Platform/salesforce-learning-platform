# What Is Next.js?

## A Framework Built on React

Next.js is a **framework** — it uses React (from the
[React domain](../../react/)) for component rendering, and adds the surrounding pieces a real
production application needs but plain React itself doesn't provide:

| Concern | Plain React | Next.js |
|---|---|---|
| Routing | Requires a separate library (React Router, from [Client-Side Routing](../../react/client-side-routing/)) | Built in, via file-system routing |
| Rendering location | Client-side only, by default | Client and server, with several strategies to choose from |
| Build tooling | Configured separately (Vite, from [setting-up-a-react-project.md](../../react/introduction-to-react/setting-up-a-react-project.md)) | Built in, pre-configured |
| API endpoints | Needs a separate backend | Can be built directly into the same project |

## Why a Framework, Rather Than Assembling These Pieces Yourself

A plain React + Vite project (from the React domain) is a genuinely reasonable choice for a
client-side-only application. Next.js exists for a different, common need: applications that
benefit from **server-side rendering** (sending fully-rendered HTML from the server, rather than
an empty `<div id="root">` for the browser to fill in — directly relevant to
[how-browsers-render-pages.md](../../html/semantic-html-and-browser-rendering/how-browsers-render-pages.md)),
better default performance, and built-in routing conventions — all pre-configured and working
together, rather than manually integrating several separate libraries and tools yourself.

## Server-Side Rendering, Briefly

Recall from
[react-project-structure.md](../../react/introduction-to-react/react-project-structure.md) that a
plain React app's `index.html` is nearly empty — the browser has to download and run JavaScript
before anything meaningful appears. Next.js can instead render a page's actual HTML **on the
server**, sending a fully-formed page immediately — improving how quickly content becomes visible,
and improving how well search engines and social-media link previews can read the page's content
without executing JavaScript first. The full mechanics of this are covered in the next module,
[Next.js Rendering Strategies](../rendering-strategies/).

## When Next.js Is (and Isn't) the Right Choice

Next.js is a strong default for most production web applications today, but it's not universally
the only right answer: a purely internal admin tool with no SEO concerns and no need for
server-rendering might be entirely well-served by plain React + Vite, without taking on Next.js's
additional conventions and concepts. As with the styling and state-management decisions covered
earlier in this platform, the right tool depends on the project's actual requirements, not a
blanket rule.

## Common Mistakes

- Assuming Next.js is a completely different language or paradigm from React — every concept from
  the React domain (components, props, hooks, state) applies directly and identically inside a
  Next.js application.
- Reaching for Next.js by default for every project, including ones with no actual need for
  server-side rendering or built-in routing, adding unnecessary framework conventions to learn.
- Confusing "framework" (Next.js, opinionated and complete) with "library" (React, focused
  specifically on UI rendering) — this distinction is exactly what separates the two, and explains
  why Next.js is built *on top of* React rather than being an alternative to it.

## Next

Continue to [creating-a-nextjs-project.md](creating-a-nextjs-project.md) to actually create one.
