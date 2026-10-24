# Chapter 19 — List Functions, Methods and Copying

> Part 4 — Python Data Structures · Video: 6:01:49–6:33:38 · Previous: [18 Data Structures Introduction and Lists](18-lists-fundamentals.md) · Next: [20 List Comprehension](20-list-comprehension.md)

**In this chapter:** the built-in functions that work on whole lists (`len`, `sum`, `min`, `max`, `sorted`, `reversed`, `any`, `all`), the methods that belong to lists (`append`, `insert`, `extend`, `remove`, `pop`, `sort`, and more), and the difference between two names for one list, a shallow copy and a deep copy.

**Before you start:** you need the basics of lists from [Lists in Python](18-lists-fundamentals.md#lists-in-python) and [List Operations](18-lists-fundamentals.md#list-operations) (creating, indexing, slicing, `+`, `*`, `in`), loops from [The for Loop](17-for-loop-range-and-nested-loops.md#the-for-loop), and the idea of a method from [Built-in Functions](03-builtin-functions-print-and-modules.md). Recap: a list is an ordered, changeable collection written in square brackets; a method is a function attached to an object and called with a dot, such as `text.upper()`. Examples were run with Python 3.13.

---

## Built-in List Functions

**Timestamp:** [6:01:49](https://www.youtube.com/watch?v=J9BI0jGOds8&t=21709s)

**Learning objectives:**

- Use `len`, `sum`, `min`, `max`, `sorted`, `reversed`, `any`, `all` and `list()` on lists.
- Explain the difference between `sorted(x)` and `x.sort()`.
- Use `key=` and `reverse=` to control sorting and comparisons.

**1. Intuition**

Built-in functions are tools in the shared toolbox: you hand them a list and get an answer back, and the list itself is not touched. Asking "how many items?", "what is the biggest?" or "show me a sorted copy" does not rearrange the original, just as counting the books on a shelf does not move them.

**2. Why does it exist?**

Counting, adding up, finding extremes, ordering and testing "is any/every item such-and-such?" are needed in nearly every program. Writing a loop for each of them would be repetitive and error-prone. Built-in functions are tested, fast (they run in compiled code), and work on many kinds of collection, not only lists.

**3. Technical explanation**

A built-in function is called as `function(list)`. The most useful ones for lists:

- `len(x)`: number of items.
- `sum(x)`: total of a list of numbers (`sum(x, start)` begins from `start`). It does not join strings.
- `min(x)`, `max(x)`: smallest and largest. They need items that can be compared with each other (numbers with numbers, strings with strings), and raise `ValueError` on an empty list unless you give `default=`.
- `sorted(x)`: a *new* list in ascending order; `reverse=True` for descending; `key=function` to sort by a computed value, such as `key=len`.
- `reversed(x)`: an iterator that walks the list backwards; wrap it in `list()` to see the items.
- `any(x)`: `True` if at least one item is truthy. `all(x)`: `True` if every item is truthy (and `True` for an empty list).
- `list(x)`: make a list from any iterable (a string, a range, a tuple).
- `enumerate`, `zip` and `range` were introduced in [The for Loop](17-for-loop-range-and-nested-loops.md#the-for-loop).

None of these changes the original list. Sorting strings uses character codes (see [Strings Revisited: ord() and chr()](10-ord-chr-and-string-methods.md#strings-revisited-ord-and-chr)), so uppercase letters sort before lowercase ones unless you use `key=str.lower`.

**4. Syntax**

```text
len(items)            sum(items)            sum(items, start)
min(items)            max(items)            min(items, key=function)
sorted(items)         sorted(items, key=function, reverse=True)
list(reversed(items)) any(items)            all(items)
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
marks = [72, 85, 60, 91, 78]
print(len(marks))
print(sum(marks))
print(min(marks), max(marks))
print(sum(marks) / len(marks))
print(sorted(marks))
print(sorted(marks, reverse=True))
print(list(reversed(marks)))
print(marks)
```

Output:

```text
5
386
60 91
77.2
[60, 72, 78, 85, 91]
[91, 85, 78, 72, 60]
[78, 91, 60, 85, 72]
[72, 85, 60, 91, 78]
```

Line by line:

- `len`, `sum`, `min` and `max` give the size, total and extremes. The average is `sum / len`.
- `sorted` and `reversed` give ordered or backwards views. The last line shows that `marks` itself is unchanged, in the original order.

**6. Example 2 — Practical**

```python
words = ["banana", "apple", "Cherry", "fig", "date"]
print(sorted(words))
print(sorted(words, key=str.lower))
print(sorted(words, key=len))
print(max(words, key=len), min(words, key=len))

scores = {"Asha": 82, "Ravi": 67, "Meena": 91}
best = max(scores, key=scores.get)
print("top student:", best, scores[best])

flags = [True, False, True]
print(any(flags), all(flags))
print(any([]), all([]))

ages = [19, 22, 31, 17]
print("all adults:", all(age >= 18 for age in ages))
print("any minor:", any(age < 18 for age in ages))

print(sum([0.1] * 10), sum([[1], [2]], []))
print(list("hello"), list(range(3)), list((1, 2)))
print(min([], default="empty"))
```

Output:

```text
['Cherry', 'apple', 'banana', 'date', 'fig']
['apple', 'banana', 'Cherry', 'date', 'fig']
['fig', 'date', 'apple', 'banana', 'Cherry']
banana fig
top student: Meena 91
True False
False True
all adults: False
any minor: True
1.0 [1, 2]
['h', 'e', 'l', 'l', 'o'] [0, 1, 2] [1, 2]
empty
```

Line by line:

- Plain `sorted(words)` puts `Cherry` first, because uppercase `C` has a smaller character code than any lowercase letter. `key=str.lower` compares the lower-case versions, and `key=len` sorts by length.
- `max(words, key=len)` returns the longest word; ties go to the first one found.
- `max(scores, key=scores.get)` goes through the dictionary keys and picks the one with the highest score (see [Dictionaries](23-dictionaries.md#dictionaries)).
- `any` and `all` with a generator expression (`age >= 18 for age in ages`) test a condition on every item without building a new list. `any([])` is `False` and `all([])` is `True`.
- `sum([0.1] * 10)` gives exactly `1.0` in Python 3.12 and later, because `sum` now compensates for float rounding when adding floats (a plain loop with `+=` still gives `0.9999999999999999`, as in [The while Loop](16-while-loop-and-loop-control.md#the-while-loop)). `sum` can also concatenate lists if you give it `[]` as the start value, though that is slow for big data.
- `min([], default="empty")` avoids an error for an empty list.

**7. Example 3 — Edge case or common mistake**

```python
print(max([]))
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 1, in <module>
    print(max([]))
          ~~~^^^^
ValueError: max() iterable argument is empty
```

Mixing types, and trying to sum strings, also fail:

```python
for action in [lambda: max([3, "a"]), lambda: sum(["a", "b"]), lambda: sorted([3, "a", 1])]:
    try:
        action()
    except TypeError as error:
        print("TypeError:", error)
```

Output:

```text
TypeError: '>' not supported between instances of 'str' and 'int'
TypeError: unsupported operand type(s) for +: 'int' and 'str'
TypeError: '<' not supported between instances of 'str' and 'int'
```

A subtler mistake is `sorted` versus `sort`:

```python
numbers = [3, 1, 2]
result = numbers.sort()
print(result, numbers)

numbers = [3, 1, 2]
result = sorted(numbers)
print(result, numbers)
```

Output:

```text
None [1, 2, 3]
[1, 2, 3] [3, 1, 2]
```

`list.sort()` changes the list and returns `None`, so `x = x.sort()` throws the list away. `sorted()` returns a new list and leaves the original alone.

**8. Common mistakes**

- Writing `numbers = numbers.sort()` and ending up with `None`.
- Calling `max` or `min` on an empty list (use `default=`) or on mixed types.
- Using `sum` on a list of strings (use `"".join(...)` instead).
- Expecting uppercase and lowercase strings to sort together alphabetically.
- Printing `reversed(x)` and expecting a list; it is an iterator object.
- Forgetting that `all([])` is `True`.

**9. Real-world and AI applications**

These functions summarise data: totals and averages of scores, the longest or shortest document, the highest-probability option (`max(options, key=...)`), and top-k selections with `sorted(..., reverse=True)[:k]`. In model evaluation, `all(...)` and `any(...)` check conditions such as "does every test case pass?". A language model's next-word choice is, at its simplest, picking the item with the largest score from a list of scores, which is exactly what `max` with a `key` does.

**10. Practice**

1. For `[14, 3, 27, 9, 21]`, print the length, sum, minimum, maximum and average.
2. Sort `["pear", "Fig", "apple", "banana"]` ignoring case, and again by length.
3. Print the three highest numbers of `[40, 15, 99, 62, 7, 84]` using `sorted`.
4. Check if every word in `["tea", "cup", "pot"]` has exactly three letters.
5. Explain why `numbers = numbers.sort()` is a bug.
6. Find the key with the smallest value in `{"a": 5, "b": 2, "c": 9}`.

**11. Interview questions**

- *What is the difference between `sorted(x)` and `x.sort()`?* `sorted` returns a new list and leaves `x` unchanged; `sort` sorts in place and returns `None`.
- *What does `key=` do?* It is a function applied to each item to produce the value that is compared.
- *What is `all([])`?* `True`, because no item fails the test.
- *Can `sum` add strings?* No; use `"".join(list_of_strings)`.

**12. Quick revision**

- `len`, `sum`, `min`, `max` summarise; `sorted`, `reversed` give ordered views; `any`, `all` test.
- None of them change the original list.
- `sorted(x, key=..., reverse=True)`; `.sort()` changes in place and returns `None`.
- Empty list: `min`/`max` raise `ValueError` unless `default=` is given.
- Items must be comparable (no numbers mixed with strings).

---

## List Methods

**Timestamp:** [6:14:35](https://www.youtube.com/watch?v=J9BI0jGOds8&t=22475s)

**Learning objectives:**

- Add items with `append`, `insert` and `extend`.
- Remove items with `remove`, `pop`, `del` and `clear`.
- Search and count with `index` and `count`; reorder with `sort` and `reverse`.
- Predict which methods return `None` and which change the list.

**1. Intuition**

A method is a verb that belongs to the list itself: "list, add this at the end", "list, drop the last item", "list, sort yourself". Unlike built-in functions that look at a list from outside, most list methods *change* the list in place, like rearranging the shelf.

**2. Why does it exist?**

Lists are changeable collections, and programs constantly add, remove and reorder items: a shopping cart, a to-do list, a queue of messages. Methods give each change a clear name and make the intent readable.

**3. Technical explanation**

Methods are called with a dot: `items.append(5)`. The main list methods:

- `append(x)`: add one item at the end. `insert(i, x)`: put `x` before position `i`. `extend(iterable)`: add every item of an iterable at the end (`append` adds the iterable as one item).
- `remove(x)`: delete the first item equal to `x` (`ValueError` if absent). `pop()`: remove and return the last item; `pop(i)` does the same for position `i`. `clear()`: remove everything. The statement `del items[i]` and `del items[a:b]` also delete by position.
- `index(x)`: position of the first `x` (`ValueError` if absent). `count(x)`: how many times `x` appears.
- `sort()`: order the list in place (accepts `key=` and `reverse=`). `reverse()`: reverse in place.
- `copy()`: make a shallow copy (see the next section).

Important facts:

- Methods that change the list in place (`append`, `insert`, `extend`, `remove`, `sort`, `reverse`, `clear`) return `None`. `pop` returns the removed item. `index` and `count` return numbers.
- `append`, `insert` and `pop(0)` differ in cost: adding or removing at the end is fast; at the front the whole list has to shift. For queues use `collections.deque`.
- `remove` deletes only the first match.
- `+=` on a list behaves like `extend`.

**4. Syntax**

```text
items.append(x)         items.insert(index, x)    items.extend(iterable)
items.remove(x)         items.pop()               items.pop(index)
items.clear()           items.index(x)            items.count(x)
items.sort()            items.reverse()           items.copy()
del items[index]        del items[start:stop]
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
tasks = ["email", "report"]
tasks.append("lunch")
print(tasks)
tasks.insert(1, "call")
print(tasks)
tasks.extend(["gym", "read"])
print(tasks)
tasks.remove("report")
print(tasks)
last = tasks.pop()
print(last, tasks)
first = tasks.pop(0)
print(first, tasks)
print(tasks.index("lunch"), tasks.count("gym"))
tasks.sort()
print(tasks)
tasks.reverse()
print(tasks)
tasks.clear()
print(tasks)
```

Output:

```text
['email', 'report', 'lunch']
['email', 'call', 'report', 'lunch']
['email', 'call', 'report', 'lunch', 'gym', 'read']
['email', 'call', 'lunch', 'gym', 'read']
read ['email', 'call', 'lunch', 'gym']
email ['call', 'lunch', 'gym']
1 1
['call', 'gym', 'lunch']
['lunch', 'gym', 'call']
[]
```

Line by line:

- `append` adds at the end, `insert(1, ...)` puts the item at position 1 and shifts the rest right, `extend` adds several.
- `remove("report")` deletes by value; `pop()` and `pop(0)` delete by position and give the item back.
- `index` and `count` search; `sort` and `reverse` reorder the same list; `clear` empties it.

**6. Example 2 — Practical**

```python
# a stack: last in, first out
stack = []
for page in ["home", "search", "result"]:
    stack.append(page)
print("back button goes to", stack.pop(), "then", stack.pop())

# a queue (list version): first in, first out
queue = ["ticket 1", "ticket 2", "ticket 3"]
served = queue.pop(0)
print("serving", served, "| waiting:", queue)

# append versus extend
a = [1, 2]
a.append([3, 4])
b = [1, 2]
b.extend([3, 4])
print(a, b, len(a), len(b))

# collecting results in a loop
squares = []
for n in range(1, 6):
    squares.append(n * n)
print(squares)

# removing every occurrence
values = [3, 1, 3, 2, 3]
while 3 in values:
    values.remove(3)
print(values)

# removing by position and by slice
letters = list("abcdefg")
del letters[0]
del letters[1:3]
print(letters)

# sorting with a key, in place
people = [("Asha", 30), ("Ravi", 25), ("Meena", 28)]
people.sort(key=lambda person: person[1])
print(people)
```

Output:

```text
back button goes to result then search
serving ticket 1 | waiting: ['ticket 2', 'ticket 3']
[1, 2, [3, 4]] [1, 2, 3, 4] 3 4
[1, 4, 9, 16, 25]
[1, 2]
['b', 'e', 'f', 'g']
[('Ravi', 25), ('Meena', 28), ('Asha', 30)]
```

Line by line:

- A stack uses `append` and `pop()` at the same end; a queue adds at the end and takes from the front with `pop(0)`.
- `append([3, 4])` adds the whole list as one nested item (length 3), while `extend([3, 4])` adds two items (length 4).
- `remove` deletes only one match, so a `while` loop is used to remove all. (A list comprehension, see [List Comprehension](20-list-comprehension.md#list-comprehension), does this more directly.)
- `del` removes by position or slice. `lambda person: person[1]` is a small function that picks the age (see [Lambda Functions](28-first-class-functions-and-lambda.md#lambda-functions)).

**7. Example 3 — Edge case or common mistake**

```python
items = [1, 2, 3]
print(items.append(4))
print(items.remove(1))
print(items.sort())
print(items)

new_items = items.append(5)
print(new_items)
```

Output:

```text
None
None
None
[2, 3, 4]
None
```

In-place methods return `None`, so never write `x = x.append(...)`.

Errors from missing values and bad positions:

```python
numbers = [10, 20, 30]
for action in [lambda: numbers.remove(99), lambda: numbers.index(99),
               lambda: numbers.pop(10), lambda: [].pop(), lambda: numbers.insert("a", 5)]:
    try:
        action()
    except Exception as error:
        print(type(error).__name__ + ":", error)
```

Output:

```text
ValueError: list.remove(x): x not in list
ValueError: 99 is not in list
IndexError: pop index out of range
IndexError: pop from empty list
TypeError: 'str' object cannot be interpreted as an integer
```

And one behaviour that surprises beginners: `insert` with an out-of-range position does not fail:

```python
items = ["a", "b"]
items.insert(100, "end")
items.insert(-100, "start")
print(items)

numbers = [1, 2, 3]
numbers += [4, 5]
numbers = numbers + [6]
print(numbers)
```

Output:

```text
['start', 'a', 'b', 'end']
[1, 2, 3, 4, 5, 6]
```

Out-of-range insert positions are clamped to the start or end. `+=` extends in place, while `numbers + [6]` builds a new list.

**8. Common mistakes**

- Assigning the result of `append`, `sort`, `reverse`, `extend` or `remove` to a variable (it is `None`).
- Using `append` when `extend` was meant (nested list by mistake), or the opposite.
- Calling `remove` or `index` for a value that is not in the list without checking `in` first.
- Calling `pop()` on an empty list.
- Removing items while looping over the same list (see [The for Loop](17-for-loop-range-and-nested-loops.md#the-for-loop)).
- Using `pop(0)` in a loop on a huge list (it is slow); use `collections.deque`.
- Expecting `remove` to delete all matches.

**9. Real-world and AI applications**

Lists with these methods hold shopping carts, message histories and queues of jobs. In chat applications the conversation is a list of messages: each turn is `messages.append({...})`, and old messages may be dropped with `pop(0)` or slicing when the history is too long for the model's context window (see [Context Engineering](32-context-engineering-and-tokens.md#context-engineering)). Data pipelines build up lists of cleaned records with `append`, and gather results from several sources with `extend`.

**10. Practice**

1. Start with an empty list. Append 5, 10, 15; insert 0 at the front; extend with `[20, 25]`. Print after each step.
2. From `["a", "b", "c", "d"]`, remove `"c"`, pop the first item, and print the result and the removed item.
3. Show the difference between `append` and `extend` using `[1, 2, 3]` and `[4, 5]`.
4. Remove every `0` from `[0, 4, 0, 7, 0]` without a list comprehension.
5. Sort a list of `(name, score)` tuples by score, highest first.
6. Why does `numbers = [3, 1, 2].sort()` leave `numbers` as `None`?
7. Use a list as a stack to reverse the string `"python"`.

**11. Interview questions**

- *Difference between `append` and `extend`?* `append` adds one object (even a list) as a single item; `extend` adds each item of an iterable.
- *What do `remove`, `pop` and `del` differ in?* `remove` deletes by value; `pop` deletes by position and returns the item; `del` deletes by position or slice and returns nothing.
- *Which methods return `None`?* Those that change the list in place: `append`, `insert`, `extend`, `remove`, `sort`, `reverse`, `clear`.
- *Why is `pop(0)` slower than `pop()`?* All remaining items must shift one place left.

**12. Quick revision**

- Add: `append`, `insert`, `extend`. Remove: `remove`, `pop`, `del`, `clear`.
- Search: `index`, `count`. Reorder in place: `sort`, `reverse`.
- In-place methods return `None`; `pop` returns the removed item.
- `remove` takes the first match only; errors if absent.
- Use `+=` like `extend`.

---

## Copying Lists

**Timestamp:** [6:28:20](https://www.youtube.com/watch?v=J9BI0jGOds8&t=23300s)

**Learning objectives:**

- Explain why `b = a` does not copy a list.
- Make shallow copies with `copy()`, slicing `[:]` and `list()`.
- Explain what a shallow copy shares with the original, and make a deep copy with `copy.deepcopy`.
- Use `is` and `id()` to check whether two names refer to the same object.

**1. Intuition**

Two name tags on one suitcase are not two suitcases. If you give a friend your *document link* and they edit the document, you see their edits; if you give them a *printout*, you do not. In Python, `b = a` hands out another name tag for the same list. A copy is a new list with the same items.

**2. Why does it exist?**

Lists are *mutable* (changeable), and assignment never copies the object: it binds a second name to it. This is efficient, but it means a change through one name shows up through the other. Programs often need an independent list (to try out changes, to keep the original, to pass data to a function that must not alter it), so Python offers explicit copies.

**3. Technical explanation**

- *Assignment* (`b = a`): both names refer to the same list object. `a is b` is `True`, and `id(a) == id(b)`.
- *Shallow copy*: a new outer list holding references to the *same* items. Made with `a.copy()`, `a[:]`, `list(a)`, or `copy.copy(a)`. For a list of numbers or strings (immutable items) this is a full independent copy, because immutable items cannot be changed in place.
- *Deep copy*: `copy.deepcopy(a)` copies the list and, recursively, every mutable object inside it. Use it for nested lists, lists of dictionaries and similar.
- Comparison: `a == b` asks "equal contents?", `a is b` asks "the same object?" (see [Identity Operators](13-identity-operators-and-precedence.md#identity-operators-is-versus-equality)).
- Passing a list to a function also shares it: the function can change the caller's list.
- Multiplying a list of lists (`[[0] * 3] * 3`) makes several references to *one* inner list, a frequent trap.

**4. Syntax**

```text
b = a                      # same list, two names
b = a.copy()               # shallow copy
b = a[:]                   # shallow copy
b = list(a)                # shallow copy
import copy
b = copy.deepcopy(a)       # deep copy
```

This is a pattern, not runnable code (except the lines that are valid on their own once `a` exists).

**5. Example 1 — Basic**

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a, b, a is b)

c = a.copy()
c.append(5)
print(a, c, a is c)

d = a[:]
e = list(a)
print(d == a, d is a, e == a, e is a)
print(id(a) == id(b), id(a) == id(c))
```

Output:

```text
[1, 2, 3, 4] [1, 2, 3, 4] True
[1, 2, 3, 4] [1, 2, 3, 4, 5] False
True False True False
True False
```

Line by line:

- `b = a` shares the list, so appending through `b` changes what `a` shows, and `a is b` is `True`.
- `a.copy()` makes a separate list: appending to `c` leaves `a` alone. Slicing and `list()` do the same.
- Copies are *equal* (`==`) but not the *same object* (`is`). `id()` tells the identity of an object.

**6. Example 2 — Practical**

```python
import copy

original = [[1, 2], [3, 4]]
shallow = original.copy()
deep = copy.deepcopy(original)

original[0].append(99)
print("original:", original)
print("shallow: ", shallow)
print("deep:    ", deep)
print(shallow[0] is original[0], deep[0] is original[0])

shallow.append([5, 6])
print(len(original), len(shallow))

def add_bonus(scores):
    scores.append(100)

def add_bonus_safely(scores):
    new_scores = scores.copy()
    new_scores.append(100)
    return new_scores

marks = [60, 70]
add_bonus(marks)
print(marks)
safe = add_bonus_safely(marks)
print(marks, safe)

rows = [[0] * 3] * 3
rows[0][0] = 7
print(rows)
good = [[0] * 3 for _ in range(3)]
good[0][0] = 7
print(good)
```

Output:

```text
original: [[1, 2, 99], [3, 4]]
shallow:  [[1, 2, 99], [3, 4]]
deep:     [[1, 2], [3, 4]]
True False
2 3
[60, 70, 100]
[60, 70, 100] [60, 70, 100, 100]
[[7, 0, 0], [7, 0, 0], [7, 0, 0]]
[[7, 0, 0], [0, 0, 0], [0, 0, 0]]
```

Line by line:

- The shallow copy has its own outer list, but its inner lists are the *same objects* as the original's. Appending to an inner list shows through both, while `deep` (a deep copy) is unaffected. Adding a new item to the shallow copy's outer list does not change the original's length.
- A function that appends to its argument changes the caller's list. `add_bonus_safely` works on a copy and returns the result, leaving the input alone.
- `[[0] * 3] * 3` repeats a reference to one inner list three times, so setting one cell changes all rows. A comprehension (see [List Comprehension](20-list-comprehension.md#list-comprehension)) creates a separate inner list per row.

**7. Example 3 — Edge case or common mistake**

```python
a = [1, 2, 3]
b = a
a = a + [4]
print(a, b)

x = [1, 2, 3]
y = x
x += [4]
print(x, y)

p = [1, 2, 3]
q = p
p = [9, 9]
print(p, q)
```

Output:

```text
[1, 2, 3, 4] [1, 2, 3]
[1, 2, 3, 4] [1, 2, 3, 4]
[9, 9] [1, 2, 3]
```

Reassigning a name (`a = a + [4]`, `p = [9, 9]`) points the name at a *new* list and leaves the other name where it was. But `x += [4]` changes the existing list in place, so `y` sees it. The difference is whether the object is changed or a new one is bound.

Copies of lists with the same immutable items are safe, but containers inside need care:

```python
import copy

people = [{"name": "Asha", "tags": ["a"]}, {"name": "Ravi", "tags": []}]
shallow = people.copy()
deep = copy.deepcopy(people)

shallow[0]["tags"].append("vip")
print(people[0]["tags"], shallow[0]["tags"], deep[0]["tags"])

text = "hello"
copy_of_text = text
text = text.upper()
print(text, copy_of_text)
```

Output:

```text
['a', 'vip'] ['a', 'vip'] ['a']
HELLO hello
```

Strings, numbers and tuples cannot be changed in place, so sharing them is harmless: "changing" a string always creates a new string.

**8. Common mistakes**

- Believing `b = a` makes a copy.
- Using a shallow copy for nested data and then changing an inner item.
- Using `[[0] * n] * m` to build a grid.
- Changing a list passed to a function without realising the caller sees it.
- Using `is` to compare contents (use `==`).
- Using `deepcopy` everywhere. It is slower and unnecessary for flat lists of immutable items.
- Confusing `x += y` (in place) with `x = x + y` (new list) when other names refer to `x`.

**9. Real-world and AI applications**

Copies protect original data: keep the raw dataset untouched and work on a copy while cleaning; copy a configuration dictionary before changing one setting for an experiment; copy a list of messages before trimming it for a model request. Deep copies are used when nested structures (a list of message dictionaries) must be changed safely. Accidental sharing is a real source of bugs in machine-learning code, for example when the same default list or dictionary is reused for every experiment.

**10. Practice**

1. Create `a = [1, 2, 3]` and `b = a`. Append 4 to `b` and explain the output for `a`.
2. Make an independent copy of `[5, 6, 7]` in three different ways and prove they are independent.
3. For `data = [[1], [2]]`, show how `data.copy()` and `copy.deepcopy(data)` differ after `data[0].append(9)`.
4. Write a function `with_total(numbers)` that returns a new list with the sum added at the end, without changing the argument.
5. Build a 3 x 4 grid of zeros so that changing one cell changes only that cell.
6. What do `a == b` and `a is b` give for `a = [1]`, `b = [1]`?
7. After `x = [1, 2]`, `y = x`, `x += [3]`, `x = x + [4]`, what are `x` and `y`?

**11. Interview questions**

- *Does `b = a` copy a list?* No, it creates a second name for the same list.
- *What is the difference between a shallow and a deep copy?* A shallow copy duplicates only the outer list and shares the inner objects; a deep copy duplicates everything recursively.
- *How do you copy a list?* `a.copy()`, `a[:]`, `list(a)`; for nested data `copy.deepcopy(a)`.
- *Difference between `==` and `is`?* Equal contents versus the same object.
- *Why is `[[0] * 3] * 3` a bad way to build a grid?* All rows are the same inner list.

**12. Quick revision**

- `b = a` shares one list; changes through either name show in both.
- `copy()`, `[:]`, `list()` give shallow copies; `copy.deepcopy` copies nested objects too.
- Shallow copies are fine for flat lists of numbers or strings.
- `==` compares contents; `is` compares identity.
- `x += y` changes in place; `x = x + y` builds a new list.

---

## Answers to Practice Exercises

### Answers: Built-in List Functions

1.

```python
numbers = [14, 3, 27, 9, 21]
print(len(numbers), sum(numbers), min(numbers), max(numbers), sum(numbers) / len(numbers))
```

Output:

```text
5 74 3 27 14.8
```

2.

```python
words = ["pear", "Fig", "apple", "banana"]
print(sorted(words, key=str.lower))
print(sorted(words, key=len))
```

Output:

```text
['apple', 'banana', 'Fig', 'pear']
['Fig', 'pear', 'apple', 'banana']
```

3.

```python
values = [40, 15, 99, 62, 7, 84]
print(sorted(values, reverse=True)[:3])
```

Output:

```text
[99, 84, 62]
```

4.

```python
print(all(len(word) == 3 for word in ["tea", "cup", "pot"]))
```

Output:

```text
True
```

5. `sort()` changes the list in place and returns `None`. Assigning that result to the name replaces the list with `None`:

```python
numbers = [3, 1, 2]
numbers = numbers.sort()
print(numbers)
```

Output:

```text
None
```

Use `numbers.sort()` on its own line, or `numbers = sorted(numbers)`.

6.

```python
data = {"a": 5, "b": 2, "c": 9}
print(min(data, key=data.get))
```

Output:

```text
b
```

### Answers: List Methods

1.

```python
items = []
items.append(5)
items.append(10)
items.append(15)
print(items)
items.insert(0, 0)
print(items)
items.extend([20, 25])
print(items)
```

Output:

```text
[5, 10, 15]
[0, 5, 10, 15]
[0, 5, 10, 15, 20, 25]
```

2.

```python
letters = ["a", "b", "c", "d"]
letters.remove("c")
removed = letters.pop(0)
print(letters, removed)
```

Output:

```text
['b', 'd'] a
```

3.

```python
x = [1, 2, 3]
x.append([4, 5])
y = [1, 2, 3]
y.extend([4, 5])
print(x)
print(y)
```

Output:

```text
[1, 2, 3, [4, 5]]
[1, 2, 3, 4, 5]
```

4.

```python
values = [0, 4, 0, 7, 0]
while 0 in values:
    values.remove(0)
print(values)
```

Output:

```text
[4, 7]
```

5.

```python
results = [("Asha", 82), ("Ravi", 67), ("Meena", 91)]
results.sort(key=lambda pair: pair[1], reverse=True)
print(results)
```

Output:

```text
[('Meena', 91), ('Asha', 82), ('Ravi', 67)]
```

6. `[3, 1, 2].sort()` sorts the temporary list and returns `None`, and that `None` is stored in `numbers`. The sorted list is lost.

```python
numbers = [3, 1, 2].sort()
print(numbers)
```

Output:

```text
None
```

7.

```python
stack = []
for letter in "python":
    stack.append(letter)
reversed_text = ""
while stack:
    reversed_text += stack.pop()
print(reversed_text)
```

Output:

```text
nohtyp
```

A stack gives back the items in the opposite order. (`"python"[::-1]` is the shorter way.)

### Answers: Copying Lists

1.

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a, b)
```

Output:

```text
[1, 2, 3, 4] [1, 2, 3, 4]
```

`b` is another name for the same list, so the change made through `b` is visible through `a`.

2.

```python
import copy

original = [5, 6, 7]
copies = [original.copy(), original[:], list(original), copy.copy(original)]
original.append(8)
print(original)
print(copies)
print([c is original for c in copies])
```

Output:

```text
[5, 6, 7, 8]
[[5, 6, 7], [5, 6, 7], [5, 6, 7], [5, 6, 7]]
[False, False, False, False]
```

3.

```python
import copy

data = [[1], [2]]
shallow = data.copy()
deep = copy.deepcopy(data)
data[0].append(9)
print(data, shallow, deep)
```

Output:

```text
[[1, 9], [2]] [[1, 9], [2]] [[1], [2]]
```

The shallow copy shares the inner list `[1]`, so it shows the `9`; the deep copy has its own inner lists.

4.

```python
def with_total(numbers):
    result = numbers.copy()
    result.append(sum(numbers))
    return result


original = [4, 5, 6]
print(with_total(original), original)
```

Output:

```text
[4, 5, 6, 15] [4, 5, 6]
```

5.

```python
grid = [[0] * 4 for _ in range(3)]
grid[1][2] = 5
print(grid)
```

Output:

```text
[[0, 0, 0, 0], [0, 0, 5, 0], [0, 0, 0, 0]]
```

6.

```python
a = [1]
b = [1]
print(a == b, a is b)
```

Output:

```text
True False
```

They are equal in content but are two separate objects.

7.

```python
x = [1, 2]
y = x
x += [3]
print(x, y)
x = x + [4]
print(x, y)
```

Output:

```text
[1, 2, 3] [1, 2, 3]
[1, 2, 3, 4] [1, 2, 3]
```

`x += [3]` extends the shared list in place, so `y` sees it. `x = x + [4]` builds a new list and rebinds `x`, so `y` keeps the old one.

---

## Chapter Summary and Key Takeaways

- Built-in functions (`len`, `sum`, `min`, `max`, `sorted`, `reversed`, `any`, `all`) read a list and never change it; `sorted` returns a new list, `sort()` changes the list and returns `None`.
- List methods such as `append`, `insert`, `extend`, `remove`, `pop`, `clear`, `sort` and `reverse` change the list in place; `index` and `count` search it.
- `append` adds one object; `extend` adds each item of an iterable.
- `b = a` does not copy: it adds a second name for the same list. Use `copy()`, `[:]` or `list()` for a shallow copy and `copy.deepcopy` for nested data.
- Shallow copies share inner mutable objects; `[[0] * n] * m` shares one inner list.

Next: [Chapter 20 — List Comprehension](20-list-comprehension.md) shows the compact way to build and filter lists.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
