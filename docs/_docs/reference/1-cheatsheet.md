---
title: "Cheatsheet"
description: "Every syntax feature in Aergia."
section: reference
order: 1
---

## Basics
`\ COMMENT` makes a comment

```aergia
\ this is a comment
```

`= NAME VALUE` assigns a variable

```aergia
= num 2
= message "hi!"
```

`> VALUE` prints a value  
`< PROMPT` takes input

```aergia
> "hello"
= name < "name? "
```

## Type Conversions
`#VALUE` converts to an integer  
`##VALUE` converts to a float  
`#'VALUE` converts a string

```aergia
= num ##< "Enter a number: "
= numstr #'num
= numint #num
```

## Control flow
`(COND BODY)(ELSE)` defines an if statement, else is mandatory

```aergia
(<< a 50
    > "a is under 50"
)(
    > "a is not under 50"
)
```

`[COND BODY]` defines a while loop

```aergia
= i 0
[<< i 10
    > i
    = i +i 1
]
```

## Maps
`.` creates an empty map  
`=. NAME KEY VALUE` sets a value to a key  
`,MAP KEY` gets a value  
 `..MAP` gets the size of a map

```aergia
= map .
=. map "a" 1
=. map "b" 2

> ,map "a"
> ..map
```

## Functions
`{PARAMS; BODY}` defines a function  
`@FUNC ARGS;` calls a function  
`? VALUE` returns a value  
`;` ends a parameter list or an argument list  
`:` refers to the current function (recursion, callbacks)

```aergia
= fact {n; (<= n 1 1)(*n @: -n 1;)}

> @fact 10;
```

## Operators
`+a b` add  
`-a b` subtract  
`*a b` multiply  
`/a b` divide  
`%a b` modulus  
`^a b` exponent  
`_a` negate

`&a b` bitwise AND  
`|a b` bitwise OR  
`~a` bitwise NOT

`<< a b` less than  
`>> a b` greater than  
`<= a b` less or equal  
`>= a b` greater or equal  
`== a b` equal  
`!= a b` not equal

`&& a b` logical AND  
`|| a b` logical OR  
`! a` logical NOT