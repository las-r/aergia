---
title: "Variables"
description: "Assigning and using variables."
section: manual
order: 1
---

## Assigning Variables
`=` followed by a name and a value assigns a variable.

```aergia
= name "Aergia"
= count 3
```

## Using Variables
Write a variable's name to use its value.

```aergia
> name  \ prints Aergia
```

## Naming
Names can only contain letters and digits, and cannot start with a digit. Underscores are not allowed because `_` is used for negation.

```aergia
= my_name "las-r"  \ error
= myName "las-r"   \ correct
```