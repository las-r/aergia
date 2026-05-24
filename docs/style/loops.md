---
layout: default
title: 5. Loops
parent: Style
nav_order: 5
---

# 5. Loops
Loop brackets `[...]` should open on the same line as the initialization or control flow statement. The execution block should immediately drop to an indented line, with the closing bracket `]` aligned horizontally with the start of the loop block.

```q
[!= guess secret
    > "Enter your guess:"
    = guess .
    = tries +tries 1
]
```