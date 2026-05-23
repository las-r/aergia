---
layout: default
title: 4. Input & Output
parent: Syntax
nav_order: 4
---

# 4. Input & Output
Aergia provisions ultra-minimalist primitives for reading from standard input and writing to standard output.

| Token | Behavior | Expected Target / Return |
| --- | --- | --- |
| `>` | Print to Console | Outputs the following expression. |
| `,` | Read String Input | Halts execution for input; returns a String. |
| `.` | Read Integer Input | Halts execution for input; returns an Int. |
| `'` | Read Float Input | Halts execution for input; returns a Float. |

## Examples
```text
# Printing a message
> "What is your age?"

# Reading an integer into a variable
= user_age .
```