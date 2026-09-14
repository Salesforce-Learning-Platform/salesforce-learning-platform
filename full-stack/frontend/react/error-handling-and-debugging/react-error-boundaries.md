# React Error Boundaries

## The Problem: One Component's Error Crashes the Whole App

By default, an uncaught error thrown during rendering anywhere in a React tree unmounts the
**entire** application — a bug in one small widget (say, a malformed product review rendering
incorrectly) can take down an entire page, including completely unrelated content like the
navigation and checkout button.

## Creating an Error Boundary

```jsx
import { Component } from "react";

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true }; // triggers the fallback UI on the next render
  }

  componentDidCatch(error, info) {
    console.error("Caught by ErrorBoundary:", error, info.componentStack);
    // typically also reported to an error-tracking service here
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }
    return this.props.children;
  }
}
```

Error boundaries currently **must** be class components (from
[classes-and-inheritance.md](../../javascript/object-oriented-programming/classes-and-inheritance.md))
— there's no hook-based equivalent, since the underlying mechanism relies on
`getDerivedStateFromError`, a class lifecycle method with no direct hook equivalent (React's docs
also point to the community `react-error-boundary` package, which wraps this exact pattern for
projects that prefer not to write it by hand).

## Using It Around a Risky Section

```jsx
function ProductPage({ productId }) {
  return (
    <div>
      <Header />
      <ErrorBoundary fallback={<p>Something went wrong loading reviews.</p>}>
        <ProductReviews productId={productId} /> {/* if this crashes... */}
      </ErrorBoundary>
      <RelatedProducts /> {/* ...this still renders fine */}
    </div>
  );
}
```

Wrapping just the risky section (rather than the entire app in one giant boundary) means a failure
in `ProductReviews` shows a contained fallback message, while `Header` and `RelatedProducts`
continue rendering completely normally — the same "smaller, deliberate boundaries" reasoning as
`Suspense` boundary placement from
[lazy-loading.md](../performance-optimization-in-react/lazy-loading.md).

## What Error Boundaries Do NOT Catch

This is the section worth deep-diving, per this module's README: error boundaries catch errors
during **rendering** only. They explicitly do **not** catch:

- Errors inside **event handlers** — use ordinary
  [try/catch](../../javascript/error-handling-and-debugging/try-catch-finally.md) there instead.
- Errors in **asynchronous code** (a `.then()` callback, a `setTimeout`) — these happen outside
  React's rendering process entirely.
- Errors during **server-side rendering**.
- Errors thrown **inside the error boundary component itself**.

```jsx
function BuyButton() {
  function handleClick() {
    throw new Error("Payment failed"); // an ErrorBoundary will NOT catch this
  }
  return <button onClick={handleClick}>Buy Now</button>;
}
```

An error thrown here needs its own `try`/`catch` inside `handleClick` — wrapping `BuyButton` in an
`ErrorBoundary` provides no protection against this specific kind of failure at all.

## Common Mistakes

- Assuming an error boundary provides blanket protection against every kind of error anywhere in
  its subtree, including event handlers and async code — it doesn't.
- Wrapping the entire application in exactly one error boundary, meaning any rendering error
  anywhere shows the same generic, unhelpful fallback — smaller, targeted boundaries around
  genuinely risky, independent sections usually provide a better experience.
- Forgetting `componentDidCatch` is the place to actually report the error to a monitoring service
  — without it, the error is caught and hidden, but nobody is ever notified it happened.

## Next

Continue to
[debugging-react-applications.md](debugging-react-applications.md) for the tools and workflow
used to diagnose issues like these in the first place.
