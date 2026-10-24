# Chapter 29 — map(), filter() and reduce()

> Part 5 — Functions and Functional Programming · Video: 10:32:38–10:47:48 · Previous: [28 First-Class Functions and Lambda](28-first-class-functions-and-lambda.md) · Next: [30 Python Wrap-Up and Introduction to the AI Section](30-python-wrap-up-and-ai-intro.md)

**In this chapter:** three classic "functional" tools that take a function and apply it to a collection: `map()` to transform every item, `filter()` to keep only the items that pass a test, and `reduce()` to combine all items into one value. You will also see how each compares with a list comprehension, and how they combine into a small data pipeline.

**Before you start:** you need functions as values and lambdas from [Functions as First-Class Citizens](28-first-class-functions-and-lambda.md#functions-as-first-class-citizens) and [Lambda Functions](28-first-class-functions-and-lambda.md#lambda-functions), list comprehensions from [List Comprehension](20-list-comprehension.md#list-comprehension), and modules and `import` from [Built-in Functions, print() and Modules](03-builtin-functions-print-and-modules.md). Recap: a function can be passed as an argument; `lambda x: x * 2` is a one-line unnamed function; `import` makes the contents of a module available. Examples were run with Python 3.13.

---

## The map() Function

**Timestamp:** [10:32:38](https://www.youtube.com/watch?v=J9BI0jGOds8&t=37958s)

**Learning objectives:**

- Use `map(function, iterable)` to transform every item.
- Explain that `map` returns a lazy iterator and how to turn it into a list.
- Use `map` with several iterables.
- Decide between `map` and a list comprehension.

**1. Intuition**

A conveyor belt with a machine on it: every item that passes under the machine gets the same treatment (stamped, painted, converted), and a new item comes out the other side. `map` is the machine; you supply the operation.

**2. Why does it exist?**

"Do the same thing to every item" is one of the most common tasks in data work: convert strings to numbers, clean every line, scale every value. `map` states this in one expression, separating *what to do* (the function) from *what to do it to* (the data). It also comes from the functional programming tradition, where such building blocks are combined into pipelines.

**3. Technical explanation**

`map(function, iterable)` applies `function` to each item and gives back the results.

- The result is a **map object**, a lazy iterator: the function runs as the results are *consumed* (by `list(...)`, a `for` loop, `sum`, and so on). Printing a `map` object directly shows `<map object at ...>`, not the values.
- An iterator can be used only once; after it is consumed it is empty (see [Iterating Safely](24-mutability-iteration-and-pitfalls.md#iterating-safely)).
- With several iterables, `map(f, a, b)` calls `f(a_item, b_item)` pairwise and stops at the shortest iterable.
- The function can be a built-in (`int`, `str`, `len`, `str.upper`), your own function, or a lambda.
- Equivalent list comprehension: `[function(x) for x in iterable]`. Many Python programmers prefer the comprehension for readability, but `map` is natural when the function already exists (`map(int, texts)`).
- `map` does not change the original collection.

**4. Syntax**

```text
map(function, iterable)
map(function, iterable1, iterable2)
list(map(function, iterable))
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
numbers = [1, 2, 3, 4]
squares = map(lambda n: n * n, numbers)
print(type(squares).__name__)
print(list(squares))
print(list(squares))

print(list(map(str, numbers)))
print(list(map(len, ["a", "bb", "ccc"])))
print(list(map(str.upper, ["tea", "milk"])))
print(list(map(int, ["10", "20", "30"])))

print(list(map(lambda a, b: a + b, [1, 2, 3], [10, 20, 30])))
print(list(map(pow, [2, 3, 4], [1, 2, 3])))
print(numbers)
```

Output:

```text
map
[1, 4, 9, 16]
[]
['1', '2', '3', '4']
[1, 2, 3]
['TEA', 'MILK']
[10, 20, 30]
[11, 22, 33]
[2, 9, 64]
[1, 2, 3, 4]
```

Line by line:

- `map` returns a map object. The first `list(squares)` consumes it; the second finds it empty.
- Built-in functions work directly: `str` converts every number to text, `len` measures every string, and `int` converts strings to integers.
- With two lists, the function receives one item from each, so `lambda a, b: a + b` adds pairs. `pow` does the same with exponents.
- The original `numbers` list is not changed.

**6. Example 2 — Practical**

```python
prices = [100, 250, 80]
with_tax = list(map(lambda p: round(p * 1.18, 2), prices))
print(with_tax)

raw = ["  Asha ", "ravi", " MEENA "]
print(list(map(lambda name: name.strip().title(), raw)))

line = "12 7 30 5"
numbers = list(map(int, line.split()))
print(numbers, sum(numbers), max(numbers))

def to_celsius(f):
    return round((f - 32) * 5 / 9, 1)


print(list(map(to_celsius, [32, 98.6, 212])))

names = ["Asha", "Ravi"]
scores = [82, 67]
print(list(map(lambda n, s: f"{n}: {s}", names, scores)))

comprehension = [to_celsius(f) for f in [32, 98.6, 212]]
print(comprehension)

matrix = [[1, 2], [3, 4], [5, 6]]
print(list(map(sum, matrix)))
print(list(map(list, zip(*matrix))))

records = ["a=1", "b=2", "c=3"]
pairs = dict(map(lambda r: r.split("="), records))
print(pairs)

total_length = sum(map(len, ["one", "three", "five"]))
print(total_length)

for value in map(lambda n: n * 2, range(3)):
    print(value, end=" ")
print()
```

Output:

```text
[118.0, 295.0, 94.4]
['Asha', 'Ravi', 'Meena']
[12, 7, 30, 5] 54 30
[0.0, 37.0, 100.0]
['Asha: 82', 'Ravi: 67']
[0.0, 37.0, 100.0]
[3, 7, 11]
[[1, 3, 5], [2, 4, 6]]
{'a': '1', 'b': '2', 'c': '3'}
12
0 2 4 
```

Line by line:

- Applying tax, cleaning names and converting a line of text to numbers are the typical uses. `map(int, line.split())` is a very common idiom for reading numbers.
- A named function (`to_celsius`) can be used instead of a lambda, and the equivalent comprehension gives the same list: choose whichever reads better.
- `map` with two lists walks them in parallel.
- `map(sum, matrix)` sums each row; `zip(*matrix)` transposes the rows into columns, and `map(list, ...)` turns each column tuple into a list.
- `dict(map(...))` builds a dictionary from the lists produced by `split("=")`.
- `sum(map(len, ...))` uses the lazy iterator directly, with no intermediate list. A `for` loop over a `map` also works.

**7. Example 3 — Edge case or common mistake**

```python
numbers = [1, 2, 3]
result = map(lambda n: n * 2, numbers)
print(result == [2, 4, 6])
print(list(result) == [2, 4, 6])
print(list(result))
```

Output:

```text
False
True
[]
```

A map object is not a list, so comparing it to a list is `False`, and once it is converted, it is used up.

The function runs only when needed (lazy evaluation), which matters when it has side effects:

```python
def noisy(n):
    print("processing", n)
    return n * 10


lazy = map(noisy, [1, 2, 3])
print("map created, nothing processed yet")
first = next(lazy)
print("first result:", first)
print(list(lazy))
```

Output:

```text
map created, nothing processed yet
processing 1
first result: 10
processing 2
processing 3
[20, 30]
```

Nothing is processed when `map` is created. `next` takes one result, and `list` takes the rest. Using `map` just for side effects (printing) and never consuming it does nothing at all.

```python
mapped = map(print, ["never", "shown"])
print("created a map; nothing printed above")
```

Output:

```text
created a map; nothing printed above
```

Mismatched lengths and wrong function arity:

```python
print(list(map(lambda a, b: a + b, [1, 2, 3], [10, 20])))
try:
    print(list(map(lambda a, b: a + b, [1, 2, 3])))
except TypeError as error:
    print("TypeError:", error)
try:
    print(list(map(int, ["5", "x"])))
except ValueError as error:
    print("ValueError:", error)
```

Output:

```text
[11, 22]
TypeError: <lambda>() missing 1 required positional argument: 'b'
ValueError: invalid literal for int() with base 10: 'x'
```

`map` stops at the shortest list; a function that needs two arguments fails with one iterable; an error inside the function appears only when the results are consumed, and the earlier results are lost.

**8. Common mistakes**

- Printing a `map` object and expecting values (convert with `list`).
- Using a `map` object twice.
- Comparing a `map` object to a list.
- Using `map` for side effects (such as printing) without consuming it.
- Passing a function with the wrong number of parameters.
- Writing a complicated lambda when a named function or comprehension would be clearer.
- Forgetting that errors surface late, when the results are consumed.

**9. Real-world and AI applications**

`map` and its comprehension equivalent clean and convert whole datasets: strip and lower-case every text, convert every field to the right type, turn every sentence into a list of tokens, and apply a scoring function to every document. In data-processing libraries, "map" over a dataset is a standard operation (often written `dataset.map(function)`), and large systems use it to spread the same function over many machines. Because the Python version is lazy, a pipeline can process huge files one line at a time without holding them in memory.

**10. Practice**

1. Use `map` and a lambda to double every number in `[3, 6, 9]`.
2. Convert `["1.5", "2.5", "4"]` into floats with `map`.
3. Get the length of every word in a sentence with `map(len, ...)`.
4. Add two lists element by element using `map` with two iterables.
5. Rewrite `list(map(lambda x: x ** 2, range(5)))` as a comprehension.
6. Explain why `print(map(str, [1, 2]))` does not print `['1', '2']`.
7. Read the line `"3 4 5"` into a list of integers and print their product (use a loop).

**11. Interview questions**

- *What does `map` return?* A lazy iterator (a map object), not a list.
- *How is `map` related to a list comprehension?* `list(map(f, xs))` equals `[f(x) for x in xs]`; the comprehension is often more readable, `map` is neat with existing functions.
- *What happens when the iterables passed to `map` have different lengths?* It stops at the shortest.
- *Can you iterate over a map object twice?* No, it is exhausted after the first pass.

**12. Quick revision**

- `map(f, items)` applies `f` to every item, giving a lazy iterator; use `list()`.
- Several iterables: the function takes several arguments; stops at the shortest.
- Single use; evaluated lazily.
- Same result as `[f(x) for x in items]`.

---

## The filter() Function

**Timestamp:** [10:37:07](https://www.youtube.com/watch?v=J9BI0jGOds8&t=38227s)

**Learning objectives:**

- Use `filter(function, iterable)` to keep items for which the function returns a true value.
- Use `None` as the function to remove falsy items.
- Compare `filter` with a list comprehension that has an `if`.
- Combine `filter` and `map`.

**1. Intuition**

A coffee filter or a sieve: everything is poured through, and only what passes the test comes out. A bouncer at a door checks each person against a rule ("18 or older") and lets through only those who pass.

**2. Why does it exist?**

Selecting the items that satisfy a condition is as common as transforming them: keep the valid records, the positive numbers, the words longer than three letters. `filter` expresses it with a *test function* separate from the data, so the same test can be reused and swapped.

**3. Technical explanation**

`filter(function, iterable)` calls `function(item)` for each item and keeps the item if the result is **truthy**.

- The result is a **filter object**, a lazy iterator; wrap it in `list(...)` to see it. It can be consumed once.
- The test function must take **one** argument and return something that can be judged true or false. It does *not* have to return exactly `True`/`False`.
- `filter(None, iterable)` keeps the truthy items and drops `0`, `""`, `None`, `[]`, `False` and other falsy values.
- The items themselves are not changed, only selected; the original order is kept.
- Equivalent list comprehension: `[x for x in iterable if function(x)]`.
- To transform *and* select, combine them: `map(f, filter(test, items))`, or use a comprehension with both parts.

**4. Syntax**

```text
filter(function, iterable)
filter(None, iterable)
list(filter(function, iterable))
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
numbers = [5, 12, 7, 20, 3, 18]
big = filter(lambda n: n > 10, numbers)
print(type(big).__name__)
print(list(big))

print(list(filter(lambda n: n % 2 == 0, numbers)))
print(list(filter(str.isdigit, ["12", "ab", "7", "x1"])))
print(list(filter(None, [0, 1, "", "a", None, [], [0], False, True])))
print(list(filter(lambda w: len(w) > 3, ["tea", "coffee", "milk", "ok"])))
print(numbers)
```

Output:

```text
filter
[12, 20, 18]
[12, 20, 18]
['12', '7']
[1, 'a', [0], True]
['coffee', 'milk']
[5, 12, 7, 20, 3, 18]
```

Line by line:

- The test `n > 10` keeps 12, 20 and 18, in their original order. The result is a lazy filter object until converted.
- Built-in methods such as `str.isdigit` can serve as tests.
- With `None`, the filter removes every falsy item (`0`, `""`, `None`, `[]`, `False`) and keeps the truthy ones, including the non-empty list `[0]`.
- The original `numbers` list is unchanged.

**6. Example 2 — Practical**

```python
emails = ["asha@example.org", "bad-address", "ravi@example.org", "", "x@y"]
valid = list(filter(lambda e: "@" in e and "." in e.split("@")[-1], emails))
print(valid)

students = [("Asha", 82), ("Ravi", 45), ("Meena", 91), ("Kiran", 38)]
passed = list(filter(lambda s: s[1] >= 50, students))
print(passed)

def is_prime(n):
    if n < 2:
        return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return False
    return True


print(list(filter(is_prime, range(1, 30))))

words = ["Python", "is", "a", "popular", "language"]
print(list(filter(lambda w: w[0].isupper(), words)))

values = [3, -1, 0, 8, -5, 2]
positives_doubled = list(map(lambda n: n * 2, filter(lambda n: n > 0, values)))
print(positives_doubled)
print([n * 2 for n in values if n > 0])

lines = ["# title", "", "text one", "  ", "text two", "# note"]
content = list(filter(None, (line.strip() for line in lines if not line.startswith("#"))))
print(content)

def is_valid_age(text):
    return text.isdigit() and 0 < int(text) < 120


print(list(filter(is_valid_age, ["25", "abc", "150", "7", "-3"])))

records = [{"name": "Asha", "active": True}, {"name": "Ravi", "active": False}]
print([r["name"] for r in filter(lambda r: r["active"], records)])
```

Output:

```text
['asha@example.org', 'ravi@example.org']
[('Asha', 82), ('Meena', 91)]
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
['Python']
[6, 16, 4]
[6, 16, 4]
['text one', 'text two']
['25', '7']
['Asha']
```

Line by line:

- A simple email check uses a lambda that tests for `@` and a dot after it (real validation is more complicated).
- Tuples of `(name, score)` are filtered by their second item.
- A named test function (`is_prime`) can be reused anywhere. The function returns `True` or `False`, but any truthy or falsy value would work.
- `map(..., filter(...))` first selects the positive values and then doubles them; the list comprehension below it does both jobs in one expression.
- A generator expression strips each line, and `filter(None, ...)` removes the empty strings.
- `is_valid_age` shows a named test that checks a string and then a number; the `and` ensures `int(...)` runs only for digit strings.
- Filtering dictionaries by a field is a common pattern.

**7. Example 3 — Edge case or common mistake**

```python
numbers = [1, 2, 3, 4]
evens = filter(lambda n: n % 2 == 0, numbers)
print(evens == [2, 4], list(evens), list(evens))
```

Output:

```text
False [2, 4] []
```

As with `map`, a filter object is not a list and can be used once.

The test function should *return* a truth value; a function that prints or forgets `return` filters out everything:

```python
def bad_test(n):
    n > 2


def good_test(n):
    return n > 2


print(list(filter(bad_test, [1, 2, 3, 4])))
print(list(filter(good_test, [1, 2, 3, 4])))
```

Output:

```text
[]
[3, 4]
```

`bad_test` has no `return`, so it returns `None` for every item, which is falsy.

`filter(None, ...)` also drops legitimate zeros:

```python
scores = [0, 55, 0, 80]
print(list(filter(None, scores)))
print(list(filter(lambda s: s is not None, [0, None, 7])))
```

Output:

```text
[55, 80]
[0, 7]
```

If `0` is a valid value, do not use `None` as the test; check explicitly (`is not None`).

The test function takes exactly one argument:

```python
try:
    print(list(filter(lambda a, b: a > b, [1, 2, 3])))
except TypeError as error:
    print("TypeError:", error)
```

Output:

```text
TypeError: <lambda>() missing 1 required positional argument: 'b'
```

**8. Common mistakes**

- Treating a filter object as a list, or using it twice.
- Writing a test function that does not `return`.
- Using `filter(None, data)` when zero or empty values are meaningful.
- Giving `filter` a function with two parameters.
- Confusing `filter` (selects items) with `map` (transforms items); `filter` never changes the items.
- Using `map` when a selection was meant: `map(lambda n: n > 2, nums)` gives a list of `True`/`False`, not the numbers.

**9. Real-world and AI applications**

Filtering is the first step of nearly every data-preparation job: dropping empty or very short texts, removing records with missing fields, keeping only examples in the right language, throwing out duplicates or too-long documents before they are sent to a model. Retrieval systems filter documents by metadata (date, topic, permission) before ranking them. In dataset libraries, `dataset.filter(function)` has the same meaning as the built-in version.

**10. Practice**

1. Keep the numbers from `[4, 9, 15, 22, 31, 40]` that are divisible by 5, using `filter`.
2. From a list of words, keep those with at least five letters.
3. Remove empty strings and `None` from `["a", "", None, "b", "  "]` using `filter(None, ...)`. What happens to `"  "`?
4. Keep the students scoring 60 or more from a list of `(name, score)` tuples.
5. Use `filter` and `map` together: square the odd numbers from 1 to 9.
6. Write `is_palindrome(word)` and use `filter` to find the palindromes in `["level", "tea", "noon", "code"]`.
7. Explain why `list(filter(lambda n: n > 5, nums))` and `list(map(lambda n: n > 5, nums))` give different results.

**11. Interview questions**

- *What does `filter` do?* Keeps the items for which the function returns a true value, as a lazy iterator.
- *What does `filter(None, items)` do?* Keeps only the truthy items.
- *What is the difference between `map` and `filter`?* `map` transforms every item (the output has the same length); `filter` selects some of the items without changing them.
- *Does the test function of `filter` have to return a boolean?* No, any value is judged by truthiness.

**12. Quick revision**

- `filter(test, items)` keeps items for which `test(item)` is truthy; lazy, single-use.
- `filter(None, items)` removes falsy items (including zeros).
- The test function takes one argument and must `return`.
- Same as `[x for x in items if test(x)]`.
- `map` transforms; `filter` selects.

---

## The reduce() Function

**Timestamp:** [10:43:06](https://www.youtube.com/watch?v=J9BI0jGOds8&t=38586s)

**Learning objectives:**

- Import and use `functools.reduce(function, iterable, initial)`.
- Trace how `reduce` combines items two at a time.
- Use an initial value, and handle empty inputs.
- Recognise when a built-in (`sum`, `max`, `"".join`) or a loop is clearer.

**1. Intuition**

Rolling a snowball along a line of snow: the ball picks up each patch in turn and gets bigger. Or the accumulator pattern you already know (`total = 0; total += x`): start with something, fold in the next item, keep the running result, repeat. `reduce` is that loop packaged as a function: it *reduces* many items to a single value.

**2. Why does it exist?**

Many calculations combine a whole collection into one result: the sum, the product, the longest word, a merged dictionary. These all share the same shape: "take the result so far and the next item, produce a new result". `reduce` captures this shape once, so only the combining step (the function) has to be supplied.

**3. Technical explanation**

`reduce` lives in the `functools` module (it was moved there from the built-ins in Python 3): `from functools import reduce`.

`reduce(function, iterable, initial)`:

1. The function takes **two** arguments: the *accumulated result so far* and the *next item*.
2. If `initial` is given, the first call is `function(initial, first_item)`. If not, the first item is used as the starting accumulator, and the first call is `function(first_item, second_item)`.
3. The result of each call becomes the accumulator for the next call.
4. When the items run out, the accumulator is the final result.

For `reduce(f, [a, b, c, d])` the computation is `f(f(f(a, b), c), d)`: it combines from left to right.

Other facts:

- An empty iterable with an initial value returns the initial value. An empty iterable *without* an initial value raises `TypeError`.
- With one item and no initial value, that item is returned, and the function is never called.
- The initial value must suit the operation: 0 for a sum, 1 for a product, `[]` or `{}` for building collections, `""` for strings.
- Often a built-in does the same job better: `sum`, `min`, `max`, `any`, `all`, `math.prod`, `"".join`. Use `reduce` when no built-in matches, but a plain `for` loop is often more readable.
- `itertools.accumulate` is a related tool that gives the *running* results instead of only the final one.

**4. Syntax**

```text
from functools import reduce

reduce(function, iterable)
reduce(function, iterable, initial)
function(accumulator, item)  ->  new accumulator
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]
print(reduce(lambda acc, n: acc + n, numbers))
print(reduce(lambda acc, n: acc * n, numbers))
print(reduce(lambda acc, n: acc + n, numbers, 100))

def show_step(acc, n):
    result = acc + n
    print(f"acc={acc}, item={n} -> {result}")
    return result


print(reduce(show_step, [10, 20, 30]))
print(reduce(show_step, [10, 20, 30], 1000))
print(reduce(lambda a, b: a if a > b else b, [4, 9, 2]))
print(reduce(lambda a, b: a + b, [], 0))
print(reduce(lambda a, b: a + b, [7]))
```

Output:

```text
15
120
115
acc=10, item=20 -> 30
acc=30, item=30 -> 60
60
acc=1000, item=10 -> 1010
acc=1010, item=20 -> 1030
acc=1030, item=30 -> 1060
1060
9
0
7
```

Line by line:

- The first two calls compute the sum (15) and the product (120). The third starts from 100, so the result is 115.
- `show_step` prints the accumulator and the item at each step: without an initial value the first accumulator is the first item (10), and the function runs twice for three items. With initial 1000 it runs three times.
- The maximum is found by keeping the larger of the running result and the next item.
- An empty list with an initial value returns that value; a list with a single item and no initial value returns the item without calling the function.

**6. Example 2 — Practical**

```python
from functools import reduce
import math

words = ["data", "science", "with", "python"]
longest = reduce(lambda a, b: a if len(a) >= len(b) else b, words)
print(longest)

sentence = reduce(lambda acc, w: acc + " " + w, words)
print(sentence)

counts = reduce(
    lambda acc, ch: {**acc, ch: acc.get(ch, 0) + 1},
    "banana",
    {},
)
print(counts)

nested = [[1, 2], [3], [4, 5]]
flat = reduce(lambda acc, part: acc + part, nested, [])
print(flat)

settings = [{"theme": "light", "size": 12}, {"size": 14}, {"debug": True}]
merged = reduce(lambda acc, d: {**acc, **d}, settings, {})
print(merged)

def digits_to_number(digits):
    return reduce(lambda acc, d: acc * 10 + d, digits, 0)


print(digits_to_number([4, 7, 2]))

factorial = reduce(lambda a, b: a * b, range(1, 8), 1)
print(factorial, math.prod(range(1, 8)), math.factorial(7))

transactions = [100, -30, 50, -20]
print(reduce(lambda balance, t: balance + t, transactions, 500))

pipeline = [str.strip, str.lower, lambda s: s.replace(" ", "-")]
slug = reduce(lambda value, step: step(value), pipeline, "  Hello Big World ")
print(slug)

total_chars = reduce(lambda acc, w: acc + len(w), words, 0)
print(total_chars, sum(len(w) for w in words))
```

Output:

```text
science
data science with python
{'b': 1, 'a': 3, 'n': 2}
[1, 2, 3, 4, 5]
{'theme': 'light', 'size': 14, 'debug': True}
472
5040 5040 5040
600
hello-big-world
21 21
```

Line by line:

- The longest word is found by keeping the longer of the running winner and the next word (`>=` keeps the earlier one in a tie).
- Joining words with spaces works, but `" ".join(words)` is simpler and faster for strings.
- Counting letters builds a dictionary step by step: the initial value `{}` is the accumulator, and each step returns a new dictionary with one count updated. (A `for` loop or `collections.Counter` is clearer.)
- Flattening and merging use an empty list and an empty dictionary as the starting values.
- `digits_to_number` shows how a sequence of digits becomes a number: multiply the running result by 10 and add the next digit.
- The factorial agrees with `math.prod` and `math.factorial`, the built-in ways to do it.
- A *pipeline* applies a list of functions one after another to one starting value, with `reduce` threading the value through them.
- The last line shows `reduce` with a built-in alternative that is clearer (`sum` over a generator expression).

**7. Example 3 — Edge case or common mistake**

```python
from functools import reduce

try:
    reduce(lambda a, b: a + b, [])
except TypeError as error:
    print("TypeError:", error)
print(reduce(lambda a, b: a + b, [], 0))
```

Output:

```text
TypeError: reduce() of empty iterable with no initial value
0
```

An empty list with no initial value is an error. Provide an initial value whenever the input might be empty.

The function must take two arguments and return the new accumulator:

```python
from functools import reduce

def no_return(acc, x):
    acc + x


print(reduce(no_return, [5], 0))
try:
    reduce(no_return, [1, 2, 3], 0)
except TypeError as error:
    print("TypeError:", error)

try:
    reduce(lambda x: x, [1, 2, 3])
except TypeError as error:
    print("TypeError:", error)
```

Output:

```text
None
TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
TypeError: <lambda>() takes 1 positional argument but 2 were given
```

`no_return` forgets `return`, so the accumulator becomes `None` after the first step: a single item gives `None`, and with more items the next step tries `None + 2` and fails. A one-parameter function fails because `reduce` always passes two.

Order matters when the operation is not commutative or associative:

```python
from functools import reduce

print(reduce(lambda a, b: a - b, [10, 3, 2]))
print(reduce(lambda a, b: b - a, [10, 3, 2]))
print(reduce(lambda a, b: a / b, [100, 5, 2]))
```

Output:

```text
5
9
10.0
```

`reduce` goes from left to right: `(10 - 3) - 2 = 5`. Swapping the roles of the accumulator and the item gives a different answer.

A wrong initial value corrupts the result:

```python
from functools import reduce

print(reduce(lambda a, b: a * b, [2, 3, 4], 0))
print(reduce(lambda a, b: a * b, [2, 3, 4], 1))
print(reduce(lambda a, b: a + b, [[1], [2]], [99]))
```

Output:

```text
0
24
[99, 1, 2]
```

A product starting from 0 is always 0. Choose the "do-nothing" value for the operation: 0 for addition, 1 for multiplication, an empty list for list-joining.

Finally, `reduce` can be slower and harder to read than the alternatives:

```python
from functools import reduce

words = ["a", "b", "c"]
print(reduce(lambda acc, w: acc + w, words, ""))
print("".join(words))

values = [3, 8, 1]
print(reduce(lambda a, b: a if a > b else b, values), max(values))
```

Output:

```text
abc
abc
8 8
```

Use the built-in when there is one.

**8. Common mistakes**

- Forgetting `from functools import reduce` (`NameError`).
- Using an empty iterable with no initial value.
- A function that takes one argument, or that forgets to `return`.
- Choosing the wrong initial value (0 for a product, for example).
- Swapping the accumulator and item in a non-commutative operation (subtraction, division).
- Using `reduce` where `sum`, `max`, `min`, `join` or a simple loop is clearer.
- Building long strings or lists with repeated `+` inside `reduce` on large data (it copies each time).

**9. Real-world and AI applications**

The pattern "fold a collection into one value" appears when merging configuration dictionaries, combining the scores of several models, accumulating a loss over a batch, and chaining processing steps. In large-scale data processing, *map* and *reduce* are the two stages of the well-known "map-reduce" approach: transform every piece of data independently and in parallel, then combine the partial results. Counting words across a huge set of files, for example, is a map (count words in each file) followed by a reduce (add the counts).

**10. Practice**

1. Use `reduce` to compute the sum and the product of `[2, 4, 6]`.
2. Find the largest number in a list with `reduce`, and then with `max`.
3. Join `["a", "b", "c"]` into `"a-b-c"` with `reduce`, and then with `"-".join`.
4. Compute `5!` using `reduce` with an initial value of 1 and `range(1, 6)`.
5. Use `reduce` to merge `[{"a": 1}, {"b": 2}, {"a": 3}]` into one dictionary. What happens to the key `"a"`?
6. Use `reduce` with an initial value to count how many items in `[3, 8, 5, 12]` are greater than 4 (the accumulator is the count).
7. Explain why `reduce(lambda a, b: a + b, [])` raises an error and how to fix it.
8. Combine all three: sum of the squares of the odd numbers in `range(1, 10)` using `map`, `filter` and `reduce`, then compare with a comprehension and `sum`.

**11. Interview questions**

- *What does `reduce` do?* Combines the items of an iterable into one value by repeatedly applying a two-argument function to the accumulated result and the next item.
- *Where is `reduce` found?* In the `functools` module.
- *What does the initial value do?* It is the starting accumulator; it is also the result for an empty iterable.
- *When would you not use `reduce`?* When `sum`, `max`, `min`, `any`, `all`, `join` or a loop expresses the intent more clearly.
- *What is the relationship between `map`, `filter` and `reduce`?* `map` transforms, `filter` selects, `reduce` combines; together they make a data pipeline.

**12. Quick revision**

- `from functools import reduce`; `reduce(function, items, initial)`.
- The function takes `(accumulator, item)` and returns the new accumulator.
- Left to right: `f(f(f(a, b), c), d)`.
- Give an initial value when the input may be empty; pick the neutral value.
- Prefer built-ins (`sum`, `max`, `join`) or a loop when clearer.

---

## Answers to Practice Exercises

### Answers: The map() Function

1.

```python
print(list(map(lambda n: n * 2, [3, 6, 9])))
```

Output:

```text
[6, 12, 18]
```

2.

```python
print(list(map(float, ["1.5", "2.5", "4"])))
```

Output:

```text
[1.5, 2.5, 4.0]
```

3.

```python
sentence = "maps are lazy iterators"
print(list(map(len, sentence.split())))
```

Output:

```text
[4, 3, 4, 9]
```

4.

```python
print(list(map(lambda a, b: a + b, [1, 2, 3], [10, 20, 30])))
```

Output:

```text
[11, 22, 33]
```

5.

```python
print([x ** 2 for x in range(5)])
```

Output:

```text
[0, 1, 4, 9, 16]
```

6. `map` returns a lazy map object. Printing it shows the object and not its values; convert it with `list` first.

```python
print(list(map(str, [1, 2])))
print(type(map(str, [1, 2])).__name__)
```

Output:

```text
['1', '2']
map
```

7.

```python
numbers = list(map(int, "3 4 5".split()))
product = 1
for n in numbers:
    product *= n
print(numbers, product)
```

Output:

```text
[3, 4, 5] 60
```

### Answers: The filter() Function

1.

```python
print(list(filter(lambda n: n % 5 == 0, [4, 9, 15, 22, 31, 40])))
```

Output:

```text
[15, 40]
```

2.

```python
words = ["tea", "coffee", "milk", "juice", "ok"]
print(list(filter(lambda w: len(w) >= 5, words)))
```

Output:

```text
['coffee', 'juice']
```

3. The string `"  "` is not empty, so it is truthy and is kept. Strip the strings first to remove it.

```python
data = ["a", "", None, "b", "  "]
print(list(filter(None, data)))
print(list(filter(None, (item.strip() if item else item for item in data))))
```

Output:

```text
['a', 'b', '  ']
['a', 'b']
```

4.

```python
students = [("Asha", 62), ("Ravi", 48), ("Meena", 91)]
print(list(filter(lambda s: s[1] >= 60, students)))
```

Output:

```text
[('Asha', 62), ('Meena', 91)]
```

5.

```python
odds = filter(lambda n: n % 2 == 1, range(1, 10))
print(list(map(lambda n: n * n, odds)))
```

Output:

```text
[1, 9, 25, 49, 81]
```

6.

```python
def is_palindrome(word):
    return word == word[::-1]


print(list(filter(is_palindrome, ["level", "tea", "noon", "code"])))
```

Output:

```text
['level', 'noon']
```

7. `filter` keeps the items that pass the test, so the result holds the numbers themselves; `map` replaces each item by the result of the function, so you get a list of `True`/`False` values.

```python
nums = [3, 7, 10, 2]
print(list(filter(lambda n: n > 5, nums)))
print(list(map(lambda n: n > 5, nums)))
```

Output:

```text
[7, 10]
[False, True, True, False]
```

### Answers: The reduce() Function

1.

```python
from functools import reduce

print(reduce(lambda a, b: a + b, [2, 4, 6]), reduce(lambda a, b: a * b, [2, 4, 6]))
```

Output:

```text
12 48
```

2.

```python
from functools import reduce

values = [14, 3, 27, 9]
print(reduce(lambda a, b: a if a > b else b, values), max(values))
```

Output:

```text
27 27
```

3.

```python
from functools import reduce

letters = ["a", "b", "c"]
print(reduce(lambda acc, x: acc + "-" + x, letters))
print("-".join(letters))
```

Output:

```text
a-b-c
a-b-c
```

4.

```python
from functools import reduce

print(reduce(lambda a, b: a * b, range(1, 6), 1))
```

Output:

```text
120
```

5. Later dictionaries overwrite earlier values for the same key, so `"a"` ends up as 3.

```python
from functools import reduce

dicts = [{"a": 1}, {"b": 2}, {"a": 3}]
print(reduce(lambda acc, d: {**acc, **d}, dicts, {}))
```

Output:

```text
{'a': 3, 'b': 2}
```

6.

```python
from functools import reduce

items = [3, 8, 5, 12]
print(reduce(lambda count, n: count + (1 if n > 4 else 0), items, 0))
```

Output:

```text
3
```

7. With no items and no initial value, `reduce` has nothing to start from. Supply an initial value:

```python
from functools import reduce

try:
    reduce(lambda a, b: a + b, [])
except TypeError as error:
    print("TypeError:", error)
print(reduce(lambda a, b: a + b, [], 0))
```

Output:

```text
TypeError: reduce() of empty iterable with no initial value
0
```

8.

```python
from functools import reduce

odds = filter(lambda n: n % 2 == 1, range(1, 10))
squares = map(lambda n: n * n, odds)
print(reduce(lambda a, b: a + b, squares, 0))
print(sum(n * n for n in range(1, 10) if n % 2 == 1))
```

Output:

```text
165
165
```

Both give 165. The comprehension version is shorter and easier to read.

---

## Chapter Summary and Key Takeaways

- `map(f, items)` applies `f` to every item, `filter(test, items)` keeps the items whose test result is truthy, and `reduce(f, items, initial)` (from `functools`) folds all items into one value with a two-argument function.
- `map` and `filter` return lazy, single-use iterators; wrap them in `list(...)` to see the values.
- `filter(None, items)` removes falsy values (including legitimate zeros); the test function of `filter` takes one argument and must return a value.
- `reduce` goes from left to right; give an initial value for empty inputs and choose the neutral value for the operation (0 for sums, 1 for products).
- List comprehensions and built-ins (`sum`, `max`, `join`, `math.prod`) often express the same idea more clearly, so use `map`, `filter` and `reduce` when they make the code simpler, not as a habit.

Next: [Chapter 30 — Python Wrap-Up and Introduction to the AI Section](30-python-wrap-up-and-ai-intro.md) wraps up the Python material and opens Part 6, the AI section.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
