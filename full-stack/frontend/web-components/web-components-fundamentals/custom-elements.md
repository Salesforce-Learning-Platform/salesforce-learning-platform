# Custom Elements

## Defining One

```js
class ProductBadge extends HTMLElement {
  connectedCallback() {
    this.textContent = this.getAttribute("label") ?? "New";
    this.style.cssText = "background:#eab308;padding:2px 8px;border-radius:4px;";
  }
}

customElements.define("product-badge", ProductBadge);
```

```html
<product-badge label="Sale"></product-badge>
```

A **Custom Element** is a JavaScript class extending `HTMLElement`, registered with the browser via
`customElements.define(name, ClassName)`. Once registered, the browser treats `<product-badge>`
exactly like a built-in element such as `<button>` — you can use it in HTML, `document.createElement`
it, and query it with `document.querySelector`, with no framework runtime involved at all.

## The Tag Name Must Contain a Hyphen

`customElements.define("product-badge", ...)` would fail if the name were `productbadge`. This is a
deliberate HTML spec guarantee: every current and future built-in HTML element name is
hyphen-free, so any hyphenated tag name is permanently safe from colliding with one. This is the
same naming-collision problem [css-modules.md](../../react/styling-in-react/css-modules.md) solves
for CSS class names, solved instead at the level of the tag name itself.

## Lifecycle Callbacks

```js
class LiveClock extends HTMLElement {
  connectedCallback() {
    // Element was just inserted into the document — safe to read attributes now
    this._interval = setInterval(() => {
      this.textContent = new Date().toLocaleTimeString();
    }, 1000);
  }

  disconnectedCallback() {
    // Element was removed from the document — clean up, same reasoning as
    // a React effect's cleanup function
    clearInterval(this._interval);
  }
}

customElements.define("live-clock", LiveClock);
```

| Callback | Fires when | React analog |
|---|---|---|
| `connectedCallback()` | Element inserted into the document | Mount phase of `useEffect` |
| `disconnectedCallback()` | Element removed from the document | `useEffect`'s cleanup function |
| `attributeChangedCallback(name, oldValue, newValue)` | An *observed* attribute changes | A prop changing, triggering a re-render |
| `adoptedCallback()` | Element moved to a different document | No direct equivalent |

Setup work belongs in `connectedCallback()`, not the constructor — attributes and child content
aren't guaranteed to be available yet when the constructor runs, only once the element is actually
connected to the document.

## Reacting to Attribute Changes

```js
class StockLevel extends HTMLElement {
  static observedAttributes = ["count"];

  attributeChangedCallback(name, oldValue, newValue) {
    this.textContent =
      Number(newValue) > 0 ? `In stock: ${newValue}` : "Out of stock";
  }
}

customElements.define("stock-level", StockLevel);
```

`attributeChangedCallback` only fires for attributes explicitly listed in the static
`observedAttributes` array — the browser doesn't watch every attribute by default, since doing so
for every element would be wasteful. This is the closest native equivalent to a component
re-rendering when a prop value changes.

## Common Mistakes

- Registering a tag name without a hyphen — `customElements.define()` throws immediately.
- Reading attributes or child elements inside the `constructor()` instead of `connectedCallback()` —
  they may not exist yet at construction time.
- Forgetting to list an attribute in `observedAttributes`, then wondering why
  `attributeChangedCallback` never fires for it.
- Not cleaning up timers, event listeners, or subscriptions in `disconnectedCallback()`, causing the
  exact same kind of leak `useEffect`'s cleanup function exists to prevent.

## Next

Continue to [shadow-dom.md](shadow-dom.md) to encapsulate a Custom Element's internal markup and
styles from the rest of the page.
