# Shadow DOM

## Attaching a Shadow Root

```js
class RatingStars extends HTMLElement {
  connectedCallback() {
    const shadow = this.attachShadow({ mode: "open" });
    shadow.innerHTML = `
      <style>
        span { color: goldenrod; }
      </style>
      <span>★★★★☆</span>
    `;
  }
}

customElements.define("rating-stars", RatingStars);
```

`attachShadow({ mode })` gives an element its own **Shadow DOM** — a separate DOM tree attached to
the element (the "shadow host") but rendered inline as part of the page. Anything appended inside
that shadow tree is invisible to, and unaffected by, the rest of the document's DOM and CSS.

## Open vs. Closed Mode

```js
const openHost = document.querySelector("#open-host");
const openShadow = openHost.attachShadow({ mode: "open" });
console.log(openHost.shadowRoot); // the ShadowRoot object — accessible

const closedHost = document.querySelector("#closed-host");
closedHost.attachShadow({ mode: "closed" });
console.log(closedHost.shadowRoot); // null — not accessible from outside
```

| Mode | `element.shadowRoot` from outside code | Typical use |
|---|---|---|
| `"open"` | Returns the `ShadowRoot` — inspectable and queryable | The vast majority of real components; used throughout this module |
| `"closed"` | Returns `null` | Rare; stronger encapsulation intent (not a real security boundary — dev tools can still inspect it) |

`"open"` is the default choice for nearly all real-world components, since fully hiding internals
from page code rarely matters and makes testing and debugging noticeably harder.

## Bidirectional CSS Encapsulation

```html
<style>
  /* Page-level CSS */
  span { color: blue; font-weight: bold; }
</style>

<rating-stars></rating-stars>
<!-- The <span> inside rating-stars's shadow DOM stays goldenrod —
     the page's `span` rule cannot reach across the shadow boundary. -->
```

This is the section worth sitting with: Shadow DOM's CSS isolation is a **browser-enforced
guarantee**, not a naming convention. Compare this against
[css-modules.md](../../react/styling-in-react/css-modules.md) and
[template-syntax-and-reactivity.md](../../vue/vue-fundamentals/template-syntax-and-reactivity.md)'s
Vue `<style scoped>`: both of those achieve scoping by having a *build tool* rewrite class names so
collisions become statistically unlikely. Shadow DOM achieves the same goal architecturally — there
is no rewriting, and no possible collision, because the two DOM trees are genuinely separate as far
as CSS selector matching is concerned. Neither direction leaks: page CSS can't style inside the
shadow tree, and CSS written inside the shadow tree can't style anything outside it.

## Common Mistakes

- Expecting global page styles (a CSS reset, a design system's base typography) to apply inside a
  shadow tree automatically — they don't; anything the component needs must be defined inside its
  own shadow DOM (or explicitly shared via a mechanism like constructable stylesheets).
- Choosing `mode: "closed"` by default out of a vague sense that it's "more secure" — it isn't a
  real security boundary, and it makes the component harder to test and debug for no real benefit
  in most cases.
- Assuming Shadow DOM also isolates JavaScript execution or global variables — it only isolates the
  DOM tree and CSS; a script inside a shadow tree still runs in the same JavaScript global scope as
  the rest of the page.

## Next

Continue to [templates-and-slots.md](templates-and-slots.md) to define a shadow tree's markup
declaratively and let consumers project their own content into it.
