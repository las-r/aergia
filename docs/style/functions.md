---
layout: default
title: 3. Functions
parent: Style
nav_order: 3
---

# 3. Functions
When defining a function, the signature and parameters should sit on the opening line. The body should be cleanly indented by 4 spaces, and the closing brace `}` should sit on its own line at the base indentation level.

In the definition, there should be a space between the function name and its parameters, however this is not necessary when calling functions.

```q
{factorial :n:
    (<= n 1
        ? 1
    )
    ? *n @factorial:-n 1:
}
```