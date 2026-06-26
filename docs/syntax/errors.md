---
layout: default
title: 12. Error Raising & Catching
parent: Syntax
nav_order: 12
---

# 12. Error Raising & Catching
Error catching in Aergia allows programs to intercept runtime errors and recover gracefully instead of crashing. The `!!` block wraps a body of code to attempt, and the `->` clause defines what runs if an error occurs.

| Token | Mechanics | Syntax Pattern |
| --- | --- | --- |
| `!!` | Raise Error | `!! type msg` |
| `!!(...)` | Catch Error | `!!(errname body ...) -> ( catchbody ... )` |

## Error Types
The following type strings are available in `std_error.aer`:

| Constant | Value | Triggered by |
| --- | --- | --- |
| `DivisionByZero` | `"DivisionByZero"` | Dividing by zero |
| `IndexOutOfRange` | `"IndexOutOfRange"` | Array index out of bounds |
| `KeyNotFound` | `"KeyNotFound"` | Missing key in a map |
| `TypeError` | `"TypeError"` | Wrong type for an operation |
| `NameError` | `"NameError"` | Accessing an undefined variable |
| `ValueError` | `"ValueError"` | Invalid value for an operation |
| `FileNotFound` | `"FileNotFound"` | File does not exist |
| `PermissionDenied` | `"PermissionDenied"` | Insufficient file permissions |
| `ImportError` | `"ImportError"` | Unresolved import path |
| `ConstraintError` | `"ConstraintError"` | Super variable constraint failure |
| `InterpolationError` | `"InterpolationError"` | String interpolation failure |
| `RuntimeError` | `"RuntimeError"` | Any other runtime error |

## Raising
The `!!` token raises an error.

```py
!! e.SyntaxError "Token %t% not expected."
```

## Catching
### Basic Usage
The `!!(` token opens a try/catch block. The first token inside the `(` is the **error binding** — the name under which the error message will be accessible in the catch body. Everything after it until `)` is the try body.

```py
!!(err
    = x / 1 0
) -> (
    > "caught an error!"
)
```

If the try body succeeds, the catch body is skipped entirely. If any runtime error occurs, execution jumps to the catch body.

### The Error Binding
Inside the catch body, the error binding gives you two variables:

- `errname` — the error message string
- `errname.type` — a stable type identifier string for branching

```py
!!(err
    = x / 1 0
) -> (
    > err         # Prints: division by zero
    > err.type    # Prints: DivisionByZero
)
```

### Branching on Error Type
Use `std_error.aer` to get named constants for every error type, then compare against `errname.type` to handle specific errors differently.

```py
+< "std_error.aer" e

!!(err
    = arr < 1 2 3 >
    > : arr 99
) -> (
    (== err.type e.IndexOutOfRange
        > "index was out of bounds"
    ) -> (
        > "something else went wrong: %err%"
    )
)
```

### Catch Body is Optional
The `-> ( )` clause can be omitted if you only want to suppress errors silently.

```py
!!(err
    = x / 1 0
)
```

### Nesting
Try/catch blocks can be nested. Each has its own independent error binding.

```py
!!(outer
    > "trying outer..."
    !!(inner
        = arr < >
        > : arr 0
    ) -> (
        > "inner caught: %inner.type%"
    )
    = x / 1 0
) -> (
    > "outer caught: %outer.type%"
)
```

## Notes
- `~>` (exit), `?` (return), `<<<` (break), and `>>>` (continue) all pass through the catch boundary unchanged — error catching does not swallow control flow signals.
- The error binding variables (`errname` and `errname.type`) are scoped to the catch body only and do not leak into the surrounding environment.