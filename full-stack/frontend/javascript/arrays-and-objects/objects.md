# Objects

## Object Literals

```js
const user = {
  name: "Ada",
  age: 36,
  isActive: true,
};
```

An object is a collection of key-value pairs (**properties**). Keys are strings (or Symbols)
though usually written without quotes when they're valid identifiers.

## Accessing Properties

```js
user.name;         // "Ada" — dot notation
user["name"];        // "Ada" — bracket notation
user[dynamicKey];      // bracket notation required for a computed/variable key

user.address;         // undefined — accessing a missing property doesn't throw
user.address.city;     // TypeError — cannot read property of undefined
```

Bracket notation is required whenever the key is dynamic (stored in a variable) or isn't a valid
identifier (contains spaces, starts with a number). Accessing a missing property returns
`undefined` rather than throwing — but chaining further access onto that `undefined` does throw,
which is exactly the problem **optional chaining** (`user.address?.city`) exists to solve, covered
in the Modern JavaScript module.

## Nested Objects

```js
const user = {
  name: "Ada",
  address: {
    city: "London",
    country: "UK",
  },
};

user.address.city; // "London"
```

Objects can nest arbitrarily deeply — accessing a deeply nested value simply chains property
access, one level at a time.

## Adding, Updating, and Deleting Properties

```js
user.email = "ada@example.com"; // add
user.age = 37;                    // update
delete user.isActive;              // remove entirely
```

## Objects Are Compared by Reference

Exactly like arrays (see [arrays.md](arrays.md)), objects are compared by reference, not by their
contents:

```js
{ a: 1 } === { a: 1 }; // false — two different objects, even with identical contents
```

## Common Mistakes

- Chaining property access onto a value that might be `undefined` (`user.address.city` when
  `address` might not exist), causing a runtime `TypeError`.
- Assuming two objects with identical-looking contents are equal with `===` — they're only equal
  if they're literally the same object reference.
- Using bracket notation everywhere out of uncertainty, when dot notation is simpler and sufficient
  whenever the key is a fixed, valid identifier known at the time the code is written.

## Next

Continue to [object-methods.md](object-methods.md) for the built-in methods that operate on
objects as a whole.
