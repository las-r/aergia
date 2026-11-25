---
title: "Control Flow"
description: "Using if statements and while loops."
section: manual
order: 5
---

## If
Two sets of parentheses (`()()`) define an if-else statement. In the first set, the first expression is the condition upon which the if block is formed. The second set, defining the else body, is mandatory.

```aergia
= age #< "Your age? "

(<< age 18
    > "You are under 18."
)(
    > "You are 18 or older."
)
```

An if-else statement is an expression that returns its last evaluation.

## While
A set of brackets (`[]`) define a while statement. The first expression is the condition and the rest of the body will be repeatedly evaluated until it is false.

```aergia
= i 0

[<< i 10
    > "i is less than 10."
    = i +i 1
]

> "i is no longer less than 10."
```

A while statement is an expression that returns its last evaluation.