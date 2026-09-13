# HTML Accessibility

## Purpose

[accessibility-basics.md](../semantic-html-and-browser-rendering/accessibility-basics.md)
established that semantic HTML is accessibility's foundation. This module goes further: ARIA (for
the cases semantic HTML alone can't cover), keyboard navigation as a first-class requirement, and
the inclusive design principles that tie it all together.

## Learning Objectives

- Apply the "use native HTML first" rule, and know when ARIA is actually the right tool.
- Ensure any custom interactive component is fully operable by keyboard.
- Write meaningful alternative text and manage focus correctly in dynamic interfaces.
- Explain accessibility as a spectrum of user needs, not a single fixed checklist.

## Prerequisites

[Semantic HTML and Browser Rendering](../semantic-html-and-browser-rendering/), especially
[accessibility-basics.md](../semantic-html-and-browser-rendering/accessibility-basics.md).

## Files in This Module

| File | Covers |
|---|---|
| [aria-when-html-isnt-enough.md](aria-when-html-isnt-enough.md) | The first rule of ARIA, roles, states, and properties |
| [keyboard-navigation-and-focus-management.md](keyboard-navigation-and-focus-management.md) | Tab order, focus indicators, and managing focus in dynamic UI |
| [inclusive-design-principles.md](inclusive-design-principles.md) | Designing for the full range of ability and context, not a single "average" user |

## When to Deep-Dive vs. Skim

If you're building any custom interactive component (a dropdown, a modal, a tab panel) rather than
using native elements, deep-dive
[keyboard-navigation-and-focus-management.md](keyboard-navigation-and-focus-management.md) before
shipping it — keyboard operability failures are the single most common accessibility defect in
custom components.

## Quick Knowledge Check

<details>
<summary>What is the "first rule of ARIA"?</summary>

If a native HTML element or attribute already has the semantics and behavior you need, use it
instead of adding ARIA to a generic element. ARIA can describe a role to assistive technology, but
it never grants the native keyboard behavior that comes for free with the real element. See
[aria-when-html-isnt-enough.md](aria-when-html-isnt-enough.md).

</details>

<details>
<summary>Why is a visible focus indicator (the outline around a focused element) not optional?</summary>

It's the only way a keyboard-only user can tell which element is currently active — removing it
(a common but harmful CSS reset) makes a page effectively unusable without a mouse, even if every
element is technically still focusable. See
[keyboard-navigation-and-focus-management.md](keyboard-navigation-and-focus-management.md).

</details>

## References

- W3C WAI, [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/)
- MDN Web Docs, [ARIA](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA)
- W3C WAI, [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)

## Continue Your Learning Path

Next: [HTML Tables and Structured Data](../html-tables-and-structured-data/) — see the
[Frontend learning path](../../README.md) for the full sequence.
