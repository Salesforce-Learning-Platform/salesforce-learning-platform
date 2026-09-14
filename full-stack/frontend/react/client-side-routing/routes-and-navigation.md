# Routes and Navigation

## Defining Routes

```jsx
import { BrowserRouter, Routes, Route } from "react-router";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/products" element={<ProductList />} />
      </Routes>
    </BrowserRouter>
  );
}
```

`<Routes>` looks at the current URL and renders the single `<Route>` whose `path` matches — each
route maps a URL path directly to the component that should render for it.

## Navigating with `<Link>`

```jsx
import { Link } from "react-router";

function Nav() {
  return (
    <nav>
      <Link to="/">Home</Link>
      <Link to="/about">About</Link>
      <Link to="/products">Products</Link>
    </nav>
  );
}
```

`<Link>` renders an actual `<a>` element under the hood (so it remains accessible and keyboard-
navigable, per [links-and-navigation-flow.md](../../html/semantic-html-and-browser-rendering/links-and-navigation-flow.md)),
but intercepts the click to perform client-side navigation instead of a full page reload — exactly
the behavior introduced in [react-router-introduction.md](react-router-introduction.md).

## `NavLink` — For Highlighting the Active Route

```jsx
import { NavLink } from "react-router";

<NavLink
  to="/about"
  className={({ isActive }) => (isActive ? "active-link" : "")}
>
  About
</NavLink>
```

`NavLink` is a variant of `Link` specifically for navigation menus — it knows whether its own
target matches the current URL and exposes that as `isActive`, commonly used to visually highlight
the currently active page in a nav bar.

## Programmatic Navigation

```jsx
import { useNavigate } from "react-router";

function LoginForm() {
  const navigate = useNavigate();

  function handleSubmit() {
    // ...perform login...
    navigate("/dashboard"); // navigate in response to something other than a direct click
  }
}
```

`useNavigate()` returns a function for navigating programmatically — necessary when navigation
should happen as a *consequence* of something else (a successful form submission, an async
operation completing) rather than a direct link click.

## A 404 / "Not Found" Route

```jsx
<Routes>
  <Route path="/" element={<Home />} />
  <Route path="*" element={<NotFound />} /> {/* matches anything not matched above */}
</Routes>
```

A wildcard `path="*"` route, placed last, catches any URL that didn't match an earlier route —
the client-side routing equivalent of the
[404 status code](../../foundations/understanding-http-and-https/http-status-codes-in-depth.md)
from the Foundations domain.

## Common Mistakes

- Using a plain `<a>` instead of `<Link>`/`<NavLink>` for in-app navigation, triggering an
  unwanted full page reload.
- Forgetting a catch-all `path="*"` route, leaving an unmatched URL rendering nothing at all
  rather than a clear "not found" message.
- Calling `navigate()` when a plain `<Link>` would have been simpler and more semantically correct
  — reserve programmatic navigation for cases genuinely triggered by something other than a direct
  user click on a link.

## Next

Continue to [route-parameters.md](route-parameters.md) to handle dynamic segments in a URL, like
a specific product's ID.
