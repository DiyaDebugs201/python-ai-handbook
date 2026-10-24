# Chapter 11 — Operators Overview and Arithmetic Operators

> Part 3 — Operators and Control Flow · Video: 2:15:50–2:26:08 · Previous: [10 ord(), chr() and String Methods](10-ord-chr-and-string-methods.md) · Next: [12 Relational, Logical and Assignment Operators](12-relational-logical-assignment-operators.md)

**In this chapter:** what operators and operands are, the families of operators in Python, and the seven arithmetic operators `+`, `-`, `*`, `/`, `//`, `%` and `**`, including how division and remainder behave with negative numbers, how `divmod()` combines two of them, and which errors arithmetic can raise.

**Before you start:** you should know the number types `int` and `float` from [Numeric Types and Booleans](05-numeric-types-and-booleans.md) and how Python converts between them ([Type Conversion](08-type-conversion.md)). Recap: an `int` is a whole number of any size, a `float` is a decimal number stored in binary (so some decimal fractions are approximate), and `type()` tells you which one a value is. Examples were run with Python 3.13; arithmetic behaves the same in all Python 3 versions.

---

## Operators in Python: Overview

**Timestamp:** [2:15:50](https://www.youtube.com/watch?v=J9BI0jGOds8&t=8150s)

**Learning objectives:**

- Define operator, operand and expression, and tell unary from binary operators.
- Name the main families of Python operators and say what each is used for.
- Explain that evaluating an expression produces a value, and that some operators work on several types.

**1. Intuition**

An operator is a small symbol that tells Python to do something with the values next to it, the way `+` on a calculator adds two numbers. The values the operator works on are called operands. In `3 + 4`, the symbol `+` is the operator and `3` and `4` are the operands. The whole piece `3 + 4` is an expression: a combination that Python evaluates to a single value, here `7`.

**2. Why does it exist?**

Writing `add(3, 4)` for every sum would make programs long and hard to read. Operators give a short, familiar notation for the most common actions: arithmetic, comparing, combining conditions, assigning a value, checking identity or membership.

**3. Technical explanation**

An operator that takes two operands is *binary* (`a + b`). An operator that takes one operand is *unary* (`-a`, `not a`). Python has a ternary conditional expression (`x if condition else y`), which is covered in [Conditional Statements](14-conditional-statements.md).

The families of operators, and where this handbook covers them:

| Family | Operators | Purpose | Chapter |
|--------|-----------|---------|---------|
| Arithmetic | `+ - * / // % **` | calculate with numbers | this chapter |
| Relational (comparison) | `== != < > <= >=` | compare two values; result is `True` or `False` | [12](12-relational-logical-assignment-operators.md) |
| Logical | `and or not` | combine conditions | [12](12-relational-logical-assignment-operators.md) |
| Assignment | `= += -= *= /= //= %= **=` and others | store a value in a name | [12](12-relational-logical-assignment-operators.md) |
| Identity | `is`, `is not` | test whether two names refer to the same object | [13](13-identity-operators-and-precedence.md) |
| Membership | `in`, `not in` | test whether a value is inside a collection | used from [06](06-strings-basics-indexing-concatenation.md) onwards |
| Bitwise | `& \| ^ ~ << >>` | work on the binary digits of integers | not covered in detail; mentioned in [05](05-numeric-types-and-booleans.md) |

There is also `@` (matrix multiplication), used by numerical libraries such as NumPy; built-in types do not use it.

Many operators are *overloaded*: they do different but related jobs on different types. `+` adds numbers, joins strings (`"a" + "b"`) and joins lists (`[1] + [2]`). `*` multiplies numbers and repeats strings and lists (`"ab" * 3`). This works because each type defines what the operator means for it.

When an expression has several operators, Python decides the order by *precedence* (which operator goes first) and *associativity* (the direction when the operators have the same precedence). `2 + 3 * 4` is `14`, not `20`, because `*` has higher precedence than `+`. The full rules are in [Operator Precedence and Associativity](13-identity-operators-and-precedence.md#operator-precedence-and-associativity). Until then, use brackets whenever the order is not obvious.

**4. Syntax**

```text
operand operator operand     (binary)
operator operand             (unary)
```

This is a pattern, not runnable code. Brackets `( )` group a part of an expression so that it is evaluated first.

**5. Example 1 — Basic**

```python
print(7 + 3)
print(-7)
print("ab" + "cd")
print("ab" * 3)
print([1, 2] + [3])
print([0] * 4)
print(2 + 3 * 4)
print((2 + 3) * 4)
print(type(2 + 3), type(2 + 3.0), type(2 > 1))
```

Output:

```text
10
-7
abcd
ababab
[1, 2, 3]
[0, 0, 0, 0]
14
20
<class 'int'> <class 'float'> <class 'bool'>
```

Line by line:

- `7 + 3` is a binary use of `+`; `-7` is a unary use of `-`.
- The next four lines show overloading: strings and lists support `+` and `*` too.
- `2 + 3 * 4` multiplies first; the brackets in `(2 + 3) * 4` change the order.
- The last line shows that the result type depends on the operands: two ints give an int, an int and a float give a float, and a comparison gives a `bool`.

**6. Example 2 — Practical**

Operators in one realistic calculation: a bill with a discount, a membership check and a comparison.

```python
unit_price = 250
quantity = 4
discount_rate = 0.10
subtotal = unit_price * quantity
discount = subtotal * discount_rate
total = subtotal - discount

print("Subtotal:", subtotal)
print("Total:", total)
print("Free delivery:", total > 800)
print("Pays by card:", "card" in ["cash", "card", "upi"])
print("Valid:", total > 0 and quantity > 0)
```

Output:

```text
Subtotal: 1000
Total: 900.0
Free delivery: True
Pays by card: True
Valid: True
```

Line by line: `*` and `-` do the arithmetic, `>` compares, `in` tests membership in a list, and `and` combines two conditions (covered in [Relational, Logical and Assignment Operators](12-relational-logical-assignment-operators.md#logical-operators)). Every line is an expression that produces a value, which `print()` displays. Notice `total` is `900.0`: the discount rate is a float, so the result is a float.

**7. Example 3 — Edge case or common mistake**

Using an operator on types that do not support it is a runtime error:

```python
print("5" + 3)
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 1, in <module>
    print("5" + 3)
          ~~~~^~~
TypeError: can only concatenate str (not "int") to str
```

```python
print("5" * 3)
print(int("5") + 3)
print("5" + str(3))
```

Output:

```text
555
8
53
```

Python refuses to guess whether you meant the text `"53"` or the number `8`. Convert explicitly: `int("5") + 3` gives 8 and `"5" + str(3)` gives `"53"`. By contrast, `"5" * 3` is allowed (repetition), which is why a missing conversion sometimes produces a wrong answer without any error.

**8. Common mistakes**

- Mixing text and numbers with `+`.
- Relying on the order of evaluation instead of brackets.
- Confusing `=` (assign a value) with `==` (compare two values); see [Relational, Logical and Assignment Operators](12-relational-logical-assignment-operators.md).
- Forgetting that `+` and `*` change meaning for strings and lists.
- Assuming `^` means "power". In Python it is bitwise exclusive-or; power is `**`.

**9. Real-world and AI applications**

Operators build formulas: a loss function is arithmetic and comparison, a data filter is relational and logical operators, and a configuration check is membership. In AI libraries the same operators are overloaded to work on whole arrays: with NumPy or PyTorch, `a + b` adds two arrays element by element and `a @ b` multiplies matrices. Knowing operators on plain numbers is the foundation for reading that code.

**10. Practice**

1. Label the operator and operands in `(a + b) * 2` and say which operators are binary.
2. Predict `3 + 4 * 2`, `(3 + 4) * 2` and `"ha" * 3 + "!"`, then check.
3. Which families do these belong to: `==`, `and`, `//`, `in`, `is`, `+=`?
4. Write one expression that tests whether `n` is between 1 and 10 (inclusive), using relational and logical operators.

**11. Interview questions**

- *What is the difference between an operator and an operand?* The operator is the symbol that performs the action; the operands are the values it acts on.
- *What does it mean that `+` is overloaded?* It performs different related actions depending on the types: addition for numbers, concatenation for strings and lists.
- *What is operator precedence?* The rule that decides which operator is evaluated first when an expression has several.

**12. Quick revision**

- Operator = symbol; operand = value it acts on; expression = combination that produces a value.
- Unary operators have one operand, binary two.
- Families: arithmetic, relational, logical, assignment, identity, membership, bitwise.
- Operators behave differently on different types; mixing text and numbers with `+` is a `TypeError`.
- Use brackets when the order is not obvious.

---

## Arithmetic Operators

**Timestamp:** [2:17:59](https://www.youtube.com/watch?v=J9BI0jGOds8&t=8279s)

**Learning objectives:**

- Use `+`, `-`, `*`, `/`, `//`, `%` and `**` and predict the type of each result.
- Explain how `/`, `//` and `%` behave with negative numbers.
- Use `divmod()` and the rule `a == (a // b) * b + a % b`.
- Recognise `ZeroDivisionError` and floating-point rounding effects.

**1. Intuition**

The first four are the calculator keys you already know. The other three are the clever ones. `//` asks "how many whole times does the second number fit into the first?" (the quotient). `%` asks "what is left over after that?" (the remainder). `**` raises a number to a power. Dividing 17 sweets among 5 children: each child gets `17 // 5 = 3` sweets, and `17 % 5 = 2` sweets are left over.

**2. Why does it exist?**

Whole-number division with a remainder appears everywhere: converting seconds to hours, minutes and seconds; deciding whether a number is even or odd; wrapping around a fixed range (hours on a clock, positions in a circular buffer); splitting items into groups. Power appears in growth, areas and many formulas.

**3. Technical explanation**

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `+` | addition | `7 + 3` | `10` |
| `-` | subtraction | `7 - 3` | `4` |
| `*` | multiplication | `7 * 3` | `21` |
| `/` | true division | `7 / 2` | `3.5` |
| `//` | floor division | `7 // 2` | `3` |
| `%` | modulus (remainder) | `7 % 2` | `1` |
| `**` | exponentiation (power) | `2 ** 10` | `1024` |

*Result types.* `+`, `-`, `*`, `//`, `%` and `**` give an `int` when both operands are `int` (except `**` with a negative exponent, which gives a `float`), and a `float` if either operand is a `float`. The `/` operator always gives a `float`, even when the division is exact: `8 / 2` is `4.0`. Python integers have no fixed size limit, so `2 ** 100` is exact.

*Floor division.* `//` rounds the quotient *down* to the next smaller whole number (toward negative infinity), not toward zero. For positive numbers this looks like cutting off the decimals. For negative numbers it differs: `-7 // 2` is `-4`, not `-3`, because `-3.5` rounded down is `-4`.

*Modulus.* `a % b` is the remainder, defined so that `a == (a // b) * b + a % b` always holds. In Python the result of `%` has the same sign as the divisor `b`: `-7 % 3` is `2` (because `-7 = -3 * 3 + 2`), and `7 % -3` is `-2`. (Some other languages, such as C, give a different answer for negative numbers.) For positive numbers, `a % b` is always in the range `0` to `b - 1`.

*divmod.* `divmod(a, b)` is a built-in function returning the pair `(a // b, a % b)` in one step.

*Power.* `a ** b` raises `a` to the power `b`. `2 ** 0.5` is a square root; `2 ** -1` is `0.5`. The three-argument built-in `pow(base, exponent, modulus)` computes a remainder of a power efficiently, used in cryptography.

*Errors.* Division or remainder by zero raises `ZeroDivisionError` for both ints and floats (`1 / 0`, `1 // 0`, `1 % 0`, `1.0 / 0`). `0 ** -1` also raises it. Floats are approximate, so results such as `0.1 + 0.2` are slightly off, as explained in [The Float Data Type](05-numeric-types-and-booleans.md#the-float-data-type).

*Precedence preview.* `**` is applied before unary minus on its left (`-2 ** 2` is `-4`), then `*`, `/`, `//` and `%`, then `+` and `-`. `**` is right-associative: `2 ** 3 ** 2` is `2 ** (3 ** 2)`, which is `512`.

**4. Syntax**

```text
a + b    a - b    a * b    a / b    a // b    a % b    a ** b
-a       +a
divmod(a, b)     pow(a, b)     pow(a, b, modulus)
```

This is a pattern, not runnable code. `-a` and `+a` are unary operators. Spaces around operators are optional, but PEP 8 recommends one space on each side of most binary operators.

**5. Example 1 — Basic**

```python
a = 17
b = 5

print(a + b, a - b, a * b)
print(a / b)
print(a // b)
print(a % b)
print(a ** 2)
print(8 / 2, type(8 / 2))
print(2 ** 10, 2 ** 0.5, 2 ** -1)
print(2 ** 100)
print(divmod(a, b))
print(a == (a // b) * b + a % b)
```

Output:

```text
22 12 85
3.4
3
2
289
4.0 <class 'float'>
1024 1.4142135623730951 0.5
1267650600228229401496703205376
(3, 2)
True
```

Line by line:

- `a / b` is `3.4`, the exact quotient as a float.
- `a // b` is 3 (how many times 5 fits in 17) and `a % b` is 2 (what is left over).
- `8 / 2` is `4.0`, a float, because `/` always returns a float.
- `2 ** 0.5` is the square root of 2, and `2 ** -1` is a float.
- `2 ** 100` is a huge but exact integer.
- `divmod(17, 5)` returns both results as a pair.
- The last line confirms the rule that links the quotient and the remainder.

**6. Example 2 — Practical**

Four everyday jobs: time conversion, even and odd, digit extraction, and a wrap-around clock.

```python
total_seconds = 7384
hours, remainder = divmod(total_seconds, 3600)
minutes, seconds = divmod(remainder, 60)
print(f"{hours}h {minutes}m {seconds}s")

for number in [10, 7, 0, -3]:
    print(number, "even" if number % 2 == 0 else "odd")

number = 4729
last_digit = number % 10
remaining = number // 10
print(last_digit, remaining)

hour = 22
print((hour + 5) % 24)
print((3 - 5) % 12)

items = 23
per_box = 6
full_boxes = items // per_box
loose = items % per_box
boxes_needed = -(-items // per_box)
print(full_boxes, loose, boxes_needed)
```

Output:

```text
2h 3m 4s
10 even
7 odd
0 even
-3 odd
9 472
3
10
3 5 4
```

Line by line:

- `divmod(7384, 3600)` gives 2 hours and 184 seconds left over; `divmod(184, 60)` splits that into 3 minutes and 4 seconds.
- A number is even when the remainder after dividing by 2 is 0. This also works for `-3`, because Python's `%` gives a result with the sign of the divisor (`-3 % 2` is `1`).
- `number % 10` is the last digit and `number // 10` removes it. Repeating this takes a number apart digit by digit.
- `(hour + 5) % 24` wraps around a 24-hour clock: five hours after 22:00 is 03:00. `(3 - 5) % 12` is `10`, showing that `%` wraps negative numbers into the range too.
- `items // per_box` counts full boxes, and `items % per_box` counts what is left. The expression `-(-items // per_box)` is a well-known idiom that rounds the quotient *up* (ceiling division) using floor division on the negated number; here 4 boxes are needed for 23 items (3 full and 1 partly filled). `math.ceil(items / per_box)` does the same and is easier to read for most people.

**7. Example 3 — Edge case or common mistake**

Negative numbers with `//` and `%`, the effect of precedence, and floating-point surprises:

```python
print(-7 // 2, 7 // -2, -7 // -2)
print(-7 % 3, 7 % -3, -7 % -3)
print(int(-7 / 2))
print(-2 ** 2, (-2) ** 2)
print(2 ** 3 ** 2, (2 ** 3) ** 2)
print(0.1 + 0.2, 0.1 + 0.2 == 0.3)
print(7.5 // 2, 7.5 % 2, -7.5 // 2)
```

Output:

```text
-4 -4 3
2 -2 -1
-3
-4 4
512 64
0.30000000000000004 False
3.0 1.5 -4.0
```

What this shows:

- `-7 // 2` is `-4`, not `-3`: floor division goes down, not toward zero. `int(-7 / 2)` truncates toward zero and gives `-3`, so the two approaches are different. Choose deliberately.
- `-7 % 3` is `2` and `7 % -3` is `-2`: the sign follows the divisor.
- `-2 ** 2` is `-4` because `**` binds more tightly than the unary minus. `(-2) ** 2` is `4`.
- `2 ** 3 ** 2` is `512` because `**` groups from the right: `2 ** 9`.
- `0.1 + 0.2` is not exactly `0.3`; compare floats with `math.isclose` instead of `==`.
- `//` and `%` also work with floats, and the result of `//` is a float (`3.0`, not `3`).

Division by zero:

```python
print(10 / 0)
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 1, in <module>
    print(10 / 0)
          ~~~^~~
ZeroDivisionError: division by zero
```

```python
for expression in ["10 // 0", "10 % 0", "10.0 / 0", "0 ** -1"]:
    try:
        eval(expression)
    except ZeroDivisionError as error:
        print(f"{expression:10} -> {error}")
```

Output:

```text
10 // 0    -> integer division or modulo by zero
10 % 0     -> integer modulo by zero
10.0 / 0   -> float division by zero
0 ** -1    -> 0.0 cannot be raised to a negative power
```

Every form of division by zero raises `ZeroDivisionError`; only the message differs. (The loop uses `eval`, which runs a piece of text as an expression. It is used here only as a compact way to show four cases; do not use `eval` on text that a user typed, because it can run any code.) Guard against it with a condition, or catch the exception as shown in [Errors: Syntax vs Runtime](04-errors-and-identifiers.md#errors-syntax-vs-runtime).

**8. Common mistakes**

- Expecting `/` to give an integer. `10 / 2` is `5.0`; use `//` when you need a whole number.
- Expecting `//` on negative numbers to cut off the decimals. It rounds down.
- Using `^` for power; write `**`.
- Forgetting that `-x ** 2` is `-(x ** 2)`.
- Dividing by a value that can be zero without a check.
- Comparing floats with `==`.
- Using integer division on floats and being surprised by `3.0`.
- Writing `x % y` when `y` can be negative and assuming a non-negative result.

**9. Real-world and AI applications**

`divmod` and `%` drive calendars, clocks, pagination (page number from an item index: `index // page_size`), circular buffers, hashing and round-robin scheduling. In machine learning, training loops use `step % 100 == 0` to print a log line every 100 steps, `len(data) // batch_size` to count full batches (and `%` for the leftover items), and `**` in formulas such as squared error `(prediction - target) ** 2`. Learning-rate schedules such as exponential decay use `rate * decay ** step`. Float behaviour matters too: model outputs are floats, and tests compare them with a tolerance, not with `==`.

**10. Practice**

1. Compute `17 + 5`, `17 - 5`, `17 * 5`, `17 / 5`, `17 // 5`, `17 % 5` and `17 ** 2` and say which results are `int` and which are `float`.
2. Convert 100000 seconds into days, hours, minutes and seconds using `divmod`.
3. Write `is_even(n)` and `last_digit(n)`, and test on `10`, `7` and `-3`.
4. A school has 47 students and each bus holds 12. How many buses are needed? Write it with `//` and `%` and then with the ceiling idiom.
5. Predict `-9 // 4`, `-9 % 4`, `9 // -4` and `9 % -4`; verify with `a == (a // b) * b + a % b`.
6. Why does `0.1 * 3 == 0.3` give `False`, and how would you test it correctly?

**11. Interview questions**

- *What is the difference between `/` and `//`?* `/` is true division and always returns a float; `//` is floor division, rounding down to a whole number.
- *What does `%` return, and how does it treat negative numbers in Python?* The remainder, with the same sign as the divisor; `-7 % 3` is `2`.
- *What is `-7 // 2` and why?* `-4`, because floor division rounds toward negative infinity.
- *What does `**` do, and what is `2 ** 3 ** 2`?* Power; it is right-associative, so the result is `2 ** 9 = 512`.
- *Which exception does division by zero raise?* `ZeroDivisionError`.

**12. Quick revision**

- `+ - *` keep `int` when both are `int`; `/` always gives `float`; `//` floors; `%` is the remainder with the divisor's sign; `**` is power.
- `a == (a // b) * b + a % b` always holds; `divmod(a, b)` returns `(a // b, a % b)`.
- `-2 ** 2` is `-4`; `2 ** 3 ** 2` is `512`.
- Division or remainder by zero raises `ZeroDivisionError`.
- Floats are approximate; compare with `math.isclose`.

---

## Answers to Practice Exercises

### Answers: Operators in Python: Overview

1. In `(a + b) * 2`, `+` and `*` are the operators and are both binary. The operands of `+` are `a` and `b`; the operands of `*` are `(a + b)` and `2`. The brackets are not operators; they group.
2. `3 + 4 * 2` is `11`; `(3 + 4) * 2` is `14`; `"ha" * 3 + "!"` is `hahaha!` (repetition happens before joining).

```python
print(3 + 4 * 2)
print((3 + 4) * 2)
print("ha" * 3 + "!")
```

Output:

```text
11
14
hahaha!
```

3. `==` relational; `and` logical; `//` arithmetic; `in` membership; `is` identity; `+=` assignment.
4. `1 <= n <= 10` (chained comparison) or `n >= 1 and n <= 10`.

```python
for n in [0, 1, 10, 11]:
    print(n, 1 <= n <= 10, n >= 1 and n <= 10)
```

Output:

```text
0 False False
1 True True
10 True True
11 False False
```

### Answers: Arithmetic Operators

1.

```python
print(17 + 5, 17 - 5, 17 * 5)
print(17 / 5, 17 // 5, 17 % 5, 17 ** 2)
print(type(17 + 5), type(17 / 5), type(17 // 5), type(17 % 5), type(17 ** 2))
```

Output:

```text
22 12 85
3.4 3 2 289
<class 'int'> <class 'float'> <class 'int'> <class 'int'> <class 'int'>
```

Only `/` gives a float; everything else here is an `int` because both operands are ints.

2.

```python
seconds_total = 100000
days, rest = divmod(seconds_total, 86400)
hours, rest = divmod(rest, 3600)
minutes, seconds = divmod(rest, 60)
print(days, hours, minutes, seconds)
```

Output:

```text
1 3 46 40
```

3.

```python
def is_even(n):
    return n % 2 == 0


def last_digit(n):
    return abs(n) % 10


for value in [10, 7, -3]:
    print(value, is_even(value), last_digit(value))
```

Output:

```text
10 True 0
7 False 7
-3 False 3
```

`abs` makes `last_digit` give the digit of the number without its sign (without it, `-3 % 10` would be `7`, because of the sign rule for `%`).

4.

```python
students = 47
bus_size = 12

full_buses = students // bus_size
left_over = students % bus_size
buses_needed = full_buses + (1 if left_over > 0 else 0)
print(full_buses, left_over, buses_needed)
print(-(-students // bus_size))
```

Output:

```text
3 11 4
4
```

Three buses are full and 11 students are left, so a fourth bus is needed. The one-line idiom gives the same answer.

5.

```python
for a, b in [(-9, 4), (9, -4)]:
    q, r = a // b, a % b
    print(a, b, q, r, a == q * b + r)
```

Output:

```text
-9 4 -3 3 True
9 -4 -3 -3 True
```

`-9 // 4` is `-3` and `-9 % 4` is `3` (because `-9 = -3 * 4 + 3`). `9 // -4` is `-3` and `9 % -4` is `-3` (because `9 = -3 * -4 + -3`). The identity holds in both cases.

6. The float `0.1` has no exact binary representation, so `0.1 * 3` is `0.30000000000000004`, which is not equal to `0.3`. Use a tolerance:

```python
import math

print(0.1 * 3 == 0.3)
print(math.isclose(0.1 * 3, 0.3))
```

Output:

```text
False
True
```

---

## Chapter Summary and Key Takeaways

- An operator acts on operands to produce a value; operators come in families (arithmetic, relational, logical, assignment, identity, membership, bitwise) and many are overloaded across types.
- `+ - *` keep `int` for ints; `/` always returns `float`; `//` floors toward negative infinity; `%` gives a remainder with the sign of the divisor; `**` is right-associative power.
- `divmod(a, b)` gives `(a // b, a % b)`, and `a == (a // b) * b + a % b` always holds.
- `%` and `//` handle clocks, parity, digits, batches and wrap-around; the ceiling idiom is `-(-a // b)`.
- Division or remainder by zero raises `ZeroDivisionError`; floats are approximate, so compare them with a tolerance.

Next: [Chapter 12 — Relational, Logical and Assignment Operators](12-relational-logical-assignment-operators.md) covers comparisons, combining conditions and storing results.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
