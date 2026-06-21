---
layout: default
title: 5. Arrays & Maps
parent: Syntax
nav_order: 5
---

# 5. Arrays & Maps
Arrays are contiguous, ordered collections with zero-based indexing. Maps are collections of key-value pairs that link unique keys to specific values. Both collections share a unified set of core operators.

| Token | Structure | Array Behavior | Map Behavior |
| --- | --- | --- | --- |
| `< ... >` | Array Initialization | Creates an ordered array (e.g., `= arr < 10 20 >`). | N/A |
| ``<` ... >`` | Map Initialization | N/A | Creates a key/value paired map (e.g., ``= map <` "a" 1 "b" 2 >``). |
| `:` | Key / Index Resolution | Resolves to the item at a numerical index. | Resolves to the value associated with the given key. |
| `+:` | Push / Merge Item | Appends an item to the end of the array. | Merges another map, or associates a `< key value >` pair. |
| `-:` | Pop Element | Removes and returns the last element. | Removes and returns the last added pair as a `< key value >` array. |
| `~:` | Pop Specific Key/Index | Removes and returns the element at a numerical index. | Removes and returns the value of a specific key. |
| `*:` | Insert / Map Pair | Inserts an item into the array at a numerical index. | Maps a key to a value (equivalent to `=:` behavior). |
| `$:` | Remove by Value/Key | Finds and removes the first occurrence of a specific value. | Deletes a key-value pair matching the given key. |
| `^:` | Slice Collection | Slices an array between two indexes. | N/A |
| `=:` | Set Index/Key | Sets the value at a specific numerical index. | Sets or updates the value associated with a key. |
| `..` | Range Initialization | Creates a range list based on a start, end, and step. | N/A |

## Examples

### Arrays
```py
# Initialize an array
= inventory < "sword" "shield" >

# Push an item to the end (Returns the pushed item)
+: inventory "potion"
# inventory is now <"sword" "shield" "potion">

# Insert an item at index 1 (Structure: *: array index item)
*: inventory 1 "helmet"
# inventory is now <"sword" "helmet" "shield" "potion">

# Pop the last element off the array (Returns "potion")
-: inventory
# inventory is now <"sword" "helmet" "shield">

# Pop an element from a specific index (Returns "helmet")
~: inventory 1
# inventory is now <"sword" "shield">

# Remove a specific item value (Returns "shield")
$: inventory "shield"
# inventory is now <"sword">
```

### Maps
```py
# Accessing a value by its key
= status : user "status"

# Assigning or updating a key-value pair
=: user "score" 100
*: user "level" 5

# Pushing a key-value pair or merging maps
+: user < "guild" "Warriors" >

# Removing map elements by key (Returns the removed value)
~: user "score" 
# Removes the "score" pair and returns 100

# Deleting a key without returning its value
$: user "level"

# Popping the last added pair (Returns a < key value > array)
= last_pair -: user
# last_pair becomes < "guild" "Warriors" >
```