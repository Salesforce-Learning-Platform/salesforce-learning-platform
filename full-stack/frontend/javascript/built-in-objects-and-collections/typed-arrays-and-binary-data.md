# 🧱 Typed Arrays and Binary Data

## When Text and Numbers Aren't Enough

Images, audio, files, compressed data, and many network protocols are sequences of **bytes**, not
strings or ordinary numbers. JavaScript handles them with **`ArrayBuffer`** (a block of raw memory)
and **typed arrays** (views that interpret that memory as a particular kind of number). Typed
arrays are the closest JavaScript comes to the C-style, fixed-size, contiguous arrays described in
[array-fundamentals.md](../../../data-structures-and-algorithms/arrays/array-fundamentals.md) — and
they appear whenever you work with files, `fetch` responses, canvas pixels, WebSockets, or
WebAssembly.

## 🧩 Buffers and Views

MDN's guide describes the split: an **`ArrayBuffer`** is raw binary data with no direct access, and
you read or write it through a **view** — a typed array or a `DataView`.

```js
const buf = new ArrayBuffer(8);        // 8 bytes of zeroed memory
const u8  = new Uint8Array(buf);       // view as 8 unsigned bytes
const u32 = new Uint32Array(buf);      // view as 2 unsigned 32-bit integers (same memory!)

u32[0] = 0x01020304;

console.log(buf.byteLength);           // 8
console.log(u8.slice(0, 4));           // Uint8Array(4) [ 4, 3, 2, 1 ]
console.log(u32.length, u8.length);    // 2 8
```

Writing through one view changes what every other view of the same buffer sees. Here the four bytes
come out as `4, 3, 2, 1` — the **byte order** of the machine that produced this output.

### The Types

| Constructor | Element | Bytes |
|-------------|---------|:-----:|
| `Int8Array`, `Uint8Array` | 8-bit integer | 1 |
| `Uint8ClampedArray` | 8-bit, values clamped to 0–255 | 1 |
| `Int16Array`, `Uint16Array` | 16-bit integer | 2 |
| `Int32Array`, `Uint32Array` | 32-bit integer | 4 |
| `Float32Array` | 32-bit float | 4 |
| `Float64Array` | 64-bit float (JavaScript's own `number`) | 8 |
| `BigInt64Array`, `BigUint64Array` | 64-bit `BigInt` | 8 |

`Uint8Array.BYTES_PER_ELEMENT` is `1`, `Int16Array`'s is `2`, `Float64Array`'s is `8`, and
`new Float64Array(4).byteLength` is `32`.

## 🔀 Endianness and `DataView`

Typed arrays use the platform's native byte order. Network protocols and file formats usually
specify one, so a **`DataView`** reads and writes with an explicit choice:

```js
const dv = new DataView(new ArrayBuffer(4));

dv.setUint32(0, 0x01020304);                    // default: big-endian
console.log(new Uint8Array(dv.buffer));         // Uint8Array(4) [ 1, 2, 3, 4 ]

dv.setUint32(0, 0x01020304, true);              // true = little-endian
console.log(new Uint8Array(dv.buffer));         // Uint8Array(4) [ 4, 3, 2, 1 ]
console.log(dv.getUint32(0, true) === 0x01020304);  // true
```

Use `DataView` whenever the byte order is part of a specification rather than an accident of the
machine.

## 🔁 Wrap-Around and Clamping

An element type has a fixed range, and out-of-range values do not throw — they wrap, or clamp:

```js
const u8 = new Uint8Array(1);
u8[0] = 256;  console.log(u8[0]);   // 0   — wrapped
u8[0] = 257;  console.log(u8[0]);   // 1

const i8 = new Int8Array(1);
i8[0] = 128;  console.log(i8[0]);   // -128

const clamped = new Uint8ClampedArray(2);
clamped[0] = 300;
clamped[1] = -5;
console.log(clamped);               // Uint8ClampedArray(2) [ 255, 0 ] — pinned to 0..255

const big = new BigInt64Array(1);
big[0] = 2n ** 63n;
console.log(big[0]);                // -9223372036854775808n — wrapped
```

`Uint8ClampedArray` exists mainly for canvas pixel data (`ImageData`), where a color channel must
stay within 0–255.

## 🆚 Not Quite Arrays

MDN lists the differences: typed arrays have a **fixed length**, so `push`, `pop`, and `splice` are
unavailable, and `Array.isArray` returns `false` — though they share most iteration methods:

```js
const u8 = new Uint8Array([1, 2, 3]);

console.log(Array.isArray(u8));          // false
console.log(typeof u8.push);             // undefined
console.log(Array.from(u8));             // [ 1, 2, 3 ]
console.log(u8.map((x) => x * 100));     // Uint8Array(3) [ 100, 200, 44 ] — results wrap to bytes!
```

Note the last line: `map` on a typed array returns a typed array of the *same type*, so
`300` wrapped to `44`.

### `subarray` Shares Memory; `slice` Copies

```js
const base = new Uint8Array([1, 2, 3, 4]);
const view = base.subarray(1, 3);      // a view onto the same buffer
const copy = base.slice(1, 3);         // an independent copy

view[0] = 99;

console.log(base);                           // Uint8Array(4) [ 1, 99, 3, 4 ] — changed through the view
console.log(copy);                           // Uint8Array(2) [ 2, 3 ]        — unaffected
console.log(view.buffer === base.buffer);    // true
console.log(copy.buffer === base.buffer);    // false
```

This is the same shared-reference behavior as shallow copies of objects, applied to raw memory — see
[copying-objects-shallow-vs-deep.md](../objects-in-depth/copying-objects-shallow-vs-deep.md).

## 🔤 Text Meets Bytes: `TextEncoder` and `TextDecoder`

Strings are UTF-16 internally ([strings-and-unicode.md](strings-and-unicode.md)), but files and
networks overwhelmingly use **UTF-8**. `TextEncoder` converts a string to UTF-8 bytes (a
`Uint8Array`), and `TextDecoder` converts back; MDN notes the encoder always uses UTF-8.

```js
const text = "héllo 😀";
const bytes = new TextEncoder().encode(text);

console.log(text.length);                    // 8   — UTF-16 code units
console.log(bytes.length);                   // 11  — UTF-8 bytes
console.log(bytes);                          // Uint8Array(11) [104, 195, 169, 108, 108, 111, 32, 240, 159, 152, 128]
console.log(new TextDecoder().decode(bytes)); // héllo 😀
```

The same text is 8 "characters" by `length` and 11 bytes on the wire — `é` takes 2 bytes in UTF-8, and
the emoji takes 4. Size limits on uploads and storage are measured in **bytes**, so measure with
`TextEncoder`, not `length`.

### Base64 and the `btoa` Trap

`btoa` and `atob` convert between binary strings and Base64, but `btoa` only accepts characters
that fit in one byte:

```js
console.log(btoa("é"), btoa("hello"));    // 6Q== aGVsbG8=
btoa("😀");                                // InvalidCharacterError: Invalid character
```

To Base64-encode arbitrary Unicode text, go through UTF-8 bytes first:

```js
function toBase64(text) {
  const bytes = new TextEncoder().encode(text);
  let binary = "";
  bytes.forEach((b) => (binary += String.fromCharCode(b)));
  return btoa(binary);
}

function fromBase64(b64) {
  const binary = atob(b64);
  const bytes = Uint8Array.from(binary, (c) => c.charCodeAt(0));
  return new TextDecoder().decode(bytes);
}

console.log(toBase64("😀"));                       // 8J+YgA==
console.log(fromBase64(toBase64("héllo 😀")));     // héllo 😀
```

## 📦 Where You Meet Binary Data

- **Files and `Blob`s** — `blob.arrayBuffer()` gives the bytes of a selected file.
- **`fetch`** — `response.arrayBuffer()` reads a binary response (see
  [fetch-api.md](../asynchronous-programming-and-modules/fetch-api.md)).
- **Canvas** — `ImageData.data` is a `Uint8ClampedArray` of pixel channels.
- **Crypto** — `crypto.getRandomValues` fills an integer typed array.
- **WebSockets, WebAssembly, audio** — all exchange `ArrayBuffer`s.
- **Float precision** — `new Float32Array([0.1])[0]` is `0.10000000149011612`: 32-bit floats
  carry fewer digits than JavaScript's 64-bit `number`.

## 🎤 Interview Angle

- **"What is the difference between an `ArrayBuffer` and a typed array?"** The buffer is raw bytes;
  a typed array is a view that interprets them as a particular numeric type. Multiple views can
  share one buffer.
- **"Is a typed array an `Array`?"** No — `Array.isArray` is `false`, and the length is fixed.
- **"What does `new Uint8Array([300])[0]` give?"** `44` — values wrap modulo 256.
- **"How do you convert a string to bytes?"** `new TextEncoder().encode(str)` yields UTF-8 bytes.

## Common Mistakes

- **Assuming a typed array's byte order** when a protocol specifies one — use `DataView`.
- **Expecting out-of-range values to throw** — they wrap (or clamp, for `Uint8ClampedArray`).
- **Using `str.length` for a size in bytes.**
- **Passing non-Latin-1 text straight to `btoa`.**
- **Forgetting that `subarray` is a view** and mutating the original through it.

## Module Summary

Across this module: **`Map` and `Set`** are purpose-built dictionary and unique-value collections
with any-type keys, guaranteed insertion order, SameValueZero equality, and fast lookups (see
[map-and-set.md](map-and-set.md)); **`WeakMap`, `WeakSet`, and `WeakRef`** hold objects without
keeping them alive, trading iteration for leak-free metadata caches (see
[weakmap-weakset-and-weakref.md](weakmap-weakset-and-weakref.md)); **strings** are UTF-16 code-unit
sequences, so `length`, slicing, and sorting need care around code points, grapheme clusters,
normalization, and locale (see [strings-and-unicode.md](strings-and-unicode.md)); **numbers** are
IEEE 754 doubles with famous precision limits, and `BigInt` handles integers beyond 2⁵³ (see
[numbers-math-and-bigint.md](numbers-math-and-bigint.md)); **`Date` and `Intl`** store UTC instants,
hide time-zone traps, and format values correctly for any locale (see
[dates-and-intl.md](dates-and-intl.md)); and **typed arrays** expose raw bytes through views, with
`TextEncoder` bridging strings and bytes (see this file).

## ➡️ Next

Continue to the Advanced Asynchronous Patterns module, the next module in this section, which builds
on promises and the event loop with combinators, cancellation, async iteration, scheduling, and Web
Workers.
