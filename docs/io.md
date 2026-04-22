---
layout: default
title: 3. Input and Output
nav_order: 3
description: "How input and output work in Aergia."
parent: "Syntax"
---

# 3. Input and Output
## 3.1 Output

The `>` operator prints the evaluated expression to the console.

```
> "Hello, world!"
> + 10 5  # Prints 15
```

## 3.2 Input

Input operators halt execution and evaluate to the value entered by the user via stdin:

* `,` : Read String
* `.` : Read Integer
* `'` : Read Float

```
> "Enter your name:"
= name ,

> "Enter your age:"
= age .
```