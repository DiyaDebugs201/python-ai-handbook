# Chapter 28 — First-Class Functions and Lambda

> Part 5 — Functions and Functional Programming · Video: 9:56:08–10:32:38 · Previous: [27 Variable Scope](27-variable-scope.md) · Next: [29 map(), filter() and reduce()](29-map-filter-reduce.md)

**In this chapter:** the idea that a function is an object like any other: it can be stored in a variable, put in a list or dictionary, passed to another function, and returned from one. This leads to higher-order functions, and to the `lambda` expression, a compact way of writing a small unnamed function for a one-off job such as a sorting key.

**Before you start:** you need defining functions and `return` from [Defining Your Own Function](25-defining-functions-and-return-values.md#defining-your-own-function), arguments from [Function Arguments](26-function-arguments.md), scope and closures from [Variable Scope](27-variable-scope.md), and `sorted(..., key=...)` from [Built-in List Functions](19-list-functions-methods-and-copying.md#built-in-list-functions). Recap: calling a function needs parentheses (`f(3)`), and writing the name alone (`f`) refers to the function without calling it. Examples were run with Python 3.13.

---

## Functions as First-Class Citizens

**Timestamp:** [9:56:08](https://www.youtube.com/watch?v=J9BI0jGOds8&t=35768s)

**Learning objectives:**

- Explain what "first-class" means and show the four things you can do with a function object.
- Distinguish a function (`f`) from a call to it (`f()`).
- Write higher-order functions that take or return functions.
- Use functions in dictionaries to replace long `if`/`elif` chains.

**1. Intuition**

A recipe card is a thing you can hand to someone. You can put it in a box with other cards, pass it to a friend who then follows it, or let a cook choose which card to use depending on the guest. In Python, a function is such a card: the *definition* is the card, and the *call* is following it. Because the card is a thing, you can treat it like any other thing.

**2. Why does it exist?**

Many tasks are the same except for one step: sort the people, but by *which* field? Apply an operation to every item, but *which* operation? Run something, and then, *whatever the caller chooses*, report the result. If functions could not be passed around, every variation would need a copy of the whole code. When a function can be an argument, you write the general routine once and let the caller plug in the varying step.

**3. Technical explanation**

In Python a function is an *object* of type `function`. "First-class" means it has all the rights of other values (numbers, strings, lists):

1. **Assign it** to a variable: `say = greet` makes a second name for the same function.
2. **Store it** in a data structure: `[len, str.upper]` or `{"add": add, "sub": sub}`.
3. **Pass it** as an argument to another function: `apply(function, value)`.
4. **Return it** from a function (a function factory), often forming a closure (see [Variable Scope](27-variable-scope.md#variable-scope-local-vs-global)).

Related ideas:

- *Higher-order function*: a function that takes a function as an argument or returns one. Built-in examples: `sorted(key=...)`, `max(key=...)`, `map`, `filter` (see [The map() Function](29-map-filter-reduce.md#the-map-function)).
- *Callback*: a function given to another function to be called later.
- *Function name versus call*: `f` is the object; `f()` runs it and gives its result. Passing `f()` where `f` was meant passes the *result*, a common mistake.
- Functions have attributes: `f.__name__` (its name) and `f.__doc__` (its docstring). `callable(x)` tells whether `x` can be called.
- *Dispatch table*: a dictionary that maps a key (a command name) to a function. It replaces a long chain of `if`/`elif` comparisons.
- Built-in and method functions are objects too: `len`, `str.upper`, `print`.
- A *decorator* (not required here) is a higher-order function that wraps another function; it is built on exactly these ideas.

**4. Syntax**

```text
alias = function_name                  # assign
table = {"key": function_name}         # store
higher_order(function_name, value)     # pass (no parentheses after the name)

def make():
    def inner(): ...
    return inner                       # return a function
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
def shout(text):
    return text.upper() + "!"


print(type(shout).__name__, shout.__name__, callable(shout))

yell = shout
print(yell("hello"))
print(yell is shout)

def apply(function, value):
    return function(value)


print(apply(shout, "hi"))
print(apply(len, "hello"))
print(apply(str.title, "python is fun"))

tools = [len, str.upper, str.title]
for tool in tools:
    print(tool.__name__, tool("data science"))

def make_greeter(greeting):
    def greeter(name):
        return f"{greeting}, {name}"
    return greeter


hello = make_greeter("Hello")
print(hello("Asha"))
print(make_greeter("Hi")("Ravi"))
```

Output:

```text
function shout True
HELLO!
True
HI!
5
Python Is Fun
len 12
upper DATA SCIENCE
title Data Science
Hello, Asha
Hi, Ravi
```

Line by line:

- A function has a type (`function`), a `__name__`, and `callable` says it can be called. (Printing it directly would show a function object with a memory address that changes from run to run, so that is not shown.)
- `yell = shout` gives the function a second name; both refer to the same object (`is` is `True`).
- `apply` receives a function and a value, and calls the function inside. It works with a user-defined function, a built-in (`len`) and a method (`str.title`).
- Functions in a list can be looped over and called.
- `make_greeter` returns a new function each time, remembering `greeting` (a closure). `make_greeter("Hi")("Ravi")` calls the returned function immediately.

**6. Example 2 — Practical**

```python
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


operations = {"add": add, "sub": subtract, "mul": multiply}


def calculate(command, a, b):
    function = operations.get(command)
    if function is None:
        return f"unknown command: {command}"
    return function(a, b)


print(calculate("add", 6, 3), calculate("sub", 6, 3), calculate("mul", 6, 3))
print(calculate("div", 6, 3))


def apply_twice(function, value):
    return function(function(value))


print(apply_twice(lambda x: x * 2, 5))
print(apply_twice(str.strip, "  padded  "))


def compose(first, second):
    def combined(value):
        return second(first(value))
    return combined


clean_and_count = compose(str.strip, len)
print(clean_and_count("   hello   "))


def process_all(items, step):
    return [step(item) for item in items]


print(process_all(["a", "b"], str.upper))
print(process_all([1, 4, 9], lambda n: n ** 0.5))


def timed_call(function, *args):
    import time
    start = time.perf_counter()
    result = function(*args)
    elapsed = time.perf_counter() - start
    return result, elapsed >= 0


print(timed_call(sum, [1, 2, 3]))

people = [("Asha", 30), ("Ravi", 25), ("Meena", 28)]


def by_age(person):
    return person[1]


print(sorted(people, key=by_age))
print(max(people, key=by_age))
```

Output:

```text
9 3 18
unknown command: div
20
padded
5
['A', 'B']
[1.0, 2.0, 3.0]
(6, True)
[('Ravi', 25), ('Meena', 28), ('Asha', 30)]
('Asha', 30)
```

Line by line:

- The dictionary `operations` maps command names to functions, so `calculate` needs no `if`/`elif` chain; adding a new command means adding one entry. `get` returns `None` for unknown commands.
- `apply_twice` takes any function and applies it two times. It works for a small anonymous function (`lambda`, see below) and for `str.strip`.
- `compose` builds a new function from two: first one, then the other. `clean_and_count` strips the text and then counts the characters.
- `process_all` applies a caller-chosen `step` to each item, the general idea behind `map`.
- `timed_call` takes a function and its arguments (`*args`), runs it, and measures the time (only the harmless "elapsed is not negative" check is shown, since timings vary).
- `by_age` is passed to `sorted` and `max` as the `key`: Python calls it on each item to get the value to compare. Note that the *name* `by_age` is given, with no parentheses.

**7. Example 3 — Edge case or common mistake**

Passing a call instead of the function:

```python
def double(n):
    return n * 2


numbers = [3, 1, 2]
try:
    print(sorted(numbers, key=double(3)))
except TypeError as error:
    print("TypeError:", error)
print(sorted(numbers, key=double))
print(sorted(numbers, key=double, reverse=True))
```

Output:

```text
TypeError: 'int' object is not callable
[1, 2, 3]
[3, 2, 1]
```

`double(3)` runs the function now and passes its *result* (6), which is not callable. `key=double` passes the function itself.

Returning the function versus its result:

```python
def make_adder(n):
    def add(x):
        return x + n
    return add


def make_adder_wrong(n):
    def add(x):
        return x + n
    return add(n)


add5 = make_adder(5)
print(add5(10), type(add5).__name__)
wrong = make_adder_wrong(5)
print(wrong, type(wrong).__name__)
try:
    wrong(10)
except TypeError as error:
    print("TypeError:", error)
```

Output:

```text
15 function
10 int
TypeError: 'int' object is not callable
```

`return add` returns the function; `return add(n)` returns the number 10, which cannot be called.

A dispatch table needs functions, not calls, as values:

```python
def hello():
    return "hello"


def bye():
    return "bye"


right = {"h": hello, "b": bye}
wrong = {"h": hello(), "b": bye()}
print(right["h"](), wrong["h"])
```

Output:

```text
hello hello
```

In `right` the values are functions to call later; in `wrong` they were called immediately when the dictionary was built, so it holds strings.

Methods looked up from a class are also functions, but "bound" methods carry their object:

```python
text = "hello"
bound = text.upper
unbound = str.upper
print(bound(), unbound("world"))
print(callable(bound), callable("hello"))
```

Output:

```text
HELLO WORLD
True False
```

`text.upper` already contains `text`; `str.upper` needs the string as an argument. A string is not callable.

**8. Common mistakes**

- Writing parentheses when you meant to pass the function (`key=f()` instead of `key=f`).
- Leaving out parentheses when you meant to call it (`f` instead of `f()`).
- Returning the result of calling the inner function instead of the function itself.
- Building a dispatch dictionary with calls instead of function names.
- Forgetting that a closure keeps a variable alive (and shares it).
- Writing deeply nested functions-returning-functions that nobody can follow, when a simple loop would do.

**9. Real-world and AI applications**

Passing functions is the basis of flexible code: sorting by a key, event handlers, callbacks, and data-processing steps chosen at run time. Dispatch tables map command names to functions, as in a chatbot that routes "/help" and "/reset" to different handlers. The idea is central to AI agents: a model chooses a *tool* by name, and the program looks the name up in a dictionary of functions and calls it with the arguments the model supplied (see [Model Context Protocol and AI Agents](38-mcp-and-ai-agents.md)). Pipelines are built by composing functions: clean, tokenise, embed, search.

**10. Practice**

1. Assign `len` to a new name `count` and use it on a string and a list.
2. Write `apply_to_all(function, items)` that returns a list of the results, and use it with `str.upper` and with your own `square` function.
3. Build a dictionary of three functions (`upper`, `lower`, `title`) and call the right one chosen by a string key.
4. Write `make_multiplier(factor)` that returns a function, and create `double` and `triple`.
5. Write `compose(f, g)` returning a function that applies `f` and then `g`; test it with `str.strip` and `str.title`.
6. Sort `["pear", "fig", "banana"]` by length by passing a function (not a call) as `key`.
7. Explain why `sorted(words, key=len())` fails.

**11. Interview questions**

- *What does "functions are first-class objects" mean?* They can be assigned to variables, stored in data structures, passed as arguments and returned from functions.
- *What is a higher-order function?* One that takes a function as an argument or returns one.
- *What is the difference between `f` and `f()`?* `f` is the function object; `f()` calls it and gives its result.
- *What is a callback?* A function passed to another function to be called later.
- *What is a dispatch table?* A dictionary from keys to functions, used instead of an `if`/`elif` chain.

**12. Quick revision**

- A function is an object: assign it, store it, pass it, return it.
- `f` is the function; `f()` is the call.
- Higher-order functions take or return functions (`sorted(key=...)`, `map`, `filter`).
- Dispatch tables replace long `if`/`elif` chains.
- Pass function names without parentheses.

---

## Lambda Functions

**Timestamp:** [10:22:04](https://www.youtube.com/watch?v=J9BI0jGOds8&t=37324s)

**Learning objectives:**

- Write a `lambda` expression and convert between a `lambda` and a `def`.
- Use lambdas as the `key` for `sorted`, `max` and `min`, and as arguments to higher-order functions.
- State the limits of a lambda and when a named function is better.
- Avoid the closure trap in lambdas created in a loop.

**1. Intuition**

A lambda is a sticky note with a one-line instruction, instead of a full recipe card. You write it where you need it, use it once, and throw it away. "Sort these people by age" needs only the tiny instruction "take the age"; giving that a name and a whole `def` block feels like overkill.

**2. Why does it exist?**

Higher-order functions (such as `sorted` with a `key`) often need a very small function used only once. Defining a named function elsewhere for such a one-liner makes the code longer and moves the logic away from where it is used. A lambda lets you write the small function right at the point of use.

**3. Technical explanation**

A lambda is a function written as an *expression*:

```text
lambda parameters: expression
```

- It can have any number of parameters (`lambda x, y: x + y`), default values, `*args` and `**kwargs`, but only a **single expression**. The value of that expression is returned automatically; there is no `return` keyword.
- It cannot contain statements: no assignment (`x = 1`), no `if` *statement* (but the conditional expression `a if test else b` is allowed), no loops, no `pass`.
- It is *anonymous*: its `__name__` is `<lambda>`. Assigning it to a name (`square = lambda x: x * x`) works but offers no advantage over `def`, and style guides recommend a `def` in that case (it gives a proper name in tracebacks and room for a docstring).
- A lambda is a normal function object: it can be called, passed, stored and returned.
- Typical uses: the `key` of `sorted`, `min`, `max`; the function arguments of `map`, `filter`, `reduce` (next chapter); small callbacks; and entries in a dispatch dictionary.
- Lambdas follow the scope rules: they can read variables from the enclosing scope (closures), and loop variables are captured *by variable*, not by value (see [Variable Scope](27-variable-scope.md#variable-scope-local-vs-global)).
- Keep lambdas short and obvious. If it needs more than one simple expression, use `def`.

**4. Syntax**

```text
lambda: constant
lambda x: expression_using_x
lambda x, y: expression_using_x_and_y
lambda x, y=2: expression
lambda item: item[1]             # as a sort key
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
def square_def(x):
    return x * x


square_lambda = lambda x: x * x
print(square_def(5), square_lambda(5))

add = lambda a, b: a + b
print(add(2, 3))
print((lambda x: x + 1)(10))

greet = lambda name="friend": f"Hello, {name}"
print(greet(), greet("Asha"))

print((lambda: 42)())
print(square_def.__name__, square_lambda.__name__)

is_even = lambda n: n % 2 == 0
print([is_even(n) for n in range(5)])

label = lambda n: "positive" if n > 0 else "non-positive"
print(label(3), label(-3))
```

Output:

```text
25 25
5
11
Hello, friend Hello, Asha
42
square_def <lambda>
[True, False, True, False, True]
positive non-positive
```

Line by line:

- The `def` and the `lambda` do the same work. The lambda has no `return` and no name of its own (its `__name__` is `<lambda>`).
- A lambda can be called immediately by wrapping it in brackets: `(lambda x: x + 1)(10)`.
- Lambdas accept several parameters and default values, and the right-hand part must be a single expression. The conditional expression `a if test else b` is allowed because it is an expression.

**6. Example 2 — Practical**

```python
students = [("Asha", 82), ("Ravi", 67), ("Meena", 91), ("Kiran", 67)]

print(sorted(students, key=lambda s: s[1]))
print(sorted(students, key=lambda s: s[1], reverse=True))
print(sorted(students, key=lambda s: (-s[1], s[0])))
print(max(students, key=lambda s: s[1]), min(students, key=lambda s: s[1]))

words = ["banana", "Apple", "cherry", "fig"]
print(sorted(words, key=lambda w: w.lower()))
print(sorted(words, key=lambda w: (len(w), w)))

records = [{"name": "Asha", "age": 30}, {"name": "Ravi", "age": 25}]
print(sorted(records, key=lambda r: r["age"]))
print(max(records, key=lambda r: r["age"])["name"])

prices = {"tea": 20, "coffee": 35, "milk": 25}
print(sorted(prices.items(), key=lambda pair: pair[1]))
print(sorted(prices, key=lambda name: prices[name], reverse=True))

operations = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: a - b,
    "pow": lambda a, b: a ** b,
}
print(operations["add"](5, 3), operations["pow"](2, 5))

def apply_to(items, function):
    return [function(item) for item in items]


print(apply_to([1, 2, 3], lambda n: n * 10))
print(apply_to(["a", "b"], lambda s: s + s))

def make_power(exponent):
    return lambda base: base ** exponent


cube = make_power(3)
print(cube(2), make_power(2)(9))
```

Output:

```text
[('Ravi', 67), ('Kiran', 67), ('Asha', 82), ('Meena', 91)]
[('Meena', 91), ('Asha', 82), ('Ravi', 67), ('Kiran', 67)]
[('Meena', 91), ('Asha', 82), ('Kiran', 67), ('Ravi', 67)]
('Meena', 91) ('Ravi', 67)
['Apple', 'banana', 'cherry', 'fig']
['fig', 'Apple', 'banana', 'cherry']
[{'name': 'Ravi', 'age': 25}, {'name': 'Asha', 'age': 30}]
Asha
[('tea', 20), ('milk', 25), ('coffee', 35)]
['coffee', 'milk', 'tea']
8 32
[10, 20, 30]
['aa', 'bb']
8 81
```

Line by line:

- Sorting records by one field is the most common use: the lambda picks the field. A tuple key (`(-s[1], s[0])`) sorts by score descending, then by name; the negative sign reverses numbers only.
- `max` and `min` accept the same `key`. When several items tie (two students with 67), the first one found is returned by `min`.
- `key=lambda w: w.lower()` sorts ignoring case; `(len(w), w)` sorts by length, then alphabetically.
- Dictionaries of records are sorted by a field with `r["age"]`. Sorting `prices.items()` by `pair[1]` sorts by value; sorting the keys by `prices[name]` does the same, giving only names.
- A dictionary of lambdas is a compact dispatch table.
- `make_power` returns a lambda that remembers `exponent`, a closure.

**7. Example 3 — Edge case or common mistake**

Lambdas cannot hold statements. These are shown as text because they are not valid Python:

```text
f = lambda x: return x * 2
g = lambda x: y = x * 2
h = lambda x: print(x); x
```

```text
SyntaxError: invalid syntax
```

Use `def` for anything that needs a statement. Note that a *call* such as `print(x)` is an expression, so `lambda x: print(x)` is allowed (and returns `None`):

```python
show = lambda x: print("value:", x)
result = show(5)
print(result)
```

Output:

```text
value: 5
None
```

The late-binding trap again:

```python
adders = [lambda x: x + i for i in range(3)]
print([f(10) for f in adders])

fixed = [lambda x, i=i: x + i for i in range(3)]
print([f(10) for f in fixed])
```

Output:

```text
[12, 12, 12]
[10, 11, 12]
```

All three lambdas read the same `i`, which is 2 when they are called. The default `i=i` is evaluated when each lambda is created, so each keeps its own value.

A lambda is no shorter than a `def` when you give it a name, and tracebacks show `<lambda>`:

```python
square = lambda x: x * x
try:
    square("a")
except TypeError as error:
    print("TypeError:", error)
print(square.__name__)


def square_named(x):
    return x * x


print(square_named.__name__)
```

Output:

```text
TypeError: can't multiply sequence by non-int of type 'str'
<lambda>
square_named
```

An unreadable lambda is worse than a small named function:

```python
data = [3, 8, 1, 9]
hard = sorted(data, key=lambda n: (n % 2, -n if n % 2 else n))
print(hard)


def odd_first_then_by_size(n):
    """Even numbers first, small to large; then odd numbers, large to small."""
    if n % 2:
        return (1, -n)
    return (0, n)


print(sorted(data, key=odd_first_then_by_size))
```

Output:

```text
[8, 9, 3, 1]
[8, 9, 3, 1]
```

Both do the same, but the named function has a docstring and can be read, tested and reused.

**8. Common mistakes**

- Trying to put statements (assignment, `return`, loops) in a lambda.
- Assigning a lambda to a name instead of writing a `def`.
- Writing long or nested lambdas that nobody can read.
- Capturing a loop variable and getting only its last value.
- Forgetting the colon, or writing `lambda x, y: (x, y)` when two separate values were wanted.
- Using `key=lambda x: x` when no key is needed at all.
- Sorting by a key that returns mixed types, which cannot be compared.

**9. Real-world and AI applications**

Lambdas are used all day in data code: sorting a list of search results by score (`sorted(results, key=lambda r: r["score"], reverse=True)`), picking the best candidate (`max(candidates, key=lambda c: c.confidence)`), grouping records, and applying a small transformation to every row of a table (data libraries accept lambdas for such steps). In AI pipelines you will often see a lambda as a small adapter: a function that extracts the text of a message, scores a document, or filters out low-quality examples.

**10. Practice**

1. Write a lambda that returns the cube of a number and call it with 3.
2. Write a lambda that takes two numbers and returns the larger one, without `max`.
3. Sort `["banana", "kiwi", "apple", "fig"]` by length with a lambda key, and then by last letter.
4. Sort `[{"name": "A", "score": 7}, {"name": "B", "score": 9}]` by score descending.
5. From `[("x", 3), ("y", 1), ("z", 2)]`, get the pair with the smallest second item using `min` and a lambda.
6. Build a dictionary of lambdas for `"square"`, `"cube"` and `"half"`, and apply each to 8.
7. Fix: `functions = [lambda: n for n in range(3)]`, so that calling them gives `0, 1, 2`.
8. Rewrite `lambda s: s.strip().lower()` as a `def` with a docstring. Which is better, and why?

**11. Interview questions**

- *What is a lambda function?* A small anonymous function written as a single expression, `lambda args: expression`.
- *What are its limits?* Only one expression, no statements, and no name or docstring of its own.
- *Where do you use lambdas?* As short function arguments, especially sort keys, and in `map`, `filter` and `reduce`.
- *Is `f = lambda x: x * 2` better than a `def`?* No; a `def` gives a proper name and docstring and is easier to debug.
- *What is the late-binding problem?* Lambdas created in a loop all use the variable's final value unless it is captured with a default argument.

**12. Quick revision**

- `lambda parameters: expression`; the value is returned automatically.
- One expression only; no statements; the name is `<lambda>`.
- Best for `key=` in `sorted`, `min`, `max`, and for `map`/`filter`/`reduce`.
- Use `def` when the logic is more than a simple expression or you need a name.
- Capture loop variables with `i=i`.

---

## Answers to Practice Exercises

### Answers: Functions as First-Class Citizens

1.

```python
count = len
print(count("hello"), count([1, 2, 3]), count is len)
```

Output:

```text
5 3 True
```

2.

```python
def apply_to_all(function, items):
    return [function(item) for item in items]


def square(n):
    return n * n


print(apply_to_all(str.upper, ["a", "b"]))
print(apply_to_all(square, [1, 2, 3]))
```

Output:

```text
['A', 'B']
[1, 4, 9]
```

3.

```python
def upper(text):
    return text.upper()


def lower(text):
    return text.lower()


def title(text):
    return text.title()


actions = {"upper": upper, "lower": lower, "title": title}
choice = "title"
print(actions[choice]("learning python"))
```

Output:

```text
Learning Python
```

4.

```python
def make_multiplier(factor):
    def multiply(value):
        return value * factor
    return multiply


double = make_multiplier(2)
triple = make_multiplier(3)
print(double(7), triple(7))
```

Output:

```text
14 21
```

5.

```python
def compose(f, g):
    def combined(value):
        return g(f(value))
    return combined


clean_title = compose(str.strip, str.title)
print(repr(clean_title("  hello world  ")))
```

Output:

```text
'Hello World'
```

6.

```python
def length(word):
    return len(word)


print(sorted(["pear", "fig", "banana"], key=length))
print(sorted(["pear", "fig", "banana"], key=len))
```

Output:

```text
['fig', 'pear', 'banana']
['fig', 'pear', 'banana']
```

7. `len()` calls `len` with no argument right away, which raises a `TypeError` before `sorted` is even called. You want the function itself: `key=len`.

```python
try:
    sorted(["a", "bb"], key=len())
except TypeError as error:
    print("TypeError:", error)
```

Output:

```text
TypeError: len() takes exactly one argument (0 given)
```

### Answers: Lambda Functions

1.

```python
cube = lambda n: n ** 3
print(cube(3))
```

Output:

```text
27
```

2.

```python
bigger = lambda a, b: a if a > b else b
print(bigger(4, 9), bigger(7, 2), bigger(5, 5))
```

Output:

```text
9 7 5
```

3.

```python
words = ["banana", "kiwi", "apple", "fig"]
print(sorted(words, key=lambda w: len(w)))
print(sorted(words, key=lambda w: w[-1]))
```

Output:

```text
['fig', 'kiwi', 'apple', 'banana']
['banana', 'apple', 'fig', 'kiwi']
```

Ties keep their original order, because Python's sort is stable.

4.

```python
items = [{"name": "A", "score": 7}, {"name": "B", "score": 9}]
print(sorted(items, key=lambda item: item["score"], reverse=True))
```

Output:

```text
[{'name': 'B', 'score': 9}, {'name': 'A', 'score': 7}]
```

5.

```python
pairs = [("x", 3), ("y", 1), ("z", 2)]
print(min(pairs, key=lambda pair: pair[1]))
```

Output:

```text
('y', 1)
```

6.

```python
actions = {
    "square": lambda n: n * n,
    "cube": lambda n: n ** 3,
    "half": lambda n: n / 2,
}
for name, function in actions.items():
    print(name, function(8))
```

Output:

```text
square 64
cube 512
half 4.0
```

7. Each lambda reads the same `n`. Capture the value with a default parameter:

```python
broken = [lambda: n for n in range(3)]
print([f() for f in broken])

fixed = [lambda n=n: n for n in range(3)]
print([f() for f in fixed])
```

Output:

```text
[2, 2, 2]
[0, 1, 2]
```

8.

```python
def clean(s):
    """Return the text without surrounding spaces, in lower case."""
    return s.strip().lower()


print(repr(clean("  HeLLo ")), clean.__name__)
```

Output:

```text
'hello' clean
```

The `def` is better when the function is used in several places or deserves a name and a docstring. The lambda is fine for a one-off argument such as a sort key.

---

## Chapter Summary and Key Takeaways

- Functions are objects: they can be assigned, stored in lists and dictionaries, passed as arguments and returned, which makes higher-order functions, callbacks, closures and dispatch tables possible.
- `f` is the function object and `f()` is a call; pass the name (no parentheses) when a function is expected, such as `key=len`.
- `lambda parameters: expression` is an anonymous one-expression function, ideal for `key=` arguments and other short, one-off uses; it cannot contain statements.
- Prefer a `def` for anything that needs a name, a docstring, several steps, or reuse, and avoid assigning lambdas to names.
- Lambdas and closures capture variables, not values, so loop-created lambdas need a default argument (`i=i`) to keep each round's value.

Next: [Chapter 29 — map(), filter() and reduce()](29-map-filter-reduce.md) uses these ideas to transform, select and combine items.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
