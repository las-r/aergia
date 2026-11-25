---
title: "Type Conversions"
description: "Converting values between types."
section: manual
order: 4
---

## Integer
To convert a float or a string to an integer, use `#`.

```aergia
#"1"   \ returns 1
#3.85  \ returns 3
```

## Float
To convert an integer or a string to a float, use `##`.

```aergia
##"2.5"  \ returns 2.5
##10     \ returns 10.0
```

## String
To convert an integer or a float to a string, use `#'`.

```aergia
#'5     \ returns "5"
#'6.28  \ returns "6.28"
```