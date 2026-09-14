# Client-Side Routing

## Purpose

A single-page React application (see
[react-project-structure.md](../introduction-to-react/react-project-structure.md)) has only one
real HTML page — but users still expect distinct, bookmarkable URLs for different views. This
module covers **React Router**, the standard library for mapping URLs to components entirely on
the client, without a full page reload.

## Learning Objectives

- Explain why client-side routing is needed at all, given a single-page app has only one HTML file.
- Define routes and navigate between them with React Router.
- Read dynamic segments from a URL (route parameters).
- Nest routes to share layout between related pages.

## Prerequisites

[React Lifecycle and useEffect](../react-lifecycle-and-useeffect/).

## Files in This Module

| File | Covers |
|---|---|
| [react-router-introduction.md](react-router-introduction.md) | Why client-side routing exists, and installing React Router |
| [routes-and-navigation.md](routes-and-navigation.md) | Defining routes, and navigating with `Link` |
| [route-parameters.md](route-parameters.md) | Reading dynamic URL segments with `useParams` |
| [nested-routes.md](nested-routes.md) | Sharing layout between related routes with `Outlet` |

## When to Deep-Dive vs. Skim

Deep-dive [react-router-introduction.md](react-router-introduction.md)'s explanation of *why*
client-side routing intercepts navigation instead of letting the browser handle it — this
distinction (and when it can actually break browser expectations like the back button, if done
carelessly) is easy to gloss over but matters for building a genuinely correct routed application.

## Quick Knowledge Check

<details>
<summary>When a user clicks a React Router `<Link>`, does the browser make a new request to the server for the new page?</summary>

No — that's the entire point. React Router intercepts the navigation, updates the URL via the
browser's History API, and renders the matching component client-side, without a network request
or full page reload. See [react-router-introduction.md](react-router-introduction.md).

</details>

<details>
<summary>For a route defined as `/products/:id`, how do you read the actual `id` value inside the matching component?</summary>

The `useParams()` hook, which returns an object of the current route's dynamic segments — e.g.,
`{ id: "42" }` for a URL of `/products/42`. See [route-parameters.md](route-parameters.md).

</details>

## References

- React Router, [Routing](https://reactrouter.com/start/declarative/routing)

## Continue Your Learning Path

Next: [Styling in React](../styling-in-react/) — see the
[Frontend learning path](../../README.md) for the full sequence.
