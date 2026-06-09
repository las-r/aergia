---
layout: default
title: 7. Arrays
parent: Style
nav_order: 7
---

# 7. Arrays
Arrays should have space separated items, or newline separated for longer lists, with space padding since the lexer wouldn't be able to properly tokenize nested arrays without the padding.

```py
# Note how the padding stops nested array indicators from being lexed as a single comparison operator
= array < "a" "b" "c" < 1 2 3 > >
```