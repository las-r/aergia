---
layout: default
title: 1. Naming Conventions
parent: Style
nav_order: 1
---

# 1. Naming Conventions
- Variables should be named using `snake_case`.
    - Constants, on the other hand, should be named using `UPPER_SNAKE_CASE`.
- Functions should be named using `camelCase`.

If you're making a library, don't prefix your own function names inside the file (e.g. write `join`, not `str_join`). Namespacing is handled by the caller's import instead:

```py
# closed import binds every export behind the "str" prefix
+< "std_str.aer" str
@str.join:< "a" "b" > "-":

# open import binds exports directly into the current scope, no prefix
+> "std_str.aer"
@join:< "a" "b" > "-":
```

Because of this, calls *within* a library file should always use the bare, unprefixed name - the std library follows this rule consistently (`std_arr.aer`, `std_str.aer`, etc).