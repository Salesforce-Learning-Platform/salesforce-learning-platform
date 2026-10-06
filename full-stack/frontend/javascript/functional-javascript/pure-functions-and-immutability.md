# 🧼 Pure Functions and Immutability

## The Property That Makes Everything Else Safe

Composition, caching, and testing all work best when functions behave like mathematical functions:
the same inputs always give the same output, and nothing else in the program is disturbed. That
property has a name.

```
A PURE function:
  1. Returns the SAME result for the SAME arguments (it is deterministic), and
  2. Has NO SIDE EFFECTS — it does not change anything outside itself
     (no mutating its arguments, no modifying outer variables, no I/O).
```

React's documentation uses the same two-part definition ("minds its own business" and "same inputs,
same output") when explaining why components must be pure.

## 🔬 Impure Functions, Concretely

```js
let total = 0;
function addToTotal(n) {          // IMPURE: modifies a variable outside itself
  total += n;
  return total;
}

function today() {                 // IMPURE: result depends on when it is called
  return new Date().toDateString();
}

function randomId() {              // IMPURE: different result for the same (empty) input
  return Math.random();
}

function addItemImpure(cart, item) {   // IMPURE: mutates its argument
  cart.push(item);
  return cart;
}
```

The last one is the most common in real code, and the subtlest:

```js
const cart1 = ["apple"];
const result1 = addItemImpure(cart1, "pear");
console.log(cart1);              // [ 'apple', 'pear' ] — the caller's array changed
console.log(result1 === cart1);  // true — it returned the very same array
```

The pure version builds and returns a new array and leaves the input alone:

```js
const addItem = (cart, item) => [...cart, item];

const cart2 = ["apple"];
const result2 = addItem(cart2, "pear");
console.log(cart2);              // [ 'apple' ]
console.log(result2);            // [ 'apple', 'pear' ]
console.log(result2 === cart2);  // false — a new array
```

## 🎁 Why Purity Is Worth the Discipline

- **Easy to test** — call it with inputs, check the output; no setup, mocks, or cleanup.
- **Safe to cache** — a result can only be reused if the same arguments always give it; see
  [memoization.md](memoization.md).
- **Safe to compose** — steps in a [pipeline](function-composition-and-pipelines.md) cannot disturb
  each other.
- **Easy to reason about** — a call can be replaced by its result (*referential transparency*):
  `add(2, 3)` can be read as `5`.
- **Required by frameworks** — Redux reducers must be pure (see
  [actions-reducers-and-store.md](../../react/state-management-using-redux/actions-reducers-and-store.md)),
  and React assumes components are.

Side effects are not "bad" — every useful program needs I/O. The discipline is to keep the
*decision-making* logic pure and push effects (network, DOM, storage) to the edges.

## 🧱 Immutability: Update by Replacing, Not Changing

Purity forbids mutating arguments, so you need ways to produce modified *copies*. The spread syntax
does this for arrays and objects (see [array-methods.md](../arrays-and-objects/array-methods.md) for
which array methods mutate):

```js
const nums = [3, 1, 2];
const sorted = nums.sort();            // sort MUTATES and returns the same array
console.log(nums, sorted === nums);    // [ 1, 2, 3 ] true

const nums2 = [3, 1, 2];
console.log(nums2.toSorted(), nums2);  // [ 1, 2, 3 ] [ 3, 1, 2 ] — the non-mutating version
```

(`toSorted` and its siblings are newer additions — see the Modern JavaScript module's ES2020+
coverage — and `[...nums].sort()` is the long-standing alternative.)

### Updating nested data

Spread copies only one level, so a nested update copies each level on the path to the change:

```js
const state = {
  user: { name: "Ada", address: { city: "London" } },
  settings: { theme: "dark" },
};

const next = {
  ...state,
  user: { ...state.user, address: { ...state.user.address, city: "Paris" } },
};

console.log(state.user.address.city, next.user.address.city);  // London Paris
console.log(next.settings === state.settings);                  // true — untouched parts are shared
console.log(next.user === state.user);                          // false — the changed path was copied
```

Only the objects along the changed path are new; everything else is shared with the old state, so
copies stay cheap (this reuse is called *structural sharing*). For deeply nested updates the spread
chain gets verbose, and libraries such as [Immer](https://immerjs.github.io/immer/) let you write
code that appears to mutate a draft while producing an immutable result.

## ❄️ `Object.freeze` Is Shallow

`Object.freeze` prevents changes to an object's own properties — but MDN is explicit that it is
shallow:

```js
const frozen = Object.freeze({ name: "Ada", tags: ["a"] });

frozen.name = "Grace";      // ignored (sloppy mode) — a TypeError in strict mode
frozen.tags.push("b");      // works! the nested array is not frozen
console.log(frozen);        // { name: 'Ada', tags: [ 'a', 'b' ] }
```

In strict mode the first assignment throws `TypeError: Cannot assign to read only property 'name' of
object '#<Object>'` (see [strict-mode.md](../execution-context-and-hoisting/strict-mode.md)). To
freeze everything, recurse:

```js
function deepFreeze(value) {
  Object.values(value).forEach((child) => {
    if (typeof child === "object" && child !== null) {
      deepFreeze(child);
    }
  });
  return Object.freeze(value);
}

const config = deepFreeze({ name: "Ada", tags: ["a"] });
config.tags.push("b");   // TypeError: Cannot add property 1, object is not extensible
```

(This simple version does not handle circular references. Treat freezing as a development-time
guard; the Objects in Depth module, later in this section, covers freezing, sealing, and copying in
full.)

Remember too that `const` does not make a value immutable — it only prevents reassigning the
binding (see [variables.md](../introduction-to-javascript/variables.md)).

## 🎤 Interview Angle

- **"What is a pure function?"** One that always returns the same output for the same input and has
  no side effects.
- **"Is `array.sort()` pure?"** No — it sorts the array in place and returns that same array, so it
  mutates its input.
- **"What does `Object.freeze` not do?"** It is shallow: nested objects and arrays remain mutable.
- **"Why does React/Redux require immutable updates?"** They detect changes by comparing references;
  mutating in place leaves the reference unchanged, so changes are missed.

## Common Mistakes

- **Believing `const` makes data immutable.**
- **Mutating function arguments** (`push`, `sort`, assigning to properties) while claiming the
  function is pure.
- **Reading hidden inputs** — `Date.now()`, `Math.random()`, globals — inside logic that should be
  deterministic; pass them in as arguments instead.
- **Treating a shallow copy as a deep copy** — a spread of a nested object still shares the inner
  objects.
- **Assuming `Object.freeze` protects nested data.**

## ➡️ Next

Continue to [memoization.md](memoization.md) to put purity to work: caching a function's results so
repeated calls cost almost nothing.
