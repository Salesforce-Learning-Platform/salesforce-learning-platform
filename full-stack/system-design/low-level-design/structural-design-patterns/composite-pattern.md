# 🌲 Composite Pattern

## The Problem: Treating Individuals and Groups Differently

```python
# WITHOUT Composite - handling a Product and a Box of Products
# requires GENUINELY different logic for each
def calculate_total(item):
    if isinstance(item, Product):
        return item.price
    elif isinstance(item, Box):
        total = 0
        for sub_item in item.contents:   # RECURSING manually, and
            total += calculate_total(sub_item)   # the CALLER has to
        return total                                # know to do this
```

Per Refactoring.guru's own framing, this pattern makes sense specifically when a system's core
model can genuinely be represented as a *tree* — an order containing products, which can themselves
be grouped into boxes containing more products (or more boxes) — and handling "one item" vs. "a
group of items" with separate logic quickly becomes genuinely complex and error-prone.

## The Pattern: a Shared Interface for Both Leaves and Containers

```python
class OrderItem:
    def get_price(self) -> float: raise NotImplementedError

class Product(OrderItem):   # a LEAF - no children
    def __init__(self, price):
        self.price = price
    def get_price(self):
        return self.price

class Box(OrderItem):   # a CONTAINER - can hold OTHER OrderItems,
    def __init__(self):  # including OTHER Boxes
        self.contents: list[OrderItem] = []
    def add(self, item: OrderItem):
        self.contents.append(item)
    def get_price(self):
        return sum(item.get_price() for item in self.contents)   # RECURSES
                                                                     # automatically
```

```python
box = Box()
box.add(Product(10))
box.add(Product(25))

inner_box = Box()
inner_box.add(Product(5))
box.add(inner_box)   # a Box containing a Box containing a Product

print(box.get_price())   # 40 - the CALLER never needed to know or
                           # care about the actual NESTING depth at all
```

The caller simply calls `get_price()` — whether on a single `Product` or an arbitrarily deeply
nested `Box`, the exact same method call works identically, with the recursion handled entirely
*inside* the `Box` class itself.

## A Real Use Case: File Systems

```
A directory can contain FILES (leaves) or OTHER directories
(containers, which can themselves contain more files and
directories). Calculating a directory's total SIZE recursively
sums every file's size - the SAME "get_size()" call works
identically whether called on a single file or an entire,
deeply-nested directory tree.
```

This is directly Refactoring.guru's own canonical real-world example — and it's genuinely one of the
most common, intuitive real-world applications of a tree structure most developers already interact
with daily.

## Why This Directly Uses Polymorphism

```
This pattern is, in a genuine sense, a specific, practical
APPLICATION of the polymorphism concept already covered in
objects-and-classes.md, from LLD Foundations, earlier in this
domain - Product and Box share ONE interface, and the CALLER never
needs to know or check WHICH concrete type it's actually working
with.
```

## Common Mistakes

- Writing separate, type-checking logic (`isinstance` branches) for leaves vs. containers instead of
  letting the shared interface's polymorphism handle the distinction automatically.
- Applying Composite to a structure that isn't genuinely tree-shaped, adding unnecessary
  abstraction where a simpler, flat structure would already work fine.
- Letting a `Leaf` class silently accept `add()` calls (adding children) when leaves should
  genuinely never have children at all — this should fail clearly, not silently succeed.

## Module Summary

Across this module: **Adapter** translates between two genuinely incompatible interfaces without
modifying either side, verified against the canonical power-plug analogy (see
[adapter-pattern.md](adapter-pattern.md)); **Facade** provides a simple, unified interface hiding a
genuinely complex subsystem, distinguished from Adapter by solving a complexity problem rather than
a compatibility one (see [facade-pattern.md](facade-pattern.md)); **Proxy** controls access to an
object behind an identical interface — lazy-loading, access control, caching, or remote
representation — distinguished precisely from Decorator by managing access rather than extending
behavior (see [proxy-pattern.md](proxy-pattern.md)); **Decorator** adds optional, composable
behavior by wrapping objects in layers, directly solving the combinatorial-subclass-explosion
problem and extending Open-Closed to optional features (see
[decorator-pattern.md](decorator-pattern.md)); and **Composite** treats individual objects and
groups of objects uniformly through a shared interface, letting recursive tree operations (like a
file system's total size) work identically regardless of nesting depth (see
[composite-pattern.md](composite-pattern.md)).
