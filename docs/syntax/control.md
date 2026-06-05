---
layout: default
title: 6. Control Flow
parent: Syntax
nav_order: 6
---

# 6. Control Flow
Control flow operations use brackets or parentheses to enclose evaluation scopes and execution bodies.

## Conditionals (If & Else)
Syntax: `( cond statement1 statement2 ... ) -> ( elsestatement1 ... )`

### Examples
```py
# If condition evaluates to true, execute the first block. 
# The second block (else) is optional.
(== age 18
    > "Welcome to adulthood!"
) -> (
    > "You are not 18."
)

# If blocks can be evaluated inline as well.
# The result is the last evaluated expression.
= a 2
= b 1
> (<< a b "A is less than B") -> ("A is not less than B")
```

## Loops (While & For)
Syntax (While): `[ cond statement1 statement2 ... ]`
Syntax (For):   `[ \` array iterator_name statement1 ... ]`

Like conditionals, loop blocks can be evaluated inline. The value of a loop expression is determined by the last evaluated expression inside its body on its **final iteration**. If the loop condition is initially false (or the array is empty), the block returns `0`.

### Examples
```py
# While Loop example
= i 0
[<< i 5
    > i
    = i + i 1
]

# For Loop iterating over an array
= my_arr <"A" "B" "C">
[`my_arr letter
    > letter
]

### Inline Evaluation Examples
# Loops can capture values inline. The result assigned is the last statement executed
# before the loop condition terminates or the loop finishes.

= counter 1
= total_sum 0

# The value assigned to 'result' will be the final value of 'total_sum' 
# evaluated right before the loop terminates.
= result [<< counter 4
    = total_sum + total_sum counter
    = counter + counter 1
    total_sum
]

> result   # Outputs: 6 (1 + 2 + 3)

# Inline For Loop capturing transformations
= numbers <10 20 30>
= running_total 0

# Iterates through the collection, altering an outside variable, and tracking 
# the final calculation state.
= final_value [`numbers num
    = running_total + running_total num
    * running_total 2
]

> final_value   # Outputs: 120 (The last calculation: (10 + 20 + 30) * 2 )

# Empty or Unexecuted loops return a default boundary value of 0
= unexecuted [<< 1 0
    "This will never run"
]
> unexecuted   # Outputs: 0
```