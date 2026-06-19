---
layout: default
title: 9. Modules & System Integration
parent: Syntax
nav_order: 9
---

# 9. Modules & System Integration
Aergia code can load external resources either from separate `.aer` files or tap natively directly into Python's vast package index.

* `+> expr prefix` **Open Import:** Parses and executes an external `.aer` source file path.
* `+< expr prefix` **Closed Import:** Parses and executes an external `.aer` source file path, mapping its internal namespace elements cleanly behind a safety string prefix: `prefix.module_item`.
* `*> module` **Open Python Import:** Imports a native Python module directly into the global execution namespace.
* `*< module prefix` **Closed Python Import:** Imports a native Python module and maps its internal namespace elements in the same way that normal closed imports do: `prefix.module_item`.
* `; expr` **Eval Execution:** Evaluates raw string sequences directly as Aergia source tokens at runtime.
* `~> expr` **Exit Engine:** Halts the interpreter process immediately with the status code provided by `expr`.

## Examples
```py
# Import local helper library
+> "utils.aer"

# Native Open Python Import
*> math
= root_val @sqrt:16:  # Access via global env

# Closed Python Import
*< random rand
# Available via custom namespace binding
= roll @rand.randint:1 6:

# Evaluate code directly from a string sequence
; "= dynamic 100"

# Stop execution and exit immediately with status 0
~> 0
```