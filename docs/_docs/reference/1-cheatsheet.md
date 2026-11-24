---
title: "Cheatsheet"
description: "Every syntax feature in Aergia."
section: reference
order: 1
---

## Basics
```aergia
\ a backslash starts a comment
```

```aergia
\ assign: = name value

= num 2
= message "hi!"
```

```aergia
\ output: > value
\ input:  < prompt

> "hello"
= name < "name? "
```

## Control flow
```aergia
\ if else: (condition body)(else), else is obligatory

(<< a 50
    > "a is under 50"
)(
    > "a is not under 50"
)
```

```aergia
\ while: [condition body]

= i 0
[<< i 10
    > i
    = i +i 1
]
```

## Maps
```aergia
\ . creates an empty map
\ set:  =. name key value
\ get:  , name key  ->  1
\ size: ..map      ->  2

= map .
=. map "a" 1
=. map "b" 2
, map "a"
..map
```

## Functions
```aergia
\ define: {params; body}, ; ends the parameters
\ call:   @fn args;, ; ends the arguments

= result @{x; +x 1} 1;
```

- `;` ends a parameter list or an argument list
- `?` returns a value
- `:` refers to the current function (recursion, callbacks)

## Operators
- `+a b` add
- `-a b` subtract
- `*a b` multiply
- `/a b` divide
- `%a b` modulus
- `^a b` exponent
- `_a` negate

- `&a b` bitwise AND
- `|a b` bitwise OR
- `~a` bitwise NOT

- `<< a b` less than
- `>> a b` greater than
- `<= a b` less or equal
- `>= a b` greater or equal
- `== a b` equal
- `!= a b` not equal

- `&& a b` logical AND
- `|| a b` logical OR
- `! a` logical NOT