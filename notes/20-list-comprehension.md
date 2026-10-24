# Chapter 20 — List Comprehension

> Part 4 — Python Data Structures · Video: 6:33:38–6:48:42 · Previous: [19 List Functions, Methods and Copying](19-list-functions-methods-and-copying.md) · Next: [21 Tuples](21-tuples.md)

**In this chapter:** the compact syntax for building a list from another iterable: the basic form, adding a filter with `if`, choosing between two values with a conditional expression, nesting loops, and when a plain `for` loop is the better choice. Dictionary, set and generator versions are mentioned briefly.

**Before you start:** you need `for` loops and `range` from [The for Loop](17-for-loop-range-and-nested-loops.md#the-for-loop), `append` from [List Methods](19-list-functions-methods-and-copying.md#list-methods), and conditions from [Conditional Statements](14-conditional-statements.md). Recap: a loop that builds a list usually starts with `result = []` and calls `result.append(...)` each round. Examples were run with Python 3.13.

---

## List Comprehension

**Timestamp:** [6:33:38](https://www.youtube.com/watch?v=J9BI0jGOds8&t=23618s)

**Learning objectives:**

- Rewrite a loop that builds a list as a list comprehension, and the reverse.
- Add a filter condition, and use a conditional expression to transform items differently.
- Write a comprehension with two loops, and explain the order of the loops.
- Decide when a comprehension is too complicated and a loop is better.

**1. Intuition**

A list comprehension is a recipe card for a new list: "take each item from this source, optionally keep only the ones that pass a test, and write down this expression for each". It reads almost like the sentence "the squares of the numbers from 1 to 5". It describes *what* the new list contains instead of listing the steps of how to build it.

**2. Why does it exist?**

Building a new list from an old one is one of the most common jobs in programming: convert every value, keep only some, extract one field. The loop version needs three or four lines (create an empty list, loop, test, append). A comprehension does the same in one clear line, and it is usually a little faster. Python offers it because the pattern is so common that giving it a short form makes programs easier to read.

**3. Technical explanation**

The general form is:

```text
[expression for item in iterable if condition]
```

It is evaluated like this:

1. Take each `item` from the `iterable`, in order.
2. If there is an `if condition` part (the *filter*) and it is false, skip the item.
3. Compute `expression` using the item and put the result in the new list.

Variations:

- *Without a filter*: `[n * n for n in range(5)]`.
- *With a filter*: `[n for n in numbers if n > 0]` keeps the items that pass.
- *With a conditional expression* (choose between two values for every item): `["even" if n % 2 == 0 else "odd" for n in numbers]`. Here `if ... else ...` comes *before* the `for`, because it is part of the expression and not a filter. A filter `if` (with no `else`) comes *after* the `for`.
- *Nested loops*: `[(a, b) for a in first for b in second]`. The loops are written in the same order as the equivalent nested `for` statements: first the outer one, then the inner one.
- *Several conditions*: `[n for n in numbers if n > 0 if n % 2 == 0]` or combine with `and`.

Further facts:

- The comprehension builds a new list and does not change the source.
- In Python 3 the loop variable lives only inside the comprehension, so it does not leak into the surrounding code.
- The same idea exists for other containers: set comprehensions `{x for x in ...}`, dictionary comprehensions `{k: v for ...}`, and generator expressions `(x for x in ...)` that produce items one at a time without building a list.
- Readability limit: if the comprehension needs several loops, several conditions, or a long expression, use a normal `for` loop.

**4. Syntax**

```text
[expression for item in iterable]
[expression for item in iterable if condition]
[value_if_true if condition else value_if_false for item in iterable]
[expression for outer in outer_iterable for inner in inner_iterable]
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
squares_loop = []
for n in range(1, 6):
    squares_loop.append(n * n)

squares = [n * n for n in range(1, 6)]
print(squares_loop == squares, squares)

words = ["apple", "kiwi", "banana"]
print([word.upper() for word in words])
print([len(word) for word in words])

numbers = [4, -1, 7, -3, 0, 10]
print([n for n in numbers if n > 0])
print([n * 2 for n in numbers if n % 2 == 0])
print(["even" if n % 2 == 0 else "odd" for n in numbers])
```

Output:

```text
True [1, 4, 9, 16, 25]
['APPLE', 'KIWI', 'BANANA']
[5, 4, 6]
[4, 7, 10]
[8, 0, 20]
['even', 'odd', 'odd', 'odd', 'even', 'even']
```

Line by line:

- The first two versions give the same list. The comprehension is the loop version squeezed into one line: the expression `n * n` comes first, then the loop header.
- `[word.upper() for word in words]` transforms every item. `[len(word) ...]` replaces each word with its length.
- `if n > 0` after the loop is a *filter*: only the positive numbers are kept. In the next line the filter keeps even numbers and then doubles them.
- `"even" if n % 2 == 0 else "odd"` comes before `for`, because it picks a value for every item, with no item removed.

**6. Example 2 — Practical**

```python
prices = [250, 99, 400, 75, 180]
with_tax = [round(price * 1.18, 2) for price in prices]
print(with_tax)

cheap = [price for price in prices if price < 200]
print(cheap)

sentence = "Python makes data tasks simple and fun"
long_words = [word for word in sentence.split() if len(word) > 4]
print(long_words)
print([word[0].upper() for word in sentence.split()])

raw = ["  Asha ", "ravi", " MEENA"]
clean = [name.strip().title() for name in raw]
print(clean)

students = [("Asha", 82), ("Ravi", 67), ("Meena", 91)]
passed = [name for name, score in students if score >= 70]
print(passed)

grades = [(name, "pass" if score >= 70 else "retry") for name, score in students]
print(grades)

text = "Data 2024: 3 models, 12 datasets"
digits = [int(ch) for ch in text if ch.isdigit()]
print(digits, sum(digits))

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [value for row in matrix for value in row]
transposed = [[row[i] for row in matrix] for i in range(3)]
print(flat)
print(transposed)

pairs = [(a, b) for a in range(1, 4) for b in range(1, 4) if a < b]
print(pairs)

table = [[row * col for col in range(1, 4)] for row in range(1, 4)]
print(table)
```

Output:

```text
[295.0, 116.82, 472.0, 88.5, 212.4]
[99, 75, 180]
['Python', 'makes', 'tasks', 'simple']
['P', 'M', 'D', 'T', 'S', 'A', 'F']
['Asha', 'Ravi', 'Meena']
['Asha', 'Meena']
[('Asha', 'pass'), ('Ravi', 'retry'), ('Meena', 'pass')]
[2, 0, 2, 4, 3, 1, 2] 14
[1, 2, 3, 4, 5, 6, 7, 8, 9]
[[1, 4, 7], [2, 5, 8], [3, 6, 9]]
[(1, 2), (1, 3), (2, 3)]
[[1, 2, 3], [2, 4, 6], [3, 6, 9]]
```

Line by line:

- `with_tax` converts every price; `cheap` keeps only the prices under 200.
- The sentence examples split into words, filter by length, and take initial letters.
- `strip().title()` cleans every name (see [String Methods](10-ord-chr-and-string-methods.md#string-methods)).
- Unpacking `name, score` in the loop header (see [Tuples](21-tuples.md#tuples)) lets the filter use the score while the expression keeps the name. The `grades` version uses a conditional expression and keeps all students.
- The digit example turns every digit character into an integer and adds them up.
- `flat` uses two loops in the same order as nested `for` statements: first `row`, then `value`. `transposed` is a comprehension inside a comprehension, giving a list of lists (the columns become rows).
- `pairs` combines two loops with a filter so that each pair appears once, with `a < b`.
- `table` builds a 3 x 3 multiplication grid: the outer comprehension makes the rows, and the inner one builds each row. Because the inner list is created anew for every row, the rows do not share data (compare the `[[0] * 3] * 3` problem in [Copying Lists](19-list-functions-methods-and-copying.md#copying-lists)).

**7. Example 3 — Edge case or common mistake**

The filter `if` and the conditional-expression `if ... else` are different and sit in different places:

```python
numbers = [1, 2, 3, 4]

print([n for n in numbers if n % 2 == 0])
print([n if n % 2 == 0 else 0 for n in numbers])
```

Output:

```text
[2, 4]
[0, 2, 0, 4]
```

The first removes the odd numbers, so the result is shorter. The second keeps every position and replaces the odd numbers by 0.

Putting the `else` in the filter position is a syntax error, and so is a conditional expression without `else`:

```text
[n for n in numbers if n % 2 == 0 else 0]
[n if n % 2 == 0 for n in numbers]
```

```text
SyntaxError: invalid syntax
```

(These are shown as text because they are not valid code.) Remember: a filter has no `else`; a choice between two values must have an `else` and goes at the front.

Over-complicated comprehensions are hard to read. Compare:

```python
data = [[3, -1, 4], [], [-5, 9, 2]]

hard = [y * 2 for x in data if x for y in x if y > 0 if y % 2 == 1 or y > 3]
print(hard)

easy = []
for row in data:
    for value in row:
        if value > 0 and (value % 2 == 1 or value > 3):
            easy.append(value * 2)
print(easy)
```

Output:

```text
[6, 8, 18]
[6, 8, 18]
```

Both give the same list, but the second version can be read and debugged line by line. Prefer the loop when the logic needs more than one filter, or a nested loop with conditions.

A comprehension is for building a list. If you only want a side effect such as printing, use a normal loop:

```python
[print(n) for n in range(2)]
for n in range(2):
    print(n)
```

Output:

```text
0
1
0
1
```

The first line also built and threw away a list of `None` values (the results of `print`). Do not use comprehensions for side effects.

Also compare memory behaviour: a list comprehension builds the whole list at once; a generator expression builds items on demand:

```python
squares_list = [n * n for n in range(5)]
squares_gen = (n * n for n in range(5))
print(squares_list)
print(type(squares_gen).__name__)
print(sum(squares_gen))
print(sum(squares_gen))
```

Output:

```text
[0, 1, 4, 9, 16]
generator
30
0
```

The generator produces values once. After it is used up it is empty, so the second `sum` is 0.

**8. Common mistakes**

- Putting `else` after the loop (it belongs at the front, as part of the expression).
- Leaving out `else` in a conditional expression.
- Writing the loops in the wrong order in nested comprehensions.
- Writing very long or deeply nested comprehensions that nobody can read.
- Using a comprehension only for its side effects (such as `print`).
- Expecting the comprehension to change the original list; it creates a new one.
- Forgetting that building a huge list uses memory; a generator expression may be better.

**9. Real-world and AI applications**

Comprehensions are everywhere in data preparation: lowercasing and stripping every text in a dataset, keeping only the records above a quality threshold, extracting one field from a list of dictionaries (`[row["text"] for row in rows]`), turning labels into numbers, and splitting a long text into chunks (`[text[i:i + 500] for i in range(0, len(text), 500)]`). In the toy retrieval examples later in this handbook, a comprehension scores every document against a query before the best ones are picked (see [Retrieval-Augmented Generation](37-retrieval-augmented-generation.md)).

**10. Practice**

1. Create a list of the cubes of 1 to 8 with a comprehension.
2. From `[12, 7, 25, 30, 41, 8]`, keep the numbers divisible by 5.
3. Convert `["10", "20", "x", "40"]` to integers, skipping non-digit strings.
4. Create labels `"high"` or `"low"` for the scores `[45, 82, 67, 91]`, with 70 as the border.
5. Turn `[[1, 2], [3, 4], [5, 6]]` into the flat list `[1, 2, 3, 4, 5, 6]`.
6. Write all (letter, number) pairs for letters `"ab"` and numbers 1 to 3.
7. Rewrite this loop as a comprehension: `result = []`, `for w in words:`, `if w.startswith("a"):`, `result.append(w.upper())`.
8. Explain why `[x if x > 0 for x in nums]` is a syntax error and fix it so that negatives become 0.

**11. Interview questions**

- *What is a list comprehension?* A compact expression that builds a new list from an iterable, with an optional filter.
- *Where does the `if` go for a filter, and where for choosing between two values?* A filter goes after the `for`; a conditional expression with `else` goes before it.
- *Is a comprehension faster than a loop with `append`?* Usually somewhat, but readability matters more.
- *What is the difference between a list comprehension and a generator expression?* The list is built at once and stored; the generator produces one item at a time and can be used only once.
- *When would you not use a comprehension?* For complex logic, side effects, or very long expressions.

**12. Quick revision**

- `[expr for x in iterable]` maps; `[expr for x in iterable if test]` filters.
- `[a if test else b for x in iterable]` chooses a value per item (no removal).
- Nested loops are written in the same order as nested `for` statements.
- Builds a new list; does not change the source.
- If it is hard to read, use a loop.

---

## Answers to Practice Exercises

### Answers: List Comprehension

1.

```python
cubes = [n ** 3 for n in range(1, 9)]
print(cubes)
```

Output:

```text
[1, 8, 27, 64, 125, 216, 343, 512]
```

2.

```python
numbers = [12, 7, 25, 30, 41, 8]
print([n for n in numbers if n % 5 == 0])
```

Output:

```text
[25, 30]
```

3.

```python
raw = ["10", "20", "x", "40"]
print([int(text) for text in raw if text.isdigit()])
```

Output:

```text
[10, 20, 40]
```

4.

```python
scores = [45, 82, 67, 91]
print(["high" if score >= 70 else "low" for score in scores])
```

Output:

```text
['low', 'high', 'low', 'high']
```

5.

```python
nested = [[1, 2], [3, 4], [5, 6]]
print([value for pair in nested for value in pair])
```

Output:

```text
[1, 2, 3, 4, 5, 6]
```

6.

```python
print([(letter, number) for letter in "ab" for number in range(1, 4)])
```

Output:

```text
[('a', 1), ('a', 2), ('a', 3), ('b', 1), ('b', 2), ('b', 3)]
```

7.

```python
words = ["apple", "banana", "avocado", "cherry"]
result = [w.upper() for w in words if w.startswith("a")]
print(result)
```

Output:

```text
['APPLE', 'AVOCADO']
```

8. A conditional expression needs an `else`, and it goes in front of the `for`. A bare `if` after the loop is a filter, which cannot have an `else`. Fix:

```python
nums = [3, -2, 5, -7]
print([x if x > 0 else 0 for x in nums])
```

Output:

```text
[3, 0, 5, 0]
```

---

## Chapter Summary and Key Takeaways

- `[expression for item in iterable]` builds a new list; add `if condition` after the loop to filter items.
- To pick between two values for every item, use `value_a if test else value_b` at the front, with the `else` required.
- Nested loops in a comprehension run in the same order as nested `for` statements; a comprehension inside a comprehension builds lists of lists.
- Prefer a normal loop when the logic is complex, and never use a comprehension just for side effects.
- Set and dictionary comprehensions work the same way, and a generator expression (with round brackets) produces values lazily and can be used once.

Next: [Chapter 21 — Tuples](21-tuples.md) covers the immutable sibling of the list.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
