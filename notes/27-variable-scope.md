# Chapter 27 — Variable Scope

> Part 5 — Functions and Functional Programming · Video: 9:40:20–9:56:08 · Previous: [26 Function Arguments](26-function-arguments.md) · Next: [28 First-Class Functions and Lambda](28-first-class-functions-and-lambda.md)

**In this chapter:** where a name can be seen and changed: local and global variables, the order in which Python looks names up (the LEGB rule), the `global` and `nonlocal` keywords, the classic `UnboundLocalError`, how nested functions and closures keep outer values alive, and why functions should usually take parameters and return values instead of changing globals.

**Before you start:** you need functions and `return` from [Defining Your Own Function](25-defining-functions-and-return-values.md#defining-your-own-function) and parameters from [Function Arguments](26-function-arguments.md). Recap: when a function is called, its parameters and the variables it creates live in a private workspace that is discarded when the call ends; a variable is a name that refers to an object. Examples were run with Python 3.13.

---

## Variable Scope: Local vs Global

**Timestamp:** [9:40:20](https://www.youtube.com/watch?v=J9BI0jGOds8&t=34820s)

**Learning objectives:**

- Define *scope* and distinguish local, enclosing, global and built-in scopes.
- Predict which variable a name refers to when the same name is used in several places.
- Use `global` and `nonlocal` correctly, and explain why they should be rare.
- Explain `UnboundLocalError` and the behaviour of closures.

**1. Intuition**

Think of a building. A notice pinned on the lobby wall (a *global* variable) can be read by everyone in the building. A note on your own desk (a *local* variable) is visible only in your room, and when you leave for the day it is cleared away. If your room has a note with the same heading as the lobby notice, people in your room read your note first. Rooms inside rooms (nested functions) can look out at the rooms around them, but not into each other.

**2. Why does it exist?**

If every variable were visible everywhere, two functions that happened to use the name `total` would overwrite each other's data, and large programs would be impossible to reason about. Scope keeps each function's working variables private, so a function can be understood, tested and reused without worrying about what the rest of the program calls its variables. Only what is deliberately passed in (parameters) and given back (`return`) crosses the boundary.

**3. Technical explanation**

*Scope* is the region of a program where a name is visible. Python looks up a name in this order, called the **LEGB rule**:

1. **L**ocal: the current function (its parameters and the variables assigned inside it).
2. **E**nclosing: the scopes of any functions that contain the current function (for nested functions).
3. **G**lobal: the module (file) level, outside all functions.
4. **B**uilt-in: names that Python provides, such as `len`, `print` and `max`.

The first match wins; if no scope has the name, the result is a `NameError`.

Key rules:

- *Assignment creates a local.* If a function assigns to a name anywhere in its body (`x = 5`, `x += 1`, a `for x in` loop), Python treats `x` as local to the *whole* function. A function that only *reads* a name uses the global value if there is no local one.
- Assigning inside a function to a name that exists globally creates a new local variable that *shadows* the global; the global is untouched.
- The `global` statement (`global counter`) says "this name refers to the global variable", so assignments change the global. Use it rarely.
- The `nonlocal` statement (`nonlocal count`) says "this name refers to the variable in the nearest enclosing function", so a nested function can change it.
- *Mutable objects*: `items.append(1)` does not assign to the name `items`, it changes the object, so it works on a global list without `global`. Rebinding the name (`items = [...]`) needs `global`.
- *Reading before assigning* in the same function gives `UnboundLocalError` (a subtype of `NameError`), because the assignment later in the body made the name local.
- *No block scope*: in Python, `if`, `for` and `while` blocks do not create a new scope. A variable first assigned inside them is visible after them in the same function (if it was assigned). Comprehension variables, however, are local to the comprehension.
- *Closures*: a nested function remembers the variables of the enclosing function even after that function has returned. This is how a function can "carry" a value with it.
- *Constants*: global values meant to stay fixed are written in capital letters by convention (`TAX_RATE = 0.18`) and are only read in functions.
- *Good practice*: pass values in as parameters and return results out. This makes functions testable and keeps the data flow visible.
- Local variable lookup is also slightly faster than global lookup, but that is a minor point.

**4. Syntax**

```text
counter = 0                      # global

def f():
    global counter               # refer to the global name
    counter += 1

def outer():
    count = 0
    def inner():
        nonlocal count           # refer to the enclosing name
        count += 1
        return count
    return inner
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
message = "global message"


def show():
    message = "local message"
    print("inside:", message)


show()
print("outside:", message)


def read_only():
    print("reading the global:", message)


read_only()


def local_only():
    secret = 42
    return secret


print(local_only())
try:
    print(secret)
except NameError as error:
    print("NameError:", error)

x = 10


def shadow(x):
    x = x + 1
    return x


print(shadow(1), x)
print(len("abc"))
```

Output:

```text
inside: local message
outside: global message
reading the global: global message
42
NameError: name 'secret' is not defined
2 10
3
```

Line by line:

- `show` assigns `message`, which makes a new local variable. It shadows the global one inside the function, and the global value is unchanged afterwards.
- `read_only` only reads `message`, so Python finds the global.
- `secret` exists only while `local_only` runs; outside it is a `NameError`.
- The parameter `x` of `shadow` is a local name, separate from the global `x`, which stays 10.
- `len` is found in the built-in scope, the last place Python looks.

**6. Example 2 — Practical**

```python
TAX_RATE = 0.18
visits = 0


def price_with_tax(price):
    return round(price * (1 + TAX_RATE), 2)


def count_visit():
    global visits
    visits += 1
    return visits


print(price_with_tax(200))
count_visit()
count_visit()
print("visits:", visits)


def make_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment


counter_a = make_counter()
counter_b = make_counter()
print(counter_a(), counter_a(), counter_a(), counter_b())


def make_multiplier(factor):
    def multiply(value):
        return value * factor
    return multiply


double = make_multiplier(2)
triple = make_multiplier(3)
print(double(10), triple(10))


def outer():
    level = "outer"

    def middle():
        def inner():
            return level
        return inner()

    return middle()


print(outer())

history = []


def remember(item):
    history.append(item)


remember("a")
remember("b")
print(history)


def pure_counter(current):
    return current + 1


n = 0
n = pure_counter(n)
n = pure_counter(n)
print(n)
```

Output:

```text
236.0
visits: 2
1 2 3 1
20 30
outer
['a', 'b']
2
```

Line by line:

- `TAX_RATE` is a global constant that functions only read. `count_visit` must use `global` because it rebinds the name `visits`.
- `make_counter` returns the inner function. The variable `count` lives on in a *closure*: each counter has its own count, which `nonlocal` allows `increment` to update. `counter_a` and `counter_b` do not interfere.
- `make_multiplier` is a function factory: the returned function remembers `factor`.
- `inner` finds `level` two scopes up (the enclosing scopes, `middle` and then `outer`).
- `remember` changes the global *list* with `append`, which needs no `global` statement because it does not rebind the name `history`.
- `pure_counter` is the better style: it takes the value in and returns the new value. The data flow is visible at the call site, and the function can be tested on its own.

**7. Example 3 — Edge case or common mistake**

The most common scope error:

```python
counter = 0


def increment():
    counter += 1
    return counter


try:
    increment()
except UnboundLocalError as error:
    print("UnboundLocalError:", error)
print(counter)
```

Output:

```text
UnboundLocalError: cannot access local variable 'counter' where it is not associated with a value
0
```

Because the function assigns to `counter` (`+=` is an assignment), Python treats `counter` as local for the whole function, and the read on the right-hand side happens before any local value exists. Fix it with `global counter`, or better, pass the value in and return the new one.

Reading works but the *same name* assigned later in the function breaks it:

```python
level = 5


def reader():
    return level


def broken():
    print(level)
    level = 10


print(reader())
try:
    broken()
except UnboundLocalError as error:
    print("UnboundLocalError:", error)
```

Output:

```text
5
UnboundLocalError: cannot access local variable 'level' where it is not associated with a value
```

`broken` assigns `level` later, so the earlier `print(level)` is a read of a local that has not got a value yet.

`global` and `nonlocal` are not interchangeable, and `nonlocal` needs an enclosing function:

```python
x = "global"


def outer():
    x = "enclosing"

    def inner_global():
        global x
        x = "changed by global"

    def inner_nonlocal():
        nonlocal x
        x = "changed by nonlocal"

    inner_nonlocal()
    after_nonlocal = x
    inner_global()
    return after_nonlocal, x


print(outer())
print(x)
```

Output:

```text
('changed by nonlocal', 'changed by nonlocal')
changed by global
```

`nonlocal` changed the variable in `outer`; `global` changed the module-level one. `nonlocal` for a name that has no enclosing function variable is a `SyntaxError` (shown as text):

```text
x = 1

def f():
    nonlocal x
```

```text
  File "example.py", line 4
    nonlocal x
    ^^^^^^^^^^
SyntaxError: no binding for nonlocal 'x' found
```

Blocks do not create scopes, but comprehensions and functions do:

```python
def demo():
    for i in range(3):
        last = i
    print(i, last)
    squares = [n * n for n in range(3)]
    try:
        print(n)
    except NameError as error:
        print("NameError:", error)
    return squares


print(demo())
```

Output:

```text
2 2
NameError: name 'n' is not defined
[0, 1, 4]
```

The loop variable `i` and `last` are still visible after the loop, while the comprehension's `n` is not.

A subtle closure trap: closures capture the *variable*, not its value at the time:

```python
functions = []
for i in range(3):
    functions.append(lambda: i)
print([f() for f in functions])

functions = []
for i in range(3):
    functions.append(lambda i=i: i)
print([f() for f in functions])
```

Output:

```text
[2, 2, 2]
[0, 1, 2]
```

All three lambdas in the first list see the same `i`, which ends at 2. Giving the lambda a parameter with a default (`i=i`) captures the current value for each (see [Lambda Functions](28-first-class-functions-and-lambda.md#lambda-functions)).

Finally, shadowing a built-in name breaks later code:

```python
def total_length(words):
    return sum(len(word) for word in words)


print(total_length(["a", "bb"]))
len = 5
try:
    print(total_length(["a", "bb"]))
except TypeError as error:
    print("TypeError:", error)
del len
print(total_length(["a", "bb"]))
```

Output:

```text
3
TypeError: 'int' object is not callable
3
```

Assigning `len = 5` at module level hid the built-in function; the call inside the generator expression then found the number 5 first. Removing the global name with `del` restored the built-in. Avoid naming variables `list`, `str`, `len`, `max`, `sum`, `input` or `type`.

**8. Common mistakes**

- Assigning to a global name inside a function without `global`, then being surprised that the global did not change (or that `UnboundLocalError` appears).
- Reading a variable and assigning it later in the same function.
- Using `global` everywhere instead of parameters and `return`.
- Confusing `global` with `nonlocal`.
- Expecting a variable created inside a function to exist outside it.
- Expecting a loop or `if` block to have its own scope (it does not), or a comprehension variable to leak (it does not).
- Capturing a loop variable in a lambda or nested function and getting its final value.
- Shadowing built-in names such as `list`, `sum` or `max`.
- Changing a global list or dictionary from many functions, which makes bugs hard to find.

**9. Real-world and AI applications**

Global *constants* are normal and useful: `MODEL_NAME`, `MAX_RETRIES`, `API_URL`, which are read in many functions. Global *mutable state* (a global list of messages that every function appends to) is the source of confusing bugs, especially when a web server handles many users at once: their data can mix. Closures are used to build configured functions (a `make_prompt_builder(system_message)` that returns a function with the system message built in) and to build counters, caches and decorators. Keeping a conversation history in an object or passing it as a parameter, instead of a global, is the standard fix.

**10. Practice**

1. Predict the output, then run it: `x = 1`, `def f(): x = 2; print(x)`, `f()`, `print(x)`.
2. Write a function that reads a global constant `RATE = 0.1` to compute interest, and explain why it needs no `global` statement.
3. Write `add_visit()` that increments a global counter, first with `global`, then rewrite it as `new_count = add_visit(count)` with no global.
4. Reproduce and then fix an `UnboundLocalError` caused by `total += 1` in a function.
5. Write `make_accumulator()` that returns a function; each call to it adds a number to a running total and returns the total (use `nonlocal`).
6. What is the output of `[f() for f in [lambda: i for i in range(3)]]`, and why? How do you fix it?
7. Explain the LEGB rule in your own words with an example for each letter.
8. Why can a function append to a global list without the `global` keyword, but not reassign it?

**11. Interview questions**

- *What is the LEGB rule?* The lookup order for names: Local, Enclosing, Global, Built-in.
- *What does the `global` keyword do?* Makes assignments to the name inside a function refer to the module-level variable.
- *What is `nonlocal` for?* To rebind a variable of the nearest enclosing function from a nested function.
- *Why does `UnboundLocalError` occur?* A name that is assigned anywhere in a function is local throughout it, so reading it before assignment fails.
- *What is a closure?* A function that remembers variables from the scope in which it was created.
- *Why avoid global variables?* They hide the flow of data, make functions hard to test and reuse, and let any code change shared state.

**12. Quick revision**

- Scope lookup: Local, Enclosing, Global, Built-in (LEGB).
- Assignment inside a function makes the name local (shadowing any global).
- `global x` and `nonlocal x` rebind outer variables; mutating an object (`append`) needs neither.
- `UnboundLocalError`: reading a name that the function also assigns, before the assignment.
- No block scope for `if`/`for`/`while`; functions and comprehensions have their own.
- Prefer parameters and `return` over globals; global constants in CAPITALS are fine.

---

## Answers to Practice Exercises

### Answers: Variable Scope: Local vs Global

1. The function creates its own local `x`, so it prints 2, and the global `x` stays 1.

```python
x = 1


def f():
    x = 2
    print(x)


f()
print(x)
```

Output:

```text
2
1
```

2. The function only *reads* `RATE`, and reading a global needs no declaration. A `global` statement is needed only to rebind the name.

```python
RATE = 0.1


def interest(amount):
    return amount * RATE


print(interest(500))
```

Output:

```text
50.0
```

3.

```python
count = 0


def add_visit():
    global count
    count += 1


add_visit()
add_visit()
print(count)


def next_count(current):
    return current + 1


value = 0
value = next_count(value)
value = next_count(value)
print(value)
```

Output:

```text
2
2
```

4.

```python
total = 0


def broken():
    total += 1


try:
    broken()
except UnboundLocalError as error:
    print("UnboundLocalError:", error)


def fixed(total):
    total += 1
    return total


print(fixed(total))
```

Output:

```text
UnboundLocalError: cannot access local variable 'total' where it is not associated with a value
1
```

5.

```python
def make_accumulator():
    running = 0

    def add(amount):
        nonlocal running
        running += amount
        return running

    return add


acc = make_accumulator()
print(acc(10), acc(5), acc(1))
other = make_accumulator()
print(other(100))
```

Output:

```text
10 15 16
100
```

6. All the lambdas share the same variable `i` of the enclosing scope, and by the time they are called it holds its final value, 2. A default parameter captures the value of each round.

```python
broken = [lambda: i for i in range(3)]
print([f() for f in broken])

fixed = [lambda i=i: i for i in range(3)]
print([f() for f in fixed])
```

Output:

```text
[2, 2, 2]
[0, 1, 2]
```

7. Local: the names inside the current function. Enclosing: names in an outer function around it. Global: names at the top of the file. Built-in: names Python provides. One example of each in a single program:

```python
greeting = "global"


def outer():
    name = "enclosing"

    def inner():
        word = "local"
        return word, name, greeting, len(word)

    return inner()


print(outer())
```

Output:

```text
('local', 'enclosing', 'global', 5)
```

`word` is local, `name` comes from the enclosing function, `greeting` is global, and `len` is built in.

8. Appending changes the list object that the global name refers to. It never assigns to the name, so Python does not make a local variable. Writing `items = [...]` is an assignment, which would create a new local name (or fail with `UnboundLocalError`) unless the function declares `global items`.

```python
items = []


def append_ok():
    items.append(1)


def reassign_global():
    global items
    items = ["new"]


def reassign_local():
    items = ["local only"]


append_ok()
print(items)
reassign_local()
print(items)
reassign_global()
print(items)
```

Output:

```text
[1]
[1]
['new']
```

---

## Chapter Summary and Key Takeaways

- Names are looked up in the order Local, Enclosing, Global, Built-in (LEGB); the first match wins, and no match is a `NameError`.
- Assigning to a name inside a function makes it local for the whole function, shadowing any global; reading before assigning in the same function gives `UnboundLocalError`.
- `global` rebinds a module-level name and `nonlocal` rebinds an enclosing function's variable; changing a mutable object in place needs neither.
- `if`, `for` and `while` blocks share the scope of their function, while functions and comprehensions create their own; closures remember the variables of the scope that created them (capturing the variable, not a snapshot).
- Prefer parameters and `return` over globals, keep global constants in capital letters, and do not name variables after built-ins such as `list` or `len`.

Next: [Chapter 28 — First-Class Functions and Lambda](28-first-class-functions-and-lambda.md) shows how functions themselves can be passed around like values.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
