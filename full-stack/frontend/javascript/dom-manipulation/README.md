# DOM Manipulation

## Purpose

The DOM (Document Object Model) is the browser's live, in-memory tree representation of a page —
introduced conceptually in
[how-browsers-render-pages.md](../../html/semantic-html-and-browser-rendering/how-browsers-render-pages.md).
This module covers using JavaScript to read and change that tree: selecting elements, creating and
removing them, and modifying their content and attributes.

## Learning Objectives

- Explain what the DOM is and how it relates to (and can differ from) the original HTML source.
- Select elements using `querySelector`/`querySelectorAll` and older selection methods.
- Read and modify element content, attributes, and classes.
- Create and remove elements programmatically.

## Prerequisites

[Semantic HTML and Browser Rendering](../../html/semantic-html-and-browser-rendering/) and
[JavaScript Arrays and Objects](../arrays-and-objects/).

## Files in This Module

| File | Covers |
|---|---|
| [dom-introduction.md](dom-introduction.md) | What the DOM is, and the DOM vs. HTML source distinction |
| [selecting-elements.md](selecting-elements.md) | `querySelector`, `querySelectorAll`, and older selection methods |
| [manipulating-elements.md](manipulating-elements.md) | Reading/changing text content, attributes, and classes |
| [creating-and-removing-elements.md](creating-and-removing-elements.md) | `createElement`, `appendChild`, and removing nodes |

## When to Deep-Dive vs. Skim

Deep-dive [dom-introduction.md](dom-introduction.md)'s explanation of why the DOM can differ from
the original HTML — this single idea explains a large share of "but the HTML file says X" confusion
when debugging a page that JavaScript has modified after load.

## Quick Knowledge Check

<details>
<summary>What does `document.querySelector(".card")` return if there are three elements with class "card" on the page?</summary>

Only the first one, in document order. Use `document.querySelectorAll(".card")` to get all of
them, returned as a NodeList. See [selecting-elements.md](selecting-elements.md).

</details>

<details>
<summary>What's the difference between `textContent` and `innerHTML`?</summary>

`textContent` treats its value as plain text (safe, and doesn't parse HTML); `innerHTML` parses the
assigned string as HTML markup — which means assigning unsanitized user input to `innerHTML` is a
genuine cross-site scripting (XSS) risk. See [manipulating-elements.md](manipulating-elements.md).

</details>

## References

- MDN Web Docs, [Document Object Model (DOM)](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model)
- MDN Web Docs, [`Document.querySelector()`](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector)

## Continue Your Learning Path

Next: [JavaScript Events](../events/) — see the
[Frontend learning path](../../README.md) for the full sequence.
