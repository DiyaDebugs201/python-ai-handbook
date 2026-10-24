# Part 2 — Extra Practice: Data Types and Strings

> [Practice index](README.md) · [Solutions for this part](solutions/part-2-solutions.md)

These 11 problems go beyond the exercises inside the chapters. Try each one on your own before opening the solutions. Run your code, compare with your prediction, and only then check the solution. Related chapters:

- [Chapter 05 — Numeric Types and Booleans](../notes/05-numeric-types-and-booleans.md)
- [Chapter 06 — Strings: Basics, Indexing, Concatenation and Repetition](../notes/06-strings-basics-indexing-concatenation.md)
- [Chapter 07 — String Slicing](../notes/07-string-slicing.md)
- [Chapter 08 — Type Conversion](../notes/08-type-conversion.md)
- [Chapter 09 — String Formatting and f-Strings](../notes/09-string-formatting-and-f-strings.md)
- [Chapter 10 — ord(), chr() and String Methods](../notes/10-ord-chr-and-string-methods.md)

Tips: write a few lines at a time and run often; if you are stuck for more than ten minutes read only the hint again, then the solution's explanation; afterwards rewrite the solution from memory.

## P2.1 — Types of results

Print the type of each result: `7 / 2`, `7 // 2`, `7 % 2`, `2 ** 10`, `True + True`, `"5" * 3`.

*Hint:* `type(...)`, and also print the value.

## P2.2 — Floating-point comparison

Show that `0.1 + 0.2 == 0.3` is `False`, then compare them correctly in two ways: with `round` and with `math.isclose`.

*Hint:* `math.isclose(a, b)`.

## P2.3 — Palindrome check

Write a function `is_palindrome(text)` that ignores case, spaces and punctuation. Test it on `"A man, a plan, a canal: Panama"` and `"Python"`.

*Hint:* Keep only characters where `ch.isalnum()`; compare with the reversed slice `[::-1]`.

## P2.4 — Slicing practice

For `word = "Programming"` print: the first 3 characters, the last 3, every second character, the string reversed, and the middle part from index 3 up to (not including) index 8.

*Hint:* `word[:3]`, `word[-3:]`, `word[::2]`, `word[::-1]`, `word[3:8]`.

## P2.5 — Safe conversion

Convert the list `["3", "4.5", "x", "10"]` to floats. Collect the converted values in one list and the strings that failed in another, then print both.

*Hint:* `try` / `except ValueError` inside a loop.

## P2.6 — Aligned table with f-strings

Print the numbers 1 to 5 with their squares and cubes as a table with right-aligned columns of width 4, 8 and 8, and a header row.

*Hint:* `f"{value:>4}"`.

## P2.7 — Caesar cipher

Write `shift(text, k)` that shifts each lowercase letter k places forward in the alphabet (wrapping from `z` to `a`) and leaves other characters unchanged. Encrypt `"hello, world"` with k=3 and decrypt it again.

*Hint:* `ord`, `chr`, and the modulo operator `%` for wrapping.

## P2.8 — Count vowels

Count the vowels in `"Learning Python is Fun"` (case-insensitive) using a string method and a loop or comprehension.

*Hint:* `text.lower()`, `text.count(letter)`.

## P2.9 — Clean and title-case

Turn `"  hELLo    wORLD  "` into `"Hello World"`.

*Hint:* `split()` with no argument splits on any whitespace; `str.capitalize`; `" ".join(...)`.

## P2.10 — Format money

Print `1234567.891` as `1,234,567.89` and `0.256` as `25.6%`.

*Hint:* Format specs `,.2f` and `.1%`.

## P2.11 — Truthiness table

Print `bool(x)` for each of `0`, `1`, `""`, `"0"`, `[]`, `[0]`, `None`, `0.0`.

*Hint:* Empty containers, zero and `None` are falsy.

---

Solutions: [part-2-solutions.md](solutions/part-2-solutions.md) · Back to the [practice index](README.md).
