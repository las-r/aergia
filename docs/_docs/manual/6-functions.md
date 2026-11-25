---
title: "Functions"
description: "Defining and calling lambdas."
section: manual
order: 6
---

## Defining a Function
To define a function (akin to a lambda), use curly brackets with the parameter list ended by a semicolon.

```aergia
{n; +n 1}
```

To give a name to a function, it needs to be assigned like a variable.

```aergia
= inc {n; +n 1}
```

## Calling a Function
Use `@` followed by the function's name and its arguments. A semicolon ends the argument list.

```aergia
= result @inc 5;
> result  \ prints 6
```

## Returning Values
By default, a function returns its last evaluated expression. To return a value and exit the function immediately, use `?`.

```aergia
= add {x y;
    ? +x y
}
```

## Self Referencing
Inside a function, `:` refers to the function itself, so `@:` calls it again. This allows recursion and callbacks even in closures.

```aergia
> @{n; (<= n 1 1)(*n @: -n 1;)} 6;  \ factorial, prints 720 (6!)
```

## Scope
Functions can read and change variables from the parent scope. Variables created inside a function are local to it.

```aergia
= total 0

= add {n;
    = total +total n  \ changes the global total
    = temp n          \ local to add
}

@add 5;
> total  \ prints 5
> temp   \ error: temp only exists inside add
```