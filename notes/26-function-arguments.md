# Chapter 26 — Function Arguments

> Part 5 — Functions and Functional Programming · Video: 9:10:11–9:40:20 · Previous: [25 Defining Functions and Return Values](25-defining-functions-and-return-values.md) · Next: [27 Variable Scope](27-variable-scope.md)

**In this chapter:** the ways of passing information into a function: positional arguments (matched by order), keyword arguments (matched by name), default values, a variable number of positional arguments with `*args`, and a variable number of named arguments with `**kwargs`; plus the rules for combining them, unpacking with `*` and `**` in a call, and the mutable-default trap.

**Before you start:** you need functions and `return` from [Defining Your Own Function](25-defining-functions-and-return-values.md#defining-your-own-function), tuples from [Tuples](21-tuples.md#tuples) and dictionaries from [Dictionaries](23-dictionaries.md#dictionaries). Recap: a parameter is the name in the `def` line, an argument is the value in the call; a tuple is an immutable ordered group; a dictionary maps keys to values. Examples were run with Python 3.13.

---

## Positional Arguments

**Timestamp:** [9:10:11](https://www.youtube.com/watch?v=J9BI0jGOds8&t=33011s)

**Learning objectives:**

- Explain that positional arguments are matched to parameters by their order.
- Call a function with keyword arguments in any order, and mix the two styles correctly.
- Diagnose `TypeError`s caused by too few, too many or duplicated arguments.
- Use `*` and `**` to unpack a list or dictionary in a call.

**1. Intuition**

Ordering a coffee at a counter: "a large, oat milk, no sugar" works if you and the barista agree on the order of the questions (size, milk, sugar). Positional arguments work the same way: the first value goes to the first parameter, the second to the second. If you say it in the wrong order, you get oat-sized sugar. Naming each choice ("milk: oat, size: large") removes the dependence on order. That is a *keyword argument*.

**2. Why does it exist?**

A function needs inputs, and the caller must say which value is meant for which parameter. Position is the shortest way: `power(2, 3)`. Names are clearer when there are many parameters or when the meaning of a bare value is not obvious: `connect(host="db", timeout=5)` is easier to read than `connect("db", 5)`.

**3. Technical explanation**

- *Positional arguments*: matched to parameters left to right. The number of positional arguments must match the number of parameters, unless the parameters have defaults.
- *Keyword arguments*: written `name=value` in the call and matched by *name*, in any order.
- *Mixing*: in a call, all positional arguments must come before any keyword argument. Passing a value both by position and by name is an error (`multiple values for argument`).
- *Errors*: too few arguments (`missing required positional argument`), too many (`takes N positional arguments but M were given`), unknown keyword (`unexpected keyword argument`).
- *Unpacking in a call*: `f(*sequence)` spreads a list or tuple into positional arguments; `f(**mapping)` spreads a dictionary into keyword arguments.
- *Positional-only and keyword-only parameters*: a `/` in the parameter list makes the parameters before it positional-only; a `*` makes the parameters after it keyword-only (for example `def f(a, /, b, *, c)`). Many built-in functions use these forms (for example, `print(*values, sep=" ", end="\n")` accepts `sep` and `end` only by name).
- Arguments are passed by *assignment* of names to objects, so a mutable argument can be changed inside the function (see [Mutable versus Immutable Objects](24-mutability-iteration-and-pitfalls.md#mutable-versus-immutable-objects)).

**4. Syntax**

```text
def describe(name, age, city):
    ...

describe("Asha", 21, "Chennai")                  # positional
describe(city="Chennai", name="Asha", age=21)    # keyword
describe("Asha", city="Chennai", age=21)         # mixed: positional first
describe(*["Asha", 21, "Chennai"])               # unpack a sequence
describe(**{"name": "Asha", "age": 21, "city": "Chennai"})   # unpack a dictionary
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
def describe(name, age, city):
    return f"{name}, {age}, from {city}"


print(describe("Asha", 21, "Chennai"))
print(describe(21, "Asha", "Chennai"))
print(describe(city="Pune", name="Ravi", age=22))
print(describe("Meena", city="Kochi", age=23))

details = ["Kiran", 24, "Delhi"]
print(describe(*details))
info = {"name": "Sana", "age": 25, "city": "Goa"}
print(describe(**info))

def subtract(a, b):
    return a - b


print(subtract(10, 3), subtract(3, 10), subtract(b=3, a=10))
```

Output:

```text
Asha, 21, from Chennai
21, Asha, from Chennai
Ravi, 22, from Pune
Meena, 23, from Kochi
Kiran, 24, from Delhi
Sana, 25, from Goa
7 -7 7
```

Line by line:

- The first call matches by order. The second swaps the first two values and gives a nonsense sentence without any error: position matters, and Python cannot check meaning.
- Keyword arguments can be in any order. A mixed call puts the positional value first.
- `*details` spreads a list into three positional arguments; `**info` spreads a dictionary into keyword arguments whose names must match the parameters.
- `subtract` shows that order changes the result for positional arguments, while keywords make the intent explicit.

**6. Example 2 — Practical**

```python
def bmi(weight_kg, height_m):
    return round(weight_kg / height_m ** 2, 1)


print(bmi(70, 1.75))
print(bmi(height_m=1.75, weight_kg=70))


def make_email(first, last, domain):
    return f"{first}.{last}@{domain}".lower()


people = [("Asha", "Nair", "example.org"), ("Ravi", "Iyer", "example.org")]
print([make_email(*person) for person in people])


def format_price(amount, /, currency="INR", *, decimals=2):
    return f"{currency} {amount:.{decimals}f}"


print(format_price(1234.5))
print(format_price(1234.5, "USD", decimals=0))
print(format_price(99, currency="EUR"))


def draw_box(width, height, char="#"):
    for _ in range(height):
        print(char * width)


draw_box(4, 2)
draw_box(char="*", width=3, height=1)

print("a", "b", "c", sep="-", end="!\n")
```

Output:

```text
22.9
22.9
['asha.nair@example.org', 'ravi.iyer@example.org']
INR 1234.50
USD 1234
EUR 99.00
####
####
***
a-b-c!
```

Line by line:

- `bmi` can be called by position or by name; the named call is self-documenting. (`height_m ** 2` is evaluated before the division.)
- `make_email(*person)` unpacks each tuple of a list into three arguments.
- `format_price` has a positional-only parameter (`amount`, before the `/`), a normal one with a default (`currency`), and a keyword-only one after the `*` (`decimals`). `decimals` must be named in a call. The nested `{amount:.{decimals}f}` takes the number of decimals from a variable (see [String Formatting and f-Strings](09-string-formatting-and-f-strings.md)).
- `draw_box` mixes positional and keyword arguments.
- `print` itself takes `sep` and `end` by name only, which is why they are written as `sep="-"`.

**7. Example 3 — Edge case or common mistake**

```python
def describe(name, age, city):
    return f"{name}, {age}, from {city}"


calls = [
    lambda: describe("Asha", 21),
    lambda: describe("Asha", 21, "Pune", "extra"),
    lambda: describe("Asha", 21, city="Pune", name="Again"),
    lambda: describe("Asha", 21, town="Pune"),
    lambda: describe(*["Asha", 21]),
    lambda: describe(**{"name": "Asha", "age": 21}),
]
for call in calls:
    try:
        call()
    except TypeError as error:
        print("TypeError:", error)
```

Output:

```text
TypeError: describe() missing 1 required positional argument: 'city'
TypeError: describe() takes 3 positional arguments but 4 were given
TypeError: describe() got multiple values for argument 'name'
TypeError: describe() got an unexpected keyword argument 'town'
TypeError: describe() missing 1 required positional argument: 'city'
TypeError: describe() missing 1 required positional argument: 'city'
```

Each message names the problem: a missing argument, too many arguments, a value given twice, an unknown keyword.

Positional before keyword, and the syntax error when the order is reversed (shown as text):

```text
describe(name="Asha", 21, "Pune")
```

```text
  File "example.py", line 1
    describe(name="Asha", 21, "Pune")
                                    ^
SyntaxError: positional argument follows keyword argument
```

Positional-only and keyword-only rules are enforced:

```python
def f(a, /, b, *, c):
    return a, b, c


print(f(1, 2, c=3))
print(f(1, b=2, c=3))
for call in [lambda: f(a=1, b=2, c=3), lambda: f(1, 2, 3)]:
    try:
        call()
    except TypeError as error:
        print("TypeError:", error)
```

Output:

```text
(1, 2, 3)
(1, 2, 3)
TypeError: f() got some positional-only arguments passed as keyword arguments: 'a'
TypeError: f() takes 2 positional arguments but 3 were given
```

Arguments that are mutable objects can be changed by the function:

```python
def add_tag(tags, tag):
    tags.append(tag)


my_tags = ["a"]
add_tag(my_tags, "b")
print(my_tags)
```

Output:

```text
['a', 'b']
```

**8. Common mistakes**

- Passing arguments in the wrong order (no error, but a wrong result).
- Passing too few or too many arguments.
- Giving the same parameter both by position and by name.
- Putting a keyword argument before a positional one.
- Misspelling a keyword name.
- Forgetting the `*` or `**` when unpacking a list or dictionary.
- Changing a mutable argument without meaning to.

**9. Real-world and AI applications**

Calls to AI libraries are mostly keyword arguments: `model="...", messages=[...], temperature=0.2, max_tokens=300`. Names make long calls readable and let the library add new options without breaking old code. Dictionaries of settings are often passed with `**settings`, so the same configuration can drive many calls (see [Keyword Arguments (**kwargs)](26-function-arguments.md#keyword-arguments-kwargs) below).

**10. Practice**

1. Write `rectangle_area(width, height)` and call it by position, by keyword and mixed.
2. Call `divide(a, b)` with `a=10, b=2` and with the values swapped; explain the difference.
3. Write `introduce(name, age)` and call it using a list `["Asha", 21]` with `*`, and a dictionary with `**`.
4. Predict the error: `introduce("Asha")`, `introduce("Asha", 21, 5)`, `introduce("Asha", age=21, name="B")`.
5. Write `join_words(first, second, *, sep)` where `sep` must be given by name.
6. Why does `print("a", "b", sep="-")` need the name `sep`?

**11. Interview questions**

- *What is the difference between positional and keyword arguments?* Positional arguments are matched by order; keyword arguments by parameter name.
- *In what order must they appear in a call?* Positional first, then keyword.
- *What do `*` and `**` do in a call?* They unpack a sequence into positional arguments and a dictionary into keyword arguments.
- *What are keyword-only parameters?* Parameters after a bare `*` in the definition; they must be passed by name.

**12. Quick revision**

- Positional: by order. Keyword: `name=value`, any order. Positional come first.
- A value cannot be given twice; unknown names are errors.
- `f(*seq)` and `f(**mapping)` unpack in a call.
- `/` marks positional-only, `*` marks keyword-only parameters.
- Mutable arguments can be changed inside the function.

---

## Default Arguments

**Timestamp:** [9:13:32](https://www.youtube.com/watch?v=J9BI0jGOds8&t=33212s)

**Learning objectives:**

- Give a parameter a default value and call the function with or without it.
- Place defaulted parameters after required ones.
- Explain when default values are evaluated, and avoid the mutable default trap.
- Use `None` as a safe "not given" default.

**1. Intuition**

A form with pre-filled fields: the country already says "India", the language already says "English". Most people leave them alone; those who want something different overwrite them. A default argument is a pre-filled field.

**2. Why does it exist?**

Many functions have a sensible usual value for some of their inputs. Without defaults, every call would have to repeat it, and adding a new option later would break every existing call. Defaults keep common calls short and allow options to be added safely.

**3. Technical explanation**

- Write `def f(a, b=10):`. If the caller omits `b`, it is 10; if the caller supplies it, the supplied value is used.
- Parameters with defaults must come *after* parameters without defaults (`def f(a=1, b)` is a `SyntaxError`).
- Default values are evaluated *once*, when the `def` statement runs, not at each call. For immutable defaults (numbers, strings, `None`, tuples) this does not matter. For a *mutable* default (a list, dictionary or set), the same object is shared by all calls that omit the argument, so changes accumulate from call to call.
- The safe pattern is `def f(items=None):` followed by `if items is None: items = []`.
- Use `None` as the default when "not provided" needs to be different from every real value. (Use `is None`, because `0` and `""` are real values that are falsy.)
- The defaults are stored on the function: `f.__defaults__`.
- A default may refer to a constant, but it is not recomputed: `def f(time=time.time())` would freeze the time at definition.

**4. Syntax**

```text
def function(required, optional="default", another=0):
    ...

function("x")
function("x", "y")
function("x", another=5)
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"


print(greet("Asha"))
print(greet("Asha", "Namaste"))
print(greet("Asha", greeting="Welcome"))
print(greet(greeting="Hi", name="Ravi"))


def power(base, exponent=2):
    return base ** exponent


print(power(5), power(5, 3), power(2, exponent=10))
print(greet.__defaults__, power.__defaults__)
```

Output:

```text
Hello, Asha!
Namaste, Asha!
Welcome, Asha!
Hi, Ravi!
25 125 1024
('Hello',) (2,)
```

Line by line:

- `greet("Asha")` uses the default greeting. The greeting can be replaced by position or by name.
- `power` squares by default and raises to any power when asked.
- `__defaults__` shows the stored default values as a tuple.

**6. Example 2 — Practical**

```python
def make_tax_invoice(amount, tax_rate=0.18, currency="INR", round_to=2):
    total = amount * (1 + tax_rate)
    return f"{currency} {total:.{round_to}f}"


print(make_tax_invoice(1000))
print(make_tax_invoice(1000, 0.05))
print(make_tax_invoice(1000, currency="USD", round_to=0))


def read_lines(text, strip=True, skip_empty=True):
    lines = text.split("\n")
    if strip:
        lines = [line.strip() for line in lines]
    if skip_empty:
        lines = [line for line in lines if line]
    return lines


raw = " a \n\n b\n"
print(read_lines(raw))
print(read_lines(raw, skip_empty=False))
print(read_lines(raw, strip=False))


def add_student(name, scores=None):
    if scores is None:
        scores = []
    scores.append(0)
    return {"name": name, "scores": scores}


print(add_student("Asha"))
print(add_student("Ravi"))
shared = [90]
print(add_student("Meena", shared), shared)


def search(items, wanted, limit=None):
    found = [item for item in items if wanted in item]
    return found if limit is None else found[:limit]


words = ["apple", "grape", "pineapple", "banana"]
print(search(words, "apple"), search(words, "a", limit=2), search(words, "z"))
```

Output:

```text
INR 1180.00
INR 1050.00
USD 1180
['a', 'b']
['a', '', 'b', '']
[' a ', ' b']
{'name': 'Asha', 'scores': [0]}
{'name': 'Ravi', 'scores': [0]}
{'name': 'Meena', 'scores': [90, 0]} [90, 0]
['apple', 'pineapple'] ['apple', 'grape'] []
```

Line by line:

- `make_tax_invoice` has several options; a typical call supplies only the amount, and unusual ones are chosen by name, so the caller does not need to remember the order of the optional parameters.
- `read_lines` uses `True`/`False` flags as options. Keyword arguments (`skip_empty=False`) make such calls readable.
- `add_student` uses `None` and creates a fresh list for each call. When the caller passes a list, that list is used (and changed), as the last line shows with `shared`.
- `search` uses `None` to mean "no limit", since `0` could be a real limit.

**7. Example 3 — Edge case or common mistake**

The mutable default trap:

```python
def add_item(item, basket=[]):
    basket.append(item)
    return basket


print(add_item("tea"))
print(add_item("milk"))
print(add_item("rice", ["own"]))
print(add_item("salt"))
print(add_item.__defaults__)
```

Output:

```text
['tea']
['tea', 'milk']
['own', 'rice']
['tea', 'milk', 'salt']
(['tea', 'milk', 'salt'],)
```

The default list is created once and kept on the function, so `"tea"`, `"milk"` and `"salt"` all end up in the same list, and the output of a call depends on earlier calls. The safe version:

```python
def add_item_safe(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket


print(add_item_safe("tea"))
print(add_item_safe("milk"))
```

Output:

```text
['tea']
['milk']
```

A default is computed once, at definition time:

```python
import itertools

counter = itertools.count(1)


def stamp(label, number=next(counter)):
    return f"{label}-{number}"


print(stamp("a"), stamp("b"), stamp("c", 99))
```

Output:

```text
a-1 b-1 c-99
```

`next(counter)` ran once, when the function was defined, so every call without a number gets the same value (1). If you want a fresh value for each call, use `None` and compute it inside.

Defaults must follow required parameters (shown as text, because it is a syntax error):

```text
def f(a=1, b):
    return a + b
```

```text
  File "example.py", line 1
    def f(a=1, b):
               ^
SyntaxError: parameter without a default follows parameter with a default
```

Finally, `None` versus falsy values:

```python
def greet(name, greeting=None):
    greeting = greeting or "Hello"
    return f"{greeting}, {name}"


print(greet("Asha"), "|", greet("Asha", ""), "|", greet("Asha", "Hi"))


def greet2(name, greeting=None):
    if greeting is None:
        greeting = "Hello"
    return f"{greeting}, {name}"


print(greet2("Asha"), "|", greet2("Asha", ""), "|", greet2("Asha", "Hi"))
```

Output:

```text
Hello, Asha | Hello, Asha | Hi, Asha
Hello, Asha | , Asha | Hi, Asha
```

`greeting or "Hello"` treats an empty string as "not given", so a deliberately empty greeting is replaced. `is None` tests only for "not given".

**8. Common mistakes**

- Using `[]`, `{}` or `set()` as a default value.
- Placing a parameter with a default before one without.
- Expecting a default to be recomputed on every call.
- Using `or` to supply a default when `0`, `""` or `[]` are valid values.
- Having so many optional parameters that calls become unreadable (group them or use keywords).
- Changing the default's meaning later in a way that breaks existing callers.

**9. Real-world and AI applications**

AI library functions are full of defaults: `temperature=1.0`, `max_tokens=None`, `top_p=1.0`. You call them with just the required inputs and override the options you care about. In your own wrapper functions, defaults such as `model="default-model"`, `temperature=0.2` and `retries=3` give every caller a safe baseline (see [Temperature](31-llms-prompting-temperature-hallucination.md#temperature)). The mutable default bug is a real danger in chat functions with a `history=[]` parameter, where every user would share one conversation.

**10. Practice**

1. Write `greet(name, greeting="Hello")` and call it three ways.
2. Write `area(length, width=None)` that returns the area of a rectangle, or of a square if only `length` is given.
3. Write `repeat(text, times=2, separator=" ")` and call it with different combinations.
4. Fix `def add(x, items=[]): items.append(x); return items` so that each call without a list starts fresh.
5. Why is `def f(a=1, b):` an error?
6. What is wrong with `def log(message, when=time.time()):`? Fix it.
7. Explain the difference between `greeting = greeting or "Hello"` and `if greeting is None:` when the caller passes an empty string.

**11. Interview questions**

- *When are default values evaluated?* Once, when the function is defined.
- *What is the mutable default argument problem?* A mutable default is shared across calls, so changes accumulate; use `None` and create the object inside.
- *Can a non-default parameter follow a default one?* No (unless keyword-only, after a `*`).
- *Why use `is None` instead of a truthiness test?* To distinguish "not provided" from legitimate falsy values such as 0 or an empty string.

**12. Quick revision**

- `def f(a, b=default):`; defaults come after required parameters.
- Evaluated once at definition time.
- Never use a mutable object as a default; use `None`.
- Test with `is None`.
- Override defaults by position or, better, by keyword.

---

## Variable-Length Arguments (*args)

**Timestamp:** [9:28:51](https://www.youtube.com/watch?v=J9BI0jGOds8&t=34131s)

**Learning objectives:**

- Write a function that accepts any number of positional arguments with `*args`.
- Explain that `args` is a tuple and the star only collects the extra positional values.
- Combine `*args` with normal parameters, and with keyword-only parameters.
- Pass a list into `*args` using `*` unpacking.

**1. Intuition**

A shopping bag with no fixed size: whatever you put in goes in. A function like `sum_all` should work for two numbers, five numbers or fifty, without a separate version for each. `*args` is the bag that collects all the extra values into one tuple.

**2. Why does it exist?**

Some operations are naturally "any number of things": add these numbers, join these words, print these values. Making the caller wrap them in a list is clumsy; fixed parameters cannot cover every case. `*args` lets the function accept as many positional arguments as the caller gives.

**3. Technical explanation**

- In a definition, `*args` collects all extra positional arguments into a *tuple* named `args`. The name `args` is only a convention; the star is what matters (`*numbers` is fine and often clearer).
- With no extra arguments, `args` is an empty tuple `()`.
- Normal parameters before `*args` take their values first; `*args` gets the rest. Parameters *after* `*args` become keyword-only.
- Only one `*args` is allowed in a definition.
- In a *call*, `f(*items)` does the opposite: it spreads a sequence into separate positional arguments.
- Built-in examples: `print(*values)`, `max(1, 5, 3)`, `min(...)`.

**4. Syntax**

```text
def total(*numbers):
    return sum(numbers)

def label(first, *others, sep="-"):
    ...

total(1, 2, 3)
total(*[1, 2, 3])
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
def total(*numbers):
    print("received:", numbers, type(numbers).__name__)
    return sum(numbers)


print(total())
print(total(5))
print(total(1, 2, 3, 4))

values = [10, 20, 30]
print(total(*values))
```

Output:

```text
received: () tuple
0
received: (5,) tuple
5
received: (1, 2, 3, 4) tuple
10
received: (10, 20, 30) tuple
60
```

Line by line:

- `numbers` is a tuple of whatever positional arguments were passed: empty for no arguments, one item for one.
- `total(*values)` spreads the list into three arguments, so the sum is 60.
- Without the star, `total(values)` would pass the list as *one* argument, so `numbers` would be a tuple holding one list (Example 3 shows what goes wrong). The star in the call matters.

**6. Example 2 — Practical**

```python
def average(*numbers):
    if not numbers:
        return None
    return sum(numbers) / len(numbers)


print(average(4, 8, 15), average(10), average())


def join_words(first, *rest, sep=" "):
    return sep.join((first,) + rest)


print(join_words("only"))
print(join_words("a", "b", "c"))
print(join_words("a", "b", "c", sep="-"))


def log(level, *messages):
    print(f"[{level}]", *messages)


log("INFO", "started", "ok")
log("WARN", "disk", 91, "percent")


def biggest(first, *others):
    result = first
    for other in others:
        if other > result:
            result = other
    return result


print(biggest(3, 9, 4), biggest(7))


def apply_all(function, *values):
    return [function(value) for value in values]


print(apply_all(str.upper, "a", "b"))
print(apply_all(abs, -1, 2, -3))

first, *middle, last = "python"
print(first, middle, last)
```

Output:

```text
9.0 10.0 None
only
a b c
a-b-c
[INFO] started ok
[WARN] disk 91 percent
9 7
['A', 'B']
[1, 2, 3]
p ['y', 't', 'h', 'o'] n
```

Line by line:

- `average` accepts any count of numbers and handles "none" explicitly.
- `join_words` needs at least one value (`first`), collects the rest in `rest`, and `sep` is keyword-only, since it comes after `*rest`. `(first,) + rest` builds a tuple of everything (the comma makes `(first,)` a one-item tuple).
- `log` forwards its extra values to `print` with `*messages`, using star in a call.
- `biggest` shows the pattern "one required value plus any number of others", which prevents calling it with nothing at all.
- `apply_all` takes a function and any number of values; it applies the function to each (functions as values are covered in [Functions as First-Class Citizens](28-first-class-functions-and-lambda.md#functions-as-first-class-citizens)).
- The last line is the same star idea in an assignment (see [Tuples](21-tuples.md#tuples)).

**7. Example 3 — Edge case or common mistake**

```python
def total(*numbers):
    return sum(numbers)


print(total([1, 2, 3]))
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 5, in <module>
    print(total([1, 2, 3]))
          ~~~~~^^^^^^^^^^^
  File "example.py", line 2, in total
    return sum(numbers)
TypeError: unsupported operand type(s) for +: 'int' and 'list'
```

Passing one list gives a tuple containing a list, and `sum` cannot add a list to 0. Use `total(*[1, 2, 3])`.

*args cannot be set by keyword, and parameters after it must be named:

```python
def f(a, *args, key=0):
    return a, args, key


print(f(1, 2, 3))
print(f(1, 2, 3, key=9))
for call in [lambda: f(), lambda: f(args=(1, 2)), lambda: f(1, 2, 3, 4, key=1, other=2)]:
    try:
        call()
    except TypeError as error:
        print("TypeError:", error)
```

Output:

```text
(1, (2, 3), 0)
(1, (2, 3), 9)
TypeError: f() missing 1 required positional argument: 'a'
TypeError: f() got an unexpected keyword argument 'args'
TypeError: f() got an unexpected keyword argument 'other'
```

A value after `*args` is never taken as `key`: `f(1, 2, 3, 9)` puts the 9 into `args`. Also, `args` is a tuple, so it cannot be changed:

```python
def show(*items):
    try:
        items[0] = "changed"
    except TypeError as error:
        print("TypeError:", error)
    items_list = list(items)
    items_list[0] = "changed"
    return items_list


print(show("a", "b"))
```

Output:

```text
TypeError: 'tuple' object does not support item assignment
['changed', 'b']
```

Misusing the star in the middle of ordinary parameters (shown as text):

```text
def f(*args, *more):
    pass
```

```text
  File "example.py", line 1
    def f(*args, *more):
                 ^
SyntaxError: * argument may appear only once
```

**8. Common mistakes**

- Passing a list without the `*` and getting a tuple holding the list.
- Forgetting that `args` is a tuple (immutable).
- Expecting a value after `*args` to be taken as a normal parameter (it must be passed by name).
- Using `*args` when a normal list parameter would be clearer.
- Using more than one `*args` in a definition.
- Not handling the case of no extra arguments.

**9. Real-world and AI applications**

`*args` is used where the number of inputs varies: `print`, `max`, `min`, string-joining helpers, logging functions that accept several messages, and wrappers that pass everything along to another function (`def wrapper(*args): return real_function(*args)`). In AI code, a helper such as `build_prompt(*parts)` that joins any number of text parts, or a function that merges several lists of documents, uses this pattern.

**10. Practice**

1. Write `multiply(*numbers)` returning the product of any number of values (1 for none).
2. Write `longest(*words)` returning the longest word, or `""` for none.
3. Write `print_all(label, *items)` that prints the label and then each item on its own line.
4. Call `multiply` with a list `[2, 3, 4]` correctly.
5. Write `join_with(sep, *parts)` and use it as `join_with("-", "a", "b", "c")`.
6. What type is `args`, and what does that mean for changing it?
7. Why is `def f(*args, x)` called with `f(1, 2, 3)` a `TypeError`?

**11. Interview questions**

- *What does `*args` do in a function definition?* Collects extra positional arguments into a tuple.
- *What does `*` do in a function call?* Unpacks a sequence into separate positional arguments.
- *Is the name `args` required?* No, the star is what matters, but `args` is the convention.
- *What happens to parameters defined after `*args`?* They become keyword-only.

**12. Quick revision**

- `def f(*args)`: `args` is a tuple of the extra positional arguments.
- Normal parameters come first; those after `*args` are keyword-only.
- `f(*sequence)` unpacks in a call.
- Without the star in the call, a list is one single argument.
- Handle the empty case.

---

## Keyword Arguments (**kwargs)

**Timestamp:** [9:33:05](https://www.youtube.com/watch?v=J9BI0jGOds8&t=34385s)

**Learning objectives:**

- Write a function that accepts any number of keyword arguments with `**kwargs`.
- Explain that `kwargs` is a dictionary and how to read from it.
- Combine normal parameters, `*args` and `**kwargs` in the correct order.
- Pass a dictionary into a function using `**` and forward arguments to another function.

**1. Intuition**

`*args` is a bag for unnamed things; `**kwargs` is a bag of labelled things, like a form with an open "Other details" section where the caller can write any label and value. The function receives them as a dictionary and decides what to do with each.

**2. Why does it exist?**

Some functions accept many optional settings, or must pass unknown options along to another function. Listing every possible option as a parameter is impractical, and new options appear over time. `**kwargs` captures all the extra named arguments so that they can be inspected or forwarded.

**3. Technical explanation**

- In a definition, `**kwargs` collects all extra *keyword* arguments into a *dictionary*: names become keys, values become values. `kwargs` is a convention; the double star is what matters.
- With no extra keyword arguments, `kwargs` is an empty dictionary.
- Order of parameters in a definition: normal parameters, then `*args`, then keyword-only parameters (with defaults), then `**kwargs` last.
- In a call, `f(**mapping)` spreads a dictionary into keyword arguments; the keys must be strings that fit the parameter names (or be collected by `**kwargs`).
- Two dictionaries can be combined into one call with `f(**a, **b)`; a duplicate key is an error.
- Typical uses: configuration options, forwarding (`def wrapper(*args, **kwargs): return target(*args, **kwargs)`), and building flexible functions such as `print`-like helpers.
- Because the caller can send any name, read values with `kwargs.get("name", default)` and check for unknown names if it matters.

**4. Syntax**

```text
def describe(**details):
    for key, value in details.items():
        ...

def f(a, b=2, *args, key=None, **kwargs):
    ...

describe(name="Asha", age=21)
describe(**{"name": "Asha", "age": 21})
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
def describe(**details):
    print(type(details).__name__, details)
    for key, value in details.items():
        print(f"  {key} = {value}")


describe()
describe(name="Asha", age=21)

info = {"city": "Chennai", "job": "engineer"}
describe(**info)
describe(**info, country="India")


def show_all(a, *args, **kwargs):
    print(a, args, kwargs)


show_all(1)
show_all(1, 2, 3)
show_all(1, 2, x=10, y=20)
```

Output:

```text
dict {}
dict {'name': 'Asha', 'age': 21}
  name = Asha
  age = 21
dict {'city': 'Chennai', 'job': 'engineer'}
  city = Chennai
  job = engineer
dict {'city': 'Chennai', 'job': 'engineer', 'country': 'India'}
  city = Chennai
  job = engineer
  country = India
1 () {}
1 (2, 3) {}
1 (2,) {'x': 10, 'y': 20}
```

Line by line:

- `details` is a dictionary of the keyword arguments; for no arguments it is `{}`.
- `**info` spreads the dictionary into keyword arguments; extra named arguments can be added in the same call.
- `show_all` shows how the three kinds of parameters divide the arguments: the first positional value goes to `a`, the other positional values to `args`, and the named ones to `kwargs`.

**6. Example 2 — Practical**

```python
def make_user(name, **options):
    user = {"name": name, "active": True}
    user.update(options)
    return user


print(make_user("Asha"))
print(make_user("Ravi", role="admin", active=False))


def build_request(prompt, model="small", **settings):
    request = {"model": model, "prompt": prompt}
    request.update(settings)
    return request


print(build_request("Hi"))
print(build_request("Hi", temperature=0.2, max_tokens=50))

defaults = {"temperature": 0.7, "max_tokens": 100}
overrides = {"temperature": 0.1}
print(build_request("Hi", **{**defaults, **overrides}))


def html_tag(tag, text, **attributes):
    attrs = "".join(f' {name}="{value}"' for name, value in attributes.items())
    return f"<{tag}{attrs}>{text}</{tag}>"


print(html_tag("a", "link", href="https://example.org", title="home"))
print(html_tag("p", "plain"))


def tell(name, greeting="Hello"):
    return f"{greeting}, {name}"


def forward(*args, **kwargs):
    print("forwarding", args, kwargs)
    return tell(*args, **kwargs)


print(forward("Asha"))
print(forward("Ravi", greeting="Hi"))
print(forward(greeting="Namaste", name="Meena"))


def configure(**options):
    allowed = {"debug", "verbose"}
    unknown = set(options) - allowed
    if unknown:
        raise ValueError(f"unknown options: {sorted(unknown)}")
    return options


print(configure(debug=True))
try:
    configure(debug=True, colour="red")
except ValueError as error:
    print("ValueError:", error)
```

Output:

```text
{'name': 'Asha', 'active': True}
{'name': 'Ravi', 'active': False, 'role': 'admin'}
{'model': 'small', 'prompt': 'Hi'}
{'model': 'small', 'prompt': 'Hi', 'temperature': 0.2, 'max_tokens': 50}
{'model': 'small', 'prompt': 'Hi', 'temperature': 0.1, 'max_tokens': 100}
<a href="https://example.org" title="home">link</a>
<p>plain</p>
forwarding ('Asha',) {}
Hello, Asha
forwarding ('Ravi',) {'greeting': 'Hi'}
Hi, Ravi
forwarding () {'greeting': 'Namaste', 'name': 'Meena'}
Namaste, Meena
{'debug': True}
ValueError: unknown options: ['colour']
```

Line by line:

- `make_user` builds a dictionary from a required `name` and any number of extra fields; `update` merges them, and an option can override a default (`active=False`).
- `build_request` has a named `model` parameter and passes any other setting into the request, similar to how model APIs are called.
- `{**defaults, **overrides}` merges two dictionaries into one (the right one wins); the outer `**` spreads the result into keyword arguments.
- `html_tag` turns arbitrary keyword arguments into attributes.
- `forward` accepts anything and passes it unchanged to `tell`: the `*args, **kwargs` pair is the standard "accept everything and forward" pattern.
- `configure` checks for unknown option names using set difference (see [Set Operations](22-sets.md#set-operations)) and raises an error with a clear message.

**7. Example 3 — Edge case or common mistake**

```python
def f(**kwargs):
    return kwargs


for call in [lambda: f(1), lambda: f(**{"a": 1}, **{"a": 2}), lambda: f(**{1: "x"}), lambda: f(**[("a", 1)])]:
    try:
        call()
    except TypeError as error:
        print("TypeError:", error)
```

Output:

```text
TypeError: f() takes 0 positional arguments but 1 was given
TypeError: __main__.f() got multiple values for keyword argument 'a'
TypeError: keywords must be strings
TypeError: __main__.f() argument after ** must be a mapping, not list
```

`**kwargs` accepts only named arguments, a repeated name is an error, keys must be strings, and `**` needs a dictionary-like object.

Order of parameters matters in the definition (shown as text, because it is a syntax error):

```text
def f(**kwargs, a):
    pass
```

```text
  File "example.py", line 1
    def f(**kwargs, a):
                    ^
SyntaxError: arguments cannot follow var-keyword argument
```

The full order of a definition and a call that uses every kind:

```python
def everything(a, b=2, *args, key="k", **kwargs):
    return {"a": a, "b": b, "args": args, "key": key, "kwargs": kwargs}


print(everything(1))
print(everything(1, 9, 8, 7, key="x", extra=True))
```

Output:

```text
{'a': 1, 'b': 2, 'args': (), 'key': 'k', 'kwargs': {}}
{'a': 1, 'b': 9, 'args': (8, 7), 'key': 'x', 'kwargs': {'extra': True}}
```

Also, `kwargs` is an ordinary new dictionary, so changing it does not change the caller's dictionary:

```python
def change(**kwargs):
    kwargs["added"] = True
    return kwargs


original = {"x": 1}
print(change(**original), original)
```

Output:

```text
{'x': 1, 'added': True} {'x': 1}
```

Typing mistakes in names are silently accepted by `**kwargs`:

```python
def connect(host, **options):
    timeout = options.get("timeout", 30)
    return host, timeout


print(connect("db", timeout=5))
print(connect("db", timeuot=5))
```

Output:

```text
('db', 5)
('db', 30)
```

The second call mis-spells `timeout`, and nothing complains: the function simply uses the default. Where the names are known, use explicit parameters (which give a clear `TypeError`) or validate the keys, as `configure` did above.

**8. Common mistakes**

- Putting `**kwargs` anywhere except last in the parameter list.
- Passing positional values to a function that only has `**kwargs`.
- Forgetting the `**` when passing a dictionary (it would be one positional argument).
- Mis-spelling an option name, which `**kwargs` silently accepts.
- Using `**kwargs` when a few explicit, documented parameters would be clearer.
- Passing the same key twice when merging dictionaries into a call.
- Expecting changes to `kwargs` to change the caller's dictionary.

**9. Real-world and AI applications**

Calling model APIs is mostly keyword arguments, and applications usually keep their settings in a dictionary and call `client.generate(**settings)`. Wrapper functions use `*args, **kwargs` to pass everything on to the library, so that they can add logging, retries or timing without knowing the library's full list of options. The same pattern is behind decorators (functions that wrap other functions), a topic you will meet again in later Python study. Tool-calling agents (see [Model Context Protocol and AI Agents](38-mcp-and-ai-agents.md)) work the same way: the model produces a dictionary of argument names and values, and the program calls the chosen function with `**arguments`.

**10. Practice**

1. Write `show_profile(**info)` that prints `key: value` for each item. Call it with three keywords.
2. Write `make_settings(**options)` that returns a dictionary with defaults `{"debug": False}` overridden by the options.
3. Write `wrapper(*args, **kwargs)` that prints its arguments and calls `max(*args, **kwargs)`. Try `wrapper(3, 9, 4)` and `wrapper([3, 9, 4], key=lambda x: -x)`.
4. Merge `{"a": 1, "b": 2}` and `{"b": 3, "c": 4}` into one set of keyword arguments for a call.
5. Write `format_user(name, *tags, **fields)` and call it with a name, two tags and two fields.
6. What does `f(**{"x": 1})` do if `f` is defined as `def f(x):`? And as `def f(**kw):`?
7. Why might `**kwargs` hide a typing mistake, and how can you catch it?

**11. Interview questions**

- *What does `**kwargs` collect?* All extra keyword arguments, as a dictionary.
- *What is the required order of parameters in a definition?* Normal, `*args`, keyword-only, `**kwargs`.
- *What does `**` do in a call?* Unpacks a dictionary into keyword arguments.
- *What is the `*args, **kwargs` forwarding pattern for?* Accepting any arguments and passing them to another function unchanged.
- *What is the downside of `**kwargs`?* Mis-spelt or unexpected names are silently accepted and the function signature does not document the options.

**12. Quick revision**

- `**kwargs` is a dictionary of extra keyword arguments; it comes last in a definition.
- Order: `a, b=2, *args, key=None, **kwargs`.
- `f(**mapping)` unpacks a dictionary; `{**a, **b}` merges two.
- Forward everything with `target(*args, **kwargs)`.
- Validate unknown names when it matters.

---

## Answers to Practice Exercises

### Answers: Positional Arguments

1.

```python
def rectangle_area(width, height):
    return width * height


print(rectangle_area(4, 5), rectangle_area(width=4, height=5), rectangle_area(4, height=5))
```

Output:

```text
20 20 20
```

2.

```python
def divide(a, b):
    return a / b


print(divide(10, 2), divide(2, 10), divide(b=2, a=10))
```

Output:

```text
5.0 0.2 5.0
```

Positional values are matched by order, so swapping them swaps the roles. The keyword version makes the roles explicit.

3.

```python
def introduce(name, age):
    return f"{name} is {age}"


print(introduce(*["Asha", 21]))
print(introduce(**{"name": "Ravi", "age": 22}))
```

Output:

```text
Asha is 21
Ravi is 22
```

4.

```python
def introduce(name, age):
    return f"{name} is {age}"


for call in [lambda: introduce("Asha"), lambda: introduce("Asha", 21, 5), lambda: introduce("Asha", age=21, name="B")]:
    try:
        call()
    except TypeError as error:
        print("TypeError:", error)
```

Output:

```text
TypeError: introduce() missing 1 required positional argument: 'age'
TypeError: introduce() takes 2 positional arguments but 3 were given
TypeError: introduce() got multiple values for argument 'name'
```

5.

```python
def join_words(first, second, *, sep):
    return first + sep + second


print(join_words("a", "b", sep="-"))
try:
    join_words("a", "b", "-")
except TypeError as error:
    print("TypeError:", error)
```

Output:

```text
a-b
TypeError: join_words() takes 2 positional arguments but 3 were given
```

6. In the definition of `print`, `sep` and `end` come after the `*values` parameter, so they are keyword-only: anything given by position is treated as one more value to print.

```python
print("a", "b", "-")
print("a", "b", sep="-")
```

Output:

```text
a b -
a-b
```

### Answers: Default Arguments

1.

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}"


print(greet("Asha"))
print(greet("Asha", "Hi"))
print(greet(name="Asha", greeting="Namaste"))
```

Output:

```text
Hello, Asha
Hi, Asha
Namaste, Asha
```

2.

```python
def area(length, width=None):
    if width is None:
        width = length
    return length * width


print(area(4), area(4, 5))
```

Output:

```text
16 20
```

3.

```python
def repeat(text, times=2, separator=" "):
    return separator.join([text] * times)


print(repeat("go"))
print(repeat("go", 3))
print(repeat("go", separator="-"))
print(repeat("go", 3, ", "))
```

Output:

```text
go go
go go go
go-go
go, go, go
```

4.

```python
def add(x, items=None):
    if items is None:
        items = []
    items.append(x)
    return items


print(add(1), add(2), add(3, [10]))
```

Output:

```text
[1] [2] [10, 3]
```

5. A parameter without a default may not follow one with a default, because a call such as `f(5)` could not say which parameter the 5 belongs to. Python rejects the definition with a `SyntaxError`.

6. The default `time.time()` is evaluated once, when the function is defined, so every call that omits `when` gets the same stale time. Fix:

```python
import time


def log(message, when=None):
    if when is None:
        when = time.time()
    return message, when is not None


print(log("started"))
```

Output:

```text
('started', True)
```

7.

```python
def with_or(greeting=None):
    greeting = greeting or "Hello"
    return repr(greeting)


def with_is(greeting=None):
    if greeting is None:
        greeting = "Hello"
    return repr(greeting)


print(with_or(""), with_is(""))
```

Output:

```text
'Hello' ''
```

`or` replaces any falsy value (including a deliberate empty string); `is None` replaces only a missing argument.

### Answers: Variable-Length Arguments (*args)

1.

```python
def multiply(*numbers):
    result = 1
    for n in numbers:
        result *= n
    return result


print(multiply(2, 3, 4), multiply(5), multiply())
```

Output:

```text
24 5 1
```

2.

```python
def longest(*words):
    result = ""
    for word in words:
        if len(word) > len(result):
            result = word
    return result


print(longest("tea", "coffee", "milk"), repr(longest()))
```

Output:

```text
coffee ''
```

3.

```python
def print_all(label, *items):
    print(label)
    for item in items:
        print(" -", item)


print_all("Fruits", "apple", "banana")
```

Output:

```text
Fruits
 - apple
 - banana
```

4.

```python
def multiply(*numbers):
    result = 1
    for n in numbers:
        result *= n
    return result


print(multiply(*[2, 3, 4]))
```

Output:

```text
24
```

5.

```python
def join_with(sep, *parts):
    return sep.join(parts)


print(join_with("-", "a", "b", "c"))
```

Output:

```text
a-b-c
```

6. `args` is a tuple, so it can be read, indexed and looped over but not changed in place; make a list from it if you need to change the items.

```python
def f(*args):
    return type(args).__name__, len(args)


print(f(1, 2, 3))
```

Output:

```text
('tuple', 3)
```

7. Parameters after `*args` are keyword-only, so `x` must be given by name; `f(1, 2, 3)` puts all three values into `args` and leaves `x` missing.

```python
def f(*args, x):
    return args, x


print(f(1, 2, 3, x=4))
try:
    f(1, 2, 3)
except TypeError as error:
    print("TypeError:", error)
```

Output:

```text
((1, 2, 3), 4)
TypeError: f() missing 1 required keyword-only argument: 'x'
```

### Answers: Keyword Arguments (**kwargs)

1.

```python
def show_profile(**info):
    for key, value in info.items():
        print(f"{key}: {value}")


show_profile(name="Asha", age=21, city="Chennai")
```

Output:

```text
name: Asha
age: 21
city: Chennai
```

2.

```python
def make_settings(**options):
    settings = {"debug": False}
    settings.update(options)
    return settings


print(make_settings())
print(make_settings(debug=True, level=3))
```

Output:

```text
{'debug': False}
{'debug': True, 'level': 3}
```

3.

```python
def wrapper(*args, **kwargs):
    print("calling max with", args, sorted(kwargs))
    return max(*args, **kwargs)


print(wrapper(3, 9, 4))
print(wrapper([3, 9, 4], key=lambda x: -x))
```

Output:

```text
calling max with (3, 9, 4) []
9
calling max with ([3, 9, 4],) ['key']
3
```

4.

```python
def show(**kw):
    return kw


a = {"a": 1, "b": 2}
b = {"b": 3, "c": 4}
print(show(**{**a, **b}))
```

Output:

```text
{'a': 1, 'b': 3, 'c': 4}
```

Using `show(**a, **b)` directly would raise a `TypeError`, because `b` is given twice; merging first lets the later dictionary win.

5.

```python
def format_user(name, *tags, **fields):
    return f"{name} tags={list(tags)} fields={fields}"


print(format_user("Asha", "admin", "dev", city="Chennai", age=21))
```

Output:

```text
Asha tags=['admin', 'dev'] fields={'city': 'Chennai', 'age': 21}
```

6. With `def f(x)`, the call `f(**{"x": 1})` becomes `f(x=1)` and works. With `def f(**kw)`, the dictionary entries arrive in `kw`.

```python
def f(x):
    return x


def g(**kw):
    return kw


print(f(**{"x": 1}), g(**{"x": 1}))
```

Output:

```text
1 {'x': 1}
```

7. `**kwargs` accepts any name, so a mis-spelt option is just another entry that the function ignores. Catch it by listing explicit parameters, or by comparing the received names to an allowed set and raising an error.

```python
def connect(**options):
    allowed = {"timeout", "retries"}
    unknown = set(options) - allowed
    if unknown:
        raise TypeError(f"unknown options: {sorted(unknown)}")
    return options


print(connect(timeout=5))
try:
    connect(timeuot=5)
except TypeError as error:
    print("TypeError:", error)
```

Output:

```text
{'timeout': 5}
TypeError: unknown options: ['timeuot']
```

---

## Chapter Summary and Key Takeaways

- Positional arguments are matched by order and keyword arguments by name; positional ones come first in a call, and a value cannot be given twice. `f(*seq)` and `f(**mapping)` unpack in a call, and `/` and `*` in a definition make parameters positional-only or keyword-only.
- A default value (`b=10`) makes a parameter optional; defaults come after required parameters and are evaluated once at definition time, so never use a mutable default; use `None` and test `is None`.
- `*args` collects extra positional arguments into a tuple; `**kwargs` collects extra keyword arguments into a dictionary; the order is normal, `*args`, keyword-only, `**kwargs`.
- `target(*args, **kwargs)` forwards everything to another function, and `{**a, **b}` merges settings dictionaries.
- Explicit parameters are clearer and give better error messages than `**kwargs`, so use the flexible forms only when the number or names of arguments really vary.

Next: [Chapter 27 — Variable Scope](27-variable-scope.md) explains where names are visible.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
