# Classes and Inheritance

## Class Syntax

```js
class User {
  constructor(name, email) {
    this.name = name;
    this.email = email;
  }

  greet() {
    return `Hello, ${this.name}`;
  }
}

const ada = new User("Ada", "ada@example.com");
ada.greet(); // "Hello, Ada"
```

This is functionally very close to the constructor-function-plus-prototype pattern from
[constructors.md](constructors.md) — `class` is a more readable, purpose-built syntax over that
same underlying prototype mechanism, with real safety improvements: calling `User()` without `new`
now throws an explicit, immediate error, rather than silently misbehaving.

## Private Fields

```js
class BankAccount {
  #balance = 0; // genuinely private — inaccessible from outside this class

  deposit(amount) {
    this.#balance += amount;
  }

  getBalance() {
    return this.#balance;
  }
}

const account = new BankAccount();
account.#balance; // SyntaxError — truly inaccessible from outside
```

Fields prefixed with `#` are **genuinely private**, enforced by the language itself — this is real
encapsulation (see [oop-concepts.md](oop-concepts.md)), unlike a plain object property, which was
always accessible to any code holding a reference to the object.

## Inheritance with `extends` and `super`

```js
class Admin extends User {
  constructor(name, email, permissions) {
    super(name, email); // MUST run before `this` can be used below
    this.permissions = permissions;
  }

  greet() {
    return `${super.greet()} (Admin)`; // calls User's greet(), then extends it
  }
}

const admin = new Admin("Grace", "grace@example.com", ["manage-users"]);
admin.greet(); // "Hello, Grace (Admin)"
```

- **`extends`** establishes that `Admin` inherits from `User` — `Admin` instances have access to
  `User`'s methods automatically, unless overridden.
- **`super(...)`** calls the parent class's constructor — required before `this` can be accessed
  in a subclass's own constructor; JavaScript enforces this ordering strictly.
- **`super.methodName()`** calls the parent's version of an overridden method, letting a subclass
  extend rather than fully replace it.

## Static Members

```js
class User {
  static createGuest() {
    return new User("Guest", "guest@example.com");
  }
}

User.createGuest(); // called on the class itself, not an instance
```

`static` members belong to the class itself, not to individual instances — commonly used for
factory functions (like `createGuest` above) or utility methods conceptually related to the class
but not needing a specific instance to operate on.

## Common Mistakes

- Trying to use `this` in a subclass's constructor before calling `super()` — this throws a
  `ReferenceError`, by design, since the parent's initialization must complete first.
- Forgetting `super.methodName()` when overriding a method that should extend, not fully replace,
  the parent's behavior.
- Treating private fields (`#field`) as equivalent to a normal property with a naming convention
  (like a leading underscore) — `#` fields are enforced by the language itself, not just a team
  convention that can be bypassed.

## Module Summary

Across this module: OOP concepts (encapsulation, inheritance, polymorphism) apply to JavaScript,
but its underlying model is prototype-based rather than classically class-based (see
[oop-concepts.md](oop-concepts.md)); constructor functions plus `new` are the original mechanism
for creating similar objects, with real footguns (like forgetting `new`) that motivated a better
syntax (see [constructors.md](constructors.md)); and modern `class` syntax — with genuinely private
`#` fields, `extends`/`super` for inheritance, and `static` members — is the current, safer,
recommended way to write this same underlying pattern.
