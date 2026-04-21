# Aergia

The most minimal yet still usable programming language.

Aergia is an expression-oriented language where every operation returns a value. It utilizes Prefix Notation (Polish Notation) to maintain a minimal footprint, eliminating the need for complex operator precedence and grouping parentheses in math.

## 1. Syntax

### 1.1 Comments

Lines starting with `/` are ignored by the interpreter.

```txt
/ This is a comment.
```

### 1.2 Values and Types

Aergia supports three primary types:

* Integers: `42`, `-7`
* Floats: `3.14`, `.5`
* Strings: `"Hello, World!"`

### 1.3 Implicit Evaluation

Simply stating a value or variable evaluates it. In any block, the last evaluated expression acts as the "result."

```txt
/ Evaluates to 1.2
1.2

/ Evaluates to "Hello"
"Hello"
```

## 2. Variables

Variables are assigned using the `=` prefix operator.

**Syntax:** `= <identifier> <expression>`

```txt
/ Sets variable `num` to 3.2
= num 3.2

/ Sets `x` to the result of (5 + 2)
= x + 5 2

/ Referencing a variable evaluates to its value
x
```



## 3. I/O (Input/Output)

### 3.1 Output

The `>` operator prints the evaluated expression to the console.

```txt
> "Hello, world!"
> + 10 5  / Prints 15
```

### 3.2 Input

Input operators halt execution and evaluate to the value entered by the user via stdin:

* `,` : Read String
* `.` : Read Integer
* `'` : Read Float

```txt
> "Enter your name:"
= name ,

> "Enter your age:"
= age .
```

## 4. Operations

All operations use prefix notation:

```
/ [OPERATOR] [ARG1] [ARG2]
+ 3 2
```

Operations can be nested:

```
* 2 + 3 4
```

### 4.1 Arithmetic

| Op | Action   | Example  | Result |
| -- | -------- | -------- | ------ |
| +  | Add      | `+ 5 2`  | 7      |
| -  | Subtract | `- 10 4` | 6      |
| *  | Multiply | `* 3 3`  | 9      |
| /  | Divide   | `/ 10 2` | 5      |
| ^  | Exponent | `^ 2 3`  | 8      |
| %  | Modulo   | `% 10 3` | 1      |

### 4.2 Bitwise & Logic

| Op  | Action      | Example  |
| --- | ----------- | -------- |
| \|  | Bitwise OR  | `\| x y` |
| &   | Bitwise AND | `& x y`  |
| $   | Bitwise XOR | `$ x y`  |
| ~   | Bitwise NOT | `~ x`    |
| !   | Logical NOT | `! x`    |

### 4.3 Comparison

Comparisons return `1` for true and `0` for false.

| Op | Action           | Example   |
| -- | ---------------- | --------- |
| == | Equals           | `== x 5`  |
| << | Less than        | `<< x 10` |
| >> | Greater than     | `>> x 0`  |
| <= | Less or equal    | `<= x 5`  |
| >= | Greater or equal | `>= x 5`  |



## 5. Control Flow

### 5.1 Conditionals (If/Else)

**Syntax:** `( [condition] [body] )`

An "else" block is defined by opening a second set of parentheses immediately after the first block's closing parenthesis.

```txt
= val .
( >> val 10
    > "Value is greater than 10"
(
    > "Value is 10 or less"
)
)
```

### 5.2 Loops (While)

**Syntax:** `[ [condition] [body] ]`

The block repeats as long as the condition evaluates to a non-zero value.

```txt
= count 0
[ << count 5
    > count
    = count + count 1
]
```

## 6. Example Program: Fibonacci Sequence

```txt
/ Aergia Fibonacci Sequence

> "How many numbers?"
= limit .
= n1 0
= n2 1
= i 0

[ << i limit
    > n1
    = temp + n1 n2
    = n1 n2
    = n2 temp
    = i + i 1
]
```
