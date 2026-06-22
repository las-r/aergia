---
layout: default
title: 11. Standard Libraries
parent: Syntax
nav_order: 11
---

# 11. Standard Libraries
Aergia includes a modular suite of 4 core standard libraries built directly into the toolkit to manage collections, boolean validation, structured errors, and string scanning.

## Library Overview
| Library File | Category | Core Purpose |
| :--- | :--- | :--- |
| `std_arr.aer` | Array Utilities | Higher-order mapping, reducing, filtering, and sequence sorting. |
| `std_bool.aer`| Boolean Logic | Definitions and validation constraints for truth values. |
| `std_error.aer`| Exception Architecture | Standard identifiers mapped to the interpreter's native runtime exceptions. |
| `std_str.aer` | String Manipulation | Substring evaluation, whitespace trimming, splitting, and merging. |

## `std_arr.aer` (Array Utilities)
### Core Predicates & Lookups
* **`has :arr itm:`** Checks if `itm` exists inside `arr`. Returns `1` if found, `0` otherwise.
* **`index :arr tar:`** Searches for `tar` sequentially within `arr`. Returns its zero-indexed location, or `_1` if absent.
* **`len :arr:`** Iterates and counts total element length. Valid for both arrays and string bounds.

### Functional Mechanics
* **`map :arr f:`** Passes each item in `arr` to expression/function `f` and generates a transformation array.
* **`filter :arr f:`** Filters items in `arr` based on boolean evaluations from predicate function `f`.
* **`reduce :arr ini f:`** Folds `arr` into a singular accumulator value, initialized at `ini`, by chaining calls via functional folder `f`.

### Transformation & Ordering
* **`reverse :arr:`** Inverts the sequence layout of `arr`.
* **`iota :n:`** Generates a list ranging sequentially from `0` to `n - 1`.
* **`zip :a b:`** Pairs items between collections `a` and `b` linearly. The size matches the shorter input bound.
* **`enumerate :arr:`** Zips array items with their corresponding index identifiers (`<index item>`).
* **`sort :arr:`** Performs an in-place bubble sort ordering items ascendingly.
* **`sortby :arr f:`** Sorts collection sequence by matching values after extracting key results via closure projection `f`.

### Logical Checks & Flattening
* **`any :arr f:`** Short-circuits or yields `1` if any element matches criteria context defined in `f`. Returns `0` if all fail.
* **`all :arr f:`** Verifies every component element honors constraints inside `f`. Returns `0` if any single item fails.
* **`flat :arr:`** Merges two-dimensional array layouts downward into a unified one-dimensional list structure.
* **`flatmap :arr f:`** Combines higher-order element transformations and automated flattening steps into a single call.

## `std_bool.aer` (Boolean Logic)
### Definitional Constants
* **`true`**: Maps value implicitly to integer scalar `1`.
* **`false`**: Maps value implicitly to integer scalar `0`.

### Utility Signatures
* **`is_bool :val:`** Strictly examines whether target `val` is structurally formatted as valid boolean data (`0` or `1`).

## `std_error.aer` (Exception Architecture)
Provides named global string constants matching native errors emitted by the `nodes.py` interpreter framework (`ETYPEMAP`).

* **`DivisionByZero`**
* **`IndexOutOfRange`**
* **`KeyNotFound`**
* **`TypeError`**
* **`NameError`**
* **`ValueError`**
* **`FileNotFound`**:
* **`PermissionDenied`**
* **`ImportError`**
* **`ConstraintError`**
* **`InterpolationError`**
* **`RuntimeError`**

## `std_str.aer` (String Manipulation)
### Merging & Splitting
* **`join :arr del:`** Flattens target array entries into a single string stream, inserting string literal `del` between each element boundary.
* **`split :str del:`** Slices string inputs into pieces delimited across boundaries marking character matches to `del`. If empty, returns individual character items.

### Traversal & Mutation
* **`has :str seq:`** Runs a sliding character window look-ahead sequence matching scan to check if substring `seq` is inside `str`. Returns `1` if true, `0` otherwise.
* **`reverse :str:`** Inverts individual character arrays before stitching components back together.
* **`ltrim :str:`** Clears leading string spacer layout blocks from the left margin until text contents hit a non-space boundary.
* **`rtrim :str:`** Clears trailing string space margins working backward from the right-hand side.
* **`trim :str:`** Symmetrically runs both `ltrim` and `rtrim` pipelines across text targets.