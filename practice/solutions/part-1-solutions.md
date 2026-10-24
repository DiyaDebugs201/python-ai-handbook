# Part 1 — Solutions: Python Fundamentals

> [Practice index](../README.md) · [Problems for this part](../part-1-exercises.md)

Every program below was run with Python 3.13 and the output shown is the real output. Your own solution may differ and still be correct: compare behaviour, not wording.

## P1.1 — Print with separators

Print the three words `red`, `green`, `blue` on one line separated by ` | `, then print `done` on the same line after a final space using the `end` argument, and finally print an empty line.

```python
print("red", "green", "blue", sep=" | ", end=" ")
print("done")
print()
print("next line")
```

Output:

```text
red | green | blue done

next line
```

`sep` sets the text between items and `end` replaces the default newline, so the second `print` continues on the same line.

## P1.2 — Circle area with the math module

Use the `math` module to compute the area of a circle of radius 3 and print it rounded to 2 decimal places.

```python
import math

radius = 3
area = math.pi * radius ** 2
print(round(area, 2))
```

Output:

```text
28.27
```

`import math` makes `math.pi` available; `**` is the power operator and `round(x, 2)` keeps two decimals.

## P1.3 — Valid identifiers

For each name in `['total', '2nd_place', 'my-var', 'class', '_hidden', 'Name']` print whether it is a valid variable name (a legal identifier that is not a Python keyword).

```python
import keyword

names = ["total", "2nd_place", "my-var", "class", "_hidden", "Name"]
for name in names:
    valid = name.isidentifier() and not keyword.iskeyword(name)
    print(f"{name:<10} {valid}")
```

Output:

```text
total      True
2nd_place  False
my-var     False
class      False
_hidden    True
Name       True
```

A valid name must be an identifier (letters, digits, underscore; not starting with a digit) and must not be a reserved keyword such as `class`.

## P1.4 — Fix the syntax error

The program below does not run. Find the problems and write the corrected version, then run it.

Given code:

```text
print("Total is" total)
if total > 3
    print("big")
```

```python
total = 5
print("Total is", total)
if total > 3:
    print("big")
```

Output:

```text
Total is 5
big
```

The first line needs a comma between the string and the variable, the `if` line needs a colon, and `total` must exist before it is used.

## P1.5 — Catch a NameError

Write code that tries to print an undefined variable `missing_value`, catches the error, and prints the error's type name and message.

```python
try:
    print(missing_value)
except Exception as error:
    print(type(error).__name__ + ":", error)
```

Output:

```text
NameError: name 'missing_value' is not defined
```

Python raises `NameError` for an unknown name; catching it lets the program continue and report the problem.

## P1.6 — Built-in functions on a list

For `numbers = [4, 8, 15, 16, 23, 42]` print the length, minimum, maximum, sum, the sorted list in descending order, and the average rounded to 2 decimals.

```python
numbers = [4, 8, 15, 16, 23, 42]
print(len(numbers), min(numbers), max(numbers), sum(numbers))
print(sorted(numbers, reverse=True))
print(round(sum(numbers) / len(numbers), 2))
```

Output:

```text
6 4 42 108
[42, 23, 16, 15, 8, 4]
18.0
```

Built-in functions work on any list of numbers; `sorted` returns a new list and leaves the original unchanged.

## P1.7 — Escape sequences

Print exactly these three lines using escape sequences in as few `print` calls as you like: a line with a tab between `Name` and `Age`, a line with the quote `She said "hi"`, and a line with a backslash `C:\\temp` shown as `C:\temp`.

```python
print("Name\tAge")
print("She said \"hi\"")
print("C:\\temp")
```

Output:

```text
Name	Age
She said "hi"
C:\temp
```

A backslash starts an escape sequence in a normal string; `\\` produces one literal backslash.

## P1.8 — Swap two variables

Given `a = 3` and `b = 7`, swap their values without using a third variable and print both.

```python
a, b = 3, 7
a, b = b, a
print(a, b)
```

Output:

```text
7 3
```

The right side `(b, a)` is built first, then unpacked into `a` and `b`, so no temporary variable is needed.

## P1.9 — Age next year

Given `birth_year = 2000` and `current_year = 2026`, print `Age now: 26` and `Age next year: 27` using variables and an f-string.

```python
birth_year = 2000
current_year = 2026
age = current_year - birth_year
print(f"Age now: {age}")
print(f"Age next year: {age + 1}")
```

Output:

```text
Age now: 26
Age next year: 27
```

f-strings evaluate expressions inside braces, so `age + 1` can be computed in place.

## P1.10 — Check the Python version safely

Print `True` if the running Python is version 3.8 or newer, using `sys.version_info`.

```python
import sys

print(sys.version_info >= (3, 8))
```

Output:

```text
True
```

`sys.version_info` compares like a tuple, so `(3, 13, ...) >= (3, 8)` is true on any modern version.

---

Back to the [problems](../part-1-exercises.md) or the [practice index](../README.md).
