# Web Components Fundamentals

## Purpose

Having compared React against [Vue](../../vue/vue-fundamentals/), this module steps back to a
different question: what if a component didn't need *any* framework at all? **Web Components** are
a suite of browser-native APIs — Custom Elements, Shadow DOM, and HTML Templates/Slots — that let
you build reusable, encapsulated components using nothing but standard HTML, CSS, and JavaScript,
runnable in any framework, or none.

## Learning Objectives

- Define a Custom Element by extending `HTMLElement` and registering it with `customElements.define()`.
- Use the Custom Element lifecycle callbacks (`connectedCallback`, `disconnectedCallback`,
  `attributeChangedCallback`) to manage a component's behavior over its lifetime.
- Attach a Shadow DOM tree to encapsulate a component's internal markup and CSS from the rest of
  the page.
- Use `<template>` and `<slot>` to define reusable, content-projecting markup.
- Explain when reaching for framework-agnostic Web Components is the right architectural choice.

## Prerequisites

- [JavaScript domain](../../javascript/) — specifically
  [classes](../../javascript/object-oriented-programming/) and
  [DOM manipulation](../../javascript/dom-manipulation/).
- The [React domain](../../react/) and [Vue domain](../../vue/vue-fundamentals/), for contrast —
  this module repeatedly compares Web Components' native approach against what a framework
  provides for you.

## Files in This Module

| File | Covers |
|---|---|
| [custom-elements.md](custom-elements.md) | Defining a Custom Element, `customElements.define()`, and the lifecycle callbacks |
| [shadow-dom.md](shadow-dom.md) | `attachShadow()`, open vs. closed mode, and bidirectional CSS encapsulation |
| [templates-and-slots.md](templates-and-slots.md) | `<template>`, cloning content, and content projection with `<slot>` |
| [web-components-in-practice.md](web-components-in-practice.md) | When to reach for Web Components vs. a framework, and interop with React/Vue |

## When to Deep-Dive vs. Skim

Deep-dive [shadow-dom.md](shadow-dom.md) — Shadow DOM's encapsulation model is the single biggest
conceptual shift from framework-based components (where isolation is a *convention*, like CSS
Modules from [css-modules.md](../../react/styling-in-react/css-modules.md), not a *browser
guarantee*). Understanding exactly what does and doesn't cross the shadow boundary matters more
than memorizing the rest of the API surface.

## Quick Knowledge Check

<details>
<summary>Does a Custom Element's tag name need anything special, and why?</summary>

Yes — it must contain a hyphen (e.g. `my-element`, not `myelement`). This is a deliberate,
permanent reservation in the HTML spec: any tag name without a hyphen is guaranteed to never be
claimed by a future native HTML element, so your custom name can never collide with one. See
[custom-elements.md](custom-elements.md).

</details>

<details>
<summary>If a page has a global CSS rule like `p { color: blue; }`, will it style a &lt;p&gt; rendered inside a component's Shadow DOM?</summary>

No. Shadow DOM provides encapsulation in both directions: page-level CSS cannot reach into a shadow
tree, and CSS written inside a shadow tree cannot leak out to the rest of the page. This is a real
browser guarantee, not a build-tool convention. See [shadow-dom.md](shadow-dom.md).

</details>

## References

- MDN, [Web Components](https://developer.mozilla.org/en-US/docs/Web/API/Web_components)
- MDN, [Using custom elements](https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_custom_elements)
- MDN, [Using shadow DOM](https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_shadow_DOM)
- MDN, [Using templates and slots](https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_templates_and_slots)

## Continue Your Learning Path

This is the only module in the Web Components domain. See the
[Frontend learning path](../../README.md) for what comes next.
