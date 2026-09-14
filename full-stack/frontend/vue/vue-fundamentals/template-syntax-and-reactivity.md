# Template Syntax and Reactivity

## HTML-Based Templates, Not JSX

```vue
<template>
  <p>{{ message }}</p>
</template>
```

Where React uses JSX (from [jsx.md](../../react/components-jsx-and-props/jsx.md)) — HTML-like
syntax embedded directly in JavaScript — Vue's standard approach is the reverse: JavaScript
expressions embedded inside otherwise-ordinary HTML, using `{{ }}` for text interpolation. Vue does
support a JSX-like syntax as an alternative, but templates are the idiomatic default seen in the
vast majority of real Vue code.

## Directives: `v-if`, `v-for`, `v-bind`, `v-on`

```vue
<template>
  <p v-if="isOnSale">On Sale!</p>

  <ul>
    <li v-for="product in products" :key="product.id">{{ product.name }}</li>
  </ul>

  <img :src="product.imageUrl" :alt="product.name" />

  <button @click="addToCart">Add to Cart</button>
</template>
```

| Directive | Role | React equivalent |
|---|---|---|
| `v-if` | Conditional rendering | A ternary or `&&` inside JSX |
| `v-for` | Rendering a list | `.map()` inside JSX |
| `v-bind` (shorthand `:`) | Binding a dynamic attribute value | `{value}` as a JSX attribute |
| `v-on` (shorthand `@`) | Binding an event handler | `onClick={handler}` |

`:key` on a `v-for` plays the exact same role as React's `key` prop from
[jsx.md](../../react/components-jsx-and-props/jsx.md) — a stable identifier helping Vue track
which list item is which across updates.

## `ref()` — Reactive State

```vue
<script setup>
import { ref } from "vue";

const count = ref(0);

function increment() {
  count.value++; // mutate .value directly — no separate setter function
}
</script>

<template>
  <button @click="increment">Count: {{ count }}</button>
</template>
```

This is the section flagged for deep-dive in this module's README, and it's a genuine, not
superficial, difference from React: `ref()` returns an object with a `.value` property. In
JavaScript code, you read and write `count.value` directly — there's no separate setter function
like `useState`'s `setCount`. In the template, Vue automatically "unwraps" the ref, so you write
`{{ count }}`, not `{{ count.value }}`.

## Why This Works Without a Setter Function

React's `useState` requires calling `setCount` because React has no way to detect a plain
JavaScript variable changing — it needs an explicit signal. Vue's reactivity system works
differently: `ref()`/`reactive()` values are wrapped in a JavaScript **Proxy** that Vue uses to
detect *when* a property is read (during rendering, establishing a dependency) and *when* it's
later written (triggering exactly the components that actually depend on it to update). This is a
fundamentally different underlying mechanism, not just a syntax shortcut — directly mutating
`count.value` is enough, because Vue's Proxy-based system observes that mutation happening.

## `reactive()` — For Objects

```vue
<script setup>
import { reactive } from "vue";

const cart = reactive({ items: [], total: 0 });

function addItem(product) {
  cart.items.push(product); // direct mutation — reactive() tracks it automatically
  cart.total += product.price;
}
</script>
```

`reactive()` makes an entire object's properties reactive, without needing `.value` at all — but
only works for object types (not primitives like a plain number), and can't be destructured
without losing reactivity (a genuinely different tradeoff than the always-immutable-update
discipline required by `useState`, covered in
[usestate.md](../../react/state-and-rerendering-logic/usestate.md)).

## Common Mistakes

- Forgetting `.value` when reading or writing a `ref` in JavaScript code (outside the template,
  where it's unwrapped automatically) — a very common early mistake for anyone coming from
  `useState`.
- Directly mutating a `reactive()` object expecting React-style immutable-update discipline to be
  required — Vue's model is built specifically around direct mutation being tracked, the opposite
  assumption from React's `useState`.
- Destructuring a `reactive()` object's properties into separate variables, which breaks their
  connection to Vue's reactivity tracking.

## Next

Continue to [components-and-props.md](components-and-props.md) to build reusable, composable
pieces from this syntax.
