---
layout: default
title: 1. Core Data Types & Literals
parent: Syntax
nav_order: 1
---

# 1. Core Data Types & Literals
Aergia dynamically determines types at runtime from three base literal formats:

*   **Numbers:** Evaluated automatically as integers or floating-point values depending on their format (e.g., `42`, `3.14`).
*   **Strings:** Wrapped in double quotes (`"Hello, Aergia!"`). Standard backslash escape sequences are supported natively, interpolated values are denoted with `%value%`.
*   **Booleans:** Evaluated from numeric truthiness. Expressions yielding `0` are considered false; any non-zero value evaluates as true.