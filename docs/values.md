---
layout: default
title: 2. Data and Values
nav_order: 2
description: "How data and values work in Aergia."
parent: "Syntax"
---

# 2. Data and Values

## 2.1 Data Types
Aergia supports four primary types:

* **Integers**: `42`, `-7`
* **Floats**: `3.14`, `.5`
* **Strings**: `"Hello, World!"`
* **Arrays**: `< 1 2 3 >`, `< "Apple" 10.5 >`

Aergia has no strict typing. A variable with a value can be set to any other value, and arrays can hold mixed types.

Here is an example:
```
= hello "World"
= hello 1
= hello < 1 2 "mixed" >
```

## 2.2 Arrays
Arrays are ordered collections of data defined by `< >`. You can also generate arrays of sequential integers using the range operator `..`.

* **Manual Array**: `< 1 2 3 >`

To access a specific element in an array, use the index operator `:` followed by the array and the index (starting at 0).

```
= my_list < "A" "B" "C" >

# Accesses "B"
: my_list 1
```

## 2.3 Implicit Evaluation
Simply stating a value or variable evaluates it. In any block, the last evaluated expression acts as the "result."

```
# Evaluates to 1.2
1.2

# Evaluates to "Hello"
"Hello"

# Evaluates to the second element of the array
: < 10 20 30 > 1
```

## 2.4 Escape Characters
In strings, some characters used in Aergia (like the comment symbol `#` or quotes) can break the string parsing. To include these characters literally, use the backslash `\` escape character.

```
# The '#' would normally start a comment and break this line.
# Use escape characters to include it in a string!
= text "ABC\#123"

# Escaping a quote
= quote "He said, \"Hello\""
```