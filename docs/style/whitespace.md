---
layout: default
title: 2. Whitespace
parent: Style
nav_order: 2
---

# 2. Whitespace
- Always use 4 spaces for indentation. Never use tabs.
- The max character count per line is 100.
- **Operator Prefix Spacing:** Never put a space between a prefix operator and its immediate first operand, but *do* use spaces to separate subsequent operands.
    - `+^a 2 ^b 2` is preferred over `+ ^ a 2 ^ b 2` or `+^a 2^b 2`.
    - This only applies to arithmetic operators. For comparison operators, you should have a space between every token.