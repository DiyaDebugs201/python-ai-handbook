# Chapter 14 — Conditional Statements

> Part 3 — Operators and Control Flow · Video: 3:28:43–4:04:18 · Previous: [13 Identity Operators and Operator Precedence](13-identity-operators-and-precedence.md) · Next: [15 Conditionals: Practice Problems](15-conditionals-practice.md)

**In this chapter:** how a program chooses between actions with `if`, `if`-`else`, `elif` ladders and nested `if` statements, why indentation is part of Python's syntax, what counts as a condition, how to write a conditional expression on one line, and when to flatten nested conditions.

**Before you start:** you need comparison and logical operators ([Relational Operators](12-relational-logical-assignment-operators.md#relational-operators), [Logical Operators](12-relational-logical-assignment-operators.md#logical-operators)) and the idea of truthiness (which values count as true or false). Recap: a condition is any expression that Python can treat as true or false; comparisons give `True` or `False`, and values such as `0`, `""`, `[]` and `None` are false while most others are true. Examples were run with Python 3.13; the `match` statement mentioned at the end needs Python 3.10 or later.

---

## Decision Control and the if Statement

**Timestamp:** [3:28:43](https://www.youtube.com/watch?v=J9BI0jGOds8&t=12523s)

**Learning objectives:**

- Explain *control flow* and why programs need decisions.
- Write an `if` statement with a condition, a colon and an indented block.
- Explain why indentation matters and recognise `IndentationError`.
- Use truthiness directly in conditions.

**1. Intuition**

Until now, every program ran its lines from top to bottom, every time. Real programs react: "if it is raining, take an umbrella". An `if` statement lets the program run a block of code only when a condition is true, and skip it otherwise. It is a fork in the road, with a sign that says "this way only if the condition holds".

**2. Why does it exist?**

Without decisions a program would do exactly the same thing for every input. Passwords must be checked, empty files handled, errors detected, discounts applied only to eligible customers. The `if` statement is the basic tool for all of these.

**3. Technical explanation**

The order in which statements run is called *control flow*. By default it is sequential. Decision statements (like `if`) and loops (covered in [while Loops and Loop Control](16-while-loop-and-loop-control.md)) change it.

An `if` statement has three parts:

1. The keyword `if`.
2. A *condition*: any expression. Python evaluates it and checks its truthiness.
3. A *block*: one or more statements, indented and introduced by a colon `:`.

If the condition is true, the block runs. If it is false, Python skips the whole block and continues with the first statement that is not indented under the `if`.

*Indentation.* Many languages mark blocks with braces `{ }`. Python uses indentation (leading spaces). Every statement in the same block must have the same indentation, and the block ends when the indentation goes back. PEP 8 recommends four spaces per level. Do not mix tabs and spaces: Python 3 rejects inconsistent mixtures with a `TabError`. An editor that inserts four spaces when you press Tab avoids the problem.

*Conditions.* The condition can be a comparison (`age >= 18`), a logical combination (`a > 0 and b > 0`), a membership test (`"x" in text`), or any value, because of truthiness: `if items:` is true when the list is not empty, and `if name:` is true when the string is not empty. Do not write `if flag == True:`; write `if flag:`.

**4. Syntax**

```text
if condition:
    statement_1
    statement_2
next_statement_outside_the_block
```

This is a pattern, not runnable code.

- `condition` ends with a colon. Forgetting the colon is a `SyntaxError`.
- The lines of the block are indented by the same amount (four spaces).
- A block needs at least one statement. If you have nothing to put there yet, use `pass` (see [The pass Statement](16-while-loop-and-loop-control.md#the-pass-statement)).
- For a very short block, you may write it on one line (`if x > 0: print("positive")`), but PEP 8 discourages this.

**5. Example 1 — Basic**

```python
temperature = 34

if temperature > 30:
    print("It is hot.")
    print("Drink water.")

print("This line always runs.")

if temperature < 10:
    print("It is cold.")

print("Done.")
```

Output:

```text
It is hot.
Drink water.
This line always runs.
Done.
```

Line by line:

- `temperature > 30` is `True`, so both indented lines run.
- The line `print("This line always runs.")` is not indented, so it is outside the `if` and runs regardless.
- The second condition is false (`34 < 10`), so its block is skipped completely, and nothing is printed for it.
- `Done.` runs, because it is outside both blocks.

**6. Example 2 — Practical**

Conditions that use truthiness, membership and combined tests, in a small order-checking routine:

```python
cart = ["pen", "notebook"]
coupon = ""
balance = 120
price = 95

if cart:
    print("Cart has", len(cart), "items.")

if not coupon:
    print("No coupon applied.")

if "pen" in cart:
    print("Pen found in the cart.")

if balance >= price and len(cart) > 0:
    balance -= price
    print("Order placed. Balance left:", balance)

if balance < 50:
    print("Low balance warning.")
```

Output:

```text
Cart has 2 items.
No coupon applied.
Pen found in the cart.
Order placed. Balance left: 25
Low balance warning.
```

Line by line:

- `if cart:` is true for a non-empty list, so there is no need to write `len(cart) > 0`.
- `if not coupon:` is true when the string is empty.
- `"pen" in cart` is a membership test.
- The compound condition uses `and`: both parts must hold. The block changes the balance, so the final `if` sees the new value (25 is below 50, so the warning is printed).

**7. Example 3 — Edge case or common mistake**

Indentation errors. Python reports these before it runs anything, so they are shown as text with the messages Python 3.13 prints. First, a block with no indentation:

```text
x = 5
if x > 3:
print("a")
```

```text
  File "example.py", line 3
    print("a")
    ^^^^^
IndentationError: expected an indented block after 'if' statement on line 2
```

A line that is indented differently from its neighbours in the same block:

```text
x = 5
if x > 3:
    print("big")
  print("oops")
```

```text
  File "example.py", line 4
    print("oops")
                 ^
IndentationError: unindent does not match any outer indentation level
```

A tab mixed with spaces:

```text
x = 5
if x > 3:
    print("a")
<TAB>print("b")
```

```text
  File "example.py", line 4
    	print("b")
    ^
TabError: inconsistent use of tabs and spaces in indentation
```

(The `<TAB>` marker stands for a real tab character.) A missing colon:

```text
if x > 3
    print("a")
```

```text
  File "example.py", line 1
    if x > 3
            ^
SyntaxError: expected ':'
```

A different kind of mistake does not cause any error. Both examples below are valid, but they do different things, because the indentation changes which statements belong to the `if`:

```python
number = 4

if number > 10:
    print("big number")
    print("checked")

print("--")

if number > 10:
    print("big number")
print("checked")
```

Output:

```text
--
checked
```

In the first version both lines are in the block and are skipped. In the second version only the first `print` belongs to the `if`, and `checked` is always printed. In Python, indentation is the program's structure, so a misplaced line can change the meaning silently.

Another trap: comparing a value with `True`, and assigning instead of comparing:

```python
items = [1, 2]

if items == True:
    print("never printed")
if items:
    print("printed, because the list is not empty")
```

Output:

```text
printed, because the list is not empty
```

`items == True` is `False`, because a list is never equal to `True`, but `if items:` uses truthiness and is true. (Writing `=` inside the condition, `if x = 5:`, is a syntax error, as shown in [Relational Operators](12-relational-logical-assignment-operators.md#relational-operators).)

**8. Common mistakes**

- Forgetting the colon at the end of the `if` line.
- Inconsistent indentation, or mixing tabs and spaces.
- Putting the statement that should be inside the block at the left margin (or the other way round).
- Writing `if x == True:` or `if len(items) > 0:` where `if x:` and `if items:` are clearer.
- Using `=` instead of `==`.
- Writing an empty block. Use `pass` as a placeholder.
- Testing floats with `==`.

**9. Real-world and AI applications**

Conditions validate input (a negative age, an empty file name), handle errors (check a status code before using a response), enforce rules (access control, limits), and choose between behaviours (a premium or a free path). In AI code, `if` statements pick the device (`if gpu_available:`), skip work that is already done (`if output_path exists:`), apply a threshold to a model's score, handle empty or missing inputs, and stop training when a validation metric stops improving.

**10. Practice**

1. Read a number `n` (set it in the code) and print `"positive"` if it is greater than 0.
2. Write code that prints `"Even"` if a number is even, and a second `if` that prints `"Multiple of 5"` if it is divisible by 5. Test with 10, 7 and 15.
3. A shop gives free delivery when the total is at least 500 and the customer is a member. Print `"Free delivery"` when both are true.
4. Find and fix the error: `if score > 50` followed by an indented `print("pass")`.
5. What is the difference between the two programs in Example 3's indentation demonstration? Explain in one sentence.

**11. Interview questions**

- *How does Python mark a block of code?* By indentation after a colon, not by braces.
- *What happens if the condition of an `if` is false and there is no `else`?* The block is skipped and execution continues after it.
- *Which values count as false in a condition?* `False`, `None`, zeros, and empty strings and collections.
- *Why is `if x == True:` discouraged?* It is redundant, and it fails for truthy values that are not equal to `True`; write `if x:`.

**12. Quick revision**

- `if condition:` then an indented block; the block runs only when the condition is true.
- Indent consistently (four spaces); never mix tabs and spaces.
- Conditions can be any expression; truthiness works (`if items:`).
- Statements at the left margin after the block always run.
- Missing colon is a `SyntaxError`; wrong indentation is an `IndentationError`.

---

## The if-else Statement

**Timestamp:** [3:41:17](https://www.youtube.com/watch?v=J9BI0jGOds8&t=13277s)

**Learning objectives:**

- Write an `if`-`else` statement and explain that exactly one of the two blocks runs.
- Choose between `if`-`else` and two separate `if` statements.
- Use the conditional expression `value_if_true if condition else value_if_false`.

**1. Intuition**

A plain `if` says "do this when the condition holds". `if`-`else` adds "otherwise, do that". It is a road that splits in two and always takes exactly one branch: a door that is either open or closed, a number that is either even or odd.

**2. Why does it exist?**

Many decisions have two outcomes, and the second outcome needs its own action. Writing `if x:` and then `if not x:` would repeat the condition and could go wrong if the two conditions were not exact opposites.

**3. Technical explanation**

An `if`-`else` statement evaluates the condition once. If it is true, the `if` block runs and the `else` block is skipped. If it is false, the `if` block is skipped and the `else` block runs. Exactly one of the two blocks always runs. The `else` has no condition of its own and must line up with its `if`.

Python also has a one-line *conditional expression* (sometimes called the ternary operator), which produces a value: `x if condition else y` evaluates to `x` when the condition is true and to `y` otherwise. It is an expression, so it can appear on the right of an assignment or inside a function call. Use it for short, simple choices; use a normal `if`-`else` statement when the branches are longer.

**4. Syntax**

```text
if condition:
    block_when_true
else:
    block_when_false

value = result_if_true if condition else result_if_false
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
number = 7

if number % 2 == 0:
    print(number, "is even")
else:
    print(number, "is odd")

age = 16
if age >= 18:
    print("You can vote.")
else:
    print("You cannot vote yet.")
    print("Years to wait:", 18 - age)

status = "adult" if age >= 18 else "minor"
print(status)
```

Output:

```text
7 is odd
You cannot vote yet.
Years to wait: 2
minor
```

Line by line:

- `7 % 2 == 0` is false, so the `else` block runs.
- In the second statement the `else` block has two lines, both indented.
- The last two lines use the conditional expression to pick one of two strings in a single line.

**6. Example 2 — Practical**

Login check, safe division and a pricing rule:

```python
def check_login(username, password):
    stored_username = "diya"
    stored_password = "s3cret!"
    if username == stored_username and password == stored_password:
        return "Welcome, " + username
    else:
        return "Invalid username or password"


print(check_login("diya", "s3cret!"))
print(check_login("diya", "wrong"))


def safe_divide(a, b):
    if b == 0:
        return None
    else:
        return a / b


print(safe_divide(10, 4), safe_divide(10, 0))


def ticket_price(age, is_student):
    base = 200
    if age < 12 or age >= 60:
        price = base / 2
    else:
        price = base
    if is_student:
        price -= 20
    return price


print(ticket_price(8, False), ticket_price(30, True), ticket_price(65, True))
```

Output:

```text
Welcome, diya
Invalid username or password
2.5 None
100.0 180 80.0
```

Line by line:

- `check_login` returns one message for each outcome; the fixed credentials here are made up for the example. Real programs never store passwords in plain text in code (see [Environment Variables, .env Files, and API Keys](30-python-wrap-up-and-ai-intro.md#environment-variables-env-files-and-api-keys)).
- `safe_divide` avoids `ZeroDivisionError` by checking first. (The functions are explained in [Defining Functions and Return Values](25-defining-functions-and-return-values.md); here they just package the decision.)
- In `ticket_price`, the first `if`-`else` picks a base price. The second `if` has no `else` because "no change" needs no code.

**7. Example 3 — Edge case or common mistake**

`if`-`else` versus two separate `if` statements; the "dangling else" and the one-line expression:

```python
x = 5

if x > 3:
    print("A")
if x > 4:
    print("B")
else:
    print("C")

print("--")

if x > 3:
    print("A")
elif x > 4:
    print("B")
else:
    print("C")
```

Output:

```text
A
B
--
A
```

In the first program, the two `if` statements are independent: the first `if` runs on its own, and the `else` belongs only to the second `if`. Both `A` and `B` print. In the second program one chain is used, so only the first true branch runs and only `A` prints. Choose the form that matches the logic you want.

A common source of confusion is the `else` that seems to belong to a different `if`. An `else` always attaches to the nearest `if` at the same indentation:

```python
a = 5
b = -2

if a > 0:
    if b > 0:
        print("both positive")
else:
    print("a is not positive")

print("--")

if a > 0:
    if b > 0:
        print("both positive")
    else:
        print("a is positive, b is not")
```

Output:

```text
--
a is positive, b is not
```

In the first statement the `else` lines up with the outer `if`, so it runs only when `a > 0` is false; with `a = 5`, nothing is printed. In the second the `else` lines up with the inner `if`, so it runs when `b > 0` is false. The indentation of the `else` decides which condition it belongs to.

Finally, a conditional expression that is too clever:

```python
n = 15
print("FizzBuzz" if n % 15 == 0 else "Fizz" if n % 3 == 0 else "Buzz" if n % 5 == 0 else n)
```

Output:

```text
FizzBuzz
```

It works, but once there are more than two choices a normal `if`-`elif`-`else` chain (next section) is easier to read.

**8. Common mistakes**

- Writing a condition after `else` (`else x > 3:`). `else` takes no condition; `elif` does.
- Placing the `else` at the wrong indentation, so that it attaches to the wrong `if`.
- Using two separate `if` statements where one `if`-`else` is meant, so both blocks can run (or neither).
- Forgetting the colon after `else`.
- Writing long or nested conditional expressions that nobody can read.
- Repeating the condition (`if x > 0:` ... `if x <= 0:`) instead of using `else`.

**9. Real-world and AI applications**

Two-way decisions are everywhere: valid or invalid input, success or failure of a request, training or evaluation mode, GPU or CPU. In AI projects you will see `device = "cuda" if gpu_available else "cpu"` in the conditional expression form, and `if` / `else` around a model call to handle an empty prompt or a failed response. Be careful with rules that look binary but are not: for instance, a classifier threshold is a policy choice, not a fact.

**10. Practice**

1. Print `"pass"` if a mark is 40 or more, otherwise print `"fail"`.
2. Write `absolute(x)` that returns `x` if it is non-negative and `-x` otherwise (without using `abs`).
3. Write a function `max_of_two(a, b)` using `if`-`else`, and again using a conditional expression.
4. Write `is_leap(year)` with `if`-`else` (a year is a leap year if it is divisible by 4 and not by 100, or divisible by 400).
5. Explain why the first program of Example 3 prints both `A` and `B`, while the `elif` version prints only `A`.

**11. Interview questions**

- *Can both blocks of an `if`-`else` run?* No. Exactly one runs.
- *What is a conditional expression?* The one-line form `a if condition else b`, which produces a value.
- *To which `if` does an `else` belong?* The nearest preceding `if` at the same indentation level.
- *Does `else` have a condition?* No; `elif` has one.

**12. Quick revision**

- `if condition: ... else: ...` runs exactly one of the two blocks.
- The `else` has no condition and no brackets, only a colon.
- `value = a if condition else b` is the one-line form for simple choices.
- Indentation decides which `if` an `else` belongs to.
- Separate `if` statements are independent; one `if`/`else` chain is exclusive.

---

## The elif Ladder

**Timestamp:** [3:47:03](https://www.youtube.com/watch?v=J9BI0jGOds8&t=13623s)

**Learning objectives:**

- Write a chain of `if` / `elif` / `else` and explain that the first true branch wins.
- Order the conditions correctly in a ladder.
- Explain the difference between an `elif` chain and several independent `if` statements.
- Recognise when a `match` statement (Python 3.10+) is an alternative.

**1. Intuition**

An `elif` ladder is like a series of questions at a ticket counter: "Are you under 5? Free. Else, are you under 18? Half price. Else, are you over 60? Concession. Otherwise: full price." You stop at the first "yes" and ignore the rest.

**2. Why does it exist?**

Many decisions have more than two outcomes: grades, tax slabs, discount levels, categories. Nesting an `if`-`else` inside another `if`-`else` for each level gets deeper and deeper. `elif` ("else if") keeps all the choices at the same level.

**3. Technical explanation**

A ladder consists of one `if`, any number of `elif` branches, and an optional final `else`. Python checks the conditions from top to bottom. It runs the block of the first condition that is true and then skips all remaining branches, including their conditions, which are not even evaluated. If no condition is true, the `else` block runs (if there is one). If there is no `else` and no condition is true, nothing runs.

Because the first true branch wins, **order matters**. For ranges, test the most specific or highest threshold first, so that each later `elif` only has to describe the remaining cases: "score >= 90", then "score >= 75" (which implicitly means "below 90 and at least 75"). If you test `score >= 40` first, all higher scores get caught by that branch.

An `elif` chain differs from a series of separate `if` statements. With separate `if`s, every condition is checked independently and several blocks can run. In an `elif` chain at most one block runs.

From Python 3.10, the `match` statement offers *structural pattern matching*, which is often used to select among many fixed values. For ranges and general conditions, an `elif` ladder remains the right tool.

**4. Syntax**

```text
if condition_1:
    block_1
elif condition_2:
    block_2
elif condition_3:
    block_3
else:
    block_else
```

This is a pattern, not runnable code. The `else` is optional. Each `elif` needs its own condition and colon.

**5. Example 1 — Basic**

```python
score = 82

if score >= 90:
    grade = "A"
elif score >= 75:
    grade = "B"
elif score >= 60:
    grade = "C"
elif score >= 40:
    grade = "D"
else:
    grade = "F"

print("Score", score, "grade", grade)
```

Output:

```text
Score 82 grade B
```

Line by line: `82 >= 90` is false, `82 >= 75` is true, so `grade` becomes `"B"` and the remaining conditions are not checked. Try other scores, such as 95, 60, 39 and 40, and trace which branch runs.

**6. Example 2 — Practical**

A function with a ladder for a ticket price, and one for a simple tax-slab calculation. The slab amounts are invented for the example.

```python
def ticket_price(age):
    if age < 0:
        return None
    elif age < 5:
        return 0
    elif age < 18:
        return 100
    elif age < 60:
        return 200
    else:
        return 120


for age in [3, 10, 30, 70, -1]:
    print(age, ticket_price(age))


def income_tax(income):
    if income <= 300000:
        rate = 0
    elif income <= 700000:
        rate = 0.05
    elif income <= 1000000:
        rate = 0.10
    else:
        rate = 0.20
    return income * rate


for income in [250000, 500000, 900000, 1500000]:
    print(income, income_tax(income))


def classify_temperature(celsius):
    if celsius < 0:
        return "freezing"
    elif celsius < 15:
        return "cold"
    elif celsius < 25:
        return "pleasant"
    elif celsius < 35:
        return "warm"
    return "hot"


print([classify_temperature(t) for t in [-5, 10, 20, 30, 40]])
```

Output:

```text
3 0
10 100
30 200
70 120
-1 None
250000 0
500000 25000.0
900000 90000.0
1500000 300000.0
['freezing', 'cold', 'pleasant', 'warm', 'hot']
```

Line by line:

- In `ticket_price`, the first branch catches impossible ages, so later branches can assume `age >= 0`. Each later `elif` only needs an upper bound because smaller values were already handled above it.
- `income_tax` uses the ladder to set a rate and then does one calculation; this avoids repeating the multiplication in every branch. (It applies one rate to the whole income. Real income tax is usually progressive, with each rate applying only to a slice of the income; see the practice problems in [Conditionals: Practice Problems](15-conditionals-practice.md).)
- `classify_temperature` has no `else`: because each earlier branch returns, the last `return` handles whatever is left.
- The last line builds a list with a *list comprehension*, a compact loop covered in [List Comprehension](20-list-comprehension.md). It simply calls the function for each temperature.

For fixed values, `match` (Python 3.10+) is an alternative:

```python
command = "stop"

match command:
    case "go":
        print("going")
    case "stop" | "halt":
        print("stopping")
    case _:
        print("unknown command")
```

Output:

```text
stopping
```

`case "stop" | "halt"` matches either value, and `case _` is the "anything else" branch. Use `match` for a choice among fixed values or structures; use `elif` for ranges and general conditions.

**7. Example 3 — Edge case or common mistake**

The ordering mistake: the first true branch wins, so a general test placed first hides the specific ones:

```python
score = 95

if score >= 40:
    grade = "D"
elif score >= 60:
    grade = "C"
elif score >= 75:
    grade = "B"
elif score >= 90:
    grade = "A"
else:
    grade = "F"

print(grade)
```

Output:

```text
D
```

A score of 95 should be an `A`, but the first condition (`score >= 40`) is already true, so the ladder stops there. Python gives no error; the logic is simply wrong. Always test the strictest condition first when the conditions overlap.

The second common mistake is using separate `if` statements where a chain is needed:

```python
score = 82
grades = []

if score >= 90:
    grades.append("A")
if score >= 75:
    grades.append("B")
if score >= 60:
    grades.append("C")

print(grades)
```

Output:

```text
['B', 'C']
```

Every condition that is true runs, so the score of 82 gets two grades, `B` and `C`. With `elif`, only the first match would run.

A third mistake is forgetting that no branch may run at all:

```python
mark = 20

if mark >= 90:
    result = "A"
elif mark >= 40:
    result = "pass"

print(result)
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 8, in <module>
    print(result)
          ^^^^^^
NameError: name 'result' is not defined
```

Because no condition was true and there is no `else`, `result` was never created, so using it later raises a `NameError` (the name is not defined). Add an `else`, or give `result` a default value before the ladder.

**8. Common mistakes**

- Putting a broad condition before a narrower one.
- Using separate `if` statements when only one branch should run.
- Writing `else if` instead of `elif` (a syntax error in Python).
- Giving `else` a condition.
- Forgetting a final `else` and leaving a variable undefined.
- Overlapping or gapped ranges (`< 18` then `> 18` leaves 18 out).
- Writing very long ladders where a dictionary lookup or `match` would be simpler.

**9. Real-world and AI applications**

Ladders classify values: HTTP status codes (success, redirect, client error, server error), grade bands, price tiers, severity levels, file types, learning-rate schedules that depend on the epoch. In an AI pipeline you might route a request by its type (`if task == "summarize": ... elif task == "translate": ... else: ...`), choose a prompt template, or react to a model's confidence level with different actions (accept, ask for confirmation, escalate to a person). Such routing logic should always include an `else` branch that handles the unexpected case safely.

**10. Practice**

1. Write a function that converts a mark to a letter grade (A at 90 and above, B at 80 and above, C at 70 and above, D at 60 and above, otherwise F) and test the boundaries 90, 89, 60, 59.
2. Write `sign(n)` that returns `"negative"`, `"zero"` or `"positive"`.
3. Write `bmi_category(bmi)`: under 18.5 `"underweight"`, under 25 `"normal"`, under 30 `"overweight"`, otherwise `"obese"`. Test the boundaries.
4. Write `day_type(day)` that returns `"weekend"` for `"Sat"` and `"Sun"`, `"weekday"` for the other five day names, and `"invalid"` otherwise.
5. Find the bug: `if age > 18: ... elif age > 12: ... elif age > 18: ...` (a branch that can never run) and say how to repair it.
6. Rewrite your answer to exercise 4 using `match` (Python 3.10+).

**11. Interview questions**

- *What is the difference between a series of `if` statements and an `if`/`elif` chain?* Separate `if`s are all checked, and several blocks can run; in a chain only the first true branch runs.
- *Why does the order of `elif` conditions matter?* Python stops at the first true condition, so overlapping conditions must be ordered from most to least specific.
- *Is `else` required at the end of a ladder?* No. Without it, nothing runs when no condition is true.
- *When would you use `match` instead of `elif`?* To choose between fixed values or structures (Python 3.10+).

**12. Quick revision**

- `if` / `elif` / `else`: conditions are tested in order; the first true one runs; the rest are skipped.
- Order from most specific to least specific; leave no gaps or overlaps.
- `elif`, not `else if`; `else` has no condition.
- Separate `if` statements are independent.
- A missing `else` can leave a variable undefined.

---

## Nested if Statements

**Timestamp:** [3:56:24](https://www.youtube.com/watch?v=J9BI0jGOds8&t=14184s)

**Learning objectives:**

- Write an `if` statement inside another `if` and trace which block runs.
- Combine nested conditions into a single condition with `and` when appropriate.
- Reduce nesting with guard clauses (early `return`).
- Decide when nesting is the right choice.

**1. Intuition**

Sometimes one decision depends on the answer to another. At airport security you first check "do you have a ticket?", and only if so, "is your bag within the weight limit?". The second question is asked only after the first answer is yes. Nested `if` statements model that: a decision inside a decision.

**2. Why does it exist?**

Some questions only make sense after an earlier one has been answered. You cannot check a password until you know the user exists, and you cannot read a field from a record until you know the record is present. Nesting expresses "ask this only if that is true".

**3. Technical explanation**

A nested `if` is an `if` statement that sits inside the block of another `if`, `elif` or `else`. It is indented one more level. Each level of indentation corresponds to one condition that must hold for that code to run. The inner statement is only evaluated when the outer condition allowed the program to reach it.

Deep nesting makes code hard to read: each level adds four spaces and one more condition to remember. Two common ways to reduce it:

1. *Combine conditions with `and`.* `if a: if b: ...` is the same as `if a and b: ...` when there is no code between the two `if`s and no `else` on the outer one.
2. *Use guard clauses.* In a function, test for the bad cases first and `return` early, so the main logic stays at the left margin. Instead of wrapping everything in `if valid:`, write `if not valid: return` and continue.

Nesting is still the right choice when the inner decision needs different branches for each outer outcome, or when the inner condition would be an error if the outer one were false (for example, indexing into a list that might be empty).

**4. Syntax**

```text
if outer_condition:
    if inner_condition:
        inner_block
    else:
        inner_else_block
else:
    outer_else_block
```

This is a pattern, not runnable code. Each `else` lines up with the `if` it belongs to.

**5. Example 1 — Basic**

```python
age = 25
has_license = True

if age >= 18:
    print("Adult.")
    if has_license:
        print("You may drive.")
    else:
        print("Get a license first.")
else:
    print("Minor: you may not drive.")
```

Output:

```text
Adult.
You may drive.
```

Line by line: the outer condition (`age >= 18`) is true, so `Adult.` prints and the inner `if` is evaluated. `has_license` is true, so `You may drive.` prints. If `age` were 15, the inner statement would never be reached, and the outer `else` would run.

**6. Example 2 — Practical**

Decisions that depend on each other, written first with nesting and then flattened:

```python
def loan_decision(age, income, credit_score):
    if age >= 21:
        if income >= 30000:
            if credit_score >= 700:
                return "approved"
            else:
                return "needs review"
        else:
            return "income too low"
    else:
        return "too young"


print(loan_decision(30, 50000, 750))
print(loan_decision(30, 50000, 650))
print(loan_decision(30, 20000, 750))
print(loan_decision(19, 50000, 750))


def loan_decision_flat(age, income, credit_score):
    if age < 21:
        return "too young"
    if income < 30000:
        return "income too low"
    if credit_score < 700:
        return "needs review"
    return "approved"


print(loan_decision_flat(30, 50000, 750))
print(loan_decision_flat(30, 50000, 650))
print(loan_decision_flat(30, 20000, 750))
print(loan_decision_flat(19, 50000, 750))
```

Output:

```text
approved
needs review
income too low
too young
approved
needs review
income too low
too young
```

Line by line:

- The first version nests three levels deep; the reader has to hold three conditions in mind at the bottom.
- The second version uses guard clauses: each failing condition returns at once, and the successful path stays at the left margin. Both versions give identical results for these cases. The limits in the example (21, 30000, 700) are made up.

Combining conditions with `and`, and a nested decision that really needs nesting:

```python
username = "diya"
users = {"diya": "s3cret!", "asha": "pa55word"}
typed_password = "s3cret!"

if username in users:
    if users[username] == typed_password:
        print("Login successful")
    else:
        print("Wrong password")
else:
    print("Unknown user")

marks = [72, 85]
if len(marks) > 0 and sum(marks) / len(marks) >= 60:
    print("Passed with average", sum(marks) / len(marks))
```

Output:

```text
Login successful
Passed with average 78.5
```

The dictionary lookup `users[username]` would raise an error if the user did not exist (see [Dictionaries](23-dictionaries.md#dictionaries)), so the outer `if` guards it, and the two outcomes ("wrong password", "unknown user") need different messages. The last `if` shows a flattened form: `and` short-circuits, so the average is only computed when the list is not empty.

**7. Example 3 — Edge case or common mistake**

Wrong `else` placement and depth, and unreachable branches:

```python
def check(n):
    if n > 0:
        if n > 100:
            return "large positive"
    else:
        return "not positive"


print(check(500))
print(check(50))
print(check(-5))
```

Output:

```text
large positive
None
not positive
```

For `check(50)`, the outer condition is true, the inner one is false, and no `else` handles that case, so the function reaches its end without a `return` and gives back `None`. Nested conditions make it easy to forget a path. Every combination of outcomes must lead to a decision. A flat version makes the gap obvious:

```python
def check(n):
    if n <= 0:
        return "not positive"
    if n > 100:
        return "large positive"
    return "small positive"


print(check(500), check(50), check(-5))
```

Output:

```text
large positive small positive not positive
```

A second common mistake is the unreachable branch:

```python
x = 15

if x > 10:
    print("greater than 10")
elif x > 20:
    print("greater than 20")
```

Output:

```text
greater than 10
```

Any value over 20 is also over 10, so the `elif` can never run. Python does not warn you. The usual repair is to put the stricter condition first.

**8. Common mistakes**

- Nesting more than two or three levels deep, where guard clauses or `and` would do.
- Not handling every combination of outcomes (a missing `else` returns `None` from a function).
- Misaligned `else` that attaches to the wrong `if`.
- Flattening with `and` when the inner condition is only safe after the outer one, in the wrong order (`items[0] == "a" and items` fails on an empty list; the safe order is `items and items[0] == "a"`).
- Duplicating the same condition at several nesting levels.
- Creating branches that cannot be reached.

**9. Real-world and AI applications**

Validation code is full of dependent checks: the file exists, then it can be opened, then it has the right format, then each field is valid. Guard clauses keep such code readable. In AI code, request handlers check that the input is present, then that it is within the allowed length, then that the model returned a usable answer, and only then continue. Using early returns for each failure makes the main path easy to follow and each error message specific.

**10. Practice**

1. Write a nested `if` that prints `"Eligible"` when age is between 18 and 60 and income is at least 25000, with different messages for each reason of failure.
2. Flatten the previous solution using guard clauses in a function.
3. Write `triangle_type(a, b, c)` that first checks if the three sides can form a triangle (each side smaller than the sum of the other two) and only then reports `"equilateral"`, `"isosceles"` or `"scalene"`.
4. For `numbers = [4, -2, 9]`, write a nested decision that says whether the list is empty, and, if not, whether its first item is positive or not. Make sure empty lists do not cause an error.
5. Fix `check(n)` from Example 3 in a version that keeps the nesting but returns a value for every case.

**11. Interview questions**

- *What is a nested `if`?* An `if` statement inside the block of another conditional statement.
- *How can you reduce nesting?* Combine conditions with `and`, use guard clauses with early returns, or move logic into functions.
- *When is `if a: if b:` equivalent to `if a and b:`?* When there is no other code between them and neither has an `else`.
- *What does a function return if no `return` statement is reached?* `None`.

**12. Quick revision**

- Nested `if` = a decision inside a decision; each level is indented once more.
- Combine with `and` when possible; use guard clauses to flatten.
- Make sure every path returns or sets a value; check `else` alignment.
- Guard risky operations (indexing, dictionary lookup, division) with an outer or earlier condition.
- Prefer shallow code: two or three levels at most.

---

## Answers to Practice Exercises

### Answers: Decision Control and the if Statement

1.

```python
n = 12
if n > 0:
    print("positive")
```

Output:

```text
positive
```

2.

```python
for number in [10, 7, 15]:
    if number % 2 == 0:
        print(number, "Even")
    if number % 5 == 0:
        print(number, "Multiple of 5")
```

Output:

```text
10 Even
10 Multiple of 5
15 Multiple of 5
```

Two separate `if` statements are right here, because a number can be both even and a multiple of 5 (10 is both).

3.

```python
total = 650
is_member = True

if total >= 500 and is_member:
    print("Free delivery")
```

Output:

```text
Free delivery
```

4. The `if` line has no colon. Correct form:

```python
score = 70
if score > 50:
    print("pass")
```

Output:

```text
pass
```

5. In the first version, both `print` calls are indented under the `if`, so both are skipped for a false condition. In the second version, only the first `print` is in the block, and `checked` is printed every time, because it is not indented.

### Answers: The if-else Statement

1.

```python
mark = 38
if mark >= 40:
    print("pass")
else:
    print("fail")
```

Output:

```text
fail
```

2.

```python
def absolute(x):
    if x >= 0:
        return x
    else:
        return -x


print(absolute(5), absolute(-5), absolute(0))
```

Output:

```text
5 5 0
```

3.

```python
def max_of_two(a, b):
    if a >= b:
        return a
    else:
        return b


def max_of_two_expression(a, b):
    return a if a >= b else b


print(max_of_two(3, 9), max_of_two_expression(3, 9), max_of_two(7, 7))
```

Output:

```text
9 9 7
```

4.

```python
def is_leap(year):
    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        return True
    else:
        return False


for year in [1900, 2000, 2023, 2024]:
    print(year, is_leap(year))
```

Output:

```text
1900 False
2000 True
2023 False
2024 True
```

(A simpler version returns the condition itself: `return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0`.)

5. In the first program, the first `if` and the second `if`/`else` are separate statements. The first prints `A` (5 > 3). The second checks `x > 4`, which is true, so `B` prints and its `else` is skipped. In the `elif` version, a single chain stops at the first true branch, `A`.

### Answers: The elif Ladder

1.

```python
def letter_grade(mark):
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "F"


for mark in [90, 89, 60, 59]:
    print(mark, letter_grade(mark))
```

Output:

```text
90 A
89 B
60 D
59 F
```

2.

```python
def sign(n):
    if n < 0:
        return "negative"
    elif n == 0:
        return "zero"
    else:
        return "positive"


print(sign(-4), sign(0), sign(12))
```

Output:

```text
negative zero positive
```

3.

```python
def bmi_category(bmi):
    if bmi < 18.5:
        return "underweight"
    elif bmi < 25:
        return "normal"
    elif bmi < 30:
        return "overweight"
    else:
        return "obese"


for bmi in [18.4, 18.5, 24.9, 25, 29.9, 30]:
    print(bmi, bmi_category(bmi))
```

Output:

```text
18.4 underweight
18.5 normal
24.9 normal
25 overweight
29.9 overweight
30 obese
```

4.

```python
def day_type(day):
    if day in ("Sat", "Sun"):
        return "weekend"
    elif day in ("Mon", "Tue", "Wed", "Thu", "Fri"):
        return "weekday"
    else:
        return "invalid"


print(day_type("Sun"), day_type("Wed"), day_type("xyz"))
```

Output:

```text
weekend weekday invalid
```

5. The condition `age > 18` appears twice, and any age greater than 18 is already handled by the first branch, so the third branch can never run. If the third branch was meant to test another range, change its condition (for example `age > 5`). If it is a duplicate, remove it.
6.

```python
def day_type_match(day):
    match day:
        case "Sat" | "Sun":
            return "weekend"
        case "Mon" | "Tue" | "Wed" | "Thu" | "Fri":
            return "weekday"
        case _:
            return "invalid"


print(day_type_match("Sun"), day_type_match("Wed"), day_type_match("xyz"))
```

Output:

```text
weekend weekday invalid
```

### Answers: Nested if Statements

1.

```python
age = 30
income = 20000

if 18 <= age <= 60:
    if income >= 25000:
        print("Eligible")
    else:
        print("Not eligible: income too low")
else:
    print("Not eligible: age out of range")
```

Output:

```text
Not eligible: income too low
```

2.

```python
def eligibility(age, income):
    if not 18 <= age <= 60:
        return "Not eligible: age out of range"
    if income < 25000:
        return "Not eligible: income too low"
    return "Eligible"


print(eligibility(30, 20000))
print(eligibility(30, 40000))
print(eligibility(70, 40000))
```

Output:

```text
Not eligible: income too low
Eligible
Not eligible: age out of range
```

3.

```python
def triangle_type(a, b, c):
    if a + b <= c or a + c <= b or b + c <= a:
        return "not a triangle"
    if a == b == c:
        return "equilateral"
    if a == b or b == c or a == c:
        return "isosceles"
    return "scalene"


print(triangle_type(3, 3, 3))
print(triangle_type(3, 3, 5))
print(triangle_type(3, 4, 5))
print(triangle_type(1, 2, 10))
```

Output:

```text
equilateral
isosceles
scalene
not a triangle
```

4.

```python
def describe_first(numbers):
    if len(numbers) == 0:
        return "empty list"
    if numbers[0] > 0:
        return "first item is positive"
    return "first item is not positive"


print(describe_first([4, -2, 9]))
print(describe_first([-1]))
print(describe_first([]))
```

Output:

```text
first item is positive
first item is not positive
empty list
```

5.

```python
def check(n):
    if n > 0:
        if n > 100:
            return "large positive"
        else:
            return "small positive"
    else:
        return "not positive"


print(check(500), check(50), check(-5))
```

Output:

```text
large positive small positive not positive
```

---

## Chapter Summary and Key Takeaways

- `if condition:` followed by an indented block runs the block only when the condition is true; indentation (four spaces, never mixed with tabs) defines the block.
- `if`-`else` runs exactly one of two blocks; `a if condition else b` is the one-line expression form.
- `elif` ladders test conditions in order, run the first true branch and skip the rest; order conditions from most to least specific, and add an `else` for the leftover cases.
- Separate `if` statements are independent; an `if`/`elif` chain is exclusive.
- Nested `if` statements express dependent decisions, but deep nesting is hard to read: combine conditions with `and` or use guard clauses with early returns.
- Watch for missing colons, wrong indentation, misplaced `else`, overlapping ranges and branches that are never reached.

Next: [Chapter 15 — Conditionals: Practice Problems](15-conditionals-practice.md) puts decisions, operators and functions together in worked problems.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
