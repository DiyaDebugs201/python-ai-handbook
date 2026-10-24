# Chapter 12 — Relational, Logical and Assignment Operators

> Part 3 — Operators and Control Flow · Video: 2:26:08–2:58:11 · Previous: [11 Operators Overview and Arithmetic Operators](11-arithmetic-operators.md) · Next: [13 Identity Operators and Operator Precedence](13-identity-operators-and-precedence.md)

**In this chapter:** the comparison operators (`==`, `!=`, `<`, `>`, `<=`, `>=`) and chained comparisons, the logical operators `and`, `or` and `not` including short-circuit evaluation and truthiness, and the assignment operators (`=`, augmented assignment such as `+=`, multiple assignment and swapping).

**Before you start:** you need the idea of an expression and an operator from [Operators in Python: Overview](11-arithmetic-operators.md#operators-in-python-overview), and the arithmetic operators from [Arithmetic Operators](11-arithmetic-operators.md#arithmetic-operators). Recap: the Boolean type `bool` has exactly two values, `True` and `False` (see [The Boolean Data Type](05-numeric-types-and-booleans.md#the-boolean-data-type)), and strings compare by their Unicode code points (see [Strings Revisited: ord() and chr()](10-ord-chr-and-string-methods.md#strings-revisited-ord-and-chr)). Examples were run with Python 3.13; the behaviour described is the same in all current Python 3 versions unless stated.

---

## Relational Operators

**Timestamp:** [2:26:08](https://www.youtube.com/watch?v=J9BI0jGOds8&t=8768s)

**Learning objectives:**

- Use the six relational operators and predict that each produces `True` or `False`.
- Write and evaluate chained comparisons such as `0 < x < 10`.
- Compare numbers, strings, lists and mixed types, and know when a comparison raises `TypeError`.
- Avoid the classic mistakes: `=` versus `==`, comparing floats exactly, and comparing to `None` with `==`.

**1. Intuition**

A relational operator asks a yes/no question about two values: "Are these equal?", "Is this one bigger?". The answer is always a Boolean value, `True` or `False`. These answers are what programs use to make decisions, as you will see in [Conditional Statements](14-conditional-statements.md).

**2. Why does it exist?**

A program that cannot compare things cannot choose between actions: it cannot check a password, find the largest value, test whether a number is in range or stop a loop at the right time. Comparison is the basis of every decision.

**3. Technical explanation**

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `==` | equal to | `5 == 5` | `True` |
| `!=` | not equal to | `5 != 3` | `True` |
| `<` | less than | `3 < 5` | `True` |
| `>` | greater than | `3 > 5` | `False` |
| `<=` | less than or equal to | `5 <= 5` | `True` |
| `>=` | greater than or equal to | `4 >= 5` | `False` |

*Equality (`==`) versus assignment (`=`).* A single `=` stores a value in a name; a double `==` compares two values. Writing `if x = 5:` is a syntax error in Python (which prevents a classic bug found in some other languages).

*What can be compared.*

- Numbers compare by value across types: `1 == 1.0` is `True`, and `True == 1` is `True` because `bool` is a kind of `int`.
- Strings compare character by character using code points (so `"apple" < "banana"` and `"Zebra" < "apple"` are both `True`).
- Lists and tuples compare element by element from the left, like words in a dictionary: `[1, 2, 3] < [1, 2, 4]` is `True`; if all common elements are equal, the shorter one is smaller.
- `==` between unrelated types, such as `5 == "5"`, simply gives `False`. The ordering operators `<`, `>`, `<=` and `>=` between unrelated types, such as `5 < "5"`, raise `TypeError`.
- Two different objects can be equal (`[1, 2] == [1, 2]` is `True`). Equality is about value, not about being the same object (identity is covered in [Identity Operators: is versus Equality](13-identity-operators-and-precedence.md#identity-operators-is-versus-equality)).

*Chained comparisons.* Python lets you write `a < b < c`. It means `a < b and b < c`, except that `b` is evaluated only once. This reads like mathematics: `0 <= score <= 100`. You can chain any number of comparisons, with mixed operators, such as `a < b == c`.

*Floating-point numbers.* Floats are stored in binary, so results of arithmetic can be slightly off, and `0.1 + 0.2 == 0.3` is `False`. Use `math.isclose(a, b)` to compare floats (see [The Float Data Type](05-numeric-types-and-booleans.md#the-float-data-type)). A special float, `nan` ("not a number"), is not equal even to itself.

*Comparing with `None`.* `None` is a unique object that means "no value". The recommended test is `x is None`, not `x == None` (see the identity chapter). `None` cannot be ordered against numbers: `None < 5` raises `TypeError`.

**4. Syntax**

```text
left_operand operator right_operand
a < b < c               # chained comparison
```

This is a pattern, not runnable code. The result is a `bool`.

**5. Example 1 — Basic**

```python
a = 10
b = 20

print(a == b, a != b)
print(a < b, a > b)
print(a <= 10, b >= 25)
print("apple" == "apple", "apple" < "banana", "Zebra" < "apple")
print(1 == 1.0, True == 1, 5 == "5")
print([1, 2, 3] < [1, 2, 4], (1, 2) < (1, 2, 0), [1, 2] == [1, 2])
print(type(a < b))
```

Output:

```text
False True
True False
True False
True True True
True True False
True True True
<class 'bool'>
```

Line by line:

- The first four lines show the basic operators; each result is a `bool`.
- `"Zebra" < "apple"` is `True` because capital letters have smaller code points than small letters.
- `1 == 1.0` and `True == 1` are `True` (numbers compare by value), but `5 == "5"` is `False` (a number is never equal to a string).
- The list comparison is element by element: the first difference (3 versus 4) decides. The tuple `(1, 2)` is smaller than `(1, 2, 0)` because it is a prefix of it.
- `type(a < b)` confirms the result is a `bool`.

**6. Example 2 — Practical**

Range checks and grading with chained comparisons, and comparing user data:

```python
def grade(score):
    if not 0 <= score <= 100:
        return "invalid"
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 40:
        return "C"
    return "F"


for mark in [95, 80, 40, 39, 101, -5]:
    print(mark, grade(mark))

age = 17
print("Adult:", age >= 18)
print("Teen:", 13 <= age < 20)

stored_password = "Secret#1"
typed_password = "secret#1"
print("Match:", stored_password == typed_password)
print("Match ignoring case:", stored_password.lower() == typed_password.lower())
```

Output:

```text
95 A
80 B
40 C
39 F
101 invalid
-5 invalid
Adult: False
Teen: True
Match: False
Match ignoring case: True
```

Line by line:

- `0 <= score <= 100` is a chained comparison that checks for a valid range in one expression. `not` reverses it (see [Logical Operators](#logical-operators)).
- The `if` statements run from the top, so the first true test decides the grade (the statement is explained in [Conditional Statements](14-conditional-statements.md)).
- `13 <= age < 20` mixes `<=` and `<`, which is allowed.
- String comparison with `==` is case-sensitive, so `"Secret#1" == "secret#1"` is `False`. Lower-casing both sides gives a case-insensitive comparison.

**7. Example 3 — Edge case or common mistake**

Four traps:

```python
print(0.1 + 0.2 == 0.3)

import math
print(math.isclose(0.1 + 0.2, 0.3))

nan = float("nan")
print(nan == nan, nan != nan)

print(1 < 2 < 3, 1 < 3 < 2, 3 > 2 > 1)
print(1 == 1 == 1.0)
```

Output:

```text
False
True
False True
True False True
True
```

```python
print(5 < "5")
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 1, in <module>
    print(5 < "5")
          ^^^^^^^
TypeError: '<' not supported between instances of 'int' and 'str'
```

```text
x = 5
if x = 5:
    print("five")
```

This is not valid Python; it raises a syntax error:

```text
  File "example.py", line 2
    if x = 5:
       ^^^^^
SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
```

What happened:

- `0.1 + 0.2 == 0.3` is `False` because of binary rounding; `math.isclose` returns `True` (it uses a small relative tolerance, which you can change).
- `nan` is not equal to anything, not even itself, so `nan == nan` is `False` and `nan != nan` is `True`. The standard function `math.isnan` tests for it.
- Chained comparisons work like mathematics: `1 < 3 < 2` is `False` because `3 < 2` is `False`.
- `5 < "5"` is a `TypeError`, because Python will not guess how to order a number against text. Convert one side first (`5 < int("5")`).
- `if x = 5:` is rejected before the program runs, and the message suggests `==`. Note that it also mentions `:=`, the "walrus" operator covered under assignment below.

Also remember that `x == None` works but is discouraged; write `x is None`.

**8. Common mistakes**

- Using `=` where `==` is meant, in a condition.
- Comparing floats with `==`; use `math.isclose`.
- Comparing text that looks like a number with a real number (`"10" < "9"` is `True` as text, but `10 < 9` is `False` as numbers).
- Expecting `5 == "5"` to be `True`.
- Writing `a < b and b < c` as `a < b < c` is fine, but writing `a == b == c` and expecting it to mean "all different" is a mistake: it means all equal.
- Comparing with `None` using `==`.
- Thinking that comparing two lists with `<` compares their lengths. It compares element by element.

**9. Real-world and AI applications**

Comparisons drive validation (age limits, password length), search and sorting, loop conditions, retry limits and thresholds. In machine learning code, a model's score is compared to a threshold (`probability >= 0.5` becomes a class label), validation loss is compared to the best loss so far to decide whether to save a model, and test code compares float results with a tolerance (`math.isclose`, or `numpy.isclose` for arrays). Data filters such as "rows where age is greater than 30" are relational operators applied to whole columns in libraries like pandas.

**10. Practice**

1. Predict the results of `3 == 3.0`, `"3" == 3`, `"a" < "b"`, `[2] > [1, 9]` and `(1, 2) == (1, 2)`; then run them.
2. Write a function `is_teen(age)` using a chained comparison (13 to 19 inclusive).
3. Write a function `classify_triangle(a, b, c)` that returns `"equilateral"`, `"isosceles"` or `"scalene"`, using `==` comparisons.
4. Why does `0.1 * 3 == 0.3` fail, and how would you compare these two numbers correctly?
5. What does `1 < x < 5` do when `x` is `3`? When `x` is `7`? Rewrite it without chaining.

**11. Interview questions**

- *What is the difference between `=` and `==`?* `=` assigns a value to a name; `==` compares two values and returns `True` or `False`.
- *How does Python evaluate `a < b < c`?* As `a < b and b < c`, with `b` evaluated once.
- *Can you compare a string and an integer?* `==` returns `False`; ordering operators raise `TypeError`.
- *Why should floats not be compared with `==`?* Binary rounding makes results approximate; use a tolerance such as `math.isclose`.

**12. Quick revision**

- `== != < > <= >=` give `True` or `False`.
- `=` assigns, `==` compares.
- Chained comparisons (`0 <= x <= 100`) mean "all comparisons are true".
- Strings compare by code point; lists and tuples compare element by element.
- `==` across unrelated types is `False`; ordering across unrelated types is `TypeError`.
- Compare floats with `math.isclose`; compare to `None` with `is None`.

---

## Logical Operators

**Timestamp:** [2:43:46](https://www.youtube.com/watch?v=J9BI0jGOds8&t=9826s)

**Learning objectives:**

- Use `and`, `or` and `not` to combine conditions.
- Explain truthiness: which values count as false and which as true.
- Explain short-circuit evaluation and that `and` / `or` return one of their operands, not always a `bool`.
- Use `or` for defaults, and recognise when that pattern fails.

**1. Intuition**

Logical operators combine yes/no answers, as in everyday language. "You may enter if you have a ticket **and** you are over 12." "You may pay with cash **or** card." "The door is **not** locked." `and` needs both sides true, `or` needs at least one side true, and `not` flips the answer.

**2. Why does it exist?**

Real decisions depend on several conditions at once. Without logical operators you would need nested decisions for every combination.

**3. Technical explanation**

Truth tables for two conditions `A` and `B`:

| A | B | `A and B` | `A or B` | `not A` |
|---|---|-----------|----------|---------|
| True | True | True | True | False |
| True | False | False | True | False |
| False | True | False | True | True |
| False | False | False | False | True |

*Truthiness.* Any value can be used where a condition is expected. Python treats these as *false* ("falsy"): `False`, `None`, the number zero (`0`, `0.0`, `0j`), and empty collections and strings (`""`, `[]`, `()`, `{}`, `set()`, `range(0)`). Everything else is *true* ("truthy"), including `"0"`, `"False"`, `" "` and `[0]`. You can check any value with `bool(value)`.

*What `and` and `or` return.* They do not always return `True` or `False`; they return one of the operands:

- `A and B`: if `A` is falsy, the result is `A` (and `B` is not even looked at); otherwise the result is `B`.
- `A or B`: if `A` is truthy, the result is `A` (and `B` is not looked at); otherwise the result is `B`.
- `not A` always returns a real `bool`.

*Short-circuit evaluation.* Because the second operand is skipped when the first one already decides the answer, `and` and `or` can protect a risky operation: `y != 0 and x / y > 2` never divides when `y` is zero. It also means that function calls on the right may not run at all.

*Precedence.* `not` binds tighter than `and`, which binds tighter than `or`. So `a or b and c` means `a or (b and c)`. Use brackets to make your intention clear.

*Useful laws (De Morgan).* `not (A and B)` equals `(not A) or (not B)`, and `not (A or B)` equals `(not A) and (not B)`.

*Do not confuse with bitwise operators.* `&` and `|` work on the binary digits of integers (and on sets); they are not the same as `and` and `or`, and they do not short-circuit.

**4. Syntax**

```text
condition1 and condition2
condition1 or condition2
not condition
```

This is a pattern, not runnable code. Each condition can be any expression.

**5. Example 1 — Basic**

```python
age = 25
has_ticket = True

print(age > 18 and has_ticket)
print(age < 18 or has_ticket)
print(not has_ticket)
print(not (age > 18 and has_ticket))

print(bool(0), bool(1), bool(-3), bool(0.0))
print(bool(""), bool(" "), bool("0"), bool("False"))
print(bool([]), bool([0]), bool({}), bool(None))
```

Output:

```text
True
True
False
False
False True True False
False True True True
False True False False
```

Line by line:

- The first four lines show `and`, `or`, and `not` on real conditions.
- The `bool(...)` lines list falsy and truthy values: `0` and `0.0` are false, but `-3` is true. An empty string is false, but `" "` (a space) and `"0"` and `"False"` are true because they are not empty. `[0]` is a non-empty list, so it is true.

**6. Example 2 — Practical**

Short-circuiting, returning operands, and the default-value pattern:

```python
def check(label, value):
    print("checking", label)
    return value


print(check("A", False) and check("B", True))
print(check("C", True) or check("D", False))
print(check("E", True) and check("F", True))
print()

x, y = 10, 0
print(y != 0 and x / y > 2)

print(0 and 5, 3 and 5, "" or "default", "hello" or "default")
print([] or "empty list", None or 0 or "last resort")

username = ""
display_name = username or "Guest"
print(display_name)

is_weekend = False
is_holiday = True
print(is_weekend or is_holiday)
```

Output:

```text
checking A
False
checking C
True
checking E
checking F
True

False
0 5 default hello
empty list last resort
Guest
True
```

Line by line:

- `check("A", False) and check("B", True)`: `A` is false, so the answer is already known and `B` is never checked. Only `checking A` is printed, and the result is `False`.
- `check("C", True) or check("D", False)`: `C` is true, so `D` is skipped.
- With `and` and two true values, both sides run and the result is the last operand.
- `y != 0 and x / y > 2` is safe: when `y` is `0`, the division never happens.
- `0 and 5` is `0` (the first falsy operand), `3 and 5` is `5` (the last operand), `"" or "default"` is `"default"` (the first truthy operand), and `None or 0 or "last resort"` skips two falsy values and returns the last one.
- `username or "Guest"` supplies a default when the string is empty.

**7. Example 3 — Edge case or common mistake**

The default-value trick treats every falsy value as "missing", which is wrong when `0` or an empty string is a legal value:

```python
def describe_volume(volume):
    level = volume or 50
    return f"volume is {level}"


print(describe_volume(30))
print(describe_volume(None))
print(describe_volume(0))
```

Output:

```text
volume is 30
volume is 50
volume is 50
```

A user who sets the volume to `0` (silent) gets `50` instead. Compare with `None` explicitly:

```python
def describe_volume(volume):
    level = 50 if volume is None else volume
    return f"volume is {level}"


print(describe_volume(30))
print(describe_volume(None))
print(describe_volume(0))
```

Output:

```text
volume is 30
volume is 50
volume is 0
```

Another classic mistake is the misplaced `or`. This test looks right in English ("color is red or blue") but is always true:

```python
color = "green"

print(color == "red" or "blue")
print(color == "red" or color == "blue")
print(color in ("red", "blue"))
```

Output:

```text
blue
False
False
```

The first line parses as `(color == "red") or "blue"`. The left side is `False`, so the result is the non-empty string `"blue"`, which is truthy, so an `if` using it would always run. The second and third lines are correct; the third (membership test) is the shortest when there are several options.

Precedence and De Morgan:

```python
a, b, c = True, False, True

print(a or b and c, (a or b) and c)
print(not a or b, not (a or b))
print((not (a and b)) == (not a or not b))
```

Output:

```text
True True
False False
True
```

`a or b and c` means `a or (b and c)`. The last line confirms one of De Morgan's laws for these values (the extra brackets are needed, because `==` binds more tightly than `not`).

**8. Common mistakes**

- Writing `x == 1 or 2` when you mean `x == 1 or x == 2` (or `x in (1, 2)`).
- Using `or` for defaults when `0`, `""` or `[]` are valid values.
- Using `&` and `|` instead of `and` and `or` for conditions; they do not short-circuit and have different precedence.
- Forgetting that `and` / `or` return operands, which may not be `True` / `False`, when the result is stored or printed.
- Mixing `and` and `or` without brackets.
- Relying on a side effect (such as a function call that prints) in the right operand, which might not run.
- Testing `if x == True:`; write `if x:`.

**9. Real-world and AI applications**

Logical operators combine validation rules (`len(password) >= 8 and any_digit`), permission checks and feature flags. The `value or default` pattern and its safer form are common when reading settings. Short-circuiting protects against errors such as a missing field (`record and record.get("id")`). In data and AI work, filters like `(age > 30) & (city == "Pune")` use the bitwise `&` operator with brackets in pandas and NumPy, because those libraries overload `&`, `|` and `~` to work element by element; plain `and` and `or` do not work on whole columns. Knowing that difference prevents a common error message.

**10. Practice**

1. Predict `True and False or True`, `not True or True`, `0 or "" or None`, and `3 and 4 and 5`; then run them.
2. Write `can_vote(age, is_citizen)` that is true when the age is at least 18 and the person is a citizen.
3. Write `is_valid_username(name)` that is true when the name is 3 to 12 characters long and consists only of letters and digits (hint: `isalnum()`).
4. Write `leap_year(year)`: true if divisible by 4 and not by 100, or divisible by 400. Test `1900`, `2000`, `2024`, `2023`.
5. Explain what `print(x and x.upper())` does when `x` is `""` and when it is `"hi"`.

**11. Interview questions**

- *What is short-circuit evaluation?* The right operand of `and` / `or` is evaluated only if the left operand does not already decide the result.
- *What does `"" or "default"` return?* `"default"`; `or` returns the first truthy operand or the last operand.
- *Which values are falsy in Python?* `False`, `None`, zero of any numeric type, and empty strings and collections.
- *What is the difference between `and` and `&`?* `and` is a logical operator that works on truthiness and short-circuits; `&` is bitwise (and element-wise on sets and arrays).

**12. Quick revision**

- `and` needs both true, `or` needs one true, `not` flips.
- Falsy: `False`, `None`, `0`, `0.0`, `""`, `[]`, `()`, `{}`, `set()`; everything else is truthy.
- `and` / `or` return an operand and short-circuit; `not` returns a `bool`.
- Precedence: `not`, then `and`, then `or`; use brackets.
- Prefer `x is None` for missing values and `x in (a, b)` for several options.

---

## Assignment Operators

**Timestamp:** [2:53:03](https://www.youtube.com/watch?v=J9BI0jGOds8&t=10383s)

**Learning objectives:**

- Explain what assignment does: it binds a name to an object.
- Use augmented assignment operators (`+=`, `-=`, `*=`, `/=`, `//=`, `%=`, `**=`).
- Use multiple assignment, unpacking and swapping.
- Explain the difference between `x += y` and `x = x + y` for lists, and the trap of `a = b = []`.

**1. Intuition**

Assignment attaches a name tag to a value. `score = 90` does not put 90 inside a box called `score`; it sticks the label `score` onto the number 90. Another label can be stuck on the same value, and a label can be moved to another value later. The operators `+=`, `-=` and friends are shortcuts for "take the value this label is on, do some arithmetic, and put the label on the result".

**2. Why does it exist?**

A program has to remember results. Updating a value from its own old value ("add 1 to the counter", "subtract the fee from the balance") is so common that Python has a shorter way of writing it.

**3. Technical explanation**

*Simple assignment.* `name = expression` first evaluates the expression on the right, then binds the name on the left to the resulting object. If the name already existed, it is rebound; the old value is not changed. Assignment is a statement, not an expression, so you cannot use it inside a larger expression (except with `:=`, below).

*Augmented assignment.* `x += 3` is shorthand for `x = x + 3`: the operator is applied, and the result is bound to the name.

| Operator | Same as |
|----------|---------|
| `x += y` | `x = x + y` |
| `x -= y` | `x = x - y` |
| `x *= y` | `x = x * y` |
| `x /= y` | `x = x / y` |
| `x //= y` | `x = x // y` |
| `x %= y` | `x = x % y` |
| `x **= y` | `x = x ** y` |

There are also `&=`, `|=`, `^=`, `<<=` and `>>=` for bitwise operations. The name must already exist: `count += 1` before `count` is defined raises `NameError` (or `UnboundLocalError` inside a function).

*One difference to know.* For mutable objects such as lists, `x += y` may change the existing object in place instead of creating a new one: with lists, `x += [1]` extends the list that `x` refers to, while `x = x + [1]` builds a new list and moves the label. This matters when two names refer to the same list (see [Copying Lists](19-list-functions-methods-and-copying.md#copying-lists)). For numbers and strings, which are immutable, both forms create a new object.

*Multiple assignment.*

- Chained: `a = b = 0` binds both names to the same object.
- Tuple (parallel) assignment: `a, b = 1, 2` evaluates the right side first, then assigns in order. This makes swapping easy: `a, b = b, a`.
- Unpacking: `first, second, third = [10, 20, 30]` needs exactly as many names as items. A starred name collects the rest: `first, *rest = [1, 2, 3, 4]` gives `rest == [2, 3, 4]`.

*The walrus operator.* Python 3.8 added `:=`, which assigns inside an expression (`if (n := len(items)) > 3:`). It is useful but rarely needed by beginners.

**4. Syntax**

```text
name = expression
name += expression            # and -=, *=, /=, //=, %=, **=
name1 = name2 = expression    # chained
name1, name2 = expr1, expr2   # parallel
first, *rest = iterable       # unpacking with a star
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
score = 50
score += 10
print(score)
score -= 5
print(score)
score *= 2
print(score)
score /= 4
print(score)
score //= 3
print(score)
score **= 2
print(score)
score %= 5
print(score)

text = "Hi"
text += " there"
text *= 2
print(text)
```

Output:

```text
60
55
110
27.5
9.0
81.0
1.0
Hi thereHi there
```

Line by line: `50 + 10 = 60`, minus 5 is 55, doubled is 110, divided by 4 is 27.5 (note: `/=` turns it into a float), floor-divided by 3 is 9.0, squared is 81.0, and `81.0 % 5` is 1.0. Strings support `+=` (joining) and `*=` (repeating). Because strings are immutable, each `+=` creates a new string and rebinds the name.

**6. Example 2 — Practical**

Counters, running totals, swapping, unpacking and a simple bank balance:

```python
balance = 1000
deposit = 250
fee = 15
balance += deposit
balance -= fee
print(balance)

total = 0
count = 0
for mark in [72, 58, 91, 66, 85]:
    total += mark
    count += 1
print(total, count, total / count)

a, b = 3, 8
a, b = b, a
print(a, b)

point = (4, 7)
x, y = point
print(x, y)

first, *middle, last = [1, 2, 3, 4, 5]
print(first, middle, last)

width = height = 5
print(width * height)

name, age, city = "Asha,27,Mysuru".split(",")
print(name, int(age), city)
```

Output:

```text
1235
372 5 74.4
8 3
4 7
1 [2, 3, 4] 5
25
Asha 27 Mysuru
```

Line by line:

- `balance += deposit` and `balance -= fee` update the same name step by step.
- The loop accumulates a running total and a counter with `+=`. This accumulator pattern is one of the most common in programming.
- `a, b = b, a` swaps two values without a temporary variable: the right side `(b, a)` is built first, and then the names are assigned.
- Unpacking splits a tuple into names; `first, *middle, last` captures the ends and collects everything in between into a list.
- `width = height = 5` binds both names to the number 5, which is safe because numbers are immutable.
- `split(",")` returns a list of three strings that are unpacked into three names.

**7. Example 3 — Edge case or common mistake**

Chained assignment with a mutable object, and `+=` on lists:

```python
a = b = []
a.append(1)
print(a, b)
print(a is b)

c = []
d = []
c.append(1)
print(c, d)

x = [1, 2]
y = x
x += [3]
print(x, y)

p = [1, 2]
q = p
p = p + [3]
print(p, q)
```

Output:

```text
[1] [1]
True
[1] []
[1, 2, 3] [1, 2, 3]
[1, 2, 3] [1, 2]
```

What happened:

- `a = b = []` binds both names to one single list. Appending through `a` is visible through `b`, because there is only one list. `a is b` is `True`.
- `c = []` and `d = []` create two separate lists.
- `x += [3]` changed the list that both `x` and `y` refer to, so `y` also shows `[1, 2, 3]`.
- `p = p + [3]` built a new list and moved the name `p` to it, so `q` still refers to the old, unchanged list.

Using an undefined name in an augmented assignment, and unpacking the wrong number of values:

```python
total += 5
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 1, in <module>
    total += 5
    ^^^^^
NameError: name 'total' is not defined
```

```python
first, second = [1, 2, 3]
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 1, in <module>
    first, second = [1, 2, 3]
    ^^^^^^^^^^^^^
ValueError: too many values to unpack (expected 2)
```

```python
first, second, third = [1, 2]
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 1, in <module>
    first, second, third = [1, 2]
    ^^^^^^^^^^^^^^^^^^^^
ValueError: not enough values to unpack (expected 3, got 2)
```

`+=` reads the old value first, so the name must already exist. Unpacking requires the number of names to match the number of values (unless a starred name takes the rest).

**8. Common mistakes**

- Using a variable in `+=` before giving it a first value.
- Writing `x =+ 1` (which means "assign positive one") when `x += 1` is meant.
- Assuming `a = b = []` creates two lists.
- Forgetting that `/=` always produces a float.
- Writing `x = x + 1` inside a function that only reads a global `x`, and getting `UnboundLocalError` (see [Variable Scope](27-variable-scope.md)).
- Unpacking with the wrong number of names.
- Believing that `=` copies a list. It only adds another name for the same list.

**9. Real-world and AI applications**

Accumulators with `+=` are everywhere: counting rows, summing losses over a training epoch (`running_loss += loss`), tracking the best score so far, and building strings or lists step by step. Parallel assignment and unpacking appear when functions return several values (`train_x, test_x = split(data)`) and in loops over pairs (`for name, score in results`). The aliasing behaviour in Example 3 is one of the most common sources of subtle bugs in data code, for example when a default list or a data structure is shared by mistake.

**10. Practice**

1. Start with `x = 10`; apply `x += 5`, `x *= 3`, `x -= 7`, `x //= 4`, `x **= 2` and print `x` after each step.
2. Swap two variables without a temporary variable. Then rotate three: after `a, b, c = 1, 2, 3`, make `a = 2, b = 3, c = 1` in one statement.
3. Write a loop that computes the sum and the product of `[2, 3, 4, 5]` using `+=` and `*=`.
4. Unpack `[10, 20, 30, 40, 50]` into `head`, `tail` (all but the first) using a starred name.
5. What does this print? `a = [1, 2]`, `b = a`, `b += [3]`, `print(a)`. Then change `b += [3]` to `b = b + [3]` and explain the difference.

**11. Interview questions**

- *What does `x += 1` do?* It adds one to `x` and rebinds `x` to the result; it is shorthand for `x = x + 1` (with a subtle in-place difference for mutable types such as lists).
- *How do you swap two variables in Python?* `a, b = b, a`.
- *What is the difference between `x += [1]` and `x = x + [1]` for a list?* The first extends the existing list in place; the second builds a new list and rebinds `x`.
- *What happens with `a = b = []`?* Both names refer to the same list object.

**12. Quick revision**

- Assignment binds a name to an object; the right side is evaluated first.
- `+=`, `-=`, `*=`, `/=`, `//=`, `%=`, `**=` update a name from its old value; `/=` gives a float.
- Parallel assignment and unpacking: `a, b = b, a`; `first, *rest = items`.
- `a = b = []` shares one list; `x += [1]` mutates in place; `x = x + [1]` makes a new list.
- A name must exist before `+=` can use it.

---

## Answers to Practice Exercises

### Answers: Relational Operators

1. `3 == 3.0` is `True`; `"3" == 3` is `False`; `"a" < "b"` is `True`; `[2] > [1, 9]` is `True` (the first elements decide: 2 is larger than 1); `(1, 2) == (1, 2)` is `True`.

```python
print(3 == 3.0, "3" == 3, "a" < "b", [2] > [1, 9], (1, 2) == (1, 2))
```

Output:

```text
True False True True True
```

2.

```python
def is_teen(age):
    return 13 <= age <= 19


print(is_teen(12), is_teen(13), is_teen(19), is_teen(20))
```

Output:

```text
False True True False
```

3.

```python
def classify_triangle(a, b, c):
    if a == b == c:
        return "equilateral"
    if a == b or b == c or a == c:
        return "isosceles"
    return "scalene"


print(classify_triangle(3, 3, 3))
print(classify_triangle(3, 3, 5))
print(classify_triangle(3, 4, 5))
```

Output:

```text
equilateral
isosceles
scalene
```

4. `0.1 * 3` is `0.30000000000000004` in binary floating point, so it is not equal to `0.3`. Compare with a tolerance:

```python
import math

print(0.1 * 3)
print(0.1 * 3 == 0.3)
print(math.isclose(0.1 * 3, 0.3))
```

Output:

```text
0.30000000000000004
False
True
```

5. For `x = 3`, `1 < x < 5` is `True`; for `x = 7` it is `False`. Without chaining: `1 < x and x < 5`.

```python
for x in [3, 7]:
    print(x, 1 < x < 5, 1 < x and x < 5)
```

Output:

```text
3 True True
7 False False
```

### Answers: Logical Operators

1. `True and False or True` is `True` (`and` first: `False`, then `False or True`). `not True or True` is `True` (`not True` is `False`; `False or True`). `0 or "" or None` is `None` (all are falsy, so the last operand is returned). `3 and 4 and 5` is `5`.

```python
print(True and False or True)
print(not True or True)
print(0 or "" or None)
print(3 and 4 and 5)
```

Output:

```text
True
True
None
5
```

2.

```python
def can_vote(age, is_citizen):
    return age >= 18 and is_citizen


print(can_vote(20, True), can_vote(20, False), can_vote(16, True))
```

Output:

```text
True False False
```

3.

```python
def is_valid_username(name):
    return 3 <= len(name) <= 12 and name.isalnum()


for candidate in ["ab", "diya99", "diya_99", "a" * 13]:
    print(repr(candidate), is_valid_username(candidate))
```

Output:

```text
'ab' False
'diya99' True
'diya_99' False
'aaaaaaaaaaaaa' False
```

`isalnum()` is `False` if the text contains an underscore, a space or a symbol.

4.

```python
def leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0


for year in [1900, 2000, 2024, 2023]:
    print(year, leap_year(year))
```

Output:

```text
1900 False
2000 True
2024 True
2023 False
```

5. When `x` is `""` (falsy), `x and x.upper()` returns `""` immediately and never calls `upper()`. When `x` is `"hi"` (truthy), it returns the right operand, `"HI"`. It is a compact "do this only if there is a value" pattern, but an `if` statement is clearer for beginners.

```python
for x in ["", "hi"]:
    print(repr(x and x.upper()))
```

Output:

```text
''
'HI'
```

### Answers: Assignment Operators

1.

```python
x = 10
x += 5
print(x)
x *= 3
print(x)
x -= 7
print(x)
x //= 4
print(x)
x **= 2
print(x)
```

Output:

```text
15
45
38
9
81
```

2.

```python
a, b = 1, 2
a, b = b, a
print(a, b)

a, b, c = 1, 2, 3
a, b, c = b, c, a
print(a, b, c)
```

Output:

```text
2 1
2 3 1
```

3.

```python
total = 0
product = 1
for number in [2, 3, 4, 5]:
    total += number
    product *= number
print(total, product)
```

Output:

```text
14 120
```

The product must start at `1` (not `0`), because `0 * anything` is `0`.

4.

```python
head, *tail = [10, 20, 30, 40, 50]
print(head)
print(tail)
```

Output:

```text
10
[20, 30, 40, 50]
```

5. With `b += [3]`, `a` also prints `[1, 2, 3]`, because `+=` extended the one shared list in place. With `b = b + [3]`, a new list is built and `b` is rebound to it, so `a` stays `[1, 2]`.

```python
a = [1, 2]
b = a
b += [3]
print(a)

a = [1, 2]
b = a
b = b + [3]
print(a, b)
```

Output:

```text
[1, 2, 3]
[1, 2] [1, 2, 3]
```

---

## Chapter Summary and Key Takeaways

- Relational operators (`== != < > <= >=`) produce `True` or `False`; `=` assigns and `==` compares; chained comparisons such as `0 <= x <= 100` read like mathematics.
- Compare floats with `math.isclose`, compare to `None` with `is None`, and remember that ordering unrelated types raises `TypeError`.
- `and`, `or` and `not` work on truthiness; `and` / `or` short-circuit and return one of their operands; precedence is `not`, then `and`, then `or`.
- Falsy values are `False`, `None`, zeros and empty strings or collections; use `x is None` rather than `x or default` when `0` or `""` is valid.
- Augmented assignment (`+=`, `-=`, `*=`, `/=`, `//=`, `%=`, `**=`) updates a name from its old value; tuple assignment swaps; unpacking splits sequences.
- `a = b = []` shares one list, and `x += [1]` mutates a list in place, whereas `x = x + [1]` creates a new one.

Next: [Chapter 13 — Identity Operators and Operator Precedence](13-identity-operators-and-precedence.md) explains `is` versus `==` and the rules that decide the order of evaluation.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
