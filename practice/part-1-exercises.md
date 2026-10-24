# Part 1 — Extra Practice: Python Fundamentals

> [Practice index](README.md) · [Solutions for this part](solutions/part-1-solutions.md)

These 10 problems go beyond the exercises inside the chapters. Try each one on your own before opening the solutions. Run your code, compare with your prediction, and only then check the solution. Related chapters:

- [Chapter 01 — Introduction to Programming and Python](../notes/01-introduction-to-programming-and-python.md)
- [Chapter 02 — Installation and Environment Setup](../notes/02-installation-and-environment-setup.md)
- [Chapter 03 — Built-in Functions, print() and Modules](../notes/03-builtin-functions-print-and-modules.md)
- [Chapter 04 — Errors and Identifiers](../notes/04-errors-and-identifiers.md)

Tips: write a few lines at a time and run often; if you are stuck for more than ten minutes read only the hint again, then the solution's explanation; afterwards rewrite the solution from memory.

## P1.1 — Print with separators

Print the three words `red`, `green`, `blue` on one line separated by ` | `, then print `done` on the same line after a final space using the `end` argument, and finally print an empty line.

*Hint:* `print(..., sep=..., end=...)`.

## P1.2 — Circle area with the math module

Use the `math` module to compute the area of a circle of radius 3 and print it rounded to 2 decimal places.

*Hint:* `math.pi`, `round()`.

## P1.3 — Valid identifiers

For each name in `['total', '2nd_place', 'my-var', 'class', '_hidden', 'Name']` print whether it is a valid variable name (a legal identifier that is not a Python keyword).

*Hint:* `str.isidentifier()` and `keyword.iskeyword()`.

## P1.4 — Fix the syntax error

The program below does not run. Find the problems and write the corrected version, then run it.

Given code:

```text
print("Total is" total)
if total > 3
    print("big")
```

*Hint:* Read the error messages from the top; one is a missing operator or comma, another a missing colon. Define `total` first.

## P1.5 — Catch a NameError

Write code that tries to print an undefined variable `missing_value`, catches the error, and prints the error's type name and message.

*Hint:* `try` / `except Exception as error`, `type(error).__name__`.

## P1.6 — Built-in functions on a list

For `numbers = [4, 8, 15, 16, 23, 42]` print the length, minimum, maximum, sum, the sorted list in descending order, and the average rounded to 2 decimals.

*Hint:* `len`, `min`, `max`, `sum`, `sorted(..., reverse=True)`.

## P1.7 — Escape sequences

Print exactly these three lines using escape sequences in as few `print` calls as you like: a line with a tab between `Name` and `Age`, a line with the quote `She said "hi"`, and a line with a backslash `C:\\temp` shown as `C:\temp`.

*Hint:* `\t`, `\"`, `\\`.

## P1.8 — Swap two variables

Given `a = 3` and `b = 7`, swap their values without using a third variable and print both.

*Hint:* Tuple assignment.

## P1.9 — Age next year

Given `birth_year = 2000` and `current_year = 2026`, print `Age now: 26` and `Age next year: 27` using variables and an f-string.

*Hint:* `f"...{expression}..."`.

## P1.10 — Check the Python version safely

Print `True` if the running Python is version 3.8 or newer, using `sys.version_info`.

*Hint:* Tuples compare element by element.

---

Solutions: [part-1-solutions.md](solutions/part-1-solutions.md) · Back to the [practice index](README.md).
