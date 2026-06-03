---
layout: default
title: 4. Conditionals & Branching
parent: Style
nav_order: 4
---

# 4. Conditionals & Branching
Because Aergia conditions rely heavily on nested parentheses, clean formatting prevents "bracket blindness":

1. **Simple If:** Place the condition and the truth action indented beneath it.
2. **If-Else Chains:** Stack sequential conditions. For fallback `else` logic, wrap the final catch-all branch tightly within closing parentheses to maintain mathematical balancing structure.

```py
(<< guess secret
    > "Too low!"
) (
    (>> guess secret
        > "Too high!"
    ) (
        > "Correct!"
    )
)
```

For large blocks of multiple conditionals where each block has not more than one line, it's often better for readability to use inline conditional notation.

```py
(== botchoice "rock"
    (== userchoice "rock" > "Draw, go again.")
    (== userchoice "paper" = winner "user")
    (== userchoice "scissors" = winner "bot")
)
(== botchoice "paper"
    (== userchoice "rock" = winner "bot")
    (== userchoice "paper" > "Draw, go again.")
    (== userchoice "scissors" = winner "user")
)
(== botchoice "scissors"
    (== userchoice "rock" = winner "user")
    (== userchoice "paper" = winner "bot")
    (== userchoice "scissors" > "Draw, go again.")
)
```
