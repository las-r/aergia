---
layout: default
title: 5. Arrays & Indexing
parent: Syntax
nav_order: 5
---

# 5. Arrays & Indexing
Arrays are contiguous ordered collections. Indexing is zero-based.

| Token | Structure | Example | Description |
| --- | --- | --- | --- |
| `<...>` | Array Initialization | `= items <10 20 30>` | Creates a new array structure. |
| `:` | Index Resolution | `: items 0` | Resolves to the item at the given index (`10`). |
| `+:` | Push Item | `+: items 40` | Appends an item to the end of the array. |
| `-:` | Pop Item | `-: items` | Removes and returns the last element of the array. |
| `~:` | Pop Index | `~: items 1` | Removes and returns the element at a specific index. |
| `*:` | Insert Item | `*: items 1 15` | Inserts an item into the array at the given index. |
| `#:` | Remove Item | `#: items 20` | Finds and removes the first occurrence of a specific item value. |
| `::` | Slice Array | `:: items 1 3` | Slices an array between two given indexes. |

## Examples
### Appending and Inserting
```q
# Initialize an array
= inventory <"sword" "shield">

# Push an item to the end (Returns the pushed item)
+: inventory "potion"
# inventory is now <"sword" "shield" "potion">

# Insert an item at index 1 (Structure: :* array index item)
*: inventory 1 "helmet"
# inventory is now <"sword" "helmet" "shield" "potion">
```

### Removing Elements
```q
# Pop the last element off the array (Returns the popped item)
-: inventory
# Returns "potion"; inventory is now <"sword" "helmet" "shield">

# Pop an element from a specific index (Returns the popped item)
~: inventory 1
# Returns "helmet"; inventory is now <"sword" "shield">

# Remove a specific item value (Returns the removed item)
#: inventory "shield"
# Returns "shield"; inventory is now <"sword">
```