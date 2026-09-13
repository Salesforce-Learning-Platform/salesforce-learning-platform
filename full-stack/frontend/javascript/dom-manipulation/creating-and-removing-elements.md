# Creating and Removing Elements

## Creating an Element

```js
const li = document.createElement("li");
li.textContent = "New item";
```

`createElement` creates a new node **in memory only** — it doesn't appear anywhere on the page
until explicitly attached to the DOM tree.

## Attaching It to the Page

```js
const list = document.querySelector("ul");
list.appendChild(li);           // adds as the last child
list.prepend(li);                 // adds as the first child
list.insertBefore(li, list.firstChild); // inserts at a specific position
```

An element only becomes visible once it's actually inserted somewhere in the live DOM tree that's
itself part of the document — creating it alone has no visible effect.

## Removing an Element

```js
li.remove();                    // modern, direct removal
list.removeChild(li);             // older syntax, requires the parent
```

`element.remove()` is the modern, simpler form; `removeChild` (called on the *parent*) is the
older equivalent, still commonly seen in existing code.

## Building Multiple Elements Efficiently

```js
const fruits = ["apple", "banana", "cherry"];
const fragment = document.createDocumentFragment();

fruits.forEach(fruit => {
  const li = document.createElement("li");
  li.textContent = fruit;
  fragment.appendChild(li);
});

document.querySelector("ul").appendChild(fragment);
```

A **DocumentFragment** is an in-memory container for building up multiple nodes before inserting
them all at once. As covered in
[reflow-and-repaint.md](../../html/semantic-html-and-browser-rendering/reflow-and-repaint.md),
inserting elements one at a time directly into the live DOM can trigger a reflow per insertion;
building them off-DOM in a fragment first and inserting once avoids that repeated cost.

## Common Mistakes

- Creating an element and setting its properties, then forgetting to actually attach it to the DOM
  with `appendChild`/`prepend` — it simply never appears on the page.
- Inserting many elements one at a time directly into the live DOM in a loop, causing unnecessary
  repeated reflow, instead of batching them with a DocumentFragment first.
- Using `removeChild` on the wrong node's parent, or forgetting the modern, simpler `.remove()`
  exists and is usually sufficient.

## Module Summary

Across this module: the DOM is a live, mutable, in-memory tree that can diverge from the original
HTML source once JavaScript runs (see [dom-introduction.md](dom-introduction.md));
`querySelector`/`querySelectorAll` (using ordinary CSS selector syntax) are the modern, preferred
way to select elements, returning a single element or a NodeList respectively (see
[selecting-elements.md](selecting-elements.md)); `textContent` should be preferred over `innerHTML`
for anything derived from user input, to avoid a real XSS risk, and `classList` is the standard
tool for managing CSS classes (see
[manipulating-elements.md](manipulating-elements.md)); and creating elements requires an explicit
insertion step to become visible, with a DocumentFragment as the efficient way to batch multiple
insertions.
