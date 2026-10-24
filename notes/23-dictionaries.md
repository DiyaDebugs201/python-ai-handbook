# Chapter 23 — Dictionaries

> Part 4 — Python Data Structures · Video: 7:48:58–8:19:30 · Previous: [22 Sets](22-sets.md) · Next: [24 Mutability, Iteration and Common Pitfalls](24-mutability-iteration-and-pitfalls.md)

**In this chapter:** the dictionary, a collection that maps *keys* to *values*; how to create, read, add, change and delete entries; safe lookups with `get`; looping over keys, values and pairs; the main dictionary methods; merging, copying and nesting dictionaries; and dictionary comprehensions.

**Before you start:** you need lists from [Lists in Python](18-lists-fundamentals.md#lists-in-python), tuples from [Tuples](21-tuples.md#tuples) (for unpacking pairs), sets and hashability from [Sets](22-sets.md#sets), and `for` loops from [The for Loop](17-for-loop-range-and-nested-loops.md#the-for-loop). Recap: a value is *hashable* if it cannot change, which allows it to be used where Python needs to look something up quickly (set elements, and now dictionary keys). Examples were run with Python 3.13.

---

## Dictionaries

**Timestamp:** [7:48:58](https://www.youtube.com/watch?v=J9BI0jGOds8&t=28138s)

**Learning objectives:**

- Explain what a dictionary stores and why lookups by key are fast.
- Create dictionaries, and read, add, change and delete entries.
- Explain the rules for keys and what values can be.
- Loop over a dictionary and use nested dictionaries.

**1. Intuition**

A dictionary is a phone book or a contact list: you look up a *name* (the key) and get the *number* (the value). You do not scan every page, and it does not matter at which position the entry sits. A shop's price list, a student's record, the settings of an app: each is a set of labels with attached values.

**2. Why does it exist?**

A list finds things by position, but real data is usually found by *meaning*: the price of "tea", the email of "Asha". Remembering that the price of tea is at index 7 is awkward and fragile. A dictionary lets the code say `prices["tea"]`. Internally it uses hashing, like a set, so looking up a key takes about the same time for ten entries or ten million.

**3. Technical explanation**

- *Creating.* `{"name": "Asha", "age": 21}`, `dict(name="Asha", age=21)`, `dict([("a", 1), ("b", 2)])`, or `{}` for an empty one. Each entry is a `key: value` pair, separated by commas.
- *Keys* must be unique and hashable: strings, numbers, tuples of hashable items. Lists, dictionaries and sets cannot be keys. If a key is repeated, the last value wins.
- *Values* can be anything, including lists and other dictionaries.
- *Order.* Since Python 3.7 a dictionary remembers the order in which keys were first inserted. It is still looked up by key, not by position.
- *Reading.* `d[key]` raises `KeyError` if the key is missing. `d.get(key)` returns `None` instead, and `d.get(key, default)` returns the default. `key in d` tests for a *key* (not a value).
- *Adding and changing.* `d[key] = value` creates the entry if the key is new, or replaces the value if it exists.
- *Deleting.* `del d[key]` or `d.pop(key)`.
- *Looping.* `for key in d` gives the keys. `d.keys()`, `d.values()` and `d.items()` give live views of the keys, the values and the `(key, value)` pairs.
- *Size.* `len(d)` is the number of entries.
- *Mutable.* Dictionaries can be changed in place, and `b = a` shares one dictionary (see [Copying Lists](19-list-functions-methods-and-copying.md#copying-lists) for the same idea).

**4. Syntax**

```text
d = {"key1": value1, "key2": value2}
d["key1"]                 # read, KeyError if missing
d.get("key3", default)    # safe read
d["key3"] = value3        # add or change
del d["key1"]             # delete
"key2" in d               # membership of keys
for key in d: ...
for key, value in d.items(): ...
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
student = {"name": "Asha", "age": 21, "city": "Chennai"}
print(student)
print(student["name"], student["age"])
print(len(student), type(student).__name__)

student["age"] = 22
student["course"] = "Data Science"
print(student)

del student["city"]
print(student)

print("name" in student, "Asha" in student)
print(student.get("phone"), student.get("phone", "not given"))

for key in student:
    print(key, "->", student[key])

empty = {}
print(len(empty), empty)
print(dict(a=1, b=2), dict([("x", 10), ("y", 20)]))
```

Output:

```text
{'name': 'Asha', 'age': 21, 'city': 'Chennai'}
Asha 21
3 dict
{'name': 'Asha', 'age': 22, 'city': 'Chennai', 'course': 'Data Science'}
{'name': 'Asha', 'age': 22, 'course': 'Data Science'}
True False
None not given
name -> Asha
age -> 22
course -> Data Science
0 {}
{'a': 1, 'b': 2} {'x': 10, 'y': 20}
```

Line by line:

- Square brackets with a key read a value. Assigning to a new key adds an entry; assigning to an existing key replaces its value (here the age changes from 21 to 22).
- `del` removes an entry. `in` looks at keys only, so `"Asha"` (a value) is not found.
- `get` returns `None` or the default you supply, instead of an error, when the key is missing.
- Looping directly over a dictionary gives its keys, in insertion order. `dict(...)` can also build one from keyword arguments or from a list of pairs.

**6. Example 2 — Practical**

```python
prices = {"tea": 20, "coffee": 35, "milk": 25}
order = ["tea", "milk", "tea", "biscuit"]

total = 0
for item in order:
    price = prices.get(item)
    if price is None:
        print("unknown item:", item)
        continue
    total += price
print("total:", total)

text = "the cat and the dog and the bird"
counts = {}
for word in text.split():
    counts[word] = counts.get(word, 0) + 1
print(counts)

by_length = {}
for word in text.split():
    by_length.setdefault(len(word), []).append(word)
print(by_length)

settings = {"theme": "dark", "font": {"name": "Mono", "size": 12}, "tags": ["a", "b"]}
print(settings["font"]["size"], settings["tags"][1])
settings["font"]["size"] = 14
print(settings)

students = {
    "asha": {"age": 21, "marks": [82, 90]},
    "ravi": {"age": 22, "marks": [67, 71]},
}
for name, info in students.items():
    average = sum(info["marks"]) / len(info["marks"])
    print(f"{name}: age {info['age']}, average {average:.1f}")

point_names = {(0, 0): "origin", (1, 0): "east"}
print(point_names[(1, 0)])
print(sorted(counts.items(), key=lambda pair: pair[1], reverse=True)[:2])
```

Output:

```text
unknown item: biscuit
total: 65
{'the': 3, 'cat': 1, 'and': 2, 'dog': 1, 'bird': 1}
{3: ['the', 'cat', 'and', 'the', 'dog', 'and', 'the'], 4: ['bird']}
12 b
{'theme': 'dark', 'font': {'name': 'Mono', 'size': 14}, 'tags': ['a', 'b']}
asha: age 21, average 86.0
ravi: age 22, average 69.0
east
[('the', 3), ('and', 2)]
```

Line by line:

- The price lookup uses `get` and checks for `None`, so unknown items are reported without crashing the loop.
- The word counter is a classic pattern: `counts.get(word, 0) + 1` means "the old count, or 0 if the word is new, plus one".
- `setdefault(key, default)` returns the value for the key, first inserting the default if the key is missing. Here it creates an empty list for each new length and appends to it, grouping words by length.
- Values can be lists or dictionaries. A chain of brackets goes down one level at a time: `settings["font"]["size"]`.
- A dictionary of dictionaries holds one record per student; `items()` gives the name and the record together. The f-string uses single quotes inside double quotes to avoid a clash (see [String Formatting and f-Strings](09-string-formatting-and-f-strings.md)).
- A tuple works as a key. `sorted(counts.items(), key=...)` sorts the pairs by count to find the most common words.

**7. Example 3 — Edge case or common mistake**

```python
student = {"name": "Asha"}
print(student["age"])
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 2, in <module>
    print(student["age"])
          ~~~~~~~^^^^^^^
KeyError: 'age'
```

`KeyError` means the key is missing. Use `get`, or test with `in` first. Other problems:

```python
for action in [lambda: {[1, 2]: "x"}, lambda: {"a": 1}[0], lambda: dict(5), lambda: {"a": 1}.add("b")]:
    try:
        action()
    except Exception as error:
        print(type(error).__name__ + ":", error)
```

Output:

```text
TypeError: unhashable type: 'list'
KeyError: 0
TypeError: 'int' object is not iterable
AttributeError: 'dict' object has no attribute 'add'
```

Keys must be hashable, a dictionary is not accessed by position, and a dictionary has no `add` method (assign to a new key).

Duplicate keys, and numbers that are equal:

```python
d = {"a": 1, "a": 2, "b": 3}
print(d)

mixed = {1: "int", 1.0: "float", True: "bool"}
print(mixed)

letters = {"x": 1, "y": 2}
print(letters.keys(), list(letters.values()))
```

Output:

```text
{'a': 2, 'b': 3}
{1: 'bool'}
dict_keys(['x', 'y']) [1, 2]
```

A repeated key keeps its original position but the last value. `1`, `1.0` and `True` are the same key (as in a set), so there is only one entry. `keys()` and `values()` return *views*, so convert them with `list()` when you need a list.

Changing the dictionary while looping over it is an error:

```python
scores = {"a": 50, "b": 80, "c": 30}
try:
    for name in scores:
        if scores[name] < 60:
            del scores[name]
except RuntimeError as error:
    print("RuntimeError:", error)

scores = {"a": 50, "b": 80, "c": 30}
for name in list(scores):
    if scores[name] < 60:
        del scores[name]
print(scores)
```

Output:

```text
RuntimeError: dictionary changed size during iteration
{'b': 80}
```

Loop over a copy of the keys (`list(scores)`) if you need to delete during the loop, or build a new dictionary with a comprehension.

**8. Common mistakes**

- Reading a missing key with `[]` and getting `KeyError`.
- Expecting `in` to look at values.
- Using a list or another unhashable object as a key.
- Repeating a key in the literal and losing earlier values.
- Adding or deleting entries while looping over the dictionary.
- Writing `d.add(...)` or `d.append(...)`; use `d[key] = value`.
- Assuming `b = a` makes a separate dictionary.
- Expecting `d[0]` to mean the first entry.

**9. Real-world and AI applications**

Dictionaries are the everyday format for structured data: a record from a database, the settings of a program, a JSON object received from a web service. Almost every AI interface speaks in dictionaries. A chat message is `{"role": "user", "content": "Hello"}`, a request to a model is a dictionary of settings (model name, messages, temperature), and the response comes back as nested dictionaries and lists. Word counts, vocabularies mapping tokens to numbers, and caches of answers are dictionaries too. Configuration values are often stored in environment variables and read into a dictionary (see [Environment Variables, .env Files, and API Keys](30-python-wrap-up-and-ai-intro.md#environment-variables-env-files-and-api-keys)).

**10. Practice**

1. Create a dictionary for a book with the keys `title`, `author` and `year`. Print the title, then change the year.
2. Write code that prints the price of `"coffee"` from a price dictionary, and `"not on the menu"` for an item that is missing.
3. Count how many times each letter appears in `"banana"`.
4. Given `{"a": 1, "b": 2}`, print each key and value on its own line, formatted as `a = 1`.
5. Create a nested dictionary for two students, each with a `marks` list, and print each one's highest mark.
6. Explain why `{[1, 2]: "x"}` fails but `{(1, 2): "x"}` works.
7. Delete every entry whose value is below 50 from `{"a": 20, "b": 70, "c": 45, "d": 90}` without getting a `RuntimeError`.

**11. Interview questions**

- *What is a dictionary?* A mutable collection of key-value pairs, looked up by key, with unique hashable keys and insertion-ordered entries (Python 3.7+).
- *Why are dictionary lookups fast?* The key is hashed, which finds the entry directly instead of scanning.
- *What is the difference between `d[key]` and `d.get(key)`?* `d[key]` raises `KeyError` for a missing key; `get` returns `None` or a default.
- *What can be a dictionary key?* Any hashable (immutable) object: strings, numbers, tuples of hashable items.
- *What happens if you repeat a key in a dictionary literal?* The last value wins.

**12. Quick revision**

- `{key: value}`; keys are unique and hashable, values can be anything.
- `d[key]` reads (`KeyError` if missing); `d.get(key, default)` is safe; `d[key] = v` adds or changes.
- `in` tests keys; `del d[key]` deletes.
- `for k in d`, `.keys()`, `.values()`, `.items()`.
- Do not change the size while looping; use `list(d)` or a comprehension.

---

## Dictionary Operations and Methods

**Timestamp:** [8:02:44](https://www.youtube.com/watch?v=J9BI0jGOds8&t=28964s)

**Learning objectives:**

- Use `keys`, `values`, `items`, `get`, `setdefault`, `update`, `pop`, `popitem`, `clear`, `copy` and `fromkeys`.
- Merge dictionaries with `update` and the `|` operator.
- Build dictionaries with comprehensions, and invert or filter them.
- Make shallow and deep copies, and use `Counter` and `defaultdict` as conveniences.

**1. Intuition**

If the dictionary is a contact list, the methods are the things you do to the whole list: "list all names", "list all numbers", "merge my friend's list into mine", "remove this person and tell me their number", "make a photocopy". Most of them have a plain-language meaning.

**2. Why does it exist?**

The same operations are needed again and again: gather the keys or values, combine two dictionaries (defaults plus overrides), remove an entry and use its value, count things, group things. Methods give each operation a clear name, and a comprehension builds a new dictionary from any iterable in a single line.

**3. Technical explanation**

Methods and operations (for a dictionary `d`):

- `d.keys()`, `d.values()`, `d.items()`: views of the keys, values and pairs. They reflect later changes to `d` and can be looped over, tested with `in`, and converted with `list()`.
- `d.get(k, default)`: safe lookup. `d.setdefault(k, default)`: return `d[k]`, inserting `default` first if the key is missing.
- `d.update(other)`: add all entries of `other` (a dictionary, pairs, or keyword arguments), replacing existing keys. The operators `d | other` (a new merged dictionary) and `d |= other` (in place) do the same since Python 3.9; in a merge the right side wins.
- `d.pop(k)`: remove the key and return its value (`KeyError` if missing, unless a default is given: `d.pop(k, None)`). `d.popitem()`: remove and return the *last inserted* pair. `d.clear()`: remove everything. `del d[k]` also removes one entry.
- `d.copy()`: shallow copy; `copy.deepcopy(d)` for nested data. `dict.fromkeys(keys, value)` makes a dictionary with the same starting value for every key.
- *Dictionary comprehension*: `{key_expr: value_expr for item in iterable if condition}`.
- *Sorting.* Dictionaries are not sorted, but `sorted(d)` gives the keys sorted, and `sorted(d.items(), key=...)` gives sorted pairs.
- Two helpers from the standard library (`collections`): `Counter(iterable)` counts items, and `defaultdict(factory)` creates a missing value automatically when a new key is used.

**4. Syntax**

```text
d.keys()   d.values()   d.items()
d.get(k, default)       d.setdefault(k, default)
d.update(other)         merged = d | other      d |= other
d.pop(k)   d.pop(k, default)   d.popitem()   d.clear()   d.copy()
dict.fromkeys(keys, value)
{k: v for k, v in pairs if condition}
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
stock = {"apple": 10, "banana": 5, "cherry": 0}

print(list(stock.keys()))
print(list(stock.values()))
print(list(stock.items()))

stock.update({"banana": 8, "date": 12})
print(stock)

removed = stock.pop("cherry")
print(removed, stock)
print(stock.pop("fig", "no such item"))

last = stock.popitem()
print(last, stock)

print(stock.setdefault("apple", 99), stock.setdefault("grape", 3))
print(stock)

copy_of_stock = stock.copy()
stock.clear()
print(stock, copy_of_stock)

print(dict.fromkeys(["a", "b", "c"], 0))
```

Output:

```text
['apple', 'banana', 'cherry']
[10, 5, 0]
[('apple', 10), ('banana', 5), ('cherry', 0)]
{'apple': 10, 'banana': 8, 'cherry': 0, 'date': 12}
0 {'apple': 10, 'banana': 8, 'date': 12}
no such item
('date', 12) {'apple': 10, 'banana': 8}
10 3
{'apple': 10, 'banana': 8, 'grape': 3}
{} {'apple': 10, 'banana': 8, 'grape': 3}
{'a': 0, 'b': 0, 'c': 0}
```

Line by line:

- `keys`, `values` and `items` show the three parts of the dictionary; wrapped in `list()` they print like lists. Each item is a tuple.
- `update` adds `date` and replaces the value of `banana`.
- `pop("cherry")` removes the entry and returns its value; with a second argument it returns that default instead of an error when the key is missing.
- `popitem()` removes the last inserted pair.
- `setdefault("apple", 99)` returns the existing value 10 without changing it; `setdefault("grape", 3)` inserts the new entry.
- `copy` makes an independent (shallow) copy, so clearing `stock` does not empty `copy_of_stock`.
- `fromkeys` creates a dictionary with a shared starting value for all keys.

**6. Example 2 — Practical**

```python
from collections import Counter, defaultdict

defaults = {"theme": "light", "font_size": 12, "language": "en"}
user = {"font_size": 16}
settings = defaults | user
print(settings)

squares = {n: n * n for n in range(1, 6)}
print(squares)

prices = {"tea": 20, "coffee": 35, "milk": 25, "juice": 60}
affordable = {item: price for item, price in prices.items() if price <= 30}
print(affordable)
with_tax = {item: round(price * 1.18, 1) for item, price in prices.items()}
print(with_tax)

codes = {"a": 1, "b": 2, "c": 3}
inverted = {value: key for key, value in codes.items()}
print(inverted)

keys = ["name", "age", "city"]
values = ["Asha", 21, "Chennai"]
record = dict(zip(keys, values))
print(record)

sentence = "to be or not to be that is the question"
counter = Counter(sentence.split())
print(counter.most_common(2))
print(counter["be"], counter["missing"])

groups = defaultdict(list)
for word in sentence.split():
    groups[len(word)].append(word)
print(dict(groups))

cheapest = min(prices, key=prices.get)
total_stock = sum({"a": 3, "b": 4}.values())
print(cheapest, total_stock)

for item, price in sorted(prices.items(), key=lambda pair: pair[1], reverse=True):
    print(f"{item:<8}{price:>4}")

print(sorted(prices))
print(max(prices.values()), "tea" in prices.keys(), 35 in prices.values())
```

Output:

```text
{'theme': 'light', 'font_size': 16, 'language': 'en'}
{1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
{'tea': 20, 'milk': 25}
{'tea': 23.6, 'coffee': 41.3, 'milk': 29.5, 'juice': 70.8}
{1: 'a', 2: 'b', 3: 'c'}
{'name': 'Asha', 'age': 21, 'city': 'Chennai'}
[('to', 2), ('be', 2)]
2 0
{2: ['to', 'be', 'or', 'to', 'be', 'is'], 3: ['not', 'the'], 4: ['that'], 8: ['question']}
tea 7
juice     60
coffee    35
milk      25
tea       20
['coffee', 'juice', 'milk', 'tea']
60 True True
```

Line by line:

- `defaults | user` merges two dictionaries into a new one; the value from the right side (`user`) replaces the default for `font_size`. This "defaults plus overrides" pattern is very common.
- Dictionary comprehensions build a dictionary from a range, filter entries by value, transform all values, or swap keys and values (inversion works only when the values are unique and hashable).
- `dict(zip(keys, values))` builds a record from two parallel lists.
- `Counter` counts the words in one step and `most_common(2)` returns the top pairs; a missing item counts as 0, without an error. `defaultdict(list)` creates an empty list the first time a key is used, so no `setdefault` is needed.
- `min(prices, key=prices.get)` finds the key with the smallest value. `sum` over `values()` adds the values.
- Sorting the items by value, and printing a small aligned table with width settings.
- `sorted(prices)` gives the sorted keys. `in` on a dictionary tests keys; `in d.values()` tests values.

**7. Example 3 — Edge case or common mistake**

`dict.fromkeys` with a mutable value shares that value between all keys:

```python
shared = dict.fromkeys(["a", "b"], [])
shared["a"].append(1)
print(shared)

separate = {key: [] for key in ["a", "b"]}
separate["a"].append(1)
print(separate)
```

Output:

```text
{'a': [1], 'b': [1]}
{'a': [1], 'b': []}
```

Every key of `fromkeys` points to the *same* list. Use a comprehension to give each key its own list.

A shallow copy shares the nested objects, as with lists:

```python
import copy

original = {"name": "Asha", "marks": [80, 90]}
shallow = original.copy()
deep = copy.deepcopy(original)
original["marks"].append(100)
original["name"] = "Asha K"
print(shallow)
print(deep)

alias = original
alias["name"] = "changed"
print(original["name"])
```

Output:

```text
{'name': 'Asha', 'marks': [80, 90, 100]}
{'name': 'Asha', 'marks': [80, 90]}
changed
```

The shallow copy shows the new mark (shared list) but not the new name (a replaced string); the deep copy shows neither. `alias = original` is not a copy at all.

Further traps with `update`, `pop` and views:

```python
d = {"a": 1}
print(d.update({"b": 2}))
print(d)

for action in [lambda: d.pop("zzz"), lambda: d.update(5), lambda: {}.popitem()]:
    try:
        action()
    except Exception as error:
        print(type(error).__name__ + ":", error)

view = d.keys()
d["c"] = 3
print(list(view))
```

Output:

```text
None
{'a': 1, 'b': 2}
KeyError: 'zzz'
TypeError: 'int' object is not iterable
KeyError: 'popitem(): dictionary is empty'
['a', 'b', 'c']
```

`update` changes the dictionary and returns `None`. `popitem` on an empty dictionary is a `KeyError`. A view reflects later changes: after `d["c"] = 3`, the earlier `view` includes `c`.

**8. Common mistakes**

- Using `dict.fromkeys(keys, [])` and sharing one list.
- Treating `d.copy()` as a deep copy.
- Writing `d = d.update(...)` (it returns `None`).
- Expecting `in d.values()` to be as fast as `in d` (values are scanned one by one).
- Expecting `d | other` to change `d` (it makes a new dictionary; use `|=` or `update`).
- Inverting a dictionary with duplicate values and losing entries.
- Using `popitem()` and expecting the first item (it removes the last inserted).
- Forgetting that `pop(k)` without a default raises `KeyError` for a missing key.

**9. Real-world and AI applications**

The merge pattern (`defaults | overrides`) is used to combine default model settings with a user's choices. Dictionary comprehensions clean and reshape records, and `Counter` is the quick way to compute word frequencies, the first step in many text-analysis jobs and in building a vocabulary of tokens. Inverting a vocabulary dictionary gives the lookup from number back to token. JSON data from a web service is parsed into dictionaries and lists, and walking it with `get` and nested keys is a daily task when working with AI services. A `defaultdict(list)` is handy for grouping examples by label.

**10. Practice**

1. Merge `{"a": 1, "b": 2}` and `{"b": 20, "c": 30}` in two ways and compare the results.
2. Build a dictionary of the cubes of 1 to 5 with a comprehension.
3. From `{"x": 5, "y": 15, "z": 10}`, create a new dictionary keeping only the entries with a value above 8.
4. Invert `{"one": 1, "two": 2, "three": 3}`.
5. Use `Counter` to find the most common letter in `"mississippi"`.
6. Use `setdefault` (or `defaultdict`) to group the words `["ant", "bee", "ape", "bat", "cow"]` by their first letter.
7. Explain why `dict.fromkeys(["a", "b"], [])` can cause a bug, and write a safe version.
8. Remove the key `"b"` from a dictionary and print the removed value, using a method that does not fail when the key is missing.

**11. Interview questions**

- *What do `keys()`, `values()` and `items()` return?* Live view objects of the keys, values, and `(key, value)` tuples.
- *How do you merge two dictionaries?* `a | b` (Python 3.9+) or `a.update(b)`; the right-hand values win.
- *What is the difference between `pop` and `popitem`?* `pop(k)` removes the given key and returns its value; `popitem()` removes and returns the last inserted pair.
- *What does `setdefault` do?* Returns the value for a key, inserting the given default first if the key is absent.
- *Is `d.copy()` a deep copy?* No, it is shallow; nested mutable values are shared.
- *What is `defaultdict`?* A dictionary that creates a default value automatically when a missing key is accessed.

**12. Quick revision**

- `keys()`, `values()`, `items()` are views; `list()` them to see the items.
- `update` / `|` merge (right side wins); `|=` merges in place.
- `pop(k, default)`, `popitem()`, `clear()`, `del d[k]` remove entries.
- `setdefault` inserts if missing; `get` never inserts.
- Comprehension: `{k: v for ... if ...}`; `Counter` counts; `defaultdict` groups.
- `copy()` is shallow; `fromkeys` shares the value.

---

## Answers to Practice Exercises

### Answers: Dictionaries

1.

```python
book = {"title": "Learning Python", "author": "A. Writer", "year": 2020}
print(book["title"])
book["year"] = 2024
print(book)
```

Output:

```text
Learning Python
{'title': 'Learning Python', 'author': 'A. Writer', 'year': 2024}
```

2.

```python
menu = {"tea": 20, "coffee": 35}
item = "coffee"
print(menu.get(item, "not on the menu"))
item = "pizza"
print(menu.get(item, "not on the menu"))
```

Output:

```text
35
not on the menu
```

3.

```python
counts = {}
for letter in "banana":
    counts[letter] = counts.get(letter, 0) + 1
print(counts)
```

Output:

```text
{'b': 1, 'a': 3, 'n': 2}
```

4.

```python
data = {"a": 1, "b": 2}
for key, value in data.items():
    print(f"{key} = {value}")
```

Output:

```text
a = 1
b = 2
```

5.

```python
students = {
    "asha": {"marks": [82, 90, 77]},
    "ravi": {"marks": [67, 71, 95]},
}
for name, info in students.items():
    print(name, max(info["marks"]))
```

Output:

```text
asha 90
ravi 95
```

6. Keys must be hashable, which means they cannot change. A list can be changed, so it is not hashable; a tuple of numbers cannot be changed, so it is.

```python
print({(1, 2): "x"})
try:
    {[1, 2]: "x"}
except TypeError as error:
    print("TypeError:", error)
```

Output:

```text
{(1, 2): 'x'}
TypeError: unhashable type: 'list'
```

7.

```python
scores = {"a": 20, "b": 70, "c": 45, "d": 90}
for key in list(scores):
    if scores[key] < 50:
        del scores[key]
print(scores)

scores = {"a": 20, "b": 70, "c": 45, "d": 90}
print({key: value for key, value in scores.items() if value >= 50})
```

Output:

```text
{'b': 70, 'd': 90}
{'b': 70, 'd': 90}
```

### Answers: Dictionary Operations and Methods

1.

```python
first = {"a": 1, "b": 2}
second = {"b": 20, "c": 30}
print(first | second)

merged = first.copy()
merged.update(second)
print(merged)
```

Output:

```text
{'a': 1, 'b': 20, 'c': 30}
{'a': 1, 'b': 20, 'c': 30}
```

Both give `b: 20`, because the right-hand dictionary wins.

2.

```python
print({n: n ** 3 for n in range(1, 6)})
```

Output:

```text
{1: 1, 2: 8, 3: 27, 4: 64, 5: 125}
```

3.

```python
values = {"x": 5, "y": 15, "z": 10}
print({key: value for key, value in values.items() if value > 8})
```

Output:

```text
{'y': 15, 'z': 10}
```

4.

```python
words = {"one": 1, "two": 2, "three": 3}
print({number: word for word, number in words.items()})
```

Output:

```text
{1: 'one', 2: 'two', 3: 'three'}
```

5.

```python
from collections import Counter

print(Counter("mississippi").most_common(1))
print(Counter("mississippi").most_common())
```

Output:

```text
[('i', 4)]
[('i', 4), ('s', 4), ('p', 2), ('m', 1)]
```

Both `i` and `s` appear four times. `Counter` lists equal counts in the order the items were first seen, so `i` comes first.

6.

```python
words = ["ant", "bee", "ape", "bat", "cow"]
groups = {}
for word in words:
    groups.setdefault(word[0], []).append(word)
print(groups)

from collections import defaultdict

grouped = defaultdict(list)
for word in words:
    grouped[word[0]].append(word)
print(dict(grouped))
```

Output:

```text
{'a': ['ant', 'ape'], 'b': ['bee', 'bat'], 'c': ['cow']}
{'a': ['ant', 'ape'], 'b': ['bee', 'bat'], 'c': ['cow']}
```

7. All keys share one list object, so appending to one key's list changes every key's list. A comprehension creates a separate list for each key:

```python
bad = dict.fromkeys(["a", "b"], [])
bad["a"].append(1)
print(bad)

good = {key: [] for key in ["a", "b"]}
good["a"].append(1)
print(good)
```

Output:

```text
{'a': [1], 'b': [1]}
{'a': [1], 'b': []}
```

8.

```python
data = {"a": 1, "b": 2, "c": 3}
print(data.pop("b", None))
print(data.pop("b", None))
print(data)
```

Output:

```text
2
None
{'a': 1, 'c': 3}
```

The second `pop` finds nothing and returns the default `None` instead of raising `KeyError`.

---

## Chapter Summary and Key Takeaways

- A dictionary maps unique, hashable keys to values of any kind; since Python 3.7 it keeps insertion order, and lookup by key is fast.
- `d[key]` raises `KeyError` for a missing key, while `d.get(key, default)` does not; `in` tests keys; assigning to a key adds or changes an entry; `del` and `pop` remove entries.
- Loop with `for key in d`, `d.values()` or `d.items()`, and never change the size of a dictionary while looping over it.
- Merge with `a | b` or `update` (the right side wins), build with comprehensions, count with `Counter`, group with `setdefault` or `defaultdict`.
- `copy()` is shallow and `dict.fromkeys(keys, [])` shares one list; use `copy.deepcopy` and comprehensions when each entry needs its own mutable object.

Next: [Chapter 24 — Mutability, Iteration and Common Pitfalls](24-mutability-iteration-and-pitfalls.md) pulls the data-structure ideas together.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
