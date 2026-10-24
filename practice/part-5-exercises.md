# Part 5 — Extra Practice: Functions and Functional Programming

> [Practice index](README.md) · [Solutions for this part](solutions/part-5-solutions.md)

These 11 problems go beyond the exercises inside the chapters. Try each one on your own before opening the solutions. Run your code, compare with your prediction, and only then check the solution. Related chapters:

- [Chapter 25 — Defining Functions and Return Values](../notes/25-defining-functions-and-return-values.md)
- [Chapter 26 — Function Arguments](../notes/26-function-arguments.md)
- [Chapter 27 — Variable Scope](../notes/27-variable-scope.md)
- [Chapter 28 — First-Class Functions and Lambda](../notes/28-first-class-functions-and-lambda.md)
- [Chapter 29 — map(), filter() and reduce()](../notes/29-map-filter-reduce.md)

Tips: write a few lines at a time and run often; if you are stuck for more than ten minutes read only the hint again, then the solution's explanation; afterwards rewrite the solution from memory.

## P5.1 — Defaults and return values

Write `greet(name, greeting="Hello", punctuation="!")` that returns (not prints) the message. Call it with only a name, with a custom greeting, and with the punctuation as a keyword argument.

*Hint:* Defaults come after required parameters.

## P5.2 — *args and **kwargs

Write `total(*numbers)` returning the sum of any number of arguments, and `describe(**details)` returning a string like `name=Asha, age=21` in sorted key order.

*Hint:* `*args` is a tuple, `**kwargs` is a dictionary.

## P5.3 — Scope and closures

Show that assigning to a variable inside a function creates a local one (the global stays 10). Then write `make_counter()` returning a function that increases and returns a private count each time it is called, using `nonlocal`.

*Hint:* `global` changes a module-level name; `nonlocal` changes an enclosing function's name.

## P5.4 — Sort with lambda keys

Sort `["pear", "fig", "banana", "kiwi", "apple"]` by length, then alphabetically for equal lengths. Then sort the dictionary items of `{"a": 3, "b": 1, "c": 2}` by value, highest first.

*Hint:* A key that returns a tuple sorts by each element in turn.

## P5.5 — map, filter, reduce

From `numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]` compute the product of the squares of the odd numbers using `filter`, `map` and `functools.reduce`.

*Hint:* Odd: `n % 2 == 1`.

## P5.6 — Compose functions

Write `compose(f, g)` returning a function that computes `f(g(x))`. Use it to build `add_then_double` from `lambda x: x * 2` and `lambda x: x + 1`.

*Hint:* A function can return a function.

## P5.7 — Return several values

Write `stats(values)` returning the minimum, maximum and mean (rounded to 2 decimals) and unpack the result into three names.

*Hint:* Return a tuple.

## P5.8 — Recursion

Write a recursive `factorial(n)` and a recursive `fib(n)` (with `fib(0) = 0`, `fib(1) = 1`). Print `factorial(6)` and the first 10 Fibonacci numbers.

*Hint:* Every recursive function needs a base case.

## P5.9 — Keyword-only arguments

Write `connect(host, *, timeout=30)` where `timeout` can only be given by keyword. Show that passing it positionally raises a `TypeError` (catch it and print the message).

*Hint:* The bare `*` ends positional parameters.

## P5.10 — A function factory

Write `make_multiplier(n)` returning a function that multiplies by `n`. Build `double` and `triple` and apply them with `map` to `[1, 2, 3]`.

*Hint:* The inner function remembers `n`.

## P5.11 — The mutable default trap

Show what goes wrong with `def add(item, bucket=[]): bucket.append(item); return bucket` when it is called twice without a bucket, then fix it.

*Hint:* Use `None` as the default and create the list inside.

---

Solutions: [part-5-solutions.md](solutions/part-5-solutions.md) · Back to the [practice index](README.md).
