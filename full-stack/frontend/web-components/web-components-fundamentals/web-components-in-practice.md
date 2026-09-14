# Web Components in Practice

## Putting the Three Pieces Together

```js
class ProductCard extends HTMLElement {
  static observedAttributes = ["price"];

  connectedCallback() {
    const template = document.getElementById("product-card-template");
    const shadow = this.attachShadow({ mode: "open" });
    shadow.appendChild(template.content.cloneNode(true));
    this._priceEl = shadow.querySelector(".price");
    this._render();
  }

  attributeChangedCallback() {
    if (this._priceEl) this._render();
  }

  _render() {
    this._priceEl.textContent = `$${this.getAttribute("price") ?? "0"}`;
  }
}

customElements.define("product-card", ProductCard);
```

```html
<template id="product-card-template">
  <style>
    .card { border: 1px solid #e0e0e0; border-radius: 8px; padding: 16px; }
  </style>
  <div class="card">
    <slot name="title">Untitled Product</slot>
    <p class="price"></p>
  </div>
</template>

<product-card price="79">
  <span slot="title">Mechanical Keyboard</span>
</product-card>
```

This combines everything from the module: [custom-elements.md](custom-elements.md)'s registration
and lifecycle, [shadow-dom.md](shadow-dom.md)'s encapsulation, and
[templates-and-slots.md](templates-and-slots.md)'s reusable, content-projecting markup — a
self-contained component usable in a plain HTML page with zero build step and zero framework
runtime.

## When You'd Actually Reach for Web Components

- **A component library meant to be framework-agnostic** — a design system's buttons or cards need
  to render correctly whether the consuming team uses React, Vue, Angular, or no framework at all.
  A Web Component ships once and works everywhere.
- **Widgets embedded in third-party or unpredictable environments** — an embeddable chat widget or
  analytics banner that must not leak styles into, or be broken by styles from, a host page you
  don't control. Shadow DOM's guaranteed CSS isolation matters far more here than in an app you
  fully own.
- **Incrementally enhancing a page that has no framework at all** — much like Vue's
  ["progressive framework" pitch](../../vue/vue-fundamentals/what-is-vue.md), a single Custom
  Element can be dropped into an otherwise-static HTML page without adopting React or Vue's full
  toolchain.

## When You'd Still Reach for React or Vue Instead

- Building a full application with substantial, deeply interconnected state — React's rendering
  model (see [usestate.md](../../react/state-and-rerendering-logic/usestate.md)) and Vue's
  reactivity (see
  [template-syntax-and-reactivity.md](../../vue/vue-fundamentals/template-syntax-and-reactivity.md))
  both do far more of that coordination work for you than the raw Custom Elements API does.
- Wanting the ecosystem — routing, server state, established patterns — that
  [the client-side routing module](../../react/client-side-routing/) and
  [server-state-and-api-integration](../../react/server-state-and-api-integration/) already cover
  for React.

## Web Components Interop With Frameworks

A Custom Element is just a DOM element, so React and Vue can both render one directly
(`<product-card>` inside JSX, or inside a Vue template) exactly like any built-in HTML tag — the two
approaches aren't mutually exclusive. A team can use Web Components for a shared, framework-agnostic
design-system layer while still building the application itself in React or Vue on top of it.

## Common Mistakes

- Treating Web Components as a replacement for React/Vue in a full application, rather than as a
  tool best suited for framework-agnostic, widely-embedded, or no-framework scenarios.
- Forgetting that a Custom Element used inside React needs its properties/attributes passed the DOM
  way (attributes as strings, or setting a JS property directly) rather than as ordinary React
  props, since a Custom Element doesn't know what a "React prop" is.
- Assuming Shadow DOM CSS isolation removes the need to think about styling at all — a component
  still needs its own deliberate styles; isolation only prevents *collisions*, not the absence of
  styling.

## Module Summary

Across this module: a **Custom Element** is a class extending `HTMLElement`, registered with
`customElements.define()`, with lifecycle callbacks (`connectedCallback`, `disconnectedCallback`,
`attributeChangedCallback`) that are the native equivalent of a framework's mount/cleanup/prop-change
hooks (see [custom-elements.md](custom-elements.md)); **Shadow DOM**, attached via `attachShadow()`,
gives a component a genuinely isolated DOM tree with browser-enforced, bidirectional CSS
encapsulation — a stronger guarantee than a framework's scoped-styling convention (see
[shadow-dom.md](shadow-dom.md)); **`<template>` and `<slot>`** define a component's reusable
internal markup and let consumers project their own content into it, the native analog of
`props.children` (see [templates-and-slots.md](templates-and-slots.md)); and Web Components earn
their place specifically for framework-agnostic, widely-embedded, or no-build-step scenarios, not
as a wholesale replacement for React or Vue in a full application.
