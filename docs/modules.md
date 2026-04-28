---
layout: default
title: 7. Modules
nav_order: 7
description: "How modules work in Aergia."
parent: "Syntax"
---

# 7. Modules

Modules are a great way to break up large projects into multiple smaller files. In Aergia, modules work by essentially running the imported file and putting all the variables and functions within the file into the global environment.

Modules also have a very special quality in Aergia: you can import Python modules directly.

## 7.1 Defining Modules
Modules can be defined by simply writing a file in Aergia. By importing said file, you can use values and functions from the file in another Aergia file. Note that **importing an Aergia module puts all the variables and functions into the global namespace.**

## 7.2 Importing Modules
You can import modules with `+> "<filename.aer>"`.
```
# The following imports the file `math.aer`:
+> "math.aer"
```

To import Python modules, use `*>` or `*<` (Closed Import).

### Open Import (`*>`)
The `*>` operator adds all values directly from the module into the global namespace.
```
*> random
# Use the randint function directly
> @randint : 1 100 :
```

### Closed Import and Aliasing (`*<`)
The `*<` operator allows you to import a module and provide an **alias** (a prefix). This keeps your global namespace clean and avoids naming conflicts.

Syntax: `*< <module_name> <alias>`

```
# Import math with the alias 'm'
*< math m

# Access sqrt using the 'm' prefix
> @m_sqrt : 144 :
```

Any classes within these modules will be flattened. Where dots would normally appear in Python, Aergia uses underscores. (e.g., `pyray.KeyboardKey.KEY_SPACE` becomes `pyray_KeyboardKey_KEY_SPACE`).

Generally, using `*<` with an alias is recommended over `*>` to prevent cluttering the global namespace. Note that Aergia modules (`+>`) do not currently support aliasing and will always load directly into the global namespace.