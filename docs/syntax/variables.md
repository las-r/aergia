---
layout: default
title: 2. Variables & Assignment
parent: Syntax
nav_order: 2
---

# 2. Variables & Assignment
Variables are declared and assigned dynamically using the `=` operator followed by the identifier name and the expression payload.

| Token | Operation | Syntax Pattern | Description |
| :--- | :--- | :--- | :--- |
| `=` | Assignment | `= variable_name expr` | Binds the result of `expr` to `variable_name` |
| `=?` | Super Assignment | `=? variable_name constraint` | Defines a supervalue `variable_name` |

## Examples
```py
# Assign the value 10 to standard_val
= standard_val 10

# Putting an operator directly following the `=` symbol can let you modify and reassign a value back to itself
# Multiply standard_val by 2
=* standard_val 2

# Assign the result of a mathematical expression
= result +5 5
```