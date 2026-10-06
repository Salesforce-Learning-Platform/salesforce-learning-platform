# 🏷️ Property Descriptors and Getters/Setters

## Every Property Has Attributes, Not Just a Value

[objects.md](../arrays-and-objects/objects.md) and [object-methods.md](../arrays-and-objects/object-methods.md)
treat a property as a name and a value. Underneath, each property also carries **attributes** that
decide whether it can be changed, listed, or deleted. Those attributes are what `Object.freeze`,
`for...in`, `JSON.stringify`, and class getters are built on, so understanding them explains a lot
of behavior that otherwise looks arbitrary.

## 📋 The Attributes

| Attribute | Applies to | Meaning |
|-----------|------------|---------|
| `value` | Data properties | The property's value |
| `writable` | Data properties | Whether the value can be changed by assignment |
| `get` / `set` | Accessor properties | Functions called when the property is read / written |
| `enumerable` | Both | Whether the property shows up in enumeration (`Object.keys`, `for...in`, spread) |
| `configurable` | Both | Whether the property can be deleted or its attributes changed |

A property is either a **data property** (`value` + `writable`) or an **accessor property**
(`get` + `set`) — never both. MDN notes that a descriptor with both `value` and `get`/`set` throws a
`TypeError`.

## 🔍 Reading a Descriptor

```js
const user = { name: "Ada" };

console.log(Object.getOwnPropertyDescriptor(user, "name"));
// { value: 'Ada', writable: true, enumerable: true, configurable: true }
```

A property created by ordinary assignment or an object literal has all three flags set to `true`.

## ✍️ Defining a Property — and the Surprising Defaults

`Object.defineProperty` gives precise control — and its defaults are the *opposite* of assignment.
MDN: through `defineProperty`, any flag you omit is `false`:

```js
Object.defineProperty(user, "id", { value: 42 });

console.log(Object.getOwnPropertyDescriptor(user, "id"));
// { value: 42, writable: false, enumerable: false, configurable: false }
```

## ⚙️ What Each Flag Does

### `writable: false` — a read-only value

```js
user.id = 99;
console.log(user.id);   // 42
```

In sloppy mode the assignment is silently ignored; in
[strict mode](../execution-context-and-hoisting/strict-mode.md) it throws
`TypeError: Cannot assign to read only property 'id' of object '#<Object>'`.

### `enumerable: false` — hidden from enumeration, still accessible

```js
const o = { name: "Ada" };
Object.defineProperty(o, "id", { value: 42, enumerable: false });

console.log(Object.keys(o));                 // [ 'name' ]
console.log(JSON.stringify(o));              // {"name":"Ada"}
console.log({ ...o });                       // { name: 'Ada' }
console.log(Object.getOwnPropertyNames(o));  // [ 'name', 'id' ]
console.log(Reflect.ownKeys(o));             // [ 'name', 'id' ]
for (const key in o) console.log(key);       // name
console.log(o.id);                           // 42 — still readable directly
```

Per MDN's enumerability reference, `for...in`, `Object.keys`, `Object.entries`, `Object.assign`, and
spread all skip non-enumerable properties, while `Object.getOwnPropertyNames` and `Reflect.ownKeys`
include them; `JSON.stringify` ignores them too. That explains why a "hidden" property survives
direct access but vanishes from copies and serialized output.

### `configurable: false` — locked in place

```js
Object.defineProperty(o, "code", { value: 1 });

console.log(delete o.code);   // false — silently refused (a TypeError in strict mode)
Object.defineProperty(o, "code", { value: 2 });
// TypeError: Cannot redefine property: code
```

There are two narrow exceptions: a non-configurable property may still have its `value` changed if
it is writable, and `writable` may be switched from `true` to `false` (never back):

```js
Object.defineProperty(o, "x", { value: 1, writable: true });
Object.defineProperty(o, "x", { writable: false });   // allowed — one-way

console.log(Object.getOwnPropertyDescriptor(o, "x"));
// { value: 1, writable: false, enumerable: false, configurable: false }
```

## 📑 Copying Properties Exactly

Spread and `Object.assign` *read* each value, so an accessor becomes a plain data property in the
copy. To preserve the attributes themselves, copy the descriptors:

```js
const src = { get now() { return "computed"; } };

const spreadCopy = { ...src };
console.log(Object.getOwnPropertyDescriptor(spreadCopy, "now"));
// { value: 'computed', writable: true, enumerable: true, configurable: true } — getter lost

const exact = Object.defineProperties({}, Object.getOwnPropertyDescriptors(src));
console.log(typeof Object.getOwnPropertyDescriptor(exact, "now").get);   // "function" — preserved
```

## 🔁 Accessor Properties: Getters and Setters

An **accessor property** runs a function when it is read (`get`) or assigned (`set`), while looking
like an ordinary property to the caller:

```js
const circle = {
  radius: 5,
  get area() {
    return Math.PI * this.radius ** 2;       // computed on every read
  },
  get diameter() {
    return this.radius * 2;
  },
  set diameter(d) {
    this.radius = d / 2;                      // assignment updates the real data
  },
};

console.log(circle.area.toFixed(2));    // 78.54
circle.diameter = 20;
console.log(circle.radius);             // 10
console.log(circle.diameter);           // 20
```

Two behaviors to know:

```js
// 1. A property with only a getter ignores writes (sloppy) or throws (strict):
const o = { get x() { return 1; } };
o.x = 5;                  // strict mode: TypeError: Cannot set property x of #<Object> which has only a getter

// 2. Own accessors defined in an object literal ARE serialized by JSON.stringify, using the getter:
console.log(JSON.stringify(circle));
// {"radius":10,"area":314.1592653589793,"diameter":20}
```

### The Classic Setter Bug

A setter must store its value somewhere *other than* the property it guards — otherwise it calls
itself:

```js
const bad = { set x(v) { this.x = v; } };
bad.x = 1;   // RangeError: Maximum call stack size exceeded
```

## 🏛️ Accessors in Classes

Accessors written in a class body are the usual way to validate on assignment or expose a derived
value. Here the stored value lives in a private field (see
[private-class-fields.md](private-class-fields.md)):

```js
class Temperature {
  #celsius = 0;

  get celsius() { return this.#celsius; }
  set celsius(value) {
    if (typeof value !== "number" || Number.isNaN(value)) {
      throw new TypeError("celsius must be a number");
    }
    this.#celsius = value;
  }

  get fahrenheit() { return this.#celsius * 9 / 5 + 32; }
}

const t = new Temperature();
t.celsius = 100;
console.log(t.fahrenheit);                // 212
console.log(Object.keys(t));              // []
console.log(JSON.stringify(t));           // {}

t.celsius = "hot";                        // TypeError: celsius must be a number
```

Notice `JSON.stringify(t)` is `{}`: accessors declared in a **class body live on the prototype**, not
on the instance, and are non-enumerable — so unlike the object-literal `circle` above, they are not
serialized. (`Object.keys(Temperature.prototype)` is `[]`, while
`Object.getOwnPropertyDescriptor(Temperature.prototype, "celsius").get` is a function.)

## 🧰 What This Is Used For

- **Derived values** that must always reflect current data (`area`, `fahrenheit`).
- **Validation on assignment**, as in `Temperature`.
- **Hiding helpers** from enumeration, copies, and JSON with `enumerable: false`.
- **Constants** with `writable: false`.
- **Framework reactivity.** Vue's reactivity guide notes that in Vue 3, getters/setters are used for
  refs while Proxies back reactive objects — see [proxy-and-reflect.md](proxy-and-reflect.md) and the
  repository's [Vue reactivity overview](../../vue/vue-fundamentals/template-syntax-and-reactivity.md).

## 🎤 Interview Angle

- **"What are property descriptors?"** The attributes — `value`, `writable`, `enumerable`,
  `configurable` (or `get`/`set`) — that govern each property. `Object.getOwnPropertyDescriptor`
  reads them and `Object.defineProperty` sets them.
- **"What are the defaults for `Object.defineProperty`?"** All flags default to `false`, unlike
  normal assignment where they are `true`.
- **"What is the difference between a getter and a method?"** A getter is invoked by plain property
  access (`obj.area`), with no parentheses.
- **"Why does `JSON.stringify` skip some properties?"** Non-enumerable properties are ignored, and
  class accessors live (non-enumerably) on the prototype.

## Common Mistakes

- **Forgetting the `defineProperty` defaults** and wondering why a new property is read-only and
  invisible to `Object.keys`.
- **Setting a property inside its own setter**, causing infinite recursion.
- **Expecting spread or `Object.assign` to copy getters** — they copy the *value* the getter returns.
- **Assuming class accessors appear in `JSON.stringify` output.**
- **Writing a getter with expensive work** and calling it in a loop — it runs on every read.

## ➡️ Next

Continue to [freezing-sealing-and-immutability.md](freezing-sealing-and-immutability.md) to see how
`Object.freeze`, `seal`, and `preventExtensions` combine these attributes into whole-object
protection.
