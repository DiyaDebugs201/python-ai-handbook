# Chapter 03 — Built-in Functions, print() and Modules

> Part 1 — Python Fundamentals · Video: 29:18–38:20 · Previous: [02 Installation and Environment Setup](02-installation-and-environment-setup.md) · Next: [04 Errors and Identifiers](04-errors-and-identifiers.md)

**In this chapter:** what a function is and how to call one, `print()` and its options, a tour of the most useful built-in functions, the `math` module, the three common ways to import, and a comparison of built-in functions, methods and imported functions.

**Before you start:** you need to be able to run Python code, either in the REPL or from a file (see [Running Python in the Terminal and IDLE](02-installation-and-environment-setup.md#running-python-in-the-terminal-and-idle)). Recap: a variable is a name that refers to a value, written `name = value`. Text in quotes is a string. A comment starts with `#` and is ignored by Python. Examples were run with Python 3.13; anything that depends on the version is called out.

---

## Built-in Functions and print()

**Timestamp:** [29:18](https://www.youtube.com/watch?v=J9BI0jGOds8&t=1758s)

**Learning objectives:**

- Explain what a function call is: name, parentheses, arguments, result.
- Use `print()` with several values and with its `sep` and `end` options.
- Use common built-ins: `type()`, `len()`, `abs()`, `round()`, `min()`, `max()`, `sum()`, `sorted()`, `pow()`, `divmod()`, `input()`.
- Know that built-ins are always available and that you should not reuse their names for your own variables.

**1. Intuition**

A function is a named, ready-made mini-machine. You hand it some inputs (arguments), it does a job, and it may hand a result back. A kettle is a useful picture: you give it water, press the button, and it gives you hot water. You do not need to know how the heating element works. A built-in function is a machine that Python supplies in every program without you installing or importing anything.

**2. Why does it exist?**

Many jobs come up in every program: show a value, find the length of a text, find the biggest number, convert a number to text. If each programmer wrote these from scratch, programs would be longer and full of mistakes. Built-in functions give everyone the same tested tools.

**3. Technical explanation**

To use a function you call it: write its name, then parentheses, with the arguments inside, separated by commas. `len("hello")` calls the function `len` with one argument. The call is an expression: it produces a value (here `5`) that you can print, store in a variable or use inside a larger expression.

Python has about seventy built-in functions. They live in a special place that Python searches automatically, which is why `print` works without an import. You can list them with `dir(__builtins__)` or read the official [built-in functions reference](https://docs.python.org/3/library/functions.html).

`print()` writes text to the screen (more exactly, to standard output). It accepts any number of values, converts each to text with `str()`, and writes them separated by a space, followed by a newline. Two keyword options change this:

- `sep` sets the separator placed between values (default: one space).
- `end` sets what is written at the very end (default: a newline `"\n"`).

There are two more options you will meet less often: `file` (where to write, default the screen) and `flush` (whether to force the text out immediately).

An important point: `print()` shows values; it does not return them. The result of a `print()` call is `None`, Python's "nothing" value. You will see why that matters in [Return Functions versus Void Functions](25-defining-functions-and-return-values.md#return-functions-versus-void-functions).

**4. Syntax**

```text
function_name(argument1, argument2, ..., keyword=value)
print(value1, value2, ..., sep=" ", end="\n", file=sys.stdout, flush=False)
```

This is a pattern, not runnable code. Positional arguments are matched by position. Keyword arguments are written as `name=value` and are matched by name; for `print`, `sep`, `end`, `file` and `flush` can only be given as keywords.

**5. Example 1 — Basic**

```python
print("Hello")
print("Python", "is", "fun")
print(10, 20, 30, sep=", ")
print("loading", end="...")
print("done")
print()
print("after an empty print")
```

Output:

```text
Hello
Python is fun
10, 20, 30
loading...done

after an empty print
```

Line by line:

- The first call prints one string and moves to a new line.
- The second call prints three strings with a space between them.
- `sep=", "` replaces the space with a comma and a space. Numbers are converted to text automatically.
- `end="..."` replaces the newline with three dots, so the next `print` continues on the same line.
- `print()` with no arguments prints just a newline, which creates an empty line.

**6. Example 2 — Practical**

A short report using several built-ins together. The marks are hard-coded so that the output is always the same.

```python
marks = [72, 58, 91, 66, 85]

print("Number of marks:", len(marks))
print("Highest:", max(marks))
print("Lowest:", min(marks))
print("Total:", sum(marks))
print("Average:", sum(marks) / len(marks))
print("Sorted:", sorted(marks))
print("Rounded average:", round(sum(marks) / len(marks)))
print("Distance from 70:", abs(58 - 70))
print("Type of marks:", type(marks))
print("Type of average:", type(sum(marks) / len(marks)))
```

Output:

```text
Number of marks: 5
Highest: 91
Lowest: 58
Total: 372
Average: 74.4
Sorted: [58, 66, 72, 85, 91]
Rounded average: 74
Distance from 70: 12
Type of marks: <class 'list'>
Type of average: <class 'float'>
```

Line by line:

- `marks` is a list, an ordered collection in square brackets (lists are covered in [Lists in Python](18-lists-fundamentals.md#lists-in-python)).
- `len()` counts items; `max()` and `min()` find the biggest and smallest; `sum()` adds them up.
- `sum(marks) / len(marks)` is the mean. The `/` operator always gives a floating-point number.
- `sorted()` returns a new sorted list and leaves `marks` unchanged.
- `round()` with one argument rounds to the nearest integer. `abs()` removes the sign of a number.
- `type()` tells you what kind of object a value is.

More built-ins worth knowing now:

```python
print(pow(2, 10))
print(divmod(17, 5))
print(int("42") + 1)
print(str(42) + "!")
print(float("3.5") * 2)
print(round(3.14159, 2))
print(len("hello"))
print(max("apple", "banana"))
```

Output:

```text
1024
(3, 2)
43
42!
7.0
3.14
5
banana
```

`pow(2, 10)` is 2 to the power of 10. `divmod(17, 5)` returns the quotient and remainder together as a pair `(3, 2)`. `int()`, `str()` and `float()` convert between types (this is the subject of [Explicit Type Casting](08-type-conversion.md#explicit-type-casting)). `max()` also works on strings, comparing them alphabetically.

Reading input is done with `input()`, which pauses and waits for the user to type a line:

```python
name = input("What is your name? ")
print("Hello,", name)
```

Because this needs a person at the keyboard, it is not run here. A session might look like this (your typing is on the first line):

```text
What is your name? Asha
Hello, Asha
```

Remember that `input()` always returns a string, even if the user types digits.

**7. Example 3 — Edge case or common mistake**

Three well-known surprises.

First, `print()` returns `None`:

```python
result = print("hello")
print(result)
print(type(result))
```

Output:

```text
hello
None
<class 'NoneType'>
```

The first line was written by the `print("hello")` call itself. The variable `result` holds `None`, because `print()` has nothing to give back. A beginner who writes `total = print(a + b)` will be surprised that `total` is empty.

Second, `round()` does not always round halves up. Python rounds exact halves to the nearest even number:

```python
print(round(0.5), round(1.5), round(2.5), round(3.5))
print(round(2.675, 2))
```

Output:

```text
0 2 2 4
2.67
```

The first line shows "round half to even" (also called banker's rounding), which avoids always rounding in the same direction. The second result, `2.67`, surprises people who expect `2.68`: the number `2.675` cannot be stored exactly in binary, and the stored value is slightly below 2.675 (see [The Float Data Type](05-numeric-types-and-booleans.md#the-float-data-type)).

Third, you can accidentally overwrite a built-in by using its name for a variable. This is legal Python but causes confusing errors later:

```python
list = [3, 1, 2]
letters = list("abc")
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 2, in <module>
    letters = list("abc")
TypeError: 'list' object is not callable
```

After the first line, the name `list` refers to your list and no longer to the built-in function that creates lists. Calling it fails, because a list is not callable. The fix is to use a different variable name such as `numbers`, and to restart your REPL or notebook if you made this mistake there.

**8. Common mistakes**

- Forgetting the parentheses. `print "hello"` was valid in Python 2; in Python 3 it is a `SyntaxError`. Write `print("hello")`.
- Writing `len` without parentheses. `len` alone is the function object; `len(x)` is a call.
- Using names such as `list`, `str`, `sum`, `max`, `min`, `id`, `type`, `input` or `print` for your own variables.
- Expecting `input()` to return a number. Convert it: `age = int(input("Age: "))`.
- Believing `print()` produces a value. It prints; it returns `None`.
- Mismatching quotes in strings, such as `print("hello')`.

**9. Real-world and AI applications**

`print()` is the first debugging tool in nearly every language: print a variable to see what it holds. Professional projects also use the `logging` module for permanent diagnostics. In AI work, `print(len(data))`, `print(type(x))` and `print(max(scores))` are common first checks on a dataset. `sorted()` with a key is used to rank model outputs, and `sum()`/`len()` give averages for quick evaluation. `type()` helps when a library returns an unexpected kind of object.

**10. Practice**

1. Print the numbers 1, 2 and 3 on one line, separated by dashes.
2. Given `prices = [120, 80, 150, 95]`, print the cheapest, the most expensive, the total, and the average price rounded to one decimal place.
3. Print `"Loading"` followed by three dots and then `"Done"` on the same line, using only `print()` options.
4. Predict the output of `print(round(4.5), round(5.5), divmod(-7, 2))` and then run it.
5. A learner writes `max = max([4, 9, 2])` and later `max([1, 2])` fails. Explain why and fix it.

**11. Interview questions**

- *What is the difference between a function call and a function name?* The name refers to the function object; adding parentheses calls it and produces its result.
- *What does `print()` return?* `None`.
- *Why does `round(2.5)` give `2` in Python 3?* It rounds halves to the nearest even number.
- *What does `sep` do, and can you pass it positionally?* It sets the separator between values; it is keyword-only.

**12. Quick revision**

- A function call is `name(arguments)` and is an expression that produces a result.
- `print(*values, sep=" ", end="\n")` shows values; its own result is `None`.
- Core built-ins: `len`, `type`, `abs`, `round`, `min`, `max`, `sum`, `sorted`, `pow`, `divmod`, `int`, `str`, `float`, `input`.
- `round()` uses round-half-to-even; floats are stored in binary.
- Never reuse a built-in name for a variable.

---

## Python Modules: math and import

**Timestamp:** [35:42](https://www.youtube.com/watch?v=J9BI0jGOds8&t=2142s)

**Learning objectives:**

- Explain what a module is and why most tools are not built-in.
- Use `import module`, `import module as alias` and `from module import name`.
- Use several functions and constants from the `math` module.
- Explain why `from module import *` is discouraged and how to find what a module contains.

**1. Intuition**

Built-in functions are the tools hanging on the wall of every kitchen. Modules are specialised cupboards: a baking cupboard, a spice rack, a toolbox for measuring. They are stored away until you need one, and you open one with `import`. The `math` module is the cupboard for mathematics.

**2. Why does it exist?**

If Python loaded every tool at start-up, it would be slow and heavy, and names from different areas would clash. Modules keep related code together, load only when requested, and give names a home (`math.sqrt` versus `numpy.sqrt` are different tools that happen to share the name `sqrt`).

**3. Technical explanation**

A module is a file of Python code (or a compiled extension) that defines functions, constants and other objects. The standard library is the set of modules that ship with Python, such as `math`, `random`, `datetime`, `os`, `json` and `collections`. Third-party modules, installed with `pip`, work the same way once installed.

When Python runs `import math`, it does three things: it searches for a module named `math`, runs the module's code once, and creates a module object that it binds to the name `math` in your program. The module is cached, so importing it a second time is cheap. You then reach its contents with dot notation: `math.sqrt`, where the dot means "look inside this module".

The most-used contents of `math` (all available in Python 3.13; those marked were added in the stated version):

- Constants: `math.pi`, `math.e`, `math.inf`, `math.nan`, `math.tau`.
- `math.sqrt(x)` square root; `math.isqrt(n)` integer square root (3.8+).
- `math.floor(x)` and `math.ceil(x)` round down and up to an integer.
- `math.factorial(n)`, `math.gcd(a, b)`, `math.comb(n, k)` and `math.perm(n, k)` (the last two are 3.8+).
- `math.log(x)` natural logarithm, `math.log10(x)`, `math.log2(x)`, `math.exp(x)`.
- `math.sin`, `math.cos`, `math.tan` work in radians; `math.radians(deg)` converts.
- `math.isclose(a, b)` compares floats within a tolerance (see [The Float Data Type](05-numeric-types-and-booleans.md#the-float-data-type)).

**4. Syntax**

```text
import module_name
import module_name as alias
from module_name import name1, name2
from module_name import name as alias
```

This is a pattern, not runnable code.

- `import math` makes the module available as `math`. You write `math.sqrt(...)`.
- `import math as m` gives it a shorter name `m`. A few aliases are conventions in the community (for example `import numpy as np`).
- `from math import sqrt, pi` copies those names into your program so you can write `sqrt(...)` without `math.`.
- `from math import *` imports every public name. Avoid it: it hides where names come from and can silently overwrite your own names.

By convention, imports go at the top of the file, one per line, standard-library imports first.

**5. Example 1 — Basic**

```python
import math

print(math.sqrt(144))
print(math.pi)
print(math.floor(3.7), math.ceil(3.2))
print(math.factorial(5))
print(math.gcd(12, 18))
print(math.log10(1000))
print(math.isqrt(50))
```

Output:

```text
12.0
3.141592653589793
3 4
120
6
3.0
7
```

`math.sqrt` always returns a float (`12.0`). `math.floor(3.7)` gives 3 and `math.ceil(3.2)` gives 4. `math.factorial(5)` is 5 × 4 × 3 × 2 × 1. `math.gcd(12, 18)` is the greatest common divisor. `math.isqrt(50)` is the whole-number part of the square root of 50.

**6. Example 2 — Practical**

Area of a circle and distance between two points, using three import styles. The same module is imported three ways just to show them side by side; in real code pick one style.

```python
import math
import math as m
from math import sqrt, pi

radius = 5
area = math.pi * radius ** 2
print("Area:", round(area, 2))

point_a = (1, 2)
point_b = (4, 6)
distance = m.sqrt((point_b[0] - point_a[0]) ** 2 + (point_b[1] - point_a[1]) ** 2)
print("Distance:", distance)

print(sqrt(81), pi == math.pi)
print(m is math)
```

Output:

```text
Area: 78.54
Distance: 5.0
9.0 True
True
```

Line by line:

- `math.pi * radius ** 2` computes πr². The `**` operator means power and is evaluated before `*`.
- `round(area, 2)` keeps two decimal places.
- Points are written as tuples `(x, y)` and read by index. The distance uses the Pythagorean formula. (Tuples are covered in [Tuples](21-tuples.md#tuples).)
- `from math import sqrt, pi` lets the last line use `sqrt` and `pi` directly. `pi == math.pi` is `True` because both names refer to the same value.
- `m is math` is `True`: an alias is just another name for the same module object.

You can explore any module with `dir()` and `help()`:

```python
import math

print([name for name in dir(math) if name.startswith("is")])
print(math.sqrt.__doc__.splitlines()[0])
```

Output:

```text
['isclose', 'isfinite', 'isinf', 'isnan', 'isqrt']
Return the square root of x.
```

`dir(math)` lists the names inside the module; the comprehension keeps those starting with `is` (list comprehensions are explained in [List Comprehension](20-list-comprehension.md#list-comprehension)). `help(math.sqrt)` in the REPL shows the full documentation. Reading these is a habit of experienced programmers.

**7. Example 3 — Edge case or common mistake**

Three typical errors.

Using a module without importing it:

```python
print(math.sqrt(16))
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 1, in <module>
    print(math.sqrt(16))
          ^^^^
NameError: name 'math' is not defined. Did you forget to import 'math'?
```

Misspelling a name inside a module:

```python
import math

print(math.squareroot(16))
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 3, in <module>
    print(math.squareroot(16))
          ^^^^^^^^^^^^^^^
AttributeError: module 'math' has no attribute 'squareroot'
```

Passing a value outside a function's domain:

```python
import math

print(math.sqrt(-4))
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 3, in <module>
    print(math.sqrt(-4))
          ~~~~~~~~~^^^^
ValueError: math domain error
```

The first is a `NameError`: the name `math` was never defined. The second is an `AttributeError`: the module exists but has no attribute with that name; check the spelling with `dir(math)`. The third is a `ValueError`: the name is right, but the argument is not valid for real-number square roots. (Complex results come from the `cmath` module.)

A fourth, more subtle problem is shadowing a module with your own file. If your project folder contains a file named `math.py`, then `import math` may load your file instead of the standard module, and `math.sqrt` fails with an `AttributeError` even though your spelling is right. Rename your file.

**8. Common mistakes**

- Forgetting the import, then getting `NameError`.
- Writing `from math import sqrt` and then using `math.sqrt` (the name `math` was never bound).
- Using `from module import *` in real code.
- Giving your own file the same name as a standard-library module.
- Importing in the middle of a program for no reason; keep imports at the top.
- Forgetting that trig functions use radians, not degrees.
- Mistaking `import math` for a download. Standard-library modules are already installed; third-party modules must be installed with `pip` first, or you get `ModuleNotFoundError`.

**9. Real-world and AI applications**

Almost every real script begins with imports. Data and AI code imports `numpy` for arrays, `pandas` for tables and `torch` or `sklearn` for models, but the same rules apply as for `math`. The `math` module itself appears in learning-rate schedules, loss calculations (`math.log`, `math.exp`) and the softmax function you will build in [LLMs, Prompting, Temperature and Hallucination](31-llms-prompting-temperature-hallucination.md#temperature). `math.isclose` is the right way to compare floating-point results in tests.

**10. Practice**

1. Import `math` and print the square root of 2 to 4 decimal places.
2. Compute the hypotenuse of a right triangle with sides 3 and 4 using `math.sqrt`, then check it with `math.hypot(3, 4)`.
3. Print how many ways there are to choose 3 items from 10, using `math.comb`.
4. Write the same computation of `sqrt(49)` using each of the three import styles.
5. Explain why `from math import *` followed by `pi = 3` changes later results, and show it.

**11. Interview questions**

- *What is the difference between `import math` and `from math import sqrt`?* The first binds the module name; you write `math.sqrt`. The second binds only `sqrt` into your namespace.
- *What happens if you import a module twice?* The module's code runs only the first time; later imports reuse the cached module object.
- *Why is `import *` discouraged?* It hides where names come from and can overwrite existing names without warning.
- *How do you find what a module contains?* `dir(module)`, `help(module)` and the official documentation.

**12. Quick revision**

- A module is a file of reusable code; the standard library is the set that ships with Python.
- `import m`, `import m as x`, `from m import name`; avoid `import *`.
- `math` gives constants (`pi`, `e`) and functions (`sqrt`, `floor`, `ceil`, `factorial`, `gcd`, `log`, `isclose`, ...).
- `NameError` = missing import; `AttributeError` = misspelt or missing name; `ModuleNotFoundError` = module not installed.
- Never name your own file after a standard module.

---

## Built-in Functions, Methods, and Imported Functions Compared

This section is supplementary: the video topic list does not name it, but it removes a very common confusion.

**Timestamp:** supplementary section (not a separate video topic; it belongs with [Built-in Functions and print()](03-builtin-functions-print-and-modules.md#built-in-functions-and-print)).

**Learning objectives:**

- Tell a built-in function, a method and an imported module function apart by how they are called.
- Choose the right one for a small task and explain why it lives where it does.
- Read the error you get when you call the wrong kind in the wrong way.

**1. Intuition**

Three kinds of "doing words" look similar but live in different places:

- A built-in function stands alone: `len(text)`.
- A method belongs to an object and is called with a dot after it: `text.upper()`.
- An imported function lives in a module you must import first: `math.sqrt(16)`.

**2. Why does it exist?**

Python groups tools by where they logically belong. A string method such as `upper()` only makes sense for strings, so it lives on the string type. A mathematical function that works on numbers lives in the `math` module. A function useful everywhere (`len`, `print`) is built in.

**3. Technical explanation**

| Kind | How you call it | Where it comes from | Needs import? | Example |
|------|-----------------|---------------------|---------------|---------|
| Built-in function | `name(args)` | The builtins namespace, always searched | No | `len([1, 2])` |
| Method | `object.name(args)` | The object's type (class) | No (but you need the object) | `"abc".upper()` |
| Imported function | `module.name(args)` or `name(args)` after `from ... import` | A module | Yes | `math.sqrt(9)` |

A method is a function stored on a type, and it receives the object it is called on as its first argument automatically. `"abc".upper()` effectively does `str.upper("abc")`. Because methods belong to types, the same method name can behave differently on different types: `.count()` on a string counts substrings, and `.count()` on a list counts equal items.

You can tell what something is by asking Python:

```python
import math

print(type(len))
print(type("abc".upper))
print(type(math.sqrt))
print(type(math))
print(callable(len), callable(math.pi))
```

Output:

```text
<class 'builtin_function_or_method'>
<class 'builtin_function_or_method'>
<class 'builtin_function_or_method'>
<class 'module'>
True False
```

`len` and `math.sqrt` are both "built-in function" objects in CPython, because they are written in C, but they are found in different places. `"abc".upper` is a "built-in method": a function bound to the string `"abc"`. `math` itself is a module and `math.pi` is a plain number, which is not callable.

**4. Syntax**

```text
len(x)             built-in function: function(argument)
x.upper()          method: object.method(arguments)
math.sqrt(x)       imported function: module.function(arguments)
```

This is a pattern, not runnable code. The dot has two meanings that you can tell apart by what is on the left: an object (method or attribute) or a module (a name inside the module).

**5. Example 1 — Basic**

```python
import math

text = "python"
print(len(text))
print(text.upper())
print(math.sqrt(len(text) * 6))
print(text)
```

Output:

```text
6
PYTHON
6.0
python
```

`len` is a built-in function. `.upper()` is a string method. `math.sqrt` is an imported function. Notice the last line: `text.upper()` returned a new string and did not change `text`, because strings are immutable (see [String Basics](06-strings-basics-indexing-concatenation.md#string-basics)).

**6. Example 2 — Practical**

The same idea, "how many?", is expressed three different ways depending on the kind of object:

```python
words = ["tea", "coffee", "tea", "milk", "tea"]
sentence = "tea or coffee or tea"

print(len(words))
print(words.count("tea"))
print(sentence.count("tea"))
print(sentence.count("or"))
print(sorted(words))
words.sort()
print(words)
print(sorted(words) is words)
```

Output:

```text
5
3
2
2
['coffee', 'milk', 'tea', 'tea', 'tea']
['coffee', 'milk', 'tea', 'tea', 'tea']
False
```

`len(words)` is a built-in function applied to a list. `words.count("tea")` is a list method that counts equal items. `sentence.count("tea")` is a string method that counts substrings. `sorted(words)` is a built-in function that returns a new list; `words.sort()` is a method that sorts the list in place and returns `None`. The last line shows `sorted(...)` gives a different list object.

**7. Example 3 — Edge case or common mistake**

Calling a method as if it were a function, or the reverse:

```python
text = "python"
print(upper(text))
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 2, in <module>
    print(upper(text))
          ^^^^^
NameError: name 'upper' is not defined. Did you mean: 'super'?
```

```python
numbers = [3, 1, 2]
print(numbers.len())
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 2, in <module>
    print(numbers.len())
          ^^^^^^^^^^^
AttributeError: 'list' object has no attribute 'len'
```

`upper` is not a built-in function; it is a method of strings, so it must be called as `text.upper()`. `len` is a built-in function, not a list method, so it must be called as `len(numbers)`. The error messages are the clue: `NameError` says "no such name", `AttributeError` says "this object has no such method or attribute". When you are unsure, `dir(obj)` lists an object's methods.

**8. Common mistakes**

- Writing `upper(text)` or `text.len()`; check whether the tool is a function or a method.
- Assuming that a method changes the object. Strings are immutable, so their methods return new strings; list methods such as `sort()` and `append()` change the list and return `None`.
- Forgetting parentheses: `text.upper` is the method object, not the result.
- Calling `math.sqrt` after only writing `from math import sqrt`.

**9. Real-world and AI applications**

Reading library documentation is mostly this skill. In an AI project you will see all three kinds side by side: built-ins (`len(dataset)`), methods (`dataframe.head()`, `tensor.shape`, `text.strip()`), and imported functions (`json.loads(...)`, `random.shuffle(...)`). Knowing which kind you are looking at tells you where to look for the documentation and what to import.

**10. Practice**

1. Classify each as built-in function, method or imported function: `max(x)`, `s.lower()`, `random.randint(1, 6)`, `abs(-3)`, `my_list.append(4)`, `math.ceil(2.1)`.
2. Fix this code so it runs: `from math import sqrt` then `print(math.sqrt(9))`.
3. For the list `data = [5, 3, 8]`, show two ways to get a sorted version, and state which one changes `data`.
4. Use `dir("")` to find three string methods you have not seen, and read one with `help`.

**11. Interview questions**

- *Is `len` a method of lists?* No. It is a built-in function that works on any object that has a length.
- *What is the difference between a function and a method?* A method is a function attached to an object's type and called through the object; it receives the object as its first argument.
- *Why does `list.sort()` return `None`?* It sorts in place, and Python returns `None` from in-place operations to make the difference from `sorted()` obvious.

**12. Quick revision**

- Built-in: `name(x)`, always available. Method: `x.name()`, belongs to the type. Imported: `module.name(x)`, needs `import`.
- `NameError` suggests a missing name or import; `AttributeError` suggests a missing method.
- Strings never change; their methods return new values.
- `dir()` and `help()` answer "what can this do?"

---

## Answers to Practice Exercises

### Answers: Built-in Functions and print()

1.

```python
print(1, 2, 3, sep="-")
```

2.

```python
prices = [120, 80, 150, 95]
print("Cheapest:", min(prices))
print("Most expensive:", max(prices))
print("Total:", sum(prices))
print("Average:", round(sum(prices) / len(prices), 1))
```

Output:

```text
Cheapest: 80
Most expensive: 150
Total: 445
Average: 111.2
```

3.

```python
print("Loading", end="...")
print("Done")
```

The first call replaces the newline with `...`, so `Done` follows on the same line, giving `Loading...Done`.

4. `round(4.5)` is 4 and `round(5.5)` is 6 (half to even). `divmod(-7, 2)` is `(-4, 1)`, because `-4 * 2 + 1 == -7` (floor division rounds down).

```python
print(round(4.5), round(5.5), divmod(-7, 2))
```

Output:

```text
4 6 (-4, 1)
```

5. `max = max([4, 9, 2])` replaces the built-in name `max` with the number 9, so `max([1, 2])` tries to call a number. Fix: use another name, such as `highest = max([4, 9, 2])`.

### Answers: Python Modules: math and import

1.

```python
import math

print(round(math.sqrt(2), 4))
```

Output:

```text
1.4142
```

2.

```python
import math

print(math.sqrt(3 ** 2 + 4 ** 2))
print(math.hypot(3, 4))
```

Output:

```text
5.0
5.0
```

3.

```python
import math

print(math.comb(10, 3))
```

Output:

```text
120
```

4.

```python
import math
import math as m
from math import sqrt

print(math.sqrt(49), m.sqrt(49), sqrt(49))
```

Output:

```text
7.0 7.0 7.0
```

5. After `from math import *`, the name `pi` refers to the real constant. Assigning `pi = 3` rebinds the name in your program, so later calculations use 3 instead:

```python
from math import *

print(round(pi, 4))
pi = 3
print(pi * 2 ** 2)
```

Output:

```text
3.1416
12
```

The star import also made it impossible to see, from the code alone, that `pi` came from `math`. That is the main reason to avoid it.

### Answers: Built-in Functions, Methods, and Imported Functions Compared

1. `max(x)` built-in function; `s.lower()` method; `random.randint(1, 6)` imported function; `abs(-3)` built-in function; `my_list.append(4)` method; `math.ceil(2.1)` imported function.
2. Either `from math import sqrt` then `print(sqrt(9))`, or `import math` then `print(math.sqrt(9))`.
3. `sorted(data)` returns a new sorted list and does not change `data`; `data.sort()` sorts `data` itself and returns `None`.
4. For example `dir("")` includes `casefold`, `partition` and `zfill`. `help("".zfill)` explains that `zfill` pads a numeric string with zeros on the left.

---

## Chapter Summary and Key Takeaways

- A function call is `name(arguments)` and produces a value. `print()` shows values and returns `None`.
- Use `sep` and `end` to control `print()` output; `round()` rounds halves to even.
- Core built-ins (`len`, `type`, `abs`, `round`, `min`, `max`, `sum`, `sorted`, `pow`, `divmod`, `int`, `str`, `float`, `input`) are always available; do not shadow them.
- Modules hold related tools. Import with `import m`, `import m as x` or `from m import name`; avoid `import *`; never name your files after standard modules.
- `math` offers `pi`, `sqrt`, `floor`, `ceil`, `factorial`, `gcd`, `log`, `isclose` and more.
- Built-in functions, methods and imported functions are called differently and live in different places; the error type (`NameError`, `AttributeError`, `ModuleNotFoundError`) tells you which mistake you made.

Next: [Chapter 04 — Errors and Identifiers](04-errors-and-identifiers.md) explains syntax errors versus runtime errors, how to read tracebacks, and the rules for naming things.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
