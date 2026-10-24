# Chapter 15 — Conditionals: Practice Problems

> Part 3 — Operators and Control Flow · Video: 4:04:18–4:19:50 · Previous: [14 Conditional Statements](14-conditional-statements.md) · Next: [16 while Loops and Loop Control](16-while-loop-and-loop-control.md)

**In this chapter:** eight worked problems that combine operators, `if` / `elif` / `else`, nested conditions, string methods and small functions: a leap-year check, a grade report, progressive income tax, a tiered electricity bill, a FizzBuzz variant, a password-strength checker, a calculator with error handling, and rock-paper-scissors. For each problem you see the thinking first, then the solution, the output, and variations to try yourself.

**Before you start:** you need everything from [Chapter 14](14-conditional-statements.md) and the operators from [Chapter 11](11-arithmetic-operators.md), [Chapter 12](12-relational-logical-assignment-operators.md) and [Chapter 13](13-identity-operators-and-precedence.md). A few solutions use a `for` loop to try several test values or to look at each character of a string; this just means "repeat the following block for each item", and it is covered in [The for Loop](17-for-loop-range-and-nested-loops.md#the-for-loop). Function definitions (`def`, `return`) are covered in [Defining Functions and Return Values](25-defining-functions-and-return-values.md); here, a function is simply a named, reusable piece of code that receives values and returns a result. All numbers in the problems (tax slabs, prices, limits) are invented for practice and are not real tax or tariff rules. Examples were run with Python 3.13.

---

## Conditionals: Practice Problems

**Timestamp:** [4:04:18](https://www.youtube.com/watch?v=J9BI0jGOds8&t=14658s)

**Learning objectives:**

- Turn a written rule into conditions, and decide whether it needs `elif`, nesting or several separate `if` statements.
- Choose test values for boundaries and unusual cases before trusting a solution.
- Write small functions whose result can be tested with several inputs.
- Read your own solution critically for overlapping or missing cases.

**How to work through these problems.** For each problem: (1) read the rule and try to solve it yourself before opening the solution; (2) write down the inputs that sit on the *boundaries* (for example, exactly 18 years old, exactly 100 units); (3) write the conditions; (4) test with the boundary values and with a few ordinary ones. Most mistakes in conditional code happen at the boundaries (`<` versus `<=`).

**1. Intuition**

Writing a conditional is translating a sentence ("children under five travel free, others pay by age") into code. The skill is to see the exact cut points and the order in which to test them.

**2. Why does it exist?**

Rules in the real world (prices, taxes, eligibility, safety checks) are conditions with thresholds. Practice with typical rules builds the habit of reading a rule precisely and testing its edges.

**3. Technical explanation**

A reliable method:

1. List the possible outcomes (for example grades A, B, C, F).
2. List the thresholds and decide whether each boundary value belongs to the lower or the upper outcome.
3. Choose the structure: an `elif` ladder when exactly one outcome applies; separate `if`s when several outcomes can apply together; nested or guard-clause form when one question only makes sense after another.
4. Order ladders from most specific to least specific.
5. Write the function so that it returns the result (rather than printing), so that it can be tested with many inputs.

**4. Syntax**

```text
def function_name(inputs):
    if condition_1:
        return result_1
    elif condition_2:
        return result_2
    return default_result
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

**Problem 1: leap year.** A year is a leap year if it is divisible by 4, except that years divisible by 100 are not leap years, unless they are also divisible by 400. Write `is_leap(year)`.

*Thinking.* Three nested rules: divisible by 400 means yes; otherwise divisible by 100 means no; otherwise divisible by 4 means yes; otherwise no. Testing from the most specific rule (400) to the most general (4) in a ladder avoids needing `and`.

```python
def is_leap(year):
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    elif year % 4 == 0:
        return True
    else:
        return False


for year in [1900, 2000, 2023, 2024, 2100]:
    print(year, is_leap(year))
```

Output:

```text
1900 False
2000 True
2023 False
2024 True
2100 False
```

*Why it works.* 1900 is divisible by 100 but not 400, so it is not a leap year. 2000 is divisible by 400, so it is. 2024 is divisible by 4 and not by 100. *Variation:* write the same rule as one `return` using `and` and `or`, and check that both versions agree for every year from 1 to 3000 (a loop with `range`, see [The for Loop with range()](17-for-loop-range-and-nested-loops.md#the-for-loop-with-range)).

**Problem 2: grade report.** Marks are 0 to 100. Grades: A for 90 and above, B for 75 and above, C for 60 and above, D for 40 and above, F below 40. Marks outside 0 to 100 are invalid. Also report `"Pass"` for 40 and above.

*Thinking.* First reject invalid input (a guard clause), then use a ladder from the highest threshold downwards. Return both pieces of information as a pair.

```python
def grade_report(marks):
    if not 0 <= marks <= 100:
        return "invalid", "n/a"
    if marks >= 90:
        grade = "A"
    elif marks >= 75:
        grade = "B"
    elif marks >= 60:
        grade = "C"
    elif marks >= 40:
        grade = "D"
    else:
        grade = "F"
    result = "Pass" if marks >= 40 else "Fail"
    return grade, result


for marks in [100, 90, 89.5, 75, 40, 39, 0, -1, 101]:
    print(marks, grade_report(marks))
```

Output:

```text
100 ('A', 'Pass')
90 ('A', 'Pass')
89.5 ('B', 'Pass')
75 ('B', 'Pass')
40 ('D', 'Pass')
39 ('F', 'Fail')
0 ('F', 'Fail')
-1 ('invalid', 'n/a')
101 ('invalid', 'n/a')
```

*Variations.* Add `"+"` and `"-"` signs. Treat marks that are not numbers as invalid (hint: `isinstance(marks, (int, float))`, see [Numeric Types and Booleans](05-numeric-types-and-booleans.md)).

**6. Example 2 — Practical**

**Problem 3: progressive income tax.** Invented rules: no tax on the first 300,000; 5% on the part from 300,000 to 700,000; 10% on the part from 700,000 to 1,000,000; 20% on the part above 1,000,000. Write `tax(income)`.

*Thinking.* "Progressive" means each rate applies only to its own slice of the income, not to the whole amount. For each slice, work out how much of the income lies in it: the smaller of the income and the top of the slice, minus the bottom of the slice, but never less than zero. A ladder from the top slice down is a clear way to write it.

```python
def tax(income):
    total = 0
    if income > 1000000:
        total += (income - 1000000) * 0.20
        income = 1000000
    if income > 700000:
        total += (income - 700000) * 0.10
        income = 700000
    if income > 300000:
        total += (income - 300000) * 0.05
    return total


for income in [250000, 300000, 500000, 700000, 900000, 1000000, 1500000]:
    print(income, tax(income))
```

Output:

```text
250000 0
300000 0
500000 10000.0
700000 20000.0
900000 40000.0
1000000 50000.0
1500000 150000.0
```

*Why it works.* For an income of 900,000: the part above 700,000 is 200,000, taxed at 10% (20,000); the part from 300,000 to 700,000 is 400,000, taxed at 5% (20,000); in total 40,000. The code takes the top slice first and then reduces `income` to the top of the next slice, so each pass only sees the remaining part. Separate `if` statements (not `elif`) are correct here, because several slices can apply to one income. *Variation:* write the same function with a list of slices and a loop after you have read [The for Loop](17-for-loop-range-and-nested-loops.md#the-for-loop).

**Problem 4: tiered electricity bill.** Invented tariff: the first 100 units cost 3.00 each, the next 100 units (101 to 200) cost 4.50 each, and every unit above 200 costs 6.00. A fixed charge of 50 is added to every bill. Write `bill(units)`; negative units are invalid.

```python
def bill(units):
    if units < 0:
        return None
    charge = 50
    if units <= 100:
        charge += units * 3.00
    elif units <= 200:
        charge += 100 * 3.00 + (units - 100) * 4.50
    else:
        charge += 100 * 3.00 + 100 * 4.50 + (units - 200) * 6.00
    return charge


for units in [-5, 0, 80, 100, 101, 200, 250]:
    print(units, bill(units))
```

Output:

```text
-5 None
0 50.0
80 290.0
100 350.0
101 354.5
200 800.0
250 1100.0
```

*Why it works.* This time the structure is an `elif` ladder, because exactly one band applies to the *last* unit, and the earlier bands are charged in full. For 250 units: 100 units at 3.00, 100 at 4.50, 50 at 6.00, plus the fixed 50. *Check:* at exactly 100 units the bill is continuous with 101 units (it rises by 4.50, the next unit's price), so there are no jumps or gaps at the boundaries. Checking for jumps is a good test for any tiered price.

**Problem 5: FizzBuzz variant.** For a number `n`: return `"FizzBuzz"` if it is divisible by both 3 and 5, `"Fizz"` if divisible by 3, `"Buzz"` if divisible by 5, otherwise the number as text.

*Thinking.* Numbers like 15 satisfy all three conditions, so the "both" test must come first.

```python
def fizzbuzz(n):
    if n % 15 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)


print([fizzbuzz(n) for n in [1, 2, 3, 5, 9, 10, 15, 30, 31]])
```

Output:

```text
['1', '2', 'Fizz', 'Buzz', 'Fizz', 'Buzz', 'FizzBuzz', 'FizzBuzz', '31']
```

*Variations.* Put the `n % 3` test first and watch 15 become `"Fizz"` (the ordering mistake from [The elif Ladder](14-conditional-statements.md#the-elif-ladder)). Write a version with two separate `if` statements that build the text piece by piece (`"Fizz"` plus `"Buzz"`), without testing `n % 15` at all.

**Problem 6: password strength.** Score a password by these rules: at least 8 characters gives 1 point; containing a digit gives 1; containing an uppercase letter gives 1; containing a lowercase letter gives 1; containing a symbol (a character that is not a letter or digit) gives 1. A score of 5 is `"strong"`, 3 or 4 is `"medium"`, otherwise `"weak"`.

*Thinking.* Each rule is independent, so use separate `if` statements that add to a score. Scan the characters once with flags, using the string methods from [String Methods](10-ord-chr-and-string-methods.md#string-methods).

```python
def password_strength(password):
    has_digit = False
    has_upper = False
    has_lower = False
    has_symbol = False
    for character in password:
        if character.isdigit():
            has_digit = True
        elif character.isupper():
            has_upper = True
        elif character.islower():
            has_lower = True
        elif not character.isalnum():
            has_symbol = True

    score = 0
    if len(password) >= 8:
        score += 1
    if has_digit:
        score += 1
    if has_upper:
        score += 1
    if has_lower:
        score += 1
    if has_symbol:
        score += 1

    if score == 5:
        label = "strong"
    elif score >= 3:
        label = "medium"
    else:
        label = "weak"
    return score, label


for candidate in ["abc", "password", "Password1", "Passw0rd!", "12345678"]:
    print(f"{candidate!r:12}", password_strength(candidate))
```

Output:

```text
'abc'        (1, 'weak')
'password'   (2, 'weak')
'Password1'  (4, 'medium')
'Passw0rd!'  (5, 'strong')
'12345678'   (2, 'weak')
```

*Why it works.* The loop sets a flag when it sees each kind of character. The `elif` chain inside the loop is safe because one character belongs to exactly one kind. The score is built by independent `if` statements, and a final ladder turns the score into a label. *Note.* This is a teaching exercise: real password policies and checks (length, breach lists, no reuse) are different, and a strength label from a few rules is only a rough hint. Never store or print real passwords.

**Problem 7: calculator with error handling.** Write `calculate(a, operator, b)` for `+`, `-`, `*`, `/`, `//`, `%` and `**`. Return an error message for an unknown operator or for division by zero.

*Thinking.* One ladder over the operator; a guard for zero divisors in the three division-like operations.

```python
def calculate(a, operator, b):
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator in ("/", "//", "%"):
        if b == 0:
            return "error: division by zero"
        if operator == "/":
            return a / b
        elif operator == "//":
            return a // b
        else:
            return a % b
    elif operator == "**":
        return a ** b
    else:
        return "error: unknown operator " + repr(operator)


tests = [(7, "+", 3), (7, "-", 3), (7, "*", 3), (7, "/", 2), (7, "//", 2),
         (7, "%", 2), (7, "**", 2), (7, "/", 0), (7, "&", 2)]
for a, operator, b in tests:
    print(a, operator, b, "=", calculate(a, operator, b))
```

Output:

```text
7 + 3 = 10
7 - 3 = 4
7 * 3 = 21
7 / 2 = 3.5
7 // 2 = 3
7 % 2 = 1
7 ** 2 = 49
7 / 0 = error: division by zero
7 & 2 = error: unknown operator '&'
```

*Why it works.* The three operators that can divide by zero are grouped, so the zero check is written once (a nested `if` inside the ladder). The `else` at the end catches every unknown operator, so the function always returns something. *Variation:* replace the ladder with a dictionary of functions after reading [Functions as First-Class Citizens](28-first-class-functions-and-lambda.md#functions-as-first-class-citizens).

**7. Example 3 — Edge case or common mistake**

**Problem 8: rock, paper, scissors.** Given two moves `"rock"`, `"paper"` or `"scissors"`, return `"draw"`, `"player 1 wins"`, `"player 2 wins"` or `"invalid move"`.

*Thinking.* Validate first. Then a draw is easy (`a == b`). Otherwise, player 1 wins in exactly three combinations; everything else is a win for player 2.

```python
def play(move1, move2):
    moves = ("rock", "paper", "scissors")
    if move1 not in moves or move2 not in moves:
        return "invalid move"
    if move1 == move2:
        return "draw"
    if (move1 == "rock" and move2 == "scissors") or \
       (move1 == "scissors" and move2 == "paper") or \
       (move1 == "paper" and move2 == "rock"):
        return "player 1 wins"
    return "player 2 wins"


for pair in [("rock", "scissors"), ("paper", "rock"), ("rock", "paper"),
             ("paper", "paper"), ("rock", "lizard")]:
    print(pair, play(*pair))
```

Output:

```text
('rock', 'scissors') player 1 wins
('paper', 'rock') player 1 wins
('rock', 'paper') player 2 wins
('paper', 'paper') draw
('rock', 'lizard') invalid move
```

*Why it works.* The backslash `\` at the end of a line continues the condition on the next line (brackets alone also allow a line break). The validity check comes first, so unknown words never reach the win rules. `play(*pair)` unpacks the pair into two arguments (see [Function Arguments](26-function-arguments.md)).

**Typical mistakes seen in these problems.** Here are three of them, each shown with a fix.

*Boundary mistakes.* The rule "children under 12 pay half price" means 12 itself pays full price. Writing `<= 12` changes the meaning for exactly one age, which no ordinary test will notice:

```python
def child_price_wrong(age):
    return 50 if age <= 12 else 100


def child_price_right(age):
    return 50 if age < 12 else 100


for age in [11, 12, 13]:
    print(age, child_price_wrong(age), child_price_right(age))
```

Output:

```text
11 50 50
12 50 100
13 100 100
```

*Order mistakes.* A ladder that tests the general case first never reaches the specific one:

```python
def classify(n):
    if n % 3 == 0:
        return "Fizz"
    elif n % 15 == 0:
        return "FizzBuzz"
    return str(n)


print(classify(15), classify(9), classify(10))
```

Output:

```text
Fizz Fizz 10
```

`15` is reported as `Fizz` because the `n % 15` branch can never be reached.

*Comparing with the wrong type.* Data from files and forms arrives as text. Comparing text with numbers silently gives wrong decisions or raises an error:

```python
age_text = "7"

print(age_text == 7)
print(age_text >= "18")
print(int(age_text) >= 18)
```

Output:

```text
False
True
False
```

`"7" >= "18"` is `True` as text, because `"7"` is greater than `"1"`, but 7 is not greater than 18 as numbers. Convert first (see [Explicit Type Casting](08-type-conversion.md#explicit-type-casting)).

**8. Common mistakes**

- Choosing `<` or `<=` without checking what the rule says about the boundary value.
- Ordering a ladder from the general case to the specific one.
- Using `elif` where several independent conditions can apply (tax slabs, password rules), or separate `if` statements where only one should (grades).
- Forgetting the invalid-input case or the `else`.
- Using `print` inside the function instead of `return`, which makes the result hard to test.
- Testing only one or two ordinary values and not the boundaries.
- Comparing text with numbers.

**9. Real-world and AI applications**

All of these problems are miniature versions of real rules engines: pricing and billing tiers, tax and eligibility checks, password and input validation, game logic and calculator parsers. AI systems use the same patterns when they validate user prompts, route requests by type, apply content or length limits, or decide what to do with a model's output (accept, retry, escalate). A small, well-tested function per rule is how such systems stay maintainable, and boundary tests are the cheapest way to find bugs.

**10. Practice**

Do these without looking at the answers. Each exercise has a solution in the answers section.

1. Write `shipping_cost(weight_kg)`: up to 1 kg costs 40, above 1 kg and up to 5 kg costs 90, above 5 kg and up to 20 kg costs 150, heavier parcels are rejected (return `None`); weights of zero or less are invalid (return `None`).
2. Write `days_in_month(month, year)` for months 1 to 12, using the leap-year rule for February; return `None` for an invalid month.
3. Write `time_greeting(hour)` for the 24-hour clock: `"Good morning"` for 5 to 11, `"Good afternoon"` for 12 to 16, `"Good evening"` for 17 to 20, `"Good night"` otherwise, and `"invalid hour"` outside 0 to 23.
4. Write `quadrant(x, y)` that returns `"origin"`, `"x-axis"`, `"y-axis"`, or `"quadrant 1"` to `"quadrant 4"` for a point.
5. Write `can_ride(age, height_cm, accompanied)`: a ride requires height of at least 120 cm; children under 10 need to be accompanied by an adult; people aged 65 and above are not allowed on this ride. Return a reason when the answer is no.
6. Write `bmi_advice(weight_kg, height_m)` that calculates BMI (weight divided by height squared), returns `"invalid"` for non-positive inputs, and otherwise classifies as in [The elif Ladder](14-conditional-statements.md#the-elif-ladder).

**11. Interview questions**

- *How do you decide between `elif` and separate `if` statements?* If the outcomes are mutually exclusive, use one chain; if several rules can apply together, use separate `if` statements.
- *How do you test a conditional function?* Test the values on each side of every boundary, plus typical and invalid values.
- *Why return values from functions instead of printing?* A returned value can be tested, reused and combined; printed text cannot.
- *What is a guard clause?* An early check for invalid or special input that returns at once, so the main logic is not nested.

**12. Quick revision**

- Translate the rule into outcomes, thresholds and boundary decisions before writing code.
- Ladders go from specific to general; independent rules use separate `if` statements.
- Validate input first; always handle the "none of the above" case.
- Return results from functions; test boundaries.
- Convert text to numbers before comparing.

---

## Answers to Practice Exercises

### Answers: Conditionals: Practice Problems

**Exercise 1: shipping cost.**

```python
def shipping_cost(weight_kg):
    if weight_kg <= 0 or weight_kg > 20:
        return None
    if weight_kg <= 1:
        return 40
    elif weight_kg <= 5:
        return 90
    else:
        return 150


for weight in [0, 0.5, 1, 1.01, 5, 5.5, 20, 21]:
    print(weight, shipping_cost(weight))
```

Output:

```text
0 None
0.5 40
1 40
1.01 90
5 90
5.5 150
20 150
21 None
```

The guard clause rejects invalid and too-heavy parcels first, so the ladder can assume the weight is between 0 (excluded) and 20.

**Exercise 2: days in month.**

```python
def days_in_month(month, year):
    if month < 1 or month > 12:
        return None
    if month == 2:
        leap = (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
        return 29 if leap else 28
    if month in (4, 6, 9, 11):
        return 30
    return 31


print(days_in_month(2, 2024), days_in_month(2, 1900), days_in_month(4, 2025))
print(days_in_month(12, 2025), days_in_month(13, 2025))
```

Output:

```text
29 28 30
31 None
```

**Exercise 3: greeting.**

```python
def time_greeting(hour):
    if hour < 0 or hour > 23:
        return "invalid hour"
    if 5 <= hour <= 11:
        return "Good morning"
    elif 12 <= hour <= 16:
        return "Good afternoon"
    elif 17 <= hour <= 20:
        return "Good evening"
    else:
        return "Good night"


for hour in [-1, 0, 4, 5, 11, 12, 16, 17, 20, 21, 23, 24]:
    print(hour, time_greeting(hour))
```

Output:

```text
-1 invalid hour
0 Good night
4 Good night
5 Good morning
11 Good morning
12 Good afternoon
16 Good afternoon
17 Good evening
20 Good evening
21 Good night
23 Good night
24 invalid hour
```

**Exercise 4: quadrant.**

```python
def quadrant(x, y):
    if x == 0 and y == 0:
        return "origin"
    if y == 0:
        return "x-axis"
    if x == 0:
        return "y-axis"
    if x > 0 and y > 0:
        return "quadrant 1"
    if x < 0 and y > 0:
        return "quadrant 2"
    if x < 0 and y < 0:
        return "quadrant 3"
    return "quadrant 4"


for point in [(0, 0), (3, 0), (0, -2), (2, 5), (-2, 5), (-2, -5), (2, -5)]:
    print(point, quadrant(*point))
```

Output:

```text
(0, 0) origin
(3, 0) x-axis
(0, -2) y-axis
(2, 5) quadrant 1
(-2, 5) quadrant 2
(-2, -5) quadrant 3
(2, -5) quadrant 4
```

The special cases (origin and axes) come first; after them, the signs of `x` and `y` are both non-zero, so the last `return` can safely mean quadrant 4.

**Exercise 5: ride eligibility.**

```python
def can_ride(age, height_cm, accompanied):
    if age >= 65:
        return False, "not allowed for ages 65 and above"
    if height_cm < 120:
        return False, "too short"
    if age < 10 and not accompanied:
        return False, "needs an accompanying adult"
    return True, "ok"


print(can_ride(30, 170, False))
print(can_ride(70, 170, False))
print(can_ride(30, 110, False))
print(can_ride(9, 125, False))
print(can_ride(9, 125, True))
```

Output:

```text
(True, 'ok')
(False, 'not allowed for ages 65 and above')
(False, 'too short')
(False, 'needs an accompanying adult')
(True, 'ok')
```

Each rule is a guard clause that returns a reason; the final `return` is reached only when no rule blocks the ride.

**Exercise 6: BMI advice.**

```python
def bmi_advice(weight_kg, height_m):
    if weight_kg <= 0 or height_m <= 0:
        return "invalid"
    bmi = weight_kg / height_m ** 2
    if bmi < 18.5:
        category = "underweight"
    elif bmi < 25:
        category = "normal"
    elif bmi < 30:
        category = "overweight"
    else:
        category = "obese"
    return round(bmi, 1), category


print(bmi_advice(50, 1.70))
print(bmi_advice(70, 1.75))
print(bmi_advice(95, 1.70))
print(bmi_advice(0, 1.70))
```

Output:

```text
(17.3, 'underweight')
(22.9, 'normal')
(32.9, 'obese')
invalid
```

`height_m ** 2` is evaluated before the division, because `**` has higher precedence (see [Operator Precedence and Associativity](13-identity-operators-and-precedence.md#operator-precedence-and-associativity)). BMI is a rough screening number and not a medical diagnosis.

---

## Chapter Summary and Key Takeaways

- Read each rule precisely: list the outcomes, the thresholds, and which side of each boundary a boundary value belongs to.
- Use an `elif` ladder for mutually exclusive outcomes (ordered from specific to general) and separate `if` statements for independent rules such as tax slabs or password checks.
- Validate input first with guard clauses; finish ladders with an `else` for the leftover case.
- Return results from functions so they can be tested; test the values on both sides of every boundary.
- Convert text to numbers before comparing, and keep `<` versus `<=` decisions deliberate.

Next: [Chapter 16 — while Loops and Loop Control](16-while-loop-and-loop-control.md) shows how to repeat work until a condition changes.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
