---
title: "I/O"
description: "Printing values and taking user input."
section: manual
order: 2
---

## Output
`>` prints a value to stdout and returns it.

```aergia
> "Hello!"
> 2
> 3.14
```

## Input
`<` prints a prompt and returns a string from stdin.

```aergia
= name < "Your name? "
= age #< "Your age? "  \ # is used to convert a value to an integer
```