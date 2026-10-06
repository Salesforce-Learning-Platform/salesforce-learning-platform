# 🧬 Objects in Depth

## 📚 Overview

This module goes below the surface of JavaScript objects: the attributes every property carries
(`writable`, `enumerable`, `configurable`, getters and setters), the three levels of freezing, what
copying really shares, how JSON serialization behaves, language-level private fields, and the
`Proxy` and `Reflect` APIs for intercepting operations. Earlier modules treated objects as bags of
named values; this module explains the machinery that `Object.freeze`, `for...in`, `JSON.stringify`,
class getters, and reactive frameworks are built on.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Read and define property descriptors, and predict which properties show up in `Object.keys`,
  `JSON.stringify`, and spread.
- Write getters and setters in object literals and classes, and avoid the self-recursion trap.
- Choose between `preventExtensions`, `seal`, and `freeze`, and explain why none is deep.
- Make shallow and deep copies, and state what `structuredClone` and the JSON round-trip each lose.
- Use `JSON.stringify` and `JSON.parse` with replacers, revivers, and `toJSON`, and handle invalid
  input safely.
- Create truly private state with `#fields`, and explain how they differ from `_names`, closures, and
  TypeScript's `private`.
- Implement validation and observation with `Proxy`, and forward operations correctly with `Reflect`.

## 📋 Prerequisites

- [Objects](../arrays-and-objects/objects.md) and [Object Methods](../arrays-and-objects/object-methods.md) — the property basics this module builds beneath.
- [Classes](../advanced-javascript/classes.md) and [Prototypes](../advanced-javascript/prototypes.md) — getters, private fields, and copying behavior all involve class instances and the prototype chain.
- [Pure Functions and Immutability](../functional-javascript/pure-functions-and-immutability.md) — introduces `Object.freeze` and immutable updates, which this module examines in full.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [property-descriptors-and-getters-setters.md](property-descriptors-and-getters-setters.md) | The four property flags, `defineProperty` defaults, and accessor properties |
| [freezing-sealing-and-immutability.md](freezing-sealing-and-immutability.md) | `preventExtensions`, `seal`, and `freeze` compared, and what failure looks like |
| [copying-objects-shallow-vs-deep.md](copying-objects-shallow-vs-deep.md) | Shared references, shallow copies, `structuredClone`, and the lossy JSON trick |
| [json-serialization.md](json-serialization.md) | Valid JSON, `stringify` and `parse` options, and precision limits |
| [private-class-fields.md](private-class-fields.md) | `#private` syntax, enforcement, inheritance, brand checks, and gotchas |
| [proxy-and-reflect.md](proxy-and-reflect.md) | Traps, practical proxies, the receiver, and limits; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you are preparing for JavaScript interviews — "shallow vs. deep copy",
"`Object.freeze` vs. `const`", "how do you make a property private", and "what is a `Proxy`" are
standard questions, and this module has worked answers to each.

**Skim** the descriptor and JSON files if you already use `Object.defineProperty` and
`JSON.stringify` replacers confidently — but read the copying and Proxy gotchas, which trip up
experienced developers.

## 🧠 Knowledge Check

<details>
<summary>Why does <code>JSON.stringify</code> include a getter defined in an object literal but not one defined in a class body?</summary>

A getter in an object literal is an **own, enumerable** property of that object, so
`JSON.stringify` reads it and includes the computed value. A getter in a class body lives on the
**prototype** and is non-enumerable, so it is not an own property of the instance and is skipped.

</details>

<details>
<summary>What happens to a class instance when you pass it to <code>structuredClone</code>?</summary>

You get a plain object containing its own data properties. The prototype chain is not preserved, so
the clone is not an `instanceof` the class and has none of its methods; property descriptors such as
getters are flattened into plain values, and class private elements are not copied. Values the
algorithm cannot clone, such as functions, throw a `DataCloneError`.

</details>

## 📚 References

- [MDN: `Object.defineProperty()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty) — descriptor attributes and defaults.
- [MDN: Enumerability and ownership of properties](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Enumerability_and_ownership_of_properties) — which operations skip non-enumerable properties.
- [MDN: `Object.freeze()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/freeze) — freezing and shallowness.
- [MDN: The structured clone algorithm](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Structured_clone_algorithm) and [`structuredClone()`](https://developer.mozilla.org/en-US/docs/Web/API/Window/structuredClone) — what can and cannot be cloned.
- [MDN: `JSON.stringify()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify) and [`JSON.parse()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse) — serialization rules, replacers, and revivers.
- [MDN: Private elements](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Private_elements) — `#` syntax, errors, and brand checks.
- [MDN: `Proxy`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy) and [`Reflect`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Reflect) — traps, invariants, and the receiver.
- [Vue: Reactivity in Depth](https://vuejs.org/guide/extras/reactivity-in-depth.html) — how Vue 3 uses Proxies for reactive objects.
- [TypeScript Handbook: Classes](https://www.typescriptlang.org/docs/handbook/2/classes.html) — `private` is enforced only during type checking.
- [javascript.info: Property flags and descriptors](https://javascript.info/property-descriptors), [JSON methods](https://javascript.info/json), and [Proxy and Reflect](https://javascript.info/proxy) — widely used walkthroughs.
- [W3Schools: JavaScript JSON](https://www.w3schools.com/js/js_json.asp) — a beginner-friendly JSON introduction.

## ➡️ Continue Your Learning Path

Continue to the Built-in Objects and Collections module, the next module in this section, which
covers `Map` and `Set`, weak collections, strings, numbers, dates, and typed arrays.
