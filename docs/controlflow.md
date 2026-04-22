---
layout: default
title: 5. Control Flow
nav_order: 5
description: "How control flow works in Aergia."
parent: "Syntax"
---

# 5. Control Flow

## 5.1 Conditionals (If/Else)

**Syntax:** `( [condition] [body] )`

An "else" block is defined by opening a second set of parentheses immediately after the first block's closing parenthesis.

```
= val .
( >> val 10
    > "Value is greater than 10"
)
(
    > "Value is 10 or less"
)
```

## 5.2 Loops (While)

**Syntax:** `[ [condition] [body] ]`

The block repeats as long as the condition evaluates to a non-zero value.

```
= count 0
[ << count 5
    > count
    = count + count 1
]
```