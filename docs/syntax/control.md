---
layout: default
title: 6. Control Flow
parent: Syntax
nav_order: 6
---

# 6. Control Flow
Control flow operations use brackets or parentheses to enclose evaluation scopes and execution bodies.

## Conditionals (If-Else)
Syntax: `( cond statement1 statement2 ... ) ( elsestatement1 ... )`

### Examples
```text
# If condition evaluates to true, execute the first block. 
# The second block (else) is optional.
(== age 18
    > "Welcome to adulthood!"
) (
    > "You are not 18."
)
```

## Loops (While & For)
Syntax (While): `[ cond statement1 statement2 ... ]`
Syntax (For): `[ \` array iterator_name statement1 ... ]`

### Examples
```text
# While Loop example
= i 0
[<< i 5
    > i
    = i +i 1
]

# For Loop iterating over an array
= my_arr <"A" "B" "C">
[`my_arr letter
    > letter
]
```