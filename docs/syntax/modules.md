---
layout: default
title: 8. Modules & System Integration
parent: Syntax
nav_order: 8
---

# 8. Modules & System Integration
Aergia code can load external resources either from separate `.aer` files or tap natively directly into Python's vast package index.

* `+> expr` **Internal Import:** Parses and executes an external `.aer` source file path.
* `*> module` **Open Python Import:** Imports a native Python module directly into the global execution namespace.
* `*< module prefix` **Closed Python Import:** Imports a native Python module mapping its internal namespace elements cleanly behind a safety string prefix: `prefix_functionName`.
* `; expr` **Eval Execution:** Evaluates raw string sequences directly as Aergia source tokens at runtime.
* `~> expr` **Exit Engine:** Halts the interpreter process immediately with the status code provided by `expr`.

## Examples
```py
# Import local helper library
+> "utils.aer"

# Native Open Python Import
*> math
= root_val @math_sqrt:16:  # Access via module name underscore convention

# Closed Python Import
*< random rand
# Available via custom namespace binding
= roll @rand_randint:1 6:

# Evaluate code directly from a string sequence
; "= dynamic 100"

# Stop execution and exit immediately with status 0
~> 0
```