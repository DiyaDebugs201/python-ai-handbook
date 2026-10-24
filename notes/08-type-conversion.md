# Chapter 08 — Type Conversion

> Part 2 — Data Types and Strings · Video: 2:01:13–2:07:12 · Previous: [07 String Slicing](07-string-slicing.md) · Next: [09 String Formatting and f-Strings](09-string-formatting-and-f-strings.md)

**In this chapter:** how Python silently promotes one numeric type to another when you mix them (`int` to `float` to `complex`, and `bool` inside arithmetic), and how you convert values on purpose with `int()`, `float()`, `str()`, `bool()` and `complex()`. You will see how `int()` reads strings in different bases, why `int(3.9)` gives `3` and not `4`, and exactly which inputs raise `ValueError` or `TypeError`.

**Before you start:** you should know the four basic value types from [Data Types and Integers](05-numeric-types-and-booleans.md#data-types-and-integers), [The Float Data Type](05-numeric-types-and-booleans.md#the-float-data-type), [Complex Numbers](05-numeric-types-and-booleans.md#complex-numbers) and [The Boolean Data Type](05-numeric-types-and-booleans.md#the-boolean-data-type), and that text is stored as `str` (see [String Basics](06-strings-basics-indexing-concatenation.md#string-basics)). Quick recap: a type is the kind of value an object is (`int`, `float`, `complex`, `bool`, `str`); `type(x)` is a built-in function that tells you the type of `x`; `True` and `False` are the only two `bool` values. Everything in this chapter was run with Python 3.13.16. Behavior of conversions is the same in all current Python 3 releases unless the text says otherwise. A few examples use a list, a `for` loop and `try`/`except` before those topics are taught in full ([Chapter 17](17-for-loop-range-and-nested-loops.md#the-for-loop), [Chapter 18](18-lists-fundamentals.md#lists-in-python)). For now, read `for item in items:` as "repeat the indented lines once for each item in the list", and `try`/`except` as "attempt this, and print a message instead of crashing if it fails".

---

## Implicit Type Conversion

**Timestamp:** [2:01:13](https://www.youtube.com/watch?v=J9BI0jGOds8&t=7273s)

**Learning objectives:**

- Explain what implicit type conversion (also called coercion or promotion) is and when Python does it.
- Predict the result type of arithmetic that mixes `bool`, `int`, `float` and `complex`.
- Explain why Python refuses to convert between `str` and numbers implicitly, and what error you get.
- Recognise the one case where implicit conversion can fail even between numbers (an integer too large for a float).

**1. Intuition**

Imagine measuring a table with a tape that shows whole centimetres, then adding a measurement written as 12.5. To add them you first write the whole number as 12.0 so that both measurements use the same "format". You did not ask for this; it is just the only sensible way to add them.

Python does the same thing. When an operator such as `+` receives two numbers of different types, Python quietly turns the "simpler" one into the "richer" one and then does the arithmetic. The programmer writes nothing extra, which is why it is called implicit conversion.

**2. Why does it exist?**

Programs constantly mix kinds of numbers: a count of items (`int`) times a price (`float`), or a real number plus an imaginary part (`complex`). If Python demanded that you convert by hand every time, simple formulas such as `3 * 2.5` would need extra code. Implicit conversion keeps everyday arithmetic short.

It also exists in a limited form only. Python does not guess when you mix text and numbers, because the right answer is unclear (`"5" + 3` could mean `8` or `"53"`). Refusing is safer than guessing.

**3. Technical explanation**

Numbers in Python form a ladder, from the narrowest type to the widest:

```text
bool  ->  int  ->  float  ->  complex
```

This is not valid Python; it is a diagram. When an arithmetic operator gets two numeric operands of different types, the narrower operand is converted to the type of the wider one, and the result has that wider type.

- `bool` is a subclass of `int`: `True` behaves as the integer `1` and `False` as `0`. So a `bool` takes part in arithmetic as an `int`.
- An `int` mixed with a `float` becomes a `float`.
- An `int` or `float` mixed with a `complex` becomes a `complex`.

Why this order? Each wider type can represent every value of the narrower one (with one caveat below), so nothing is lost on the way up. This is a design rule of the numeric types, not something you configure.

Three details worth knowing:

1. The true division operator `/` always returns a `float`, even when both operands are `int` and the division is exact. This is not a promotion; it is how `/` is defined. (Operators have their own chapter: [Chapter 11](11-arithmetic-operators.md#arithmetic-operators).)
2. Comparing different numeric types also converts. `1 == 1.0` is `True`, and `True == 1` is `True`.
3. The "nothing is lost" rule has one caveat. A `float` stores about 15 to 17 significant decimal digits, and its largest value is about `1.8e308`. A very large `int` can exceed that. Python then raises `OverflowError`; for integers that fit but have more digits than a float can hold, the float result is a rounded approximation.

Implicit conversion does not happen between `str` and numbers. `"5" + 3` raises `TypeError`.

**4. Syntax**

There is no syntax to write. Implicit conversion happens inside operators. The general pattern is:

```text
narrow_value  operator  wide_value   ->   result in the wider type
```

This is not valid Python; it names the pieces. `narrow_value` and `wide_value` are any two numeric values, and `operator` is `+`, `-`, `*`, `/`, `//`, `%`, `**` and so on. You can inspect the result type with the built-in function `type()`.

**5. Example 1 — Basic**

Runnable (standard library only). Each line mixes two types and prints the type of the result.

```python
whole = 4
fraction = 2.5
imaginary = 3j

print(whole + fraction, type(whole + fraction))
print(whole + imaginary, type(whole + imaginary))
print(fraction + imaginary, type(fraction + imaginary))
print(True + 1, type(True + 1))
print(True + 1.5, type(True + 1.5))
```

Output:

```text
6.5 <class 'float'>
(4+3j) <class 'complex'>
(2.5+3j) <class 'complex'>
2 <class 'int'>
2.5 <class 'float'>
```

Reading the output: `4 + 2.5` is `6.5`, a `float`. Adding `3j` produces a `complex` whose real part is the number you started with. `True + 1` is `2` because `True` acts as `1`, and the result stays `int`. `True + 1.5` is `2.5`, a `float`.

**6. Example 2 — Practical**

Runnable (standard library only). A price calculation that mixes `int`, `float` and `bool`. Booleans are handy for counting, because adding `True` adds one.

```python
quantity = 3                # int
unit_price = 19.99          # float
gift_wrap_requested = True  # bool
gift_wrap_fee = 2           # int

subtotal = quantity * unit_price
total = subtotal + gift_wrap_requested * gift_wrap_fee

print(subtotal, type(subtotal))
print(total, type(total))

answers = [True, False, True, True]
print("correct answers:", sum(answers))
print("share correct:", sum(answers) / len(answers))
```

Output:

```text
59.97 <class 'float'>
61.97 <class 'float'>
correct answers: 3
share correct: 0.75
```

Line by line:

- `quantity * unit_price` multiplies an `int` by a `float`; the `3` becomes `3.0` and the result is a `float`. (Floats are stored in binary, so some results show extra digits such as `0.30000000000000004`; see [The Float Data Type](05-numeric-types-and-booleans.md#the-float-data-type).)
- `gift_wrap_requested * gift_wrap_fee` is `True * 2`, which is `2`. If the flag were `False`, it would be `0`, and the fee would vanish. Multiplying by a bool is a compact way to say "include this amount only if the flag is true".
- `sum(answers)` is a built-in function that adds up the items of a list. Each `True` counts as `1`, so it counts the correct answers. Dividing by `len(answers)` uses `/`, which always gives a `float`.

**7. Example 3 — Edge case or common mistake**

Runnable (standard library only). Implicit conversion does not cross between text and numbers, and it can fail for huge integers.

The examples use `try` and `except` so that one error does not stop the whole program. Code under `try:` runs normally; if it raises the named error, Python skips the rest of that block and runs the matching `except` block instead, where `error` holds the error object (printing it shows its message). You only need to read this pattern here; it is not the topic of this chapter.

```python
try:
    print("Total: " + 30)
except TypeError as error:
    print("TypeError:", error)

try:
    print(5 + "3")
except TypeError as error:
    print("TypeError:", error)

try:
    print(10 ** 400 + 1.5)
except OverflowError as error:
    print("OverflowError:", error)

print(2 ** 53 + 1)
print(float(2 ** 53 + 1))
```

Output:

```text
TypeError: can only concatenate str (not "int") to str
TypeError: unsupported operand type(s) for +: 'int' and 'str'
OverflowError: int too large to convert to float
9007199254740993
9007199254740992.0
```

The first two errors have different wording because the left operand decides which side complains. `"Total: " + 30` asks a `str` to add an `int`; the message says it can only concatenate a `str`. `5 + "3"` asks an `int` to add a `str`; the message says the operand types are unsupported.

`10 ** 400` has about 400 digits. A `float` cannot hold that, so adding `1.5` raises `OverflowError`.

The last two lines show the quiet side of the same limit. `2 ** 53 + 1` is `9007199254740993` as an `int`, which Python stores exactly. Converting it to `float` gives `9007199254740992.0`, because 53 bits of precision are not enough to store the final `1`. No error, but the value changed. Keep this in mind when mixing very large integers with floats.

To fix a text-and-number mix, convert on purpose. Use `str(30)` to join to text, or `int("3")` to add numbers. Those functions are the next topic.

**8. Common mistakes**

- Expecting `"5" + 3` to give `8` or `"53"`. Python raises `TypeError`. Decide which you want and convert explicitly.
- Assuming `/` returns an `int` when the division is exact. `6 / 3` is `2.0`. Use `//` if you want an `int` quotient (for integer operands).
- Treating `True` as "just a flag" and being surprised that `True + True` is `2`. A `bool` is an `int` in arithmetic.
- Assuming any `int` can be mixed with any `float`. Extremely large integers raise `OverflowError`, and integers above 2 to the power 53 may lose exactness when converted.
- Using `==` between a float result and a decimal literal and expecting exact matches (`0.1 + 0.2 == 0.3` is `False`). That is floating-point representation, not conversion, but mixed arithmetic often exposes it.

**9. Real-world and AI applications**

- Data science libraries such as NumPy and pandas follow the same idea, called type promotion or upcasting: an array mixing integers and floats becomes a float array. Knowing the rule in plain Python makes their behavior predictable.
- Machine learning code often computes an accuracy as `correct / total`. Because `/` produces a `float`, the result is a fraction between 0 and 1 even when both counts are integers.
- Counting with booleans (`sum(predictions == labels)` style) is common in evaluation code. The idea that `True` is `1` is what makes it work.
- Mixed-type bugs appear when numbers arrive as text from files, web forms or JSON. Data loaded from CSV files is text until you convert it, which is why explicit conversion (next topic) matters in every data pipeline.

**10. Practice**

1. Without running it, give the type of each result: `7 + 2.0`, `7 // 2`, `7 / 7`, `True + True`, `2 * 3j`, `1.5 + True`.
2. A shop sells `items = 4` things at `price = 12.5` each. Write one expression that gives the total and print its value and type. Then change `items` to `0` and explain the type of the result.
3. The list `flags = [True, False, False, True, True]` marks which tests passed. Print how many passed and the pass rate as a decimal number. Then explain why `sum(flags)` works at all.
4. Predict what happens for `print("Score: " + 95.5)` and fix it so it prints `Score: 95.5`. (You will need the next topic for the fix.)
5. Explain why `1 == 1.0` and `True == 1` both print `True`, but `"1" == 1` prints `False`.

**11. Interview questions**

1. What is implicit type conversion? Give one example and one case where Python refuses.
   Short answer: Python automatically converts a narrower numeric type to a wider one when mixing them in an operation (`1 + 2.0` gives `3.0`). It refuses between `str` and numbers: `"1" + 2` raises `TypeError`.
2. What is the result type of `True + True`, and why?
   Short answer: `int`, value `2`. `bool` is a subclass of `int`, with `True` equal to `1`.
3. What type does `/` return for two integers?
   Short answer: always `float`, for example `4 / 2` is `2.0`.
4. Code question: what does this print?

```python
print(type(3 + 4.0), type(3 // 2), type(3 / 1), type(3 + 4j))
```

Short answer: `<class 'float'> <class 'int'> <class 'float'> <class 'complex'>`.
5. Why can mixing a huge `int` and a `float` fail or give surprising results?
   Short answer: a float has limited precision and range. An `int` above about `1.8e308` raises `OverflowError` when converted, and integers above 2 to the power 53 may be rounded.

**12. Quick revision**

- Numeric ladder: `bool` then `int` then `float` then `complex`. Mixed operands are promoted to the wider type.
- `bool` acts as `0` or `1` in arithmetic, which makes counting with `sum()` possible.
- `/` always returns `float`; `//` keeps integer type for integer operands.
- No implicit conversion between `str` and numbers: you get `TypeError`.
- Very large integers can overflow or lose exactness when promoted to `float`.

---

## Explicit Type Casting

**Timestamp:** [2:07:12](https://www.youtube.com/watch?v=J9BI0jGOds8&t=7632s)

**Learning objectives:**

- Convert values on purpose with `int()`, `float()`, `str()`, `bool()` and `complex()`.
- Read integers written in other bases (binary, octal, hexadecimal) with `int(text, base)`.
- Explain why `int()` truncates (drops the fraction) instead of rounding.
- Predict which conversions raise `ValueError`, which raise `TypeError`, and which are always allowed.

**1. Intuition**

Explicit conversion is the programmer saying "I know this is a piece of text, but treat it as a number" or "show this number as text". It is like writing a number on a cheque in words, or typing a phone number from a form into a calculator: the same information, written in a form that the next step can use.

Python calls this explicit type conversion. Many programmers call it casting, borrowing the word from other languages. In Python it is not a special syntax; it is a call to a built-in function named after the target type.

**2. Why does it exist?**

Data often arrives in the wrong type for the job:

- Anything typed into a prompt with `input()` arrives as a `str`, even if the user typed `25`.
- Values read from files, web pages, command-line arguments and environment variables are text.
- Output often needs the reverse: numbers turned into text to build messages.

Without explicit conversion you could not do arithmetic on such data, and you could not combine numbers with text. Because Python refuses to guess (previous topic), you state the conversion yourself and Python checks that it makes sense.

**3. Technical explanation**

`int`, `float`, `str`, `bool` and `complex` are classes (types). Calling one of them, for example `int("42")`, builds a new object of that type from the value you pass. The original object is never changed: `int(x)` does not turn `x` into an integer; it returns a new integer and leaves `x` alone. If you want to keep the result you must assign it.

The functions are built-in functions, so they need no `import`. Their rules:

- `int(x)`:
  - from a `float`: drops the fractional part, moving toward zero (truncation). `int(3.9)` is `3` and `int(-3.9)` is `-3`.
  - from a `bool`: `int(True)` is `1`, `int(False)` is `0`.
  - from a `str`: the text must be a whole number written in the chosen base. Leading and trailing whitespace is allowed. A decimal point or any other character raises `ValueError`.
  - from a `complex`, `None`, a list and most other types: `TypeError`.
  - `int(float("nan"))` raises `ValueError` and `int(float("inf"))` raises `OverflowError`.
- `int(text, base)`: reads `text` as a number in the given base, from 2 to 36, or base `0` to follow the prefix in the text (`0x`, `0o`, `0b`). The `base` argument is only allowed when the first argument is text (or bytes).
- `float(x)`: from an `int` or `bool`, gives the closest float; from text, reads decimal numbers such as `"3.14"`, `"1e3"`, `".5"`, and the special words `"inf"`, `"-inf"`, `"nan"` (any letter case). Anything else raises `ValueError`.
- `str(x)`: gives the readable text form of any object. It never fails for normal objects.
- `bool(x)`: applies Python's truth rules. It never fails. Values that count as false are called falsy; everything else is truthy.
- `complex(real, imag)` or `complex(text)`: builds a complex number. `complex("1+2j")` works; spaces inside the text raise `ValueError`.

Python does not have a rounding-style conversion in `int()`. The functions `round()` (a built-in), `math.floor()`, `math.ceil()` and `math.trunc()` (imported from the `math` module) do other roundings. `int()` on a float behaves like `math.trunc()`.

Falsy values: `0`, `0.0`, `0j`, `False`, `None`, and empty containers and strings: `""`, `[]`, `()`, `{}`, `set()`, `range(0)`. Everything else is truthy, including the string `"False"` and the string `"0"`, because those strings are not empty.

**4. Syntax**

```text
int(value)
int(text, base)
float(value)
str(value)
bool(value)
complex(real=0, imag=0)
complex(text)
```

This is not valid Python as a whole; it lists the call forms. In each form:

- `value` is any object the function knows how to convert.
- `text` is a string such as `"1010"`.
- `base` is a whole number from 2 to 36, or `0` to detect the base from a prefix in the text.
- `real` and `imag` are numbers for the real and imaginary parts.

**5. Example 1 — Basic**

Runnable (standard library only). One conversion of each kind.

```python
print(int("42"), type(int("42")))
print(int(3.99), int(-3.99))
print(float("3.14"), float(7))
print(str(100), str(3.0), str(True), str(None))
print(bool(0), bool(1), bool(""), bool("hello"))
print(complex(3, 4), complex("2+5j"))
```

Output:

```text
42 <class 'int'>
3 -3
3.14 7.0
100 3.0 True None
False True False True
(3+4j) (2+5j)
```

Notes: `int(3.99)` is `3` and `int(-3.99)` is `-3`; the fraction is cut off, not rounded. `str(3.0)` is `"3.0"`: the text keeps the decimal point because the object was a `float`. `complex(3, 4)` prints as `(3+4j)`; the parentheses are how Python shows a complex number that has a real part.

**6. Example 2 — Practical**

Runnable (standard library only). Text in, number out, text back. A hard-coded string stands in for what `input()` would return. (With `input()`, you would write `age_text = input("Age: ")`; the returned value is always a `str`.)

```python
age_text = "25"               # what input() would give you
price_text = " 19.99 \n"      # text read from a file often has spaces and a newline

age = int(age_text)
price = float(price_text)     # surrounding whitespace is allowed

next_year_age = age + 1
total = price * 3

message = "Next year you will be " + str(next_year_age)
print(message)
print("Three items cost " + str(round(total, 2)))
print(f"Total again with an f-string: {total:.2f}")
```

Output:

```text
Next year you will be 26
Three items cost 59.97
Total again with an f-string: 59.97
```

Line by line:

- `int(age_text)` returns a new `int`. Arithmetic on `age_text` itself would fail, because it is still text.
- `float(price_text)` accepts the spaces and the newline around the number; `int()` and `float()` both ignore whitespace at the ends.
- `str(next_year_age)` is needed before joining with `+`, because `+` will not join a `str` and an `int`.
- `round(total, 2)` is a built-in function that rounds to two decimal places. Here it is used for display.
- The last line uses an f-string, which is the usual modern way to mix text and numbers. Formatting gets its own chapter: [Chapter 09](09-string-formatting-and-f-strings.md#python-f-strings).

**7. Example 3 — Edge case or common mistake**

Runnable (standard library only). The cases that raise errors, with the exact messages, and the base argument.

```python
attempts = ["3.7", "", "12abc", "1,000", "0x1f", None, [1, 2], 3 + 4j]

for item in attempts:
    try:
        print(repr(item), "->", int(item))
    except (ValueError, TypeError) as error:
        print(repr(item), "->", type(error).__name__ + ":", error)
```

Output:

```text
'3.7' -> ValueError: invalid literal for int() with base 10: '3.7'
'' -> ValueError: invalid literal for int() with base 10: ''
'12abc' -> ValueError: invalid literal for int() with base 10: '12abc'
'1,000' -> ValueError: invalid literal for int() with base 10: '1,000'
'0x1f' -> ValueError: invalid literal for int() with base 10: '0x1f'
None -> TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType'
[1, 2] -> TypeError: int() argument must be a string, a bytes-like object or a real number, not 'list'
(3+4j) -> TypeError: int() argument must be a string, a bytes-like object or a real number, not 'complex'
```

Rules shown by the output:

- `ValueError` means the type is acceptable (a string) but the content is not a valid whole number. `"3.7"` is not a whole number; to read it, go through a float first: `int(float("3.7"))` is `3`.
- `TypeError` means the type of the object is not convertible at all: `None`, a list, and a complex number cannot become an `int`.
- Commas in `"1,000"` are not accepted. Remove them first with a string method such as `.replace(",", "")` (see [String Methods](10-ord-chr-and-string-methods.md#string-methods)).
- `"0x1f"` fails with the default base 10, but succeeds when you tell `int()` the base. The next block shows that.

Reading other bases:

```python
print(int("1010", 2))
print(int("777", 8))
print(int("ff", 16), int("FF", 16))
print(int("0x1f", 16), int("0x1f", 0), int("0b101", 0), int("0o17", 0))
print(int("z", 36))

for text, base in [("9", 8), ("12", 2)]:
    try:
        int(text, base)
    except ValueError as error:
        print("ValueError:", error)

try:
    int(3.7, 10)
except TypeError as error:
    print("TypeError:", error)
```

Output:

```text
10
511
255 255
31 31 5 15
35
ValueError: invalid literal for int() with base 8: '9'
ValueError: invalid literal for int() with base 2: '12'
TypeError: int() can't convert non-string with explicit base
```

How to read it: `int("1010", 2)` interprets the text as binary: 8 + 2 = `10`. `"ff"` in base 16 is 15 * 16 + 15 = `255`; letter case does not matter. In base 36 the digits are `0-9` then `a-z`, so `"z"` is `35`. With base `0`, Python reads the prefix: `0x` means hexadecimal, `0b` binary, `0o` octal. With base 16 the prefix `0x` is also allowed. Digits outside the base (such as `9` in base 8) raise `ValueError`. The `base` argument with a non-text first argument raises `TypeError`.

Truncation versus rounding:

```python
import math

values = [3.9, -3.9, 2.5, 3.5, -0.5]
print("value  int  round  floor  ceil")
for value in values:
    print(f"{value:5}  {int(value):3}  {round(value):5}  {math.floor(value):5}  {math.ceil(value):4}")
```

Output:

```text
value  int  round  floor  ceil
  3.9    3      4      3     4
 -3.9   -3     -4     -4    -3
  2.5    2      2      2     3
  3.5    3      4      3     4
 -0.5    0      0     -1     0
```

`int()` always moves toward zero, so `int(-3.9)` is `-3` while `math.floor(-3.9)` is `-4`. The built-in `round()` goes to the nearest whole number, and for an exact tie such as `2.5` it picks the even neighbor: `round(2.5)` is `2` and `round(3.5)` is `4`. This rule is called round-half-to-even (banker's rounding). If you need "drop the fraction", use `int()`; if you need "nearest", use `round()`.

Finally, converting to `bool` and `str`, where surprises are about meaning rather than errors:

```python
for value in [0, 0.0, "", [], None, "0", "False", " ", [0], 0.1, -1]:
    print(f"{value!r:8} -> {bool(value)}")

print(bool("False"))
print(str([1, 2]), str("hi"), repr("hi"))
print(float("inf"), float("-inf"), float("nan"))
```

Output:

```text
0        -> False
0.0      -> False
''       -> False
[]       -> False
None     -> False
'0'      -> True
'False'  -> True
' '      -> True
[0]      -> True
0.1      -> True
-1       -> True
True
[1, 2] hi 'hi'
inf -inf nan
```

`bool("False")` is `True` because the string is not empty; `bool` checks emptiness, not meaning. If a text answer must become a real boolean, compare it: `answer.strip().lower() == "true"`. `str("hi")` gives `hi` while `repr("hi")` gives `'hi'` with quotes; `repr()` is a built-in function that shows a value the way you would write it in code, which is useful when debugging. Special float words `inf` and `nan` come from the text forms; `nan` means "not a number".

**8. Common mistakes**

- Calling `int()` on text with a decimal point (`int("3.7")`). Fix: `int(float("3.7"))`, or decide if you really want `round(float("3.7"))`.
- Expecting `int(-3.9)` to be `-4`. It is `-3`. Use `math.floor()` if you need the lower whole number.
- Writing `int(x)` and ignoring the result. The call returns a new value; `x` stays as it was. Assign it: `x = int(x)`.
- Assuming `bool("False")` is `False`. Any non-empty string is truthy. Compare the text instead.
- Passing text with spaces inside, thousand separators or currency symbols (`"1 000"`, `"1,000"`, `"$5"`). Strip or replace those characters before converting.
- Using `int("0x1f")` without a base. Pass `16` or `0`.
- Converting user input without handling errors. `int(input())` crashes if the user types letters; catching `ValueError` with `try`/`except` is the robust approach (Part 5 and later chapters build on this).
- Forgetting that `str()` is needed before joining a number to text with `+`. An f-string avoids the problem.

**9. Real-world and AI applications**

- Every data-loading pipeline converts text to numbers. A row read from a CSV file is a list of strings, and a loop such as `float(cell)` turns the numeric columns into numbers. Dirty values like empty cells or `"N/A"` raise `ValueError`, which is why cleaning code often wraps conversions in `try`/`except`.
- Command-line tools and web servers receive everything as text: command-line arguments, query-string parameters, environment variables such as a port number. Converting with `int()` is the first step.
- Training scripts read hyper-parameters such as a learning rate (`float("0.001")`) or batch size (`int("32")`) from configuration files or arguments.
- Model outputs often arrive as text. For example, a language model's reply of `"42"` is a string; your code must convert it (and be ready for it to fail, since models sometimes return extra words). Defensive conversion matters here.
- Identifiers in hexadecimal and binary appear in hashing, color codes (`int("ff", 16)`) and file formats; `int(text, base)` is the standard tool.

**10. Practice**

1. Convert each of these and print the result and its type: `"250"`, `"2.5e2"`, `"0.1"`, `"True"` (to `bool`), `7` (to `str`). One of them will raise an error when converted with `int()`. Which, and why?
2. Predict, then check: `int(7.9)`, `int(-7.9)`, `round(7.9)`, `round(-7.5)`, `round(6.5)`.
3. A program receives `"1010"` from a binary-file reader and `"1f"` from a hex reader. Convert each to a decimal integer and print them.
4. Write code that takes the hard-coded string `raw = "  42.0  "` and produces the integer `42`. Explain why `int(raw)` alone fails and what you did instead.
5. Write a loop over `["10", "x", "3.5", "", "7"]`. For each item, print the integer value, or print a message `"cannot convert: ..."` using `try`/`except ValueError`. Items that are valid decimals but not whole numbers (such as `"3.5"`) must also be reported.
6. Explain the difference between `bool("")` and `bool(" ")`, and write one line that turns the text `"yes"`, `"true"`, or `"1"` (any letter case) into the boolean `True` and everything else into `False`.

**11. Interview questions**

1. What is the difference between implicit and explicit type conversion?
   Short answer: implicit is done by Python automatically inside an operation (for example `int` to `float`); explicit is done by the programmer calling `int()`, `float()`, `str()` and so on.
2. What does `int(3.9)` return, and how is it different from `round(3.9)`?
   Short answer: `3`, because `int()` truncates toward zero; `round(3.9)` is `4`, the nearest integer.
3. What is the difference between `ValueError` and `TypeError` when converting?
   Short answer: `ValueError` means the type is acceptable but the value is not (`int("abc")`); `TypeError` means the type itself cannot be converted (`int(None)`).
4. Why does `int("3.7")` fail but `int(float("3.7"))` work?
   Short answer: `int()` on a string requires text for a whole number; a decimal point is invalid. `float("3.7")` first produces a float, and `int()` on a float truncates it.
5. Code question: what does this print?

```python
print(bool("False"), bool(""), int("0b11", 0))
```

Short answer: `True False 3`. The non-empty string is truthy, the empty string is falsy, and base `0` reads the `0b` prefix as binary.
6. Does `int(x)` change `x`?
   Short answer: no. It returns a new object. `x` still refers to the old one unless you reassign it.
7. What does `int("ff", 16)` return and what does the second argument mean?
   Short answer: `255`. The second argument is the base in which the text is written.

**12. Quick revision**

- Explicit conversion is a call to the type: `int()`, `float()`, `str()`, `bool()`, `complex()`. They are built-in functions and create new objects.
- `int(float)` truncates toward zero; `round()` rounds to nearest (ties to even); `math.floor()` and `math.ceil()` go down and up.
- `int(text)` accepts only whole numbers (optional sign, optional surrounding spaces); `int(text, base)` reads bases 2 to 36, or base `0` with a prefix.
- `ValueError`: right type, bad content. `TypeError`: type cannot be converted.
- `bool()` is about emptiness and zero, not meaning: `bool("False")` is `True`.
- `str()` and `repr()` differ: `str` is for people, `repr` is for debugging.

---

## Answers to Practice Exercises

### Answers: Implicit Type Conversion

**Exercise 1.**

```python
print(type(7 + 2.0).__name__)
print(type(7 // 2).__name__)
print(type(7 / 7).__name__)
print(type(True + True).__name__)
print(type(2 * 3j).__name__)
print(type(1.5 + True).__name__)
```

Output:

```text
float
int
float
int
complex
float
```

Explanation: `int + float` is `float`; `//` of two integers stays `int`; `/` always gives `float`; `True + True` is `2`, an `int`; an `int` times a `complex` is `complex`; `float + bool` treats `True` as `1` and gives `float`. `__name__` is an attribute that holds the type's name as text.

**Exercise 2.**

```python
items = 4
price = 12.5
total = items * price
print(total, type(total).__name__)

items = 0
total = items * price
print(total, type(total).__name__)
```

Output:

```text
50.0 float
0.0 float
```

Explanation: even with `items = 0` the product is `0.0`, a `float`, because the `int` is promoted before multiplying. The type depends on the operand types, not on the value.

**Exercise 3.**

```python
flags = [True, False, False, True, True]
passed = sum(flags)
print(passed)
print(passed / len(flags))
```

Output:

```text
3
0.6
```

Explanation: `sum()` adds the items starting from `0`. Since `True` acts as `1` and `False` as `0`, the sum counts the `True` values. `/` gives a `float` pass rate (`0.6`).

**Exercise 4.**

```python
score = 95.5
print("Score: " + str(score))
print(f"Score: {score}")
```

Output:

```text
Score: 95.5
Score: 95.5
```

Explanation: `"Score: " + 95.5` raises `TypeError: can only concatenate str (not "float") to str`. Converting with `str()` (or using an f-string) fixes it.

**Exercise 5.**

```python
print(1 == 1.0, True == 1, "1" == 1)
```

Output:

```text
True True False
```

Explanation: comparisons between numbers use the numeric values, so `1`, `1.0` and `True` are equal. A `str` and an `int` are never equal, because Python does not convert between them; `==` returns `False` rather than raising an error.

### Answers: Explicit Type Casting

**Exercise 1.**

```python
print(repr(int("250")), type(int("250")).__name__)
print(repr(float("2.5e2")), type(float("2.5e2")).__name__)
print(repr(float("0.1")), type(float("0.1")).__name__)
print(repr(bool("True")), type(bool("True")).__name__)
print(repr(str(7)), type(str(7)).__name__)

try:
    int("2.5e2")
except ValueError as error:
    print("ValueError:", error)
```

Output:

```text
250 int
250.0 float
0.1 float
True bool
'7' str
ValueError: invalid literal for int() with base 10: '2.5e2'
```

Explanation: `"2.5e2"` is a valid float text (`250.0`), but `int()` accepts only whole-number text, so `int("2.5e2")` raises `ValueError`. Also note `bool("True")` is `True` simply because the string is not empty.

**Exercise 2.**

```python
print(int(7.9), int(-7.9), round(7.9), round(-7.5), round(6.5))
```

Output:

```text
7 -7 8 -8 6
```

Explanation: `int()` truncates toward zero (`7` and `-7`). `round(7.9)` is `8`. `-7.5` and `6.5` are exact ties, so `round()` picks the even neighbor: `-8` and `6`.

**Exercise 3.**

```python
print(int("1010", 2))
print(int("1f", 16))
```

Output:

```text
10
31
```

Explanation: binary `1010` is 8 + 2 = 10. Hex `1f` is 1 * 16 + 15 = 31.

**Exercise 4.**

```python
raw = "  42.0  "
value = int(float(raw))
print(value, type(value).__name__)

try:
    int(raw)
except ValueError as error:
    print("ValueError:", error)
```

Output:

```text
42 int
ValueError: invalid literal for int() with base 10: '  42.0  '
```

Explanation: `int(raw)` fails because the text contains a decimal point. `float(raw)` accepts it (and the spaces), then `int()` truncates `42.0` to `42`.

**Exercise 5.**

```python
for item in ["10", "x", "3.5", "", "7"]:
    try:
        print(int(item))
    except ValueError:
        print("cannot convert:", repr(item))
```

Output:

```text
10
cannot convert: 'x'
cannot convert: '3.5'
cannot convert: ''
7
```

Explanation: `"x"`, `"3.5"` and `""` are all strings, so they raise `ValueError` (not `TypeError`), and the `except ValueError` branch handles them. `repr(item)` shows the quotes, which makes the empty string visible.

**Exercise 6.**

```python
print(bool(""), bool(" "))

for answer in ["yes", "TRUE", "1", "no", "maybe"]:
    print(answer, answer.strip().lower() in ("yes", "true", "1"))
```

Output:

```text
False True
yes True
TRUE True
1 True
no False
maybe False
```

Explanation: the empty string is falsy; a string with one space is not empty, so it is truthy. The comparison against allowed words is the right way to read a yes/no answer. `.strip()` and `.lower()` are string methods (see [Chapter 10](10-ord-chr-and-string-methods.md#string-methods)); `in` tests whether the text matches one of the items in the tuple.

---

## Chapter Summary and Key Takeaways

- Implicit conversion promotes numbers along `bool`, `int`, `float`, `complex`. `/` always returns `float`.
- `bool` behaves as `0` or `1` in arithmetic, so `sum()` can count `True` values.
- Python never converts between `str` and numbers implicitly; mixing them raises `TypeError`.
- Very large integers can overflow when mixed with floats; integers above 2 to the power 53 may lose exactness as floats.
- Explicit conversion uses the built-in type functions `int()`, `float()`, `str()`, `bool()`, `complex()`. They return new objects and leave the original unchanged.
- `int()` of a float truncates toward zero; use `round()`, `math.floor()` or `math.ceil()` for other roundings.
- `int(text)` accepts only whole-number text; `int(text, base)` reads bases 2 to 36, and base `0` follows the `0x`, `0o`, `0b` prefix.
- `ValueError` means the content is invalid; `TypeError` means the type cannot be converted.
- `bool()` tests for zero or emptiness, not meaning: `bool("False")` is `True`.

Next: [Chapter 09 — String Formatting and f-Strings](09-string-formatting-and-f-strings.md) shows how to build readable text from values without manual `str()` calls.
