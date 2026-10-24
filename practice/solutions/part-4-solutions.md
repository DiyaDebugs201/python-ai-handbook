# Part 4 — Solutions: Python Data Structures

> [Practice index](../README.md) · [Problems for this part](../part-4-exercises.md)

Every program below was run with Python 3.13 and the output shown is the real output. Your own solution may differ and still be correct: compare behaviour, not wording.

## P4.1 — List operations

Start with `items = ["b", "d"]`. Append `"e"`, insert `"a"` at the front, insert `"c"` at index 3, remove `"e"`, pop the last item (print it) and print the list after each change.

```python
items = ["b", "d"]
items.append("e")
print(items)
items.insert(0, "a")
print(items)
items.insert(3, "c")
print(items)
items.remove("e")
print(items)
print(items.pop())
print(items)
```

Output:

```text
['b', 'd', 'e']
['a', 'b', 'd', 'e']
['a', 'b', 'd', 'c', 'e']
['a', 'b', 'd', 'c']
c
['a', 'b', 'd']
```

`insert(i, x)` shifts later items right; `pop()` removes and returns the last item.

## P4.2 — Alias versus copy

Create `a = [1, 2, 3]`, `b = a`, `c = a.copy()`. Append 4 to `a` and print all three lists. Then show a nested list `m = [[1], [2]]` where a shallow copy still shares the inner lists.

```python
import copy

a = [1, 2, 3]
b = a
c = a.copy()
a.append(4)
print(a, b, c)

m = [[1], [2]]
shallow = m.copy()
deep = copy.deepcopy(m)
m[0].append(99)
print(shallow, deep)
```

Output:

```text
[1, 2, 3, 4] [1, 2, 3, 4] [1, 2, 3]
[[1, 99], [2]] [[1], [2]]
```

`b` is the same list as `a`; `c` is a new list. A shallow copy copies only the outer list, so inner lists are shared; `deepcopy` copies everything.

## P4.3 — Comprehension

Build the list of squares of the even numbers from 1 to 10, and a list of the words in `"the quick brown fox"` that have more than 3 letters, in upper case.

```python
squares = [n ** 2 for n in range(1, 11) if n % 2 == 0]
long_words = [w.upper() for w in "the quick brown fox".split() if len(w) > 3]
print(squares)
print(long_words)
```

Output:

```text
[4, 16, 36, 64, 100]
['QUICK', 'BROWN']
```

The `if` at the end filters; the expression at the front transforms each kept item.

## P4.4 — Tuple unpacking

Given `point = (3, 4)` unpack it into `x` and `y`. Then write a function returning `(min, max)` of a list and unpack its result. Finally unpack `first, *middle, last = [1, 2, 3, 4, 5]`.

```python
point = (3, 4)
x, y = point
print(x, y)


def low_high(values):
    return min(values), max(values)


low, high = low_high([7, 2, 9])
print(low, high)

first, *middle, last = [1, 2, 3, 4, 5]
print(first, middle, last)
```

Output:

```text
3 4
2 9
1 [2, 3, 4] 5
```

A function can return a tuple, which the caller unpacks; `*middle` takes whatever is left between the first and last.

## P4.5 — Set operations

With `a = {1, 2, 3, 4}` and `b = {3, 4, 5}` print the union, intersection, difference `a - b`, symmetric difference, and whether `{1, 2}` is a subset of `a`. Use `sorted` for stable output.

```python
a = {1, 2, 3, 4}
b = {3, 4, 5}
print(sorted(a | b))
print(sorted(a & b))
print(sorted(a - b))
print(sorted(a ^ b))
print({1, 2} <= a)
```

Output:

```text
[1, 2, 3, 4, 5]
[3, 4]
[1, 2]
[1, 2, 5]
True
```

Set operators mirror mathematics; printing sorted lists avoids relying on set order.

## P4.6 — Word frequency

Count how often each word occurs in `"to be or not to be that is the question to be"` and print the words by count (highest first, ties alphabetical).

```python
text = "to be or not to be that is the question to be"
counts = {}
for word in text.split():
    counts[word] = counts.get(word, 0) + 1
for word, n in sorted(counts.items(), key=lambda pair: (-pair[1], pair[0])):
    print(word, n)
```

Output:

```text
be 3
to 3
is 1
not 1
or 1
question 1
that 1
the 1
```

`counts.get(word, 0) + 1` handles a first sighting; the sort key puts larger counts first and breaks ties alphabetically.

## P4.7 — Invert a dictionary

Invert `{"a": 1, "b": 2, "c": 1}` so that each value maps to a list of keys.

```python
original = {"a": 1, "b": 2, "c": 1}
inverted = {}
for key, value in original.items():
    inverted.setdefault(value, []).append(key)
print(inverted)
```

Output:

```text
{1: ['a', 'c'], 2: ['b']}
```

Values can repeat, so each inverted key needs a list; `setdefault` creates it on first use.

## P4.8 — Remove duplicates, keep order

Remove duplicates from `[3, 1, 3, 2, 1, 4]` keeping the first occurrence of each.

```python
items = [3, 1, 3, 2, 1, 4]
seen = set()
unique = []
for item in items:
    if item not in seen:
        seen.add(item)
        unique.append(item)
print(unique)
print(list(dict.fromkeys(items)))
```

Output:

```text
[3, 1, 2, 4]
[3, 1, 2, 4]
```

A set gives fast membership checks; dictionaries keep insertion order, so `dict.fromkeys` is a one-line alternative.

## P4.9 — Transpose a matrix

Transpose `[[1, 2, 3], [4, 5, 6]]` (rows become columns) using `zip` and then using a nested comprehension.

```python
matrix = [[1, 2, 3], [4, 5, 6]]
print([list(col) for col in zip(*matrix)])
print([[row[i] for row in matrix] for i in range(len(matrix[0]))])
```

Output:

```text
[[1, 4], [2, 5], [3, 6]]
[[1, 4], [2, 5], [3, 6]]
```

`*matrix` passes each row to `zip`, which pairs up the entries column by column.

## P4.10 — Remove while iterating, safely

Remove all negative numbers from `[4, -1, -2, 7, -3, 8]` correctly. First show what goes wrong when you remove inside a `for` loop over the same list.

```python
data = [4, -1, -2, 7, -3, 8]
buggy = data.copy()
for n in buggy:
    if n < 0:
        buggy.remove(n)
print("buggy:", buggy)

fixed = [n for n in data if n >= 0]
print("fixed:", fixed)
```

Output:

```text
buggy: [4, -2, 7, 8]
fixed: [4, 7, 8]
```

Removing items shifts the later ones left, so the loop skips the element after each removal (`-2` survives). Building a new list avoids the problem.

## P4.11 — Group words by first letter

Group `["apple", "avocado", "banana", "blueberry", "cherry"]` into a dictionary from first letter to a list of words.

```python
from collections import defaultdict

words = ["apple", "avocado", "banana", "blueberry", "cherry"]
groups = defaultdict(list)
for word in words:
    groups[word[0]].append(word)
print(dict(groups))
```

Output:

```text
{'a': ['apple', 'avocado'], 'b': ['banana', 'blueberry'], 'c': ['cherry']}
```

`defaultdict(list)` creates an empty list the first time a key is used.

---

Back to the [problems](../part-4-exercises.md) or the [practice index](../README.md).
