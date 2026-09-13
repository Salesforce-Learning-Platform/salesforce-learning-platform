# Specificity and the Cascade

## Why This File Exists

More CSS debugging time is lost to "why isn't my style applying" than almost anything else, and
the answer is almost always resolvable by understanding two mechanisms precisely: the **cascade**
and **specificity**.

## The Cascade — Resolution Order

When multiple rules could apply to the same element, the browser resolves the conflict through a
defined sequence, roughly in this order of precedence:

1. **Origin and importance** — author styles (yours) normally beat browser default styles; `!important`
   flips normal precedence.
2. **Specificity** — a more specific selector beats a less specific one (detailed below).
3. **Source order** — if specificity is tied, the rule that appears later in the source wins.

Critically: **specificity is checked before source order**. A highly specific rule defined earlier
in a stylesheet still beats a less specific rule defined later — "the last rule in the file always
wins" is a common but incorrect simplification.

## Calculating Specificity

Specificity is commonly represented as a triplet of counts:

| Selector type | Weight |
|---|---|
| Inline style (`style="..."`) | Highest — beats any selector in a stylesheet |
| ID selectors (`#header`) | High |
| Class, attribute, and pseudo-class selectors (`.card`, `[type]`, `:hover`) | Medium |
| Type selectors and pseudo-elements (`div`, `::before`) | Low |
| Universal selector (`*`) | None |

```css
#nav .link { color: blue; }   /* 1 ID + 1 class → wins */
.link { color: red; }          /* 1 class → loses, regardless of source order */
```

Even though `.link { color: red; }` might appear after the first rule, `#nav .link` wins because
an ID contributes more specificity than a class, and specificity is compared before source order.

## `!important`

`!important` overrides normal cascade/specificity resolution entirely for that declaration — a
`!important` declaration wins over any non-`!important` one, regardless of specificity. It's
appropriate as a rare, deliberate escape hatch (commonly for utility classes designed to always
win), but overusing it defeats the predictability of the whole cascade system and makes future
overrides progressively harder — each new override may need its own `!important` to compete.

## A Practical Debugging Approach

When a style "isn't applying," use browser DevTools' Elements panel (see
[browser-devtools-essentials.md](../../foundations/preparing-your-machine/browser-devtools-essentials.md))
to inspect the element — it shows every matching rule, with overridden ones struck through,
directly answering which rule actually won and why, rather than guessing.

## Common Mistakes

- Reaching for `!important` as a first fix rather than understanding why the intended rule is
  losing the specificity comparison.
- Assuming source order alone determines the winner, ignoring that specificity is evaluated first.
- Chaining unnecessary selectors (`div.card.featured.active`) to "win" a specificity fight instead
  of addressing the actual structural conflict — this compounds the same problem for the next
  override.

## Next

Continue to
[inheritance-and-computed-styles.md](inheritance-and-computed-styles.md) to see the separate
mechanism that determines which values pass down to child elements at all.
