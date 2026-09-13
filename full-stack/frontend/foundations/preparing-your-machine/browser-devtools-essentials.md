# Browser DevTools Essentials

## Why DevTools Are Non-Negotiable

Every modern browser ships a full suite of developer tools ("DevTools"), and frontend engineering
is genuinely difficult to do well without them — they're how you verify what your code is actually
doing, as opposed to what you assume it's doing. This file covers the panels used constantly;
deeper coverage of specific workflows (network debugging, performance profiling) belongs to later,
more specialized modules.

## The Core Panels

| Panel | What it's for |
|---|---|
| **Elements** | Inspect and live-edit the rendered DOM and applied CSS |
| **Console** | Run JavaScript directly against the page, view logged output and errors |
| **Network** | See every request the page makes, with full timing and headers — the practical companion to [what-happens-when-you-enter-a-url.md](../how-the-internet-works/what-happens-when-you-enter-a-url.md) |
| **Application/Storage** | Inspect cookies, local storage, session storage, and cached data |
| **Sources** | View source files and set breakpoints to pause and step through JavaScript execution |

## Elements Panel

Shows the live DOM tree (which can differ from the original HTML source once JavaScript has run)
and, for any selected element, the full computed CSS — including which rule "won" under the
cascade and which were overridden. Edits made here are temporary (they don't change your actual
source files) but are invaluable for testing a CSS change before committing to it in code.

## Console Panel

Displays `console.log`/`console.error` output from your code and any errors thrown, and doubles
as a live JavaScript REPL against the current page — you can inspect a global variable, call a
function, or test an expression without modifying and re-running your source code.

## Network Panel

Lists every HTTP request the page makes, each with its method, status code, timing breakdown (DNS,
connection, TLS, waiting, download — directly mapping onto the sequence in
[what-happens-when-you-enter-a-url.md](../how-the-internet-works/what-happens-when-you-enter-a-url.md)),
and full request/response headers and bodies. This is the first place to check when a request
"isn't working" — it tells you definitively whether the request was even sent, what came back, and
exactly how long each phase took.

## Common Mistakes

- Debugging purely by inserting more `console.log` statements when a breakpoint in the Sources
  panel would let you inspect the actual live state at the moment of failure.
- Ignoring the Network panel when an API call misbehaves, and guessing about what was sent instead
  of simply looking at the actual request that went out.
- Not realizing that edits made directly in the Elements panel are temporary and disappear on
  reload — a common source of "I fixed it, but it's back" confusion.

## Module Summary

Across this module: comfort with the terminal is the foundation everything else in frontend
tooling assumes (see
[terminal-and-command-line-basics.md](terminal-and-command-line-basics.md)); Node.js and a package
manager install and run your project's dependencies and tooling reproducibly (see
[installing-a-package-manager-and-node.md](installing-a-package-manager-and-node.md)); a
well-configured editor with linting and formatting catches mistakes before you run anything (see
[setting-up-your-code-editor.md](setting-up-your-code-editor.md)); and browser DevTools are how you
verify what your code and network requests are actually doing, in practice.
