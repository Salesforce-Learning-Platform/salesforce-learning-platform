# Vue vs. React: A Direct Comparison

## The Shared Foundation

Both frameworks solve the exact same core problem — declarative, component-based UI that updates
automatically when state changes — introduced identically in
[what-is-react.md](../../react/introduction-to-react/what-is-react.md) and
[what-is-vue.md](what-is-vue.md). Everything in the table below is a difference in *implementation
choice*, not a difference in the fundamental problem being solved.

## Side-by-Side

| Concept | React | Vue |
|---|---|---|
| Markup syntax | JSX — JavaScript with embedded HTML-like syntax | Templates — HTML with embedded directives (`v-if`, `v-for`) |
| Reactive state | `useState` + an explicit setter function | `ref()`/`reactive()`, mutated directly |
| Why re-rendering happens | Calling the setter function signals React explicitly | A Proxy-based system detects reads/writes automatically |
| Component file | `.tsx`/`.jsx`, logic and JSX together | `.vue` Single-File Component — template, script, and (optionally scoped) styles together |
| Conditional rendering | A ternary or `&&` inside JSX | `v-if` directive |
| List rendering | `.map()` inside JSX, with a `key` prop | `v-for` directive, with a `:key` binding |
| Child-to-parent communication | A callback function passed as a prop | `defineEmits`/`emit`, a distinct, named-event convention |
| Styling scoped to one component | A separate tool (CSS Modules, CSS-in-JS) | Built in, via `<style scoped>` |

## What This Comparison Actually Teaches

The genuinely valuable takeaway isn't memorizing this table — it's recognizing that **concepts
like "component," "props," "reactive state," and "conditional rendering" are universal problems in
UI development**, while the *specific mechanism* each framework uses to solve them (JSX vs.
templates, an explicit setter vs. a tracked Proxy) is a design choice, not an inherent requirement.
This is exactly the same reasoning skill applied throughout this platform to styling approaches
(from [the React domain's styling module](../../react/styling-in-react/)) and state-management
libraries (from
[Redux fundamentals](../../react/state-management-using-redux/redux-fundamentals.md)) — evaluating
a tool by the actual tradeoff it makes, not by treating it as an arbitrary set of syntax to
memorize.

## When You'd Actually Reach for Vue

- Joining or maintaining an existing team/codebase that has already standardized on Vue.
- A project wanting a lower floor for adoption — enhancing a single page incrementally, without
  necessarily committing to a full build pipeline from day one.
- A team that finds Vue's template-based, HTML-first syntax more approachable than JSX for members
  with a strong HTML/CSS background but less JavaScript-heavy experience.

Neither framework is objectively superior — exactly the same "match the tool to the actual
context" conclusion reached for styling and state-management choices earlier in this platform.

## Common Mistakes

- Trying to force React idioms into Vue code (or vice versa) rather than learning and using each
  framework's own idiomatic patterns.
- Treating this comparison as an argument for one framework being "better," rather than as a tool
  for recognizing which ideas are universal and which are implementation-specific.
- Assuming skills don't transfer between the two — the *conceptual* skills (component design,
  thinking in terms of state, prop interfaces) transfer directly; only the specific syntax differs.

## Module Summary

Across this module: Vue shares React's core "declarative UI driven by reactive state" foundation,
offering the Composition API (used throughout this module) as its closest analog to React's hooks
(see [what-is-vue.md](what-is-vue.md)); Vue's HTML-based templates with directives (`v-if`,
`v-for`, `v-bind`, `v-on`) replace JSX, and its `ref()`/`reactive()` reactivity is
Proxy-tracked rather than requiring an explicit setter function like `useState` (see
[template-syntax-and-reactivity.md](template-syntax-and-reactivity.md)); Single-File Components
bundle template, script, and scoped styles together, with props following the same read-only rule
as React but child-to-parent communication using the distinct `defineEmits`/`emit` convention (see
[components-and-props.md](components-and-props.md)); and the real value of learning a second
framework is recognizing which UI-development ideas are universal versus which are one framework's
specific implementation choice.
