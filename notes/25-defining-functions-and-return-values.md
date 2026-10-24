# Chapter 25 — Defining Functions and Return Values

> Part 5 — Functions and Functional Programming · Video: 8:41:36–9:10:11 · Previous: [24 Mutability, Iteration and Common Data-Structure Pitfalls](24-mutability-iteration-and-pitfalls.md) · Next: [26 Function Arguments](26-function-arguments.md)

**In this chapter:** how to define your own function with `def`, the difference between parameters and arguments, what `return` does, the difference between functions that return a value and functions that only perform an action ("void" functions, which return `None`), returning several values, docstrings, and the core ideas that make functions the main tool for organising programs.

**Before you start:** you need conditions and loops from [Conditional Statements](14-conditional-statements.md) and [The for Loop](17-for-loop-range-and-nested-loops.md#the-for-loop), tuples from [Tuples](21-tuples.md#tuples) (for returning several values), and the idea of calling built-in functions from [Built-in Functions, print() and Modules](03-builtin-functions-print-and-modules.md). Recap: you have already *called* functions such as `len("abc")` and `print("hi")`; this chapter shows how to *write* your own. Examples were run with Python 3.13.

---

## Defining Your Own Function

**Timestamp:** [8:41:36](https://www.youtube.com/watch?v=J9BI0jGOds8&t=31296s)

**Learning objectives:**

- Write a function with `def`, a name, parameters, a body and a call.
- Distinguish *defining* a function from *calling* it, and parameters from arguments.
- Write a docstring and give functions clear names.
- Explain why functions make code reusable, testable and readable.

**1. Intuition**

A function is a recipe card with a name. The recipe says "to make tea: boil water, add leaves, wait three minutes". Writing the card does not make tea; following it ("calling" it) does. Once the card exists, you can make tea any number of times, for any number of cups (the *parameter*), without rewriting the steps.

**2. Why does it exist?**

Without functions, a program that needs the same calculation in ten places has ten copies of the code, and a bug fix must be repeated ten times. Functions give a block of code a name, so you write it once and call it whenever needed. They also break a large problem into small, named pieces that can be understood and tested one by one.

**3. Technical explanation**

A function is defined with the keyword `def`:

1. `def` starts the definition, followed by the function name, parentheses with optional *parameters*, and a colon.
2. The indented block that follows is the *body*. It does not run at definition time.
3. A function is *called* by writing its name with parentheses and *arguments*: `greet("Asha")`. The argument values are bound to the parameter names, the body runs, and then execution continues after the call.

Terms:

- *Parameter*: the name in the definition (`name` in `def greet(name):`).
- *Argument*: the actual value passed in a call (`"Asha"`).
- *Docstring*: a string as the first statement of the body, describing what the function does; `help(function)` and `function.__doc__` show it.
- A function must be defined *before* the line that calls it runs (the definition can appear lower in the file only if the call happens later, for example inside another function that is called after the definition).
- The name follows the rules for identifiers (see [Errors and Identifiers](04-errors-and-identifiers.md)). The convention is `lowercase_with_underscores`, and a verb that says what the function does (`calculate_total`, `is_even`).
- Calling a function with the wrong number of arguments is a `TypeError`.
- Function names are ordinary variables that refer to a function object, so defining a second function with the same name replaces the first.

**4. Syntax**

```text
def function_name(parameter1, parameter2):
    """Short description of what the function does."""
    body_statements
    return result

function_name(argument1, argument2)
```

This is a pattern, not runnable code. The `return` line is optional.

**5. Example 1 — Basic**

```python
def greet(name):
    """Print a greeting for the given name."""
    print("Hello,", name)


greet("Asha")
greet("Ravi")


def add(a, b):
    return a + b


print(add(2, 3))
print(add("py", "thon"))
print(add(1.5, 2))

print(greet.__doc__)
print(type(greet).__name__)
```

Output:

```text
Hello, Asha
Hello, Ravi
5
python
3.5
Print a greeting for the given name.
function
```

Line by line:

- `greet` is defined once and called twice with different arguments; each call runs the body with `name` bound to a different value.
- `add` computes and *returns* a value, which `print` then shows. Because Python does not fix the types of parameters, the same function adds integers, joins strings, and adds floats.
- `greet.__doc__` shows the docstring. The type of a function is `function`.

**6. Example 2 — Practical**

```python
def area_of_rectangle(width, height):
    """Return the area of a rectangle."""
    return width * height


def is_even(number):
    """Return True if the number is even."""
    return number % 2 == 0


def grade(score):
    """Return a letter grade for a score from 0 to 100."""
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 50:
        return "C"
    return "F"


def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32


def count_vowels(text):
    count = 0
    for letter in text.lower():
        if letter in "aeiou":
            count += 1
    return count


print(area_of_rectangle(4, 5))
print([n for n in range(1, 8) if is_even(n)])
print([grade(s) for s in [95, 80, 60, 20]])
print(celsius_to_fahrenheit(100), celsius_to_fahrenheit(-40))
print(count_vowels("Functions are reusable"))

total = area_of_rectangle(2, 3) + area_of_rectangle(4, 4)
print(total)
print(is_even(area_of_rectangle(3, 4)))
```

Output:

```text
20
[2, 4, 6]
['A', 'B', 'C', 'F']
212.0 -40.0
9
22
True
```

Line by line:

- Each function does one small job and has a name that says what it is.
- `grade` uses `return` in several branches: the first one reached ends the function, so no `else` is needed after a `return`.
- Functions can be used inside comprehensions and expressions, and can call each other: the last line passes the result of one function into another.
- `count_vowels` uses a local variable `count` and a loop, then returns the result. The same loop-and-accumulate pattern from [The for Loop with range()](17-for-loop-range-and-nested-loops.md#the-for-loop-with-range) now lives behind a name.

**7. Example 3 — Edge case or common mistake**

Defining a function does not run it, and forgetting the parentheses does not call it:

```python
def say_hello():
    print("hello")


print("before")
say_hello
print(type(say_hello).__name__)
say_hello()
```

Output:

```text
before
function
hello
```

`say_hello` on its own line only names the function and does nothing visible (printing it would show a function object and a memory address); the parentheses make the call.

Calling before defining, and the wrong number of arguments:

```python
try:
    early()
except NameError as error:
    print("NameError:", error)


def early():
    return "defined now"


print(early())


def add_two(a, b):
    return a + b


for action in [lambda: early(1), lambda: add_two(1), lambda: add_two(1, 2, 3)]:
    try:
        action()
    except TypeError as error:
        print("TypeError:", error)
```

Output:

```text
NameError: name 'early' is not defined
defined now
TypeError: early() takes 0 positional arguments but 1 was given
TypeError: add_two() missing 1 required positional argument: 'b'
TypeError: add_two() takes 2 positional arguments but 3 were given
```

The first call (before the definition) fails with a `NameError` because `early` did not exist yet. The `TypeError` messages state exactly how many arguments were expected and how many were given.

A missing colon or indentation is a syntax error, shown as text:

```text
def broken()
    return 1
```

```text
  File "example.py", line 1
    def broken()
                ^
SyntaxError: expected ':'
```

Redefining a name replaces the earlier function:

```python
def message():
    return "first"


def message():
    return "second"


print(message())
```

Output:

```text
second
```

**8. Common mistakes**

- Forgetting the parentheses when calling (`say_hello` instead of `say_hello()`).
- Forgetting the colon after the header, or the indentation of the body.
- Calling a function before it has been defined.
- Passing the wrong number of arguments.
- Confusing parameters with arguments, or using a parameter name outside the function.
- Using the same name for two functions by accident, so the second silently replaces the first.
- Writing one very long function that does several jobs, instead of several small ones.

**9. Real-world and AI applications**

Real programs are collections of functions: `load_data`, `clean_text`, `split_into_chunks`, `build_prompt`, `call_model`, `parse_answer`. Each does one job, can be tested alone, and is reused wherever needed. When you call a model API, you are calling a function that someone else wrote and published; writing your own wrappers for it (a function that takes a question and returns an answer) is the first step toward building AI applications.

**10. Practice**

1. Write `square(n)` that returns the square of a number, and print `square(7)`.
2. Write `greet_user(name, city)` that prints `Hello <name> from <city>`.
3. Write `is_adult(age)` that returns `True` for 18 or more.
4. Write `max_of_three(a, b, c)` without using `max`.
5. Write `count_words(text)` that returns the number of words in a sentence.
6. Add a docstring to one of your functions and print it with `help` or `__doc__`.
7. What happens if you call `square()` with no argument, or with two? Predict the error message, then check.

**11. Interview questions**

- *What is a function and why use one?* A named, reusable block of code; it avoids repetition and organises programs.
- *What is the difference between a parameter and an argument?* The parameter is the name in the definition; the argument is the value supplied in the call.
- *Does defining a function run its body?* No; only calling it does.
- *What is a docstring?* A string as the first statement of a function that documents it.

**12. Quick revision**

- `def name(parameters):` with an indented body; call with `name(arguments)`.
- Definition does not run the code; the call does.
- Parameters are names; arguments are values.
- Use clear verb names, one job per function, and a docstring.
- The function must exist before it is called.

---

## Return Functions versus Void Functions

**Timestamp:** [8:48:01](https://www.youtube.com/watch?v=J9BI0jGOds8&t=31681s)

**Learning objectives:**

- Explain what `return` does, and how a function ends.
- Distinguish functions that return a value from "void" functions that only do something, and explain that void functions return `None`.
- Return several values and unpack them.
- Avoid the common mistakes of `print` instead of `return` and code after `return`.

**1. Intuition**

A calculator that shows the answer on its screen (`print`) is not the same as a calculator that hands you the answer so you can use it in the next calculation (`return`). A function that *returns* is a vending machine: you put something in, a product comes out, and you can carry it away. A *void* function is a light switch: you press it, something happens, and nothing is handed back.

**2. Why does it exist?**

Programs build results from smaller results: the total feeds the tax, the tax feeds the bill. That only works if each function *gives back* its answer to the caller. Printing is for people; returning is for the rest of the program. Python has no separate "void" keyword: a function that never returns a value simply gives back `None`, and many useful functions do their work through a side effect (printing, writing a file, changing a list).

**3. Technical explanation**

- `return value` ends the function immediately and sends `value` to the caller. Statements after it in the same path never run.
- A function that reaches its end without `return`, or uses a bare `return`, returns `None`. (`None` is Python's value meaning "nothing here".)
- *Void* is the informal name for a function that is called for what it *does* (print, save, modify an argument) and not for what it gives back. A *return function* (or "fruitful function") is called for its result.
- A function may have several `return` statements, in different branches. Only one runs per call.
- To return several values, separate them by commas: `return low, high`. Python packs them into a *tuple*, which the caller can unpack: `low, high = f()`.
- `print` and `return` are different: `print` shows text on the screen; `return` passes a value back. A function that prints its result and returns nothing cannot be used in further calculations: the caller gets `None`.
- Side effects: a function can change a mutable argument in place (see [Mutable versus Immutable Objects](24-mutability-iteration-and-pitfalls.md#mutable-versus-immutable-objects)). It is clearer to make a function either compute and return, or act, and not both.
- Return `None` explicitly or implicitly for "no result", and `True`/`False` for yes/no questions (functions with such names usually start with `is_` or `has_`).

**4. Syntax**

```text
def with_result(x):
    return x * 2            # returns a value

def only_acts(x):
    print(x)                # no return: returns None

def several(x):
    return x, x * 2         # returns a tuple

low, high = several(5)
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
def double(n):
    return n * 2


def show_double(n):
    print(n * 2)


a = double(4)
b = show_double(4)
print("a is", a)
print("b is", b)
print(double(double(3)))


def min_max(numbers):
    return min(numbers), max(numbers)


low, high = min_max([5, 2, 9, 1])
print(low, high)
print(min_max([5, 2, 9, 1]))


def early_exit():
    print("start")
    return
    print("never printed")


print(early_exit())
```

Output:

```text
8
a is 8
b is None
12
1 9
(1, 9)
start
None
```

Line by line:

- `double(4)` returns 8, which is stored in `a`. `show_double(4)` prints 8 and returns nothing, so `b` is `None`.
- Because `double` returns a value, it can be nested: `double(double(3))` is 12. A void function cannot be used this way.
- `min_max` returns two values as a tuple; the caller unpacks them into `low` and `high`, or keeps the tuple.
- `return` by itself ends the function early; the line after it never runs, and the call gives `None`.

**6. Example 2 — Practical**

```python
def calculate_bill(price, quantity, tax_rate=0.18):
    subtotal = price * quantity
    tax = subtotal * tax_rate
    return subtotal, tax, subtotal + tax


def print_receipt(item, price, quantity):
    subtotal, tax, total = calculate_bill(price, quantity)
    print(f"{item} x{quantity}: {subtotal} + tax {tax:.2f} = {total:.2f}")


print_receipt("Notebook", 50, 3)

subtotal, tax, total = calculate_bill(100, 2)
print(round(total))


def find_first_negative(numbers):
    for index, value in enumerate(numbers):
        if value < 0:
            return index
    return -1


print(find_first_negative([4, 7, -2, 9]), find_first_negative([1, 2]))


def classify(n):
    if n < 0:
        return "negative"
    elif n == 0:
        return "zero"
    return "positive"


print([classify(n) for n in (-5, 0, 5)])


def append_twice(items, value):
    items.append(value)
    items.append(value)


data = [1]
result = append_twice(data, 7)
print(data, result)


def average(numbers):
    if not numbers:
        return None
    return sum(numbers) / len(numbers)


print(average([2, 4, 9]), average([]))
```

Output:

```text
Notebook x3: 150 + tax 27.00 = 177.00
236
2 -1
['negative', 'zero', 'positive']
[1, 7, 7] None
5.0 None
```

Line by line:

- `calculate_bill` returns three numbers; `print_receipt` is a void function that uses them to print. This split (compute in one function, display in another) keeps each function easy to test.
- `find_first_negative` returns from inside the loop as soon as it finds a match, and returns `-1` after the loop if nothing was found. It uses the early-return idea from [The break Statement](16-while-loop-and-loop-control.md#the-break-statement).
- `classify` has three return statements, and only one runs per call.
- `append_twice` is void: its work is a side effect on the list that was passed in, and its return value is `None`.
- `average` returns `None` for an empty list instead of failing with a division by zero. The caller must then check for `None`.

**7. Example 3 — Edge case or common mistake**

Using `print` where `return` was meant:

```python
def add_print(a, b):
    print(a + b)


result = add_print(2, 3)
print(result)
try:
    print(result + 10)
except TypeError as error:
    print("TypeError:", error)
```

Output:

```text
5
None
TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
```

The sum was shown on the screen, but the function gave `None` back, so the next calculation failed. Return the value and let the caller decide what to print.

A `return` inside a loop ends the whole function on the first round, which is a classic bug:

```python
def sum_to_n_wrong(n):
    total = 0
    for i in range(1, n + 1):
        total += i
        return total


def sum_to_n(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


print(sum_to_n_wrong(4), sum_to_n(4))
```

Output:

```text
1 10
```

The wrong version returns after adding only 1, because the `return` is indented inside the loop. Put the `return` after the loop.

Code after a `return` never runs, and a missing `return` in some branch silently gives `None`:

```python
def sign(n):
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"


print(sign(5), sign(-5), sign(0))


def tricky():
    return 1
    print("unreachable")


print(tricky())
```

Output:

```text
positive negative None
1
```

For `0` neither branch returns, so the function ends at the bottom and gives `None`. Add a final `return "zero"` so that every path returns something.

Returning several values versus returning a list:

```python
def pair():
    return 1, 2


def as_list():
    return [1, 2]


print(pair(), type(pair()).__name__)
print(as_list(), type(as_list()).__name__)
x, y = pair()
print(x + y)
```

Output:

```text
(1, 2) tuple
[1, 2] list
3
```

`return 1, 2` returns a tuple (no brackets needed). A list works too, and is the better choice when the number of items varies.

**8. Common mistakes**

- Printing a result instead of returning it, then trying to use it.
- Putting `return` inside a loop when it belongs after the loop.
- Missing `return` in one branch, so the function returns `None`.
- Writing code after `return` and expecting it to run.
- Assigning the result of a void function and using it as if it held a value.
- Returning different kinds of things from different branches (a number in one case, a string in another).
- Mixing computation and printing in one function, which makes it hard to reuse and test.

**9. Real-world and AI applications**

A function that calls a model and *returns* the answer text can be used in a larger program: store it, check it, pass it to the next step. A function that only prints the answer is useful in a demo but cannot be tested or chained. Pipelines are built from functions that each return something: `clean(text)` returns text, `chunk(text)` returns a list of chunks, `embed(chunk)` returns a list of numbers, `search(query)` returns the best matches. Void functions handle the edges: saving a file, logging, printing a report.

**10. Practice**

1. Write `cube(n)` that returns `n ** 3`, and `show_cube(n)` that prints it. Explain the difference in what each returns.
2. Write `stats(numbers)` returning the smallest, largest and average. Unpack the result.
3. Write `is_palindrome(text)` that returns `True` or `False` (ignore case).
4. Write `first_long_word(words, limit)` that returns the first word longer than `limit`, or `None`.
5. Find the bug: a function `total(numbers)` with `return` inside the `for` loop. Fix it.
6. What do `print(print("x"))` and `len(print("y"))` do, and why?
7. Write a void function `add_item(basket, item)` that appends to a list, and a return function `with_item(basket, item)` that returns a new list. When would you prefer each?

**11. Interview questions**

- *What does a function return if it has no `return` statement?* `None`.
- *What is the difference between `print` and `return`?* `print` displays text; `return` hands a value back to the caller, ending the function.
- *How can a function return multiple values?* It returns a tuple, which the caller can unpack.
- *Can a function have more than one `return`?* Yes, but only one executes per call.
- *What is a void function in Python?* An informal term for a function used for its side effects that returns `None`.

**12. Quick revision**

- `return` sends a value back and ends the function at once.
- No `return` (or bare `return`) gives `None`.
- Return functions compute; void functions act. Prefer to separate the two.
- `return a, b` gives a tuple; unpack with `x, y = f()`.
- Check that every branch returns something sensible.

---

## Functions: Core Concepts

**Timestamp:** [8:59:32](https://www.youtube.com/watch?v=J9BI0jGOds8&t=32372s)

**Learning objectives:**

- Describe what happens, step by step, when a function is called (the call and the return).
- Explain that functions can call other functions and themselves (recursion), and that each call has its own local variables.
- Use a docstring and meaningful names, and write small functions with one job.
- Test a function with a few calls, including edge cases.
- Know where `main()` and `if __name__ == "__main__":` fit.

**1. Intuition**

Each call to a function is like handing a worker a fresh sheet of paper: they write their working on it, give you the answer, and throw the paper away. The next call gets a new, clean sheet. This is why two calls to the same function never interfere with each other's working, and why variables inside a function do not exist outside it.

**2. Why does it exist?**

Large programs are manageable only if they are made of pieces that can be understood on their own. The core ideas (a call creates a fresh workspace, results come back by `return`, small functions can be combined) are what make that possible: you can trust a function by its name, inputs and outputs without re-reading its inside.

**3. Technical explanation**

*What happens at a call.* When `f(a, b)` runs:

1. The arguments are evaluated.
2. Python creates a new, temporary *local scope* (a private set of names) for this call.
3. The arguments are bound to the parameters inside that scope.
4. The body runs. Variables created inside live in the local scope.
5. At `return` (or the end of the body), the local scope is discarded and the value goes back to the caller, which continues from where it left off.

Python keeps track of calls that are in progress on a *call stack*: if `a()` calls `b()` which calls `c()`, then `c` finishes first, then `b`, then `a`. A traceback prints this stack.

*Functions calling functions.* Break a task into helper functions, each with one job, and have a higher-level function call them. This is called *decomposition*.

*Recursion.* A function can call itself. It needs a *base case* (when to stop) and a step that moves toward it. Each call has its own local variables. Recursion that never reaches the base case ends with `RecursionError` (Python limits the depth, by default about 1000 calls).

*Good function habits.*

- One job per function, with a name that says it.
- A docstring for what it does, what it takes and what it returns.
- Prefer returning values over printing and over changing global variables (scope is covered in [Variable Scope](27-variable-scope.md)).
- Do not change the arguments in place unless that is the purpose.
- Test with normal input, edge cases (empty, zero, negative) and wrong input.

*The `main` pattern.* Put the program's entry code in a `main()` function and call it under `if __name__ == "__main__":`. The code in that block runs when the file is run directly, but not when the file is imported as a module by another file (see [Built-in Functions, print() and Modules](03-builtin-functions-print-and-modules.md)).

**4. Syntax**

```text
def helper(x):
    ...

def main():
    result = helper(5)
    print(result)

if __name__ == "__main__":
    main()
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
def square(n):
    return n * n


def sum_of_squares(a, b):
    return square(a) + square(b)


print(sum_of_squares(3, 4))


def countdown(n):
    if n == 0:
        print("liftoff")
        return
    print(n)
    countdown(n - 1)


countdown(3)


def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)


print(factorial(5))


def f():
    value = "inside"
    return value


print(f())
try:
    print(value)
except NameError as error:
    print("NameError:", error)
```

Output:

```text
25
3
2
1
liftoff
120
inside
NameError: name 'value' is not defined
```

Line by line:

- `sum_of_squares` calls `square` twice. The caller does not need to know how `square` works.
- `countdown` calls itself with a smaller number until the base case `n == 0` stops the recursion. Each call prints one number.
- `factorial(5)` works by `5 * factorial(4)`, down to the base case `factorial(1)`, then multiplies the results on the way back.
- `value` exists only inside `f`; outside it is a `NameError`.

**6. Example 2 — Practical**

```python
def clean(text):
    """Lower-case the text and strip spaces."""
    return text.strip().lower()


def tokenize(text):
    """Split cleaned text into words without punctuation."""
    words = []
    for word in clean(text).split():
        word = word.strip(".,!?")
        if word:
            words.append(word)
    return words


def word_frequencies(text):
    """Return a dictionary of word counts."""
    counts = {}
    for word in tokenize(text):
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_words(text, n=2):
    """Return the n most frequent words as (word, count) pairs."""
    counts = word_frequencies(text)
    ranked = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))
    return ranked[:n]


def report(text):
    for word, count in top_words(text, 3):
        print(f"{word:<8}{count}")


def main():
    sample = "  The cat sat. The dog sat! The end.  "
    print(tokenize(sample))
    print(word_frequencies(sample))
    report(sample)


main()

print(top_words.__doc__)


def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


print([fibonacci(i) for i in range(10)])


def depth_first_sum(nested):
    total = 0
    for item in nested:
        if isinstance(item, list):
            total += depth_first_sum(item)
        else:
            total += item
    return total


print(depth_first_sum([1, [2, 3], [4, [5, 6]]]))
```

Output:

```text
['the', 'cat', 'sat', 'the', 'dog', 'sat', 'the', 'end']
{'the': 3, 'cat': 1, 'sat': 2, 'dog': 1, 'end': 1}
the     3
sat     2
cat     1
Return the n most frequent words as (word, count) pairs.
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
21
```

Line by line:

- The text pipeline is built from four small functions, each calling the one before it: `clean`, `tokenize`, `word_frequencies`, `top_words`. Each can be tested separately, and `main` shows the whole flow.
- Sorting with `key=lambda pair: (-pair[1], pair[0])` ranks by count (highest first) and breaks ties alphabetically (see [Lambda Functions](28-first-class-functions-and-lambda.md#lambda-functions)).
- Docstrings document each function; `top_words.__doc__` prints one.
- `fibonacci` calls itself twice (a natural but slow recursion for large `n`). `depth_first_sum` uses recursion for nested lists, where the depth is not known in advance: when an item is itself a list, the function calls itself on it.

**7. Example 3 — Edge case or common mistake**

Recursion without a base case, shown with a small depth limit so that the example is quick:

```python
import sys

print(sys.getrecursionlimit() >= 1000)


def endless(n):
    return endless(n + 1)


try:
    endless(0)
except RecursionError as error:
    print("RecursionError:", error)
```

Output:

```text
True
RecursionError: maximum recursion depth exceeded
```

Without a base case, each call starts another, until Python stops the program with `RecursionError`. Every recursive function needs a base case, and each call must get closer to it.

A recursive function that is correct but slow, and a loop version:

```python
def fib_slow(n):
    return n if n < 2 else fib_slow(n - 1) + fib_slow(n - 2)


def fib_loop(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


print(fib_slow(20), fib_loop(20))
print(fib_loop(90))
```

Output:

```text
6765 6765
2880067194370816120
```

`fib_slow` recomputes the same values again and again, so its running time explodes as `n` grows; `fib_loop(90)` is instant. Prefer a loop when it is as clear as the recursion.

Testing edge cases before trusting a function:

```python
def average(numbers):
    return sum(numbers) / len(numbers)


for case in [[2, 4, 6], [5], []]:
    try:
        print(case, "->", average(case))
    except ZeroDivisionError as error:
        print(case, "-> ZeroDivisionError:", error)
```

Output:

```text
[2, 4, 6] -> 4.0
[5] -> 5.0
[] -> ZeroDivisionError: division by zero
```

The empty list is an edge case the author did not think about. Decide what the function should do (return `None`, raise a clearer error, or return 0) and test it.

The `main` guard:

```python
def main():
    print("running as a program")


print("__name__ is", __name__)
if __name__ == "__main__":
    main()
```

Output:

```text
__name__ is __main__
running as a program
```

When the file is run directly, `__name__` is `"__main__"`, so `main()` runs. If another file imports this one, `__name__` is the module's name and `main()` does not run automatically. (Here the output shows `__main__` because the example is run as a program.)

**8. Common mistakes**

- Recursion without a base case, or a step that never reaches it.
- Repeating the same code in several places instead of making a helper function.
- Writing a long function that does five things.
- Using variables from outside the function instead of parameters.
- Not testing edge cases: empty input, zero, one item, negative numbers.
- Forgetting that each call has its own local variables, then expecting a value to persist from one call to the next.
- Putting program code at the top level of a module that will be imported, instead of under `if __name__ == "__main__":`.

**9. Real-world and AI applications**

AI code follows the same shape: small functions with one job (`clean_text`, `split_into_chunks`, `build_prompt`, `parse_response`) composed into a pipeline, with a `main()` at the bottom. Recursion appears in traversing nested data, such as the nested dictionaries and lists in a JSON response, and in tree-structured data such as file folders. The `__main__` guard lets you write a module of helper functions that other scripts import and that can also be run on its own for a quick test. Agent programs (see [Model Context Protocol and AI Agents](38-mcp-and-ai-agents.md)) are loops that call functions (tools) and use their return values.

**10. Practice**

1. Write `power(base, exponent)` recursively (use `power(b, 0) == 1` as the base case) and compare with `**`.
2. Write `sum_digits(n)` recursively: `sum_digits(1234)` gives 10.
3. Write `reverse_text(text)` recursively.
4. Split a task into helper functions: read a list of numbers as text (`"3, 5, x, 8"`), convert the valid ones to integers, and compute their sum. Each step must be a function.
5. Write `count_down_then_up(n)` that prints `n` down to 1 and then back up to `n`, using recursion.
6. Test `average` from this chapter with an empty list and rewrite it to return `None` for that case.
7. Use the `__main__` guard to make a script that prints a message only when run directly.

**11. Interview questions**

- *What is recursion and what does it need?* A function that calls itself; it needs a base case and progress toward it.
- *What is the call stack?* The record of active function calls; the most recent call finishes first.
- *What happens to local variables when a function returns?* They are discarded; each new call starts with fresh ones.
- *What does `if __name__ == "__main__":` do?* Runs the block only when the file is executed directly, not when it is imported.
- *When would you prefer a loop to recursion?* When the loop is as clear, because it avoids the depth limit and repeated work.

**12. Quick revision**

- A call creates a fresh local scope; `return` ends it and delivers the value.
- Functions can call functions; recursion needs a base case.
- Keep functions small, named by their job, documented and tested on edge cases.
- Local variables vanish after the call.
- `main()` plus `if __name__ == "__main__":` for runnable scripts.

---

## Answers to Practice Exercises

### Answers: Defining Your Own Function

1.

```python
def square(n):
    return n * n


print(square(7))
```

Output:

```text
49
```

2.

```python
def greet_user(name, city):
    print(f"Hello {name} from {city}")


greet_user("Asha", "Chennai")
```

Output:

```text
Hello Asha from Chennai
```

3.

```python
def is_adult(age):
    return age >= 18


print(is_adult(17), is_adult(18), is_adult(40))
```

Output:

```text
False True True
```

4.

```python
def max_of_three(a, b, c):
    largest = a
    if b > largest:
        largest = b
    if c > largest:
        largest = c
    return largest


print(max_of_three(4, 9, 2), max_of_three(7, 7, 1), max_of_three(-1, -5, -3))
```

Output:

```text
9 7 -1
```

5.

```python
def count_words(text):
    return len(text.split())


print(count_words("functions make code reusable"), count_words(""))
```

Output:

```text
4 0
```

6.

```python
def square(n):
    """Return n multiplied by itself."""
    return n * n


print(square.__doc__)
```

Output:

```text
Return n multiplied by itself.
```

7. Calling `square()` with no argument gives `TypeError: square() missing 1 required positional argument: 'n'`. Calling it with two gives `TypeError: square() takes 1 positional argument but 2 were given`.

```python
def square(n):
    return n * n


for args in [(), (1, 2)]:
    try:
        square(*args)
    except TypeError as error:
        print("TypeError:", error)
```

Output:

```text
TypeError: square() missing 1 required positional argument: 'n'
TypeError: square() takes 1 positional argument but 2 were given
```

### Answers: Return Functions versus Void Functions

1.

```python
def cube(n):
    return n ** 3


def show_cube(n):
    print(n ** 3)


print(cube(3))
result = show_cube(3)
print(result)
```

Output:

```text
27
27
None
```

`cube` hands the value back (it can be used in further calculations); `show_cube` only prints and returns `None`.

2.

```python
def stats(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)


smallest, largest, mean = stats([4, 8, 15, 16, 23, 42])
print(smallest, largest, mean)
```

Output:

```text
4 42 18.0
```

3.

```python
def is_palindrome(text):
    text = text.lower()
    return text == text[::-1]


print(is_palindrome("Level"), is_palindrome("Python"))
```

Output:

```text
True False
```

4.

```python
def first_long_word(words, limit):
    for word in words:
        if len(word) > limit:
            return word
    return None


print(first_long_word(["go", "python", "code"], 4), first_long_word(["a", "b"], 3))
```

Output:

```text
python None
```

5. The `return` is inside the loop, so the function ends after the first item. Move it out:

```python
def total_wrong(numbers):
    result = 0
    for n in numbers:
        result += n
        return result


def total(numbers):
    result = 0
    for n in numbers:
        result += n
    return result


print(total_wrong([1, 2, 3]), total([1, 2, 3]))
```

Output:

```text
1 6
```

6. `print("x")` prints `x` and returns `None`, so the outer `print` then prints `None`. `len(print("y"))` prints `y`, and then `len(None)` fails with a `TypeError`, because `None` has no length.

```python
print(print("x"))
try:
    len(print("y"))
except TypeError as error:
    print("TypeError:", error)
```

Output:

```text
x
None
y
TypeError: object of type 'NoneType' has no len()
```

7.

```python
def add_item(basket, item):
    basket.append(item)


def with_item(basket, item):
    return basket + [item]


cart = ["tea"]
add_item(cart, "milk")
print(cart)
new_cart = with_item(cart, "rice")
print(cart, new_cart)
```

Output:

```text
['tea', 'milk']
['tea', 'milk'] ['tea', 'milk', 'rice']
```

Use the void version when the list is meant to be updated (a shared cart). Use the returning version when you must keep the original unchanged or want to chain calls.

### Answers: Functions: Core Concepts

1.

```python
def power(base, exponent):
    if exponent == 0:
        return 1
    return base * power(base, exponent - 1)


print(power(2, 10), 2 ** 10, power(5, 0))
```

Output:

```text
1024 1024 1
```

2.

```python
def sum_digits(n):
    if n < 10:
        return n
    return n % 10 + sum_digits(n // 10)


print(sum_digits(1234), sum_digits(7))
```

Output:

```text
10 7
```

3.

```python
def reverse_text(text):
    if len(text) <= 1:
        return text
    return reverse_text(text[1:]) + text[0]


print(reverse_text("python"))
```

Output:

```text
nohtyp
```

4.

```python
def split_values(text):
    return [part.strip() for part in text.split(",")]


def to_numbers(parts):
    return [int(part) for part in parts if part.isdigit()]


def total(numbers):
    return sum(numbers)


def main():
    parts = split_values("3, 5, x, 8")
    numbers = to_numbers(parts)
    print(parts, numbers, total(numbers))


main()
```

Output:

```text
['3', '5', 'x', '8'] [3, 5, 8] 16
```

5.

```python
def count_down_then_up(n):
    if n == 0:
        return
    print(n, end=" ")
    count_down_then_up(n - 1)
    print(n, end=" ")


count_down_then_up(3)
print()
```

Output:

```text
3 2 1 1 2 3 
```

The second `print` runs as each call returns, in reverse order.

6.

```python
def average(numbers):
    if not numbers:
        return None
    return sum(numbers) / len(numbers)


print(average([2, 4, 6]), average([]))
```

Output:

```text
4.0 None
```

7.

```python
def main():
    print("this runs only when executed directly")


if __name__ == "__main__":
    main()
```

Output:

```text
this runs only when executed directly
```

---

## Chapter Summary and Key Takeaways

- `def name(parameters):` defines a function; the body runs only when the function is called with arguments. Parameters are the names in the definition, arguments are the values supplied.
- `return` sends a value back and ends the function; a function with no `return` gives `None`. Return functions compute results; void functions act (print, save, change a list).
- `return a, b` returns a tuple, which the caller unpacks. Do not confuse `print` with `return`, and keep `return` outside loops unless an early exit is intended.
- Each call has its own local variables and is discarded when the function returns; functions can call other functions, and recursion needs a base case.
- Keep functions small, named for their job, documented, and tested on edge cases; use `main()` and the `__main__` guard to make runnable scripts.

Next: [Chapter 26 — Function Arguments](26-function-arguments.md) covers positional, default, `*args` and `**kwargs` arguments.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
