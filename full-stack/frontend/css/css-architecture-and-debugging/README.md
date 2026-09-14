# 🏗️ CSS Architecture and Debugging

## Purpose

Every prior CSS module taught individual techniques — layout, Sass, frameworks. This module is
about **organizing** all of it at real-project scale: a naming convention that keeps a large
stylesheet predictable, a sensible folder structure, and the debugging skill to actually diagnose a
layout problem when one inevitably appears.

## 🎯 Learning Objectives

- Apply the BEM naming convention to avoid CSS naming collisions and unpredictable cascade effects.
- Design component-based CSS that stays predictable as a project grows.
- Choose between utility classes and component classes for a given situation.
- Organize a real-world CSS folder structure.
- Debug overflow and layout-shift issues directly with browser DevTools.

## 📋 Prerequisites

- [CSS Core Fundamentals](../css-core-fundamentals/) — specifically
  [specificity-and-cascade.md](../css-core-fundamentals/specificity-and-cascade.md), since this
  module's naming discipline exists specifically to keep specificity predictable.
- [CSS Frameworks](../css-frameworks/) — this module directly compares utility classes against
  component classes, building on both approaches already covered there.

## 📂 Files in This Module

| File | Covers |
|---|---|
| [bem-naming-convention.md](bem-naming-convention.md) | Block, Element, Modifier — the syntax and the real problem it solves |
| [component-based-css.md](component-based-css.md) | Designing reusable, predictable style blocks |
| [utility-classes-vs-component-classes.md](utility-classes-vs-component-classes.md) | Choosing between the two approaches, and combining them deliberately |
| [real-world-css-folder-structure.md](real-world-css-folder-structure.md) | Organizing `css/`, `components/`, `layout/`, `utilities/` in a real project |
| [debugging-with-devtools.md](debugging-with-devtools.md) | Inspecting overflow and layout shifts with browser DevTools |

## 🔍 When to Deep-Dive vs. Skim

Deep-dive [bem-naming-convention.md](bem-naming-convention.md) — a consistent naming discipline is
what actually prevents the specificity wars and unpredictable overrides that make large CSS
codebases painful; every other file in this module assumes that discipline is already in place.

## ✅ Quick Knowledge Check

<details>
<summary>In BEM, is .card__title--large valid syntax, and what does each part mean?</summary>

Yes — it's a **modifier on an element**: `card` is the block, `__title` names the element (an
element belonging to that block), and `--large` is a modifier describing a variation of that
specific element. What BEM doesn't support is chaining a second modifier directly onto an existing
modifier (there's no such thing as `--large--bold`); a class needs a separate modifier class for
each variation instead. See [bem-naming-convention.md](bem-naming-convention.md).

</details>

<details>
<summary>Should a whole page layout be built entirely from BEM-style component classes, or is mixing in utility classes ever appropriate?</summary>

Mixing is a completely normal, common real-world pattern — component classes (BEM or otherwise)
for a component's own identity and structure, with utility classes layered on for small, one-off
adjustments (spacing, alignment) that don't deserve their own named class. See
[utility-classes-vs-component-classes.md](utility-classes-vs-component-classes.md).

</details>

## 📚 References

- CSS-Tricks, [BEM 101](https://css-tricks.com/bem-101/)
- Chrome for Developers, [View and change CSS](https://developer.chrome.com/docs/devtools/css)
- W3Schools, [CSS Specificity](https://www.w3schools.com/css/css_specificity.asp)

## ➡️ Continue Your Learning Path

This is the final module in the CSS domain's Beyond Sigma expansion. See the
[Frontend learning path](../../README.md) for the remaining modules and what comes next.
