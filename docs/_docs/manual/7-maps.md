---
title: "Maps"
description: "Creating and using maps to store data."
section: manual
order: 7
---

## Creating a Map
Use `.` to create an empty map.

```aergia
= map .
```

## Using Values
`=.` sets a key-value pair and `,` gets a value from a key.

If a value is not defined, then getting it will simply return `0`.

```aergia
=. map "a" 10
=. map "b" 20

> ,map "a"  \ prints 10
> ,map "b"  \ prints 20
> ,map "c"  \ prints 0
```