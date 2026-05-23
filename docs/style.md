---
layout: default
title: Style Guide
nav_order: 4
---

# Style Guide
Programs written in Aergia, like all programming languages, can either be easy to read or hard to read. Most of the time, you'd want it to be easy to read. These guidelines should help you do just that.

Aergia code should almost always prioritize clarity over cleverness. If a piece of code can be written explicitly or implicitly, prefer explicit syntax. Then again, it's your code. These are just some loose guidelines, whether you follow them or not is up to you.

## Basic Guidelines
### Naming Conventions
- Variables should be named using `snake_case`.
    - Constants, on the other hand, should be named using `UPPER_SNAKE_CASE`.
- Functions should be named using `camelCase`.

If you're making a library, you should append the name of the library to the front of any functions or values using an underscore. `e.g. math_squareRoot`

### Whitespace
- Always use 4 spaces for indentation. Never use tabs.
- The max character count per line is 100.
- **Operator Prefix Spacing:** Never put a space between a prefix operator and its immediate first operand, but *do* use spaces to separate subsequent operands.
    - `+^a 2 ^b 2` is preferred over `+ ^ a 2 ^ b 2` or `+^a 2^b 2`.
    - This only applies to arithmetic operators. For comparison operators, you should have a space between every token.
- **Sigil Spacing:** Leave a single space after the output sigil `>` and the import sigil `*<` for better visual parsing.
    - Prefer: `> "Side A:"` over `>"Side A:"`
    - Prefer: `*< math m` over `*<math m`

### Functions
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

### Conditionals & Branching
Because Aergia conditions rely heavily on nested parentheses, clean formatting prevents "bracket blindness":

1. **Simple If:** Place the condition and the truth action indented beneath it.
2. **If-Else Chains:** Stack sequential conditions. For fallback `else` logic, wrap the final catch-all branch tightly within closing parentheses to maintain mathematical balancing structure.

```q
(<< guess secret
    > "Too low!"
) (
    (>> guess secret
        > "Too high!"
    ) (
        > +"Correct!"
    )
)
```

### Loops
Loop brackets `[...]` should open on the same line as the initialization or control flow statement. The execution block should immediately drop to an indented line, with the closing bracket `]` aligned horizontally with the start of the loop block.

```q
[!= guess secret
    > "Enter your guess:"
    = guess .
    = tries +tries 1
]
```

### Input & Capturing Values
When asking for user input, always display the prompt string immediately *above* the assignment block rather than cramming them onto a single dense line.

```q
> "Side A:"
= a '
```