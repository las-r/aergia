---
layout: default
title: 6. Functions
nav_order: 6
description: "How functions work in Aergia."
parent: "Syntax"
---

# 6. Functions

## 6.1 Defining Functions
Functions are defined with `{name :<parameters>: body}`.

```
{ print_add : x y :
    > + x y
}
```

## 6.2 Calling Functions
Functions are called with `@ name :<args>:`.

```
# The following code prints `Hello, world!` in the console.

{ hello
    > "Hello, world!"
}

@ hello
```

## 6.3 Returning Values
Functions can return values with the `?` prefix. This will halt the function.

```
# The following code prints `2` in the console.

{ subtract : x y :
    ? - x y
}

> @subtract 5 3

# Note how unlike the hello example, this needs a `>` to print.
```