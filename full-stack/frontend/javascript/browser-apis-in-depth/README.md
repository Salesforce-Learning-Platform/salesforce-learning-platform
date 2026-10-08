# 🌐 Browser APIs in Depth

## 📚 Overview

[Browser APIs](../using-browser-functionalities/browser-apis.md) introduced the idea that the browser —
not the JavaScript language — provides most of what front-end code touches. This module goes deep on
the browser APIs that real applications reach for beyond the DOM and storage: the observer APIs for
visibility, DOM changes, and size; `URL` and the History API; files, blobs, and the clipboard; the
performance APIs; debouncing and throttling; form validation and `FormData`; and the `XMLHttpRequest`
that came before `fetch`.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Use `IntersectionObserver`, `MutationObserver`, and `ResizeObserver` instead of scroll listeners and
  polling, and clean them up.
- Parse and build URLs with `URL` and `URLSearchParams`, and explain `pushState`, `replaceState`, and
  `popstate` well enough to sketch a client-side router.
- Read files with `Blob`/`File`/`FileReader`, create and revoke object URLs, and use the Clipboard API
  within its security rules.
- Measure code and page loads with `performance.now()`, marks/measures, and `PerformanceObserver`.
- Implement `debounce` and `throttle`, and choose correctly between them.
- Validate forms with the Constraint Validation API, collect values with `FormData`, and explain why
  client-side validation is never enough.
- Read and write `XMLHttpRequest` code and explain how it differs from `fetch`.

## 📋 Prerequisites

- [Browser APIs](../using-browser-functionalities/browser-apis.md) — why these APIs belong to the browser rather than the language.
- [Events](../events/) and [DOM Manipulation](../dom-manipulation/) — the observers, form handling, and routing here build on them.
- [Advanced Asynchronous Patterns](../advanced-async-patterns/) — timers, `AbortController`, and async iteration appear throughout.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [intersection-mutation-and-resize-observers.md](intersection-mutation-and-resize-observers.md) | The three observers, lazy loading, infinite scroll, `waitForElement`, and cleanup |
| [url-and-history-apis.md](url-and-history-apis.md) | `URL`, `URLSearchParams`, encoding, `pushState`/`popstate`, and a router skeleton |
| [files-blobs-and-clipboard.md](files-blobs-and-clipboard.md) | `Blob`, `File`, `FileReader`, object URLs, downloads, and the Clipboard API |
| [performance-apis.md](performance-apis.md) | `performance.now()`, user timing, `PerformanceObserver`, navigation and paint timing |
| [debouncing-and-throttling.md](debouncing-and-throttling.md) | Implementations, leading/trailing variants, and `requestAnimationFrame` throttling |
| [forms-and-constraint-validation.md](forms-and-constraint-validation.md) | `validity`, custom messages, `FormData`, submission, and the limits of client validation |
| [ajax-and-xmlhttprequest.md](ajax-and-xmlhttprequest.md) | XHR basics, `readyState`, errors, progress, and a comparison with `fetch`; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** the observers, URL/History, and debounce/throttle files if you build or interview for
front-end roles — "implement `debounce`", "how would you build infinite scroll", and "how does client-side
routing work" are standard questions, and each has a tested answer here.

**Skim** the XHR file unless you maintain older code, but read its error-handling section (HTTP errors
are not network errors), which applies to `fetch` as well. Read the form-validation file's security
section regardless.

## 🧠 Knowledge Check

<details>
<summary>What is the difference between debouncing and throttling, and which suits a search-as-you-type box?</summary>

Debouncing waits until the calls stop and then runs once, with the latest arguments; throttling runs at
most once per interval while calls keep arriving. A search box wants **debouncing** — only the final
text matters, so five keystrokes become one request after the user pauses. Throttling (or
`requestAnimationFrame`) suits continuous gestures such as scrolling, where regular updates during the
action matter.

</details>

<details>
<summary>Why doesn't <code>history.pushState()</code> trigger a <code>popstate</code> event, and what does that mean for a router?</summary>

`popstate` fires only when the user (or script) *moves through* history — Back, Forward, `go()`. Adding
an entry with `pushState` is the app's own action, so the browser does not notify it. A router must
therefore render the new view itself right after calling `pushState`, and separately listen for
`popstate` to render the correct view when the user navigates back or forward.

</details>

## 📚 References

- [MDN: Intersection Observer API](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API), [`MutationObserver`](https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver), and [`ResizeObserver`](https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserver) — the observer APIs.
- [MDN: `URL`](https://developer.mozilla.org/en-US/docs/Web/API/URL), [`URLSearchParams`](https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams), and [History API](https://developer.mozilla.org/en-US/docs/Web/API/History_API) — URLs and navigation without reloads.
- [MDN: `Blob`](https://developer.mozilla.org/en-US/docs/Web/API/Blob), [`FileReader`](https://developer.mozilla.org/en-US/docs/Web/API/FileReader), and [Clipboard API](https://developer.mozilla.org/en-US/docs/Web/API/Clipboard_API) — files and clipboard access, including the security requirements.
- [MDN: `performance.now()`](https://developer.mozilla.org/en-US/docs/Web/API/Performance/now), [`PerformanceObserver`](https://developer.mozilla.org/en-US/docs/Web/API/PerformanceObserver), and [`performance.mark()`](https://developer.mozilla.org/en-US/docs/Web/API/Performance/mark) — measurement APIs.
- [MDN: Constraint validation](https://developer.mozilla.org/en-US/docs/Web/API/Constraint_validation), [`ValidityState.tooShort`](https://developer.mozilla.org/en-US/docs/Web/API/ValidityState/tooShort), and [`FormData`](https://developer.mozilla.org/en-US/docs/Web/API/FormData) — form validation and values.
- [MDN: `XMLHttpRequest`](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest), [Using XMLHttpRequest](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest_API/Using_XMLHttpRequest), and [Using the Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) — XHR and its modern replacement.
- [Lodash: `debounce` and `throttle`](https://lodash.com/docs/#debounce) — a widely used, tested implementation with `leading`, `trailing`, and `maxWait`.
- [javascript.info: Mutation observer](https://javascript.info/mutation-observer), [URL objects](https://javascript.info/url), [File and FileReader](https://javascript.info/file), and [XMLHttpRequest](https://javascript.info/xmlhttprequest) — widely used walkthroughs.
- [W3Schools: JavaScript History API](https://www.w3schools.com/js/js_api_history.asp) and [JavaScript Validation API](https://www.w3schools.com/js/js_validation_api.asp) — beginner-friendly overviews.

## ➡️ Continue Your Learning Path

Continue to the Offline Storage and Real-Time Web APIs module, the next module in this section, which
covers IndexedDB, service workers and the Cache API, WebSockets, and Server-Sent Events.
