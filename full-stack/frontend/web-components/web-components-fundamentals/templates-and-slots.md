# Templates and Slots

## `<template>` — Inert, Reusable Markup

```html
<template id="product-card-template">
  <style>
    .card { border: 1px solid #e0e0e0; border-radius: 8px; padding: 16px; }
  </style>
  <div class="card">
    <slot name="title">Untitled Product</slot>
    <slot></slot>
  </div>
</template>
```

A `<template>` element's content is parsed by the browser but never rendered and never runs any
scripts or loads any images inside it — it sits inert in the document until JavaScript explicitly
clones it. This makes it a safe place to define a component's internal markup once, then reuse it
for every instance.

## Cloning a Template Into a Shadow Root

```js
class ProductCard extends HTMLElement {
  connectedCallback() {
    const template = document.getElementById("product-card-template");
    const shadow = this.attachShadow({ mode: "open" });
    shadow.appendChild(template.content.cloneNode(true));
  }
}

customElements.define("product-card", ProductCard);
```

`template.content` returns a `DocumentFragment` — the template's markup, ready to insert.
`cloneNode(true)` (a deep clone) is essential: appending the fragment directly would *move* it out
of the `<template>`, leaving nothing left to clone for the next instance. Cloning lets the same
`<template>` back any number of component instances.

## `<slot>` — Projecting Light DOM Content Into Shadow DOM

```html
<product-card>
  <span slot="title">Mechanical Keyboard</span>
  <p>Hot-swappable switches, USB-C.</p>
</product-card>
```

The children written between `<product-card>` and `</product-card>` — called the element's **light
DOM** — don't disappear when the component attaches its shadow DOM. Instead, `<slot>` elements
inside the shadow tree act as placeholders: a `<slot name="title">` receives whichever light DOM
child has a matching `slot="title"` attribute, and a nameless `<slot>` receives everything else that
wasn't claimed by a named slot.

This is the native, browser-level version of the same "project arbitrary child content into a
component's markup" idea that `props.children` solves in React and the default `<slot>` solves in
Vue — see [props.md](../../react/components-jsx-and-props/props.md) for the React comparison. The
mechanism differs (matching by a `slot` attribute vs. passing `children` as a prop value), but the
underlying goal — letting the *consumer* of a component supply some of its content — is identical.

## Fallback Content

```html
<slot name="title">Untitled Product</slot>
```

The text (or markup) written directly inside a `<slot>` in the template is **fallback content** —
it renders only if nothing in the light DOM claims that slot. In the earlier example, a
`<product-card>` used without a `slot="title"` child would display "Untitled Product" instead of
rendering empty.

## Common Mistakes

- Appending `template.content` directly instead of `template.content.cloneNode(true)` — this moves
  the template's only copy of the markup into the first instance, leaving nothing for any
  subsequent instance to clone.
- Forgetting the `slot="name"` attribute on a light DOM child, so it falls into the unnamed default
  slot instead of the intended named one.
- Expecting `<template>` content to run embedded `<script>` tags or load embedded `<img>` sources
  before it's cloned into the live document — it deliberately does neither while inert.

## Next

Continue to [web-components-in-practice.md](web-components-in-practice.md) to see when reaching for
native Web Components, instead of a framework, is actually the right call.
