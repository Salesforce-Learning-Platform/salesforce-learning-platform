# 🔐 Private Class Fields

## Real Privacy in the Language

For most of JavaScript's history an object's properties were all public. The usual workaround was a
naming convention — `_balance` — which is only a polite request: nothing stops outside code from
reading or changing it. Closures
([iife-and-the-module-pattern.md](../functional-javascript/iife-and-the-module-pattern.md)) could
hide data but were awkward to combine with classes. **Private elements** — names starting with `#` —
make privacy a feature of the language itself. MDN lists them as widely available across browsers
since July 2021.

## ✍️ The Syntax

```js
class BankAccount {
  #balance = 0;                        // private field

  constructor(owner) {
    this.owner = owner;                // ordinary public property
  }

  deposit(amount) {
    this.#validate(amount);
    this.#balance += amount;
  }

  withdraw(amount) {
    this.#validate(amount);
    if (amount > this.#balance) {
      throw new RangeError("insufficient funds");
    }
    this.#balance -= amount;
  }

  get balance() {                      // a public, read-only view of the private value
    return this.#balance;
  }

  #validate(amount) {                  // private method
    if (!(amount > 0)) {
      throw new RangeError("amount must be positive");
    }
  }
}
```

Private elements can be fields, methods, accessors, and `static` members. The `#name` must be
**declared in the class body** before it is used.

```js
const account = new BankAccount("Ada");
account.deposit(100);
account.withdraw(30);

console.log(account.balance);          // 70
console.log(account["#balance"]);      // undefined — "#balance" is not an ordinary property name
console.log(Object.keys(account));     // [ 'owner' ]
console.log(JSON.stringify(account));  // {"owner":"Ada"}
console.log(Reflect.ownKeys(account)); // [ 'owner' ]

account.withdraw(500);                 // RangeError: insufficient funds
account.deposit(-5);                   // RangeError: amount must be positive
```

The private field is invisible to `Object.keys`, `JSON.stringify`, `Reflect.ownKeys`, spread, and
bracket access. Only code inside the class body can touch it.

## 🚫 How the Language Enforces It

Referencing a private name from outside the class is not a runtime failure you can catch — it is a
**syntax error**, rejected before the code runs:

```js
account.#balance;
// SyntaxError: Private field '#balance' must be declared in an enclosing class
```

The same error appears for a misspelled private name, and private elements cannot be deleted:

```js
class A { m() { return this.#nope; } }
// SyntaxError: Private field '#nope' must be declared in an enclosing class

class B { #x = 1; remove() { delete this.#x; } }
// SyntaxError: Private fields can not be deleted
```

Because the check is at parse time, typos are caught immediately — a real advantage over the
`_underscore` convention, where a misspelled property just yields `undefined`.

## 👪 Inheritance: Each Class Has Its Own Private Names

Per MDN, private elements are not inherited: a subclass cannot read its parent's private field, even
through `this`:

```js
class A { #secret = 1; }
class B extends A {
  read() { return this.#secret; }
}
// SyntaxError: Private field '#secret' must be declared in an enclosing class
```

The parent must expose what subclasses need through public (or conventionally protected) methods and
accessors:

```js
class A {
  #secret = 1;
  get secret() { return this.#secret; }
}
class B extends A {
  read() { return this.secret + 1; }
}

console.log(new B().read());   // 2
```

## 🔖 Brand Checks: Is This One of Mine?

Reading a private field from an object that does not have it throws a `TypeError`. The `in` operator
can ask first, giving a "brand check":

```js
class BankAccount {
  #balance = 0;
  static isAccount(obj) {
    return #balance in obj;      // true only for real instances of this class
  }
}

console.log(BankAccount.isAccount(new BankAccount())); // true
console.log(BankAccount.isAccount({}));                // false
```

## ⚠️ Gotchas

### Proxies cannot see private fields

A `Proxy` wrapping an instance is a different object, and private fields belong to the *target*.
MDN lists this as a critical caveat; calling a method that touches `#p` through a proxy throws:

```js
class A {
  #p = 1;
  get p() { return this.#p; }
}

const proxy = new Proxy(new A(), {});
proxy.p;
// TypeError: Cannot read private member #p from an object whose class did not declare it
```

See [proxy-and-reflect.md](proxy-and-reflect.md) for the workaround of binding methods to the target.

### Cloning and copying drop them

`structuredClone` does not carry over class private elements, and spread and `Object.keys` never
see them (see [copying-objects-shallow-vs-deep.md](copying-objects-shallow-vs-deep.md)):

```js
class A {
  #p = 1;
  x = 2;
  hasP(o) { return #p in o; }
}

const a = new A();
const c = structuredClone(a);

console.log(c);           // { x: 2 }
console.log(a.hasP(a));   // true
console.log(a.hasP(c));   // false
```

### Static private members

```js
class Counter {
  static #count = 0;
  static next() { return ++Counter.#count; }
}

console.log(Counter.next(), Counter.next());   // 1 2
```

## 🆚 Privacy Options Compared

| Approach | Truly private? | Notes |
|----------|----------------|-------|
| `_name` convention | No | Only a hint; easy to bypass or typo |
| Closures / module pattern | Yes | Awkward with classes; see the previous module |
| `#name` private elements | **Yes** — enforced by the language | Parse-time errors; unavailable to subclasses and proxies |
| TypeScript's `private` keyword | **No** — compile-time only | The TypeScript handbook states `private` is "only enforced during type checking"; the emitted JavaScript can still access it |

If you write TypeScript, the `#name` syntax gives you privacy that survives into the running code;
TypeScript's `private` keyword does not. See the repository's
[TypeScript essentials](../../typescript/typescript-essentials/) for the type-level view.

## 🎤 Interview Angle

- **"How do you make a property private in JavaScript?"** With a `#name` private field inside a
  class; before that, closures or a naming convention.
- **"Are private fields inherited?"** No — each class has its own private namespace; subclasses must
  use public accessors.
- **"What happens if you access `obj.#x` outside the class?"** A `SyntaxError`, caught before the
  code runs.
- **"Difference between `#x` and TypeScript's `private x`?"** `#x` is enforced at runtime by the
  language; `private` is erased and enforced only by the type checker.

## Common Mistakes

- **Using `_underscore` names and calling them private.**
- **Accessing a parent's private field from a subclass.**
- **Wrapping a class instance in a `Proxy`** and then calling methods that use private fields.
- **Expecting `JSON.stringify` or `structuredClone` to include private state.**
- **Assuming TypeScript's `private` keyword hides data at runtime.**

## ➡️ Next

Continue to [proxy-and-reflect.md](proxy-and-reflect.md) to see how to intercept and customize
property access on any object — including the limits that private fields place on it.
