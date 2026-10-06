# ❄️ Freezing, Sealing, and Immutability

## Three Levels of Whole-Object Protection

[property-descriptors-and-getters-setters.md](property-descriptors-and-getters-setters.md) showed
per-property flags. JavaScript also offers three built-in operations that apply restrictions to an
**entire object** at once — and `Object.freeze` is simply the strictest, built from those same
flags. [pure-functions-and-immutability.md](../functional-javascript/pure-functions-and-immutability.md)
introduced `freeze` as a tool for immutable data; this file lays out exactly what each level
prevents.

## 📋 What Each Level Prevents

| Operation | Add properties | Delete properties | Change values | Reconfigure properties |
|-----------|:--------------:|:-----------------:|:-------------:|:----------------------:|
| *(normal object)* | yes | yes | yes | yes |
| `Object.preventExtensions(o)` | **no** | yes | yes | yes |
| `Object.seal(o)` | **no** | **no** | yes | **no** |
| `Object.freeze(o)` | **no** | **no** | **no** | **no** |

Reading the table top to bottom, each row is stricter than the one above. `preventExtensions` only
stops *new* properties; `seal` also locks the existing set of properties in place; `freeze`
additionally makes every data property read-only.

The results below come from running the same probes on each level:

```js
const mk = () => ({ name: "Ada" });

function probe(o) {
  o.extra = 1;                                  // try to add
  const added = "extra" in o;
  const deleted = delete o.name && !("name" in o);   // try to delete
  return { added, deleted };
}

console.log(probe(mk()));                           // { added: true,  deleted: true  }
console.log(probe(Object.preventExtensions(mk()))); // { added: false, deleted: true  }
console.log(probe(Object.seal(mk())));              // { added: false, deleted: false }
console.log(probe(Object.freeze(mk())));            // { added: false, deleted: false }
```

(These probes run in sloppy mode, where a refused operation is ignored or returns `false`. In strict
mode the same operations throw a `TypeError` instead.)

And for changing a value and reconfiguring a property:

```js
for (const [level, o] of Object.entries({
  normal: { a: 1 },
  preventExtensions: Object.preventExtensions({ a: 1 }),
  seal: Object.seal({ a: 1 }),
  freeze: Object.freeze({ a: 1 }),
})) {
  o.a = 2;
  console.log(level, "value changed:", o.a === 2);
}
// normal value changed: true
// preventExtensions value changed: true
// seal value changed: true
// freeze value changed: false
```

(Attempting `Object.defineProperty(o, "a", { enumerable: false })` succeeds on a normal and a
`preventExtensions` object, and throws on a sealed or frozen one.)

## 🔎 Checking the State

```js
const frozen = Object.freeze({ a: 1 });
console.log(Object.isExtensible(frozen), Object.isSealed(frozen), Object.isFrozen(frozen));
// false true true      — a frozen object is also sealed and non-extensible

const sealed = Object.seal({ a: 1 });
console.log(Object.isExtensible(sealed), Object.isSealed(sealed), Object.isFrozen(sealed));
// false true false     — sealed, but its values are still writable

console.log(Object.freeze(frozen) === frozen);   // true — freeze returns the SAME object
```

Note the last line: `Object.freeze` freezes the object **in place** and returns it; it does not
produce a frozen copy.

## 🚨 How Failures Show Up

Writes to a frozen object fail silently in sloppy mode and throw in
[strict mode](../execution-context-and-hoisting/strict-mode.md) (which includes modules and class
bodies). Some operations throw regardless of mode, such as the array methods that add elements:

```js
const arr = Object.freeze([1, 2]);

arr[0] = 99;
console.log(arr);        // [ 1, 2 ] — the assignment was silently ignored (sloppy mode)

arr.push(3);
// TypeError: Cannot add property 2, object is not extensible — thrown even in sloppy mode
```

The takeaway: don't rely on silent failure. If code must never modify an object, run it in strict
mode so a violation is an error rather than a mystery.

## 🪆 Freeze Is Shallow

As MDN states, `Object.freeze` applies only to an object's own immediate properties; nested objects
stay mutable unless they are frozen too. The recursive `deepFreeze` helper in
[pure-functions-and-immutability.md](../functional-javascript/pure-functions-and-immutability.md)
handles nested data, and the next file, [copying-objects-shallow-vs-deep.md](copying-objects-shallow-vs-deep.md),
covers the related shallow-versus-deep question for copies.

## 🧱 `const` vs. `Object.freeze`

They protect different things:

```js
const a = { n: 1 };
a.n = 2;
console.log(a);                 // { n: 2 } — const only fixes the BINDING; the object changed

const b = Object.freeze({ n: 1 });
b.n = 2;
console.log(b);                 // { n: 1 } — freeze protects the OBJECT
```

For a value that must be neither re-pointed nor modified, use both.

## 🧰 Typical Uses

**Constant lookup tables ("enums")** — a frozen object makes accidental edits no-ops:

```js
const Direction = Object.freeze({ UP: "up", DOWN: "down" });

Direction.UP = "sideways";     // ignored (sloppy mode) / TypeError (strict)
Direction.LEFT = "left";       // ignored: cannot add
console.log(Direction);        // { UP: 'up', DOWN: 'down' }
```

**Configuration objects** shared across a program, and **defensive returns** from a module that
exposes internal data it does not want callers to alter.

Accessors are unaffected in one respect: freezing makes *data* properties read-only, but a getter
still runs and returns whatever it computes:

```js
const o = Object.freeze({ get x() { return 1; } });
console.log(o.x, Object.isFrozen(o));   // 1 true
```

## 🎤 Interview Angle

- **"What is the difference between `preventExtensions`, `seal`, and `freeze`?"** Progressively
  stricter: no new properties; additionally no deleting or reconfiguring; additionally no changing
  values.
- **"Does `const` make an object immutable?"** No — it only prevents reassigning the variable;
  `Object.freeze` prevents changing the object.
- **"Is `Object.freeze` deep?"** No, it is shallow.
- **"What happens when you assign to a frozen object?"** Silently ignored in sloppy mode;
  `TypeError` in strict mode.

## Common Mistakes

- **Assuming `freeze` makes a copy** — it freezes the original object in place.
- **Assuming nested objects are frozen too.**
- **Relying on silent failure in sloppy mode** to catch bugs; run in strict mode instead.
- **Freezing objects that other code legitimately needs to update** — and then debugging "why does
  my assignment do nothing?".
- **Confusing `seal` with `freeze`** — a sealed object's values can still change.

## ➡️ Next

Continue to [copying-objects-shallow-vs-deep.md](copying-objects-shallow-vs-deep.md) to see exactly
what a copy shares with its original, and the options for a truly independent one.
