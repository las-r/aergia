---
layout: default
title: 2. Data and Values
nav_order: 2
description: "How data and values work in Aergia."
parent: "Syntax"
---

# 2. Data and Values

## 2.1 Data Types
Aergia supports three primary types:

* Integers: `42`, `-7`
* Floats: `3.14`, `.5`
* Strings: `"Hello, World!"`

Aergia has no strict typing. A variable with a value can be set to any other value.

Here is an example:
```
= hello "World"
= hello 1
= hello 3.14
```

## 2.2 Implicit Evaluation

Simply stating a value or variable evaluates it. In any block, the last evaluated expression acts as the "result."

```
# Evaluates to 1.2
1.2

# Evaluates to "Hello"
"Hello"
```