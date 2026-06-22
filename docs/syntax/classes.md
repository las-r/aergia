---
layout: default
title: 9. Classes & Objects
parent: Syntax
nav_order: 9
---

# 9. Classes & Objects
Classes provide an object-oriented paradigm for creating stateful blueprints with independent values and functions.

Every instantiated class receives its own isolated state environment, automatically exposing a reference pointer called `this`.

| Token | Mechanics | Syntax Pattern |
| --- | --- | --- |
| ``{` `` | Class Blueprint Declaration | ``{`ClassName :p1 p2: ...}`` |
| `->` | Member Read / Method Extraction | `-> object property` |
| `=>` | Member Property Mutation | `=> object property value` |
| `@` | Object Instantiation | `= instance @ClassName:args:` |

## Class Definitions & Constructors
The parameter layout immediately following the class identifier acts as the constructor signatures. When the class is instantiated using the invocation operator (`@`), these parameters are localized into the object's fresh state scope. 

Inside the class block body, you initialize instance attributes and define methods. Instance properties are assigned and bound directly to the object context using the `this` context pointer.

```py
# Define a Person class blueprint with a constructor accepting name and age
{`Person :name age:
    # Bind constructor values to instance fields
    => this name name
    => this age age

    # Define an instance method (accepts 'this' to read local fields)
    {greet :this:
        > "Hello, %name%! You are %age% years old."
    }
}
```

## Instantiation & Member Manipulation
To spin up a living copy of a class blueprint, use the standard execution operator (`@`). Once initialized, the object's unique fields can be dynamically read using the member getter (`->`) or updated using the member setter (`=>`).

```py
# Instantiate an isolated copy of the Person class
= kane @Person:"Kane Pixels" 20:

# Read property values
= currentAge -> kane age  # Resolves to 20

# Mutate a property value directly
=> kane age 21
```

## Instance Methods
Methods are functions defined inside a class block. When you extract a method from an object using the `->` operator, it returns a special Bound Method. Aergia automatically wraps this method so that the object itself is silently injected as the first parameter (`this`), enabling easy local field lookups and string interpolation.

```py
# Bind and execute the 'greet' method on the 'sam' instance
# Structure: @ -> instance method_name
@-> kane greet  # Prints: "Hello, Kane Pixels! You are 21 years old."
```