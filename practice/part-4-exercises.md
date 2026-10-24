# Part 4 — Extra Practice: Python Data Structures

> [Practice index](README.md) · [Solutions for this part](solutions/part-4-solutions.md)

These 11 problems go beyond the exercises inside the chapters. Try each one on your own before opening the solutions. Run your code, compare with your prediction, and only then check the solution. Related chapters:

- [Chapter 18 — Data Structures Introduction and Lists](../notes/18-lists-fundamentals.md)
- [Chapter 19 — List Functions, Methods and Copying](../notes/19-list-functions-methods-and-copying.md)
- [Chapter 20 — List Comprehension](../notes/20-list-comprehension.md)
- [Chapter 21 — Tuples](../notes/21-tuples.md)
- [Chapter 22 — Sets](../notes/22-sets.md)
- [Chapter 23 — Dictionaries](../notes/23-dictionaries.md)
- [Chapter 24 — Mutability, Iteration and Common Data-Structure Pitfalls](../notes/24-mutability-iteration-and-pitfalls.md)

Tips: write a few lines at a time and run often; if you are stuck for more than ten minutes read only the hint again, then the solution's explanation; afterwards rewrite the solution from memory.

## P4.1 — List operations

Start with `items = ["b", "d"]`. Append `"e"`, insert `"a"` at the front, insert `"c"` at index 3, remove `"e"`, pop the last item (print it) and print the list after each change.

*Hint:* `append`, `insert`, `remove`, `pop`.

## P4.2 — Alias versus copy

Create `a = [1, 2, 3]`, `b = a`, `c = a.copy()`. Append 4 to `a` and print all three lists. Then show a nested list `m = [[1], [2]]` where a shallow copy still shares the inner lists.

*Hint:* `copy.deepcopy` for nested data.

## P4.3 — Comprehension

Build the list of squares of the even numbers from 1 to 10, and a list of the words in `"the quick brown fox"` that have more than 3 letters, in upper case.

*Hint:* `[expression for item in iterable if condition]`.

## P4.4 — Tuple unpacking

Given `point = (3, 4)` unpack it into `x` and `y`. Then write a function returning `(min, max)` of a list and unpack its result. Finally unpack `first, *middle, last = [1, 2, 3, 4, 5]`.

*Hint:* Starred unpacking collects the rest into a list.

## P4.5 — Set operations

With `a = {1, 2, 3, 4}` and `b = {3, 4, 5}` print the union, intersection, difference `a - b`, symmetric difference, and whether `{1, 2}` is a subset of `a`. Use `sorted` for stable output.

*Hint:* `|`, `&`, `-`, `^`, `<=`.

## P4.6 — Word frequency

Count how often each word occurs in `"to be or not to be that is the question to be"` and print the words by count (highest first, ties alphabetical).

*Hint:* A dictionary with `get`, or `collections.Counter`.

## P4.7 — Invert a dictionary

Invert `{"a": 1, "b": 2, "c": 1}` so that each value maps to a list of keys.

*Hint:* `setdefault(value, []).append(key)`.

## P4.8 — Remove duplicates, keep order

Remove duplicates from `[3, 1, 3, 2, 1, 4]` keeping the first occurrence of each.

*Hint:* A `seen` set, or `dict.fromkeys`.

## P4.9 — Transpose a matrix

Transpose `[[1, 2, 3], [4, 5, 6]]` (rows become columns) using `zip` and then using a nested comprehension.

*Hint:* `zip(*matrix)`.

## P4.10 — Remove while iterating, safely

Remove all negative numbers from `[4, -1, -2, 7, -3, 8]` correctly. First show what goes wrong when you remove inside a `for` loop over the same list.

*Hint:* Iterate over a copy, or build a new list.

## P4.11 — Group words by first letter

Group `["apple", "avocado", "banana", "blueberry", "cherry"]` into a dictionary from first letter to a list of words.

*Hint:* `dict.setdefault` or `collections.defaultdict(list)`.

---

Solutions: [part-4-solutions.md](solutions/part-4-solutions.md) · Back to the [practice index](README.md).
