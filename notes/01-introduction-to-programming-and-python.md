# Chapter 01 — Introduction to Programming and Python

> Part 1 — Python Fundamentals · Video: 00:00–11:10 · Next: [02 Installation and Environment Setup](02-installation-and-environment-setup.md)

**In this chapter:** what this handbook covers and how to use it, why people write programs at all, what Python is and where it is used, and the language features that shape how Python code looks and behaves (interpreted execution, dynamic typing, indentation, a large standard library, multiple programming styles).

**Before you start:** nothing from earlier chapters is needed, because this is the first chapter. A computer science background helps (you have seen terms like variable, loop and compiler), but every term is defined when it first appears. Examples were run with Python 3.13; where a feature depends on the Python version, the text says so. If you have not installed Python yet, read [Chapter 02](02-installation-and-environment-setup.md) first and then come back to run the examples.

A note about tracebacks: when an example shows an error message, the file path in the first line of a traceback is replaced with `example.py`, because your own paths will differ.

---

## Introduction: Master Python and AI

**Timestamp:** [00:00](https://www.youtube.com/watch?v=J9BI0jGOds8)

**Learning objectives:**

- Describe how this handbook is organized and how to study from it.
- Explain, at a high level, why Python is a common first language for AI work.
- Run your first one-line Python program (or know where to find out how, in Chapter 02).

**1. Intuition**

Learning a language to build AI applications has two layers. The first layer is the language itself: variables, decisions, loops, collections and functions. The second layer is what people build on top of it: programs that call machine-learning libraries or language-model services. This handbook follows that order. You cannot read AI code until you can read plain Python, so the first five parts teach Python and the last part explains how language-model applications are put together.

**2. Why does it exist?**

Many learners jump straight into AI libraries and get stuck on small language details: why a value is text and not a number, why a loop never ends, why a list changed unexpectedly. A course that builds the foundation first removes those obstacles before they appear inside bigger programs.

**3. Technical explanation**

The handbook has 40 chapters in 6 parts. Each chapter ends with answers to its own exercises and a summary. Extra practice problems are in the `practice/` folder, and each part has a mini-project in the `projects/` folder. The key idea for how to study: you learn programming by running code and reading real error messages, not by reading alone. Every code example in these notes has its real output beside it so you can compare against your own.

**4. Syntax**

There is no new syntax in this topic apart from the smallest possible Python program, a call to the built-in function `print`:

```python
print("text to display")
```

- `print` is the name of a built-in function (a ready-made action that Python provides).
- The parentheses `()` call the function, meaning "run it now".
- `"text to display"` is a string literal (a piece of text written directly in the code). It is the argument, the value handed to the function.

**5. Example 1 — Basic**

```python
print("Hello, Python!")
```

Output:

```text
Hello, Python!
```

**6. Example 2 — Practical**

A first program that does a small amount of real work: it summarizes a list of daily temperatures.

```python
temperatures = [21.5, 23.0, 19.8, 25.1, 22.4]
average = sum(temperatures) / len(temperatures)
print("Days recorded:", len(temperatures))
print("Highest:", max(temperatures))
print("Lowest:", min(temperatures))
print("Average:", round(average, 2))
```

Output:

```text
Days recorded: 5
Highest: 25.1
Lowest: 19.8
Average: 22.36
```

Line by line:

- `temperatures = [...]` stores a list of five numbers under the name `temperatures`.
- `sum(...)` and `len(...)` are built-in functions that add up the items and count them. Dividing gives the average.
- `max`, `min` and `round` are also built-in functions. You will meet them properly in [Chapter 03](03-builtin-functions-print-and-modules.md).

You do not need to understand every symbol yet. The goal is to notice that a few readable lines produce a useful summary.

**7. Example 3 — Edge case or common mistake**

A beginner often expects a program to "understand what was meant". It only does what was written. Here the programmer wants a total of all prices:

```python
prices = [10, 20, 30]
total = 0
for price in prices:
    total = price      # bug: should be total += price
print(total)
```

Output:

```text
30
```

There is no error message, yet the answer is wrong (it should be 60). Python replaced `total` on every loop pass instead of adding to it. This is a logic error, a mistake in the idea of the program rather than its spelling, and the interpreter cannot detect it. The fix is `total += price`. Chapter 04 classifies the different kinds of errors.

**8. Common mistakes**

- Reading code without running it. Fix: type every example yourself and change a value to see what happens.
- Skipping the exercises. Fix: attempt them before opening the answers at the end of each chapter.
- Copying code you do not understand. Fix: explain each line aloud or in a comment before moving on.

**9. Real-world and AI applications**

Almost every popular AI toolkit exposes a Python interface: you load data, call a function, and inspect the result. Even a tiny script that cleans text, counts words or calls a web service uses exactly the building blocks in Parts 1 to 5.

**10. Practice**

1. Write a program that prints your name on one line and the name of a city on the next line.
2. Write a program that prints the result of `7 * 6` without typing the answer yourself.
3. Using the temperature example as a model, write a program that prints the highest, lowest and total of the list `[4, 9, 2, 7]`.

**11. Interview questions**

1. Why is it useful to learn plain Python before using AI libraries? Answer: AI libraries are written and called in Python code, and their behavior depends on the same rules for types, loops, functions and errors that plain Python uses. Without them, debugging library code is guesswork.
2. What is the difference between a syntax error and a logic error? Answer: a syntax error breaks the language rules and is reported before the program runs; a logic error follows the rules but produces a wrong result, so no error is reported.

**12. Quick revision**

- The handbook builds from language basics to AI application concepts.
- Learn by running code, reading output and trying the exercises.
- `print("text")` is the smallest Python program.

---

## Why Do We Need Programming?

**Timestamp:** [02:38](https://www.youtube.com/watch?v=J9BI0jGOds8&t=158s)

**Learning objectives:**

- Define a program, an algorithm and automation.
- Explain why precise written instructions are needed to make a computer do work.
- Describe the typical input, process, output shape of a program.

**1. Intuition**

A recipe is a list of exact steps that turns ingredients into a meal. A program is a recipe for a computer. The computer is extremely fast and never gets bored, but it has no common sense: it will follow the steps literally, millions of times, without asking what you meant.

**2. Why does it exist?**

People have tasks that are repetitive, large, or error-prone when done by hand: totalling thousands of numbers, searching millions of records, resizing a thousand photos. A computer can do this quickly and consistently, but only if someone describes the task in a form the machine can follow. Programming is the activity of writing that description.

**3. Technical explanation**

An algorithm is a finite, ordered set of well-defined steps that solves a problem. A program is an algorithm written in a programming language so that a computer can execute it. A programming language is a formal language with strict rules (its syntax) and defined meaning (its semantics). Processors only run machine instructions (binary patterns), which are hard for people to write, so higher-level languages such as Python are translated into something the machine can run. Section "What Is Python and Where Is It Used?" explains how Python does this.

Most programs have the same shape:

```text
input  ->  process  ->  output
```

Input may be a typed value, a file, a sensor reading or a web request. Processing is the calculation or decision. Output is what the program shows or stores.

Automation means letting a program do repetitive work so that people do not have to. Scale is the other reason: a task that takes a minute by hand, repeated a million times, is impossible by hand and trivial for a program.

**4. Syntax**

A programming language gives you a few kinds of building blocks. The names below are previews; later chapters cover each one.

- Values and variables: data and names for data (Chapters 05 to 09).
- Operators and expressions: calculations (Chapters 11 to 13).
- Conditionals: choose between actions (Chapters 14 and 15).
- Loops: repeat actions (Chapters 16 and 17).
- Collections: hold many values (Chapters 18 to 24).
- Functions: package a task under a name (Chapters 25 to 29).

**5. Example 1 — Basic**

Adding the numbers 1 to 100 by hand means typing 100 terms. A loop describes the repetition once:

```python
total = 0
for number in range(1, 101):
    total += number
print("Sum of 1 to 100:", total)
```

Output:

```text
Sum of 1 to 100: 5050
```

Changing `101` to `1_000_001` would add the first million numbers with no extra typing. That is the leverage a program gives.

**6. Example 2 — Practical**

Input, process, output in one short script, using a hard-coded input so the output is always the same:

```python
price_per_item = 249.50
quantity = 3
tax_rate = 0.05

subtotal = price_per_item * quantity
tax = subtotal * tax_rate
total = subtotal + tax

print("Subtotal:", subtotal)
print("Tax:", tax)
print("Total:", total)
```

Output:

```text
Subtotal: 748.5
Tax: 37.425000000000004
Total: 785.925
```

The tiny extra digits in the tax line are not a bug in your program. Computers store most decimal fractions in binary, which cannot represent them exactly, so some results show a rounding artifact (see [The Float Data Type](05-numeric-types-and-booleans.md#the-float-data-type) for the explanation and how to display clean numbers).

The first three lines are the input, the three calculation lines are the process, and the `print` calls are the output. In a real program the input would come from a user or a file rather than being typed into the code.

**7. Example 3 — Edge case or common mistake**

A computer follows instructions exactly, so an unclear instruction gives an unexpected result. A beginner wants "the average of two numbers" and writes:

```python
first = 10
second = 20
average = first + second / 2
print(average)
```

Output:

```text
20.0
```

The expected answer is 15.0. The cause is operator precedence: division happens before addition, so Python computed `first + (second / 2)`. Parentheses state the intention: `(first + second) / 2`. Precedence is covered in [Chapter 13](13-identity-operators-and-precedence.md); the lesson here is that the program followed the rules, not the intention.

**8. Common mistakes**

- Thinking "the computer will figure out what I mean". It cannot. Fix: write each step explicitly, and test with a small known input.
- Starting to type code before understanding the problem. Fix: write the steps in plain words first (an algorithm), then translate them.
- Doing repetitive work by hand "just this once". Fix: if you will repeat a task more than a few times, consider a short script.

**9. Real-world and AI applications**

Programs process tickets at a station, compute grades, route messages and recommend videos. In AI work, a programmer writes code that loads data, cleans it, passes it to a model, and checks the results. The model itself is also produced by a program (a training program) that repeats a calculation many times over a data set. Without programming, none of this scales.

**10. Practice**

1. Write the steps (in plain English, not code) for making a cup of tea, then identify which part is input, which is process and which is output.
2. Write a program that computes the total cost of 12 items at 15.75 each and prints it.
3. Write a program with a loop that prints the numbers 1 to 10 in a single line using `print(number, end=" ")`.
4. The expression `2 + 3 * 4` gives 14, not 20. Explain why, and write it so that the result is 20.

**11. Interview questions**

1. What is an algorithm and how does it differ from a program? Answer: an algorithm is a step-by-step method to solve a problem, independent of language; a program is an implementation of an algorithm in a specific language.
2. Why can a computer not "just understand" plain English instructions? Answer: natural language is ambiguous, while a processor needs exact, unambiguous instructions; programming languages remove the ambiguity by having strict rules.
3. What are the three typical stages of a program? Answer: input, process, output.

**12. Quick revision**

- A program is a precise recipe that a computer follows exactly.
- An algorithm is the method; a program is the method written in a language.
- Programs exist for automation and scale.
- Most programs follow input, process, output.

---

## What Is Python and Where Is It Used?

**Timestamp:** [06:45](https://www.youtube.com/watch?v=J9BI0jGOds8&t=405s)

**Learning objectives:**

- Define Python as a general-purpose, high-level programming language.
- Explain the difference between the language and an implementation such as CPython.
- Name major areas where Python is used and why it suits them.

**1. Intuition**

Think of a language as a set of rules for writing and an implementation as a translator who reads your writing and acts on it. Python is the set of rules. The program that reads Python and carries out your instructions is called the Python interpreter. You write in Python; the interpreter does the work.

**2. Why does it exist?**

Many older languages made the programmer manage low-level details such as memory. That slows development and invites mistakes. Python was designed (by Guido van Rossum, first released in 1991) to be easy to read and quick to write, so that more time goes to solving the problem than to fighting the language. The name comes from the comedy group Monty Python, not the snake.

**3. Technical explanation**

Python is:

- General-purpose: not limited to one domain; it is used for scripts, web back ends, data analysis, automation and more.
- High-level: it hides hardware details such as memory addresses and registers.
- Interpreted (in practice): you run source code through the interpreter without a separate manual compile step. Internally, the standard implementation first compiles your source to bytecode (a compact instruction format), then a virtual machine runs that bytecode. This happens automatically.
- Dynamically typed: values carry types, names do not. See "Key Features of Python".

The word "Python" can mean the language definition or a particular program that runs it. The standard and most widely used implementation, from python.org, is called CPython because it is written in C. Others exist (for example PyPy), and they aim to run the same language. In these notes, "Python" means CPython unless stated.

Python has two major lines of history. Python 2 reached end of life on 1 January 2020. Python 3 is the current line and the only one used in this handbook. Code written for Python 2 often fails on Python 3. A well-known difference: `print` was a statement in Python 2 and is a function in Python 3.

Where Python is used:

| Area | What Python does there | Examples of tools |
|------|-----------------------|-------------------|
| Scripting and automation | rename files, process logs, call web services | standard library |
| Web back ends | handle requests and talk to databases | Django, Flask, FastAPI |
| Data analysis | load, clean and summarize tables | pandas, NumPy |
| Machine learning and AI | build, train and call models | PyTorch, TensorFlow, scikit-learn |
| Scientific computing | numerical simulation, plotting | SciPy, Matplotlib |
| Testing and tooling | test runners, build tools | pytest |

Note that many scientific libraries run heavy calculations in compiled code (often C or C++) and expose them through a Python interface. Python is the convenient control layer; it is not always the part doing the number crunching.

**4. Syntax**

Python source files conventionally end in `.py`. You run a file with the interpreter:

```bash
python3 hello.py
```

On Windows the command is commonly `python` or the launcher `py`. Chapter 02 explains how to find out which works on your machine.

- `python3` is the interpreter program.
- `hello.py` is the path to your source file, which the interpreter reads and runs from top to bottom.

**5. Example 1 — Basic**

Ask the running interpreter what kinds of values exist:

```python
print(type(10), type(3.5), type("hi"), type([1, 2]), type({"a": 1}))
```

Output:

```text
<class 'int'> <class 'float'> <class 'str'> <class 'list'> <class 'dict'>
```

`type` is a built-in function that reports the type of a value. Even an integer such as `10` is an object that belongs to the class `int`.

**6. Example 2 — Practical**

Check which implementation and version are running, using the standard library module `platform` (a module is a file of ready-made code that you load with `import`; see [Chapter 03](03-builtin-functions-print-and-modules.md#python-modules-math-and-import)).

```python
import platform
print(platform.python_implementation())
```

Output (tested with Python 3.13; yours may differ if you use another implementation):

```text
CPython
```

To check your version from a script, use `sys.version_info`:

```python
import sys
print(sys.version_info.major >= 3)
```

Output:

```text
True
```

**7. Example 3 — Edge case or common mistake**

Code or tutorials written for Python 2 may fail. This is not valid Python 3; it shows the old `print` statement and the error it causes:

```text
print "hello"
```

Running a file with that line in Python 3.13 gives:

```text
  File "example.py", line 1
    print "hello"
    ^^^^^^^^^^^^^
SyntaxError: Missing parentheses in call to 'print'. Did you mean print(...)?
```

The fix is to call the function: `print("hello")`. Seeing `print` without parentheses in a tutorial usually means it is Python 2 material and should be treated with care.

**8. Common mistakes**

- Assuming Python is slow for everything. Heavy numeric libraries use compiled code under the hood, so the Python layer is often not the bottleneck.
- Mixing up the language and the interpreter. Fix: remember that a Python file is just text; the interpreter runs it.
- Following Python 2 tutorials. Fix: check that examples use `print(...)` and that the tutorial targets Python 3.

**9. Real-world and AI applications**

Data analysis, web services and machine learning all use Python. For AI applications, vendors typically provide a Python client library (a package of code you install) and Python is the language most examples are written in. The reason is partly historical and partly practical: the libraries already exist, so using Python means reusing them.

**10. Practice**

1. Write a program that prints the type of the values `42`, `4.2`, `"42"` and `True`.
2. Write a program that prints the name of the Python implementation running it, and whether the major version is 3.
3. Name three areas where Python is used and one library for each. (Use the table above only as a starting point; you may name others.)
4. Explain in two or three sentences why "Python" can refer both to a language and to a program.

**11. Interview questions**

1. Is Python compiled or interpreted? Answer: both, in a sense. CPython compiles source to bytecode automatically and then a virtual machine interprets the bytecode. From the programmer's view it is run directly without a separate compile step.
2. What is CPython? Answer: the reference implementation of Python, written in C.
3. Who created Python and when was it first released? Answer: Guido van Rossum; first released in 1991.
4. What is a major difference between Python 2 and Python 3 that beginners see first? Answer: `print` changed from a statement to a function, so Python 3 requires parentheses.

**12. Quick revision**

- Python is a general-purpose, high-level language; CPython is its standard implementation.
- Source is compiled to bytecode and run by a virtual machine, automatically.
- Used in scripting, web, data, science and AI, often as a control layer over compiled libraries.
- Use Python 3; Python 2 is end of life.

---

## Key Features of Python

**Timestamp:** [11:10](https://www.youtube.com/watch?v=J9BI0jGOds8&t=670s)

**Learning objectives:**

- Describe readable syntax and significant indentation.
- Explain dynamic typing and what it means that variables are names for objects.
- Recognize that Python supports several programming styles and has a large standard library.

**1. Intuition**

Imagine labeled sticky notes that you can stick onto any object and move to another object later. In Python a variable name behaves like such a label. The label has no fixed type; the object it points to does. Python also uses layout (indentation) to show structure, much as an outline uses indenting to show which points belong under which heading.

**2. Why does it exist?**

Each feature solves a practical problem:

- Readable syntax: code is read far more often than it is written, so it should be easy to read.
- Indentation as structure: forces consistent layout so that the visible shape of the code matches how it runs.
- Dynamic typing: removes the need to declare types before use, so small programs are short.
- Standard library: common tasks (dates, files, JSON, statistics) are available without extra downloads.
- Multiple styles: different problems fit different approaches.

**3. Technical explanation**

Readable syntax. Python uses plain words for many operations (`and`, `or`, `not`, `in`) and few symbols. The module `this` prints "The Zen of Python", a short list of design guidelines, including "Readability counts."

Indentation. Python marks a block of code (the statements that belong to a `def`, `if`, `for` and so on) by indenting them. There are no braces. All lines in one block must be indented by the same amount, and PEP 8 (the official style guide) recommends 4 spaces per level. Wrong indentation is an error, not merely bad style.

Dynamic typing. Every value is an object with a type. A name is a reference to an object, and the same name can later refer to an object of another type. Types are checked when an operation runs, not before. Python is also strongly typed: it does not silently convert incompatible types (it refuses to add `"30"` and `1`). Do not confuse "dynamic" with "weak".

Interpreted execution. Covered above: you run source directly, and the interpreter reports an error when it meets one.

Standard library ("batteries included"). A large set of modules installed with Python. You load one with `import`.

Multiple paradigms (programming styles). Python supports procedural code (step-by-step statements), object-oriented code (classes), and functional style (functions passed as values). You can mix them.

Other properties worth knowing: automatic memory management (a garbage collector reclaims objects that are no longer used, so you do not free memory yourself), and portability (the same source runs on Windows, macOS and Linux, provided the code does not rely on OS-specific features).

**4. Syntax**

Block structure with a colon and indentation:

```text
header_line:
    first statement in the block
    second statement in the block
```

This is a template, not runnable Python. The header (such as `def`, `if` or `for`) ends with a colon, and the lines after it are indented by the same amount.

Assignment binds a name to an object: `name = value`.

**5. Example 1 — Basic**

Dynamic typing: one name, two types over time.

```python
value = 42
print(value, type(value))
value = "forty-two"
print(value, type(value))
```

Output:

```text
42 <class 'int'>
forty-two <class 'str'>
```

The name `value` first refers to an `int` object and is then rebound to a `str` object. No declaration was needed and the type belongs to the object, not the name.

**6. Example 2 — Practical**

Standard library in action: summary statistics, JSON text and a file path, with no installation.

```python
import statistics, json, pathlib

scores = [72, 85, 90, 66, 85]
print(statistics.mean(scores))
print(statistics.median(scores))
print(statistics.mode(scores))
print(json.dumps({"name": "Asha", "scores": scores}))
print(pathlib.Path("notes") / "ch01.md")
```

Output (the last line uses `/` on macOS and Linux; Windows prints a backslash):

```text
79.6
85
85
{"name": "Asha", "scores": [72, 85, 90, 66, 85]}
notes/ch01.md
```

- `statistics.mean`, `median` and `mode` are functions inside the `statistics` module.
- `json.dumps` turns a Python dictionary into JSON text.
- `pathlib.Path("notes") / "ch01.md"` builds a file path in a way that suits the operating system.

The same task in three styles (multiple paradigms):

```python
numbers = [1, 2, 3, 4]

# procedural
squares = []
for n in numbers:
    squares.append(n * n)
print(squares)

# functional style
print(list(map(lambda n: n * n, numbers)))


# object-oriented
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1


counter = Counter()
counter.increment()
counter.increment()
print(counter.count)
```

Output:

```text
[1, 4, 9, 16]
[1, 4, 9, 16]
2
```

Do not worry about `lambda`, `map` or `class` yet; they are covered in Part 5 and later. The point is that Python lets the same idea be written in different styles.

Readability: the same join task written verbosely and idiomatically.

```python
words = ["python", "is", "readable"]
sentence = ""
for index in range(len(words)):
    if index > 0:
        sentence = sentence + " "
    sentence = sentence + words[index]
print(sentence)
print(" ".join(words))
```

Output:

```text
python is readable
python is readable
```

**7. Example 3 — Edge case or common mistake**

Dynamic typing does not mean Python guesses. Strong typing stops incompatible operations. Valid syntax, but it fails when run:

```python
age = "30"
print(age + 1)
```

Output (error):

```text
Traceback (most recent call last):
  File "example.py", line 2, in <module>
    print(age + 1)
          ~~~~^~~
TypeError: can only concatenate str (not "int") to str
```

`age` refers to text, not a number, so adding an integer is refused. The fix depends on intent: `int(age) + 1` gives 31, while `age + "1"` gives the text `"301"`. Type conversion is the subject of [Chapter 08](08-type-conversion.md).

Indentation is also enforced. This is not valid Python; the second line is not indented under `def`:

```text
def greet(name):
message = "Hello, " + name
    return message
```

Running it gives:

```text
  File "example.py", line 2
    message = "Hello, " + name
    ^^^^^^^
IndentationError: expected an indented block after function definition on line 1
```

The corrected form:

```python
def greet(name):
    message = "Hello, " + name
    return message


print(greet("Asha"))
```

Output:

```text
Hello, Asha
```

**8. Common mistakes**

- Mixing tabs and spaces in one block. Fix: configure your editor to insert 4 spaces when you press Tab.
- Believing that dynamic typing means "no types". Fix: every object has a type; use `type(x)` to inspect.
- Forgetting the colon at the end of a block header. Fix: read the error message; it normally points at the line.
- Assuming that a variable "contains" a value. Fix: think of the name as a label attached to an object.

**9. Real-world and AI applications**

Readable syntax and the standard library make Python common for quick data-cleaning scripts. Dynamic typing speeds up experimenting, a typical need in AI work where you try many small variations. The trade-off is that type mistakes appear at run time, so larger projects add optional type hints and tests. Because the same code runs on several operating systems, a script written on a laptop often runs on a server with little change.

**10. Practice**

1. Write a program that stores an integer in a variable, prints its type, stores a string in the same variable, and prints its type again.
2. Using the `statistics` module, print the mean and median of `[3, 8, 5, 10]`.
3. The program below has an indentation problem. Describe the error and fix it.

```text
for number in range(3):
print(number)
```

4. Explain the difference between dynamically typed and weakly typed, and give an example from Python of each idea (or its absence).

**11. Interview questions**

1. Is Python statically or dynamically typed? Answer: dynamically typed; types belong to objects and are checked when code runs.
2. Is Python strongly typed? Answer: yes; it does not silently convert unrelated types, so `"30" + 1` raises `TypeError`.
3. Why does Python use indentation? Answer: indentation defines blocks, which keeps layout consistent with structure and removes the need for braces.
4. What does "batteries included" mean? Answer: the standard library ships with many ready-to-use modules for common tasks.
5. Does a Python variable store a value? Answer: more precisely, a name refers to an object; assignment binds the name to the object.

**12. Quick revision**

- Readable syntax; blocks are defined by indentation (4 spaces recommended).
- Dynamically but strongly typed; names refer to objects.
- Large standard library; multiple programming styles.
- Automatic memory management; portable across operating systems.

---

## Answers to Practice Exercises

### Answers: Introduction: Master Python and AI

1. Two `print` calls:

```python
print("Asha")
print("Bengaluru")
```

Each call prints its text and then moves to a new line.

2. Let Python compute it:

```python
print(7 * 6)
```

Output: `42`. The expression `7 * 6` is evaluated first, then the result is printed.

3. Using the built-in functions `max`, `min` and `sum`:

```python
values = [4, 9, 2, 7]
print("Highest:", max(values))
print("Lowest:", min(values))
print("Total:", sum(values))
```

Output:

```text
Highest: 9
Lowest: 2
Total: 22
```

### Answers: Why Do We Need Programming?

1. Example steps: boil water; put a tea bag in a cup; pour water; wait for three minutes; remove the bag; add milk or sugar if wanted. Input: water, tea bag, milk. Process: boiling, steeping. Output: a cup of tea. Different valid decompositions exist as long as the steps are exact and ordered.

2. `print(12 * 15.75)` prints `189.0`. A fuller version stores the numbers in variables first.

3. Using `end=" "` keeps the output on one line:

```python
for number in range(1, 11):
    print(number, end=" ")
print()
```

Output:

```text
1 2 3 4 5 6 7 8 9 10 
```

The final `print()` adds a newline so later output starts on a fresh line. There is a trailing space after `10`.

4. Multiplication has higher precedence than addition, so `3 * 4` is evaluated first (12), then 2 is added (14). Write `(2 + 3) * 4` to get 20.

### Answers: What Is Python and Where Is It Used?

1. Program:

```python
print(type(42), type(4.2), type("42"), type(True))
```

Output:

```text
<class 'int'> <class 'float'> <class 'str'> <class 'bool'>
```

2. Program:

```python
import platform
import sys

print(platform.python_implementation())
print(sys.version_info.major == 3)
```

Output with the tested setup: `CPython` then `True`.

3. Any three, for example: data analysis with pandas, web back ends with Django or Flask, machine learning with PyTorch or scikit-learn.

4. The language is the set of rules and meaning (what valid Python is). An implementation such as CPython is a program that reads Python code and runs it. Different implementations can exist for the same language, so the word is used for both.

### Answers: Key Features of Python

1. Program:

```python
item = 10
print(item, type(item))
item = "ten"
print(item, type(item))
```

Output:

```text
10 <class 'int'>
ten <class 'str'>
```

2. Program:

```python
import statistics

data = [3, 8, 5, 10]
print(statistics.mean(data))
print(statistics.median(data))
```

Output: `6.5` for both (the mean is 26 / 4; the median is the average of the middle values 5 and 8). 

3. The line `print(number)` must be indented under the `for` line, otherwise Python raises `IndentationError: expected an indented block after 'for' statement on line 1`. Fix:

```python
for number in range(3):
    print(number)
```

Output:

```text
0
1
2
```

4. Dynamically typed: types are attached to objects and checked at run time, as when `value` was first an `int` and later a `str`. Weakly typed would mean the language silently converts between unrelated types; Python does not (`"30" + 1` raises `TypeError`), so Python is dynamic and strong.

---

## Chapter Summary and Key Takeaways

- A program is a precise, ordered set of instructions; an algorithm is the method behind it.
- Most programs follow input, process, output, and exist for automation and scale.
- Python is a general-purpose, high-level language; CPython is the standard implementation. Use Python 3.
- Python source is compiled to bytecode and run by a virtual machine automatically.
- Python is dynamically and strongly typed; names refer to objects.
- Indentation defines blocks. Use 4 spaces, never mix tabs and spaces.
- A large standard library and multiple programming styles are core strengths.
- Run every example yourself and read the real output and error messages.

Next: [Chapter 02 — Installation and Environment Setup](02-installation-and-environment-setup.md) shows how to install Python and run code.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
