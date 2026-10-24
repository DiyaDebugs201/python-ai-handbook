# Chapter 22 — Sets

> Part 4 — Python Data Structures · Video: 7:18:01–7:48:58 · Previous: [21 Tuples](21-tuples.md) · Next: [23 Dictionaries](23-dictionaries.md)

**In this chapter:** the set, a collection of unique items with no fixed order; how to create sets (and why `{}` is not an empty set), add and remove items, test membership quickly, remove duplicates, and combine sets with union, intersection, difference and symmetric difference; plus subset tests and `frozenset`.

**Before you start:** you need lists from [Lists in Python](18-lists-fundamentals.md#lists-in-python), list methods from [List Methods](19-list-functions-methods-and-copying.md#list-methods), tuples from [Tuples](21-tuples.md#tuples), and comprehensions from [List Comprehension](20-list-comprehension.md#list-comprehension). Recap: a list keeps items in order and allows repeats; a tuple cannot be changed, which makes it usable where a fixed value is needed. Examples were run with Python 3.13.

---

## Sets

**Timestamp:** [7:18:01](https://www.youtube.com/watch?v=J9BI0jGOds8&t=26281s)

**Learning objectives:**

- Create sets with braces and with `set()`, and explain why `{}` creates a dictionary.
- Explain what *unordered*, *unique* and *hashable* mean for sets.
- Add, remove and discard items, and test membership.
- Use a set to remove duplicates and to count distinct items.

**1. Intuition**

A set is a bag of distinct stickers: putting the same sticker in twice changes nothing, and the bag does not remember the order you put them in. All you can ask is "is this sticker in the bag?" and "how many different stickers are there?". Think of the unique visitors to a website: it does not matter how many times a person visited, or in which order, only whether they came.

**2. Why does it exist?**

Many tasks are about *membership and uniqueness*: which words occur in a text, which users have already been seen, which tags are shared by two items. With a list you would search item by item (slow for big data) and remove repeats by hand. A set stores items by their *hash* (a number computed from the value), so a membership test takes about the same time however many items there are, and duplicates are ignored automatically.

**3. Technical explanation**

- *Creating.* `{1, 2, 3}` or `set([1, 2, 3])` or `set("hello")`. The empty set must be `set()`, because `{}` is an empty *dictionary*.
- *Unique.* Adding an item that is already present does nothing.
- *Unordered.* A set has no positions: `my_set[0]` is an error, and you cannot slice it. The order in which a set is printed or looped over should not be relied on (for strings it can even change from one run of the program to the next).
- *Elements must be hashable*: numbers, strings, tuples of hashable items and `frozenset` are allowed; lists, dictionaries and other sets are not.
- *Mutable.* A set can grow and shrink: `add(x)`, `update(iterable)`, `remove(x)` (error if missing), `discard(x)` (no error if missing), `pop()` (removes an arbitrary item), `clear()`.
- *Fast membership.* `x in my_set` is fast; for a list it scans item by item.
- `len`, `min`, `max`, `sum`, `sorted` (returns a list) and `for` loops work. Sets support set comprehensions: `{n % 3 for n in range(10)}`.
- `1`, `1.0` and `True` count as the same item, because they are equal and have the same hash.
- `frozenset(iterable)` is an immutable set; it can itself be an element of another set or a dictionary key.

**4. Syntax**

```text
colours = {"red", "green"}
empty = set()
unique = set(items)
colours.add("blue")
colours.remove("red")        # KeyError if missing
colours.discard("pink")      # no error if missing
"green" in colours
len(colours)
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
colours = {"red", "green", "blue", "red"}
print(len(colours), "red" in colours, "pink" in colours)

numbers = set([3, 1, 2, 3, 3])
print(sorted(numbers), len(numbers))

letters = set("mississippi")
print(sorted(letters))

colours.add("pink")
colours.add("pink")
colours.discard("green")
colours.discard("not there")
print(sorted(colours))

print(type({}), type(set()))
print(len(set()))
```

Output:

```text
3 True False
[1, 2, 3] 3
['i', 'm', 'p', 's']
['blue', 'pink', 'red']
<class 'dict'> <class 'set'>
0
```

Line by line:

- The duplicate `"red"` is dropped: 3 items remain. Membership tests give `True` or `False`.
- A list with repeats becomes a set of distinct numbers. The sets are printed with `sorted(...)` because a set has no fixed order.
- `set("mississippi")` has one entry per distinct letter.
- Adding `"pink"` twice leaves one `"pink"`. `discard` of a missing item is silent.
- `{}` is a dictionary; `set()` is the empty set.

**6. Example 2 — Practical**

```python
visits = ["asha", "ravi", "asha", "meena", "ravi", "asha"]
unique_visitors = set(visits)
print(len(visits), "visits from", len(unique_visitors), "visitors")

seen = set()
first_time = []
for name in visits:
    if name not in seen:
        first_time.append(name)
        seen.add(name)
print(first_time)

# remove duplicates but keep the original order
print(list(dict.fromkeys(visits)))

text = "the cat sat on the mat and the dog sat on the log"
words = set(text.split())
print(len(text.split()), "words,", len(words), "distinct")
print(sorted(words))

print({len(word) for word in words})
print(sorted({word[0] for word in words}))

print(set([1, 1.0, True, 2]))
print({(1, 2), (1, 2), (2, 1)})

duplicates = []
checked = set()
for n in [4, 7, 4, 9, 7, 4]:
    if n in checked and n not in duplicates:
        duplicates.append(n)
    checked.add(n)
print(duplicates)

big = list(range(100000))
big_set = set(big)
print(99999 in big, 99999 in big_set)
```

Output:

```text
6 visits from 3 visitors
['asha', 'ravi', 'meena']
['asha', 'ravi', 'meena']
13 words, 8 distinct
['and', 'cat', 'dog', 'log', 'mat', 'on', 'sat', 'the']
{2, 3}
['a', 'c', 'd', 'l', 'm', 'o', 's', 't']
{1, 2}
{(1, 2), (2, 1)}
[4, 7]
True True
```

Line by line:

- Converting to a set counts distinct visitors. The second block does the same job by hand and keeps the order of first appearance, because a set alone would not.
- `dict.fromkeys(visits)` is a short way to remove duplicates *and* keep the order, since dictionaries remember insertion order (see [Dictionaries](23-dictionaries.md#dictionaries)).
- Splitting a text into words and making a set gives its vocabulary (the distinct words), a first step in text processing.
- Set comprehensions work like list comprehensions: the set of word lengths and the set of first letters.
- `1`, `1.0` and `True` collapse into one item because they are equal. Tuples are allowed as items, and order inside a tuple matters: `(1, 2)` and `(2, 1)` are different.
- The duplicate finder uses a set for "already seen" checks.
- The last lines show the same membership question asked of a list and of a set: the answer is identical, but the set answers without scanning (the speed difference is large for big data, though it is not timed here).

**7. Example 3 — Edge case or common mistake**

```python
colours = {"red", "green"}
print(colours[0])
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 2, in <module>
    print(colours[0])
          ~~~~~~~^^^
TypeError: 'set' object is not subscriptable
```

Other errors:

```python
for action in [lambda: {1, 2}.remove(9), lambda: {[1, 2], 3}, lambda: {1, 2}.add(3, 4),
               lambda: set(5)]:
    try:
        action()
    except Exception as error:
        print(type(error).__name__ + ":", error)
```

Output:

```text
KeyError: 9
TypeError: unhashable type: 'list'
TypeError: set.add() takes exactly one argument (2 given)
TypeError: 'int' object is not iterable
```

`remove` raises `KeyError` for a missing item (use `discard` to avoid it), lists are not hashable and cannot be elements, and an integer is not iterable, so `set(5)` fails.

The empty-braces trap and the order trap:

```python
empty = {}
print(type(empty).__name__)
empty = set()
empty.add(1)
print(empty)

s = {3, 1, 2}
print(len(s), 2 in s)
print(sorted(s), list(s) == sorted(s))
```

Output:

```text
dict
{1}
3 True
[1, 2, 3] True
```

For small integers a set often *happens* to print in ascending order, which tempts people to rely on it. Do not: the order is not guaranteed. Use `sorted(...)` whenever order matters.

Finally, `pop` removes an arbitrary item, and a set cannot be changed while looping over it:

```python
numbers = {1, 2, 3}
try:
    for n in numbers:
        numbers.add(n + 10)
except RuntimeError as error:
    print("RuntimeError:", error)
```

Output:

```text
RuntimeError: Set changed size during iteration
```

Loop over a copy (`for n in list(numbers):`) if you need to change the set while processing it.

**8. Common mistakes**

- Using `{}` for an empty set.
- Indexing or slicing a set.
- Relying on the order of a set.
- Putting lists or dictionaries into a set (not hashable); use tuples instead.
- Using `remove` on a possibly missing item (use `discard`).
- Using a set to remove duplicates when the order of the items matters.
- Forgetting that `1`, `1.0` and `True` are the same item.
- Changing a set while looping over it.

**9. Real-world and AI applications**

Sets are used to deduplicate records, to build vocabularies of distinct words, to keep track of seen items (visited pages, processed files), and to test membership quickly (a blocklist, a list of stop words). In language processing, the *vocabulary* of a dataset is a set of its distinct tokens, and checking "is this word in the vocabulary?" is a set lookup. Removing exact duplicate examples from a training dataset is another typical use, since repeated examples can distort evaluation if the same text appears in both the training and the test data.

**10. Practice**

1. Create a set from `[5, 3, 5, 1, 3, 9]` and print the number of distinct items.
2. Remove the duplicates from `["a", "b", "a", "c", "b"]` while keeping the first-seen order.
3. Show the difference between `remove` and `discard` for an item that is not in the set.
4. Count how many distinct letters are in the word `"programming"`.
5. Write a function that returns `True` if a list has any duplicate values.
6. Explain why `{}` is not an empty set, and how to create one.
7. Why can a set contain `(1, 2)` but not `[1, 2]`?

**11. Interview questions**

- *What are the properties of a set?* Unordered, no duplicates, mutable, with hashable elements.
- *Why is membership testing faster for a set than for a list?* A set uses the hash of the value to find it directly, instead of scanning from the start.
- *How do you remove duplicates from a list?* `list(set(items))` (order is lost), or `list(dict.fromkeys(items))` (order kept).
- *What is the difference between `remove` and `discard`?* `remove` raises `KeyError` if the item is missing; `discard` does not.
- *What is a `frozenset`?* An immutable set that can be used as an element of another set or as a dictionary key.

**12. Quick revision**

- `{1, 2, 3}` or `set(iterable)`; the empty set is `set()`, not `{}`.
- Unique items, no order, no indexing; elements must be hashable.
- `add`, `update`, `remove` (error), `discard` (silent), `pop` (arbitrary), `clear`.
- Fast `in` tests; great for deduplicating and counting distinct items.
- `1`, `1.0` and `True` are one item; use `sorted()` when you need an order.

---

## Set Operations

**Timestamp:** [7:28:17](https://www.youtube.com/watch?v=J9BI0jGOds8&t=26897s)

**Learning objectives:**

- Compute union, intersection, difference and symmetric difference with operators and methods.
- Test for subset, superset and disjoint sets.
- Use the update forms (`|=`, `&=`, `-=`, `^=`) and explain how they differ.
- Pick the right operation for a "both / either / only in one / not in both" question.

**1. Intuition**

Draw two overlapping circles, one for the students who study maths and one for those who study physics. *Union* is everyone inside either circle, *intersection* is the overlap, *difference* is the part of one circle outside the other, and *symmetric difference* is everything except the overlap. Set operations answer these "both, either, only, neither" questions in one line.

**2. Why does it exist?**

Comparing two collections is a constant task: which customers bought both products, which words appear in one text but not the other, which files are new since yesterday. Written with loops and `if` statements it takes many lines. The set operations state the question directly, in the same terms as mathematics, and run quickly.

**3. Technical explanation**

For sets `a` and `b`:

| Operation | Operator | Method | Meaning |
|---|---|---|---|
| Union | `a \| b` | `a.union(b)` | all items in either |
| Intersection | `a & b` | `a.intersection(b)` | items in both |
| Difference | `a - b` | `a.difference(b)` | items in `a` but not in `b` |
| Symmetric difference | `a ^ b` | `a.symmetric_difference(b)` | items in exactly one of them |
| Subset | `a <= b` | `a.issubset(b)` | every item of `a` is in `b` |
| Superset | `a >= b` | `a.issuperset(b)` | every item of `b` is in `a` |
| Disjoint | | `a.isdisjoint(b)` | nothing in common |

Details:

- These operations return a *new* set; `a` and `b` are unchanged. The in-place forms `a |= b`, `a &= b`, `a -= b`, `a ^= b` (and `update`, `intersection_update`, `difference_update`, `symmetric_difference_update`) change `a`.
- The operators need both sides to be sets. The methods accept any iterable (a list, for instance) as the argument.
- Difference is not symmetric: `a - b` and `b - a` are different. `<` and `>` test *proper* subset or superset (not equal).
- The empty set is a subset of every set.

**4. Syntax**

```text
a | b          a.union(b)
a & b          a.intersection(b)
a - b          a.difference(b)
a ^ b          a.symmetric_difference(b)
a <= b         a.issubset(b)
a >= b         a.issuperset(b)
a.isdisjoint(b)
a |= b         a.update(b)
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
maths = {"Asha", "Ravi", "Meena", "Kiran"}
physics = {"Ravi", "Kiran", "Sana"}

print(sorted(maths | physics))
print(sorted(maths & physics))
print(sorted(maths - physics))
print(sorted(physics - maths))
print(sorted(maths ^ physics))

print(sorted(maths.union(physics)) == sorted(maths | physics))
print(sorted(maths.intersection(["Ravi", "Zed"])))
print(sorted(maths))
```

Output:

```text
['Asha', 'Kiran', 'Meena', 'Ravi', 'Sana']
['Kiran', 'Ravi']
['Asha', 'Meena']
['Sana']
['Asha', 'Meena', 'Sana']
True
['Ravi']
['Asha', 'Kiran', 'Meena', 'Ravi']
```

Line by line:

- The union has everyone, the intersection only those in both, `maths - physics` only the maths-only students, and `physics - maths` the physics-only student (note that it is a different set). The symmetric difference is everyone who is in exactly one subject.
- The methods give the same results as the operators, and accept a list as the argument.
- The last line shows that none of these operations changed `maths`.

**6. Example 2 — Practical**

```python
cart_a = {"milk", "bread", "eggs", "rice"}
cart_b = {"bread", "rice", "tea"}
print("common:", sorted(cart_a & cart_b))
print("only in A:", sorted(cart_a - cart_b))
print("everything:", sorted(cart_a | cart_b))

old_files = {"a.txt", "b.txt", "c.txt"}
new_files = {"b.txt", "c.txt", "d.txt", "e.txt"}
print("added:", sorted(new_files - old_files))
print("removed:", sorted(old_files - new_files))
print("unchanged:", sorted(old_files & new_files))

text1 = "the cat sat on the mat"
text2 = "the dog sat on the log"
w1, w2 = set(text1.split()), set(text2.split())
similarity = len(w1 & w2) / len(w1 | w2)
print(sorted(w1 & w2), round(similarity, 3))

required = {"name", "email"}
provided = {"name", "email", "phone"}
print(required <= provided, provided <= required, required < provided)
print(required.isdisjoint({"phone", "age"}), required.isdisjoint({"email"}))

stop_words = {"the", "on", "and"}
print([w for w in text1.split() if w not in stop_words])

subscribers = {"a", "b", "c"}
subscribers |= {"d"}
subscribers -= {"a"}
subscribers &= {"b", "c", "d", "z"}
subscribers ^= {"c", "q"}
print(sorted(subscribers))
```

Output:

```text
common: ['bread', 'rice']
only in A: ['eggs', 'milk']
everything: ['bread', 'eggs', 'milk', 'rice', 'tea']
added: ['d.txt', 'e.txt']
removed: ['a.txt']
unchanged: ['b.txt', 'c.txt']
['on', 'sat', 'the'] 0.429
True False True
True False
['cat', 'sat', 'mat']
['b', 'd', 'q']
```

Line by line:

- The cart examples answer "what do both carts contain?", "what only A?", and "what in total?".
- Comparing two lists of file names shows which were added, removed or unchanged: a typical change-detection task.
- *Jaccard similarity* is the size of the intersection divided by the size of the union: 1 for identical word sets, 0 for no shared word. It is a simple measure of how alike two texts are.
- `required <= provided` checks that all required fields are present. `isdisjoint` asks if two sets share nothing.
- Filtering out stop words uses a set for fast membership tests.
- The in-place operators modify `subscribers` step by step: add `d`, remove `a`, keep only members of the other set, then toggle `c` and `q` (items in exactly one of the sets).

**7. Example 3 — Edge case or common mistake**

Operators need sets on both sides, while methods accept any iterable:

```python
a = {1, 2, 3}
print(a.union([3, 4]))

try:
    print(a | [3, 4])
except TypeError as error:
    print("TypeError:", error)
```

Output:

```text
{1, 2, 3, 4}
TypeError: unsupported operand type(s) for |: 'set' and 'list'
```

Difference is not symmetric, and the empty set is a subset of everything:

```python
a = {1, 2, 3}
b = {3, 4}
print(a - b, b - a, a - b == b - a)
print(set() <= a, a <= a, a < a)
print(a.isdisjoint(set()))
```

Output:

```text
{1, 2} {4} False
True True False
True
```

`a - b` and `b - a` differ. A set is a subset of itself (`<=`) but not a *proper* subset (`<`). The empty set is a subset of every set, and is disjoint from every set.

Operators do not change the operands, but the update forms do, and that can affect another name that refers to the same set:

```python
a = {1, 2}
b = a
a = a | {3}
print(a, b)

x = {1, 2}
y = x
x |= {3}
print(x, y)
```

Output:

```text
{1, 2, 3} {1, 2}
{1, 2, 3} {1, 2, 3}
```

`a = a | {3}` builds a new set and rebinds `a`; `x |= {3}` changes the shared set, so `y` sees it too (the same behaviour as with lists, see [Copying Lists](19-list-functions-methods-and-copying.md#copying-lists)). Use `.copy()` for an independent set.

Also remember the precedence of the operators: `&` binds tighter than `^`, which binds tighter than `|`, and `-` binds tighter than all three. Use brackets when mixing them:

```python
a, b, c = {1, 2}, {2, 3}, {3, 4}
print(a | b & c)
print((a | b) & c)
```

Output:

```text
{1, 2, 3}
{3}
```

**8. Common mistakes**

- Using `+` on sets (not supported); use `|`.
- Using the operators with a list on one side (use the methods).
- Mixing up `a - b` and `b - a`.
- Confusing `^` (symmetric difference) with `|` (union).
- Forgetting that `<` is a *proper* subset test.
- Using `|=` or `update` when the original set must remain unchanged.
- Mixing set operators without brackets and misreading the precedence.

**9. Real-world and AI applications**

Set operations compare collections: customers who bought both products (intersection), users who have not yet been emailed (difference), the combined vocabulary of two corpora (union), differences between two versions of a dataset, and overlap between predicted and true labels. In evaluation of retrieval systems, the overlap between the documents a system returned and the documents that were truly relevant is an intersection; precision and recall are sizes of these sets divided by the sizes of the returned and relevant sets. Jaccard similarity, shown above, is also used to find near-duplicate documents.

**10. Practice**

1. For `{1, 2, 3, 4}` and `{3, 4, 5, 6}`, print the union, intersection, both differences, and the symmetric difference.
2. Find the words that appear in both `"red green blue"` and `"blue yellow red"`.
3. Given two lists of email addresses, print the addresses that are in the first list but not the second.
4. Check whether `{"a", "b"}` is a subset of `{"a", "b", "c"}`, and whether it is a proper subset of itself.
5. Compute the Jaccard similarity of the letter sets of `"listen"` and `"silent"`, and of `"hello"` and `"world"`.
6. Explain the difference between `s = s | {5}` and `s |= {5}` when another name refers to `s`.
7. What does `{1, 2, 3} ^ {3, 4}` give, and how would you calculate it using only `|`, `&` and `-`?

**11. Interview questions**

- *What does `a & b` return?* A new set of the items in both `a` and `b`.
- *What is the difference between `a - b` and `a ^ b`?* `a - b` keeps items only in `a`; `a ^ b` keeps items in exactly one of the two sets.
- *Do set operators modify their operands?* No, but the update forms (`|=`, `&=`, `-=`, `^=`) do.
- *How do you check if one set contains all the items of another?* `a >= b` or `a.issuperset(b)`.
- *Can `|` take a list as one side?* No; the method `union` accepts any iterable.

**12. Quick revision**

- `|` union, `&` intersection, `-` difference, `^` symmetric difference.
- `<=` subset, `>=` superset, `<` and `>` proper; `isdisjoint()` for no overlap.
- Operators return new sets; `|=`, `&=`, `-=`, `^=` change in place.
- Methods accept any iterable; operators need sets.
- `a - b` is not the same as `b - a`.

---

## Answers to Practice Exercises

### Answers: Sets

1.

```python
values = {5, 3, 5, 1, 3, 9}
print(len(values), sorted(values))
```

Output:

```text
4 [1, 3, 5, 9]
```

2.

```python
items = ["a", "b", "a", "c", "b"]
print(list(dict.fromkeys(items)))

seen = set()
result = []
for item in items:
    if item not in seen:
        seen.add(item)
        result.append(item)
print(result)
```

Output:

```text
['a', 'b', 'c']
['a', 'b', 'c']
```

3.

```python
s = {1, 2}
s.discard(9)
print("discard ok:", sorted(s))
try:
    s.remove(9)
except KeyError as error:
    print("KeyError:", error)
```

Output:

```text
discard ok: [1, 2]
KeyError: 9
```

4.

```python
print(len(set("programming")), sorted(set("programming")))
```

Output:

```text
8 ['a', 'g', 'i', 'm', 'n', 'o', 'p', 'r']
```

5.

```python
def has_duplicates(values):
    return len(set(values)) != len(values)


print(has_duplicates([1, 2, 3]), has_duplicates([1, 2, 1]), has_duplicates([]))
```

Output:

```text
False True False
```

6. `{}` is the literal for an empty dictionary, because dictionaries were written with braces first. Make an empty set with `set()`:

```python
print(type({}).__name__, type(set()).__name__)
```

Output:

```text
dict set
```

7. Set elements must be hashable, which requires the value to be immutable. A tuple of numbers is hashable; a list is mutable and is not.

```python
print({(1, 2)})
try:
    print({[1, 2]})
except TypeError as error:
    print("TypeError:", error)
```

Output:

```text
{(1, 2)}
TypeError: unhashable type: 'list'
```

### Answers: Set Operations

1.

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(sorted(a | b), sorted(a & b), sorted(a - b), sorted(b - a), sorted(a ^ b))
```

Output:

```text
[1, 2, 3, 4, 5, 6] [3, 4] [1, 2] [5, 6] [1, 2, 5, 6]
```

2.

```python
first = set("red green blue".split())
second = set("blue yellow red".split())
print(sorted(first & second))
```

Output:

```text
['blue', 'red']
```

3.

```python
list_a = ["x@mail.com", "y@mail.com", "z@mail.com"]
list_b = ["y@mail.com", "w@mail.com"]
print(sorted(set(list_a) - set(list_b)))
```

Output:

```text
['x@mail.com', 'z@mail.com']
```

4.

```python
small = {"a", "b"}
print(small <= {"a", "b", "c"}, small < small, small <= small)
```

Output:

```text
True False True
```

5.

```python
def jaccard(first, second):
    a, b = set(first), set(second)
    return len(a & b) / len(a | b)


print(jaccard("listen", "silent"), round(jaccard("hello", "world"), 3))
```

Output:

```text
1.0 0.286
```

`"listen"` and `"silent"` use exactly the same letters, so the similarity is 1.0. `"hello"` and `"world"` share `l` and `o` out of 7 distinct letters.

6.

```python
s = {1}
t = s
s = s | {5}
print(s, t)

s = {1}
t = s
s |= {5}
print(s, t)
```

Output:

```text
{1, 5} {1}
{1, 5} {1, 5}
```

The first form builds a new set and rebinds `s`; `t` still refers to the old set. The second changes the shared set in place, so `t` also shows the new item.

7. The result is `{1, 2, 4}`: the items in exactly one set. With only `|`, `&` and `-`: union minus intersection.

```python
a, b = {1, 2, 3}, {3, 4}
print(a ^ b, (a | b) - (a & b), (a - b) | (b - a))
```

Output:

```text
{1, 2, 4} {1, 2, 4} {1, 2, 4}
```

---

## Chapter Summary and Key Takeaways

- A set stores unique, hashable items with no order and no indexing; the empty set is `set()`, because `{}` is an empty dictionary.
- `add`, `update`, `remove` (raises `KeyError`), `discard` (silent), `pop` and `clear` change a set; `in` tests are fast.
- Sets remove duplicates and count distinct items, but lose the order (use `dict.fromkeys` when order matters), and `1`, `1.0` and `True` are the same item.
- `|`, `&`, `-`, `^` give union, intersection, difference and symmetric difference as new sets; `<=`, `>=` and `isdisjoint` compare them; the in-place forms (`|=`, `&=`, `-=`, `^=`) modify the original.
- Operators need sets on both sides, while the methods accept any iterable; the order of items in a set must never be relied on.

Next: [Chapter 23 — Dictionaries](23-dictionaries.md) introduces the key-to-value mapping.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
