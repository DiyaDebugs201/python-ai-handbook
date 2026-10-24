# Chapter 17 — for Loops, range() and Nested Loops

> Part 3 — Operators and Control Flow · Video: 4:48:36–5:33:56 · Previous: [16 while Loops and Loop Control](16-while-loop-and-loop-control.md) · Next: [18 Data Structures Introduction and Lists](18-lists-fundamentals.md)

**In this chapter:** how to visit every item of a sequence with `for`, how `range()` produces numbers on demand, how to combine the two for counted loops, and how to place one loop inside another to work with rows and columns, patterns and combinations.

**Before you start:** you need the `while` loop and `break`/`continue` from [while Loops and Loop Control](16-while-loop-and-loop-control.md), strings and indexing from [String Indexing](06-strings-basics-indexing-concatenation.md#string-indexing), and `print(..., end=" ")` from [Built-in Functions](03-builtin-functions-print-and-modules.md). Recap: a string is a sequence of characters; `end=" "` replaces the newline that `print` normally adds. Examples were run with Python 3.13.

---

## The for Loop

**Timestamp:** [4:48:36](https://www.youtube.com/watch?v=J9BI0jGOds8&t=17316s)

**Learning objectives:**

- Explain what an iterable is and how `for` takes items from it one at a time.
- Loop over strings, lists, tuples, dictionaries and ranges.
- Use `enumerate()` and `zip()` instead of manual index counters.
- Use `break`, `continue` and `else` in a `for` loop.

**1. Intuition**

A `for` loop is "do this for each item": for each plate in the stack, wash it; for each name on the guest list, write a card. You do not count the plates or keep a counter. The loop hands you the next item until there are none left.

**2. Why does it exist?**

Most repeated work in programs is "do something with every element of a collection": print each line of a file, add each price, check each word. A `while` loop can do this, but you must manage an index, test the length and update the counter yourself, and each of those is a place for a bug. The `for` loop does the bookkeeping for you.

**3. Technical explanation**

`for name in iterable:` works like this:

1. Python asks the *iterable* (anything that can produce items one by one: a string, list, tuple, set, dictionary, range, file, and so on) for an *iterator*.
2. Each round, it takes the next item from the iterator and binds it to the loop variable (`name`), then runs the body.
3. When the iterator has no more items, the loop ends and the program continues after the block.

Details worth knowing:

- The loop variable is an ordinary variable. It is not deleted after the loop, so it keeps the last item (and stays undefined if the iterable was empty).
- Looping over a string gives characters; over a list or tuple gives elements in order; over a dictionary gives its keys (use `.items()` for key and value pairs); over a set gives elements in no guaranteed order.
- `enumerate(items, start=0)` gives `(index, item)` pairs. `zip(a, b)` walks two iterables together and stops at the shorter one.
- `break`, `continue` and `else` behave as in `while` loops (see [The break Statement](16-while-loop-and-loop-control.md#the-break-statement)).
- Do not add or remove items from a list while looping over it; the loop can skip items. Loop over a copy, or build a new list instead.

**4. Syntax**

```text
for variable in iterable:
    body_statements
else:
    statements_run_if_the_loop_was_not_ended_by_break
```

This is a pattern, not runnable code. The colon is required and the body is indented. The `else` part is optional.

**5. Example 1 — Basic**

```python
for letter in "cat":
    print(letter)

for fruit in ["apple", "banana", "cherry"]:
    print("I like", fruit)

total = 0
for price in (120, 80, 45):
    total += price
print("Total:", total)

for key in {"a": 1, "b": 2}:
    print("key:", key)
```

Output:

```text
c
a
t
I like apple
I like banana
I like cherry
Total: 245
key: a
key: b
```

Line by line:

- The first loop gives one character per round. The second gives the elements of a list, and the third those of a tuple, which are added into the accumulator `total`.
- Looping over a dictionary gives its keys, in the order they were inserted.

**6. Example 2 — Practical**

```python
names = ["Asha", "Ravi", "Meena"]
scores = [82, 67, 91]

for index, name in enumerate(names, start=1):
    print(index, name)

for name, score in zip(names, scores):
    grade = "pass" if score >= 70 else "retry"
    print(f"{name:<6}{score:>4}  {grade}")

marks = {"maths": 88, "physics": 75, "chemistry": 69}
for subject, mark in marks.items():
    print(subject, "->", mark)

text = "Python is fun and Python is easy"
vowels = 0
for ch in text.lower():
    if ch in "aeiou":
        vowels += 1
print("vowels:", vowels)

for word in text.split():
    if word == "fun":
        print("found 'fun'")
        break
else:
    print("'fun' not found")
```

Output:

```text
1 Asha
2 Ravi
3 Meena
Asha    82  pass
Ravi    67  retry
Meena   91  pass
maths -> 88
physics -> 75
chemistry -> 69
vowels: 8
found 'fun'
```

Line by line:

- `enumerate(names, start=1)` supplies a counter starting at 1, so there is no need for a separate `i = 0` and `i += 1`.
- `zip(names, scores)` pairs the n-th name with the n-th score. Two names in the loop header unpack each pair (see [Tuples](21-tuples.md#tuples)). The `{name:<6}` and `{score:>4}` parts are alignment settings from [String Formatting and f-Strings](09-string-formatting-and-f-strings.md).
- `marks.items()` gives key and value together.
- The vowel loop is the counter pattern: start at 0, add 1 when a condition is true.
- The last loop searches the words and uses `break`; the loop `else` runs only when no word matched.

**7. Example 3 — Edge case or common mistake**

An empty iterable means the body never runs, and the loop variable is not created:

```python
for item in []:
    print("never printed")
print("loop over empty list done")
print(item)
```

Output:

```text
loop over empty list done
Traceback (most recent call last):
  File "example.py", line 4, in <module>
    print(item)
          ^^^^
NameError: name 'item' is not defined. Did you mean: 'iter'?
```

Changing a list while looping over it skips items, because the loop walks by position:

```python
numbers = [1, 2, 3, 4, 5, 6]
for n in numbers:
    if n % 2 == 0:
        numbers.remove(n)
print(numbers)

numbers = [1, 2, 3, 4, 5, 6]
odds = [n for n in numbers if n % 2 != 0]
print(odds)

numbers = [1, 2, 3, 4, 5, 6]
for n in numbers[:]:
    if n % 2 == 0:
        numbers.remove(n)
print(numbers)
```

Output:

```text
[1, 3, 5]
[1, 3, 5]
[1, 3, 5]
```

The first version happens to give the right answer here, only because no two even numbers are next to each other. With `[2, 4, 6, 8]` it would leave `[4, 8]` (see the answer to practice exercise 6).  The safe versions are to build a new list (a comprehension, see [List Comprehension](20-list-comprehension.md#list-comprehension)) or to loop over a copy (`numbers[:]`).

Strings cannot be changed in place, and a `for` loop over a number is an error:

```python
for digit in 12345:
    print(digit)
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 1, in <module>
    for digit in 12345:
                 ^^^^^
TypeError: 'int' object is not iterable
```

An integer is not iterable. Convert it first (`str(12345)`) or use `range`.

**8. Common mistakes**

- Forgetting the colon or the indentation of the body.
- Trying to loop over an integer instead of `range(n)` or `str(n)`.
- Removing from or adding to a list while looping over it.
- Using `range(len(items))` and indexing when `for item in items` is enough (or `enumerate` when the index is also needed).
- Using the loop variable after an empty loop.
- Assuming a set or dictionary is looped in sorted order (sets have no guaranteed order; dictionaries keep insertion order).
- Reusing the loop variable name for something else inside the body.

**9. Real-world and AI applications**

A `for` loop is how programs process every row of a file, every image in a folder, every message in a conversation, every document in a collection. In AI work you loop over a list of training examples, over batches of data, over the chunks of a text before sending them to an embedding model, and over the tool calls a model asks for. Counting, summing, filtering and searching are all `for` loops with an accumulator or a condition.

**10. Practice**

1. Print each character of your name on its own line.
2. Given `prices = [250, 99, 400, 75]`, print the sum and the largest price using a loop (not `sum` or `max`).
3. Use `enumerate` to print `1. tea`, `2. coffee`, `3. milk` from a list of drinks.
4. Use `zip` to combine `["a", "b", "c"]` and `[1, 2, 3]` into lines like `a=1`.
5. Count how many words in a sentence have more than four letters.
6. Why does removing items from a list during a `for` loop over the same list give wrong results? Show a safe alternative.

**11. Interview questions**

- *What is an iterable?* An object that can give its items one at a time, such as a list, string, tuple, dictionary, set, range or file.
- *What does looping over a dictionary give?* Its keys; use `.items()` for pairs or `.values()` for values.
- *When would you use `enumerate`?* When you need both the position and the item.
- *What does `zip` do when the lists have different lengths?* It stops at the shortest one.
- *Is the loop variable available after the loop?* Yes, with the last value, unless the iterable was empty.

**12. Quick revision**

- `for item in iterable:` visits each item in turn; no counter is needed.
- Strings give characters, dictionaries give keys.
- `enumerate` for index and item; `zip` for parallel lists.
- `break`, `continue` and `else` work as in `while`.
- Never modify a list while looping over it; loop over a copy or build a new list.

---

## The range() Function

**Timestamp:** [5:00:29](https://www.youtube.com/watch?v=J9BI0jGOds8&t=18029s)

**Learning objectives:**

- Use `range(stop)`, `range(start, stop)` and `range(start, stop, step)`.
- Explain why `stop` is excluded and how negative steps work.
- Describe what kind of object `range` is and why it is memory-friendly.

**1. Intuition**

`range` is a number ruler: it tells Python "the numbers from here up to (but not including) there, stepping by this much". It does not write the numbers out in advance; it can produce each one when asked, like a ticket machine that prints the next number only when someone pulls.

**2. Why does it exist?**

Counted loops need a sequence of numbers: 0 to 9, 1 to 100, every second number, 10 down to 1. Typing such lists by hand is tedious and impossible for large ranges. `range` describes the sequence in a few characters and stores almost nothing.

**3. Technical explanation**

`range` has three forms:

- `range(stop)` gives 0, 1, ..., `stop - 1`.
- `range(start, stop)` gives `start`, ..., `stop - 1`.
- `range(start, stop, step)` moves by `step` each time. A negative step counts down, and then `start` must be larger than `stop`.

Rules:

- All arguments must be integers. `range(2.5)` is a `TypeError`.
- `stop` is never included. The number of items in `range(a, b)` is `b - a` (when `b > a`).
- `step` cannot be 0 (`ValueError`).
- If the range cannot move from `start` toward `stop`, it is empty, with no error.
- A `range` is its own type, a lazy sequence: it stores only `start`, `stop` and `step`, and can be indexed, sliced, measured with `len()`, and tested with `in`. Use `list(range(5))` to see the numbers.

The "up to but not including" rule matches slicing (see [String Slicing](07-string-slicing.md)) and makes the length easy: `range(0, n)` has exactly `n` items, and `range(a, b)` followed by `range(b, c)` has no overlap and no gap.

**4. Syntax**

```text
range(stop)
range(start, stop)
range(start, stop, step)
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
print(list(range(5)))
print(list(range(2, 8)))
print(list(range(0, 20, 5)))
print(list(range(10, 0, -3)))
print(list(range(5, 5)))
print(list(range(5, 2)))
print(type(range(3)))
```

Output:

```text
[0, 1, 2, 3, 4]
[2, 3, 4, 5, 6, 7]
[0, 5, 10, 15]
[10, 7, 4, 1]
[]
[]
<class 'range'>
```

Line by line:

- `range(5)` starts at 0 and stops before 5. `range(2, 8)` starts at 2 and stops before 8.
- `range(0, 20, 5)` steps by 5; 20 is not included.
- `range(10, 0, -3)` counts down by 3 and stops before reaching 0.
- `range(5, 5)` and `range(5, 2)` are empty: no numbers lie between the endpoints in the direction of the step, and there is no error.

**6. Example 2 — Practical**

```python
r = range(1, 100, 2)
print(len(r), r[0], r[-1], 51 in r, 52 in r)
print(r[:5], list(r[:5]))

print(sum(range(1, 101)))
print(list(range(100, 0, -25)))

big = range(10**12)
print(len(big))
print(big[999999999999])

print(list(range(-3, 3)))
print([n * n for n in range(1, 6)])
```

Output:

```text
50 1 99 True False
range(1, 11, 2) [1, 3, 5, 7, 9]
5050
[100, 75, 50, 25]
1000000000000
999999999999
[-3, -2, -1, 0, 1, 2]
[1, 4, 9, 16, 25]
```

Line by line:

- The range of odd numbers has 50 items. Indexing, negative indexing and `in` all work. Slicing a range gives another range (not a list).
- `sum(range(1, 101))` adds 1 to 100 without writing out the list.
- A range of a trillion numbers is created instantly and has a length, because only the three numbers `start`, `stop`, `step` are stored. Making `list(big)` would exhaust memory, so it is not done here.
- Ranges may include negative numbers. The last line shows a list comprehension over a range, which is common.

**7. Example 3 — Edge case or common mistake**

```python
for value in [lambda: range(2.5), lambda: range(0, 10, 0), lambda: range("5")]:
    try:
        value()
    except Exception as error:
        print(type(error).__name__ + ":", error)

print(list(range(1, 6)), "has", len(range(1, 6)), "items")
print(list(range(1, 10, 3)))
```

Output:

```text
TypeError: 'float' object cannot be interpreted as an integer
ValueError: range() arg 3 must not be zero
TypeError: 'str' object cannot be interpreted as an integer
[1, 2, 3, 4, 5] has 5 items
[1, 4, 7]
```

`range` rejects floats and a zero step. For decimal steps, compute values from an integer counter: `[i * 0.25 for i in range(5)]`.

A very common mistake is the off-by-one on the upper bound: to include 10, write `range(1, 11)`, not `range(1, 10)`:

```python
print(list(range(1, 10)))
print(list(range(1, 11)))
print([i * 0.25 for i in range(5)])
print(list(range(10, 0)))
print(list(range(10, 0, -1)))
```

Output:

```text
[1, 2, 3, 4, 5, 6, 7, 8, 9]
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
[0.0, 0.25, 0.5, 0.75, 1.0]
[]
[10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
```

The fourth line shows another mistake: counting down without a negative step gives an empty range.

**8. Common mistakes**

- Expecting the `stop` value to be included.
- Using floats as arguments.
- Counting down without a negative step (`range(10, 0)` is empty).
- Using a step of 0.
- Printing a `range` and expecting a list (`print(range(5))` shows `range(0, 5)`).
- Converting a huge range to a list and running out of memory.

**9. Real-world and AI applications**

`range` provides the counters for loops, the indices of items, the batch positions in a dataset (`range(0, len(data), batch_size)` steps through the data one batch at a time), the epoch numbers in a training loop, and the positions of tokens in a text. Because it is lazy, it can describe millions of positions without storing them.

**10. Practice**

1. Print `list(range(...))` for: 0 to 9, 5 to 15, even numbers up to 20, 50 down to 10 in steps of 10.
2. Without running it, say how many items `range(3, 30, 4)` has, then check with `len`.
3. Print the multiples of 7 from 7 to 70.
4. What is the result of `list(range(10, 1))`? How do you make it count down?
5. Print the numbers 1 to 5 as `0.5, 1.0, 1.5, ...` (multiples of 0.5) using `range` for the counter.
6. Check whether 97 is in `range(1, 100, 3)` without making a list.

**11. Interview questions**

- *Is the `stop` value included in `range`?* No.
- *Is `range` a list?* No, it is a lazy sequence type that stores only start, stop and step.
- *What does `range(5, 0)` produce?* An empty range, because the default step is +1.
- *Can `range` take float arguments?* No; use an integer counter and multiply.

**12. Quick revision**

- `range(stop)`, `range(start, stop)`, `range(start, stop, step)`.
- The stop value is excluded; `len(range(a, b))` is `b - a`.
- Negative step counts down.
- Integers only; step cannot be 0.
- Lazy: cheap in memory, supports `len`, indexing, slicing and `in`.

---

## The for Loop with range()

**Timestamp:** [5:15:08](https://www.youtube.com/watch?v=J9BI0jGOds8&t=18908s)

**Learning objectives:**

- Write counted loops with `for ... in range(...)`.
- Choose between looping over items and looping over indices.
- Apply the accumulator, counter, maximum/minimum and search patterns.

**1. Intuition**

When you know *how many times* to repeat, you ask `range` for that many numbers and let `for` use them one at a time. It is like a coach saying "ten push-ups" instead of "keep going until you are tired".

**2. Why does it exist?**

Counted repetition is everywhere: print a table, add the numbers 1 to n, build a pattern, try each candidate, process positions in a list. Combining `for` with `range` expresses the count, the start and the step in the loop header, so the body can concentrate on the work.

**3. Technical explanation**

`for i in range(a, b, step):` runs the body once for each number produced by the range, with `i` holding that number. There is no separate initialise/test/update, because the loop header does all three. Compare with the equivalent `while`:

- `for i in range(5):` is the same as `i = 0`, `while i < 5:`, body, `i += 1`, but shorter and impossible to make infinite.
- Changing `i` inside the body does not change the next value: the next round takes the next number from the range regardless.
- If the loop variable is not needed (only the count matters), the convention is to name it `_`.
- Prefer `for item in items` when you only need items. Use `range(len(items))` only when you need the positions for something else (for example to compare neighbours); `enumerate` is often better.

Common patterns:

- *Accumulator*: `total = 0` before, `total += value` inside.
- *Counter*: `count = 0` before, `count += 1` when a condition holds.
- *Maximum*: start with the first value, replace it when a larger one appears.
- *Search*: loop until a match, `break` when found.
- *Build a result*: start with an empty list or string, add to it each round.

**4. Syntax**

```text
for i in range(n):              # n times, i = 0..n-1
for i in range(1, n + 1):       # i = 1..n
for i in range(a, b, step):     # custom start, stop, step
for _ in range(n):              # only the count matters
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
for i in range(5):
    print("i is", i)

for i in range(1, 6):
    print(i, "squared is", i * i)

for i in range(10, 0, -2):
    print(i, end=" ")
print()

for _ in range(3):
    print("hello")

for i in range(3):
    i = i * 10
    print("inside:", i)
```

Output:

```text
i is 0
i is 1
i is 2
i is 3
i is 4
1 squared is 1
2 squared is 4
3 squared is 9
4 squared is 16
5 squared is 25
10 8 6 4 2 
hello
hello
hello
inside: 0
inside: 10
inside: 20
```

Line by line:

- `range(5)` gives five rounds, numbered 0 to 4. `range(1, 6)` gives 1 to 5.
- `range(10, 0, -2)` counts down by 2 and stops before 0.
- The loop with `_` repeats three times and ignores the number.
- In the last loop, assigning to `i` changes it only for the rest of that round; the next round still gets 1 and then 2 from the range.

**6. Example 2 — Practical**

```python
n = 5
print("Multiplication table of", n)
for i in range(1, 11):
    print(f"{n} x {i:>2} = {n * i:>3}")

total = 0
for i in range(1, 101):
    total += i
print("Sum 1..100:", total)

factorial = 1
for i in range(2, 8):
    factorial *= i
print("7! =", factorial)

numbers = [14, 3, 27, 9, 21]
largest = numbers[0]
for i in range(1, len(numbers)):
    if numbers[i] > largest:
        largest = numbers[i]
print("largest:", largest)

increases = 0
values = [3, 5, 4, 8, 9, 2]
for i in range(1, len(values)):
    if values[i] > values[i - 1]:
        increases += 1
print("increases:", increases)

word = "level"
is_palindrome = True
for i in range(len(word) // 2):
    if word[i] != word[-1 - i]:
        is_palindrome = False
        break
print(word, "is a palindrome:", is_palindrome)

balance = 1000
for year in range(1, 4):
    balance *= 1.05
    print(f"year {year}: {balance:.2f}")
```

Output:

```text
Multiplication table of 5
5 x  1 =   5
5 x  2 =  10
5 x  3 =  15
5 x  4 =  20
5 x  5 =  25
5 x  6 =  30
5 x  7 =  35
5 x  8 =  40
5 x  9 =  45
5 x 10 =  50
Sum 1..100: 5050
7! = 5040
largest: 27
increases: 3
level is a palindrome: True
year 1: 1050.00
year 2: 1102.50
year 3: 1157.62
```

Line by line:

- The multiplication table uses the loop variable twice and formats it with width settings so the columns align.
- The sum and factorial are accumulators; the factorial starts at 1 because it is a product, not a sum.
- The maximum starts at the first element and examines the rest, so the loop starts at index 1.
- Comparing `values[i]` with `values[i - 1]` needs positions, which is a good use of `range(len(...))`.
- The palindrome check compares the first half with the mirrored positions, and stops early on a mismatch.
- The savings loop applies 5% growth for three years, printing each year.

**7. Example 3 — Edge case or common mistake**

```python
numbers = [10, 20, 30]
for i in range(1, len(numbers) + 1):
    print(numbers[i])
```

Output:

```text
20
30
Traceback (most recent call last):
  File "example.py", line 3, in <module>
    print(numbers[i])
          ~~~~~~~^^^
IndexError: list index out of range
```

The range went one step too far: valid indices are 0 to `len - 1`. Use `range(len(numbers))` for all positions, or loop over the items directly.

Other edge cases:

```python
for i in range(0):
    print("never")
print("after empty range")

for i in range(3):
    pass
print("last i:", i)

items = ["a", "b", "c"]
for i in range(len(items)):
    print(i, items[i])
for i, item in enumerate(items):
    print(i, item)
```

Output:

```text
after empty range
last i: 2
0 a
1 b
2 c
0 a
1 b
2 c
```

`range(0)` is empty. The loop variable keeps the last value. The two versions at the bottom produce the same result, but `enumerate` is shorter and cannot go out of range.

**8. Common mistakes**

- Off-by-one in the bounds (`range(1, n)` when `n` should be included).
- Indexing past the end: `range(len(x) + 1)`.
- Expecting changes to the loop variable inside the body to affect the next round.
- Writing `range(len(items))` for a loop that only needs the items.
- Starting an accumulator at the wrong value (0 for a sum, 1 for a product).
- Starting the maximum search at 0 when all numbers may be negative; start from the first element.

**9. Real-world and AI applications**

Counted loops generate tables and test data, repeat an experiment a fixed number of times, step through a dataset in batches, and run training for a fixed number of epochs (`for epoch in range(epochs):`). A typical batch loop looks like `for start in range(0, len(data), batch_size): batch = data[start:start + batch_size]`, which uses the three-argument `range` and slicing together.

**10. Practice**

1. Print the squares of 1 to 10, each on its own line.
2. Print the sum of all even numbers from 1 to 100.
3. Print a multiplication table for a number of your choice, from 1 to 12.
4. Compute 10! with a `for` loop.
5. Given `[4, -2, 9, 0, -7]`, count the negatives and print the minimum, using `range(len(...))`.
6. Split `list(range(10))` into batches of 4 with `range(0, 10, 4)` and slicing.
7. Print the first ten terms of the Fibonacci sequence (1, 1, 2, 3, 5, ...).

**11. Interview questions**

- *What is the difference between `range(n)` and `range(1, n + 1)`?* The first gives 0 to n-1; the second gives 1 to n.
- *If you change the loop variable inside the body, does the next round change?* No; the next value comes from the range.
- *When do you use `_` as a loop variable?* When the value is not needed.
- *Is `for i in range(len(x))` good style?* Only when you need the index; otherwise loop over the items or use `enumerate`.

**12. Quick revision**

- `for i in range(n)` repeats `n` times with `i` from 0 to n-1.
- `range(1, n + 1)` for 1 to n; a negative step to count down.
- Accumulator, counter, maximum, search and build patterns.
- Valid indices are `0` to `len - 1`.
- Use `_` if the counter value is unused.

---

## Nested Loops

**Timestamp:** [5:20:55](https://www.youtube.com/watch?v=J9BI0jGOds8&t=19255s)

**Learning objectives:**

- Explain how a loop inside a loop runs, and count the total rounds.
- Print rectangles, triangles and tables with nested `for` loops.
- Use nested loops for grids, combinations and comparisons of every pair.
- Recognise the cost of nested loops on large data.

**1. Intuition**

A clock: for each hour, the minute hand goes round completely. The outer loop is the hour hand and moves slowly; the inner loop is the minute hand and runs all of its steps for every single step of the outer one. A grid of seats is the same: for each row, go through each seat in that row.

**2. Why does it exist?**

Many problems have two (or more) dimensions: rows and columns of a table, pairs of items, every start point with every end point, every pixel of an image. One loop gives one dimension; a second loop inside it gives the second.

**3. Technical explanation**

When a loop is placed inside another loop's body, the *inner* loop starts afresh and runs to completion for each round of the *outer* loop. If the outer loop runs `a` times and the inner loop `b` times, the inner body runs `a * b` times.

Points to remember:

- Use different names for the loop variables (`row`, `column`, not `i` twice).
- The inner loop's range may depend on the outer variable (`range(row + 1)` gives a triangle).
- `break` and `continue` affect only the innermost loop (see [The break Statement](16-while-loop-and-loop-control.md#the-break-statement)).
- `print(..., end="")` keeps output on one line; an empty `print()` after the inner loop ends the line.
- Work grows quickly: two nested loops over `n` items do about `n * n` steps. 1,000 items give a million; 100,000 give ten billion. Be careful with nested loops over big data.

**4. Syntax**

```text
for outer in outer_iterable:
    for inner in inner_iterable:
        body_statements
    statements_after_inner_loop
```

This is a pattern, not runnable code. The inner `for` is indented one level under the outer one, and its body one level further.

**5. Example 1 — Basic**

```python
for row in range(3):
    for column in range(4):
        print("*", end=" ")
    print()

print()

for row in range(1, 5):
    for column in range(row):
        print("*", end=" ")
    print()

print()

for a in range(1, 4):
    for b in range(1, 4):
        print(f"{a}x{b}={a * b}", end="  ")
    print()
```

Output:

```text
* * * * 
* * * * 
* * * * 

* 
* * 
* * * 
* * * * 

1x1=1  1x2=2  1x3=3  
2x1=2  2x2=4  2x3=6  
3x1=3  3x2=6  3x3=9  
```

Line by line:

- The first pair of loops prints a rectangle of 3 rows and 4 columns: for every row, the inner loop prints 4 stars and `print()` ends the line.
- In the triangle, the inner range is `range(row)`, so row 1 has 1 star, row 2 has 2, and so on.
- The last block prints a small multiplication grid: 3 times 3 equals 9 products.

**6. Example 2 — Practical**

```python
size = 4
for row in range(1, size + 1):
    print(" " * (size - row) + "*" * (2 * row - 1))

print()

for row in range(1, 5):
    print(" ".join(str(n) for n in range(1, row + 1)))

print()

colours = ["red", "blue"]
sizes = ["S", "M", "L"]
count = 0
for colour in colours:
    for size_name in sizes:
        count += 1
        print(count, colour, size_name)

print()

numbers = [2, 7, 11, 15]
target = 18
for i in range(len(numbers)):
    for j in range(i + 1, len(numbers)):
        if numbers[i] + numbers[j] == target:
            print("pair:", numbers[i], numbers[j])

grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
total = 0
for row in grid:
    for value in row:
        total += value
print("grid total:", total)
```

Output:

```text
   *
  ***
 *****
*******

1
1 2
1 2 3
1 2 3 4

1 red S
2 red M
3 red L
4 blue S
5 blue M
6 blue L

pair: 7 11
grid total: 45
```

Line by line:

- The pyramid pads each row with spaces and prints an odd number of stars (`2 * row - 1`). It uses string repetition (`"*" * 3`) so only one loop is needed, with the inner loop hidden inside the `*` operator.
- The number triangle uses `join` to put spaces between numbers (see [String Methods](10-ord-chr-and-string-methods.md)).
- The colour and size loops produce every combination: 2 x 3 = 6 lines.
- The pair search starts the inner loop at `i + 1` so that each pair is tested once and no number is paired with itself.
- The grid is a list of lists (see [Lists: Fundamentals](18-lists-fundamentals.md)): the outer loop takes each row (a list), and the inner loop takes each value in that row.

**7. Example 3 — Edge case or common mistake**

`break` only leaves the inner loop, and reusing the same variable name for both loops causes confusion:

```python
for row in range(3):
    for column in range(3):
        if column == 1:
            break
        print(row, column)

print()

for i in range(3):
    for i in range(2):
        print("inner i:", i)
    print("outer i after inner loop:", i)
```

Output:

```text
0 0
1 0
2 0

inner i: 0
inner i: 1
outer i after inner loop: 1
inner i: 0
inner i: 1
outer i after inner loop: 1
inner i: 0
inner i: 1
outer i after inner loop: 1
```

In the second example the inner loop overwrites `i`. The outer loop still runs three times, because it takes its next value from the range, but inside the body `i` has been changed to the last inner value. Use different names to avoid surprises.

The number of rounds is the product of the two counts, which you can verify:

```python
rounds = 0
for a in range(6):
    for b in range(7):
        rounds += 1
print(rounds, 6 * 7)

rounds = 0
for a in range(6):
    for b in range(a):
        rounds += 1
print(rounds, 6 * 5 // 2)
```

Output:

```text
42 42
15 15
```

When the inner range depends on the outer variable, the total is a sum: 0 + 1 + 2 + 3 + 4 + 5 = 15.

**8. Common mistakes**

- Using the same variable name in both loops.
- Forgetting the empty `print()` after the inner loop (everything ends up on one line).
- Putting `print()` inside the inner loop (every item on its own line).
- Wrong indentation, so that a statement lands in the wrong loop.
- Expecting `break` to leave both loops.
- Using nested loops on large data when a better approach (a set, a dictionary) would be much faster.
- Pairing an item with itself, or counting pairs twice, by starting the inner loop at the wrong place.

**9. Real-world and AI applications**

Nested loops process two-dimensional data: tables, spreadsheets, grids of pixels, game boards. They generate combinations (every setting with every other, as in a hyperparameter grid search over learning rates and batch sizes) and compare every pair of items (for example, similarity between every pair of documents). They also reveal why some AI computations are expensive: comparing every token with every other token makes the work grow with the square of the length (see [Attention and Transformers](35-attention-and-transformers.md)). Real libraries replace such loops with optimised array operations, but the idea is the same.

**10. Practice**

1. Print a 5 x 5 square of `#` characters.
2. Print a right-angled triangle of numbers: `1`, `1 2`, `1 2 3`, up to 5 rows.
3. Print an inverted triangle of stars with 5 rows (5 stars, then 4, ... 1).
4. Print the multiplication tables from 1 to 5 in a grid, each row on one line.
5. For `sizes = ["S", "M"]` and `colours = ["red", "green", "blue"]`, print every combination, and the total count.
6. Find all pairs of distinct numbers in `[1, 2, 3, 4, 5, 6]` that add up to 7.
7. Given a grid `[[3, 8, 1], [9, 4, 7]]`, find the largest value and its (row, column) position.
8. How many times does the body of `for a in range(4): for b in range(a, 4):` run? Verify by counting.

**11. Interview questions**

- *How many times does the inner body run in two nested loops of sizes a and b?* `a * b` times.
- *Does `break` in the inner loop stop the outer loop?* No; only the innermost loop ends.
- *How do you print a triangle pattern?* Make the inner loop's range depend on the outer variable.
- *Why are nested loops slow on big data?* The number of steps grows with the product of the sizes, roughly the square for two loops over `n` items.

**12. Quick revision**

- The inner loop runs completely for each round of the outer loop.
- Total rounds = outer rounds x inner rounds (or a sum, if the inner range depends on the outer variable).
- Use different variable names; `print()` after the inner loop ends the line.
- `break` and `continue` affect only the innermost loop.
- Cost grows quickly; watch out on large data.

---

## Answers to Practice Exercises

### Answers: The for Loop

1.

```python
name = "Maya"
for ch in name:
    print(ch)
```

Output:

```text
M
a
y
a
```

2.

```python
prices = [250, 99, 400, 75]
total = 0
largest = prices[0]
for price in prices:
    total += price
    if price > largest:
        largest = price
print(total, largest)
```

Output:

```text
824 400
```

3.

```python
drinks = ["tea", "coffee", "milk"]
for number, drink in enumerate(drinks, start=1):
    print(f"{number}. {drink}")
```

Output:

```text
1. tea
2. coffee
3. milk
```

4.

```python
for letter, number in zip(["a", "b", "c"], [1, 2, 3]):
    print(f"{letter}={number}")
```

Output:

```text
a=1
b=2
c=3
```

5.

```python
sentence = "Loops make repeated work simple and clear"
long_words = 0
for word in sentence.split():
    if len(word) > 4:
        long_words += 1
print(long_words)
```

Output:

```text
4
```

6. The loop walks through the list by position. When an item is removed, the items after it shift left by one, and the loop moves on to the next position, which skips the item that moved into the gap. Here is the problem with data where evens are adjacent, and a safe alternative:

```python
numbers = [2, 4, 6, 8]
for n in numbers:
    if n % 2 == 0:
        numbers.remove(n)
print(numbers)

numbers = [2, 4, 6, 8]
numbers = [n for n in numbers if n % 2 != 0]
print(numbers)
```

Output:

```text
[4, 8]
[]
```

### Answers: The range() Function

1.

```python
print(list(range(10)))
print(list(range(5, 16)))
print(list(range(0, 21, 2)))
print(list(range(50, 9, -10)))
```

Output:

```text
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
[50, 40, 30, 20, 10]
```

2. The numbers are 3, 7, 11, 15, 19, 23, 27, so there are 7 items. In general the count is the ceiling of (stop - start) / step = ceiling(27 / 4) = 7.

```python
print(len(range(3, 30, 4)), list(range(3, 30, 4)))
```

Output:

```text
7 [3, 7, 11, 15, 19, 23, 27]
```

3.

```python
for n in range(7, 71, 7):
    print(n, end=" ")
print()
```

Output:

```text
7 14 21 28 35 42 49 56 63 70 
```

4. It is empty, because the default step is +1 and 10 is already past 1. Use a negative step:

```python
print(list(range(10, 1)))
print(list(range(10, 1, -1)))
```

Output:

```text
[]
[10, 9, 8, 7, 6, 5, 4, 3, 2]
```

5.

```python
for i in range(1, 6):
    print(i * 0.5, end=" ")
print()
```

Output:

```text
0.5 1.0 1.5 2.0 2.5 
```

6.

```python
print(97 in range(1, 100, 3))
print(97 in range(1, 100, 2))
```

Output:

```text
True
True
```

The membership test on a range is computed from the start, stop and step; it does not build a list. 97 = 1 + 3 x 32, so it is in the first range.

### Answers: The for Loop with range()

1.

```python
for i in range(1, 11):
    print(i * i)
```

Output:

```text
1
4
9
16
25
36
49
64
81
100
```

2.

```python
total = 0
for n in range(2, 101, 2):
    total += n
print(total)
```

Output:

```text
2550
```

3.

```python
number = 9
for i in range(1, 13):
    print(f"{number} x {i:>2} = {number * i:>3}")
```

Output:

```text
9 x  1 =   9
9 x  2 =  18
9 x  3 =  27
9 x  4 =  36
9 x  5 =  45
9 x  6 =  54
9 x  7 =  63
9 x  8 =  72
9 x  9 =  81
9 x 10 =  90
9 x 11 =  99
9 x 12 = 108
```

4.

```python
result = 1
for i in range(2, 11):
    result *= i
print(result)
```

Output:

```text
3628800
```

5.

```python
values = [4, -2, 9, 0, -7]
negatives = 0
smallest = values[0]
for i in range(len(values)):
    if values[i] < 0:
        negatives += 1
    if values[i] < smallest:
        smallest = values[i]
print(negatives, smallest)
```

Output:

```text
2 -7
```

6.

```python
data = list(range(10))
for start in range(0, len(data), 4):
    print(data[start:start + 4])
```

Output:

```text
[0, 1, 2, 3]
[4, 5, 6, 7]
[8, 9]
```

The last batch is shorter, because slicing past the end is safe.

7.

```python
previous, current = 1, 1
print(previous, current, end=" ")
for _ in range(8):
    previous, current = current, previous + current
    print(current, end=" ")
print()
```

Output:

```text
1 1 2 3 5 8 13 21 34 55 
```

### Answers: Nested Loops

1.

```python
for row in range(5):
    print("#" * 5)
```

Output:

```text
#####
#####
#####
#####
#####
```

2.

```python
for row in range(1, 6):
    for number in range(1, row + 1):
        print(number, end=" ")
    print()
```

Output:

```text
1 
1 2 
1 2 3 
1 2 3 4 
1 2 3 4 5 
```

3.

```python
for row in range(5, 0, -1):
    for _ in range(row):
        print("*", end=" ")
    print()
```

Output:

```text
* * * * * 
* * * * 
* * * 
* * 
* 
```

4.

```python
for a in range(1, 6):
    for b in range(1, 6):
        print(f"{a * b:>3}", end="")
    print()
```

Output:

```text
  1  2  3  4  5
  2  4  6  8 10
  3  6  9 12 15
  4  8 12 16 20
  5 10 15 20 25
```

5.

```python
sizes = ["S", "M"]
colours = ["red", "green", "blue"]
count = 0
for size in sizes:
    for colour in colours:
        print(size, colour)
        count += 1
print("combinations:", count)
```

Output:

```text
S red
S green
S blue
M red
M green
M blue
combinations: 6
```

6.

```python
numbers = [1, 2, 3, 4, 5, 6]
for i in range(len(numbers)):
    for j in range(i + 1, len(numbers)):
        if numbers[i] + numbers[j] == 7:
            print(numbers[i], numbers[j])
```

Output:

```text
1 6
2 5
3 4
```

7.

```python
grid = [[3, 8, 1], [9, 4, 7]]
best = grid[0][0]
position = (0, 0)
for r in range(len(grid)):
    for c in range(len(grid[r])):
        if grid[r][c] > best:
            best = grid[r][c]
            position = (r, c)
print(best, position)
```

Output:

```text
9 (1, 0)
```

8. The inner loop runs 4, 3, 2 and 1 times, so 10 rounds in total.

```python
rounds = 0
for a in range(4):
    for b in range(a, 4):
        rounds += 1
print(rounds)
```

Output:

```text
10
```

---

## Chapter Summary and Key Takeaways

- `for item in iterable:` visits every item in turn; strings give characters, dictionaries give keys; use `enumerate` for positions and `zip` for parallel sequences.
- `range(stop)`, `range(start, stop)` and `range(start, stop, step)` produce integers lazily; `stop` is excluded and a negative step counts down.
- `for i in range(...)` is the standard counted loop; start an accumulator at 0 for sums and 1 for products, and remember that valid indices run from 0 to `len - 1`.
- A nested loop runs its inner loop completely for every round of the outer loop; use distinct variable names, and note that `break` leaves only the inner loop.
- Never modify a list while looping over it, and watch the cost of nested loops on large data.

Next: [Chapter 18 — Data Structures Introduction and Lists](18-lists-fundamentals.md) begins Part 4, the built-in containers.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
