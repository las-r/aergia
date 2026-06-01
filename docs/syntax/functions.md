---
layout: default
title: 7. Functions
parent: Syntax
nav_order: 7
---

# 7. Functions
Functions handle execution isolation, scoping transitions, and value boundaries.

| Token | Mechanics | Syntax Pattern |
| --- | --- | --- |
| `{` | Function Declaration | `{name :param1 param2: body ...}` |
| `@` | Function Call Execution | `@name:arg1 arg2:` |
| `?` | Return Force | `? return_expr` |

## Examples
```text
# Define a function named 'add_nums' accepting two parameters
{addNums :a b:
    ? +a b
}

# Invoke the function and assign the result
= total @addNums:10 20:
> total  # Prints 30
```
