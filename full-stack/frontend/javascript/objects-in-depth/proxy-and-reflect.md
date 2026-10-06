# 🪞 Proxy and Reflect

## Intercepting Operations on an Object

A **`Proxy`** wraps another object (the **target**) and lets you intercept fundamental operations on
it — reading a property, assigning one, checking `in`, deleting, calling it as a function — by
supplying a **handler** object whose methods are called **traps**. Operations with no trap are
forwarded to the target unchanged. This is the mechanism behind validation layers, observability,
and modern reactive frameworks.

```js
const proxy = new Proxy(target, handler);
```

MDN lists thirteen traps, corresponding to an object's internal operations:

| Trap | Intercepts |
|------|------------|
| `get` / `set` | Reading / writing a property |
| `has` | The `in` operator |
| `deleteProperty` | `delete obj.prop` |
| `ownKeys` | `Object.keys`, `Reflect.ownKeys`, and similar |
| `getOwnPropertyDescriptor` / `defineProperty` | Descriptor reads and definitions |
| `getPrototypeOf` / `setPrototypeOf` | Prototype access |
| `isExtensible` / `preventExtensions` | Extensibility checks and changes |
| `apply` / `construct` | Calling a function / using `new` on one |

## 🧪 Practical Examples

### A default value for missing keys

```js
const counts = new Proxy({}, {
  get(target, key) {
    return key in target ? target[key] : 0;
  },
});

counts.a++;
counts.a++;
counts.b++;
console.log(counts.a, counts.b, counts.zzz);   // 2 1 0
```

### Validation on assignment

```js
const person = new Proxy({}, {
  set(target, key, value) {
    if (key === "age" && !Number.isInteger(value)) {
      throw new TypeError("age must be an integer");
    }
    target[key] = value;
    return true;                     // signal that the assignment succeeded
  },
});

person.age = 36;
console.log(person.age);             // 36
person.age = "old";                  // TypeError: age must be an integer
```

The `return true` matters. A `set` trap that returns a falsy value reports failure: in strict mode
that becomes a `TypeError`.

```js
"use strict";
const p = new Proxy({}, { set(target, key, value) { target[key] = value; } });
p.a = 1;
// TypeError: 'set' on proxy: trap returned falsish for property 'a'
```

(In sloppy mode the assignment is quietly accepted.)

### Observing reads and writes

```js
const log = [];
const watched = new Proxy({ n: 1 }, {
  get(target, key, receiver) {
    log.push("get " + String(key));
    return Reflect.get(target, key, receiver);
  },
  set(target, key, value, receiver) {
    log.push("set " + String(key) + "=" + value);
    return Reflect.set(target, key, value, receiver);
  },
});

watched.n;
watched.n = 2;
console.log(log);   // [ 'get n', 'set n=2' ]
```

### A read-only view and hidden keys

```js
const readOnly = (obj) => new Proxy(obj, {
  set() { throw new TypeError("read-only"); },
  deleteProperty() { throw new TypeError("read-only"); },
});

const config = readOnly({ a: 1 });
try { config.a = 2; } catch (e) { console.log(e.message); }   // read-only
console.log(config.a);                                         // 1

const hidden = new Proxy({ a: 1, _b: 2, c: 3 }, {
  ownKeys(target) {
    return Reflect.ownKeys(target).filter((key) => !String(key).startsWith("_"));
  },
});
console.log(Object.keys(hidden), JSON.stringify(hidden));      // [ 'a', 'c' ] {"a":1,"c":3}
```

### Wrapping a function with `apply`

```js
const sum = (a, b) => a + b;
const traced = new Proxy(sum, {
  apply(target, thisArg, args) {
    console.log("call", args);
    return Reflect.apply(target, thisArg, args);
  },
});

console.log(traced(2, 3));   // logs "call [ 2, 3 ]", then 5
```

### Negative array indexes

```js
const arr = new Proxy([10, 20, 30], {
  get(target, key, receiver) {
    const i = Number(key);
    return Number.isInteger(i) && i < 0 ? target[target.length + i] : Reflect.get(target, key, receiver);
  },
});

console.log(arr[-1], arr[0], arr.length);   // 30 10 3
```

## 🔁 Reflect: The Default Behavior, as Functions

**`Reflect`** is a built-in namespace whose methods mirror the proxy traps one-for-one
(`Reflect.get`, `Reflect.set`, `Reflect.has`, `Reflect.deleteProperty`, `Reflect.apply`, …), so a
trap can perform the default operation with a single call. Two benefits over the matching `Object`
methods, per MDN: they take a **receiver** argument that controls `this` for getters and setters,
and they **return a boolean** instead of throwing:

```js
const frozen = Object.freeze({});

console.log(Reflect.defineProperty(frozen, "a", { value: 1 }));   // false
Object.defineProperty(frozen, "a", { value: 1 });
// TypeError: Cannot define property a, object is not extensible
```

### Why the Receiver Matters

When a property is a getter, `this` inside it should usually be the *proxy* — so that reads the getter
makes are also intercepted. Forwarding with `target[key]` ignores that; `Reflect.get(target, key,
receiver)` preserves it:

```js
const target = { _name: "Ada", get name() { return this._name; } };

const seen1 = [];
const p1 = new Proxy(target, {
  get(t, key) { seen1.push(String(key)); return t[key]; },
});
p1.name;
console.log("without receiver:", seen1);   // without receiver: [ 'name' ]

const seen2 = [];
const p2 = new Proxy(target, {
  get(t, key, receiver) { seen2.push(String(key)); return Reflect.get(t, key, receiver); },
});
p2.name;
console.log("with receiver:", seen2);      // with receiver: [ 'name', '_name' ]
```

Without the receiver, the getter's inner `this._name` read bypasses the proxy and goes unobserved.
Following the pattern `return Reflect.get(target, key, receiver)` (and the same for `set`) keeps
proxies faithful.

## 🏗️ Where Proxies Are Used for Real

Vue 3's reactivity system is built on this idea: per the Vue guide, Proxies back reactive objects,
with the `get` trap *tracking* which code reads each property and the `set` trap *triggering* that
code to re-run when a property changes — the same two traps used in the observer above. See
[Reactivity in Depth](https://vuejs.org/guide/extras/reactivity-in-depth.html) and the repository's
[Vue reactivity overview](../../vue/vue-fundamentals/template-syntax-and-reactivity.md). Proxies also
power validation layers, logging and debugging tools, and API-mocking libraries.

## ⚠️ Limits and Gotchas

**A proxy is not its target.**

```js
const target = {};
const proxy = new Proxy(target, {});
console.log(proxy === target);   // false
```

**Invariants are enforced.** A trap may not lie about certain facts; if it does, the engine throws.
For example, a read-only, non-configurable property must be reported with its true value:

```js
const t = {};
Object.defineProperty(t, "x", { value: 1, writable: false, configurable: false });

new Proxy(t, { get() { return 2; } }).x;
// TypeError: 'get' on proxy: property 'x' is a read-only and non-configurable data property
//            on the proxy target but the proxy did not return its actual value
//            (expected '1' but got '2')
```

**Built-ins and private fields rely on internal slots a proxy does not have.** A `Map` keeps its
data in internal state tied to the real object, so calling its methods with the proxy as `this`
fails — as does any class method that uses a `#private` field
([private-class-fields.md](private-class-fields.md)):

```js
const p = new Proxy(new Map(), {});
p.set("a", 1);
// TypeError: Method Map.prototype.set called on incompatible receiver #<Map>
```

The standard fix is to run methods against the target:

```js
const wrapped = new Proxy(new Map(), {
  get(target, key) {
    const value = Reflect.get(target, key, target);      // use the target as receiver
    return typeof value === "function" ? value.bind(target) : value;
  },
});

wrapped.set("a", 1);
console.log(wrapped.get("a"), wrapped.size);   // 1 1
```

**Revocable proxies.** `Proxy.revocable` returns a proxy together with a `revoke()` function that
permanently disables it — useful for handing out temporary access:

```js
const { proxy: temp, revoke } = Proxy.revocable({ a: 1 }, {});
console.log(temp.a);   // 1
revoke();
temp.a;                // TypeError: Cannot perform 'get' on a proxy that has been revoked
```

**Overhead.** Every intercepted operation runs your handler, so proxies cost more than direct
property access; measure before using one on a hot path.

## 🎤 Interview Angle

- **"What is a `Proxy`?"** An object that wraps a target and intercepts operations on it through a
  handler of traps such as `get`, `set`, `has`, and `deleteProperty`.
- **"Why use `Reflect` inside a trap?"** It performs the default operation correctly — including the
  receiver — and returns a boolean for success.
- **"How does Vue 3's reactivity work?"** Reactive objects are Proxies; the `get` trap records
  which effects read a property and the `set` trap re-runs them when it changes.
- **"What breaks when you proxy a `Map` or a class with private fields?"** Their internal slots and
  private names belong to the target, so methods called with the proxy as `this` throw a `TypeError`.

## Common Mistakes

- **Forgetting `return true` from a `set` trap**, which throws in strict mode.
- **Forwarding with `target[key]` instead of `Reflect.get(target, key, receiver)`**, losing the
  receiver.
- **Comparing a proxy to its target with `===`.**
- **Proxying built-ins or private-field classes** without binding methods to the target.
- **Using proxies where plain getters, setters, or functions would do** — they add indirection and
  overhead.

## Module Summary

Across this module: **property descriptors** — `value`, `writable`, `enumerable`, `configurable`, or
`get`/`set` — control how every property behaves, and `Object.defineProperty` defaults them all to
`false`, unlike assignment; accessors let a property compute or validate, and live on the prototype
when declared in a class (see
[property-descriptors-and-getters-setters.md](property-descriptors-and-getters-setters.md));
**`preventExtensions`, `seal`, and `freeze`** apply progressively stricter whole-object protection,
all shallow (see [freezing-sealing-and-immutability.md](freezing-sealing-and-immutability.md));
**copying** is shallow by default, with `structuredClone` as the built-in deep copy and the JSON
round-trip as a lossy alternative (see
[copying-objects-shallow-vs-deep.md](copying-objects-shallow-vs-deep.md)); **JSON** is a strict text
format whose `stringify` and `parse` have replacers, revivers, `toJSON`, and precision limits (see
[json-serialization.md](json-serialization.md)); **`#private` fields** give runtime-enforced
privacy with parse-time errors (see [private-class-fields.md](private-class-fields.md)); and
**`Proxy` and `Reflect`** intercept and forward operations — powering validation, observability, and
Vue 3's reactivity — within the limits that invariants, built-ins, and private fields impose (see
this file).

## ➡️ Next

Continue to the Built-in Objects and Collections module, the next module in this section, which
covers `Map` and `Set`, weak collections, strings, numbers, dates, and typed arrays.
