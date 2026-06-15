---
layout: default
title: 1. Core Data Types & Literals
parent: Syntax
nav_order: 1
---

# 1. Core Data Types & Literals
Aergia dynamically determines types at runtime from four base literal formats:
* **Numbers:** Evaluated automatically as integers or floating-point values. Negative numbers are explicitly prefixed with an underscore (e.g., `42`, `3.14`, `_120`) to keep the binary subtraction operator separate and unambiguous.
* **Strings:** Wrapped in double quotes (`"Hello, Aergia!"`). Standard backslash escape sequences are supported natively, and runtime expressions can be dynamically injected via `%value%` interpolation.
* **Booleans:** Evaluated via numeric truthiness. Expressions or literals yielding `0` are false; any non-zero value evaluates to true.
* **Supervalues:** Used for constraint programming to represent a state of multiple potential values until collapsed.

## Examples
```py
# Numbers & Negatives
= positive 42
= negative _42

# String interpolation
= name "Aergia"
= greeting "Welcome to %name%!"

# Declaring a supervalue x constrained between -100 and 100
=? x "&& >> x _100 << x 100"
```