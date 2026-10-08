# 🎯 `this` and Prototype Puzzles

## 🧩 What These Puzzles Test

Two ideas generate most "tricky JavaScript" questions about objects:

- **`this` is decided by how a function is called**, not by where it was written. The same function can
  have a different `this` on every call.
- **Property lookup follows a prototype chain.** Reading finds the nearest object that has the property;
  writing usually creates a property on the object you wrote to.

The twelve puzzles below combine those two ideas in the ways interviewers favour: detached methods, arrow
functions, `bind` and `new`, shared prototype state, and inherited read-only properties.

Every answer was **produced by running the code** (three times, to confirm it is stable), and the
explanations link back to the concept files.

## 🛠️ How to Use This File

1. **Cover the answer** and predict the output.
2. **For every function call, find the call site and apply the rules in this order**:
   1. called with `new` → `this` is the new object;
   2. called through `call`, `apply`, or a `bind`-created function → `this` is the one given;
   3. called as `object.method()` → `this` is `object`;
   4. otherwise → `this` is `undefined` in strict mode, or the global object in sloppy mode.

   Arrow functions skip all four: they use the `this` of the code that *created* them.
3. **For property reads and writes**, walk the prototype chain, and remember that assignment writes to the
   object itself.

Some puzzles begin with `"use strict";` so that the answer does not depend on which runtime you use (in
sloppy mode, a plain call receives the global object, which differs between browsers and Node.js). Class
bodies are always strict. Error wording is V8's.

The concept files behind these puzzles are [this-keyword.md](../advanced-javascript/this-keyword.md),
[arrow-functions.md](../functions/arrow-functions.md),
[call-apply-and-bind.md](../functional-javascript/call-apply-and-bind.md),
[prototypes.md](../advanced-javascript/prototypes.md), and
[prototypal-inheritance.md](../advanced-javascript/prototypal-inheritance.md).

## 🧪 The Puzzles

### Puzzle 1 — The detached method

*Difficulty: ⭐ Warm-up*

```js
"use strict";

const user = {
  owner: "Ana",
  describe() {
    return this === undefined ? "no this" : this.owner;
  },
};

const detached = user.describe;

console.log(user.describe());
console.log(detached());
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
Ana
no this
```

`user.describe()` is a method call, so `this` is `user`. But `detached()` is a plain call: the function was
copied out of the object, and a plain call has no object in front of it. In strict mode that means `this`
is `undefined`.

In sloppy mode, `this` becomes the global object instead, so the function does not fail — it quietly reads
`globalThis.owner`, which is `undefined`. This is why lost-`this` bugs are often silent in older code and
loud in strict-mode code and classes. The same thing happens when you pass `user.describe` as a callback
(`setTimeout(user.describe, 0)`, an event listener, `array.map(user.describe)`).
See [this-keyword.md](../advanced-javascript/this-keyword.md) ("Losing `this`").

**Variation — The same code without strict mode**

```js
const user = {
  owner: "Ana",
  describe() {
    return this === undefined ? "no this" : this.owner;
  },
};

const detached = user.describe;

console.log(user.describe());
console.log(detached());
```

```text
Ana
undefined
```

</details>

### Puzzle 2 — Arrow property versus method property

*Difficulty: ⭐⭐ Interview standard*

```js
"use strict";

function Timer() {
  this.seconds = 0;
  this.tickArrow = () => ++this.seconds;
  this.tickMethod = function () {
    return ++this.seconds;
  };
}

const t = new Timer();
const { tickArrow, tickMethod } = t;

console.log(tickArrow(), t.seconds);

try {
  tickMethod();
} catch (e) {
  console.log(e.name + ": " + e.message);
}
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
1 1
TypeError: Cannot read properties of undefined (reading 'seconds')
```

An arrow function has no `this` of its own; it uses the `this` of the code that **created** it. `tickArrow`
was created inside the constructor, where `this` is the new `Timer`, so it keeps using that object even
after being pulled out of `t` by destructuring: it increments `t.seconds` (now `1`).

`tickMethod` is an ordinary function, so its `this` comes from the call. After destructuring, the call
`tickMethod()` has no receiver, `this` is `undefined` in strict mode, and `this.seconds` throws.

This is the trade-off behind the advice "use arrow functions for callbacks that need the outer `this`,
but not for object methods that should use the receiver." See
[arrow-functions.md](../functions/arrow-functions.md) ("The Real Difference: Lexical `this`").

</details>

### Puzzle 3 — `bind` and `new`

*Difficulty: ⭐⭐⭐ Tricky*

```js
function who() {
  return this && this.id;
}

const a = { id: "A" };
const b = { id: "B" };

const bound = who.bind(a);
console.log(bound(), bound.call(b), bound.apply(b));

const instance = new bound();
console.log(instance instanceof who, instance.id);
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
A A A
true undefined
```

`bind` creates a new function whose `this` is **fixed**. Trying to override it with `call` or `apply`
(`bound.call(b)`) has no effect: all three calls return `"A"`.

There is one exception: `new`. When a bound function is used as a constructor, the constructor call wins
and `this` is the freshly created object, so `bind`'s object is ignored. The new object has no `id`, and
because `who` returns `undefined` (a primitive), `new` returns the new object itself. It is an instance of
`who` (bound functions delegate to their target), and `instance.id` is `undefined`.

So the precedence is: `new` beats `bind`, and `bind` beats `call`/`apply`. See
[call-apply-and-bind.md](../functional-javascript/call-apply-and-bind.md) ("`bind` is permanent").

</details>

### Puzzle 4 — What `new` returns

*Difficulty: ⭐⭐ Interview standard*

```js
function A() {
  this.x = 1;
  return { y: 2 };
}

function B() {
  this.x = 1;
  return 42;
}

console.log(new A(), new B());
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
{ y: 2 } B { x: 1 }
```

A constructor called with `new` returns the new object — **unless** it explicitly returns another *object*.
`A` returns `{ y: 2 }`, an object, so that is what `new A()` gives you, and the work done on `this` is
discarded. `B` returns `42`, a primitive, which `new` ignores, so you still get the new `B` instance with
`x` set. (The `B { x: 1 }` notation is Node.js's way of showing an object created by the `B` constructor.)

</details>

### Puzzle 5 — Shadowing and deleting an inherited property

*Difficulty: ⭐⭐ Interview standard*

```js
function Animal() {}
Animal.prototype.sound = "generic";

const dog = new Animal();
dog.sound = "woof";
console.log(dog.sound, Animal.prototype.sound);

delete dog.sound;
console.log(dog.sound);

Animal.prototype.sound = "changed";
console.log(dog.sound);
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
woof generic
generic
changed
```

Assigning `dog.sound = "woof"` creates an **own** property on `dog` that *shadows* the prototype's `sound`;
it does not modify the prototype, which still holds `"generic"`. Deleting the own property removes the
shadow, so reads fall through to the prototype again (`"generic"`).

Because `dog` does not copy the prototype's properties — it looks them up when asked — changing
`Animal.prototype.sound` afterwards is visible through `dog` immediately (`"changed"`). The prototype chain
is a live link, not a snapshot. See [prototypes.md](../advanced-javascript/prototypes.md) ("Own Properties
vs. Inherited Properties").

</details>

### Puzzle 6 — State stored on the prototype

*Difficulty: ⭐⭐⭐ Tricky*

```js
function Basket() {}
Basket.prototype.items = [];

const b1 = new Basket();
const b2 = new Basket();

b1.items.push("apple");
console.log(b2.items, b1.items === b2.items, Object.hasOwn(b1, "items"));

b1.items = ["pear"];
console.log(b2.items, b1.items, Object.hasOwn(b1, "items"));
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
[ 'apple' ] true false
[ 'apple' ] [ 'pear' ] true
```

`b1.items.push("apple")` is a **read** followed by a method call: `b1.items` is found on the prototype,
and `push` mutates that one shared array. So `b2.items` also contains `"apple"`; both instances point at the
same array, and `b1` has no own `items`.

The second block is an **assignment** `b1.items = [...]`, and assignment creates an own property on `b1`.
Now `b1` has its own array, while `b2` still reads the shared one. Mutating shared prototype data is a
classic bug; per-instance data belongs in the constructor (`this.items = []`), with only methods on the
prototype. See [prototypal-inheritance.md](../advanced-javascript/prototypal-inheritance.md).

</details>

### Puzzle 7 — Replacing the prototype later

*Difficulty: ⭐⭐⭐ Tricky*

```js
function P() {}
P.prototype.hi = () => "old";

const early = new P();

P.prototype = { hi: () => "new" };

const late = new P();

console.log(early.hi(), late.hi(), early instanceof P, late instanceof P);
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
old new false true
```

An instance is linked to the prototype object that existed **when it was created**. `early` keeps its link
to the original object, so `early.hi()` is still `"old"`. Reassigning `P.prototype` points the *constructor*
at a new object; only instances created afterwards (`late`) use it.

`instanceof` checks whether `P.prototype` (as it is *now*) appears in the object's chain. For `early`, the
new `P.prototype` is not in its chain, so `early instanceof P` is `false` — even though `early` was created
by `new P()`. Adding properties to the existing prototype is safe; replacing it orphans old instances.

</details>

### Puzzle 8 — The method that forgets its object (classes)

*Difficulty: ⭐⭐ Interview standard*

```js
class Button {
  constructor() {
    this.label = "OK";
  }

  click() {
    return this.label;
  }
}

const btn = new Button();
const handler = btn.click;

try {
  handler();
} catch (e) {
  console.log(e.name + ": " + e.message);
}

console.log(handler.call(btn), btn.click.bind(btn)());
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
TypeError: Cannot read properties of undefined (reading 'label')
OK OK
```

Class bodies are always strict, so a detached method gets `this === undefined` and `this.label` throws a
`TypeError`. Supplying `this` explicitly with `call` or `bind` fixes it.

The variation shows the other common fix: defining the method as an **arrow-function class field**. The
arrow is created per instance, inside the constructor's context, so `this` is always that instance and
destructuring is safe. The trade-off is that each instance gets its own copy of the function instead of
sharing one on the prototype. See [classes.md](../advanced-javascript/classes.md).

**Variation — An arrow function as a class field**

```js
class Counter {
  count = 0;
  inc = () => ++this.count;
}

const { inc } = new Counter();
console.log(inc(), inc());
```

```text
1 2
```

</details>

### Puzzle 9 — `this` inside callbacks

*Difficulty: ⭐⭐ Interview standard*

```js
"use strict";

const team = {
  name: "Core",
  members: ["Ann", "Raj"],

  withFunction() {
    return this.members.map(function (m) {
      return this === undefined ? m + " (no this)" : this.name + ":" + m;
    });
  },

  withArrow() {
    return this.members.map((m) => this.name + ":" + m);
  },

  withThisArg() {
    return this.members.map(function (m) {
      return this.name + ":" + m;
    }, this);
  },
};

console.log(team.withFunction());
console.log(team.withArrow());
console.log(team.withThisArg());
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
[ 'Ann (no this)', 'Raj (no this)' ]
[ 'Core:Ann', 'Core:Raj' ]
[ 'Core:Ann', 'Core:Raj' ]
```

Each callback is an independent function with its own call. `map` calls a regular function callback as a
plain call, so `this` is `undefined` in strict mode (`withFunction`). The arrow callback has no `this` of its
own and uses the one from `withArrow`, which was called as `team.withArrow()`, so it is `team` (`withArrow`).

`map` (like `forEach`, `filter`, and others) also accepts a second argument, `thisArg`, which becomes `this`
for a regular function callback. Passing `this` there (`withThisArg`) gives the same result as the arrow.
Prefer the arrow; know `thisArg` because you will meet it in older code.

</details>

### Puzzle 10 — `this` is the receiver, not the owner

*Difficulty: ⭐⭐ Interview standard*

```js
const base = {
  name: "base",
  who() {
    return this.name;
  },
};

const kid = Object.create(base);
kid.name = "kid";

console.log(base.who(), kid.who(), base.who.call(kid));
console.log(Object.getPrototypeOf(kid) === base, Object.hasOwn(kid, "who"));
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
base kid kid
true false
```

`kid` has no `who` of its own, so `kid.who` finds the function on `base` through the prototype chain. But
`this` is determined by the object **in front of the dot at the call** — `kid` — not by the object where the
function happens to be stored. So `kid.who()` returns `kid.name` (`"kid"`), exactly like `base.who.call(kid)`.

That is what makes prototype methods work: one function on the prototype serves every instance, each call
seeing the instance it was invoked on. The second line confirms `base` is `kid`'s prototype and that `who`
is not an own property.

</details>

### Puzzle 11 — A read-only property on the prototype

*Difficulty: ⭐⭐⭐ Tricky*

```js
"use strict";

const proto = Object.freeze({ id: 1 });
const child = Object.create(proto);

try {
  child.id = 2;
} catch (e) {
  console.log(e.name + ": " + e.message);
}

console.log(child.id, Object.hasOwn(child, "id"));
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
TypeError: Cannot assign to read only property 'id' of object '#<Object>'
1 false
```

You might expect `child.id = 2` to simply create an own property that shadows the prototype's, as in the
`dog.sound` puzzle. But if an inherited property is **read-only** (here, because the prototype is frozen),
assignment is refused: the write does not create a shadowing property. In strict mode the refusal throws a
`TypeError`; in sloppy mode it is silently ignored, and `child.id` stays `1` with no own property. See
[freezing-sealing-and-immutability.md](../objects-in-depth/freezing-sealing-and-immutability.md) and
[property-descriptors-and-getters-setters.md](../objects-in-depth/property-descriptors-and-getters-setters.md).

If you really want a shadowing property, define it explicitly with `Object.defineProperty(child, "id", …)`,
which is not blocked by the inherited read-only flag (the last variation: `child` gets its own `id` of `2`
while the frozen prototype keeps `1`).

**Variation — The same code in sloppy mode**

```js
const proto = Object.freeze({ id: 1 });
const child = Object.create(proto);

child.id = 2;

console.log(child.id, Object.hasOwn(child, "id"));
```

```text
1 false
```

**Variation — Defining the shadowing property explicitly**

```js
"use strict";

const proto = Object.freeze({ id: 1 });
const child = Object.create(proto);

Object.defineProperty(child, "id", { value: 2, enumerable: true });

console.log(child.id, Object.hasOwn(child, "id"), proto.id);
```

```text
2 true 1
```

</details>

### Puzzle 12 — Who points at whom

*Difficulty: ⭐ Warm-up*

```js
function Car() {}
const c = new Car();

console.log(c.constructor === Car);
console.log(Car.prototype.constructor === Car);
console.log(Object.getPrototypeOf(c) === Car.prototype);
console.log(Object.getPrototypeOf(Car) === Function.prototype);
console.log(Object.getPrototypeOf(Car.prototype) === Object.prototype);
console.log(Object.getPrototypeOf(Object.prototype));
```

**Predict the output (and its order) before opening the answer.**

<details>
<summary>Show the answer</summary>

**Output:**

```text
true
true
true
true
true
null
```

Two different links exist, and confusing them is a classic interview slip:

- `Car.prototype` is an ordinary object that becomes the **prototype of instances** created with `new Car()`
  (line 3). Its `constructor` property points back at `Car` (line 2), which is why `c.constructor === Car`
  (line 1) — `c` finds `constructor` through the chain.
- `Car` is itself a function object, and *its* prototype is `Function.prototype` (line 4).
- `Car.prototype` is a plain object, so its prototype is `Object.prototype` (line 5), whose own prototype is
  `null` — the end of every ordinary chain (last line).

So the chain for `c` is: `c` → `Car.prototype` → `Object.prototype` → `null`. See
[prototypes.md](../advanced-javascript/prototypes.md) ("`prototype` vs. `__proto__` vs.
`Object.getPrototypeOf()`").

</details>

## 🧭 Patterns to Remember

| Pattern in the question | What to check |
|-------------------------|---------------|
| `const f = obj.method; f()` | Plain call: `this` is `undefined` (strict) or the global object (sloppy) |
| Arrow function created inside another function | Its `this` is the `this` of that outer function's call |
| `bind` then `call`/`apply` | Ignored: `bind` is permanent |
| `new` on a bound function | `new` wins; the bound `this` is ignored |
| A constructor that returns something | An object replaces `this`; a primitive is ignored |
| `obj.prop = value` where `prop` is inherited | Creates an own property — unless the inherited one is read-only |
| `obj.prop.push(…)` where `prop` is inherited | Mutates the shared inherited array |
| `Constructor.prototype = {…}` after creating instances | Old instances keep the old prototype |

## 🎤 Interview Angle

- **State the four call-site rules in order** (`new`, `call`/`apply`/`bind`, method call, default) and
  mention that arrows are the exception. That structure answers almost every `this` question.
- **Distinguish `prototype` from `__proto__`** (better: `Object.getPrototypeOf`). The first belongs to
  constructor functions; the second is the actual link on every object.
- **Mention classes are syntax over prototypes.** A `class` method lives on `Class.prototype`, and a class
  body is always strict — which is why detached class methods throw instead of misbehaving silently.
- **Expect "how would you fix it?"** Answers: `bind`, an arrow wrapper, an arrow class field, or calling the
  method through its object.

## Common Mistakes

- **Reading `this` from where the function was written** instead of how it was called.
- **Expecting an arrow function's `this` to change with `call` or `bind`.**
- **Putting mutable state (arrays, objects) on a prototype.**
- **Replacing `Constructor.prototype` after instances exist** and expecting them to update.
- **Assuming assignment always creates a property on the target object** — inherited read-only properties and setters change that.

## ➡️ Next

Continue to [coercion-and-equality-puzzles.md](coercion-and-equality-puzzles.md), which turns from objects
to the language's most notorious corner: automatic type conversion.
