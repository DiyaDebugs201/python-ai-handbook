# Chapter 21 — Tuples

> Part 4 — Python Data Structures · Video: 6:48:42–7:18:01 · Previous: [20 List Comprehension](20-list-comprehension.md) · Next: [22 Sets](22-sets.md)

**In this chapter:** the tuple, an ordered collection that cannot be changed after it is created; how to create one (including the one-item trap), index and slice it, pack and unpack it, use it to return several values and swap variables, and decide between a tuple and a list.

**Before you start:** you need lists from [Lists in Python](18-lists-fundamentals.md#lists-in-python), indexing and slicing from [String Indexing](06-strings-basics-indexing-concatenation.md#string-indexing) and [String Slicing](07-string-slicing.md), and `for` loops from [The for Loop](17-for-loop-range-and-nested-loops.md#the-for-loop). Recap: items in a sequence have positions starting at 0; a slice `x[a:b]` takes positions `a` up to but not including `b`. Examples were run with Python 3.13.

---

## Tuples

**Timestamp:** [6:48:42](https://www.youtube.com/watch?v=J9BI0jGOds8&t=24522s)

**Learning objectives:**

- Create tuples, including empty and single-item tuples, and explain what makes a tuple.
- Explain *immutability* and what it does and does not protect.
- Index, slice, loop over, count, search and combine tuples.
- Pack and unpack tuples, including swapping and `*` unpacking.
- Choose between a tuple and a list.

**1. Intuition**

A tuple is a sealed envelope of values: you can read what is inside, but you cannot cross anything out or add anything. A date `(2026, 10, 21)`, a point `(3, 4)` and an RGB colour `(255, 128, 0)` are naturally fixed: three values that belong together as one thing. A list is a notebook you keep editing; a tuple is a printed label.

**2. Why does it exist?**

Programs need to group a small, fixed set of values and pass them around as one unit, and to be sure that nobody changes the group by accident. Because a tuple cannot change, Python can store it compactly and use it as a dictionary key or a set member (lists cannot be used that way). Functions that "return several values" actually return a tuple. The immutability also communicates intent to the reader: "these values belong together and are not going to change".

**3. Technical explanation**

*Creating.* A tuple is written with commas, and usually with round brackets: `(1, 2, 3)`. It is the *comma* that makes the tuple, not the brackets. Special cases:

- Empty tuple: `()` or `tuple()`.
- One item: `(5,)` with a trailing comma. `(5)` is just the number 5 in brackets.
- Without brackets: `a = 1, 2, 3` is a tuple (called *packing*).
- From another iterable: `tuple([1, 2])`, `tuple("abc")`.

*Immutable* means the tuple object cannot be changed after creation: no item assignment, no `append`, `remove` or `sort`. A tuple has only two methods, `count(x)` and `index(x)`. But a tuple *holds references*: if an item is itself a mutable object such as a list, that inner list can still be changed. Immutability protects the structure of the tuple, not the contents of mutable objects inside it.

*Using a tuple.* Indexing, negative indexing, slicing, `len`, `in`, `+` (makes a new tuple), `*` (repeat), looping, `min`, `max`, `sum`, `sorted` (gives a list) all work as for lists. Tuples compare item by item: `(1, 2) < (1, 3)` is `True`.

*Packing and unpacking.* Assigning several values to one name packs them into a tuple: `point = 3, 4`. Assigning a tuple to several names unpacks it: `x, y = point`. The number of names must match the number of items, unless one name has a star: `first, *rest = items` collects the remaining items into a list. A swap `a, b = b, a` works because the right side is packed into a tuple first, then unpacked.

*Tuple or list?* Use a tuple for a fixed group of values of possibly different kinds (a record, a coordinate, a function's several results). Use a list for a collection of similar items that grows, shrinks or is reordered. Tuples are also slightly smaller and faster to create.

**4. Syntax**

```text
empty = ()
single = (5,)
pair = (1, 2)
packed = 1, 2, 3
a, b = pair
first, *rest = (1, 2, 3, 4)
pair.count(1)
pair.index(2)
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
point = (3, 4)
colours = ("red", "green", "blue")
empty = ()
single = (7,)
not_a_tuple = (7)

print(point, type(point))
print(type(single), type(not_a_tuple))
print(colours[0], colours[-1], colours[1:])
print(len(colours), "green" in colours)

for colour in colours:
    print(colour.upper())

x, y = point
print(x, y)
print(point + (5,), point * 2)
print(colours.count("red"), colours.index("blue"))
```

Output:

```text
(3, 4) <class 'tuple'>
<class 'tuple'> <class 'int'>
red blue ('green', 'blue')
3 True
RED
GREEN
BLUE
3 4
(3, 4, 5) (3, 4, 3, 4)
1 2
```

Line by line:

- `(3, 4)` is a tuple, `(7,)` is a one-item tuple, and `(7)` is only the integer 7.
- Indexing, slicing, `len` and `in` work as for a list; the slice `colours[1:]` is again a tuple.
- Looping visits the items in order.
- `x, y = point` unpacks the two values into two names.
- `+` and `*` build new tuples; `count` and `index` are the only two tuple methods.

**6. Example 2 — Practical**

```python
def min_max_average(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

result = min_max_average([4, 8, 15, 16, 23, 42])
print(result)
low, high, mean = result
print(low, high, round(mean, 2))

a, b = 10, 20
a, b = b, a
print(a, b)

record = ("Asha", 21, "Chennai")
name, age, city = record
print(f"{name} is {age} and lives in {city}")

first, *middle, last = (1, 2, 3, 4, 5)
print(first, middle, last)
head, *tail = "python"
print(head, tail)

students = [("Asha", 82), ("Ravi", 67), ("Meena", 91)]
for name, score in students:
    print(f"{name}: {score}")
best = max(students, key=lambda pair: pair[1])
print("best:", best)
print(sorted(students, key=lambda pair: pair[0], reverse=True))

visits = {(0, 0): "start", (3, 4): "treasure"}
print(visits[(3, 4)])

print((1, 2) < (1, 3), (2, 0) > (1, 99), (1, 2) == (1, 2))
print(list(zip(["a", "b"], [1, 2])))
```

Output:

```text
(4, 42, 18.0)
4 42 18.0
20 10
Asha is 21 and lives in Chennai
1 [2, 3, 4] 5
p ['y', 't', 'h', 'o', 'n']
Asha: 82
Ravi: 67
Meena: 91
best: ('Meena', 91)
[('Ravi', 67), ('Meena', 91), ('Asha', 82)]
treasure
True True True
[('a', 1), ('b', 2)]
```

Line by line:

- `return min(...), max(...), ...` packs three values into one tuple. The caller can keep the tuple or unpack it into three names. This is how a Python function "returns several values" (see [Return Functions versus Void Functions](25-defining-functions-and-return-values.md#return-functions-versus-void-functions)).
- `a, b = b, a` swaps two values with no temporary variable.
- The record unpacks into three named values, which reads better than `record[0]`, `record[1]`, `record[2]`.
- `*middle` collects the items between the first and last into a list; `*tail` collects the rest of the string's characters.
- A list of tuples is a common way to hold records; the loop unpacks each tuple in the header. `max` and `sorted` use a `key` function to choose the item to compare (see [Built-in List Functions](19-list-functions-methods-and-copying.md#built-in-list-functions)).
- A tuple can be a dictionary key (see [Dictionaries](23-dictionaries.md#dictionaries)), which is handy for coordinates; a list cannot.
- Tuples compare item by item from the left, so `(1, 2) < (1, 3)` is `True`. `zip` produces tuples.

**7. Example 3 — Edge case or common mistake**

Tuples cannot be changed, and a mutable item inside can:

```python
point = (3, 4)
point[0] = 10
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 2, in <module>
    point[0] = 10
    ~~~~~^^^
TypeError: 'tuple' object does not support item assignment
```

```python
for action in [lambda: (1, 2).append(3), lambda: (1, 2).remove(1), lambda: {[1, 2]: "x"}]:
    try:
        action()
    except Exception as error:
        print(type(error).__name__ + ":", error)
```

Output:

```text
AttributeError: 'tuple' object has no attribute 'append'
AttributeError: 'tuple' object has no attribute 'remove'
TypeError: unhashable type: 'list'
```

A tuple that contains a list is only half protected:

```python
data = ("report", [1, 2])
data[1].append(3)
print(data)

try:
    data[1] += [4]
except TypeError as error:
    print("TypeError:", error)
print(data)

try:
    {data: "x"}
except TypeError as error:
    print("TypeError:", error)
```

Output:

```text
('report', [1, 2, 3])
TypeError: 'tuple' object does not support item assignment
('report', [1, 2, 3, 4])
TypeError: unhashable type: 'list'
```

The inner list changed even though the tuple is immutable. The `+=` line is a famous oddity: the list was extended in place (so the list now has 4 items), and then Python failed to assign the result back to the tuple slot, raising an error. A tuple that contains a list is also not *hashable*, so it cannot be a dictionary key.

The one-item trap and unpacking mismatches:

```python
single = (5,)
not_tuple = (5)
print(type(single).__name__, type(not_tuple).__name__)
print(type(()).__name__, type((1, 2)).__name__, len((None,)))

try:
    x, y = (1, 2, 3)
except ValueError as error:
    print("ValueError:", error)
try:
    a, b, c = (1, 2)
except ValueError as error:
    print("ValueError:", error)
```

Output:

```text
tuple int
tuple tuple 1
ValueError: too many values to unpack (expected 2)
ValueError: not enough values to unpack (expected 3, got 2)
```

The number of names must match the number of values, unless one name has a star.

**8. Common mistakes**

- Writing `(5)` instead of `(5,)` for a one-item tuple.
- Trying to assign to an item, or to call `append`, `remove` or `sort` on a tuple.
- Thinking a tuple holding a list is completely unchangeable.
- Unpacking into the wrong number of names.
- Using a list where a dictionary key is needed.
- Converting back and forth between lists and tuples when a list would have been the right choice from the start.
- Forgetting that `+` builds a new tuple (it does not change the old one).

**9. Real-world and AI applications**

Tuples appear wherever values travel together: coordinates, colours, image sizes `(height, width, channels)`, database rows, dictionary items `(key, value)`, and function results such as `(prediction, confidence)`. In machine learning code, the *shape* of an array is a tuple (for example `(32, 128)` for 32 examples with 128 features), and datasets are often lists of `(input, label)` pairs. Fixed settings, such as `("train", "validation", "test")` split names, are naturally tuples.

**10. Practice**

1. Create the tuple `(10, 20, 30, 40)`, print its length, its last item, and the slice of the middle two.
2. Create a one-item tuple containing your favourite number and show its type.
3. Unpack `("Asha", 21, "Chennai")` into three names and print them in a sentence.
4. Swap two variables without a temporary variable.
5. Write a function `circle_info(radius)` that returns the diameter and the circumference (use 3.14) as a tuple. Unpack the result.
6. Given `(1, 2, 3, 4, 5)`, use star unpacking to put the first item in `a`, the last in `c`, and the rest in `b`.
7. From `[("Asha", 82), ("Ravi", 67), ("Meena", 91)]`, print the names sorted by score from highest to lowest.
8. Explain why `t = ([1], 2)` followed by `t[0].append(5)` works, but `t[1] = 3` does not.

**11. Interview questions**

- *What is the difference between a list and a tuple?* A list can be changed after creation; a tuple cannot. Tuples can be dictionary keys (if all items are hashable).
- *How do you make a tuple with one item?* Add a trailing comma: `(5,)`.
- *Can the contents of a tuple change?* The tuple's own items cannot be replaced, but a mutable object stored in it (such as a list) can be modified.
- *What is tuple unpacking?* Assigning the items of a tuple to several names in one statement.
- *Why can a function appear to return multiple values?* It returns one tuple that the caller can unpack.

**12. Quick revision**

- Tuple: ordered, immutable, written with commas (usually in round brackets); `(5,)` for one item.
- Indexing, slicing, `len`, `in`, `+`, `*` and loops work like lists; only `count` and `index` are methods.
- Packing `t = 1, 2`; unpacking `a, b = t`; star unpacking `first, *rest = t`; swap `a, b = b, a`.
- A mutable object inside a tuple can still change.
- Use tuples for fixed groups of values and as dictionary keys.

---

## Answers to Practice Exercises

### Answers: Tuples

1.

```python
values = (10, 20, 30, 40)
print(len(values), values[-1], values[1:3])
```

Output:

```text
4 40 (20, 30)
```

2.

```python
favourite = (7,)
print(favourite, type(favourite))
```

Output:

```text
(7,) <class 'tuple'>
```

3.

```python
record = ("Asha", 21, "Chennai")
name, age, city = record
print(f"{name} is {age} years old and lives in {city}.")
```

Output:

```text
Asha is 21 years old and lives in Chennai.
```

4.

```python
first, second = "left", "right"
first, second = second, first
print(first, second)
```

Output:

```text
right left
```

5.

```python
def circle_info(radius):
    diameter = 2 * radius
    circumference = 3.14 * diameter
    return diameter, circumference


d, c = circle_info(5)
print(d, c)
print(circle_info(5))
```

Output:

```text
10 31.400000000000002
(10, 31.400000000000002)
```

6.

```python
a, *b, c = (1, 2, 3, 4, 5)
print(a, b, c)
```

Output:

```text
1 [2, 3, 4] 5
```

7.

```python
results = [("Asha", 82), ("Ravi", 67), ("Meena", 91)]
ranked = sorted(results, key=lambda pair: pair[1], reverse=True)
print([name for name, score in ranked])
```

Output:

```text
['Meena', 'Asha', 'Ravi']
```

8. `t[0].append(5)` does not change the tuple: it changes the list that the tuple holds a reference to, and the tuple still refers to the same list. `t[1] = 3` tries to replace an item of the tuple itself, which is not allowed.

```python
t = ([1], 2)
t[0].append(5)
print(t)
try:
    t[1] = 3
except TypeError as error:
    print("TypeError:", error)
```

Output:

```text
([1, 5], 2)
TypeError: 'tuple' object does not support item assignment
```

---

## Chapter Summary and Key Takeaways

- A tuple is an ordered, immutable collection written with commas; `(5,)` needs the trailing comma, and `()` is the empty tuple.
- Indexing, slicing, `len`, `in`, `+`, `*` and loops work as for lists; tuples have only the methods `count` and `index`.
- Immutability stops item assignment and structural changes, but a mutable object stored inside a tuple (a list, a dictionary) can still be modified, and such a tuple cannot be a dictionary key.
- Packing and unpacking (`a, b = b, a`, `first, *rest = items`) make swaps, multiple return values and record handling easy.
- Choose a tuple for a fixed group of related values, and a list for a changing collection of similar items.

Next: [Chapter 22 — Sets](22-sets.md) introduces the unordered collection of unique items.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
