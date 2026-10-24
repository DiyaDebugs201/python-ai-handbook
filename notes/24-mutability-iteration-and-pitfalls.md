# Chapter 24 — Mutability, Iteration and Common Data-Structure Pitfalls

> Part 4 — Python Data Structures · Supplementary chapter (not a separate video topic) · Previous: [23 Dictionaries](23-dictionaries.md) · Next: [25 Defining Functions and Return Values](25-defining-functions-and-return-values.md)

**In this chapter:** a consolidating chapter for Part 4. It explains which objects can change and which cannot, how to loop over collections safely, the bugs that catch most beginners (shared references, mutable defaults, accidental aliasing), and how to choose between a list, tuple, set and dictionary.

**Before you start:** you need all of Part 4: [Lists](18-lists-fundamentals.md), [List Methods and Copying](19-list-functions-methods-and-copying.md), [List Comprehension](20-list-comprehension.md), [Tuples](21-tuples.md), [Sets](22-sets.md) and [Dictionaries](23-dictionaries.md). Recap: lists, sets and dictionaries can be changed in place; tuples, strings and numbers cannot; `b = a` makes a second name, not a copy. Examples were run with Python 3.13.

This chapter is supplementary: the video topic list does not name it, but it ties the previous six chapters together and prepares you for functions in Part 5.

---

## Mutable versus Immutable Objects

**Timestamp:** supplementary section (not a separate video topic; it belongs with [Tuples](21-tuples.md#tuples) and [Lists](18-lists-fundamentals.md)).

**Learning objectives:**

- Classify built-in types as mutable or immutable.
- Explain "variables are names, not boxes" and what `id()` and `is` show.
- Predict what happens when a mutable object is shared by two names or passed to a function.

**1. Intuition**

A whiteboard is mutable: you can rub out a word and write another, and everyone looking at the board sees the change. A printed page is immutable: to "change" it you print a new page. A variable is a name tag attached to an object; two tags on one whiteboard see the same writing.

**2. Why does it exist?**

Immutable objects are safe to share (nobody can change them behind your back) and can be used as dictionary keys. Mutable objects are efficient for collections that grow and change, because they are updated in place instead of being rebuilt each time. Python offers both, and you must know which one you hold.

**3. Technical explanation**

- *Immutable:* `int`, `float`, `bool`, `str`, `tuple` (of immutables), `frozenset`, `bytes`, `None`.
- *Mutable:* `list`, `dict`, `set`, and most user-defined objects.
- Assignment binds a name to an object; it never copies. `id(x)` gives an identity number; `a is b` is true when both names refer to the same object.
- "Changing" an immutable value, such as `s = s + "!"` or `n += 1`, creates a *new* object and rebinds the name; the old object is untouched.
- Changing a mutable object in place (`items.append(3)`) keeps the same identity.
- Passing an argument to a function binds the parameter name to the same object. A function that changes a mutable argument in place changes the caller's object; rebinding the parameter to a new object does not.

**4. Syntax**

```text
id(x)          # identity number of the object
a is b         # same object?
a == b         # equal contents?
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
n = 5
m = n
n += 1
print(n, m)

s = "cat"
t = s
s += "s"
print(s, t)

items = [1, 2]
other = items
items.append(3)
print(items, other, items is other)

before = id(items)
items.append(4)
print(id(items) == before)

x = 10
before = id(x)
x += 1
print(id(x) == before)
```

Output:

```text
6 5
cats cat
[1, 2, 3] [1, 2, 3] True
True
False
```

Line by line: after `n += 1` the number 5 still exists under the name `m`; `n` now names a new object, 6. The same holds for strings. The list, in contrast, is changed in place, so both names see the change and its identity does not change. The integer got a new identity when it was "changed".

**6. Example 2 — Practical**

```python
def add_item(basket, item):
    basket.append(item)

def add_item_new(basket, item):
    return basket + [item]

def reset(basket):
    basket = []
    return basket

def shout(text):
    text = text.upper()
    return text

cart = ["tea"]
add_item(cart, "milk")
print(cart)
new_cart = add_item_new(cart, "rice")
print(cart, new_cart)
reset(cart)
print(cart)

word = "hello"
shout(word)
print(word)
print(shout(word))

for kind, value in [("int", 1), ("str", "a"), ("tuple", (1, 2)), ("list", [1]),
                    ("dict", {"a": 1}), ("set", {1})]:
    try:
        hash(value)
        print(kind, "is hashable")
    except TypeError:
        print(kind, "is not hashable")
```

Output:

```text
['tea', 'milk']
['tea', 'milk'] ['tea', 'milk', 'rice']
['tea', 'milk']
hello
HELLO
int is hashable
str is hashable
tuple is hashable
list is not hashable
dict is not hashable
set is not hashable
```

Line by line: `add_item` changes the caller's list in place; `add_item_new` builds a new list and leaves the argument alone; `reset` only rebinds its own local name `basket` to a new list, so the caller's list is untouched. Strings cannot be changed in place, so `shout(word)` has no effect on `word` unless the result is used. The last loop shows that immutable types are hashable and mutable types are not.

**7. Example 3 — Edge case or common mistake**

```python
t = ([1, 2], "x")
t[0].append(3)
print(t)

a = [1, 2]
b = [a, a]
b[0].append(99)
print(b)

c = "abc"
try:
    c[0] = "X"
except TypeError as error:
    print("TypeError:", error)
c = "X" + c[1:]
print(c)

small1, small2 = 256, 256
print(small1 is small2, small1 == small2)
```

Output:

```text
([1, 2, 3], 'x')
[[1, 2, 99], [1, 2, 99]]
TypeError: 'str' object does not support item assignment
Xbc
True True
```

A tuple's own slots are fixed, but a list stored in it may change. `b = [a, a]` holds the same list twice, so one change shows in both. Strings are rebuilt, not edited. Do not use `is` for comparing numbers or strings: whether equal small values happen to be the same object is an implementation detail (see [Identity Operators](13-identity-operators-and-precedence.md#identity-operators-is-versus-equality)).

**8. Common mistakes**

- Thinking `b = a` copies a mutable object.
- Expecting a function to change a string or number passed to it.
- Expecting `basket = []` inside a function to empty the caller's list.
- Using `is` where `==` is meant.
- Assuming a tuple is deeply unchangeable.

**9. Real-world and AI applications**

Shared mutable state is a major source of bugs in data pipelines: a cleaning function that edits its input in place silently damages the raw data, and a configuration dictionary shared between experiments can leak settings from one run into the next. Immutable values (tuples, strings) are used for keys, identifiers and fixed settings because they cannot change unexpectedly.

**10. Practice**

1. Which of these are mutable: `"text"`, `[1]`, `(1, 2)`, `{1}`, `3.5`, `{"a": 1}`?
2. Predict and check: `a = [1]; b = a; b += [2]; print(a)`.
3. Predict and check: `a = "go"; b = a; b += "!"; print(a, b)`.
4. Write a function `add_tax(prices)` that returns a new list and leaves the argument unchanged.
5. Explain why a function that does `numbers = sorted(numbers)` on its parameter does not sort the caller's list, while `numbers.sort()` does.

**11. Interview questions**

- *Which built-in types are immutable?* int, float, bool, str, tuple, frozenset, bytes, None.
- *What does it mean that Python passes objects by assignment?* The parameter becomes another name for the same object, so in-place changes are visible to the caller, and rebinding is not.
- *Why can't a list be a dictionary key?* It is mutable and therefore unhashable.

**12. Quick revision**

- Names refer to objects; assignment never copies.
- Immutable: numbers, strings, tuples, frozensets. Mutable: lists, dicts, sets.
- In-place changes affect every name for the object; rebinding affects only one name.
- Use `==` for contents, `is` for identity.

---

## Iterating Safely

**Timestamp:** supplementary section (not a separate video topic; it belongs with [List Comprehension](20-list-comprehension.md#list-comprehension)).

**Learning objectives:**

- Loop over lists, dictionaries and sets without skipping items or raising errors.
- Choose between filtering with a comprehension and removing in place.
- Use `enumerate`, `zip`, `sorted` and `reversed` for common loop shapes.

**1. Intuition**

Imagine counting people in a queue while some of them leave: if the line shifts as you count, you skip someone. Looping over a collection that is being changed has the same problem, so you either count a snapshot or build a new line.

**2. Why does it exist?**

Programs often need to remove or update items while processing them. Python's iterators walk by position or by internal table, and changing the size mid-walk causes skipped items (lists) or errors (dictionaries and sets). Knowing the safe patterns avoids the most common loop bug.

**3. Technical explanation**

- Do not add or remove items of a list while iterating over that same list: later items shift and are skipped.
- Dictionaries and sets raise `RuntimeError` if their size changes during iteration. Changing the *value* of an existing key is allowed.
- Safe patterns: (a) build a new collection with a comprehension; (b) loop over a copy (`list(d)`, `items[:]`, `set(s)`); (c) collect the keys to change, then change them after the loop; (d) loop over indices backwards when deleting from a list by position.
- `enumerate` gives position and item; `zip` walks several sequences together; `reversed` walks backwards; `sorted` walks a sorted copy without changing the original.
- Dictionary iteration order is the insertion order; set order is arbitrary.

**4. Syntax**

```text
[x for x in items if keep(x)]
for x in items[:]: ...
for key in list(d): ...
for i, x in enumerate(items): ...
for a, b in zip(first, second): ...
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
numbers = [1, 2, 3, 4, 5, 6]
evens = [n for n in numbers if n % 2 == 0]
print(evens, numbers)

for n in numbers[:]:
    if n % 2 == 0:
        numbers.remove(n)
print(numbers)

values = [10, 20, 30]
for i, value in enumerate(values):
    values[i] = value + 1
print(values)

for a, b in zip("abc", [1, 2]):
    print(a, b)

for item in reversed([1, 2, 3]):
    print(item, end=" ")
print()
```

Output:

```text
[2, 4, 6] [1, 2, 3, 4, 5, 6]
[1, 3, 5]
[11, 21, 31]
a 1
b 2
3 2 1 
```

Line by line: the comprehension keeps the evens without touching the original; the second loop walks over a copy while removing from the original; `enumerate` lets us replace items by position (changing a value, not the size, is safe); `zip` stops at the shorter input; `reversed` walks backwards.

**6. Example 2 — Practical**

```python
scores = {"asha": 82, "ravi": 45, "meena": 91, "kiran": 38}

passed = {name: mark for name, mark in scores.items() if mark >= 50}
print(passed)

for name in list(scores):
    if scores[name] < 50:
        del scores[name]
print(scores)

for name in scores:
    scores[name] += 5
print(scores)

tags = {"python", "ai", "data", "ml"}
long_tags = {t for t in tags if len(t) > 2}
print(sorted(long_tags))

items = ["a", "b", "c", "d", "e"]
for i in range(len(items) - 1, -1, -1):
    if i % 2 == 1:
        del items[i]
print(items)

matrix = [[1, 2], [3, 4]]
for row in matrix:
    for j in range(len(row)):
        row[j] *= 10
print(matrix)

first, second = [1, 2, 3], [10, 20, 30]
print([a + b for a, b in zip(first, second)])
print(sorted(scores, key=scores.get, reverse=True))
```

Output:

```text
{'asha': 82, 'meena': 91}
{'asha': 82, 'meena': 91}
{'asha': 87, 'meena': 96}
['data', 'python']
['a', 'c', 'e']
[[10, 20], [30, 40]]
[11, 22, 33]
['meena', 'asha']
```

Line by line: the first filter builds a new dictionary; the second loops over `list(scores)`, a snapshot of the keys, so deleting is safe; the third changes values (not size), which is allowed. Deleting by index from the *end* means earlier positions do not shift. Nested loops can change inner list items in place. `zip` adds two lists element by element; `sorted(scores, key=scores.get, reverse=True)` ranks names by score.

**7. Example 3 — Edge case or common mistake**

```python
numbers = [2, 4, 6, 8]
for n in numbers:
    if n % 2 == 0:
        numbers.remove(n)
print(numbers)

scores = {"a": 1, "b": 2}
try:
    for key in scores:
        scores[key + "x"] = 0
except RuntimeError as error:
    print("RuntimeError:", error)

letters = ["a", "b", "c"]
for letter in letters:
    letters.append(letter.upper())
    if len(letters) > 6:
        break
print(letters)

it = iter([1, 2, 3])
print(list(it), list(it))
```

Output:

```text
[4, 8]
RuntimeError: dictionary changed size during iteration
['a', 'b', 'c', 'A', 'B', 'C', 'A']
[1, 2, 3] []
```

Removing from the list during the loop skipped every other item, leaving `[4, 8]`. Adding keys during dictionary iteration raises an error. Appending to a list while looping over it makes the loop run on the growing list, so without the `break` it would never end. An iterator can be used only once: the second `list(it)` is empty.

**8. Common mistakes**

- Removing items from a list while looping over it.
- Adding or deleting dictionary or set entries during iteration.
- Appending to a list while iterating over it.
- Reusing an exhausted iterator or generator.
- Depending on set order.

**9. Real-world and AI applications**

Cleaning a dataset means removing bad records; the safe patterns are the standard way to do it. Filtering a list of messages to fit a model's context window, dropping empty documents before embedding them, and removing finished jobs from a queue all use "build a new list" or "loop over a copy".

**10. Practice**

1. Remove all negative numbers from `[3, -1, 4, -5, 9]` in two safe ways.
2. Delete all entries with an empty string value from `{"a": "x", "b": "", "c": "z", "d": ""}`.
3. Print each item of a list with its position, starting at 1.
4. Why does `for x in items: items.append(x)` run forever?
5. Show that an iterator is exhausted after one pass.

**11. Interview questions**

- *Why is it dangerous to modify a list while iterating over it?* The list shifts under the loop, so items are skipped.
- *What error do you get when a dictionary changes size during iteration?* `RuntimeError`.
- *Name two safe patterns for removing items.* A comprehension that builds a new collection, or looping over a copy.

**12. Quick revision**

- Never change the size of a collection while looping over it.
- Build a new collection, or loop over a copy.
- `enumerate`, `zip`, `reversed`, `sorted` for common loop shapes.
- Iterators are single-use.

---

## Common Data-Structure Pitfalls

**Timestamp:** supplementary section (not a separate video topic; it belongs with [Dictionaries](23-dictionaries.md#dictionaries)).

**Learning objectives:**

- Recognise and fix the mutable default argument bug.
- Avoid shared inner lists in grids and `dict.fromkeys` mistakes.
- Avoid misreading `sort()`, `append()` and similar methods that return `None`.

**1. Intuition**

Some bugs repeat because they come from the same trap: two things look separate but share one object, or a method quietly returns nothing. Learning the short list of traps saves hours.

**2. Why does it exist?**

These behaviours are consequences of the rules in the previous chapters: assignment shares, defaults are created once, in-place methods return `None`. They are not bugs in Python, but they surprise people who expect "copy" semantics.

**3. Technical explanation**

- *Mutable default argument.* A default value in a function definition is created once, when the function is defined, and then reused in every call. A default of `[]` therefore collects items across calls. The fix is `def f(items=None):` and `if items is None: items = []` (functions are covered in [Defining Your Own Function](25-defining-functions-and-return-values.md#defining-your-own-function) and [Default Arguments](26-function-arguments.md#default-arguments)).
- *Shared inner lists.* `[[0] * 3] * 3` repeats one inner list; `dict.fromkeys(keys, [])` shares one list.
- *`None` returns.* `append`, `extend`, `sort`, `reverse`, `insert`, `remove`, `clear`, `update` all return `None`.
- *Shallow copies.* `copy()`, `[:]` and `list()` copy only the outer container.
- *Float keys and equality.* `1`, `1.0`, `True` are the same key; floats may not compare equal after arithmetic.
- *Unpacking size.* The count of names must match, unless `*` is used.

**4. Syntax**

```text
def function(items=None):
    if items is None:
        items = []
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
def add_bad(x, bucket=[]):
    bucket.append(x)
    return bucket

print(add_bad(1))
print(add_bad(2))

def add_good(x, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(x)
    return bucket

print(add_good(1))
print(add_good(2))
```

Output:

```text
[1]
[1, 2]
[1]
[2]
```

Line by line: the default list of `add_bad` is created once, so the second call sees the first call's item. `add_good` creates a fresh list each time, because `None` is immutable and a new list is made inside the function.

**6. Example 2 — Practical**

```python
grid_bad = [[0] * 3] * 2
grid_bad[0][0] = 1
print(grid_bad)
grid_good = [[0] * 3 for _ in range(2)]
grid_good[0][0] = 1
print(grid_good)

numbers = [3, 1, 2]
result = numbers.append(4)
print(result)
result = sorted(numbers)
print(result)

stats = {"a": 0.1 + 0.2}
print(stats["a"] == 0.3, abs(stats["a"] - 0.3) < 1e-9)

counts = {}
for word in "a b a".split():
    if word in counts:
        counts[word] += 1
    else:
        counts[word] = 1
print(counts)

original = {"user": "asha", "roles": ["admin"]}
shallow = dict(original)
shallow["roles"].append("editor")
print(original["roles"])
```

Output:

```text
[[1, 0, 0], [1, 0, 0]]
[[1, 0, 0], [0, 0, 0]]
None
[1, 2, 3, 4]
False True
{'a': 2, 'b': 1}
['admin', 'editor']
```

Line by line: the first grid has two rows that are one list; the second has two separate lists. `append` returns `None` while `sorted` returns a list. Float arithmetic is not exact, so compare with a tolerance. The counting pattern with `if word in counts` avoids a `KeyError`. A shallow copy of a dictionary shares its inner list.

**7. Example 3 — Edge case or common mistake**

```python
def log(message, history=[]):
    history.append(message)
    return len(history)

print(log("a"), log("b"), log("c"))
print(log.__defaults__)

a, b = [1, 2, 3][:2]
print(a, b)
try:
    x, y, z = [1, 2]
except ValueError as error:
    print("ValueError:", error)

values = [1, 2, 3]
values = values.reverse()
print(values)

d = {1: "int", 1.0: "float"}
print(d, len(d))
```

Output:

```text
1 2 3
(['a', 'b', 'c'],)
1 2
ValueError: not enough values to unpack (expected 3, got 2)
None
{1: 'float'} 1
```

The history list lives in the function's `__defaults__` and keeps growing: the counts 1, 2, 3 show the shared state. Assigning the result of `reverse()` stores `None`. The keys `1` and `1.0` are the same key, so the dictionary has one entry whose value was replaced and whose key is the first one seen.

**8. Common mistakes**

- Using `[]`, `{}` or `set()` as a default argument value.
- Building grids with `*`.
- Assigning the result of an in-place method.
- Comparing floats with `==`.
- Trusting a shallow copy of nested data.

**9. Real-world and AI applications**

The mutable default bug is a classic in code that keeps a "history" or "cache" parameter, for example a chat function with `messages=[]`, where different users' conversations would mix. Shared inner lists corrupt feature tables, and shallow copies of configuration dictionaries cause one experiment's change to appear in another.

**10. Practice**

1. Fix `def collect(item, seen=set()): seen.add(item); return seen`.
2. Create a 4 x 4 grid of zeros where changing `grid[1][1]` changes one cell.
3. What is `x` after `x = [3, 1].sort()`? Fix it two ways.
4. Make an independent copy of `{"a": [1], "b": [2]}` so that appending to the copy's list does not change the original.
5. Check `0.1 + 0.2 == 0.3` and rewrite the comparison safely with `math.isclose`.

**11. Interview questions**

- *What is the mutable default argument problem?* A mutable default is created once and shared by all calls that rely on it.
- *How do you fix it?* Use `None` as the default and create the object inside the function.
- *Why is `[[0]*3]*3` wrong for a grid?* All rows are the same list.

**12. Quick revision**

- Defaults are created once: use `None`.
- Build grids with a comprehension.
- In-place methods return `None`.
- Use `deepcopy` for nested data.
- Compare floats with a tolerance.

---

## Choosing the Right Data Structure

**Timestamp:** supplementary section (not a separate video topic; it belongs with [Sets and Set Operations](22-sets.md)).

**Learning objectives:**

- Choose between list, tuple, set and dictionary for a given job.
- Combine structures (list of dictionaries, dictionary of lists) for records.
- Know the cost differences between searching a list and a set or dictionary.

**1. Intuition**

Picking a container is like picking a storage box: a shelf for ordered items (list), a sealed envelope for a fixed group (tuple), a bag for distinct things where only "is it in there?" matters (set), and a labelled filing cabinet for lookup by name (dictionary).

**2. Why does it exist?**

Each structure makes some tasks easy and others awkward. The right choice makes code shorter, clearer and faster; the wrong one forces extra loops and conversions.

**3. Technical explanation**

| Need | Use | Why |
|---|---|---|
| Ordered items, may repeat, will change | list | indexing, append, sort |
| Fixed group of related values | tuple | immutable, hashable, unpacking |
| Unique items, fast membership, set algebra | set | hashing, union and intersection |
| Look up by a label | dict | key to value, fast |
| Many records with fields | list of dicts | readable, JSON-like |
| Group items by category | dict of lists | `defaultdict(list)` |
| Count occurrences | dict or `Counter` | `counts[x] += 1` |

Costs: `x in a_list` scans (time grows with length); `x in a_set` and `key in a_dict` take about the same time for any size. Appending to a list end is fast; inserting at the front is slow.

**4. Syntax**

```text
records = [{"name": "Asha", "score": 82}, {"name": "Ravi", "score": 67}]
by_city = {"Chennai": ["Asha"], "Pune": ["Ravi"]}
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
students = [
    {"name": "Asha", "city": "Chennai", "score": 82},
    {"name": "Ravi", "city": "Pune", "score": 67},
    {"name": "Meena", "city": "Chennai", "score": 91},
]

print([s["name"] for s in students if s["score"] >= 80])
print(sum(s["score"] for s in students) / len(students))

by_city = {}
for s in students:
    by_city.setdefault(s["city"], []).append(s["name"])
print(by_city)

print({s["name"]: s["score"] for s in students})
print(set(s["city"] for s in students) == {"Chennai", "Pune"})
```

Output:

```text
['Asha', 'Meena']
80.0
{'Chennai': ['Asha', 'Meena'], 'Pune': ['Ravi']}
{'Asha': 82, 'Ravi': 67, 'Meena': 91}
True
```

Line by line: a list of dictionaries is the standard record table; comprehensions filter and extract fields; a dictionary of lists groups names by city; a dictionary comprehension builds a lookup by name; a set gives the distinct cities.

**6. Example 2 — Practical**

```python
import time

n = 20000
data_list = list(range(n))
data_set = set(data_list)
queries = list(range(n - 200, n + 200))

start = time.perf_counter()
hits_list = sum(1 for q in queries if q in data_list)
t_list = time.perf_counter() - start

start = time.perf_counter()
hits_set = sum(1 for q in queries if q in data_set)
t_set = time.perf_counter() - start

print(hits_list == hits_set, hits_list)
print("set faster than list:", t_set < t_list)

point = (3, 4)
distance = (point[0] ** 2 + point[1] ** 2) ** 0.5
print(distance)

seen = {}
route = [(0, 0), (1, 0), (1, 0), (2, 1)]
for position in route:
    seen[position] = seen.get(position, 0) + 1
print(seen)

queue = ["a", "b", "c"]
print(queue.pop(0), queue)
```

Output:

```text
True 200
set faster than list: True
5.0
{(0, 0): 1, (1, 0): 2, (2, 1): 1}
a ['b', 'c']
```

Line by line: the same lookups are done on a list and on a set and the results agree, while the set answers faster (the exact times vary by computer, so only the comparison is printed). A tuple holds a fixed point and works as a dictionary key to count visits. A list used as a queue works for small data; for large queues use `collections.deque`.

**7. Example 3 — Edge case or common mistake**

```python
words = ["b", "a", "b", "c"]
print(list(set(words)) == words)
print(sorted(set(words)))

print(list(dict.fromkeys(words)))

pairs = [("a", 1), ("b", 2), ("a", 3)]
print(dict(pairs))

grouped = {}
for key, value in pairs:
    grouped.setdefault(key, []).append(value)
print(grouped)
```

Output:

```text
False
['a', 'b', 'c']
['b', 'a', 'c']
{'a': 3, 'b': 2}
{'a': [1, 3], 'b': [2]}
```

A set loses order and repeats. `dict(pairs)` silently keeps only the last value for a repeated key (`"a"` ends with 3), so group the values when keys can repeat.

**8. Common mistakes**

- Using a list for membership tests on large data.
- Using a set when order or duplicates matter.
- Using parallel lists (`names`, `scores`) when a list of dictionaries is clearer.
- Using `dict(pairs)` when keys repeat.
- Using a dictionary when the data is just an ordered sequence.

**9. Real-world and AI applications**

Datasets are lists of dictionaries (one per example), vocabularies are dictionaries from token to number, stop-word lists and seen-ID collections are sets, shapes and coordinates are tuples, and batches are lists. Choosing a set or dictionary for lookups instead of repeated list scans is the first optimisation to try when a data-cleaning script is slow.

**10. Practice**

1. Which structure would you use for: (a) the unique tags of a blog post, (b) latitude and longitude, (c) a shopping cart in order, (d) a phone book?
2. Given a list of `{"name", "dept"}` dictionaries, build a dictionary mapping each department to a list of names.
3. Convert two parallel lists of names and scores into a list of dictionaries.
4. Explain why `if word in stop_words` is better with a set than with a list for a large text.
5. Count the distinct words in a sentence, ignoring case.

**11. Interview questions**

- *When would you choose a set over a list?* For uniqueness and fast membership tests, when order does not matter.
- *When would you choose a tuple over a list?* For a fixed group of values, or when a hashable value is needed.
- *How would you represent a table of records in Python?* A list of dictionaries (or a list of tuples).

**12. Quick revision**

- List: ordered, changeable. Tuple: fixed. Set: unique, fast `in`. Dict: key to value.
- Records: list of dicts. Groups: dict of lists.
- Prefer sets and dicts for lookups on large data.

---

## Answers to Practice Exercises

### Answers: Mutable versus Immutable Objects

1. Mutable: `[1]`, `{1}`, `{"a": 1}`. Immutable: `"text"`, `(1, 2)`, `3.5`.

2.

```python
a = [1]
b = a
b += [2]
print(a)
```

Output:

```text
[1, 2]
```

3.

```python
a = "go"
b = a
b += "!"
print(a, b)
```

Output:

```text
go go!
```

4.

```python
def add_tax(prices):
    return [round(price * 1.18, 2) for price in prices]


original = [100, 200]
print(add_tax(original), original)
```

Output:

```text
[118.0, 236.0] [100, 200]
```

5. `sorted(numbers)` creates a new list, and assigning it to the parameter only rebinds the local name. `numbers.sort()` changes the object that both the caller and the function share.

```python
def sort_rebind(numbers):
    numbers = sorted(numbers)

def sort_inplace(numbers):
    numbers.sort()

data = [3, 1, 2]
sort_rebind(data)
print(data)
sort_inplace(data)
print(data)
```

Output:

```text
[3, 1, 2]
[1, 2, 3]
```

### Answers: Iterating Safely

1.

```python
numbers = [3, -1, 4, -5, 9]
print([n for n in numbers if n >= 0])

copy_list = numbers[:]
for n in copy_list:
    if n < 0:
        numbers.remove(n)
print(numbers)
```

Output:

```text
[3, 4, 9]
[3, 4, 9]
```

2.

```python
data = {"a": "x", "b": "", "c": "z", "d": ""}
for key in list(data):
    if data[key] == "":
        del data[key]
print(data)
```

Output:

```text
{'a': 'x', 'c': 'z'}
```

3.

```python
for position, item in enumerate(["tea", "milk", "rice"], start=1):
    print(position, item)
```

Output:

```text
1 tea
2 milk
3 rice
```

4. Each round appends one item, so the list the loop is walking keeps growing, and there is always a next item. (Shown with a safety limit:)

```python
items = [1, 2]
rounds = 0
for x in items:
    items.append(x)
    rounds += 1
    if rounds == 5:
        break
print(items)
```

Output:

```text
[1, 2, 1, 2, 1, 2, 1]
```

5.

```python
it = iter([1, 2, 3])
print(list(it))
print(list(it))
```

Output:

```text
[1, 2, 3]
[]
```

### Answers: Common Data-Structure Pitfalls

1.

```python
def collect(item, seen=None):
    if seen is None:
        seen = set()
    seen.add(item)
    return seen


print(collect(1), collect(2))
```

Output:

```text
{1} {2}
```

2.

```python
grid = [[0] * 4 for _ in range(4)]
grid[1][1] = 7
print(grid)
```

Output:

```text
[[0, 0, 0, 0], [0, 7, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
```

3. `x` is `None`, because `sort()` returns `None`. Fixes:

```python
x = [3, 1]
x.sort()
print(x)

y = sorted([3, 1])
print(y)
```

Output:

```text
[1, 3]
[1, 3]
```

4.

```python
import copy

original = {"a": [1], "b": [2]}
independent = copy.deepcopy(original)
independent["a"].append(99)
print(original, independent)
```

Output:

```text
{'a': [1], 'b': [2]} {'a': [1, 99], 'b': [2]}
```

5.

```python
import math

print(0.1 + 0.2 == 0.3, math.isclose(0.1 + 0.2, 0.3))
```

Output:

```text
False True
```

### Answers: Choosing the Right Data Structure

1. (a) a set, (b) a tuple, (c) a list, (d) a dictionary.

2.

```python
staff = [{"name": "Asha", "dept": "IT"}, {"name": "Ravi", "dept": "HR"}, {"name": "Meena", "dept": "IT"}]
by_dept = {}
for person in staff:
    by_dept.setdefault(person["dept"], []).append(person["name"])
print(by_dept)
```

Output:

```text
{'IT': ['Asha', 'Meena'], 'HR': ['Ravi']}
```

3.

```python
names = ["Asha", "Ravi"]
scores = [82, 67]
print([{"name": n, "score": s} for n, s in zip(names, scores)])
```

Output:

```text
[{'name': 'Asha', 'score': 82}, {'name': 'Ravi', 'score': 67}]
```

4. Looking up a word in a list scans the list item by item, so the time grows with the list length for every word of the text. A set finds the word through its hash in about the same time however large the set is. (See the timing comparison in this chapter.)

5.

```python
sentence = "The cat and the Hat and THE bat"
print(len({word.lower() for word in sentence.split()}))
```

Output:

```text
5
```

---

## Chapter Summary and Key Takeaways

- Numbers, strings and tuples are immutable; lists, dictionaries and sets are mutable. Assignment binds names and never copies, so changes to a mutable object show through every name.
- Never change the size of a collection while looping over it: build a new collection or loop over a copy.
- Mutable default arguments, `[[0] * n] * m`, `dict.fromkeys(keys, [])`, shallow copies of nested data, and assigning the result of in-place methods are the classic pitfalls.
- Pick the structure by the job: list for ordered changeable items, tuple for fixed groups, set for unique items and fast membership, dictionary for lookup by key, and a list of dictionaries for records.

Next: [Chapter 25 — Defining Functions and Return Values](25-defining-functions-and-return-values.md) begins Part 5.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
