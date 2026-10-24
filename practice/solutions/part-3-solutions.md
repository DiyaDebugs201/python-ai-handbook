# Part 3 — Solutions: Operators and Control Flow

> [Practice index](../README.md) · [Problems for this part](../part-3-exercises.md)

Every program below was run with Python 3.13 and the output shown is the real output. Your own solution may differ and still be correct: compare behaviour, not wording.

## P3.1 — FizzBuzz

For the numbers 1 to 15 print `Fizz` for multiples of 3, `Buzz` for multiples of 5, `FizzBuzz` for multiples of both, and the number otherwise.

```python
for n in range(1, 16):
    if n % 15 == 0:
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)
```

Output:

```text
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
```

The combined case must come first; otherwise multiples of 15 would match the `% 3` test and print only `Fizz`.

## P3.2 — Grade classifier

Write `grade(score)` returning `A` for 90 and above, `B` for 80 to 89, `C` for 70 to 79, `D` for 60 to 69 and `F` below 60. Print the grades for 95, 80, 79.5, 60 and 12.

```python
def grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    return "F"


print([grade(s) for s in (95, 80, 79.5, 60, 12)])
```

Output:

```text
['A', 'B', 'C', 'D', 'F']
```

Each `elif` only runs if the earlier tests failed, so each condition needs just a lower bound.

## P3.3 — Leap year

A year is a leap year if it is divisible by 4, except years divisible by 100, unless also divisible by 400. Test 1900, 2000, 2024 and 2026.

```python
def is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


for year in (1900, 2000, 2024, 2026):
    print(year, is_leap(year))
```

Output:

```text
1900 False
2000 True
2024 True
2026 False
```

The parentheses matter: the century exception applies only when the year is divisible by 4.

## P3.4 — Operator precedence

Predict, then compute: `2 + 3 * 4 ** 2 / 8`, `(2 + 3) * 4 ** 2 / 8`, `-3 ** 2`, `(-3) ** 2`, `not True or True`.

```python
print(2 + 3 * 4 ** 2 / 8)
print((2 + 3) * 4 ** 2 / 8)
print(-3 ** 2)
print((-3) ** 2)
print(not True or True)
```

Output:

```text
8.0
10.0
-9
9
True
```

`**` binds tightest, so `-3 ** 2` is `-(3 ** 2)`; `not` binds tighter than `or`, so the last line is `(not True) or True`.

## P3.5 — is versus ==

Create `a = [1, 2]`, `b = [1, 2]`, `c = a`. Print `a == b`, `a is b`, `a is c`. Then show that `None` should be compared with `is`.

```python
a = [1, 2]
b = [1, 2]
c = a
print(a == b, a is b, a is c)
value = None
print(value is None)
```

Output:

```text
True False True
True
```

`a` and `b` are equal but distinct objects; `c` is another name for the same object as `a`.

## P3.6 — Sum of digits

Use a `while` loop to compute the sum of the digits of 90871 without converting to a string.

```python
n = 90871
total = 0
while n > 0:
    total += n % 10
    n //= 10
print(total)
```

Output:

```text
25
```

Each pass adds the last digit and drops it, until nothing is left.

## P3.7 — Multiplication table

Print a 4 by 4 multiplication table with right-aligned columns of width 4, using nested loops.

```python
for row in range(1, 5):
    for col in range(1, 5):
        print(f"{row * col:>4}", end="")
    print()
```

Output:

```text
   1   2   3   4
   2   4   6   8
   3   6   9  12
   4   8  12  16
```

The inner loop prints a row without newlines; the bare `print()` ends each row.

## P3.8 — Primes with for/else

Print all prime numbers up to 30, using a `for ... else` with `break` for the divisibility test.

```python
primes = []
for n in range(2, 31):
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            break
    else:
        primes.append(n)
print(primes)
```

Output:

```text
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```

If a divisor is found the inner loop breaks and skips the `else`; otherwise the number is prime.

## P3.9 — break and continue

Given guesses `[5, 12, -1, 7, 42, 9]`, loop through them: skip negative numbers, stop at the first guess equal to 42, and print each guess that is processed. Then print how many were processed.

```python
guesses = [5, 12, -1, 7, 42, 9]
processed = 0
for guess in guesses:
    if guess < 0:
        continue
    if guess == 42:
        print("found 42, stopping")
        break
    print("processing", guess)
    processed += 1
print("processed:", processed)
```

Output:

```text
processing 5
processing 12
processing 7
found 42, stopping
processed: 3
```

`continue` jumps over the negative value; `break` stops the loop at 42 so 9 is never reached.

## P3.10 — Triangle pattern

Print a right triangle of stars with 5 rows (1 star in the first row, 5 in the last).

```python
for row in range(1, 6):
    print("*" * row)
```

Output:

```text
*
**
***
****
*****
```

String repetition builds each row; a nested loop would also work.

## P3.11 — Collatz steps

Starting from 27, repeat: if the number is even halve it, otherwise multiply by 3 and add 1, until it reaches 1. Print the number of steps.

```python
n = 27
steps = 0
while n != 1:
    n = n // 2 if n % 2 == 0 else 3 * n + 1
    steps += 1
print(steps)
```

Output:

```text
111
```

The conditional expression chooses the next value; the counter records how many times it was applied.

## P3.12 — Chained comparisons

Write `in_range(x)` that returns whether `x` is at least 10 and below 20 using a single chained comparison. Test 9, 10, 19 and 20.

```python
def in_range(x):
    return 10 <= x < 20


print([in_range(x) for x in (9, 10, 19, 20)])
```

Output:

```text
[False, True, True, False]
```

Chained comparisons read like mathematics and evaluate each side once.

---

Back to the [problems](../part-3-exercises.md) or the [practice index](../README.md).
