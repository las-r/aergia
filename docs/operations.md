---
layout: default
title: Operations
nav_order: 4
description: "How operations work in Aergia."
parent: "Syntax"
---

# 4. Operations

All operations use prefix notation:

```
/ [OPERATOR] [ARG1] [ARG2]
+ 3 2
```

Operations can be nested:

```
* 2 + 3 4
```

## 4.1 Arithmetic

| Op | Action   | Example  | Result |
| -- | -------- | -------- | ------ |
| +  | Add      | `+ 5 2`  | 7      |
| -  | Subtract | `- 10 4` | 6      |
| *  | Multiply | `* 3 3`  | 9      |
| /  | Divide   | `/ 10 2` | 5      |
| ^  | Exponent | `^ 2 3`  | 8      |
| %  | Modulo   | `% 10 3` | 1      |

## 4.2 Bitwise & Logic

| Op  | Action      | Example  |
| --- | ----------- | -------- |
| \|  | Bitwise OR  | `\| x y` |
| &   | Bitwise AND | `& x y`  |
| $   | Bitwise XOR | `$ x y`  |
| ~   | Bitwise NOT | `~ x`    |
| !   | Logical NOT | `! x`    |

## 4.3 Comparison

Comparisons return `1` for true and `0` for false.

| Op | Action           | Example   |
| -- | ---------------- | --------- |
| == | Equals           | `== x 5`  |
| << | Less than        | `<< x 10` |
| >> | Greater than     | `>> x 0`  |
| <= | Less or equal    | `<= x 5`  |
| >= | Greater or equal | `>= x 5`  |