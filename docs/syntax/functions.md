---
layout: default
title: 7. Functions
parent: Syntax
nav_order: 7
---

# 7. Functions
Functions handle execution isolation, scoping transitions, and value boundaries. In Aergia, functions are first-class values, meaning both named blocks and anonymous lambdas evaluate to function objects that can be assigned to variables, passed to other operations, or invoked inline.

If a function does not explicitly return a value, it will just return the value of the last evaluated expression.

| Token | Mechanics | Syntax Pattern |
| --- | --- | --- |
| `{` | Function / Lambda Declaration | Named: `{name :p1 p2: body ...}` <br> Anonymous: `{ :p1 p2: expr }` |
| `@` | Function Evaluation & Call | `@target :arg1 arg2:` |
| `?` | Return Force | `? return_expr` |

## Named Functions
Named functions are defined using an identifier immediately following the opening `{`. They can contain a multi-statement block body. To exit early or pass back a specific value from a named function body, use the return force token (`?`).

```py
# Define a function named 'addNums' accepting two parameters
{addNums :a b:
    ? +a b
}

# Invoke the function directly by its identifier name
= total @addNums:10 20:
> total  # Prints 30
```

## Anonymous Functions (Lambdas)
Anonymous functions omit the identifier name entirely, moving straight into the parameter block `{:params: ...}`.

```py
# An inline multiplier lambda executed immediately
> @{:a b: *a b}:4 5:  # Prints 20

# A function that's defined similar to a variable
= subtract {:a b: -a b}
> @subtract:10 3:  # Prints 7
```