# ⏱️ Time and Space Complexity

## 📚 Overview

This module gives precise, formal shape to the performance differences already observed informally
in [Introduction to Data Structures and Algorithms](../introduction-to-data-structures-and-algorithms/):
Big-O notation, the practical rules for analyzing real code, and the full time and space complexity
picture every later module in this domain builds on when comparing data structures and algorithms.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Classify an algorithm's growth rate using Big-O notation, and explain why constants and
  lower-order terms are deliberately dropped.
- Analyze real code — including loops, nested loops, and halving patterns — to determine its Big-O
  complexity.
- Distinguish time complexity from space complexity, and reason about the trade-off between them.

## 📋 Prerequisites

- [Introduction to Data Structures and Algorithms](../introduction-to-data-structures-and-algorithms/) — this module directly formalizes the performance differences that module observed informally.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [big-o-notation.md](big-o-notation.md) | The core notation, complexity classes, and why constants are dropped |
| [analyzing-algorithms.md](analyzing-algorithms.md) | Repeatable rules for classifying real code by complexity |
| [time-complexity.md](time-complexity.md) | A complete reference table of common operations' time complexity |
| [space-complexity.md](space-complexity.md) | Memory cost analysis and the time-space trade-off; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if Big-O notation is new — every remaining module in this domain assumes fluency with
classifying an algorithm's time and space complexity by reading its code.

**Skim** if you already analyze algorithmic complexity comfortably — but the time-complexity
reference table is worth bookmarking, since later modules refer back to it directly.

## 🧠 Knowledge Check

<details>
<summary>Why does Big-O notation deliberately drop constant multipliers and lower-order terms?</summary>

Big-O describes an algorithm's growth rate as input size grows toward infinity, not its exact
operation count for one specific input. As n grows genuinely large, a constant multiplier or a
smaller additive term becomes insignificant compared to the dominant term's own growth — so an
algorithm doing "2n + 10" operations is classified simply as O(n).

</details>

<details>
<summary>Why can a nested loop over the same input push an algorithm's time complexity from O(n) to O(n²)?</summary>

A single loop over n items runs n times, giving O(n). Nesting a second loop over the same n items
inside the first means that for *each* of the n outer iterations, another full pass of up to n
inner iterations runs — multiplying to roughly n × n = n² total operations, giving O(n²).

</details>

## 📚 References

- [Big O Cheat Sheet](https://www.bigocheatsheet.com/) — a widely-used community reference for common data structure and algorithm complexities.
- [MDN Web Docs: Algorithm](https://developer.mozilla.org/en-US/docs/Glossary/Algorithm) — MDN's glossary entry introducing algorithmic complexity and Big-O notation.

## ➡️ Continue Your Learning Path

Continue to [Arrays](../arrays/) to apply this complexity vocabulary to the first concrete data
structure in this domain.
