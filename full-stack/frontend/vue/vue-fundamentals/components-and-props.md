# Components and Props

## A Single-File Component (SFC)

```vue
<!-- ProductCard.vue -->
<script setup>
defineProps({
  name: String,
  price: Number,
});
</script>

<template>
  <div class="card">
    <h3>{{ name }}</h3>
    <p>${{ price }}</p>
  </div>
</template>

<style scoped>
.card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
}
</style>
```

A Vue **Single-File Component** (`.vue` file) bundles a component's template, script, and styles
into one file — a structural difference from React, where JSX/logic lives in a `.tsx` file and
styling is typically a genuinely separate concern (via CSS Modules, CSS-in-JS, or Tailwind, from
[the React domain's Styling module](../../react/styling-in-react/)). The `scoped` attribute on
`<style>` automatically locally-scopes those styles to this component, directly comparable to what
[css-modules.md](../../react/styling-in-react/css-modules.md) achieves in React, but built into
the framework itself rather than requiring a separate tool.

## Defining and Using Props

```vue
<!-- Using ProductCard -->
<template>
  <ProductCard name="Keyboard" :price="79" />
</template>
```

`defineProps` declares exactly which props a component accepts — directly comparable to
destructuring props in a function's parameters, per
[props.md](../../react/components-jsx-and-props/props.md). A static value (`name="Keyboard"`) is
passed as a plain string; `:price="79"` (using the `v-bind` shorthand from
[template-syntax-and-reactivity.md](template-syntax-and-reactivity.md)) passes an actual
JavaScript value rather than the literal string `"79"`.

## Props Are Read-Only, Exactly Like React

```vue
<script setup>
const props = defineProps({ price: Number });

// props.price = 100; // WRONG — Vue warns against this, exactly like React's read-only props rule
</script>
```

This rule carries over identically from
[props.md](../../react/components-jsx-and-props/props.md): a component should never modify a prop
it receives. Vue explicitly warns in the console if you try — the underlying reasoning (props
represent data owned by the parent) is completely framework-agnostic.

## Emitting Events — Vue's Equivalent of a Callback Prop

```vue
<!-- ProductCard.vue -->
<script setup>
const emit = defineEmits(["add-to-cart"]);
</script>

<template>
  <button @click="emit('add-to-cart', product.id)">Add to Cart</button>
</template>
```

```vue
<!-- Using it -->
<template>
  <ProductCard :product="product" @add-to-cart="handleAddToCart" />
</template>
```

Where React passes a callback function directly as a prop (`onAddToCart={handleAddToCart}`, per
[props.md](../../react/components-jsx-and-props/props.md)), Vue has a distinct, explicit mechanism:
`defineEmits` declares which named events a component can emit, and `emit('event-name', data)`
triggers one — the parent listens with `@event-name`. Both achieve the same goal (a child
communicating something back to its parent), through a different, more structured convention.

## Common Mistakes

- Mutating a prop directly inside a component, exactly the same real bug as in React — Vue warns
  about it explicitly, but the underlying reasoning for avoiding it is identical.
- Trying to pass a callback function as a plain prop the React way, rather than using Vue's
  `defineEmits`/`emit` convention, which is the idiomatic mechanism for this specific pattern.
- Forgetting `scoped` on a component's `<style>` block, letting its styles leak globally and
  potentially collide with another component's — the exact naming-collision problem
  [css-modules.md](../../react/styling-in-react/css-modules.md) exists to solve, here handled by a
  single attribute instead of a build-tool convention.

## Next

Continue to [vue-vs-react.md](vue-vs-react.md) to consolidate every comparison made throughout this
module into one direct summary.
