---
layout: default
title: Examples
nav_order: 3
---

# Examples
This section has a few examples of how the Aergia language can be used.

## Hello World
```txt
> "Hello, world!"
```

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