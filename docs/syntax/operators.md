---
layout: default
title: 3. Mathematical & Logical Operators
parent: Syntax
nav_order: 3
---

# 3. Mathematical & Logical Operators
Because Aergia uses prefix notation, binary operations consume the next two valid parsed sub-expressions. Unary operations consume exactly one.

Syntax: `[operator] [operand_1] [operand_2]`

## Binary Operators
* `+` Addition / String Concatenation (Auto-formats)
* `-` Subtraction
* `*` Multiplication
* `/` Division
* `^` Power
* `%` Modulo

## Bitwise Operators
* `&` Bitwise AND
* `|` Bitwise OR
* `$` Bitwise XOR
* `~` Bitwise NOT (Unary)

## Comparison Operators
These evaluate to `1` if the condition is true, or `0` if false.
* `==` Equal to
* `!=` Not equal to
* `<<` Less than
* `>>` Greater than
* `<=` Less than or equal to
* `>=` Greater than or equal to


## Logical Operators
* `&&` Logical AND (Short-circuit)
* `||` Logical OR (Short-circuit)
* `!` Logical NOT (Unary: turns truthy to `0`, falsy to `1`)

## Examples
```py
# Prefix math examples:
= x +2 3       # x = 2 + 3 (Evaluates to 5)
= y *10 +2 3   # y = 10 * (2 + 3) (Evaluates to 50)

# Comparisons:
= is_equal == x 5  # assigns 1 to is_equal
```