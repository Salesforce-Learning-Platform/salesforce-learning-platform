# Route Parameters

## Defining a Dynamic Segment

```jsx
<Route path="/products/:productId" element={<ProductDetail />} />
```

A segment prefixed with `:` is a **dynamic segment** — it matches any value at that position in
the URL (`/products/42`, `/products/abc` both match), capturing the actual value for the matching
component to use.

## Reading the Parameter with `useParams`

```jsx
import { useParams } from "react-router";

function ProductDetail() {
  const { productId } = useParams(); // { productId: "42" } for a URL of /products/42
  return <p>Showing product {productId}</p>;
}
```

`useParams()` returns an object whose keys match the dynamic segment names from the matched route
— destructured (see
[destructuring.md](../../javascript/arrays-and-objects/destructuring.md)) exactly like props or
any other object.

## Parameters Are Always Strings

```jsx
const { productId } = useParams(); // "42" — a STRING, not a number
const numericId = Number(productId); // convert explicitly if numeric comparison/math is needed
```

URL segments are text by definition — `useParams()` never returns a number, even if the segment
looks numeric. Forgetting this and comparing `productId === 42` (a number) instead of `"42"` (the
actual string) is a real, easy-to-make bug — an instance of the type-coercion awareness from
[type-coercion.md](../../javascript/operators-and-type-system/type-coercion.md).

## Fetching Data Based on a Route Parameter

```jsx
function ProductDetail() {
  const { productId } = useParams();
  const [product, setProduct] = useState(null);

  useEffect(() => {
    fetchProduct(productId).then(setProduct);
  }, [productId]); // re-fetch whenever the URL's productId actually changes

  if (!product) return <p>Loading...</p>;
  return <h1>{product.name}</h1>;
}
```

This combines route parameters with the `useEffect` dependency-array discipline from
[dependency-array.md](../react-lifecycle-and-useeffect/dependency-array.md): including
`productId` in the dependency array ensures navigating from `/products/1` directly to
`/products/2` correctly re-fetches, rather than continuing to show the first product's stale data.

## Common Mistakes

- Comparing a route parameter directly against a number (`productId === 42`) without converting it
  first — `useParams()` values are always strings.
- Forgetting to include a route parameter in an effect's dependency array when the effect uses it
  to fetch data, causing stale data to persist after navigating to a different parameter value
  within the same rendered component.
- Assuming a dynamic segment can only appear at the end of a path — `:id` can appear anywhere in a
  route pattern, including in the middle (`/users/:userId/posts/:postId`).

## Next

Continue to [nested-routes.md](nested-routes.md) to share layout between multiple related routes.
