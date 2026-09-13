# CSS Syntax and Selectors

## Basic Rule Syntax

A CSS rule pairs a **selector** (what to target) with a **declaration block** (what to apply):

```css
selector {
  property: value;
  property: value;
}
```

```css
p {
  color: navy;
  font-size: 16px;
}
```

## Selector Types

| Selector | Targets | Example |
|---|---|---|
| Type | All elements of a tag | `p { }` |
| Class | Elements with a given class | `.card { }` |
| ID | The single element with a given id | `#header { }` |
| Attribute | Elements with a given attribute/value | `[type="email"] { }` |
| Universal | Every element | `* { }` |
| Descendant | Any matching element nested inside another | `article p { }` |
| Child | A direct child only | `ul > li { }` |
| Adjacent sibling | The element immediately following another | `h2 + p { }` |
| Pseudo-class | An element in a particular state | `a:hover { }` |
| Pseudo-element | A specific part of an element | `p::first-line { }` |

## Combining Selectors

Selectors can be combined for precision:

```css
nav ul li a          /* an <a> inside <li> inside <ul> inside <nav> */
.card.featured        /* an element with BOTH classes "card" and "featured" */
input:not([type="submit"])  /* any input except submit buttons */
```

## Grouping Selectors

Multiple selectors sharing the same declarations can be grouped with a comma, avoiding repetition:

```css
h1, h2, h3 {
  font-family: sans-serif;
}
```

## Common Mistakes

- Using an ID selector for styling that might need to be reused — IDs must be unique per page,
  which prevents applying the same rule to multiple elements, and (as covered in
  [specificity-and-cascade.md](specificity-and-cascade.md)) IDs carry high specificity that can make
  later overrides difficult.
- Confusing the descendant combinator (a space, meaning "anywhere inside") with the child combinator
  (`>`, meaning "direct child only") — these can select very different sets of elements.
- Forgetting the semicolon at the end of a declaration, which can cause the *next* declaration in
  the block to be parsed incorrectly.

## Next

Continue to [specificity-and-cascade.md](specificity-and-cascade.md) to see exactly how the
browser resolves conflicts when multiple selectors target the same element.
