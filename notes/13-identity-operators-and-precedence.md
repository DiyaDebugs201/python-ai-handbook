# Chapter 13 — Identity Operators and Operator Precedence

> Part 3 — Operators and Control Flow · Video: 2:58:11–3:13:46 · Previous: [12 Relational, Logical and Assignment Operators](12-relational-logical-assignment-operators.md) · Next: [14 Conditional Statements](14-conditional-statements.md)

**In this chapter:** the identity operators `is` and `is not` and how they differ from `==`, why using `is` to compare numbers or strings can give misleading answers, the one place where `is` is the right tool (`is None`), and the rules of operator precedence and associativity that decide how an expression with several operators is evaluated.

**Before you start:** you need the comparison operators from [Relational Operators](12-relational-logical-assignment-operators.md#relational-operators) and the idea that a name refers to an object (see [Assignment Operators](12-relational-logical-assignment-operators.md#assignment-operators)). Recap: every value in Python is an object stored somewhere in memory; a variable is a name that refers to such an object; two names can refer to the same object. Examples were run with Python 3.13. Behaviour that depends on the CPython implementation (the standard Python interpreter) is marked as such.

---

## Identity Operators: is versus Equality

**Timestamp:** [2:58:11](https://www.youtube.com/watch?v=J9BI0jGOds8&t=10691s)

**Learning objectives:**

- Explain the difference between equality (`==`, same value) and identity (`is`, same object).
- Use `id()` to look at object identity.
- Explain why `is` can seem to work for small numbers and some strings, and why you must not rely on it.
- Use `is None` and `is not None` correctly.

**1. Intuition**

Two identical-looking books on a shelf are *equal* in content, but they are two separate physical books. Two names for the same book (a bookmark in each of two lists pointing to the same copy) are the *same* object. Equality asks, "do these have the same content?" Identity asks, "are these literally the same thing?"

**2. Why does it exist?**

Sometimes you need to know whether two names point to the same object, for example when a change through one name might show up through the other (shared lists), or when you need to test for a unique marker such as `None`. Equality cannot answer that, because two different objects can have equal content.

**3. Technical explanation**

- `a == b` is true when the *values* of `a` and `b` are equal, as decided by the type of the objects. Two different lists with the same items are equal.
- `a is b` is true when `a` and `b` refer to the *same object*. In CPython this is the same as comparing the numbers returned by `id()`, which identify an object during its lifetime.
- `a is not b` is the negation of `a is b`.

If `a is b` is true, then `a == b` is almost always true as well (the exceptions are special values such as `nan`, which is not equal to itself). The reverse is not true.

*Why `is` appears to work on small numbers.* CPython keeps ready-made objects for the integers from -5 to 256, and reuses them. So two separate computations that produce `256` give the same object, and `is` returns `True`. For bigger numbers, each computation usually creates a new object, and `is` returns `False`. The same kind of reuse (called interning) exists for some strings, especially short strings that look like identifiers. These are implementation details of CPython. They can differ between versions and between other Python implementations, and the compiler may also merge identical constants written in the same piece of code. Therefore: **never use `is` to compare numbers, strings or other values for equality. Use `==`.**

*Singletons.* `None`, `True` and `False` each exist as exactly one object in the whole program. For these, `is` is the correct and fast test, and `x is None` is the standard way to check for "no value". PEP 8, Python's style guide, says comparisons to singletons such as `None` should be done with `is` or `is not`, never with the equality operators.

*Literals and warnings.* Since Python 3.8, using `is` with a literal on one side (such as `x is 5` or `x is "a"`) produces a `SyntaxWarning`, because the result is unreliable; the wording of the message depends on the version. The warning is printed when the code is compiled, even though the program continues.

*Mutable objects.* For lists, dictionaries and sets, identity matters in practice. Two names for the same list share changes. Two lists with equal content do not. `copy` operations create a new object, so the copy `is not` the original but `==` it (see [Copying Lists](19-list-functions-methods-and-copying.md#copying-lists)).

**4. Syntax**

```text
a is b
a is not b
id(a)
```

This is a pattern, not runnable code. `is` and `is not` have the same precedence as the comparison operators and can be chained, though that is rarely useful.

**5. Example 1 — Basic**

```python
x = [1, 2, 3]
y = [1, 2, 3]
z = x

print(x == y)
print(x is y)
print(x is z)
print(id(x) == id(z), id(x) == id(y))

z.append(4)
print(x)
print(y)

a = None
print(a is None, a is not None)
print(type(None))
```

Output:

```text
True
False
True
True False
[1, 2, 3, 4]
[1, 2, 3]
True False
<class 'NoneType'>
```

Line by line:

- `x == y` is `True`: both lists hold the same items.
- `x is y` is `False`: they are two separate list objects, created by two separate list expressions.
- `x is z` is `True`, because `z = x` did not copy anything; it made a second name for the same list.
- `id(x) == id(z)` confirms that: the same identity number. The actual numbers differ on every run, so they are compared rather than printed.
- Appending through `z` changes `x` too, since both names refer to one list, while `y` is untouched.
- `a is None` is the standard test for "no value". `None` is the only value of the type `NoneType`.

**6. Example 2 — Practical**

Using `is None` to tell "no argument given" from a real value, and using `is` to detect aliases:

```python
def describe(value=None):
    if value is None:
        return "no value given"
    return f"value is {value!r}"


print(describe())
print(describe(0))
print(describe(""))
print(describe([]))
print(describe(None))


def append_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items


first = append_item("a")
second = append_item("b")
shared = append_item("c", first)
print(first, second, shared)
print(shared is first, second is first)
```

Output:

```text
no value given
value is 0
value is ''
value is []
no value given
['a', 'c'] ['b'] ['a', 'c']
True False
```

Line by line:

- `value is None` is `True` only when no argument (or `None`) was passed. A test such as `if not value:` would wrongly treat `0`, `""` and `[]` as "missing" (see [Logical Operators](12-relational-logical-assignment-operators.md#logical-operators)).
- In `append_item`, the default is `None` and a new list is created inside the function. This is the safe pattern for optional mutable arguments, explained in [Function Arguments](26-function-arguments.md).
- `first` and `second` are separate lists, because each call without `items` created a new one. `shared` is the same list as `first`, because the function received `first` and returned that same object.

**7. Example 3 — Edge case or common mistake**

Using `is` on numbers and strings gives answers that look right until they do not:

```python
a = int("256")
b = int("256")
print(a is b, a == b)

c = int("257")
d = int("257")
print(c is d, c == d)

s1 = "hello"
s2 = "".join(["hel", "lo"])
print(s1 == s2, s1 is s2)

one = int("1")
print(one == True, one is True)
first = []
second = []
print(first == second, first is second)
```

Output:

```text
True True
False True
True False
True False
True False
```

The two numbers are computed separately (with `int()`), so the compiler cannot merge them. `256` is cached by CPython, so `a is b` is `True`; `257` is not, so `c is d` is `False`. Both pairs are equal. The string built at run time is equal to `"hello"` but is a different object. The number `1` is equal to `True` (a `bool` is a kind of `int`), but it is not the same object as `True`. Two separately created empty lists are equal but not the same object.

The numbers shown are specific to CPython 3.13. You should never write a program whose behaviour depends on them. Python warns you when you try, at compile time. For example, a file containing

```text
x = 5
print(x is 5)
```

prints a warning like the following on Python 3.13 (the exact words differ between versions) and then still runs:

```text
example.py:2: SyntaxWarning: "is" with 'int' literal. Did you mean "=="?
```

Another subtle case is the compiler merging identical constants. In the same piece of code, `(1, 2) is (1, 2)` may be `True` because the compiler stores one copy of the constant tuple, while a tuple built at run time (`tuple([1, 2]) is tuple([1, 2])`) would not be. This is another reason why identity comparisons of values are unreliable.

The correct rule of thumb:

| Question | Use |
|----------|-----|
| Are these two values the same? | `==` |
| Is this value missing (`None`)? | `is None` |
| Are these two names for one object (aliases)? | `is` |

**8. Common mistakes**

- Using `is` to compare numbers, strings or lists for equality.
- Using `== None` instead of `is None`. It usually works, but a class can define `==` in a way that makes it wrong, and `is` is faster and clearer.
- Forgetting that `b = a` does not copy a list: `b is a` is `True`.
- Assuming `a is b` implies different content is impossible (it is the same object, so content is always the same).
- Treating the cached small-integer behaviour as a rule.
- Writing `if x is not None == True` and similar chained mixtures; keep identity tests simple.

**9. Real-world and AI applications**

`is None` is everywhere: optional function arguments, "not found" results from lookups, the initial state of a variable that is filled later, sentinel markers in configuration. In AI and data code, identity checks help to confirm that two model components share the very same weights object (weight tying) or that a copy really is independent from the original (`copy is not original`) before changing it. Many hard-to-find bugs in data pipelines are aliasing bugs: a "copy" that is secretly the same list or array, so a change to one silently changes the other.

**10. Practice**

1. Create `a = [1, 2]`, `b = a`, `c = [1, 2]`. Predict `a == c`, `a is c`, `a is b`, then check.
2. Write `first_or_default(items, default=None)` that returns the first item of a list, or `default` if the list is empty. Use `is None` appropriately and test with `[0, 1]`, `[]` and `[]` with `default="none"`.
3. What is wrong with `if name is "admin":`? Rewrite it correctly.
4. Make a copy of a list with `.copy()` and show that the copy is equal to, but not identical with, the original.
5. Explain why `int("256") is int("256")` and `int("257") is int("257")` can differ, and why you should not depend on it.

**11. Interview questions**

- *What is the difference between `is` and `==`?* `==` compares values; `is` compares identity (whether both names refer to the same object).
- *Why should you use `is None` and not `== None`?* `None` is a singleton, so identity is the exact test; `==` can be overridden by a class and may give a different answer.
- *Why can `a is b` be `True` for small integers but `False` for large ones?* CPython caches small integers (-5 to 256); this is an implementation detail and not part of the language guarantee.
- *Does `b = a` copy a list?* No. Both names refer to the same list.

**12. Quick revision**

- `==` is about value, `is` is about identity; `id()` shows identity.
- Use `is None` / `is not None`; use `==` for everything else.
- Small-integer and string caching make `is` misleading; Python 3.8+ warns about `is` with literals.
- `b = a` creates an alias, not a copy.
- Equal objects need not be identical; identical objects are always equal (except `nan`).

---

## Operator Precedence and Associativity

**Timestamp:** [3:06:08](https://www.youtube.com/watch?v=J9BI0jGOds8&t=11168s)

**Learning objectives:**

- Explain what precedence and associativity mean.
- Use the precedence table to predict the value of mixed expressions.
- Recognise the surprising cases: `-2 ** 2`, `2 ** 3 ** 2`, `not a == b`, chained comparisons.
- Use brackets to make an expression unambiguous.

**1. Intuition**

In arithmetic at school you learned that multiplication comes before addition: `2 + 3 * 4` is 14. That rule is *precedence*: which operator gets its operands first. When two operators have the same level, a second rule decides the direction, *associativity*: `10 - 4 - 3` is `(10 - 4) - 3`, working from left to right. Python follows these rules for every operator, not only the arithmetic ones.

**2. Why does it exist?**

Without a fixed rule, `2 + 3 * 4` would be ambiguous. Precedence lets short formulas be written the way mathematicians write them, and it makes programs predictable.

**3. Technical explanation**

*Precedence.* The operator with higher precedence is applied first. The table below goes from the lowest precedence (applied last) at the top to the highest (applied first) at the bottom. It is based on the "Operator precedence" section of the official Python language reference. Operators in the same row have the same precedence.

| Level | Operators | Notes |
|------:|-----------|-------|
| 1 (lowest) | `:=` | assignment expression |
| 2 | `lambda` | anonymous function |
| 3 | `x if condition else y` | conditional expression |
| 4 | `or` | logical or |
| 5 | `and` | logical and |
| 6 | `not x` | logical not |
| 7 | `in`, `not in`, `is`, `is not`, `<`, `<=`, `>`, `>=`, `!=`, `==` | comparisons, identity and membership; they can be chained |
| 8 | `\|` | bitwise or |
| 9 | `^` | bitwise xor |
| 10 | `&` | bitwise and |
| 11 | `<<`, `>>` | shifts |
| 12 | `+`, `-` | addition and subtraction |
| 13 | `*`, `@`, `/`, `//`, `%` | multiplication, matrix multiplication, division, floor division, remainder |
| 14 | `+x`, `-x`, `~x` | unary plus, minus and bitwise not |
| 15 | `**` | power |
| 16 | `await x` | used with asynchronous code |
| 17 | `x[index]`, `x[start:stop]`, `x(arguments)`, `x.attribute` | subscription, slicing, calls, attribute access |
| 18 (highest) | `(expressions)`, `[...]`, `{...}` | brackets, list, dict and set displays |

(The statement `=` and the augmented assignments such as `+=` are not operators in expressions, so they are not in this table. They are applied after the whole right-hand side has been evaluated.)

*Associativity.* For operators at the same level:

- Most binary operators are *left-associative*: they group from the left. `10 - 4 - 3` is `(10 - 4) - 3 = 3`, and `100 / 10 / 5` is `(100 / 10) / 5 = 2.0`.
- `**` is *right-associative*: `2 ** 3 ** 2` is `2 ** (3 ** 2) = 512`.
- A conditional expression is right-associative: `a if c1 else b if c2 else c` is `a if c1 else (b if c2 else c)`.
- Comparisons are special. They *chain*: `a < b < c` means `a < b and b < c`. They are not simply grouped left or right.

*Special details about `**` and unary operators.* `**` binds more tightly than a unary minus on its left, but a unary operator on its right side is applied first. So `-2 ** 2` is `-(2 ** 2) = -4`, while `2 ** -1` is `2 ** (-1) = 0.5`.

*`not` and comparisons.* Because `not` has lower precedence than `==`, `not a == b` means `not (a == b)`. And `and` has higher precedence than `or`, so `a or b and c` means `a or (b and c)`.

*Brackets.* Brackets override every rule, and they cost nothing. If you have to look up the order, add brackets so that the next reader does not have to.

**4. Syntax**

```text
(expression)    groups part of an expression so it is evaluated first
```

This is a pattern, not runnable code. There is no special syntax for precedence; it is the grammar of the language.

**5. Example 1 — Basic**

```python
print(2 + 3 * 4)
print((2 + 3) * 4)
print(10 - 4 - 3)
print(100 / 10 / 5)
print(2 * 3 % 4)
print(2 + 3 * 4 ** 2)
print(2 ** 3 ** 2, (2 ** 3) ** 2)
print(-2 ** 2, (-2) ** 2, 2 ** -1)
print(10 // 3 * 3 + 10 % 3)
print(7 - 2 * 3 ** 2 // 4)
```

Output:

```text
14
20
3
2.0
2
50
512 64
-4 4 0.5
10
3
```

Line by line:

- `2 + 3 * 4`: multiplication first (12), then addition (14). With brackets, the addition happens first (20).
- `10 - 4 - 3` groups from the left: `(10 - 4) - 3 = 3`. Grouped from the right it would be `10 - (4 - 3) = 9`, so the direction matters. Likewise `100 / 10 / 5 = 2.0`.
- `2 * 3 % 4`: `*` and `%` are at the same level, so left to right: `(2 * 3) % 4 = 6 % 4 = 2`.
- `2 + 3 * 4 ** 2`: power first (16), then multiplication (48), then addition (50).
- `2 ** 3 ** 2` is `2 ** 9 = 512`; with brackets the left power happens first: `8 ** 2 = 64`.
- `-2 ** 2` is `-4`, `(-2) ** 2` is `4`, and `2 ** -1` is `0.5`.
- `10 // 3 * 3 + 10 % 3`: `(10 // 3) * 3 + (10 % 3) = 9 + 1 = 10`, which rebuilds the original number from quotient and remainder.
- `7 - 2 * 3 ** 2 // 4`: `3 ** 2 = 9`, then `2 * 9 = 18`, then `18 // 4 = 4`, then `7 - 4 = 3`.

**6. Example 2 — Practical**

Mixed arithmetic, comparison and logic in realistic expressions, and the cure (brackets and named intermediate values):

```python
price = 200
quantity = 3
discount_percent = 10
tax_percent = 5

total_unclear = price * quantity - price * quantity * discount_percent / 100 + 5
subtotal = price * quantity
discount = subtotal * discount_percent / 100
total_clear = subtotal - discount + tax_percent
print(total_unclear, total_clear)

celsius = 37
print(celsius * 9 / 5 + 32)
print(celsius * 9 / (5 + 32))

age = 25
income = 20000
has_guarantor = False
print(age > 18 and income > 15000 or has_guarantor)
print(age > 18 and (income > 15000 or has_guarantor))
print(not age > 30)
print(1 + 2 < 4 and 3 > 1)
print(1 or 0 and 0)

x = 5
label = "big" if x > 10 else "medium" if x > 3 else "small"
print(label)
```

Output:

```text
545.0 545.0
98.6
9.0
True
True
True
True
1
medium
```

Line by line:

- In the bill, every `*` and `/` runs before the `+` and `-`. Both versions give the same number, but the second with named steps is much easier to check. (The 5 added at the end is just a fixed fee used for the example.)
- `celsius * 9 / 5 + 32` is the correct Fahrenheit formula; with the wrong brackets, `9 / (5 + 32)` gives a different, wrong answer (the logic error from [Errors: Syntax vs Runtime](04-errors-and-identifiers.md#errors-syntax-vs-runtime)).
- `age > 18 and income > 15000 or has_guarantor` means `((age > 18) and (income > 15000)) or has_guarantor` because `and` binds tighter than `or`. Here both ways give `True`, but with other values they would differ, so use brackets to state your intention.
- `not age > 30` is `not (age > 30)` because `not` is lower than `>`.
- Arithmetic is evaluated before comparison, and comparison before `and`, so `1 + 2 < 4 and 3 > 1` reads as `((1 + 2) < 4) and (3 > 1)`.
- `1 or 0 and 0` is `1 or (0 and 0)`, which is `1`.
- The conditional expression chain is read from the right: `"big" if x > 10 else ("medium" if x > 3 else "small")`.

**7. Example 3 — Edge case or common mistake**

Expressions that look obvious and are not:

```python
print(not True == False)
print((not True) == False)
print(5 > 3 > 1 == 1)
print(1 in [1] == True)
print(True + True * 3)
print(2 ** 3 ** 0)
print(6 & 3 | 8, 1 << 2 + 1)
print(-3 ** 2, (-3) ** 2)
```

Output:

```text
True
True
True
False
4
2
10 8
-9 9
```

What happened:

- `not True == False` is `not (True == False)`, which is `not False`, so `True`. The version with brackets, `(not True) == False`, is `False == False`, which is also `True`. With Booleans the two forms always agree, so the next example uses numbers to show the difference.
- `5 > 3 > 1 == 1` is a chain: `5 > 3 and 3 > 1 and 1 == 1`, which is `True`.
- `1 in [1] == True` is also a chain: `(1 in [1]) and ([1] == True)`, which is `False`, because a list is never equal to `True`. A beginner expects `True`.
- `True + True * 3` is `1 + 1 * 3 = 4`, because `bool` is a kind of `int`.
- `2 ** 3 ** 0` is `2 ** (3 ** 0) = 2 ** 1 = 2`.
- `6 & 3 | 8` is `(6 & 3) | 8 = 2 | 8 = 10`, because `&` binds tighter than `|`. `1 << 2 + 1` is `1 << 3 = 8`, because `+` binds tighter than `<<`: a trap for people who think of shifts as multiplication.
- `-3 ** 2` is `-9`, but `(-3) ** 2` is `9`.

Because these results are hard to predict by reading, the practical rule is: **use brackets whenever more than two operator levels appear in one expression, and split long expressions into named steps.**

Booleans hide the difference between `not a == b` and `(not a) == b`; numbers reveal it:

```python
a = 0
b = 5
print(not a == b)
print((not a) == b)
```

Output:

```text
True
False
```

`not a == b` is read as `not (a == b)`: `0 == 5` is `False`, and `not False` is `True`. The bracketed form `(not a) == b` first computes `not 0`, which is `True`, and then compares `True == 5`, which is `False`. The same text with and without brackets gives different answers, which is why precedence matters.

**8. Common mistakes**

- Expecting `-x ** 2` to square a negative number.
- Expecting `**` to group from the left.
- Writing `a or b and c` without brackets and meaning `(a or b) and c`.
- Writing `not a == b` and meaning `(not a) == b`.
- Assuming `<<` and `>>` bind more tightly than `+` and `-` (they bind less tightly).
- Writing very long one-line formulas that nobody can check.
- Mixing `&`/`|` with comparisons without brackets (in pandas, `df.a > 1 & df.b < 2` fails; each comparison needs its own brackets).
- Forgetting that comparisons chain.

**9. Real-world and AI applications**

Readable formulas depend on precedence. Mean-squared error, softmax and learning-rate decay written in code must follow the right order of operations, and a missing bracket is a typical source of silent logic errors. In pandas and NumPy, filters such as `(df["age"] > 30) & (df["city"] == "Pune")` need brackets, because `&` has higher precedence than the comparison operators. Code reviewers regularly ask for brackets or intermediate variables for exactly the cases in this chapter.

**10. Practice**

1. Evaluate by hand, then check: `4 + 6 / 2 * 3`, `2 ** 2 ** 3`, `-4 ** 2`, `15 // 4 + 15 % 4`, `not 0 or 1 and 0`.
2. Insert brackets to show how Python reads `a + b * c ** d - e / f` and `x or y and not z`.
3. Rewrite `price = base - base * discount / 100 + shipping` with named intermediate steps.
4. Write the expression for the average of three numbers `a`, `b`, `c` correctly, and show the common mistake `a + b + c / 3`.
5. Without running it, say whether `1 + 1 << 2` is 6 or 8, then check. Explain why.
6. Why does `df.age > 30 & df.city == "Pune"` cause trouble in pandas (conceptually), and how do you fix it?

**11. Interview questions**

- *What is operator precedence?* The rule that decides which operator is applied first when an expression contains several different operators.
- *What is associativity?* The rule that decides the grouping direction when operators of the same precedence are chained; most are left-to-right, but `**` is right-to-left.
- *What is `-2 ** 2`?* `-4`, because `**` has higher precedence than unary minus on its left.
- *Which binds more tightly: `and` or `or`?* `and`.
- *How should you deal with complicated expressions?* Use brackets and intermediate variables for clarity.

**12. Quick revision**

- High to low: brackets and calls, `**`, unary `-`, `* / // %`, `+ -`, shifts, `&`, `^`, `|`, comparisons (and `is`, `in`), `not`, `and`, `or`, conditional expression, `lambda`.
- Same level: left to right, except `**` (right to left); comparisons chain.
- `-2 ** 2` is `-4`; `2 ** 3 ** 2` is `512`; `not a == b` is `not (a == b)`.
- Brackets cost nothing; use them.

---

## Answers to Practice Exercises

### Answers: Identity Operators: is versus Equality

1. `a == c` is `True` (same content); `a is c` is `False` (two separate lists); `a is b` is `True` (an alias).

```python
a = [1, 2]
b = a
c = [1, 2]
print(a == c, a is c, a is b)
```

Output:

```text
True False True
```

2.

```python
def first_or_default(items, default=None):
    if len(items) == 0:
        return default
    return items[0]


print(first_or_default([0, 1]))
print(first_or_default([]))
print(first_or_default([], default="none"))
print(first_or_default([]) is None)
```

Output:

```text
0
None
none
True
```

The first call returns `0`, which is a perfectly good value; testing `if items[0]:` or `items or default` would have treated it as "missing". The last line uses `is None` to check the default result.

3. `name is "admin"` compares identity, not content. It may work by accident when both strings are cached, and fail when the string comes from user input, a file or a calculation. Python also warns about it. The correct version is `if name == "admin":`.

```python
typed = "".join(["ad", "min"])
print(typed == "admin", typed is "admin")
```

This code is valid, but Python 3.8 and later warn about `is` with a literal when it is compiled. Output (and the warning is printed separately on stderr):

```text
True False
```

4.

```python
original = [3, 1, 2]
duplicate = original.copy()
print(duplicate == original, duplicate is original)

duplicate.append(9)
print(original, duplicate)
```

Output:

```text
True False
[3, 1, 2] [3, 1, 2, 9]
```

5. `int("256")` creates (or returns) the cached object for 256, so two calls return the same object. `int("257")` creates a new object each time, so the two results are equal but not identical. This caching is an implementation detail of CPython (and its range can change), so never rely on `is` for numbers.

### Answers: Operator Precedence and Associativity

1. `4 + 6 / 2 * 3`: `6 / 2` is `3.0`, `3.0 * 3` is `9.0`, `4 + 9.0` is `13.0`. `2 ** 2 ** 3` is `2 ** 8 = 256`. `-4 ** 2` is `-16`. `15 // 4 + 15 % 4` is `3 + 3 = 6`. `not 0 or 1 and 0` is `(not 0) or (1 and 0)`, which is `True or 0`, so `True`.

```python
print(4 + 6 / 2 * 3)
print(2 ** 2 ** 3)
print(-4 ** 2)
print(15 // 4 + 15 % 4)
print(not 0 or 1 and 0)
```

Output:

```text
13.0
256
-16
6
True
```

2. `a + b * c ** d - e / f` is `(a + (b * (c ** d))) - (e / f)`. `x or y and not z` is `x or (y and (not z))`.
3.

```python
base = 500
discount = 12
shipping = 40

discount_amount = base * discount / 100
price = base - discount_amount + shipping
print(price)
```

Output:

```text
480.0
```

4. Correct: `(a + b + c) / 3`. The mistake `a + b + c / 3` divides only `c`.

```python
a, b, c = 70, 80, 90
print((a + b + c) / 3)
print(a + b + c / 3)
```

Output:

```text
80.0
180.0
```

5. `1 + 1 << 2` is `(1 + 1) << 2 = 2 << 2 = 8`, because `+` binds more tightly than `<<`. The result is 8, not 6.

```python
print(1 + 1 << 2)
```

Output:

```text
8
```

6. `&` binds more tightly than `>` and `==`, so `df.age > 30 & df.city == "Pune"` is read as `df.age > (30 & df.city) == "Pune"`, which makes no sense for columns. Fix it with brackets: `(df.age > 30) & (df.city == "Pune")`. (The expression is shown as an idea; it is not run here because it needs the pandas library.)

---

## Chapter Summary and Key Takeaways

- `==` compares values; `is` compares identity (the same object, as shown by `id()`).
- Use `is None` / `is not None` for the missing-value check. Use `==` for everything else, because `is` on numbers and strings depends on CPython caching and is not reliable (Python 3.8+ warns about `is` with literals).
- `b = a` creates an alias of the same object; copies are equal but not identical.
- Precedence: brackets, `**`, unary signs, `* / // %`, `+ -`, shifts, `&`, `^`, `|`, comparisons, `not`, `and`, `or`, conditional expression, `lambda`.
- Operators at one level group left to right, except `**` (right to left); comparisons chain.
- `-2 ** 2` is `-4`; `2 ** 3 ** 2` is `512`; `not a == b` is `not (a == b)`; `+` binds tighter than `<<`.
- When in doubt, add brackets or split the expression into named steps.

Next: [Chapter 14 — Conditional Statements](14-conditional-statements.md) uses these operators to make programs choose between actions.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
