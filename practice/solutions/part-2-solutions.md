# Part 2 — Solutions: Data Types and Strings

> [Practice index](../README.md) · [Problems for this part](../part-2-exercises.md)

Every program below was run with Python 3.13 and the output shown is the real output. Your own solution may differ and still be correct: compare behaviour, not wording.

## P2.1 — Types of results

Print the type of each result: `7 / 2`, `7 // 2`, `7 % 2`, `2 ** 10`, `True + True`, `"5" * 3`.

```python
for expression, value in [("7 / 2", 7 / 2), ("7 // 2", 7 // 2), ("7 % 2", 7 % 2), ("2 ** 10", 2 ** 10), ("True + True", True + True), ('"5" * 3', "5" * 3)]:
    print(f"{expression:<12} {value!r:<8} {type(value).__name__}")
```

Output:

```text
7 / 2        3.5      float
7 // 2       3        int
7 % 2        1        int
2 ** 10      1024     int
True + True  2        int
"5" * 3      '555'    str
```

`/` always gives a float, `//` and `%` keep ints, `True` counts as 1 in arithmetic, and a string times an int repeats the string.

## P2.2 — Floating-point comparison

Show that `0.1 + 0.2 == 0.3` is `False`, then compare them correctly in two ways: with `round` and with `math.isclose`.

```python
import math

total = 0.1 + 0.2
print(total == 0.3)
print(round(total, 10) == round(0.3, 10))
print(math.isclose(total, 0.3))
```

Output:

```text
False
True
True
```

Binary floating point cannot store 0.1 exactly, so tiny errors appear; compare with a tolerance instead of `==`.

## P2.3 — Palindrome check

Write a function `is_palindrome(text)` that ignores case, spaces and punctuation. Test it on `"A man, a plan, a canal: Panama"` and `"Python"`.

```python
def is_palindrome(text):
    cleaned = "".join(ch.lower() for ch in text if ch.isalnum())
    return cleaned == cleaned[::-1]


print(is_palindrome("A man, a plan, a canal: Panama"))
print(is_palindrome("Python"))
```

Output:

```text
True
False
```

Cleaning first removes case and punctuation; the slice `[::-1]` reverses the string for comparison.

## P2.4 — Slicing practice

For `word = "Programming"` print: the first 3 characters, the last 3, every second character, the string reversed, and the middle part from index 3 up to (not including) index 8.

```python
word = "Programming"
print(word[:3])
print(word[-3:])
print(word[::2])
print(word[::-1])
print(word[3:8])
```

Output:

```text
Pro
ing
Pormig
gnimmargorP
gramm
```

Slices are `[start:stop:step]`; stop is excluded, negative indexes count from the end, and a step of -1 reverses.

## P2.5 — Safe conversion

Convert the list `["3", "4.5", "x", "10"]` to floats. Collect the converted values in one list and the strings that failed in another, then print both.

```python
raw = ["3", "4.5", "x", "10"]
converted, failed = [], []
for item in raw:
    try:
        converted.append(float(item))
    except ValueError:
        failed.append(item)
print(converted)
print(failed)
```

Output:

```text
[3.0, 4.5, 10.0]
['x']
```

`float("x")` raises `ValueError`; catching it per item keeps the loop going so good values are still converted.

## P2.6 — Aligned table with f-strings

Print the numbers 1 to 5 with their squares and cubes as a table with right-aligned columns of width 4, 8 and 8, and a header row.

```python
print(f"{'n':>4}{'square':>8}{'cube':>8}")
for n in range(1, 6):
    print(f"{n:>4}{n ** 2:>8}{n ** 3:>8}")
```

Output:

```text
   n  square    cube
   1       1       1
   2       4       8
   3       9      27
   4      16      64
   5      25     125
```

The format spec `>4` right-aligns in a field of width 4; the header uses string literals inside the braces.

## P2.7 — Caesar cipher

Write `shift(text, k)` that shifts each lowercase letter k places forward in the alphabet (wrapping from `z` to `a`) and leaves other characters unchanged. Encrypt `"hello, world"` with k=3 and decrypt it again.

```python
def shift(text, k):
    result = []
    for ch in text:
        if "a" <= ch <= "z":
            result.append(chr((ord(ch) - ord("a") + k) % 26 + ord("a")))
        else:
            result.append(ch)
    return "".join(result)


secret = shift("hello, world", 3)
print(secret)
print(shift(secret, -3))
```

Output:

```text
khoor, zruog
hello, world
```

`ord(ch) - ord('a')` gives 0 to 25; adding k and taking `% 26` wraps around; `chr` converts back to a letter. A negative shift decrypts.

## P2.8 — Count vowels

Count the vowels in `"Learning Python is Fun"` (case-insensitive) using a string method and a loop or comprehension.

```python
text = "Learning Python is Fun"
lowered = text.lower()
print(sum(lowered.count(v) for v in "aeiou"))
```

Output:

```text
6
```

`str.count` counts occurrences of a substring; summing over the five vowels gives the total.

## P2.9 — Clean and title-case

Turn `"  hELLo    wORLD  "` into `"Hello World"`.

```python
messy = "  hELLo    wORLD  "
clean = " ".join(word.capitalize() for word in messy.split())
print(repr(clean))
```

Output:

```text
'Hello World'
```

`split()` drops extra whitespace, `capitalize` fixes each word's case, and `join` puts single spaces back.

## P2.10 — Format money

Print `1234567.891` as `1,234,567.89` and `0.256` as `25.6%`.

```python
print(f"{1234567.891:,.2f}")
print(f"{0.256:.1%}")
```

Output:

```text
1,234,567.89
25.6%
```

`,` adds thousands separators, `.2f` fixes two decimals, and `%` multiplies by 100 and appends a percent sign.

## P2.11 — Truthiness table

Print `bool(x)` for each of `0`, `1`, `""`, `"0"`, `[]`, `[0]`, `None`, `0.0`.

```python
for value in [0, 1, "", "0", [], [0], None, 0.0]:
    print(f"{value!r:<5} {bool(value)}")
```

Output:

```text
0     False
1     True
''    False
'0'   True
[]    False
[0]   True
None  False
0.0   False
```

Zero, empty strings and containers, and `None` are false; the string `"0"` and the list `[0]` are non-empty, so true.

---

Back to the [problems](../part-2-exercises.md) or the [practice index](../README.md).
