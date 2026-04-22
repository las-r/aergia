---
layout: default
title: Introduction
nav_order: 1
description: "Introduction to the Aergias programming language."
---

# Aergia

The most minimal yet still usable programming language.

Aergia is an expression-oriented language where every operation returns a value. It utilizes Prefix Notation (Polish Notation) to maintain a minimal footprint, eliminating the need for complex operator precedence and grouping parentheses in math.

## 6. Example Program: Fibonacci Sequence

```txt
/ Aergia Fibonacci Sequence

> "How many numbers?"
= limit .
= n1 0
= n2 1
= i 0

[ << i limit
    > n1
    = temp + n1 n2
    = n1 n2
    = n2 temp
    = i + i 1
]
```
