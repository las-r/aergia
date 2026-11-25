---
title: "Math"
description: "Calculating via arithmetic and operators."
section: manual
order: 3
---

## Prefix Notation
Operators come before their operands, so there is no `1 + 2`. Write the operator first.

```aergia
> +1 2  \ prints 3
> *4 5  \ prints 20
```

A full list of operators can be found in the [cheatsheet]({{ site.baseurl }}/reference/1-cheatsheet/#operators).

## Nesting
Each operator takes a fixed number of operands, so expressions nest without parentheses. Operators are evaluated from the inside out.

```aergia
> +1 *2 3   \ 1 + (2 * 3), prints 7
> *+1 2 3   \ (1 + 2) * 3, prints 9
```

## Using Variables
Variables work anywhere a value does.

```aergia
= price 20
= qty 3
> *price qty  \ prints 60
```

## Negation
`_` negates a value. This is why underscores aren't allowed in variable names.

```aergia
= num 5
> _num  \ prints -5
```

Next: [Functions](../functions)