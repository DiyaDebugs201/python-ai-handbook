# Chapter 05 — Numeric Types and Booleans

> Part 2 — Data Types and Strings · Video: 51:57–1:12:28 · Previous: [04 Errors and Identifiers](04-errors-and-identifiers.md) · Next: [06 Strings: Basics, Indexing, Concatenation and Repetition](06-strings-basics-indexing-concatenation.md)

**In this chapter:** what a data type is; the whole-number type `int` (including its unlimited size); the decimal-number type `float` and why `0.1 + 0.2` is not exactly `0.3`; how to compare floats safely with `math.isclose()`; a short mention of the `decimal` module; the complex-number type `complex`; the boolean type `bool`, including the fact that `bool` is a subclass of `int` and how truthiness works; and the two tools for checking a type, `type()` and `isinstance()`.

**Before you start:** you should be able to run a Python file or the interactive prompt, call the built-in function `print()`, and create a variable with `name = value` (see [Chapter 03](03-builtin-functions-print-and-modules.md) and [Chapter 04](04-errors-and-identifiers.md)). Recap: a variable is a name that refers to a value; a value has a type; and an error such as `TypeError` is Python telling you an operation does not fit the types involved. Everything in this chapter was run with Python 3.13.16. Where behavior differs between Python versions, the text says so. A glossary of terms is in [../docs/GLOSSARY.md](../docs/GLOSSARY.md).

---

## Data Types and Integers

**Timestamp:** [51:57](https://www.youtube.com/watch?v=J9BI0jGOds8&t=3117s)

**Learning objectives:**

- Explain what a data type is and why Python needs one for every value.
- Create `int` values, including very large ones, and write integer literals with underscores and in binary, octal and hexadecimal.
- Use `type()` and `isinstance()` to inspect the type of a value, and know when to prefer each.

**1. Intuition**

A data type tells Python what kind of thing a value is and therefore what you can do with it. You can add two numbers, but adding a number to a piece of text makes no sense. Think of a kitchen: a measuring jug is for liquids, a weighing scale is for solids, and you do not weigh milk on the scale. The type of a value decides which "tools" apply to it.

An integer, written `int` in Python, is a whole number: `25`, `0`, `-7`, `1000000`. It has no fractional part.

**2. Why does it exist?**

A computer stores everything as bits. The same bit pattern can mean a whole number, a decimal number, a letter or a true/false answer. Types tell Python (and you) how to interpret the bits and which operations are legal. Without types, `"42" + 1` would have no defined meaning: should the result be `43` or `"421"`? Python refuses to guess and raises an error instead.

**3. Technical explanation**

In Python, every value is an object, and every object has a type. The type is fixed for the life of the object. The variable does not have a type; the value it refers to does. The same name can later refer to a value of a different type (this is called dynamic typing).

The built-in types you meet first are:

| Type | Meaning | Example literal |
|------|---------|-----------------|
| `int` | whole number | `25` |
| `float` | decimal (floating-point) number | `3.14` |
| `complex` | complex number | `3 + 4j` |
| `bool` | true or false | `True` |
| `str` | text | `"hello"` |
| `NoneType` | "no value" marker | `None` |

Python's `int` has no fixed size limit. In many other languages (C, Java) an integer occupies a fixed number of bits, for example 32 or 64, so there is a largest value and exceeding it wraps around or overflows. Python integers grow as needed, limited only by available memory. Internally, a large integer is stored as a sequence of smaller digit chunks, so bigger numbers take more memory and more time to compute with. For everyday numbers the difference is invisible.

Python 3 has only one integer type, `int`. (Python 2 had a separate `long` type; it no longer exists.)

**4. Syntax**

```text
name = integer_literal
```

This is a pattern, not runnable code. Integer literals can be written in these forms:

- Decimal: `1000`
- With underscores for readability: `1_000_000` (underscores are ignored by Python)
- Binary: `0b1010` (prefix `0b`)
- Octal: `0o17` (prefix `0o`)
- Hexadecimal: `0xFF` (prefix `0x`)

Tools for checking types:

- `type(value)` is a built-in function that returns the exact type of `value`.
- `isinstance(value, type_or_tuple_of_types)` is a built-in function that returns `True` if `value` is an instance of that type (or of a subclass of it), otherwise `False`.

**5. Example 1 — Basic**

```python
age = 25
print(age)
print(type(age))

big = 2 ** 100
print(big)
print(big + 1)
print(type(big))

print(1_000_000)
print(0b1010, 0o17, 0xFF)
```

Output:

```text
25
<class 'int'>
1267650600228229401496703205376
1267650600228229401496703205377
<class 'int'>
1000000
10 15 255
```

`2 ** 100` is "2 to the power 100" (the `**` operator is covered in [Chapter 11](11-arithmetic-operators.md)). The result has 31 digits and Python stores it exactly, with no overflow. The last line shows that `0b1010`, `0o17` and `0xFF` are just other ways to write the integers 10, 15 and 255; `print()` always shows them in decimal.

**6. Example 2 — Practical**

Computing a factorial (the product 1 × 2 × 3 × ... × n) quickly produces numbers far beyond what a 64-bit integer holds.

```python
factorial = 1
for number in range(1, 26):
    factorial *= number

print(factorial)
print(type(factorial))
print(len(str(2 ** 1000)))
```

Output:

```text
15511210043330985984000000
<class 'int'>
302
```

Line by line: `factorial` starts at 1; the `for` loop multiplies it by each number from 1 to 25 (`*=` multiplies and reassigns); the result, 25!, is about 1.5 × 10^25, which is larger than the biggest 64-bit integer (about 9.2 × 10^18) but is stored exactly in Python. The last line converts `2 ** 1000` to text with `str()` and counts its characters with `len()`, showing that it has 302 digits.



**7. Example 3 — Edge case or common mistake**

A frequent mistake is mixing up the integer `42` and the text `"42"`. They look alike when printed but are different types, and a related surprise is that `/` always produces a `float`.

```python
print(int("42") + 1)
print("42" + "1")

try:
    print("42" + 1)
except TypeError as error:
    print("TypeError:", error)

print(5 / 2, type(5 / 2))
print(4 / 2, type(4 / 2))
print(5 // 2, type(5 // 2))
```

Output:

```text
43
421
TypeError: can only concatenate str (not "int") to str
2.5 <class 'float'>
2.0 <class 'float'>
2 <class 'int'>
```

`int("42")` converts text into an integer, so `+ 1` is arithmetic. `"42" + "1"` joins two strings. `"42" + 1` mixes a string and an integer, and Python raises `TypeError`. The fix is to convert explicitly, either `int("42") + 1` (arithmetic) or `"42" + str(1)` (joining). Conversion functions are covered fully in [Chapter 08](08-type-conversion.md).

The division line shows that `/` returns a `float` even when the answer is a whole number (`4 / 2` is `2.0`), while `//` (floor division) between two integers returns an `int`.

**type() versus isinstance()**

Both are built-in functions, and both tell you about a type.

```python
value = 7
print(type(value))
print(type(value) == int)
print(isinstance(value, int))
print(isinstance(value, (int, float)))
print(isinstance("7", (int, float)))
print(isinstance(True, int))
print(type(True) == int)
```

Output:

```text
<class 'int'>
True
True
True
False
True
False
```

- `type(value)` returns the exact type. `type(value) == int` is true only when the type is exactly `int`.
- `isinstance(value, int)` is true when the value is an `int` or an instance of a subclass of `int`. Passing a tuple, such as `(int, float)`, means "any of these".
- `isinstance(True, int)` is `True` because `bool` is a subclass of `int` (explained in [The Boolean Data Type](#the-boolean-data-type)), while `type(True) == int` is `False`. In practice, prefer `isinstance()` for checks inside programs, because it respects subclasses; use `type()` when you want to display or log the exact type.

**8. Common mistakes**

- Writing `"42" + 1` and expecting `43`. Convert first with `int()`.
- Writing numbers with leading zeros such as `007`. In Python 3 this is a `SyntaxError`; write `7`, or `0o7` if you really want octal.
- Assuming integers overflow like in C or Java. They do not; only memory limits them.
- Believing that the variable has a type. The value has the type; `x = 5` then `x = "five"` is allowed.
- Using `type(x) == int` when `isinstance(x, int)` is what you mean (or the reverse). The first rejects subclasses such as `bool`; the second accepts them. Decide which behavior you want.
- Forgetting that `/` returns a `float`. If you need a whole-number result, use `//`.

**9. Real-world and AI applications**

- Counters, loop indexes, IDs, sizes and lengths are all `int` values. In AI code, the number of tokens, the batch size, the number of training epochs and the position of a word in a sentence are integers.
- Arbitrary-size integers make exact calculations possible, for example in cryptography, combinatorics (counting arrangements) and hash computations, without extra libraries.
- Machine-learning libraries such as NumPy have their own fixed-size integer types (for example 8-bit or 32-bit integers) for speed and memory; these can overflow, unlike Python's `int`. Remember that the unlimited size is a property of Python's built-in `int`, not of every integer type you will meet.
- `isinstance()` is commonly used to validate input: "is this argument a number or a list?".

**10. Practice**

1. Create a variable `apples = 12` and print its value and its type.
2. Print `2 ** 64`. Then print the same value written with an underscore separator as `18_446_744_073_709_551_616` and confirm both print the same number.
3. Write the values `255`, `0b11111111` and `0xFF` in one `print()` call. What do you see, and why?
4. Without running it, predict the output of `print(type(10 / 5))` and `print(type(10 // 5))`. Then run it.
5. Use `isinstance()` with a tuple of types to check whether `x = 3.5` is a number (either `int` or `float`).
6. Predict `isinstance(False, int)` and `type(False) == int`. Explain any difference.

**11. Interview questions**

- *What is the maximum value of an `int` in Python?* There is no fixed maximum. Python integers have arbitrary precision and are limited only by available memory.
- *What is the difference between `type()` and `isinstance()`?* `type(x)` returns the exact type of `x`. `isinstance(x, T)` returns `True` if `x` is an instance of `T` or of a subclass of `T`; it also accepts a tuple of types.
- *Does Python have a `long` type?* Not in Python 3. Python 2 had one; Python 3 merged it into `int`.
- *What does this print: `print(4 / 2)`?* `2.0`. The `/` operator always returns a `float`.
- *Is `type()` a function or a method?* It is a built-in function (technically it is also the class `type`, but you call it like a function here).

**12. Quick revision**

- Every value has a type; the variable is only a name for the value.
- `int` is a whole number with unlimited size; underscores and `0b`, `0o`, `0x` prefixes are allowed in literals.
- `type()` gives the exact type; `isinstance()` checks type including subclasses and accepts a tuple.
- `/` returns `float`; `//` between ints returns `int`.

---

## The Float Data Type

**Timestamp:** [1:00:14](https://www.youtube.com/watch?v=J9BI0jGOds8&t=3614s)

**Learning objectives:**

- Create `float` values, including values written in scientific notation.
- Explain, in simple terms, why `0.1 + 0.2` is not exactly `0.3`.
- Compare floats safely with `math.isclose()` and know when to use the `decimal` module instead.

**1. Intuition**

A `float` is a number with a fractional part: `3.14`, `-0.5`, `2.0`. The name comes from "floating point", because the decimal point can "float" to different positions, which lets one format store both very large and very small numbers.

Here is a school-maths analogy. The fraction one third is `0.3333...` forever; written in decimal you must cut it off somewhere, so the written value is slightly off. Computers store numbers in binary (base 2), and many decimal fractions that look short to us, such as `0.1`, are endless repeating fractions in binary. The computer must also cut them off, so it stores a very close neighbour of the number, not the number itself.

**2. Why does it exist?**

Integers cannot represent measurements such as height, price per kilogram, probabilities or learning rates. Computers need a compact format for a huge range of values (from about 1e-308 up to about 1e+308) in a fixed amount of memory, with fast arithmetic in hardware. Floating-point numbers, defined by the IEEE 754 standard, are the answer. The price is that most values are stored approximately.

**3. Technical explanation**

A Python `float` is a 64-bit "double precision" floating-point number (IEEE 754 binary64) on essentially all platforms. It stores a sign, an exponent and a 53-bit significand (the digits part), all in binary. Consequences:

- Only numbers that can be written as a fraction with a power of two in the denominator (such as `0.5`, `0.25`, `0.75`) are stored exactly. `0.1` is not one of them, so the stored value is a nearby binary fraction. Python prints the shortest decimal text that converts back to the same stored value, which is why `0.1` prints as `0.1` even though the stored number is slightly different.
- Each arithmetic operation may round its result. Tiny rounding errors can accumulate.
- A float has about 15 to 17 significant decimal digits of precision.
- Floats have limits: the largest finite value is about `1.8e308`. Results beyond it become `inf` (infinity) in many operations; some operations such as `**` raise `OverflowError` instead. There is also `nan` ("not a number"), which is not equal to anything, including itself.
- Unlike `int`, a `float` cannot grow: integers above `2**53` cannot all be represented as floats.

In the standard library, `math.isclose()` is an imported function (you must `import math` first) that tests whether two floats are close enough. The `decimal` module provides a `Decimal` type that stores decimal digits exactly, at a cost in speed.

**4. Syntax**

```text
name = decimal_literal
name = mantissa e exponent         (scientific notation, no spaces)
```

This is a pattern, not runnable code. For example `2.5e3` means 2.5 × 10^3 = 2500.0 and `1e-4` means 0.0001. A number is a `float` if it contains a decimal point or an `e`/`E` exponent.

```text
math.isclose(a, b, rel_tol=1e-09, abs_tol=0.0)
```

Again a pattern. `a` and `b` are the numbers to compare. `rel_tol` is the allowed relative difference (a fraction of the larger value); `abs_tol` is an allowed absolute difference, useful when comparing against zero. The default `rel_tol` is `1e-09`.

**5. Example 1 — Basic**

```python
price = 19.99
print(price, type(price))
print(3.0, 2.5e3, 1e-4)
print(0.5 + 0.25)
print(7 / 2, 2 ** 0.5)
print(float("3.5") + 1)
```

Output:

```text
19.99 <class 'float'>
3.0 2500.0 0.0001
0.75
3.5 1.4142135623730951
4.5
```

`2.5e3` is scientific notation for 2500.0, and Python prints it as a plain decimal. `0.5 + 0.25` is exact because both are sums of powers of two. `2 ** 0.5` is the square root of 2, which has infinitely many digits, so Python shows only the 17 significant digits a float can hold. `float("3.5")` converts text into a float.

**6. Example 2 — Practical**

Adding `0.1` ten times looks like it should reach exactly `1.0`. A safe comparison avoids depending on that.

```python
import math

subtotal = 0.0
for _ in range(10):
    subtotal += 0.1

print(subtotal)
print(subtotal == 1.0)
print(math.isclose(subtotal, 1.0))
print(abs(subtotal - 1.0) < 1e-9)
```

Output:

```text
0.9999999999999999
False
True
True
```

Line by line: `import math` makes the standard-library `math` module available. The loop uses `_` as a throwaway variable name (we do not need the loop counter). Each `+= 0.1` adds a slightly inexact value, and the tiny errors accumulate, so `subtotal` ends at `0.9999999999999999`. Direct comparison with `==` fails. `math.isclose(subtotal, 1.0)` returns `True` because the numbers differ by far less than the default relative tolerance of `1e-09`. The last line shows the manual equivalent: check that the absolute difference is smaller than a chosen small number.

**7. Example 3 — Edge case or common mistake**

The classic surprise:

```python
import math
from decimal import Decimal

print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
print(0.1 + 0.2 - 0.3)
print(f"{0.1:.20f}")
print(f"{0.5:.20f}")
print(Decimal(0.1))
print(math.isclose(0.1 + 0.2, 0.3))
print(Decimal("0.1") + Decimal("0.2"))
print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))
print(math.isclose(0.0, 1e-12))
print(math.isclose(0.0, 1e-12, abs_tol=1e-9))
```

Output:

```text
0.30000000000000004
False
5.551115123125783e-17
0.10000000000000000555
0.50000000000000000000
0.1000000000000000055511151231257827021181583404541015625
True
0.3
True
False
True
```

What this shows, line by line:

- `0.1 + 0.2` gives `0.30000000000000004`, and the equality with `0.3` is `False`. This is not a Python bug. The same result occurs in any language that uses IEEE 754 doubles (JavaScript, Java, C and others).
- `f"{0.1:.20f}"` asks for 20 digits after the decimal point (formatting is covered in [Chapter 09](09-string-formatting-and-f-strings.md)). It reveals that the stored value of `0.1` is slightly above 0.1. `0.5` is stored exactly.
- `Decimal(0.1)` prints the exact stored value, all 55 digits of it.
- `math.isclose()` says the two sums are close, which is almost always the question you actually want to ask.
- With the `decimal` module, `Decimal("0.1") + Decimal("0.2")` is exactly `Decimal("0.3")`. Pass strings to `Decimal`, not floats; `Decimal(0.1)` copies the inexact float.
- The last two lines show a pitfall of `isclose()`: comparing with zero fails with only a relative tolerance, because the relative difference to zero is always 100 percent. Supply `abs_tol` when one value may be zero.

Use `decimal.Decimal` when exact decimal digits matter (for example money in accounting software), and use ordinary floats for scientific and machine-learning computations, where small rounding errors are acceptable and speed matters. The `decimal` module is only mentioned here; a full treatment is beyond this chapter.

**8. Common mistakes**

- Comparing floats with `==`. Use `math.isclose()` or an absolute-difference check.
- Using `isclose()` against `0.0` without `abs_tol`.
- Building `Decimal` from a float (`Decimal(0.1)`) instead of a string (`Decimal("0.1")`).
- Expecting `round(2.675, 2)` to return `2.68`. It returns `2.67` because the stored value is slightly below 2.675. `round()` is a built-in function that works on the stored value, not the text you typed.
- Assuming `nan == nan` is `True`. It is `False`; use `math.isnan(x)`.
- Believing huge integers convert to floats without loss. `float(2 ** 53 + 1)` is `9007199254740992.0`, not `...993.0`.
- Using `int()` to round. `int(3.9)` gives `3` and `int(-3.9)` gives `-3`: it truncates toward zero.

**9. Real-world and AI applications**

- Almost all machine-learning quantities are floats: model weights, activations, learning rates, loss values, probabilities and embedding vectors. Libraries such as NumPy and PyTorch also offer smaller floats (16-bit and 32-bit) to save memory; they have even less precision than Python's 64-bit `float`.
- Tests of numeric code use tolerance comparisons (`math.isclose()`, or `numpy.isclose()` and `numpy.allclose()` in NumPy) instead of `==`.
- Running totals of many floats can drift. The standard-library function `math.fsum()` sums floats with extra care to reduce that error.
- Money and billing code generally uses `Decimal` or integers (cents) to avoid fractional-penny errors.

**10. Practice**

1. Print `0.1 + 0.1 + 0.1` and print whether it equals `0.3`. Explain the result.
2. Write `1.5e3`, `2e-2` and `-4.0E1` as plain decimal numbers by printing them.
3. Use `math.isclose()` to test whether `0.1 * 3` is close to `0.3`.
4. Write a function `nearly_equal(a, b)` that returns `True` when `abs(a - b) < 1e-9`. Test it with `0.1 + 0.2` and `0.3`.
5. Use `Decimal` to compute `1.10 + 2.20` exactly, then compare it with the float result `1.10 + 2.20`.
6. Explain why `math.isclose(0.0, 1e-12)` is `False` and show how to make it `True`.

**11. Interview questions**

- *Why is `0.1 + 0.2 != 0.3` in Python?* Floats are binary fractions; `0.1` and `0.2` cannot be stored exactly, so their sum differs from the stored `0.3` by a tiny amount.
- *How do you compare floats safely?* Use `math.isclose(a, b)` with suitable tolerances, or compare `abs(a - b)` to a small threshold.
- *When would you use `Decimal` instead of `float`?* When you need exact decimal arithmetic, for example money.
- *What is `float("nan") == float("nan")`?* `False`. Use `math.isnan()`.
- *What precision does a Python float have?* About 15 to 17 significant decimal digits (IEEE 754 double precision).
- *Code: what does `int(-3.9)` give?* `-3`; `int()` truncates toward zero.

**12. Quick revision**

- `float` is an IEEE 754 double: fast and wide-ranging, but usually approximate.
- Never test floats for exact equality; use `math.isclose()` (with `abs_tol` near zero).
- `Decimal` (from the `decimal` module, built from strings) gives exact decimal arithmetic at lower speed.
- `/` returns floats; `int()` truncates toward zero; floats above `2**53` skip integers.

---

## Complex Numbers

**Timestamp:** [1:03:13](https://www.youtube.com/watch?v=J9BI0jGOds8&t=3793s)

**Learning objectives:**

- Write complex numbers with the `j` suffix and read their `real` and `imag` parts.
- Do arithmetic with complex numbers and use `abs()` for the magnitude.
- Know the limits: no ordering comparisons, and `math.sqrt()` does not accept negative numbers (use `cmath`).

**1. Intuition**

A complex number has two parts: a real part and an imaginary part. Mathematicians define the imaginary unit `i` as the square root of -1. It lets you solve equations such as x² + 1 = 0 that have no answer among ordinary numbers. A complex number can be pictured as a point on a flat map, with the real part as the east-west position and the imaginary part as the north-south position.

**2. Why does it exist?**

Many scientific and engineering fields need complex numbers: electrical engineering (alternating current), signal processing (the Fourier transform), quantum mechanics and control systems. Python supports them directly so that these calculations do not need extra libraries for the basics. Most everyday programs, and most beginner machine-learning code, never use complex numbers, so treat this topic as short and good to know.

**3. Technical explanation**

- Python writes the imaginary unit as `j` (engineering style), not `i`. The imaginary part is written with a `j` suffix directly after a number: `4j`. There must be no space and a number must precede the `j`, so write `1j`, not `j`. A bare `j` is a variable name, and Python will raise `NameError` if it does not exist.
- A complex number `3 + 4j` is stored as two floats, so both parts are always `float` values: `(3+4j).real` is `3.0`.
- The built-in function `abs(z)` returns the magnitude, the distance from the origin: for `3+4j` it is `5.0` (the 3-4-5 right triangle).
- The method `z.conjugate()` returns the complex number with the sign of the imaginary part flipped.
- Complex numbers support `+`, `-`, `*`, `/` and `**`, but not ordering comparisons (`<`, `>`). They can be tested for equality.
- The `math` module functions reject negative square roots; the standard-library `cmath` module offers complex-aware versions.

**4. Syntax**

```text
z = real_part + imaginary_part j
z = complex(real, imag)
```

This is a pattern, not runnable code. `complex(real, imag)` is a built-in constructor (a built-in type used like a function). `z.real` and `z.imag` are attributes (stored values, accessed with a dot and no parentheses), and `z.conjugate()` is a method (a function attached to the value, called with parentheses).

**5. Example 1 — Basic**

```python
z = 3 + 4j
print(z, type(z))
print(z.real, z.imag)
print(abs(z))
print(z.conjugate())
print(complex(2, 5))
```

Output:

```text
(3+4j) <class 'complex'>
3.0 4.0
5.0
(3-4j)
(2+5j)
```

Python prints complex numbers in parentheses. `z.real` and `z.imag` are floats. `abs(z)` is the magnitude, the square root of 3² + 4². `complex(2, 5)` builds `2+5j` another way.

**6. Example 2 — Practical**

```python
a = 1 + 2j
b = 3 - 1j

print(a + b)
print(a * b)
print(a / b)
print(1j * 1j)
print((a * b).real, (a * b).imag)
print(2 + 0j == 2)
```

Output:

```text
(4+1j)
(5+5j)
(0.1+0.7000000000000001j)
(-1+0j)
5.0 5.0
True
```

Line by line: addition and subtraction work on the real and imaginary parts separately. Multiplication follows the usual algebra with `j * j = -1`: `(1+2j)(3-1j) = 3 - j + 6j - 2j² = 5 + 5j`. `1j * 1j` is `-1`, which is the defining property of the imaginary unit. Division is also defined; the exact answer is `0.1+0.7j`, but the parts are floats, so Python prints `0.1+0.7000000000000001j` (the same rounding effect described in [The Float Data Type](#the-float-data-type)). The last line shows that a complex number whose imaginary part is zero is equal to the corresponding real number.

**7. Example 3 — Edge case or common mistake**

```python
import cmath
import math

z = 3 + 4j
try:
    print(z < 2j)
except TypeError as error:
    print("TypeError:", error)

try:
    print(math.sqrt(-1))
except ValueError as error:
    print("ValueError:", error)

print(cmath.sqrt(-1))
print((-1) ** 0.5)

try:
    print(3 + j)
except NameError as error:
    print("NameError:", error)

print(3 + 1j)
```

Output:

```text
TypeError: '<' not supported between instances of 'complex' and 'complex'
ValueError: math domain error
1j
(6.123233995736766e-17+1j)
NameError: name 'j' is not defined
(3+1j)
```

- Complex numbers have no natural order (is `3+4j` bigger than `2j`?), so `<` raises `TypeError`. To order them, compare something specific, such as `abs(z)`.
- `math.sqrt(-1)` raises `ValueError` because `math` works with real numbers only. `cmath.sqrt(-1)` returns `1j`. Here `math` and `cmath` are imported modules and `sqrt` is an imported function from each.
- `(-1) ** 0.5` gives `(6.123233995736766e-17+1j)`: a real part that is almost, but not exactly, zero. This is floating-point rounding again ([The Float Data Type](#the-float-data-type)). `cmath.sqrt(-1)` is cleaner for this purpose.
- `3 + j` fails because `j` alone is a name; write `1j`.

**8. Common mistakes**

- Using `i` instead of `j`.
- Writing `j` without a leading number, or with a space (`3 + 4 j` is a `SyntaxError`).
- Using `<` or `>` on complex numbers.
- Using `math.sqrt()` for negative inputs; use `cmath.sqrt()`.
- Forgetting that `real` and `imag` are attributes, so no parentheses: `z.real`, not `z.real()`.

**9. Real-world and AI applications**

- Signal processing and audio analysis use the Fourier transform, whose results are complex numbers; libraries such as NumPy (`numpy.fft`) return complex arrays.
- Some positional encodings and rotation-based techniques in machine learning can be described with complex numbers, but you will rarely write `3 + 4j` in everyday AI code. Awareness is enough at this stage.
- Electrical-engineering simulations and physics code use complex numbers directly.

**10. Practice**

1. Create `z = 5 - 12j`. Print its real part, imaginary part and magnitude.
2. Compute `(2 + 3j) * (2 - 3j)` and print the result. What do you notice about the imaginary part?
3. Use `cmath.sqrt()` to find the square root of `-9`.
4. Predict the output of `print(type((1 + 2j).real))`, then run it.
5. Write the expression that raises a `TypeError` by comparing two complex numbers, and catch it with `try`/`except`.

**11. Interview questions**

- *How do you write the imaginary unit in Python?* As `1j` (or any number followed by `j`), not `i`.
- *What type are the real and imaginary parts of a complex number?* Both are `float`.
- *Can you sort a list of complex numbers?* Not directly, because ordering comparisons are not defined; sort with a key such as `abs`.
- *What does `abs(3 + 4j)` return?* `5.0`, the magnitude.

**12. Quick revision**

- `complex` numbers use the `j` suffix; `real` and `imag` are float attributes.
- Arithmetic works; ordering comparisons raise `TypeError`; equality works.
- `abs()` gives magnitude; `cmath` handles square roots and functions of negative or complex inputs.

---

## The Boolean Data Type

**Timestamp:** [1:06:20](https://www.youtube.com/watch?v=J9BI0jGOds8&t=3980s)

**Learning objectives:**

- Use the two boolean values `True` and `False` and understand that `bool` is a subclass of `int`.
- Predict the truthiness of any value: which values count as false in a condition.
- Avoid the common pitfalls with `bool()` on strings and with lowercase `true`.

**1. Intuition**

A boolean answers a yes/no question: is the light on, is the password correct, is the number greater than 10. There are exactly two boolean values, `True` and `False`. They are named after George Boole, the mathematician who developed the algebra of logic.

**2. Why does it exist?**

Programs make decisions, and every decision boils down to a yes/no answer. Conditions in `if` statements and loops ([Chapter 14](14-conditional-statements.md), [Chapter 16](16-while-loop-and-loop-control.md)) need a value that means "go ahead" or "stop". A dedicated type for this keeps code readable and lets comparisons (`5 > 3`) produce a clear result.

**3. Technical explanation**

- `True` and `False` are built-in constants and keywords. They must start with a capital letter. `true` is just an unknown name.
- `bool` is a subclass of `int`. `True` behaves as the integer `1` and `False` as `0` in arithmetic: `True + True` is `2`. This is why `isinstance(True, int)` is `True`. The class hierarchy can be shown with `bool.__mro__` (method resolution order: the chain of classes Python searches), which lists `bool`, then `int`, then `object`.
- Comparison operators (`==`, `<`, `>` and so on) return `bool` values.
- Truthiness: when a non-boolean value is used where a condition is expected, Python converts it with `bool()`. The following are false ("falsy"): `False`, `None`, zero of any numeric type (`0`, `0.0`, `0j`), and empty containers (`""`, `[]`, `()`, `{}`, `set()`, `range(0)`). Almost everything else is true ("truthy"), including non-zero numbers, non-empty strings (even `"False"` and `" "`) and non-empty lists (even `[0]`).
- `bool()` is the built-in type used as a function to convert any value to `True` or `False`.

**4. Syntax**

```text
flag = True
flag = False
flag = bool(value)
flag = left_value comparison_operator right_value
```

This is a pattern, not runnable code. `bool(value)` applies the truthiness rules above. A comparison such as `5 > 3` evaluates to `True`.

**5. Example 1 — Basic**

```python
print(True, False, type(True))
print(5 > 3, type(5 > 3))
print(10 == 10.0)
print(bool(0), bool(1), bool(-5), bool(0.0), bool(0.1))
print(bool(""), bool("False"), bool(" "))
print(bool([]), bool([0]), bool(None), bool(0j))
```

Output:

```text
True False <class 'bool'>
True <class 'bool'>
True
False True True False True
False True True
False True False False
```

Zero of any kind is false, any other number is true (even negative ones). The empty string is false, but `"False"` and `" "` (a single space) are non-empty strings and therefore true. A list with one item, even `[0]`, is true because it is not empty.

**6. Example 2 — Practical**

Because `bool` is a subclass of `int`, you can count how many items satisfy a condition by summing booleans, and you can test truthiness directly in an `if`.

```python
scores = [45, 80, 92, 30]
passed = sum(score >= 50 for score in scores)
print(passed)

print(sum([True, False, True, True]))
print(True + True, True * 10, False + 5)

username = ""
if username:
    print("Hello,", username)
else:
    print("Please enter a name")

print(True and 5, 0 or "default")
print(not 0, not "hello")
print([10, 20, 30][True])
```

Output:

```text
2
3
2 10 5
Please enter a name
5 default
True False
20
```

Line by line: `score >= 50 for score in scores` produces one boolean per score (a generator expression, introduced properly in [Chapter 20](20-list-comprehension.md)); `sum()` adds them as 1s and 0s, so `passed` is 2. `if username:` uses truthiness, and an empty string is falsy, so the `else` branch runs. `True and 5` returns `5` and `0 or "default"` returns `"default"` because `and` / `or` return one of their operands, not necessarily a boolean (see [Chapter 12](12-relational-logical-assignment-operators.md)). `not` always returns a real `bool`. The last line works because `True` is the integer `1`, so `[10, 20, 30][True]` is `[10, 20, 30][1]`; this is legal but poor style, shown only to illustrate that `bool` is an `int`.

**7. Example 3 — Edge case or common mistake**

```python
print(bool("False"))
print(isinstance(True, bool), isinstance(True, int))
print(type(True) is int, type(True) is bool)
print(True == 1, False == 0)

try:
    print(true)
except NameError as error:
    print("NameError:", error)

print(type(None), bool(None))
```

Output:

```text
True
True True
False True
True True
NameError: name 'true' is not defined
<class 'NoneType'> False
```

- `bool("False")` is `True`: the string has characters in it, so it is truthy. Converting text to a boolean with `bool()` does not read the word. To interpret user text such as `"yes"` or `"False"`, compare it yourself, for example `answer.strip().lower() in ("true", "yes", "1")`.
- `True == 1` is `True` because they compare equal as numbers, yet `type(True) is int` is `False` because the exact type is `bool`. This is the `type()` versus `isinstance()` distinction from [Data Types and Integers](#data-types-and-integers).
- `true` (lowercase) is not a Python keyword, so the name is undefined and `NameError` occurs.
- `None` is its own type (`NoneType`) and is falsy.

**8. Common mistakes**

- Writing `true` or `false` in lowercase.
- Using `bool("False")` or `bool("0")` to parse text. Any non-empty string is truthy.
- Writing `if flag == True:`; write `if flag:` instead. Similarly, `if not items:` is the usual way to test for an empty list, but remember that `0`, `""` and `[]` are all falsy, so be explicit when the difference matters.
- Forgetting that `0.0` and `0j` are falsy, not only the integer `0`.
- Treating `None` as `False` when `None` means "no value yet". Test `value is None` when you need to tell them apart.
- Doing arithmetic with booleans accidentally and not noticing, since `True + 1` is `2` without error.

**9. Real-world and AI applications**

- Conditions in every program: validation (`is_valid`), feature flags, "is the user logged in".
- Truthiness is used to test emptiness: `if results:`, `while queue:`.
- In data and AI code, comparisons produce boolean masks (arrays of `True`/`False`) used to filter data, for example "keep rows where the score is at least 0.8". Summing booleans counts matches, which is how accuracy-style metrics are computed: correct predictions divided by total predictions.
- Boolean settings appear in model and API configuration, for example a flag to turn streaming of a response on or off.

**10. Practice**

1. Print `bool(x)` for each of `x` in `0`, `-1`, `0.0`, `"0"`, `""`, `[]`, `[[]]`, `None`. Predict first.
2. Given `values = [3, 0, 7, 0, 0, 5]`, count how many values are non-zero using `sum()` and a comparison.
3. Without running it, predict `True + True + False`, `True * 3` and `False - 1`.
4. Write `if` code that prints `"empty"` when a list is empty and `"has items"` otherwise, using truthiness (no `len()`).
5. Write a small function `parse_bool(text)` that returns `True` for `"true"`, `"yes"` or `"1"` (any letter case, ignoring surrounding spaces) and `False` otherwise.
6. Explain the difference between `type(True) == int` and `isinstance(True, int)`.

**11. Interview questions**

- *Is `bool` a subclass of `int`?* Yes. `True` is `1` and `False` is `0` in arithmetic, and `isinstance(True, int)` is `True`.
- *Which values are falsy in Python?* `False`, `None`, zero of any numeric type, and empty containers such as `""`, `[]`, `()`, `{}` and `set()`.
- *What does `bool("False")` return?* `True`, since the string is non-empty.
- *What does `print(True + True)` print?* `2`.
- *What is the difference between `1 == True` and `1 is True`?* The first is `True` (equal values); the second is `False` because they are different objects (identity is covered in [Chapter 13](13-identity-operators-and-precedence.md)).

**12. Quick revision**

- Only two bool values: `True` and `False`, capitalized.
- `bool` is a subclass of `int`: `True == 1`, `False == 0`, and they can be added.
- Falsy: `False`, `None`, zeros, empty containers; everything else is truthy.
- `bool("False")` is `True`; parse text explicitly.

---

## Answers to Practice Exercises

### Answers: Data Types and Integers

Exercise code for answers 1 to 6 together:

```python
apples = 12
print(apples, type(apples))

print(2 ** 64)
print(18_446_744_073_709_551_616)
print(2 ** 64 == 18_446_744_073_709_551_616)

print(255, 0b11111111, 0xFF)

print(type(10 / 5))
print(type(10 // 5))

x = 3.5
print(isinstance(x, (int, float)))

print(isinstance(False, int))
print(type(False) == int)
```

Output:

```text
12 <class 'int'>
18446744073709551616
18446744073709551616
True
255 255 255
<class 'float'>
<class 'int'>
True
True
False
```

1. `apples = 12` creates an `int`; `type()` reports `<class 'int'>`.
2. Both lines print `18446744073709551616`. The underscores in a literal exist only for human readability and are ignored. The equality check confirms it.
3. All three print `255`, because they are the same number written in decimal, binary and hexadecimal. `print()` always displays integers in decimal.
4. `10 / 5` is `2.0`, a `float`, because `/` always returns a float. `10 // 5` is `2`, an `int`, because floor division of two ints returns an int.
5. `isinstance(x, (int, float))` returns `True` since `3.5` is a `float`; the tuple means "either type".
6. `isinstance(False, int)` is `True` because `bool` is a subclass of `int`; `type(False) == int` is `False` because the exact type is `bool`.

### Answers: The Float Data Type

```python
import math
from decimal import Decimal

print(0.1 + 0.1 + 0.1)
print(0.1 + 0.1 + 0.1 == 0.3)

print(1.5e3, 2e-2, -4.0E1)

print(math.isclose(0.1 * 3, 0.3))


def nearly_equal(a, b):
    return abs(a - b) < 1e-9


print(nearly_equal(0.1 + 0.2, 0.3))

print(Decimal("1.10") + Decimal("2.20"))
print(1.10 + 2.20)
print(Decimal("1.10") + Decimal("2.20") == Decimal("3.30"))

print(math.isclose(0.0, 1e-12))
print(math.isclose(0.0, 1e-12, abs_tol=1e-9))
```

Output:

```text
0.30000000000000004
False
1500.0 0.02 -40.0
True
True
3.30
3.3000000000000003
True
False
True
```

1. The sum is `0.30000000000000004`, not `0.3`, so `==` gives `False`. Each of the three `0.1` values is stored with a tiny error, and the errors add up to a value slightly above the stored `0.3`.
2. Scientific notation prints as `1500.0`, `0.02` and `-40.0`. Results are always floats.
3. `math.isclose(0.1 * 3, 0.3)` is `True`; the difference is far below the default relative tolerance.
4. `nearly_equal` compares the absolute difference against `1e-9`. This is simple and works for numbers of moderate size; for very large or very small numbers, a relative tolerance as used by `math.isclose()` is better.
5. With strings, `Decimal` gives exactly `3.30`, while the float sum prints `3.3000000000000003`. The `Decimal` comparison with `Decimal("3.30")` is `True`.
6. `isclose()` uses a relative tolerance by default. Relative to zero, any non-zero difference is huge, so it returns `False`. Passing `abs_tol=1e-9` allows an absolute difference up to that size, so it returns `True`.

### Answers: Complex Numbers

```python
import cmath

z = 5 - 12j
print(z.real, z.imag, abs(z))

print((2 + 3j) * (2 - 3j))

print(cmath.sqrt(-9))

print(type((1 + 2j).real))

try:
    print((1 + 2j) < (3 + 4j))
except TypeError as error:
    print("TypeError:", error)
```

Output:

```text
5.0 -12.0 13.0
(13+0j)
3j
<class 'float'>
TypeError: '<' not supported between instances of 'complex' and 'complex'
```

1. The real part is `5.0`, the imaginary part is `-12.0`, and the magnitude is `13.0` (the 5-12-13 right triangle).
2. A number multiplied by its conjugate gives a purely real result: `(a+bj)(a-bj) = a² + b²`, here `13`. Python shows it as `(13+0j)` because the type stays `complex`.
3. `cmath.sqrt(-9)` is `3j`, since `(3j)² = -9`.
4. The real part of a complex number is a `float`: `<class 'float'>`.
5. Ordering comparisons between complex numbers raise `TypeError`, which the `try`/`except` catches.

### Answers: The Boolean Data Type

```python
for x in (0, -1, 0.0, "0", "", [], [[]], None):
    print(repr(x), bool(x))

values = [3, 0, 7, 0, 0, 5]
print(sum(value != 0 for value in values))

print(True + True + False, True * 3, False - 1)

items = []
if items:
    print("has items")
else:
    print("empty")


def parse_bool(text):
    return text.strip().lower() in ("true", "yes", "1")


print(parse_bool(" Yes "), parse_bool("TRUE"), parse_bool("no"), parse_bool("False"))
```

Output:

```text
0 False
-1 True
0.0 False
'0' True
'' False
[] False
[[]] True
None False
3
2 3 -1
empty
True True False False
```

1. `0` and `0.0` are false; `-1` is true; `"0"` is a non-empty string and so is true; `""` and `[]` are false; `[[]]` is a list containing one item (an empty list), so it is non-empty and true; `None` is false.
2. `value != 0` produces a boolean for each value; `sum()` counts the `True` results, giving `3`.
3. `True + True + False` is `1 + 1 + 0 = 2`; `True * 3` is `3`; `False - 1` is `-1`.
4. `if items:` is false for an empty list, so `"empty"` is printed.
5. `parse_bool` removes surrounding spaces with `strip()`, lowercases the text with `lower()`, and checks membership in a tuple of accepted words. Anything else, including `"False"` and `"no"`, gives `False`. (The `in` operator is covered for strings in [Chapter 06](06-strings-basics-indexing-concatenation.md#string-basics).)
6. `type(True) == int` is `False` because the exact type of `True` is `bool`. `isinstance(True, int)` is `True` because `bool` is a subclass of `int`, and `isinstance()` accepts subclasses.

---

## Chapter Summary and Key Takeaways

- Every value has a type; variables are only names. `type()` returns the exact type and `isinstance()` also accepts subclasses and tuples of types.
- `int` has arbitrary precision: no overflow, limited only by memory. Literals may use underscores and `0b`, `0o`, `0x` prefixes.
- `float` is a 64-bit IEEE 754 binary number and is usually approximate. `0.1 + 0.2` is `0.30000000000000004`. Compare floats with `math.isclose()` (add `abs_tol` near zero); use `Decimal` built from strings when exact decimal digits matter.
- `complex` numbers use `j`, have `float` real and imaginary parts, support arithmetic and `abs()`, but cannot be ordered. Use `cmath` for square roots of negatives.
- `bool` is a subclass of `int` with the two values `True` and `False`. Falsy values: `False`, `None`, zeros and empty containers. `bool("False")` is `True`.

Next: [Chapter 06 — Strings: Basics, Indexing, Concatenation and Repetition](06-strings-basics-indexing-concatenation.md) covers how text is written, read by position, joined and repeated.
