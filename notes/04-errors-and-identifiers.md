# Chapter 04 — Errors and Identifiers

> Part 1 — Python Fundamentals · Video: 38:20–51:57 · Previous: [03 Built-in Functions, print() and Modules](03-builtin-functions-print-and-modules.md) · Next: [05 Numeric Types and Booleans](05-numeric-types-and-booleans.md)

**In this chapter:** the three families of program mistakes (syntax errors, runtime errors, logic errors), how to read a traceback, how to catch an error with `try` and `except`, the rules and conventions for naming variables and functions (identifiers), and practical debugging techniques.

**Before you start:** you should be able to run a script and call functions such as `print()`, `len()` and `int()` (see [Built-in Functions and print()](03-builtin-functions-print-and-modules.md#built-in-functions-and-print)). Recap: a variable is a name bound to a value with `=`, and an expression is code that produces a value. Examples were run with Python 3.13. Python's error messages have become more helpful with each release (especially from 3.10 onwards), so older versions may word them differently or give a plainer `invalid syntax`. The content of this chapter is the same on all current versions.

In the code blocks that follow, the file path in a traceback is shortened to `example.py`, because your own path will differ.

---

## Errors: Syntax vs Runtime

**Timestamp:** [38:20](https://www.youtube.com/watch?v=J9BI0jGOds8&t=2300s)

**Learning objectives:**

- Distinguish syntax errors, runtime errors (exceptions) and logic errors, and say when each is detected.
- Read a traceback from the bottom up and locate the failing line.
- Recognise the most common exception types and their usual causes.
- Catch a simple exception with `try` and `except`.

**1. Intuition**

Imagine writing a recipe for someone. A *syntax error* is a sentence that is not grammatical ("Whisk the eggs until."): the reader stops before cooking anything. A *runtime error* is a grammatical instruction that cannot be carried out ("Add the flour from the empty jar"): the cook starts, then gets stuck. A *logic error* is an instruction that can be followed but is wrong ("Bake for 2 minutes instead of 20"): the dish is finished and wrong, and nobody complains until you taste it.

**2. Why does it exist?**

Programs are written by people, and people make mistakes. Python reports problems in three different moments so that you can tell what kind of mistake you made: before the program runs at all (syntax), while it runs (runtime), or never (logic, which you must discover by checking the result). Good error messages exist so that you can fix a problem quickly instead of guessing.

**3. Technical explanation**

*Syntax errors.* Before running a file, Python reads the whole file and checks that it follows the grammar of the language. If it does not, Python raises a `SyntaxError` (or its subclass `IndentationError`) and runs nothing from that file. The program never starts, so even `print()` calls above the faulty line do not run. The message points at the place where Python noticed the problem. The real mistake is sometimes on the previous line (for example, an unclosed bracket).

*Runtime errors (exceptions).* If the code is grammatical, Python starts executing it line by line. When a statement cannot be carried out, Python creates an exception object, stops normal execution, and looks for code that handles it. If none is found, the program ends and Python prints a *traceback*. Everything printed before the failing line stays on the screen. Common exception types:

| Exception | Typical cause |
|-----------|---------------|
| `NameError` | using a name that has not been defined (often a typo) |
| `TypeError` | an operation on the wrong kind of value, such as `"5" + 3` |
| `ValueError` | the right type but an unusable value, such as `int("abc")` |
| `ZeroDivisionError` | dividing or taking a remainder by zero |
| `IndexError` | a list or string position that does not exist |
| `KeyError` | a dictionary key that does not exist |
| `AttributeError` | an attribute or method that the object does not have |
| `FileNotFoundError` | opening a file that is not there |
| `ModuleNotFoundError` | importing a module that is not installed |

*Logic errors.* The program runs to the end without any message, but the result is wrong, for example because of a wrong formula or a wrong condition. Python cannot detect these; only tests and careful checking can.

*Reading a traceback.* A traceback lists the chain of function calls that led to the error, with the oldest call first and the most recent last (the heading says "most recent call last"). The last line names the exception type and a message. The lines just above it show the exact line of code that failed. Start from the bottom: read the exception type and message, then the failing line, then work upwards if you need to know how the program got there.

*Handling exceptions.* The `try` statement lets a program react to an exception instead of crashing:

```text
try:
    risky code
except SomeError:
    what to do if that error happens
else:
    runs only if no error happened
finally:
    runs always (clean-up)
```

**4. Syntax**

```text
try:
    statements
except ExceptionType:
    statements
except ExceptionType as name:
    statements using the exception object
```

This is a pattern, not runnable code. The code after `try:` is attempted. If it raises an exception of the named type, Python jumps to the matching `except` block. `as name` binds the exception object so that you can print its message. Always name the type you expect; a bare `except:` also catches things you did not plan for (including a keyboard interrupt), which hides bugs.

**5. Example 1 — Basic**

Syntax errors. These snippets are not valid Python, so they are shown as plain text together with the messages Python 3.13 prints. Each one is saved in a file and run.

A bracket that is never closed:

```text
print("hello"
```

```text
  File "example.py", line 1
    print("hello"
         ^
SyntaxError: '(' was never closed
```

A missing colon after a condition:

```text
if score > 50
    print("pass")
```

```text
  File "example.py", line 1
    if score > 50
                 ^
SyntaxError: expected ':'
```

A string that is not closed:

```text
message = "unfinished
```

```text
  File "example.py", line 1
    message = "unfinished
              ^
SyntaxError: unterminated string literal (detected at line 1)
```

A missing indented block, and an unexpected indent (both `IndentationError`):

```text
for i in range(3):
print(i)
```

```text
  File "example.py", line 2
    print(i)
    ^^^^^
IndentationError: expected an indented block after 'for' statement on line 1
```

```text
x = 10
  y = 20
```

```text
  File "example.py", line 2
    y = 20
IndentationError: unexpected indent
```

In each case the program does not start. Python explains what it expected, and the caret `^` shows roughly where it noticed the problem.

A runtime error, by contrast, happens only after the earlier lines have run:

```python
print("start")
total = 10 / 0
print("this line never runs")
```

Output:

```text
start
Traceback (most recent call last):
  File "example.py", line 2, in <module>
    total = 10 / 0
            ~~~^~~
ZeroDivisionError: division by zero
```

`start` appears first because the program was grammatical, so it began running. At the second line the division is impossible, so Python raised `ZeroDivisionError` and stopped. The third line never ran.

**6. Example 2 — Practical**

A traceback with several levels. The error is raised inside `average`, which was called from `report`, which was called from the main program:

```python
def average(values):
    return sum(values) / len(values)


def report(scores):
    print("Average:", average(scores))


report([])
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 9, in <module>
    report([])
    ~~~~~~^^^^
  File "example.py", line 6, in report
    print("Average:", average(scores))
                      ~~~~~~~^^^^^^^^
  File "example.py", line 2, in average
    return sum(values) / len(values)
           ~~~~~~~~~~~~^~~~~~~~~~~~~
ZeroDivisionError: division by zero
```

How to read it, from the bottom:

1. The last line says `ZeroDivisionError: division by zero`. An empty list has length 0.
2. The line above shows the failing code: `return sum(values) / len(values)` in `average`.
3. Going upwards shows who called `average` (line 6 in `report`) and who called `report` (line 9, the main program).

The cause is that the program never decided what to do with an empty list. One fix is to check before dividing:

```python
def average(values):
    if len(values) == 0:
        return None
    return sum(values) / len(values)


print(average([4, 6, 8]))
print(average([]))
```

Output:

```text
6.0
None
```

Another fix is to handle the exception where it makes sense to recover. Here the program asks for a number and copes with bad input:

```python
def read_age(text):
    try:
        return int(text)
    except ValueError as error:
        print("Could not read the age:", error)
        return None


print(read_age("27"))
print(read_age("twenty"))
```

Output:

```text
27
Could not read the age: invalid literal for int() with base 10: 'twenty'
None
```

The `try` block runs `int(text)`. For `"27"` it succeeds and returns 27. For `"twenty"` it raises `ValueError`, Python jumps to the `except ValueError` block, prints the message stored in `error`, and the function returns `None`. The program carries on instead of crashing.

**7. Example 3 — Edge case or common mistake**

The most dangerous category is the logic error, because Python is silent. A temperature converter with a misplaced bracket:

```python
celsius = 100
fahrenheit = celsius * 9 / (5 + 32)
print(fahrenheit)
```

Output:

```text
24.324324324324323
```

The program runs perfectly and prints a plausible-looking number, but boiling water is 212 degrees Fahrenheit. The formula is `celsius * 9 / 5 + 32`. Python did exactly what the code said, not what the programmer meant. The defence is to test with a known answer (0 gives 32, 100 gives 212):

```python
def to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32


print(to_fahrenheit(0), to_fahrenheit(100), to_fahrenheit(-40))
```

Output:

```text
32.0 212.0 -40.0
```

Another subtle case: a `try` block that catches too much hides real mistakes. In the next example the typo `valu` is a bug in the code, but a broad `except` makes it look like bad user input:

```python
def read_number(text):
    try:
        value = int(text)
        return valu
    except Exception:
        return "invalid input"


print(read_number("12"))
```

Output:

```text
invalid input
```

The answer is `invalid input` even though `12` is perfectly valid, because the `NameError` caused by the typo was swallowed. Catch the narrowest exception that you expect (`ValueError` here), and the typo would show up immediately.

**8. Common mistakes**

- Reading a traceback from the top instead of the bottom.
- Looking only at the line Python points to for a `SyntaxError`; the real mistake may be on the line before (an unclosed bracket or quote).
- Mixing tabs and spaces for indentation. Use four spaces per level and configure your editor to insert spaces.
- Using a bare `except:` or `except Exception:` and hiding bugs.
- Ignoring an error message because it looks long. The last line is usually enough to start.
- Treating "no error" as "correct". Always check results against a known answer.

**9. Real-world and AI applications**

Real systems expect failures: a file is missing, a network call times out, a user types text where a number is needed. Production code catches specific exceptions, logs them and continues or stops safely. In AI work, runtime errors are common and informative: a `ValueError` or a shape mismatch when feeding data to a model, a `KeyError` from a missing column or API field, a `TypeError` because a number arrived as a string. Logic errors are the dangerous ones: a wrong preprocessing step quietly lowers model accuracy without any exception, so teams write small tests with known answers (like the temperature check above).

**10. Practice**

1. Which of these is a syntax error, a runtime error or a logic error? (a) `print("hi"` (b) `int("x")` (c) computing the average of 3 numbers as `a + b + c / 3` (d) `result = 5 +` (e) `[1, 2, 3][5]`
2. The program `print("A")`, then `print(1 / 0)`, then `print("B")` is run. Which lines are printed?
3. Write a function `safe_divide(a, b)` that returns `None` instead of crashing when `b` is zero, once with an `if` check and once with `try`/`except ZeroDivisionError`.
4. Run `int("12.5")`. Which exception do you get and why? How do you convert the string `"12.5"` to the integer 12?
5. Explain why this code reports `"invalid"` for every input, then fix it: `try: n = int(text); return nn / 2 except Exception: return "invalid"` (inside a function).

**11. Interview questions**

- *What is the difference between a syntax error and an exception?* A syntax error is found before the program runs, because the code does not follow the grammar; an exception is raised while the program runs.
- *What does "most recent call last" mean?* In a traceback the calls are listed oldest first, so the failing line is at the bottom.
- *Why is a bare `except:` considered bad practice?* It catches every exception, including ones you did not expect, and can hide bugs.
- *Give an example of a logic error.* A formula with a wrong bracket that still runs and prints a number.

**12. Quick revision**

- Syntax error: detected before running; nothing in that file runs.
- Runtime error (exception): raised while running; earlier output stays, later lines do not run.
- Logic error: no message, wrong result; find it with tests and known answers.
- Read a traceback from the bottom: type and message, failing line, then the call chain.
- Use `try`/`except SpecificError` to recover from errors you expect.

---

## Identifiers and Naming Rules

**Timestamp:** [43:59](https://www.youtube.com/watch?v=J9BI0jGOds8&t=2639s)

**Learning objectives:**

- State the rules for valid identifiers and test names with `str.isidentifier()`.
- Explain what keywords are and list them with the `keyword` module.
- Apply the PEP 8 naming conventions for variables, functions, constants and classes.
- Choose meaningful names and avoid shadowing built-ins.

**1. Intuition**

An identifier is a name you give to something in your program: a variable, a function, a class. Names are labels on boxes. A box labelled "stuff" is useless a month later; a box labelled `monthly_rent` tells you everything. The rules decide which labels Python accepts, and the conventions decide which labels other programmers find easy to read.

**2. Why does it exist?**

Python needs a strict, unambiguous definition of a name so that it can tell `price` from `price + 1` from `price2`. Conventions exist because code is read much more often than it is written, and a team that names things consistently can read each other's code quickly. The conventions are written down in PEP 8, Python's official style guide.

**3. Technical explanation**

*Rules (enforced by Python).*

1. An identifier may contain letters, digits and underscores. Letters are not limited to English: `café` and `名前` are valid in Python 3.
2. It cannot start with a digit. `2name` is invalid; `name2` is valid.
3. It is case-sensitive. `Score`, `score` and `SCORE` are three different names.
4. It cannot be a *keyword*, a word that has a special meaning in the language, such as `if`, `for`, `class`, `True`.
5. It cannot contain spaces or symbols such as `-`, `$`, `@`, `%`, `!`. (`my-var` is read as `my - var`, a subtraction.)
6. There is no length limit, but very long names hurt readability.

*Keywords.* Python 3.13 has 35 keywords. They are reserved: they cannot be used as identifiers. `True`, `False` and `None` are keywords too, and they are capitalised. The `keyword` module lists them; the list can change slightly between versions.

*Soft keywords.* Words such as `match`, `case`, `type` and `_` are keywords only in particular contexts. You can still use `match` as an ordinary variable name, but it is better to avoid it.

*Built-in names are not keywords.* `print`, `list`, `max`, `sum`, `id`, `type` and `input` are ordinary names provided by Python. Python allows you to overwrite them, which is why shadowing them is dangerous (see [Built-in Functions and print()](03-builtin-functions-print-and-modules.md#built-in-functions-and-print)).

*Conventions from PEP 8 (not enforced, but expected).*

| Kind | Style | Example |
|------|-------|---------|
| Variable, function, method, module | `lower_case_with_underscores` ("snake case") | `total_price`, `read_file` |
| Constant (a value that should not change) | `UPPER_CASE_WITH_UNDERSCORES` | `MAX_RETRIES`, `PI` |
| Class | `CapitalizedWords` ("PascalCase") | `Student`, `LinearModel` |
| "Private by convention" | leading underscore | `_cache` |
| Avoiding a clash with a keyword | trailing underscore | `class_`, `type_` |
| Special "dunder" names that Python defines | double underscores at both ends | `__init__`, `__name__` |

Do not invent your own dunder names. Single-letter names are fine for short loops and maths (`i`, `x`), and misleading ones are not: avoid `l` (looks like 1), `O` (looks like 0) and `I`.

Python has no real constants. `MAX_RETRIES = 3` is only a promise to other programmers; Python will not stop you from changing it.

**4. Syntax**

```text
name = value
```

This is a pattern, not runnable code. The left side must be a valid identifier. The same rules apply to function names, parameter names, class names and module names.

To test a string against the rules (but not against the keyword list), use the string method `isidentifier()`; to check for keywords use `keyword.iskeyword()`.

**5. Example 1 — Basic**

```python
import keyword

candidates = ["total", "total_price", "_hidden", "price2", "café", "2price", "my-var", "my var", "class", "True", "total$"]

for name in candidates:
    print(f"{name!r:14} valid={name.isidentifier()}  keyword={keyword.iskeyword(name)}")
```

Output:

```text
'total'        valid=True  keyword=False
'total_price'  valid=True  keyword=False
'_hidden'      valid=True  keyword=False
'price2'       valid=True  keyword=False
'café'         valid=True  keyword=False
'2price'       valid=False  keyword=False
'my-var'       valid=False  keyword=False
'my var'       valid=False  keyword=False
'class'        valid=True  keyword=True
'True'         valid=True  keyword=True
'total$'       valid=False  keyword=False
```

`isidentifier()` checks the character rules only. `class` and `True` pass the character rules but are keywords, so they cannot be used as names. The `!r` inside the f-string shows each name with quotes, which helps to see spaces (f-strings are explained in [Python f-Strings](09-string-formatting-and-f-strings.md#python-f-strings)).

**6. Example 2 — Practical**

Naming well. The first version works but is hard to read; the second does the same job and explains itself.

```python
a = 1500
b = 0.18
c = a * b
d = a + c
print(d)
```

Output:

```text
1770.0
```

```python
PRICE_BEFORE_TAX = 1500
GST_RATE = 0.18

tax_amount = PRICE_BEFORE_TAX * GST_RATE
total_price = PRICE_BEFORE_TAX + tax_amount
print(total_price)
```

Output:

```text
1770.0
```

Line by line: the constants are written in upper case to signal "do not change"; `tax_amount` and `total_price` say what they contain. Both programs produce the same number, but only the second one can be understood without a comment. (The tax rate is only an example value.)

A quick look at the keywords and soft keywords in your version:

```python
import keyword

print(len(keyword.kwlist))
print(keyword.kwlist)
print(keyword.softkwlist)
```

Output:

```text
35
['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
['_', 'case', 'match', 'type']
```

**7. Example 3 — Edge case or common mistake**

Names that look similar are different names (case-sensitivity):

```python
score = 90
Score = 40

print(score, Score)
print(score + Score)
print(scor)
```

Output:

```text
90 40
130
Traceback (most recent call last):
  File "example.py", line 6, in <module>
    print(scor)
          ^^^^
NameError: name 'scor' is not defined. Did you mean: 'score'?
```

`score` and `Score` coexist peacefully; the typo `scor` is a new, undefined name, so it raises `NameError`. Python suggests the closest name it knows, which is often exactly the typo fix you need.

Invalid names produce syntax errors, because Python cannot even read the line:

```text
class = 3
```

```text
  File "example.py", line 1
    class = 3
          ^
SyntaxError: invalid syntax
```

```text
2name = "x"
```

```text
  File "example.py", line 1
    2name = "x"
    ^
SyntaxError: invalid decimal literal
```

```text
my-var = 4
```

```text
  File "example.py", line 1
    my-var = 4
    ^^^^^^
SyntaxError: cannot assign to expression here. Maybe you meant '==' instead of '='?
```

The third message is a good example of how Python reads your code: `my-var` is an expression (`my` minus `var`), and you cannot assign to an expression.

Finally, an identifier may be valid and still a bad idea, because it overwrites a built-in. This code is legal and breaks the next line:

```python
sum = 10 + 20
total = sum([1, 2, 3])
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 2, in <module>
    total = sum([1, 2, 3])
TypeError: 'int' object is not callable
```

**8. Common mistakes**

- Starting a name with a digit, or using a hyphen or space inside a name.
- Using a keyword as a name (`class`, `from`, `in`, `is`, `lambda`, `pass`).
- Capitalisation slips: `Name` versus `name`; `true` versus `True`; `none` versus `None`.
- Shadowing built-ins with names such as `list`, `str`, `sum`, `max`, `min`, `id`, `type`, `input`.
- Meaningless names (`a`, `b`, `temp2`, `data1`) in code that is not a tiny example.
- Mixing styles in one project (`totalPrice` in one place, `total_price` in another).
- Starting a file name with a digit or using spaces; a module file you want to import must follow the identifier rules too.

**9. Real-world and AI applications**

Teams check naming with automatic tools (linters and formatters such as `ruff`, `flake8` or `pylint`), because consistent names make code reviews faster. In machine-learning code you will see conventions such as `X_train` and `y_train` for data (a long-standing exception to lower-case naming), `learning_rate` and `batch_size` for settings, and class names in PascalCase for models (`TextClassifier`). Names are part of an interface: API fields and configuration keys that other programs read must be spelled exactly, with the same case.

**10. Practice**

1. Which are valid identifiers? `user_name`, `1st_place`, `total-cost`, `_temp`, `Class`, `class`, `price$`, `naïve`, `x2`.
2. Rewrite `d = r * t` and `n = 5` as meaningful names for "distance equals speed times time" and "number of students".
3. Give the PEP 8 style names for: a constant for the maximum login attempts, a function that loads a dataset, a class for a customer record.
4. Write code that prints how many keywords your Python has and whether `match` is a keyword.
5. What is wrong with `max = 10; biggest = max(3, 7)`? Fix it.

**11. Interview questions**

- *Are Python identifiers case-sensitive?* Yes: `data` and `Data` are different names.
- *What is the difference between a keyword and a built-in function name?* Keywords are reserved and cannot be used as names; built-in names such as `print` are ordinary names that you can overwrite (which you should not do).
- *What is the convention for constants and for classes?* `UPPER_CASE` for constants and `CapitalizedWords` for classes.
- *What does a single leading underscore mean?* By convention, the name is for internal use only.

**12. Quick revision**

- Identifier = letters, digits, underscores; not starting with a digit; case-sensitive; not a keyword.
- 35 keywords in Python 3.13; check with `keyword.kwlist` and `keyword.iskeyword()`.
- PEP 8: `snake_case` for variables and functions, `UPPER_CASE` for constants, `PascalCase` for classes.
- Do not shadow built-ins such as `list`, `sum`, `max`, `type`, `input`.
- Choose names that say what the value means.

---

## Practical Debugging Techniques

This section is supplementary: the video topic list does not name it, but you will use it in every chapter that follows.

**Timestamp:** supplementary section (not a separate video topic; it belongs with [Errors: Syntax vs Runtime](04-errors-and-identifiers.md#errors-syntax-vs-runtime)).

**Learning objectives:**

- Follow a repeatable routine to locate a bug instead of guessing.
- Use `print`, the traceback and small experiments to narrow down a problem.
- Recognise when to simplify the code or ask for help with a minimal example.

**1. Intuition**

Debugging is detective work. The program has done something you did not expect, and you gather evidence until you find the point where reality and your assumptions diverge. The best detectives do not guess; they look.

**2. Why does it exist?**

Every programmer writes bugs. What separates beginners from experienced developers is not fewer bugs but a calm, repeatable method for finding them. A method turns a frustrating hour into a five-minute check.

**3. Technical explanation**

A reliable routine:

1. **Read the error.** Start with the last line of the traceback: type and message. Then the failing line.
2. **Reproduce it.** Find the smallest input or the smallest piece of code that still shows the problem. Often the bug becomes obvious while you shrink the example.
3. **Inspect the values.** Print the variables just before the failing line, and print their types. Use `repr()` (or `!r` in an f-string) to expose hidden characters such as spaces and newlines.
4. **Form one hypothesis and test it.** Change one thing at a time. If you change three things, you will not know which one mattered.
5. **Split the problem.** Check the first half of the program. If it is right, the bug is in the second half; repeat (a binary search through your code).
6. **Use a debugger when printing is not enough.** `breakpoint()` (Python 3.7+) pauses the program and opens the `pdb` debugger, where you can step through lines and inspect variables.
7. **Explain it aloud.** Describing the code line by line to a colleague, or to a rubber duck, often exposes the wrong assumption ("rubber-duck debugging").
8. **Fix the cause, then re-test.** Re-run the program and a known-good example to make sure nothing else broke.

Useful tools at this stage:

- `print(variable)` and `print(type(variable))`.
- `print(repr(variable))` to see quotes and escape characters.
- The f-string `=` specifier (Python 3.8+): `print(f"{variable = }")` prints both the expression and its value.
- `assert condition, "message"` stops the program with an `AssertionError` if the condition is false; it documents what you assume is true.
- `dir(obj)` and `help(obj)` to see what an object can do.

**4. Syntax**

```text
print(f"{expression=}")
assert condition, "message shown if the condition is false"
breakpoint()
```

This is a pattern, not runnable code. In the `pdb` debugger, the most useful commands are `n` (run the next line), `s` (step into a call), `c` (continue until the next breakpoint), `p expression` (print a value), `l` (list the code around the current line), `q` (quit).

**5. Example 1 — Basic**

Print debugging: find where a value stops being what you think it is.

```python
price = "2.5"
quantity = 3

total = price * quantity
print(total)
```

Output:

```text
2.52.52.5
```

There is no error, but the answer is not 7.5. Print the types:

```python
price = "2.5"
quantity = 3

print(f"{price = }, {type(price) = }")
print(f"{quantity = }, {type(quantity) = }")
print(f"{price * quantity = }")
```

Output:

```text
price = '2.5', type(price) = <class 'str'>
quantity = 3, type(quantity) = <class 'int'>
price * quantity = '2.52.52.5'
```

The evidence is clear: `price` is a string, and multiplying a string by an integer repeats the text. The fix is to convert at the point where the data enters the program: `price = float("2.5")` (see [Explicit Type Casting](08-type-conversion.md#explicit-type-casting)).

**6. Example 2 — Practical**

Hidden characters, found with `repr()`. A program checks whether a typed answer is correct:

```python
answer = "yes\n"

if answer == "yes":
    print("accepted")
else:
    print("rejected")

print(answer)
print(repr(answer))
print(repr(answer.strip()))
```

Output:

```text
rejected
yes

'yes\n'
'yes'
```

`print(answer)` looks normal (the extra blank line is easy to overlook), but `repr(answer)` shows `'yes\n'`: the text ends with a newline character, so it is not equal to `"yes"`. After `strip()` removes the whitespace at both ends, the comparison would succeed. Lines read from files, and text copied from web pages, very often carry invisible whitespace.

Using `assert` to state an assumption, so that a wrong input fails early and loudly:

```python
def percentage(part, whole):
    assert whole > 0, "whole must be positive"
    return part / whole * 100


print(percentage(30, 120))
print(percentage(5, 0))
```

Output:

```text
25.0
Traceback (most recent call last):
  File "example.py", line 7, in <module>
    print(percentage(5, 0))
          ~~~~~~~~~~^^^^^^
  File "example.py", line 2, in percentage
    assert whole > 0, "whole must be positive"
           ^^^^^^^^^
AssertionError: whole must be positive
```

The first call prints 25.0. The second raises `AssertionError` with your message, pointing at the bad input instead of producing a confusing `ZeroDivisionError` later. (Assertions are for catching programmer mistakes; for input that users can get wrong, use real checks or `try`/`except`.)

A short debugger session, which you can try with `breakpoint()` in a script (shown as a transcript, not run here):

```text
> example.py(3)total_cost()
-> result = price * quantity
(Pdb) p price
'2.5'
(Pdb) p type(price)
<class 'str'>
(Pdb) n
> example.py(4)total_cost()
-> return result
(Pdb) q
```

**7. Example 3 — Edge case or common mistake**

Changing several things at once, and fixing the symptom instead of the cause. A function should return the average of a list of marks. A beginner sees a wrong answer and "fixes" it by changing the formula until the number looks right:

```python
def average(marks):
    total = 0
    for mark in marks:
        total = mark
    return total / len(marks)


print(average([70, 80, 90]))
```

Output:

```text
30.0
```

The answer 30.0 is wrong (it should be 80.0). Adding a `* 3` at the end would give the right result for this list and the wrong result for every other list length. Print the intermediate value instead:

```python
def average(marks):
    total = 0
    for mark in marks:
        total = mark
        print(f"{mark = }, {total = }")
    return total / len(marks)


print(average([70, 80, 90]))
```

Output:

```text
mark = 70, total = 70
mark = 80, total = 80
mark = 90, total = 90
30.0
```

The printout shows that `total` is replaced by each mark instead of accumulating them. The cause is `=` where `+=` was meant. The correct version:

```python
def average(marks):
    total = 0
    for mark in marks:
        total += mark
    return total / len(marks)


print(average([70, 80, 90]))
print(average([100]))
```

Output:

```text
80.0
100.0
```

(The `for` loop is covered in [The for Loop](17-for-loop-range-and-nested-loops.md#the-for-loop).)

**8. Common mistakes**

- Changing code at random until the output "looks right".
- Not reading the error message, or reading only the first line of the traceback.
- Leaving debug `print` calls in finished code. Remove them, or use the `logging` module for messages that should stay.
- Testing only one example. Try an empty input, a single item, a very large value and a wrong type.
- Catching an exception just to silence it.
- Debugging a big program all at once instead of shrinking the failing case.

**9. Real-world and AI applications**

Professional teams turn debugging evidence into automated tests, so that a fixed bug cannot return. For AI work, the same habits apply to data and model code: print the shape and type of data at each stage of a pipeline, check a few rows by eye, test the pipeline on a tiny input with a known answer, and make the experiment reproducible (fixed random seed, recorded package versions). A model that trains without errors but gives poor results is the AI version of a logic error, and the same method (shrink, inspect, test one change at a time) is how it is solved.

**10. Practice**

1. The code `a = "1"`, `b = "2"`, `c = "3"`, `print(a + b + c)` is meant to print the sum 6, but it does not. Use `type()` to explain what it prints and fix it so that it prints `6`.
2. `name = "  Asha "` and the check `name == "Asha"` is `False`. Use `repr()` to show why and write the fix.
3. Add an `assert` to a function `square_root_of(x)` that stops with a clear message for negative numbers, using `math.sqrt` inside.
4. Reproduce and read the traceback for each of these, and name the exception: `[1, 2, 3][3]`, `{"a": 1}["b"]`, `int("3.5")`, `"abc".upper(1)`.
5. A student's function returns the largest mark but returns the wrong value for `[5, 9, 2]`. Write a version that prints its internal values to find the mistake. Start from: `best = 0` then a loop `for mark in marks: if mark > best: best = mark`, and explain where it could go wrong for a list of all negative numbers.

**11. Interview questions**

- *How do you approach a bug you have never seen?* Read the error, reproduce with a minimal example, inspect values, test one hypothesis at a time, and fix the cause.
- *What does `repr()` do and why is it useful in debugging?* It returns the unambiguous text form of a value (with quotes and escape sequences), which reveals hidden whitespace and type differences.
- *What is the difference between `print` debugging and using a debugger?* Printing shows chosen values at chosen points and needs code changes; a debugger lets you pause, step and inspect interactively.
- *When should you use `assert`?* To state conditions that must be true if the code is correct. Not for validating user input, because assertions can be disabled with the `-O` option.

**12. Quick revision**

- Read the traceback from the bottom; reproduce with the smallest example.
- Inspect values and types: `print(f"{x = }")`, `repr(x)`, `type(x)`.
- Change one thing at a time; split the problem in half.
- `assert` documents assumptions; `breakpoint()` opens the debugger.
- Fix the cause, not the symptom; re-test with known answers and edge cases.

---

## Answers to Practice Exercises

### Answers: Errors: Syntax vs Runtime

1. (a) syntax error (missing closing bracket); (b) runtime error (`ValueError`); (c) logic error (operator precedence: only `c` is divided by 3; it should be `(a + b + c) / 3`); (d) syntax error (nothing after `+`); (e) runtime error (`IndexError`).
2. `A` is printed, then `ZeroDivisionError` stops the program. `B` is never printed. If the file had a syntax error, nothing at all would print.
3. Two versions:

```python
def safe_divide_if(a, b):
    if b == 0:
        return None
    return a / b


def safe_divide_try(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


print(safe_divide_if(10, 4), safe_divide_if(10, 0))
print(safe_divide_try(10, 4), safe_divide_try(10, 0))
```

Output:

```text
2.5 None
2.5 None
```

4. `int("12.5")` raises `ValueError`, because the text is not a valid whole-number literal. To get 12 from the string, convert through a float:

```python
print(int(float("12.5")))
```

Output:

```text
12
```

5. The typo `nn` raises `NameError`, but `except Exception` catches it and returns `"invalid"` every time. Fixed, catching only the expected exception:

```python
def half(text):
    try:
        n = int(text)
        return n / 2
    except ValueError:
        return "invalid"


print(half("10"), half("ten"))
```

Output:

```text
5.0 invalid
```

### Answers: Identifiers and Naming Rules

1. Valid: `user_name`, `_temp`, `Class` (capital `C`, so it is not the keyword), `naïve`, `x2`. Invalid: `1st_place` (starts with a digit), `total-cost` (hyphen), `class` (keyword), `price$` (symbol).

```python
import keyword

for name in ["user_name", "1st_place", "total-cost", "_temp", "Class", "class", "price$", "naïve", "x2"]:
    print(name, name.isidentifier() and not keyword.iskeyword(name))
```

Output:

```text
user_name True
1st_place False
total-cost False
_temp True
Class True
class False
price$ False
naïve True
x2 True
```

2. `distance = speed * time_taken` (avoid `time` alone if you will import the `time` module) and `student_count = 5` (or `number_of_students`).
3. `MAX_LOGIN_ATTEMPTS = 3`, `def load_dataset(...)`, `class CustomerRecord:`.
4.

```python
import keyword

print(len(keyword.kwlist))
print(keyword.iskeyword("match"))
print("match" in keyword.softkwlist)
```

Output:

```text
35
False
True
```

`match` is a soft keyword (reserved only in the `match` statement context), so `iskeyword` returns `False` for it.
5. `max = 10` replaces the built-in function with the number 10, so `max(3, 7)` fails with `TypeError: 'int' object is not callable`. Fix: `largest_allowed = 10` and `biggest = max(3, 7)`.

### Answers: Practical Debugging Techniques

1. `type(a)` shows `<class 'str'>`. Adding strings joins them, so the first `print` shows `123`. To print 6, convert to numbers:

```python
a = "1"
b = "2"
c = "3"
print(a + b + c)
print(int(a) + int(b) + int(c))
```

Output:

```text
123
6
```

2.

```python
name = "  Asha "
print(repr(name))
print(name == "Asha")
print(name.strip() == "Asha")
```

Output:

```text
'  Asha '
False
True
```

3.

```python
import math


def square_root_of(x):
    assert x >= 0, "x must not be negative"
    return math.sqrt(x)


print(square_root_of(16))
print(square_root_of(-4))
```

Output:

```text
4.0
Traceback (most recent call last):
  File "example.py", line 10, in <module>
    print(square_root_of(-4))
          ~~~~~~~~~~~~~~^^^^
  File "example.py", line 5, in square_root_of
    assert x >= 0, "x must not be negative"
           ^^^^^^
AssertionError: x must not be negative
```

4. `[1, 2, 3][3]` is `IndexError: list index out of range`. `{"a": 1}["b"]` is `KeyError: 'b'`. `int("3.5")` is `ValueError: invalid literal for int() with base 10: '3.5'`. `"abc".upper(1)` is `TypeError: str.upper() takes no arguments (1 given)`.

```python
try:
    "abc".upper(1)
except TypeError as error:
    print(error)
```

Output:

```text
str.upper() takes no arguments (1 given)
```

5. With `best = 0` as the starting value, a list of only negative numbers never beats 0, so the function returns 0, a value that is not in the list. A version that prints its internals and a corrected start:

```python
def largest(marks):
    best = marks[0]
    for mark in marks:
        if mark > best:
            best = mark
        print(f"{mark = }, {best = }")
    return best


print(largest([5, 9, 2]))
print(largest([-8, -3, -5]))
```

Output:

```text
mark = 5, best = 5
mark = 9, best = 9
mark = 2, best = 9
9
mark = -8, best = -8
mark = -3, best = -3
mark = -5, best = -3
-3
```

Starting from the first item, rather than from a made-up number, makes the function correct for every non-empty list. (The built-in `max()` already does this for you.)

---

## Chapter Summary and Key Takeaways

- Syntax errors stop the program before it starts; runtime errors (exceptions) stop it when a statement fails; logic errors give no message and a wrong answer.
- Read a traceback from the bottom: exception type and message, then the failing line, then the call chain.
- Catch only the exceptions you expect with `try`/`except SpecificError`.
- Identifiers use letters, digits and underscores, cannot start with a digit, are case-sensitive and cannot be keywords. Follow PEP 8: `snake_case`, `UPPER_CASE`, `PascalCase`.
- Never reuse built-in names such as `list`, `sum`, `max` or `input`.
- Debug with a method: read, reproduce, inspect (`print`, `type`, `repr`), test one change at a time, then fix the cause.

Next: [Chapter 05 — Numeric Types and Booleans](05-numeric-types-and-booleans.md) starts Part 2 with integers, floats, complex numbers and booleans.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
