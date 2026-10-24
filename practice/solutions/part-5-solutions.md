# Part 5 — Solutions: Functions and Functional Programming

> [Practice index](../README.md) · [Problems for this part](../part-5-exercises.md)

Every program below was run with Python 3.13 and the output shown is the real output. Your own solution may differ and still be correct: compare behaviour, not wording.

## P5.1 — Defaults and return values

Write `greet(name, greeting="Hello", punctuation="!")` that returns (not prints) the message. Call it with only a name, with a custom greeting, and with the punctuation as a keyword argument.

```python
def greet(name, greeting="Hello", punctuation="!"):
    return f"{greeting}, {name}{punctuation}"


print(greet("Asha"))
print(greet("Asha", "Namaste"))
print(greet("Asha", punctuation="?"))
```

Output:

```text
Hello, Asha!
Namaste, Asha!
Hello, Asha?
```

Parameters with defaults can be omitted; keyword arguments let you skip earlier defaults.

## P5.2 — *args and **kwargs

Write `total(*numbers)` returning the sum of any number of arguments, and `describe(**details)` returning a string like `name=Asha, age=21` in sorted key order.

```python
def total(*numbers):
    return sum(numbers)


def describe(**details):
    return ", ".join(f"{k}={v}" for k, v in sorted(details.items()))


print(total(1, 2, 3, 4))
print(total())
print(describe(name="Asha", age=21))
```

Output:

```text
10
0
age=21, name=Asha
```

Extra positional arguments are collected into a tuple and extra keyword arguments into a dictionary.

## P5.3 — Scope and closures

Show that assigning to a variable inside a function creates a local one (the global stays 10). Then write `make_counter()` returning a function that increases and returns a private count each time it is called, using `nonlocal`.

```python
x = 10


def change():
    x = 99
    return x


print(change(), x)


def make_counter():
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter


c1, c2 = make_counter(), make_counter()
print(c1(), c1(), c1(), c2())
```

Output:

```text
99 10
1 2 3 1
```

Each call to `make_counter` creates its own `count`; `nonlocal` lets the inner function update it, so the counters are independent.

## P5.4 — Sort with lambda keys

Sort `["pear", "fig", "banana", "kiwi", "apple"]` by length, then alphabetically for equal lengths. Then sort the dictionary items of `{"a": 3, "b": 1, "c": 2}` by value, highest first.

```python
fruits = ["pear", "fig", "banana", "kiwi", "apple"]
print(sorted(fruits, key=lambda f: (len(f), f)))
scores = {"a": 3, "b": 1, "c": 2}
print(sorted(scores.items(), key=lambda item: item[1], reverse=True))
```

Output:

```text
['fig', 'kiwi', 'pear', 'apple', 'banana']
[('a', 3), ('c', 2), ('b', 1)]
```

`key` is called once per element; tuples compare left to right, giving the tie-breaker for free.

## P5.5 — map, filter, reduce

From `numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]` compute the product of the squares of the odd numbers using `filter`, `map` and `functools.reduce`.

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
odds = filter(lambda n: n % 2 == 1, numbers)
squares = map(lambda n: n ** 2, odds)
print(reduce(lambda a, b: a * b, squares))
```

Output:

```text
893025
```

`filter` and `map` produce lazy iterators that are consumed once by `reduce`, which folds them into a single product.

## P5.6 — Compose functions

Write `compose(f, g)` returning a function that computes `f(g(x))`. Use it to build `add_then_double` from `lambda x: x * 2` and `lambda x: x + 1`.

```python
def compose(f, g):
    return lambda x: f(g(x))


add_then_double = compose(lambda x: x * 2, lambda x: x + 1)
print(add_then_double(5))
```

Output:

```text
12
```

`g` runs first, then `f`; functions are values, so they can be passed in and returned.

## P5.7 — Return several values

Write `stats(values)` returning the minimum, maximum and mean (rounded to 2 decimals) and unpack the result into three names.

```python
def stats(values):
    return min(values), max(values), round(sum(values) / len(values), 2)


low, high, mean = stats([3, 9, 4, 8])
print(low, high, mean)
```

Output:

```text
3 9 6.0
```

A function returns one object; returning a tuple gives several values that the caller unpacks.

## P5.8 — Recursion

Write a recursive `factorial(n)` and a recursive `fib(n)` (with `fib(0) = 0`, `fib(1) = 1`). Print `factorial(6)` and the first 10 Fibonacci numbers.

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


print(factorial(6))
print([fib(i) for i in range(10)])
```

Output:

```text
720
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

The base case stops the recursion; each call reduces `n` until it is reached. This `fib` is simple but slow for large `n`.

## P5.9 — Keyword-only arguments

Write `connect(host, *, timeout=30)` where `timeout` can only be given by keyword. Show that passing it positionally raises a `TypeError` (catch it and print the message).

```python
def connect(host, *, timeout=30):
    return f"{host} (timeout {timeout}s)"


print(connect("example.org"))
print(connect("example.org", timeout=5))
try:
    connect("example.org", 5)
except TypeError as error:
    print("TypeError:", error)
```

Output:

```text
example.org (timeout 30s)
example.org (timeout 5s)
TypeError: connect() takes 1 positional argument but 2 were given
```

Everything after the bare `*` is keyword-only, which makes calls self-documenting.

## P5.10 — A function factory

Write `make_multiplier(n)` returning a function that multiplies by `n`. Build `double` and `triple` and apply them with `map` to `[1, 2, 3]`.

```python
def make_multiplier(n):
    return lambda x: x * n


double, triple = make_multiplier(2), make_multiplier(3)
print(list(map(double, [1, 2, 3])))
print(list(map(triple, [1, 2, 3])))
```

Output:

```text
[2, 4, 6]
[3, 6, 9]
```

The returned function keeps access to `n` from the enclosing call (a closure).

## P5.11 — The mutable default trap

Show what goes wrong with `def add(item, bucket=[]): bucket.append(item); return bucket` when it is called twice without a bucket, then fix it.

```python
def add_bad(item, bucket=[]):
    bucket.append(item)
    return bucket


print(add_bad(1))
print(add_bad(2))


def add_good(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


print(add_good(1))
print(add_good(2))
```

Output:

```text
[1]
[1, 2]
[1]
[2]
```

Default values are created once, when the function is defined, so the same list is reused on every call; `None` plus a fresh list avoids that.

---

Back to the [problems](../part-5-exercises.md) or the [practice index](../README.md).
