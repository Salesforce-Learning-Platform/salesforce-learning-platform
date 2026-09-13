# DOM Introduction

## What the DOM Actually Is

The **DOM (Document Object Model)** is the browser's live, in-memory, tree-structured
representation of a page — built by the browser during the parsing stage introduced in
[how-browsers-render-pages.md](../../html/semantic-html-and-browser-rendering/how-browsers-render-pages.md).
JavaScript interacts with the page exclusively through this DOM tree, using a global `document`
object as the entry point.

```text
document
  └── html
        ├── head
        │     └── title
        └── body
              ├── h1
              └── p
```

## The DOM Can Differ From the Original HTML

This is the single most important idea in this file: the DOM is **live and mutable**. Once
JavaScript runs, it can add, remove, or change nodes — meaning what's currently in the DOM can be
completely different from what was originally written in the HTML source file. Viewing a page's
source (`Ctrl`/`Cmd`+`U`) shows the *original* HTML; the browser DevTools' Elements panel (see
[browser-devtools-essentials.md](../../foundations/preparing-your-machine/browser-devtools-essentials.md))
shows the DOM's *current, live* state — these can genuinely diverge, and confusing the two is a
common source of "but the HTML says X" debugging confusion.

## Nodes and Elements

Every item in the DOM tree is a **node** — this includes actual HTML **elements**
(`<p>`, `<div>`), but also text content and comments, each as their own node type. "Element" refers
specifically to tag-based nodes; "node" is the broader term encompassing all of them.

## Why This Matters for JavaScript

Every DOM manipulation technique covered in this module — selecting, reading, modifying, creating,
removing — is really just reading or writing to this live tree. Understanding it as a genuine,
mutable, in-memory tree (not a static reflection of the HTML file) is what makes the rest of this
module's methods make sense, rather than feeling like a list of unrelated function calls to
memorize.

## Common Mistakes

- Debugging by re-reading the original HTML file when the actual problem is in what JavaScript
  changed at runtime — the DevTools Elements panel, not the source file, shows the current truth.
- Assuming "the DOM" and "HTML" are synonyms — HTML is a source format; the DOM is the live
  in-memory structure the browser builds from it and that JavaScript actually manipulates.
- Forgetting that text and comments are also DOM nodes, not just tag-based elements — relevant when
  a DOM traversal method returns more than expected.

## Next

Continue to [selecting-elements.md](selecting-elements.md) to start actually working with this
tree.
