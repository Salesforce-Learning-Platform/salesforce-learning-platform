# 📚 Stack Fundamentals

## Last In, First Out

A **stack** is a collection where you can only add and remove items at **one end**, called the *top*. The item added most recently is the
first one removed — **Last In, First Out (LIFO)**. Think of a stack of plates: you put a clean plate on top and take the top plate when you
need one. You never pull from the middle.

```
        push(30)           pop() → 30
           │                  ▲
           ▼                  │
        ┌──────┐          ┌──────┐
 top ─▶ │  30  │   top ─▶ │  20  │
        │  20  │          │  10  │
        │  10  │          └──────┘
        └──────┘
```

The restriction is the point. Because a stack promises nothing except "most recent first", it can be implemented with the cheapest possible
operations — and that behaviour turns out to match a surprising number of problems: function calls, undo history, matching brackets,
evaluating expressions, and depth-first search. All outputs below were produced by running the code on CPython 3.9.

## ⚙️ The Operations

| Operation | Meaning | Cost |
|-----------|---------|------|
| `push(x)` | Place `x` on top | O(1) |
| `pop()` | Remove and return the top item | O(1) |
| `peek()` (or `top()`) | Look at the top item without removing it | O(1) |
| `is_empty()` / `len()` | Is there anything on the stack? | O(1) |

Popping or peeking an **empty** stack is an error ("stack underflow"); a stack with a fixed capacity pushed beyond that capacity is a
"stack overflow" (the same term used for runaway recursion — see [recursion-fundamentals.md](../recursion/recursion-fundamentals.md)).

## 🐍 A Stack in Python: Just Use a List

A Python `list` already has the two operations a stack needs: `append` pushes onto the end and `pop()` removes from the end. Both are
O(1) (amortized for `append`, as explained in [array-fundamentals.md](../arrays/array-fundamentals.md)).

```python
stack = []
stack.append(10)             # push
stack.append(20)
stack.append(30)
print(stack[-1])             # 30   — peek
print(stack.pop())           # 30   — pop
print(stack.pop(), stack)    # 20 [10]
```

The "top" is the **end** of the list, not the front: `pop(0)` would work but costs O(n), which defeats the purpose. A small wrapper class
gives the operations names and a clear error on underflow:

```python
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def is_empty(self):
        return not self._items

    def __len__(self):
        return len(self._items)

s = Stack()
for word in ["to", "be", "or"]:
    s.push(word)
print(s.pop(), s.pop(), len(s), s.is_empty())      # or be 1 False
try:
    Stack().pop()
except IndexError as error:
    print(error)                                    # pop from empty stack
```

### A Linked-List Stack

The same behaviour with [linked nodes](../linked-lists/singly-linked-lists.md): push and pop both work at the head, so both are O(1)
*without any resizing*, because there is no array to grow:

```python
class Node:
    __slots__ = ("value", "next")

    def __init__(self, value, next=None):
        self.value = value
        self.next = next

class LinkedStack:
    def __init__(self):
        self._top = None
        self._size = 0

    def push(self, item):
        self._top = Node(item, self._top)           # the new node points at the old top
        self._size += 1

    def pop(self):
        if self._top is None:
            raise IndexError("pop from empty stack")
        node = self._top
        self._top = node.next
        self._size -= 1
        return node.value

    def peek(self):
        if self._top is None:
            raise IndexError("peek at empty stack")
        return self._top.value

    def __len__(self):
        return self._size

ls = LinkedStack()
for n in (1, 2, 3):
    ls.push(n)
print(ls.pop(), ls.peek(), len(ls))     # 3 2 2
```

In Python the list version is simpler and faster; the linked version matters as an illustration that "stack" describes *behaviour*, not a
storage layout — it can sit on top of either.

## 🔎 Where Stacks Appear

### 1. The Call Stack

Every function call pushes a **frame** (arguments, local variables, return address); returning pops it. That is why deep recursion
overflows — the stack runs out of room. A recursion can always be rewritten with an explicit stack of your own, as
`flatten_iterative` does in [recursive-problem-solving.md](../recursion/recursive-problem-solving.md).

### 2. Matching Brackets

The bracket problem from [string-patterns.md](../strings/string-patterns.md) is the classic stack exercise: push each opener; when a closer
arrives it must match the *most recent* unmatched opener — the top of the stack. This version also reports **where** the first problem is:

```python
def check_brackets(text):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []                                       # holds (opening character, its index)
    for index, ch in enumerate(text):
        if ch in "([{":
            stack.append((ch, index))
        elif ch in pairs:
            if not stack or stack[-1][0] != pairs[ch]:
                return False, index                  # a closer with no matching opener
            stack.pop()
    if stack:
        return False, stack[-1][1]                   # the innermost opener that was never closed
    return True, None

print(check_brackets("{[()]}"))             # (True, None)
print(check_brackets("f(a[1], {b: 2})"))    # (True, None)   — other characters are ignored
print(check_brackets("(]"))                 # (False, 1)
print(check_brackets("((()"))               # (False, 2)
print(check_brackets("())"))                # (False, 2)
```

O(n) time and O(n) space in the worst case (all openers). This is what editors do to highlight a mismatched bracket.

### 3. Evaluating Postfix Expressions

Ordinary (infix) arithmetic, `3 + 4 * 2`, needs precedence rules. **Postfix** notation (also called Reverse Polish Notation) puts the
operator *after* its operands — `3 4 2 * +` — and needs no precedence rules or parentheses. A stack evaluates it in one pass: push numbers;
on an operator, pop the two most recent values, apply it, and push the result.

```python
def evaluate_postfix(tokens):
    stack = []
    for token in tokens:
        if token in ("+", "-", "*", "/"):
            if len(stack) < 2:
                raise ValueError("malformed expression")
            right = stack.pop()                      # the right operand was pushed last
            left = stack.pop()
            if token == "+":
                stack.append(left + right)
            elif token == "-":
                stack.append(left - right)
            elif token == "*":
                stack.append(left * right)
            else:
                stack.append(int(left / right))      # division truncating toward zero
        else:
            stack.append(int(token))
    if len(stack) != 1:
        raise ValueError("malformed expression")
    return stack[0]

print(evaluate_postfix("3 4 2 * +".split()))          # 11     — 3 + 4 * 2
print(evaluate_postfix("5 1 2 + 4 * + 3 -".split()))  # 14     — 5 + (1 + 2) * 4 - 3
print(evaluate_postfix("7 2 /".split()))              # 3
```

Pop the *right* operand first: it was pushed last. Getting that order wrong is harmless for `+` and `*` and silently wrong for `-` and `/`.

### 4. Converting Infix to Postfix

How do you get from `3 + 4 * 2` to `3 4 2 * +`? A second stack, holding *operators*, does it (a simplified form of Dijkstra's shunting-yard
algorithm). Numbers go straight to the output. An operator waits on the stack; before it is pushed, any operators already there with
**equal or higher precedence** are popped to the output first, since they must be applied earlier. Parentheses mark groups.

```python
PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2}

def infix_to_postfix(tokens):
    output, operators = [], []
    for token in tokens:
        if token in PRECEDENCE:
            while operators and operators[-1] != "(" and PRECEDENCE[operators[-1]] >= PRECEDENCE[token]:
                output.append(operators.pop())       # higher or equal precedence goes first (left-associative)
            operators.append(token)
        elif token == "(":
            operators.append(token)
        elif token == ")":
            while operators[-1] != "(":
                output.append(operators.pop())       # everything back to the matching "("
            operators.pop()                          # discard the "(" itself
        else:
            output.append(token)                     # a number
    while operators:
        output.append(operators.pop())
    return output

print(infix_to_postfix("3 + 4 * 2".split()))                    # ['3', '4', '2', '*', '+']
print(infix_to_postfix("( 1 + 2 ) * 4".split()))                # ['1', '2', '+', '4', '*']
print(infix_to_postfix("10 - 4 - 3".split()))                   # ['10', '4', '-', '3', '-']
print(evaluate_postfix(infix_to_postfix("2 * ( 3 + 4 ) - 5".split())))    # 9
```

The `>=` makes subtraction and division **left-associative**: `10 - 4 - 3` must mean `(10 - 4) - 3 = 3`, which the third output reflects. With
`>` it would produce `10 4 3 - -`, i.e. `10 - (4 - 3) = 9`. (Unbalanced parentheses make `operators[-1]` fail with `IndexError`; a
production parser checks for that and reports a syntax error.)

### 5. A Stack That Knows Its Minimum

*Design a stack with `push`, `pop`, `top`, and `minimum`, all in O(1).* Finding the minimum by scanning would be O(n). The trick: keep a second
stack that records, at each depth, **the smallest value at or below that depth**:

```python
class MinStack:
    def __init__(self):
        self._items = []
        self._minimums = []          # _minimums[i] = the smallest of _items[0..i]

    def push(self, value):
        self._items.append(value)
        self._minimums.append(value if not self._minimums else min(value, self._minimums[-1]))

    def pop(self):
        self._minimums.pop()
        return self._items.pop()

    def top(self):
        return self._items[-1]

    def minimum(self):
        return self._minimums[-1]

m = MinStack()
for value in (5, 3, 7, 3, 8):
    m.push(value)
print(m.minimum())                  # 3
m.pop(); m.pop()                    # removes 8, then the second 3
print(m.minimum())                  # 3    — the first 3 is still there
m.pop()                              # removes 7
m.pop()                              # removes the first 3
print(m.minimum())                  # 5
```

Because the minimum is stored *per level*, popping automatically restores the previous minimum — no recomputation. The price is O(n) extra
space. This "an auxiliary stack records history" idea recurs in the [monotonic stack](monotonic-stack.md) pattern.

### 6. Undo

An editor pushes each action onto a stack; **undo** pops the latest one and reverses it. (Redo is a second stack that receives what undo pops.)

```python
text = []                           # the document, as a list of characters
undo_stack = []                     # pairs of ("typed", character)

def type_char(ch):
    text.append(ch)
    undo_stack.append(("typed", ch))

def undo():
    action, ch = undo_stack.pop()
    if action == "typed":
        text.pop()                  # reverse the action

for ch in "hey":
    type_char(ch)
undo()
print("".join(text))                # he
```

## ✅ Verification

All of the structures above were checked against reliable references with thousands of random inputs. The tests below use the code in this
file: the bracket checker against a "delete matching pairs until nothing changes" method, the postfix pipeline against Python's own `eval`,
and `MinStack` against the built-in `min`.

```python
import random

random.seed(9)

def reduces_to_empty(text):                                  # an independent bracket checker
    brackets = "".join(ch for ch in text if ch in "()[]{}")
    previous = None
    while previous != brackets:
        previous = brackets
        brackets = brackets.replace("()", "").replace("[]", "").replace("{}", "")
    return brackets == ""

for _ in range(20000):
    text = "".join(random.choice("()[]{}ab") for _ in range(random.randint(0, 10)))
    assert check_brackets(text)[0] == reduces_to_empty(text), text

def random_expression(depth=0):                              # an infix token list using + - * and parentheses
    if depth > 3 or random.random() < 0.3:
        return [str(random.randint(0, 9))]
    left, right = random_expression(depth + 1), random_expression(depth + 1)
    op = random.choice("+-*")
    group = lambda tokens: ["("] + tokens + [")"] if len(tokens) > 1 and random.random() < 0.7 else tokens
    return group(left) + [op] + group(right)

for _ in range(5000):
    tokens = random_expression()
    expected = eval(" ".join(tokens))
    assert evaluate_postfix(infix_to_postfix(tokens)) == expected, tokens

ms, values = MinStack(), []
for _ in range(20000):
    if values and random.random() < 0.45:
        assert ms.pop() == values.pop()
    else:
        value = random.randint(-20, 20)
        ms.push(value)
        values.append(value)
    if values:
        assert ms.minimum() == min(values) and ms.top() == values[-1]
print("brackets, infix-to-postfix evaluation, and MinStack agree with their references")
```

```text
brackets, infix-to-postfix evaluation, and MinStack agree with their references
```

## ⚖️ Stack Cost Summary

| Implementation | push | pop | peek | Notes |
|----------------|------|-----|------|-------|
| Python `list` (`append`/`pop`) | O(1) amortized | O(1) | O(1) | Simplest and fastest in Python |
| Linked list (at the head) | O(1) | O(1) | O(1) | No resizing; extra memory per node |
| `collections.deque` (`append`/`pop`) | O(1) | O(1) | O(1) | Also fine; useful if you need both ends |

## Common Mistakes

- **Using `pop(0)` / `insert(0, …)` on a list** as a stack — the top should be the *end* of the list.
- **Popping or peeking an empty stack** without checking (`IndexError`). Decide whether to check first or to catch the error.
- **Popping operands in the wrong order** when evaluating postfix expressions (subtraction and division expose it).
- **Forgetting to check the stack is empty at the end** of bracket matching — leftover openers mean the text is unbalanced.
- **Mixing up "top of the stack" and "front of the list"**, especially when printing a stack.
- **Treating a stack as random-access**: if you need the middle, a stack is the wrong structure.

## ➡️ Next

Continue to [queue-fundamentals.md](queue-fundamentals.md) for the mirror-image structure: first in, first out.
