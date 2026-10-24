# Chapter 18 — Data Structures Introduction and Lists

> Part 4 — Python Data Structures · Video: 5:33:56–5:54:24 · Previous: [17 for Loops, range() and Nested Loops](17-for-loop-range-and-nested-loops.md) · Next: [19 List Functions, Methods and Copying](19-list-functions-methods-and-copying.md)

**In this chapter:** why programs need data structures, a first look at the four built-in collections (list, tuple, set, dict), how to create lists (including lists with mixed types and lists inside lists), how to read and change list items with indexes and slices, why lists are mutable, and the everyday list operators (`+`, `*`, `in`, `len()`, `del`, and looping over a list).

**Before you start:** you should know that a variable is a name that refers to a value, and that strings can be read by position. Recap: an index is a position number that starts at 0 (see [String Indexing](06-strings-basics-indexing-concatenation.md#string-indexing)), a negative index counts from the end (see [Negative Indexing](06-strings-basics-indexing-concatenation.md#negative-indexing)), and a slice such as `text[1:4]` copies a range of items (see [String Slicing](07-string-slicing.md#string-slicing) and [Slicing with a Step Value](07-string-slicing.md#slicing-with-a-step-value)). You should also be able to write a `for` loop (see [The for Loop](17-for-loop-range-and-nested-loops.md#the-for-loop)). Everything in this chapter was run with Python 3.13.16; list behavior shown here is the same in all current Python 3 versions unless the text says otherwise.

---

## Introduction to Data Structures

**Timestamp:** [5:33:56](https://www.youtube.com/watch?v=J9BI0jGOds8&t=20036s)

**Learning objectives:**

- Explain what a data structure is and what problem it solves.
- Name the four built-in collection types (list, tuple, set, dict) and state one property of each.
- Write the literal form of each collection and check its type with `type()`.

**1. Intuition**

So far each variable has held one value: one number, one string, one boolean. Real programs deal with many values at once: the marks of forty students, the words of a sentence, the rows of a spreadsheet. Writing `mark1`, `mark2`, `mark3` up to `mark40` is not practical. A data structure is a way of storing many values together under one name, with rules for how you may add, find, and change them.

An everyday picture: a single variable is one labelled jar. A data structure is a shelf, a filing cabinet, or an address book. Each one holds many things, but each is organized differently, and the organization decides what is quick to do (look something up by name, keep things in order, avoid duplicates).

**2. Why does it exist?**

Two problems appear as soon as a program grows:

1. You do not know in advance how many values you will have. A program that reads a file may find 3 lines or 3 million.
2. You want to treat the values as a group: count them, sort them, loop over them, send them to a function in one piece.

Separate variables cannot solve either problem. A collection can. Python offers several built-in collections because different jobs need different rules: sometimes order matters, sometimes uniqueness matters, sometimes you want to look a value up by a label.

**3. Technical explanation**

A collection (also called a container) is an object that holds references to other objects. The collection does not store the values "inside itself" in the way a number is stored; each slot refers to another object. This detail matters later, in the copying section of [Chapter 19](19-list-functions-methods-and-copying.md#copying-lists).

Two words used throughout this part:

- **Sequence:** a collection whose items have a fixed order and can be reached by position (an index). Strings, lists, tuples and `range` objects are sequences.
- **Mutable / immutable:** a mutable object can be changed after it is created; an immutable object cannot. Mutable means "can be modified in place".

The four built-in collections compared:

| Type | Literal | Ordered by position | Mutable | Duplicates allowed | Main use |
|------|---------|--------------------|---------|--------------------|----------|
| `list` | `[1, 2, 3]` | yes | yes | yes | an ordered, changeable sequence of items |
| `tuple` | `(1, 2, 3)` | yes | no | yes | a fixed group of related values |
| `set` | `{1, 2, 3}` | no (no index) | yes | no (each item once) | membership tests and removing duplicates |
| `dict` | `{"a": 1}` | keys keep insertion order (Python 3.7 and later) | yes | keys must be unique | looking up a value by a key |

"Ordered by position" for a set means you cannot ask for "the third item"; sets have no indexing. Dictionaries remember the order in which keys were inserted, but you look values up by key, not by position. Items of a set and keys of a dict must be hashable, a term explained in [Chapter 21](21-tuples.md#tuples) and [Chapter 22](22-sets.md).

This chapter and the next two cover lists in depth. Chapter 21 covers tuples, Chapter 22 sets, and Chapter 23 dictionaries.

**4. Syntax**

```text
list_literal  = [item, item, item]
tuple_literal = (item, item, item)
set_literal   = {item, item, item}
dict_literal  = {key: value, key: value}
```

The block above is a pattern, not runnable Python (the names `item`, `key` and `value` are placeholders). Square brackets make a list, round brackets make a tuple, curly brackets make either a set (items only) or a dict (`key: value` pairs). An empty `{}` is a dict, not a set; an empty set is written `set()`.

**5. Example 1 — Basic**

```python
marks_list = [78, 91, 64]
marks_tuple = (78, 91, 64)
marks_set = {78, 91, 64}
marks_dict = {"maths": 78, "physics": 91, "chemistry": 64}

for collection in (marks_list, marks_tuple, marks_set, marks_dict):
    print(type(collection).__name__, len(collection))
```

Output:

```text
list 3
tuple 3
set 3
dict 3
```

`type()` is a built-in function that returns the type of an object; `.__name__` reads the type's name as text. `len()` is a built-in function that returns the number of items (for a dict it counts keys). The loop itself iterates over a tuple of four collections, which shows that a collection can hold other collections.

**6. Example 2 — Practical**

The same facts can be modeled in different ways. Suppose you want to store the subjects a student has passed.

```python
# Task A: keep every mark in the order the exams were taken
marks_in_order = [78, 91, 64, 91]

# Task B: keep the exam date and the room, a fixed pair that never changes
exam_slot = ("2025-11-03", "Hall B")

# Task C: record which subjects were attempted, no repeats
subjects_attempted = {"maths", "physics", "chemistry"}

# Task D: look up a mark using the subject name
mark_by_subject = {"maths": 78, "physics": 91, "chemistry": 64}

print(marks_in_order[1])
print(exam_slot[1])
print("physics" in subjects_attempted)
print(mark_by_subject["chemistry"])
```

Output:

```text
91
Hall B
True
64
```

Line by line: Task A needs order and allows the repeated 91, so a list fits. Task B is a small fixed record; a tuple signals that it should not be edited. Task C only asks "is this subject in the group?", so a set fits. Task D asks "what is the value for this label?", so a dict fits. Choosing the structure that matches the question is the main skill of this part of the handbook; [Chapter 24](24-mutability-iteration-and-pitfalls.md#choosing-the-right-data-structure) returns to it.

**7. Example 3 — Edge case or common mistake**

```python
empty_braces = {}
empty_set = set()
not_a_tuple = (5)
a_tuple = (5,)

print(type(empty_braces).__name__)
print(type(empty_set).__name__)
print(type(not_a_tuple).__name__)
print(type(a_tuple).__name__)
```

Output:

```text
dict
set
int
tuple
```

Two surprises. First, `{}` creates an empty dict because dicts used braces first; to get an empty set you must call `set()`. Second, round brackets alone do not make a tuple: `(5)` is just the number 5 in parentheses, exactly as in `(2 + 3) * 4`. The comma is what makes a tuple, so a one-item tuple is written `(5,)`. Chapter 21 explains this in full.

**8. Common mistakes**

- Using `{}` and expecting an empty set. Use `set()`.
- Writing `(5)` and expecting a one-item tuple. Write `(5,)`.
- Creating a list of 40 separate variables instead of one list. If you find yourself numbering variable names, you need a collection.
- Choosing a list for everything. A list answers "what is at position i?" well, but "is this value present?" is faster with a set and "what is the value for this key?" is what a dict is for.

**9. Real-world and AI applications**

Every nontrivial program is built from these four structures. In AI and data work you will meet them constantly: a list of text chunks to send to a model, a list of dicts where each dict is one chat message (`{"role": "user", "content": "..."}`), a tuple for an array shape such as `(rows, columns)`, a set for the vocabulary of unique words in a dataset, and a dict for configuration settings or for JSON data returned by a web service.

**10. Practice**

1. Write the literal for each of the four collections holding the three numbers 1, 2, 3 (use `1: "one"` style pairs for the dict). Print the `type()` of each.
2. Predict the type of each: `[]`, `()`, `{}`, `set()`, `(7)`, `(7,)`, `{7}`, `{7: 7}`. Then check by running.
3. For each need, name the best collection and give a reason: (a) the days of the week in order; (b) the unique cities in a customer list; (c) the price of each product by product name; (d) a latitude and longitude pair.

**11. Interview questions**

1. *What is a data structure?* A way of organizing many values under one name, together with the operations allowed on them.
2. *Which of list, tuple, set, dict are mutable?* List, set and dict are mutable; tuple is immutable.
3. *How do you create an empty set?* With `set()`. Literal `{}` creates an empty dict.
4. *(Code)* What does `type((1))` return? `<class 'int'>`, because the parentheses do not create a tuple without a comma.

**12. Quick revision**

- A data structure stores many values under one name.
- List: ordered, mutable, duplicates allowed. Tuple: ordered, immutable. Set: unique items, no index. Dict: key-to-value lookup.
- `{}` is an empty dict; `set()` is an empty set; `(5,)` is a one-item tuple.

---

## Lists in Python

**Timestamp:** [5:43:37](https://www.youtube.com/watch?v=J9BI0jGOds8&t=20617s)

**Learning objectives:**

- Create lists, including empty lists, lists of mixed types, and nested lists.
- Read items with positive and negative indexes and copy ranges with slices.
- Change items by index assignment and explain why lists are mutable.

**1. Intuition**

A list is an ordered row of boxes. Each box has a position number starting at 0, and each box can hold anything. You can look in any box, replace what is in it, add boxes at the end, and remove boxes. Think of a train: carriages are in a fixed order, you can name carriage 3, and the railway can swap the contents of a carriage without replacing the whole train.

**2. Why does it exist?**

Programs constantly need a changeable ordered group: the items in a shopping cart, the lines read from a file, the scores of a game that are still being added. A string is ordered but cannot be edited, and separate variables cannot grow. The list is Python's general-purpose answer.

**3. Technical explanation**

A list is an object of type `list`. Internally it stores a sequence of references, one per item, to other objects. Consequences:

- Items can be of different types because each slot only holds a reference. `[1, "two", 3.0, True]` is valid.
- A list can contain another list, giving a nested list. The inner list is one item of the outer list.
- Indexing starts at 0. For a list of length `n`, valid indexes are `0` to `n - 1`, and `-1` to `-n` counting from the end. Anything outside this range raises `IndexError`.
- Slicing `items[start:stop:step]` returns a new list holding references to the selected items. `stop` is excluded, any of the three parts may be omitted, and out-of-range slice bounds are quietly clipped instead of raising an error (see Example 3).
- Lists are mutable: `items[i] = value` replaces the reference in slot `i` and the list object itself stays the same object. This is the key difference from strings, where every "change" produces a new string.

**4. Syntax**

```text
name = [item1, item2, item3]     create a list
name = []                        create an empty list
name = list(iterable)            build a list from any iterable
name[index]                      read one item
name[start:stop:step]            read a slice (new list)
name[index] = new_value          replace one item
```

This block is a pattern, not runnable Python. `list(iterable)` is the built-in `list` constructor; an iterable is anything you can loop over, such as a string or a `range`. For example, `list("abc")` gives `['a', 'b', 'c']` and `list(range(3))` gives `[0, 1, 2]`.

**5. Example 1 — Basic**

```python
fruits = ["apple", "banana", "cherry", "date", "elderberry"]
mixed = [42, "text", 3.14, True, None]
nested = [[1, 2, 3], [4, 5, 6]]
empty = []

print(fruits[0])
print(fruits[-1])
print(fruits[1:4])
print(fruits[::2])
print(fruits[::-1])
print(mixed)
print(nested[1][2])
print(len(empty))

fruits[1] = "blueberry"
print(fruits)
```

Output:

```text
apple
elderberry
['banana', 'cherry', 'date']
['apple', 'cherry', 'elderberry']
['elderberry', 'date', 'cherry', 'banana', 'apple']
[42, 'text', 3.14, True, None]
6
0
['apple', 'blueberry', 'cherry', 'date', 'elderberry']
```

Reading the output: `fruits[0]` is the first item and `fruits[-1]` the last. `fruits[1:4]` takes positions 1, 2 and 3 (the stop position 4 is excluded). `fruits[::2]` takes every second item, and `fruits[::-1]` walks backward and so produces a reversed copy. `nested[1][2]` first picks the inner list at position 1 (`[4, 5, 6]`) and then item 2 of it, which is 6. The last two lines show assignment by index: the list is edited in place and now contains `"blueberry"`.

**6. Example 2 — Practical**

A small seating plan for a game of noughts and crosses (tic-tac-toe) stored as a list of rows, where each row is itself a list.

```python
board = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "],
]

board[1][1] = "X"      # centre square
board[0][2] = "O"      # top-right square
board[2][0] = "X"      # bottom-left square

for row in board:
    print("|".join(row))
    print("-+-+-")

print("Centre:", board[1][1])
print("Last row, first column:", board[-1][0])
```

Output:

```text
 | |O
-+-+-
 |X| 
-+-+-
X| | 
-+-+-
Centre: X
Last row, first column: X
```

Line by line: `board` holds three rows. `board[1][1] = "X"` first finds row 1 and then replaces item 1 inside that row, so only one cell changes. The `for` loop visits each row (a list of three strings); `"|".join(row)` is a string method that glues the strings of `row` together using `|` between them. `board[-1][0]` uses a negative index for the last row and a positive index for the first column. Nested lists like this are the simplest way to represent grids, tables and images before using specialized libraries.

**7. Example 3 — Edge case or common mistake**

```python
colors = ["red", "green", "blue"]

print(colors[1:10])
print(colors[5:])
```

Output:

```text
['green', 'blue']
[]
```

Slices never raise `IndexError`: out-of-range bounds are clipped, and a slice that selects nothing gives an empty list. A single index is stricter:

```python
colors = ["red", "green", "blue"]
print(colors[3])
```

Output (the error, with the file path shortened):

```text
Traceback (most recent call last):
  File "example.py", line 2, in <module>
    print(colors[3])
          ~~~~~~^^^
IndexError: list index out of range
```

There are three items so the valid indexes are 0, 1, 2 and -1, -2, -3. Index 3 does not exist. A related common mistake is trying to edit a string the way you edit a list:

```python
word = "cat"
word[0] = "b"
```

Output (the error):

```text
Traceback (most recent call last):
  File "example.py", line 2, in <module>
    word[0] = "b"
    ~~~~^^^
TypeError: 'str' object does not support item assignment
```

Strings are immutable. To "change" a string you build a new one, for example `"b" + word[1:]`. A list accepts the same assignment because it is mutable:

```python
letters = ["c", "a", "t"]
letters[0] = "b"
print(letters)
```

Output:

```text
['b', 'a', 't']
```

**8. Common mistakes**

- Off-by-one errors: the last valid index is `len(items) - 1`, not `len(items)`. Use `items[-1]` for the last item.
- Reading from an empty list: `[][0]` raises `IndexError`. Check `len(items)` or use a condition first.
- Confusing `items[i]` (one item) with `items[i:i+1]` (a list containing one item).
- Expecting `items[1:3]` to include position 3. The stop position is excluded.
- Assuming slicing changes the original. A slice is a new list; the original is untouched.
- Forgetting that nested lists need two indexes: `grid[row][column]`.

**9. Real-world and AI applications**

Lists hold nearly every "many things" value in practical programs: lines of a text file, command-line arguments, search results, rows fetched from a database. In AI code, a list of token IDs is what a tokenizer returns, a list of floats is the plain-Python form of an embedding vector, and a list of lists is the plain-Python form of a matrix or a batch of inputs. Libraries such as NumPy convert these lists into faster array types, but the indexing and slicing rules you learned here carry over almost unchanged.

**10. Practice**

1. Create a list of five cities. Print the first, the last, the middle one (by index), and the first three using a slice.
2. Given `numbers = [10, 20, 30, 40, 50, 60]`, write one slice expression each for: every item from position 2 onward; every second item; the list reversed; the last two items.
3. Given `matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]`, print the number 6, then change it to 60 and print the whole matrix.
4. Predict the output without running, then check: `data = [1, 2, 3]`, `print(data[1:100])`, `print(data[-4:])`, `print(data[3])` (the last line fails; say what error and why).

**11. Interview questions**

1. *Why are lists called mutable?* You can change their contents in place (assignment by index, adding and removing items) without creating a new list object.
2. *Can a list hold different data types?* Yes. Each slot holds a reference, so types can differ.
3. *What is the difference between `items[5]` and `items[5:6]` when the list has 3 items?* `items[5]` raises `IndexError`; `items[5:6]` returns an empty list.
4. *(Code)* What does `[1, 2, 3, 4][::-1]` return? `[4, 3, 2, 1]`, a new reversed list.

**12. Quick revision**

- `[a, b, c]` creates a list; items may differ in type and may be lists themselves.
- Index from 0 or from -1; slices copy and never raise `IndexError`; single bad indexes do.
- `items[i] = x` edits in place; this is why lists are mutable and strings are not.
- Nested lists need `grid[row][col]`.

---

## List Operations

**Timestamp:** [5:54:24](https://www.youtube.com/watch?v=J9BI0jGOds8&t=21264s)

**Learning objectives:**

- Combine and repeat lists with `+` and `*`, and test membership with `in`.
- Measure a list with `len()` and remove items or slices with `del`.
- Iterate over a list by value and by index, and avoid the shared-rows pitfall of `*` on nested lists.

**1. Intuition**

Operators that worked on strings also work on lists, with the same meaning: `+` joins, `*` repeats, `in` checks presence, `len()` counts. The difference is that a list can also lose items with `del`. Think of a list as a queue of people: you can join two queues, count the people, ask whether someone is in the queue, and remove people from it.

**2. Why does it exist?**

Once data is in a list, you need to do routine things to it: combine two sources of data, make a starting list of a given size, ask whether a value is present, and visit every item. Operators give short, readable forms for these routine jobs.

**3. Technical explanation**

- `a + b` creates a new list holding the items of `a` followed by the items of `b`. Both operands must be lists; `[1, 2] + 3` raises `TypeError`. The originals are not modified.
- `a * n` creates a new list with the items of `a` repeated `n` times. If `n` is zero or negative the result is an empty list. The repeats are references to the same item objects, which is harmless for numbers and strings but important for nested lists (Example 3).
- `x in a` checks whether any item equals `x` (it compares with `==`). It scans from the start until it finds a match, so on a long list it can be slow. `x not in a` is the opposite.
- `len(a)` is a built-in function returning the number of items. It counts top-level items only: `len([[1, 2], [3]])` is 2.
- `del a[i]` removes the item at index `i`, and the items after it shift one position to the left. `del a[i:j]` removes a slice. `del a[::2]` removes every second item. `del a` (without brackets) removes the name `a` itself, not just its contents.
- `a += b` extends `a` in place (it modifies the existing list), whereas `a = a + b` builds a new list and rebinds the name. This difference becomes visible when two names refer to the same list.
- `a == b` compares lists item by item and returns `True` if they have the same length and equal items. Lists also compare with `<` and `>` item by item from the left, like words in a dictionary.
- Iteration: `for item in a:` visits items in order. When you also need the position, `for i in range(len(a)):` gives indexes; the more convenient `enumerate()` is covered in [Chapter 19](19-list-functions-methods-and-copying.md#built-in-list-functions).

**4. Syntax**

```text
a + b              new list: items of a, then items of b
a * n              new list: a repeated n times
x in a             True if some item of a equals x
x not in a         True if no item of a equals x
len(a)             number of items
del a[i]           delete one item by index
del a[i:j]         delete a slice
for item in a:     loop over the items
```

This is a pattern block, not runnable Python. All of `+`, `*`, `in` and `not in` are operators; `len()` is a built-in function; `del` is a statement (a keyword, not a function, so it is written without parentheses).

**5. Example 1 — Basic**

```python
morning = ["tea", "toast"]
evening = ["rice", "curry"]

meals = morning + evening
print(meals)
print(morning)                 # unchanged

print(["ab"] * 3)
print([0] * 5)
print([1, 2] * 0)

print("rice" in meals)
print("pizza" in meals)
print("pizza" not in meals)
print(len(meals))

del meals[0]
print(meals)
del meals[1:]
print(meals)

for meal in evening:
    print("Meal:", meal)
```

Output:

```text
['tea', 'toast', 'rice', 'curry']
['tea', 'toast']
['ab', 'ab', 'ab']
[0, 0, 0, 0, 0]
[]
True
False
True
4
['toast', 'rice', 'curry']
['toast']
Meal: rice
Meal: curry
```

`morning + evening` leaves both original lists unchanged and gives a third list. `[0] * 5` is the standard way to make a list of five zeros. After `del meals[0]` the remaining items moved left, so the former item at index 1 is now at index 0; `del meals[1:]` then removed everything from index 1 onward.

**6. Example 2 — Practical**

Remove all entries of a specific kind by building a new list, and count how many visits each position had using a list as a table of counters.

```python
# Task 1: keep only the long words, building a new list
words = ["a", "list", "can", "hold", "any", "words"]
long_words = []
for word in words:
    if len(word) > 3:
        long_words.append(word)
print(long_words)

# Task 2: a list as a table of counters (index = die face minus one)
rolls = [3, 1, 6, 3, 3, 2, 6]
counts = [0] * 6
for roll in rolls:
    counts[roll - 1] += 1
print(counts)

# Task 3: iterate by index when you need the position
for position in range(len(long_words)):
    print(position, long_words[position])
```

Output:

```text
['list', 'hold', 'words']
[1, 1, 3, 0, 0, 2]
0 list
1 hold
2 words
```

Task 1 uses `.append()`, a list method that adds one item at the end; methods are covered fully in [Chapter 19](19-list-functions-methods-and-copying.md#list-methods). The result is a new list; the original `words` is unchanged. Task 2 shows why `[0] * n` is useful: it creates `n` independent counters (numbers are immutable, so changing one counter with `+=` replaces only that slot). `counts[roll - 1] += 1` reads the slot, adds one and stores it back. Task 3 loops over valid indexes created by `range(len(...))`.

**7. Example 3 — Edge case or common mistake**

The repetition operator copies references, not objects. With numbers this is invisible, but with nested lists every "row" is the same list object:

```python
grid = [[0] * 3] * 3
grid[0][0] = 9
print(grid)
print(grid[0] is grid[1])
```

Output:

```text
[[9, 0, 0], [9, 0, 0], [9, 0, 0]]
True
```

All three rows changed because `[[0] * 3] * 3` repeats the reference to one inner list three times. `grid[0] is grid[1]` is `True`: the same object appears in three positions. The correct way is to build a separate inner list on each pass, which a list comprehension does (see [Chapter 20](20-list-comprehension.md#list-comprehension)):

```python
grid = [[0] * 3 for _ in range(3)]
grid[0][0] = 9
print(grid)
print(grid[0] is grid[1])
```

Output:

```text
[[9, 0, 0], [0, 0, 0], [0, 0, 0]]
False
```

A second subtlety is `+=` versus `+`:

```python
original = [1, 2]
alias = original

original += [3]            # extends the existing list in place
print(alias)

original = original + [4]  # builds a new list and rebinds the name
print(alias)
print(original)
```

Output:

```text
[1, 2, 3]
[1, 2, 3]
[1, 2, 3, 4]
```

After the first statement `alias` shows the 3 because `+=` changed the one shared list. After the second, `original` refers to a brand-new list, so `alias` is left behind. The first mistake of this example, `[1, 2] + 3`, fails like this:

```python
print([1, 2] + 3)
```

Output (the error):

```text
Traceback (most recent call last):
  File "example.py", line 1, in <module>
    print([1, 2] + 3)
          ~~~~~~~^~~
TypeError: can only concatenate list (not "int") to list
```

`+` needs two lists. To add a single item use `[1, 2] + [3]` or the `.append()` method.

**8. Common mistakes**

- Using `[[0] * 3] * 3` to build a grid (shared rows). Use a comprehension such as `[[0] * 3 for _ in range(3)]`.
- Adding a non-list with `+` (`TypeError`). Wrap the item in a list or use `.append()`.
- Deleting inside a loop over the same list. Items shift while the loop is running and some are skipped. Build a new list instead, or see [Chapter 24](24-mutability-iteration-and-pitfalls.md#iterating-safely).
- Using `in` on a very large list inside a loop. Each test scans the list; Chapter 22 shows how a set makes membership tests fast.
- Writing `del(my_list[0])` and thinking `del` is a function. The parentheses are harmless but misleading.
- Expecting `len()` to count nested items. It counts top-level items only.

**9. Real-world and AI applications**

`+` is how you concatenate batches of data or merge two lists of results. `[0] * n` creates fixed-size buffers, zero vectors, and count tables (as in Task 2). `in` is used for simple filters such as "is this word in the list of stop words?". Looping over a list of text chunks, one at a time, is the basic shape of most data-preparation scripts in machine-learning projects.

**10. Practice**

1. Given `a = [1, 2, 3]` and `b = [4, 5]`, print `a + b`, `b * 3`, and whether `3 in a` and `3 in b`.
2. Create a list of ten zeros using an operator. Set the fifth item to 1 and print the list.
3. Given `items = ["a", "b", "c", "d", "e", "f"]`, use `del` once to remove "b" and "c", and once more to remove every second remaining item. Print the result.
4. Predict the output, then run: `x = [[1, 2]] * 2`, `x[0].append(3)`, `print(x)`. Explain it, and rewrite the first line so the rows are independent.
5. Write a loop with `range(len(...))` that prints each item of a list together with its index. Then explain what goes wrong if you write `range(len(items) + 1)`.

**11. Interview questions**

1. *What is the difference between `a + b` and `a += b` for lists?* `a + b` creates a new list; `a += b` extends `a` in place and keeps the same object, so other names referring to `a` see the change.
2. *What does `[[]] * 3` create?* A list of three references to the same empty list, not three separate lists.
3. *How does `in` work on a list and what does it cost?* It compares each item with `==` from the start until a match is found, so the cost grows with the list length.
4. *(Code)* What is `len([[1, 2], [3, 4, 5]])`? 2, because only the two inner lists are counted.

**12. Quick revision**

- `+` joins into a new list; `*` repeats references; `in` and `not in` test membership; `len()` counts top-level items.
- `del a[i]`, `del a[i:j]`, `del a[::2]` remove items in place; `del a` removes the name.
- `+=` mutates in place; `a = a + b` makes a new list.
- Never build a grid with `[[0] * 3] * 3`.

---

## Answers to Practice Exercises

### Answers: Introduction to Data Structures

**Exercise 1.**

```python
as_list = [1, 2, 3]
as_tuple = (1, 2, 3)
as_set = {1, 2, 3}
as_dict = {1: "one", 2: "two", 3: "three"}

for collection in (as_list, as_tuple, as_set, as_dict):
    print(type(collection))
```

```text
<class 'list'>
<class 'tuple'>
<class 'set'>
<class 'dict'>
```

Explanation: `[]` gives a list, `()` with commas a tuple, `{}` with items only a set, and `{}` with `key: value` pairs a dict. The printed form `<class 'list'>` is what `type()` returns.

**Exercise 2.**

```python
for value in ([], (), {}, set(), (7), (7,), {7}, {7: 7}):
    print(repr(value), type(value).__name__)
```

```text
[] list
() tuple
{} dict
set() set
7 int
(7,) tuple
{7} set
{7: 7} dict
```

Explanation: `{}` is a dict; `set()` is the empty set; `(7)` is just the int 7 (the printed `7` shows no brackets); `(7,)` is a tuple; `{7}` is a set; `{7: 7}` is a dict. `repr()` is a built-in function that shows a value the way you would write it in code.

**Exercise 3.** (a) A list or tuple, because the order of the days matters and the days do not change; a tuple is the better signal for a fixed list. (b) A set, because it stores each city once and tests membership quickly. (c) A dict, with the product name as key and the price as value. (d) A tuple `(latitude, longitude)`, a small fixed pair of related values.

### Answers: Lists in Python

**Exercise 1.**

```python
cities = ["Mumbai", "Delhi", "Chennai", "Kolkata", "Pune"]
print(cities[0])
print(cities[-1])
print(cities[len(cities) // 2])
print(cities[:3])
```

```text
Mumbai
Pune
Chennai
['Mumbai', 'Delhi', 'Chennai']
```

Explanation: `len(cities) // 2` is 2 (integer division), which is the middle position of five items. `cities[:3]` omits the start, so it begins at 0 and stops before position 3.

**Exercise 2.**

```python
numbers = [10, 20, 30, 40, 50, 60]
print(numbers[2:])
print(numbers[::2])
print(numbers[::-1])
print(numbers[-2:])
```

```text
[30, 40, 50, 60]
[10, 30, 50]
[60, 50, 40, 30, 20, 10]
[50, 60]
```

Explanation: `[2:]` goes from position 2 to the end; `[::2]` uses step 2 from the start; `[::-1]` steps backward through the whole list; `[-2:]` starts two items from the end and runs to the end.

**Exercise 3.**

```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(matrix[1][2])
matrix[1][2] = 60
print(matrix)
```

```text
6
[[1, 2, 3], [4, 5, 60], [7, 8, 9]]
```

Explanation: the number 6 is in row 1 (the second row) at column 2 (the third item). Assigning to `matrix[1][2]` replaces only that one slot inside that one inner list.

**Exercise 4.**

```python
data = [1, 2, 3]
print(data[1:100])
print(data[-4:])
print(data[3])
```

```text
[2, 3]
[1, 2, 3]
Traceback (most recent call last):
  File "example.py", line 4, in <module>
    print(data[3])
          ~~~~^^^
IndexError: list index out of range
```

Explanation: the first two lines succeed because slice bounds are clipped: `data[1:100]` gives `[2, 3]` and `data[-4:]` (start before the beginning) gives the whole list. `data[3]` is a single index beyond the last valid one (2), so it raises `IndexError`.

### Answers: List Operations

**Exercise 1.**

```python
a = [1, 2, 3]
b = [4, 5]
print(a + b)
print(b * 3)
print(3 in a, 3 in b)
```

```text
[1, 2, 3, 4, 5]
[4, 5, 4, 5, 4, 5]
True False
```

Explanation: `+` joins, `*` repeats, and `in` returns `True` or `False`. `print` shows two values separated by a space.

**Exercise 2.**

```python
zeros = [0] * 10
zeros[4] = 1
print(zeros)
```

```text
[0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
```

Explanation: the fifth item has index 4. Using `*` is safe here because the repeated item is the immutable number 0.

**Exercise 3.**

```python
items = ["a", "b", "c", "d", "e", "f"]
del items[1:3]
print(items)
del items[::2]
print(items)
```

```text
['a', 'd', 'e', 'f']
['d', 'f']
```

Explanation: `del items[1:3]` removes positions 1 and 2 ("b" and "c"), leaving `['a', 'd', 'e', 'f']`. `del items[::2]` then removes positions 0 and 2 ("a" and "e"), leaving `['d', 'f']`.

**Exercise 4.**

```python
x = [[1, 2]] * 2
x[0].append(3)
print(x)

x = [[1, 2] for _ in range(2)]
x[0].append(3)
print(x)
```

```text
[[1, 2, 3], [1, 2, 3]]
[[1, 2, 3], [1, 2]]
```

Explanation: in the first version both positions hold the same inner list, so appending through `x[0]` appears in `x[1]` too. The comprehension creates a new `[1, 2]` on each pass, so the rows are independent.

**Exercise 5.**

```python
items = ["red", "green", "blue"]
for index in range(len(items)):
    print(index, items[index])

for index in range(len(items) + 1):
    print(index, items[index])
```

```text
0 red
1 green
2 blue
0 red
1 green
2 blue
Traceback (most recent call last):
  File "example.py", line 6, in <module>
    print(index, items[index])
                 ~~~~~^^^^^^^
IndexError: list index out of range
```

Explanation: the first loop prints indexes 0, 1, 2. The second loop runs the index to 3, which does not exist, so it prints the valid three lines and then raises `IndexError`. The last valid index is always `len(items) - 1`, which is exactly what `range(len(items))` produces.

---

## Chapter Summary and Key Takeaways

- A data structure stores many values under one name; Python's four built-in collections are list, tuple, set and dict.
- A list is an ordered, mutable sequence of references. Items may be of any type, including other lists.
- Index from 0 (or from -1 at the end). Slices make new lists and never raise `IndexError`; a bad single index does.
- `items[i] = value` changes a list in place; strings cannot be changed this way.
- `+` joins, `*` repeats references, `in` tests membership, `len()` counts top-level items, `del` removes items by index or slice.
- `[[0] * 3] * 3` creates three references to one row; build grids with a comprehension instead.
- `+=` modifies a list in place; `a = a + b` makes a new list.

Next: [Chapter 19 — List Functions, Methods and Copying](19-list-functions-methods-and-copying.md) covers the built-in functions that work on lists, the list methods, and how copying and aliasing really behave.
