# Chapter 09 — String Formatting and f-Strings

> Part 2 — Data Types and Strings · Video: 3:13:46–3:25:07 · Previous: [08 Type Conversion](08-type-conversion.md) · Next: [10 ord(), chr() and String Methods](10-ord-chr-and-string-methods.md)

**In this chapter:** how to build text that contains values. You will see the three formatting styles in Python (the old `%` operator, the `str.format()` method and f-strings), and the format specification mini-language that controls width, alignment, number of decimal places, thousands separators, percentages, and binary or hexadecimal output. The second half is about f-strings in detail: expressions inside braces, the `=` debugging form, nested replacement fields, quoting rules, and what changed in Python 3.12.

**Before you start:** you should know that a string (`str`) is text written in quotes (see [String Basics](06-strings-basics-indexing-concatenation.md#string-basics)), that `+` joins two strings and that a number must be turned into text first with `str()` (see [String Concatenation and Repetition](06-strings-basics-indexing-concatenation.md#string-concatenation-and-repetition) and [Explicit Type Casting](08-type-conversion.md#explicit-type-casting)). Quick recap: `print()` is a built-in function that shows values on the screen; a function call such as `round(3.14159, 2)` hands values in and gets a result back; a method is a function that belongs to an object and is called with a dot, such as `"abc".upper()`. A few examples use a list and a `for` loop before those topics are taught in full ([Chapter 17](17-for-loop-range-and-nested-loops.md#the-for-loop)); read `for row in rows:` as "repeat the indented lines once for each item". Everything here was run with Python 3.13.16. Where behavior differs by version, the text names the version, and the older-version claims were checked with Python 3.11.17 and 3.12 on the same machine.

---

## String Formatting

**Timestamp:** [3:13:46](https://www.youtube.com/watch?v=J9BI0jGOds8&t=11626s)

**Learning objectives:**

- Explain why formatting is better than joining strings with `+` and `str()`.
- Read and write the three styles: `%` formatting, `str.format()` and f-strings (the last is studied in the next topic).
- Use the format specification mini-language: fill, alignment, sign, width, thousands separator, precision and type codes (`d`, `f`, `e`, `g`, `%`, `b`, `o`, `x`, `s`).
- Recognise the common errors: wrong type code, too few arguments, mixing automatic and manual field numbers.

**1. Intuition**

A form letter has blanks: "Dear ____, your balance is ____." The letter stays the same; only the blanks are filled in for each person. String formatting is the same idea. You write the sentence once with placeholders, and Python fills the placeholders with values.

Placeholders can also say how to show each value: "right-aligned in a column 10 characters wide", "two decimal places", "with commas between thousands". That is the second half of formatting: not only inserting a value, but deciding its appearance.

**2. Why does it exist?**

Without formatting you build text by joining pieces:

```python
name = "Asha"
marks = 92.456
print("Name: " + name + ", marks: " + str(marks) + " out of " + str(100))
```

Output:

```text
Name: Asha, marks: 92.456 out of 100
```

This works, but it has problems: every number needs `str()`, spaces and punctuation are easy to forget, the sentence is hard to read in the code, and there is no control over decimal places or column width. Formatting solves all four by keeping the sentence whole and putting the values in marked places.

**3. Technical explanation**

Python has three formatting styles. All of them produce a new `str`; none of them modifies an existing string (strings are immutable).

1. `%` formatting (the oldest, borrowed from the C language's `printf`). The `%` operator takes a string on the left and a value or a tuple of values on the right: `"%s scored %d" % (name, score)`. Codes such as `%s` (text), `%d` (integer) and `%.2f` (float with 2 decimals) mark the places. It still works and you will meet it in older code and in the `logging` module's messages, but newer code prefers the other two.
2. `str.format()` (introduced in Python 2.6 and 3.0). The string holds replacement fields in braces `{}`; calling the method `.format(...)` on it supplies values: `"{} scored {}".format(name, score)`. The string is an ordinary value that you can store in a variable and fill in later, many times.
3. f-strings (formatted string literals, introduced in Python 3.6). The string starts with `f` and holds expressions in braces that are evaluated on the spot: `f"{name} scored {score}"`. They are the shortest and the most readable, and the usual choice today. They are the topic after this one.

`str.format()` and f-strings share the same specification language for describing how a value is shown, called the format specification mini-language. It is also available through the built-in function `format(value, spec)`. The distinction between the three tools:

| Tool | Kind | Example |
|------|------|---------|
| `%` | operator on a string | `"%.2f" % 3.14159` |
| `str.format()` | method of `str` | `"{:.2f}".format(3.14159)` |
| `format()` | built-in function | `format(3.14159, ".2f")` |

Each replacement field in `str.format()` has up to three parts: `{field_name!conversion:format_spec}`.

- `field_name` picks which value: empty (next value in order), a number (position), or a name (keyword argument). It may also reach inside a value: `{0.real}` (an attribute), `{p[0]}` (an index) or `{d[key]}` (a dictionary key).
- `!conversion` is optional: `!s` calls `str()`, `!r` calls `repr()`, `!a` calls `ascii()`.
- `:format_spec` is optional and controls appearance.

Literal braces are written doubled: `{{` gives `{` and `}}` gives `}`.

The format specification has this general form (every part optional):

```text
[[fill]align][sign][#][0][width][grouping][.precision][type]
```

This is not valid Python; it is the layout of the spec after the colon. The parts, in order:

| Part | Meaning | Example |
|------|---------|---------|
| `fill` | character used to pad (any single character; needs `align` after it) | `*` in `*^10` |
| `align` | `<` left, `>` right, `^` centre, `=` pad between sign and digits (numbers only) | `>` in `>8` |
| `sign` | `+` always show sign, `-` only for negatives (default), a space shows a space for positives | `+` in `+.1f` |
| `#` | alternate form: adds `0b`, `0o`, `0x` prefixes for integers | `#x` gives `0xff` |
| `0` | pad numbers with zeros after the sign (same as fill `0` with `=`) | `05` |
| `width` | minimum total width of the result | `8` |
| `grouping` | `,` or `_` as thousands separator (and `_` also groups binary, octal and hex digits in fours) | `,` in `,.2f` |
| `.precision` | for floats: digits after the decimal point (types `f`, `e`, `%`) or total significant digits (`g` and no type); for strings: maximum characters | `.2` |
| `type` | how to present the value | `f`, `d`, `s` ... |

The main type codes:

| Code | For | Meaning |
|------|-----|---------|
| `s` | strings | text (default for strings) |
| `d` | integers | decimal integer (default for integers) |
| `b`, `o` | integers | binary, octal |
| `x`, `X` | integers | hexadecimal in lower or upper case |
| `c` | integers | the character with that Unicode code point |
| `f` | floats | fixed point, default 6 decimals |
| `e` | floats | scientific notation |
| `g` | floats | general: fixed or scientific, whichever is shorter; drops trailing zeros |
| `%` | floats | multiply by 100, show with a percent sign |

Two facts to remember. First, default alignment depends on type: numbers align right and text aligns left, so `{:5}` of `42` gives `   42` while `{:5}` of `"42"` gives `42   `. Second, formatting rounds the displayed value only; the variable still holds the original number.

**4. Syntax**

```text
"%[flags][width][.precision]code" % value_or_tuple
"... {field_name!conversion:format_spec} ...".format(*positional, **keyword)
format(value, format_spec)
```

This is not valid Python as a whole; it shows the three forms. In the `%` form, `code` is a letter such as `s`, `d`, `f`; one value goes straight after `%`, several values must be in a tuple. In the `.format()` form, `positional` values fill fields by order or by number, and `keyword` values fill named fields. The `format()` form takes a single value and a spec string and returns the formatted text.

**5. Example 1 — Basic**

Runnable (standard library only). The same sentence in the three styles.

```python
name = "Asha"
marks = 92.456

print("Name: %s, marks: %.1f" % (name, marks))
print("Name: {}, marks: {:.1f}".format(name, marks))
print("Name: {n}, marks: {m:.1f}".format(n=name, m=marks))
print("Name: {0}, marks: {1:.1f}, again: {0}".format(name, marks))
print(f"Name: {name}, marks: {marks:.1f}")
```

Output:

```text
Name: Asha, marks: 92.5
Name: Asha, marks: 92.5
Name: Asha, marks: 92.5
Name: Asha, marks: 92.5, again: Asha
Name: Asha, marks: 92.5
```

All five lines give the same text except for the extra phrase in the fourth. `.1f` means "float with one digit after the decimal point", so `92.456` is shown as `92.5`. Empty braces take values in order; `{0}` and `{1}` take by position and may repeat a value (the fourth line uses `{0}` twice); `{n}` and `{m}` take by keyword.

**6. Example 2 — Practical**

Runnable (standard library only). A template string kept in a variable and reused for every row of a small receipt. This is where `str.format()` is still the better tool: the template is separate from the data.

```python
header = "{:<12}{:>5}{:>12}"
row = "{:<12}{:>5}{:>12,.2f}"

items = [
    ("Notebook", 3, 45.5),
    ("Pen", 12, 8.25),
    ("Backpack", 1, 1499.0),
]

print(header.format("Item", "Qty", "Price"))
print("-" * 29)
total = 0
for name, quantity, unit_price in items:
    line_total = quantity * unit_price
    total += line_total
    print(row.format(name, quantity, line_total))
print("-" * 29)
print("{:<17}{:>12,.2f}".format("Total", total))
```

Output:

```text
Item          Qty       Price
-----------------------------
Notebook        3      136.50
Pen            12       99.00
Backpack        1    1,499.00
-----------------------------
Total                1,734.50
```

Line by line:

- `{:<12}` means "left-align in a field 12 characters wide"; `{:>5}` right-aligns in 5; `{:>12,.2f}` right-aligns in 12, with a comma between thousands (`,`) and 2 decimal places (`.2f`).
- `header` and `row` are plain strings. They are not changed by `.format()`; each call returns a new string.
- `"-" * 29` repeats the dash 29 times (the widths add up: 12 + 5 + 12).
- `for name, quantity, unit_price in items:` takes each tuple apart; `total += line_total` adds to the running total.
- The last line reuses the same idea with widths 17 and 12 so that the total lines up with the last column.

**7. Example 3 — Edge case or common mistake**

Runnable (standard library only). The errors that formatting produces, and a classic `%` trap.

```python
def attempt(label, action):
    try:
        print(label, "->", action())
    except Exception as error:
        print(label, "->", type(error).__name__ + ":", error)

attempt("d with float", lambda: "{:d}".format(3.5))
attempt("d with str  ", lambda: "{:d}".format("7"))
attempt("s with int  ", lambda: "{:s}".format(42))
attempt("= on text   ", lambda: "{:=5}".format("ab"))
attempt("too few     ", lambda: "{} {}".format(1))
attempt("bad keyword ", lambda: "{name}".format(nme=1))
attempt("auto+manual ", lambda: "{} {0}".format(1))
attempt("% too few   ", lambda: "%s %s" % ("a",))
attempt("% extra     ", lambda: "%s" % (1, 2))
attempt("% one tuple ", lambda: "%s" % ((1, 2),))
attempt("braces      ", lambda: "{{}} {}".format(5))
```

Output:

```text
d with float -> ValueError: Unknown format code 'd' for object of type 'float'
d with str   -> ValueError: Unknown format code 'd' for object of type 'str'
s with int   -> ValueError: Unknown format code 's' for object of type 'int'
= on text    -> ValueError: '=' alignment not allowed in string format specifier
too few      -> IndexError: Replacement index 1 out of range for positional args tuple
bad keyword  -> KeyError: 'name'
auto+manual  -> ValueError: cannot switch from automatic field numbering to manual field specification
% too few    -> TypeError: not enough arguments for format string
% extra      -> TypeError: not all arguments converted during string formatting
% one tuple  -> (1, 2)
braces       -> {} 5
```

(`attempt` is a small helper function that runs an action and prints either its result or the error; `lambda` creates a tiny unnamed function. You do not need to study them now; they are covered in [Chapter 28](28-first-class-functions-and-lambda.md#lambda-functions).)

Reading the results:

- Type code `d` only accepts integers. A `float` (`3.5`) or a `str` (`"7"`) raises `ValueError`. Convert first (`int(...)`), or use `f` for floats. Likewise `s` does not accept an `int` in the format spec; leave the type off or convert with `str()`.
- The `=` alignment is for numbers only.
- Fewer arguments than fields gives `IndexError` (positional) or `KeyError` (named). Mixing `{}` and `{0}` in one string raises `ValueError`.
- With `%`, a tuple on the right is read as the list of values. To print a tuple itself you must wrap it in another tuple: `"%s" % ((1, 2),)`.
- Literal braces must be doubled in `.format()`; `{{}}` gives `{}`.

The next example shows a surprise that is about numbers and not about formatting itself:

```python
print(f"{2.675:.2f}", round(2.675, 2))
print(f"{2.5:.0f}", f"{3.5:.0f}", f"{0.125:.2f}")
print(f"{0.1 + 0.2:.20f}")
```

Output:

```text
2.67 2.67
2 4 0.12
0.30000000000000004441
```

`2.675` cannot be stored exactly in binary, so the stored value is slightly below `2.675` and rounds to `2.67`. Ties that can be stored exactly (such as `2.5` and `0.125`) round to the nearest even digit: `2.5` shows as `2`, `3.5` as `4`, and `0.125` as `0.12`. The last line asks for 20 digits and reveals the true stored value of `0.1 + 0.2`. This is why formatting is best used for display only: format when you print, and keep the full-precision value in your calculations.

Finally, the specification options on one value each:

```python
count = 1234567
price = 1234.5678
ratio = 0.4567
number = 255

print(f"[{'left':<10}] [{'right':>10}] [{'mid':^10}] [{'fill':*^10}] [{'cut':.2}]")
print(f"[{42:5}] [{'42':5}] [{42:<5}] [{42:05}] [{-42:05}] [{42:+}] [{42: }]")
print(f"[{count:,}] [{count:_}] [{price:,.2f}] [{price:>12,.1f}] [{price:e}] [{price:g}]")
print(f"[{ratio:.1%}] [{ratio:.0%}] [{ratio:10.2%}]")
print(f"[{number:b}] [{number:o}] [{number:x}] [{number:X}] [{number:#x}] [{number:08b}] [{number:_b}] [{65:c}]")
```

Output:

```text
[left      ] [     right] [   mid    ] [***fill***] [cu]
[   42] [42   ] [42   ] [00042] [-0042] [+42] [ 42]
[1,234,567] [1_234_567] [1,234.57] [     1,234.6] [1.234568e+03] [1234.57]
[45.7%] [46%] [    45.67%]
[11111111] [377] [ff] [FF] [0xff] [11111111] [1111_1111] [A]
```

Notes: `{42:5}` right-aligns a number but `{'42':5}` left-aligns a string. `05` pads with zeros after the sign (`-0042`). `+` forces a sign on positive numbers, and a space leaves room for a sign. `.2` on a string cuts it to two characters. `%` multiplies by 100 and adds the percent sign. `#x` adds the `0x` prefix, `08b` gives 8 binary digits padded with zeros, and `_b` groups binary digits in fours with underscores. `{65:c}` shows the character with code point 65, which is `A` (see [Chapter 10](10-ord-chr-and-string-methods.md#strings-revisited-ord-and-chr)).

**8. Common mistakes**

- Using `%d` or `{:d}` with a float. Use `f`, or convert with `int()` knowing that it truncates (see [Explicit Type Casting](08-type-conversion.md#explicit-type-casting)).
- Forgetting the tuple in `%` formatting when there is more than one value: `"%s %s" % a, b` is wrong; write `"%s %s" % (a, b)`.
- Passing `%` a tuple as a single value (it is unpacked); wrap it in a one-item tuple.
- Mixing `{}` and `{0}` in one string.
- Writing `{:5.2}` for floats and expecting 2 decimals. Without `f`, the precision means significant digits: `format(3.14159, ".3")` gives `3.14`, and `format(1234.5, ".3")` gives `1.23e+03`. Add `f` for fixed decimals.
- Forgetting to double braces for literal braces in `.format()`.
- Rounding with format and then calculating with the rounded text. Keep numbers as numbers; format only for output.
- Assuming a width is a maximum. A value wider than `width` is never cut (strings are cut only by `.precision`).

**9. Real-world and AI applications**

- Reports and logs: aligned columns for tables, `:.2f` for money, `:,` for large counts, `:.1%` for rates.
- Training logs for machine learning typically print values such as epoch number, loss and accuracy in a fixed layout, for example `epoch 03  loss 0.4821  acc 87.5%`. The format spec keeps the columns aligned so trends are easy to read.
- Prompt templates for language models are often strings with named fields (`"Summarize this text: {text}"`) that are filled per request with `.format(text=...)`. The template lives in one place and the data in another, which is the strength of `str.format()` over f-strings.
- The `logging` module still accepts `%`-style messages (`logger.info("loaded %d rows", n)`) and only builds the final text when the message is actually emitted. That is one reason you will still see `%` codes in current code.
- Hex and binary output (`:x`, `:08b`) appear when working with colors, bit flags, hashes and byte data.
- A safety note: never use `.format()` on a template that comes from an untrusted user, because field names such as `{0.__class__}` can reach attributes of the values you pass in.

**10. Practice**

1. Write one line that prints `Total: 1,234,567.50` from `amount = 1234567.5`, using any style.
2. Given `name = "Ravi"` and `age = 21`, print `Ravi is 21 years old.` using (a) `%`, (b) `.format()` with positional fields, (c) `.format()` with named fields.
3. Print the number `0.8765` as a percentage with one decimal place (`87.7%`), and the number `47` in binary with at least 8 digits (`00101111`).
4. Build a three-row table using one template string: names left-aligned in 10 characters, scores right-aligned in 6 characters with one decimal place. Use the data `("Asha", 91.5), ("Ben", 78.25), ("Chandra", 100.0)`.
5. Explain why `"{:d}".format(2.0)` raises an error and show two ways to fix it.
6. Predict the output of `print("%s and %s" % ("tea",))` and explain how to correct it. Then explain the difference between `"%s" % (1, 2)` and `"%s" % ((1, 2),)`.
7. Center the word `Python` in a line of 20 characters padded with `=` on both sides, using the format spec only.

**11. Interview questions**

1. Name the three ways to format strings in Python and when you would use each.
   Short answer: `%` formatting (legacy, still seen in older code and `logging`), `str.format()` (reusable templates stored separately from data), f-strings (default choice for readable inline formatting).
2. What does `"{:>10.2f}".format(3.14159)` return?
   Short answer: `'      3.14'`: right-aligned in a field of width 10 with two decimals (6 spaces then `3.14`).
3. How do you print a literal `{` with `str.format()`?
   Short answer: double it: `"{{".format()` gives `"{"`.
4. Why does `"{:d}".format(3.5)` fail?
   Short answer: `d` requires an integer; the float raises `ValueError`.
5. Code question: what does this print?

```python
print("{1}-{0}-{1}".format("a", "b"), "{:^7}|".format("mid"))
```

Short answer: `b-a-b   mid  |`. Positional numbers select the arguments; `^7` centres `mid` in 7 characters, with extra space put on the right when the padding is uneven.
6. Does formatting change the original number?
   Short answer: no. It returns a new string; the number is unchanged.
7. What is the difference between `str.format()` and the built-in `format()`?
   Short answer: `str.format()` is a string method that fills a whole template with several values; `format(value, spec)` formats one value using only a specification.

**12. Quick revision**

- Formatting puts values into a sentence with placeholders and controls how each value appears.
- Styles: `%` (old), `str.format()` (templates), f-strings (inline, next topic). All return new strings.
- Spec: `[[fill]align][sign][#][0][width][grouping][.precision][type]`.
- Alignment: `<` left, `>` right, `^` centre; numbers default right, text default left.
- `,` and `_` group digits; `.2f` fixed decimals; `%` percent; `b o x X` for other bases; `e` and `g` for scientific and general.
- Wrong type code gives `ValueError`; too few values gives `IndexError` or `KeyError` (and `TypeError` with `%`).
- Format for display only; keep full-precision numbers for calculation.

---

## Python f-Strings

**Timestamp:** [3:25:07](https://www.youtube.com/watch?v=J9BI0jGOds8&t=12307s)

**Learning objectives:**

- Write f-strings with expressions, conversions and format specifications.
- Use the `=` specifier (Python 3.8 and later) to print an expression together with its value.
- Use nested replacement fields to make width and precision variable.
- Follow the quoting rules and know exactly what changed in Python 3.12.
- Choose between an f-string and `str.format()`.

**1. Intuition**

An f-string is a string with windows cut into it. Anything inside curly braces is not text; it is a small piece of Python code whose result is put into the window. The `f` before the opening quote tells Python to look for those windows.

**2. Why does it exist?**

`str.format()` still separates the template from the values, so you read `"{} scored {}"` and then must look at the end of the line to learn which value goes where. An f-string removes that jump: `f"{name} scored {score}"` shows the names where the values appear. It is also shorter and, in practice, faster than the older styles, because Python compiles the pieces directly instead of calling a method. Python 3.6 introduced them (PEP 498).

**3. Technical explanation**

An f-string is not a special type. It is a normal string literal with an `f` (or `F`) prefix, and at runtime Python evaluates it and produces an ordinary `str`. For each `{...}` Python:

1. evaluates the expression inside the braces, using the variables available at that point;
2. optionally applies a conversion (`!s`, `!r` or `!a`);
3. formats the result with the format specification after the `:` (the same mini-language as in the previous topic);
4. inserts the resulting text.

Two consequences follow. First, an f-string is evaluated immediately, where it is written, so it cannot be used as a stored template to fill in later; for that, use `str.format()`. Second, any expression is allowed inside the braces: arithmetic, function calls, method calls, indexing, comparisons, conditional expressions, even comprehensions. Keep expressions short so that the string stays readable.

The `=` specifier, added in Python 3.8 (as documented in the language reference; the sandbox used for these notes has 3.11 and later, so the 3.8 introduction date itself is taken from the documentation), writes the expression text, an equals sign, and the value: `f"{x=}"` gives `x=10`. By default it uses `repr()` for the value; `f"{x=:>6}"` applies a format spec after it, and spaces around the `=` are kept (`f"{x = }"` gives `x = 10`). It exists to make quick debugging prints shorter.

Nested replacement fields: inside the format spec you can use more braces to supply the width or precision from variables: `f"{value:{width}.{precision}f}"`.

Braces: to show literal braces, double them: `{{` and `}}`.

The quoting rules changed in Python 3.12 (PEP 701), and this is where version matters:

| Rule | Python 3.11 and earlier | Python 3.12 and later |
|------|------------------------|-----------------------|
| Reuse the same quote type inside the braces (`f"{d["k"]}"`) | `SyntaxError` | allowed |
| Backslash inside the braces (`f"{'\n'.join(words)}"`) | `SyntaxError` | allowed |
| Comment `#` inside the braces | not allowed | allowed |
| Expression spanning several lines inside a single-quoted f-string | not allowed | allowed |
| Nested f-strings using the same quote | not allowed | allowed |

These were checked by running the same code under Python 3.11.17, 3.12 and 3.13.16. Writing code that works on every version means using the portable style: pick a different quote type for the inside than for the outside (`f"{d['k']}"`), and compute anything with a backslash before the f-string.

Even in 3.12 and later, the text parts of an f-string (outside the braces) follow the usual string rules, so `\n` and `\t` work there. A raw f-string (`rf"..."` or `fr"..."`) keeps backslashes literally.

**4. Syntax**

```text
f"text {expression!conversion:format_spec} more text"
f"{expression=}"
f"{expression=!r:format_spec}"
f"{value:{width}.{precision}f}"
f"{{ literal braces }}"
```

This is not valid Python as written; it lists the forms. `expression` is any Python expression; `!conversion` is optional and is `!s`, `!r` or `!a`; `format_spec` is the same mini-language as before; `=` after the expression turns on the debugging form. The prefix may be `f` or `F`; triple quotes (`f"""..."""`) make multi-line f-strings.

**5. Example 1 — Basic**

Runnable (standard library only). Values, expressions and calls inside f-strings.

```python
name = "Asha"
items = 3
price = 49.99
scores = [70, 85, 90]

print(f"Hello, {name}!")
print(f"{items} items cost {items * price:.2f}")
print(f"Name in capitals: {name.upper()}")
print(f"First score: {scores[0]}, best score: {max(scores)}, count: {len(scores)}")
print(f"Pass: {'yes' if max(scores) >= 40 else 'no'}")
print(f"Braces: {{literal}} and a value {items}")
```

Output:

```text
Hello, Asha!
3 items cost 149.97
Name in capitals: ASHA
First score: 70, best score: 90, count: 3
Pass: yes
Braces: {literal} and a value 3
```

Each `{...}` is evaluated: `items * price` is `149.97` and `:.2f` formats it; `name.upper()` is a method call; `max()` and `len()` are built-in functions; `'yes' if ... else 'no'` is a conditional expression (an expression that picks one of two values; it is covered with `if` in [Chapter 14](14-conditional-statements.md#the-if-else-statement)). Note the single quotes around `'yes'` inside the double-quoted f-string; that is the portable style. `{{literal}}` shows literal braces.

**6. Example 2 — Practical**

Runnable (standard library only). A short training-log style report using conversions, widths, percentages, the `=` form, nested fields and a date.

```python
import datetime

model_name = "baseline"
rows = [
    (1, 0.9132, 0.612),
    (2, 0.5547, 0.748),
    (10, 0.0821, 0.9355),
]

print(f"Run: {model_name!r}")
for epoch, loss, accuracy in rows:
    print(f"epoch {epoch:02d}  loss {loss:.4f}  accuracy {accuracy:6.1%}")

width = 12
precision = 3
value = 3.14159265
print(f"[{value:{width}.{precision}f}]")
print(f"[{model_name:>{width}}]")

best = max(accuracy for _, _, accuracy in rows)
print(f"{best=}")
print(f"{best = :.1%}")

report_date = datetime.date(2026, 10, 19)
print(f"Report date: {report_date:%d %B %Y} ({report_date:%A})")
```

Output:

```text
Run: 'baseline'
epoch 01  loss 0.9132  accuracy  61.2%
epoch 02  loss 0.5547  accuracy  74.8%
epoch 10  loss 0.0821  accuracy  93.5%
[       3.142]
[    baseline]
best=0.9355
best = 93.5%
Report date: 19 October 2026 (Monday)
```

Line by line:

- `{model_name!r}` applies `repr()`, so the string appears with quotes (`'baseline'`), which makes whitespace or quote mistakes visible.
- `{epoch:02d}` is an integer padded with zeros to width 2; `{loss:.4f}` is 4 decimals; `{accuracy:6.1%}` is a percentage with 1 decimal in a field of 6 characters.
- `{value:{width}.{precision}f}` takes the width and precision from the variables `width` and `precision`; change the variables and the layout changes. The nested fields are replaced first and then the spec is applied.
- `{best=}` prints `best=0.9355`; it shows both the expression text and the value, which is why it is popular for quick debugging. `{best = :.1%}` keeps the spaces and applies a spec. The `max(... for ...)` is a generator expression, a compact loop; you do not need to master it yet.
- Dates and times have their own format codes after the colon (`%d`, `%B`, `%Y`, `%A`). These come from the object's own `__format__` method; the `datetime` module is imported with `import datetime` (see [Python Modules: math and import](03-builtin-functions-print-and-modules.md#python-modules-math-and-import)). Any class can define how it formats this way.

**7. Example 3 — Edge case or common mistake**

Runnable (standard library only, Python 3.12 or later). Quoting rules, and how the same code behaves on 3.11.

```python
prices = {"apple": 3, "pear": 5}
words = ["red", "green"]
x = 5

print(f"Price: {prices['apple']}")
print(f"Price: {prices["pear"]}")
print(f"{'\n'.join(words)}")
print(f"{x
    + 1}")
print(f"{f"{x:>4}"}")
```

Output:

```text
Price: 3
Price: 5
red
green
6
   5
```

The first print uses the portable style (single quotes inside double quotes). The remaining four lines only work in Python 3.12 and later: same-type quotes inside the braces, a backslash inside the braces, an expression broken over two lines, and an f-string nested in an f-string using the same quote. Python 3.11.17, running the second line, fails like this. This is output from the other interpreter (file path shortened):

```text
  File "example.py", line 2
    print(f"Price: {prices["apple"]}")
                            ^^^^^
SyntaxError: f-string: unmatched '['
```

and running `print(f"{'\n'.join(words)}")` on 3.11.17 fails with:

```text
SyntaxError: f-string expression part cannot include a backslash
```

Fixes that work on every version:

```python
words = ["red", "green"]
separator = "\n"
prices = {"apple": 3}

print(f"{separator.join(words)}")
print(f"{prices['apple']}")
print(f'{prices["apple"]}')
```

Output:

```text
red
green
3
3
```

Other mistakes that raise errors, shown here with a helper that compiles the text so that the error is displayed instead of stopping the program. (`eval` runs a piece of text as code; use it only for experiments like this one, never on text from users.)

```python
x = 5
snippets = [
    'f"{}"',
    'f"{x:.2f"',
    'f"}"',
    'f"{undefined_name}"',
    'f"{x:d}"',
    'f"{x:.2f}"',
    'f"{lambda y: y}"',
    'f"{(lambda y: y + 1)(x)}"',
]
for text in snippets:
    try:
        print(text.ljust(28), "->", eval(text))
    except Exception as error:
        print(text.ljust(28), "->", type(error).__name__ + ":", error)
```

Output:

```text
f"{}"                        -> SyntaxError: f-string: valid expression required before '}' (<string>, line 1)
f"{x:.2f"                    -> SyntaxError: f-string: expecting '}', or format specs (<string>, line 1)
f"}"                         -> SyntaxError: f-string: single '}' is not allowed (<string>, line 1)
f"{undefined_name}"          -> NameError: name 'undefined_name' is not defined
f"{x:d}"                     -> 5
f"{x:.2f}"                   -> 5.00
f"{lambda y: y}"             -> SyntaxError: f-string: lambda expressions are not allowed without parentheses (<string>, line 1)
f"{(lambda y: y + 1)(x)}"    -> 6
```

Reading the results: empty braces, a missing closing brace and a lone `}` are syntax errors. An unknown variable name is a `NameError`, raised when the f-string is evaluated, not when it is written. A `d` type code with an `int` works. A lambda must be wrapped in parentheses inside an f-string, because a bare colon would start the format spec. Notice that `x:.2f` works on an integer: `f` converts the integer to a float for display.

**8. Common mistakes**

- Forgetting the `f` prefix. `"{name}"` prints the braces and the word `name`. If you see braces in your output, check the prefix.
- Using the same quote inside as outside on Python 3.11 or earlier (works only on 3.12 and later).
- Putting a backslash inside the braces (also 3.12 and later only). Build the value first, then use it.
- Putting a colon-containing expression in braces without parentheses: lambdas, and dictionary or slice literals at the start. Wrap in `()` when in doubt.
- Writing very long expressions inside braces. Compute them on the line above and give the result a name.
- Storing an f-string in a variable and expecting it to "fill in later". It is evaluated once, when the line runs. Use `str.format()` for templates that you fill many times.
- Doubling a brace when it is not needed (or forgetting to double it when it is). `{{` shows one literal `{`.
- Using `=` and then being surprised by quotes: `f"{name=}"` shows `name='Asha'` because the default conversion is `repr()`. Use `f"{name=!s}"` for no quotes.
- Putting user-controlled text into an f-string that is later passed to `eval` or to a database query. Never build commands or queries this way; use parameters.

**9. Real-world and AI applications**

- Building prompts for language models from variables is a daily use: `prompt = f"Question: {question}\nContext: {context}"`. For a reusable template with many fillings, a `.format()` template string or a template library is neater.
- Log lines and progress messages in training loops: `print(f"step {step} loss={loss:.4f}")`. The `=` form is handy during debugging: `print(f"{learning_rate=}")`.
- Building file names and paths for experiments: `f"model_{run_id:03d}_epoch{epoch}.bin"`.
- Presenting metrics: `f"{accuracy:.1%}"`, `f"{n_tokens:,}"`.
- Building JSON-like text by hand is a common source of bugs (literal braces must be doubled). Use the `json` module to create JSON instead.
- API request text and error messages: `raise ValueError(f"Expected positive count, got {count!r}")` shows the bad value clearly.

**10. Practice**

1. Given `city = "Pune"` and `temperature = 28.456`, print `Pune: 28.5 degrees` using an f-string.
2. Print the expression and its value for `a = 7` and `b = 3` in the form `a * b = 21` using the `=` specifier. Then show the version with `!r` for a string variable.
3. Using nested fields, print the number `1234.5678` in a field of width 14 with 2 decimal places, right-aligned, with a comma as thousands separator, where the width and precision come from variables.
4. Print a three-row table of names and scores (`("Ana", 81.5)`, `("Bilal", 92.25)`, `("Chen", 77.0)`) with the names left-aligned in 8 characters and the scores right-aligned in 7 characters with 2 decimals.
5. Print `{count}` literally together with the value of `count = 3`, giving `{count} = 3`.
6. Write a portable f-string (valid on Python 3.11 and 3.12 alike) that prints the values of a dictionary entry whose key is `"total"`, and a second line that joins the list `["a", "b", "c"]` with newlines.
7. A variable `ratio = 0.07312`. Print it as a percentage with two decimals (`7.31%`) and, on another line, its default repr form using `=` (`ratio=0.07312`).

**11. Interview questions**

1. What is an f-string and from which Python version is it available?
   Short answer: a string literal prefixed with `f` whose braces hold expressions evaluated at runtime and inserted as text. Available since Python 3.6.
2. What does `f"{x=}"` do, and from which version?
   Short answer: it prints the expression text and its `repr()` value, for example `x=10`. Python 3.8 and later.
3. What changed about f-strings in Python 3.12?
   Short answer: PEP 701 let them reuse the same quote type inside the braces, allowed backslashes, comments and multi-line expressions inside the braces, and allowed nesting without quote tricks.
4. Why can an f-string not be used as a reusable template?
   Short answer: it is evaluated when the line runs and becomes a plain string at once; a template you fill in later should be a normal string used with `.format()` or `format_map()`.
5. Code question: what does this print?

```python
width = 6
n = 42
print(f"[{n:>{width}}] [{n:<{width}}] [{n=}]")
```

Short answer: `[    42] [42    ] [n=42]`.
6. How do you write a literal brace inside an f-string?
   Short answer: double it: `f"{{"` gives `{`.
7. Is an f-string faster than `%` or `.format()`?
   Short answer: in common benchmarks f-strings are usually the fastest, because they compile to direct string-building steps. The difference is rarely important; readability is the main reason to prefer them.

**12. Quick revision**

- `f"...{expression}..."`: expressions are evaluated at runtime and inserted; the result is a normal `str`.
- Format spec after `:`; conversions `!s`, `!r`, `!a` before it.
- `{x=}` prints `x=value` (3.8+); `{x = :spec}` keeps the spaces.
- Nested fields: `{value:{width}.{precision}f}`.
- Literal braces: `{{` and `}}`.
- Before 3.12: use different quote types inside and outside, and no backslashes or comments in braces. 3.12+ lifts these limits.
- For stored templates filled many times, use `str.format()`.

---

## Answers to Practice Exercises

### Answers: String Formatting

**Exercise 1.**

```python
amount = 1234567.5
print(f"Total: {amount:,.2f}")
print("Total: {:,.2f}".format(amount))
print("Total: %.2f" % amount)
```

Output:

```text
Total: 1,234,567.50
Total: 1,234,567.50
Total: 1234567.50
```

Explanation: `,` inserts thousands separators and `.2f` gives two decimals. The `%` style has no thousands separator, so the third line shows `1234567.50` without commas. That is one reason to prefer the newer styles.

**Exercise 2.**

```python
name = "Ravi"
age = 21
print("%s is %d years old." % (name, age))
print("{} is {} years old.".format(name, age))
print("{n} is {a} years old.".format(n=name, a=age))
```

Output:

```text
Ravi is 21 years old.
Ravi is 21 years old.
Ravi is 21 years old.
```

Explanation: `%` needs a tuple for several values; `.format()` fills empty braces in order, or named fields from keyword arguments.

**Exercise 3.**

```python
print(f"{0.8765:.1%}")
print(f"{47:08b}")
```

Output:

```text
87.6%
00101111
```

Explanation: `.1%` multiplies by 100, rounds to one decimal place and adds `%`. `08b` means zero-padded binary of width 8.

**Exercise 4.**

```python
template = "{:<10}{:>6.1f}"
rows = [("Asha", 91.5), ("Ben", 78.25), ("Chandra", 100.0)]
for name, score in rows:
    print(template.format(name, score))
```

Output:

```text
Asha        91.5
Ben         78.2
Chandra    100.0
```

Explanation: one template string is reused for every row. `78.25` shows as `78.2` because that value is an exact tie in binary and rounds to the even digit.

**Exercise 5.**

```python
try:
    print("{:d}".format(2.0))
except ValueError as error:
    print("ValueError:", error)

print("{:.0f}".format(2.0))
print("{:d}".format(int(2.0)))
```

Output:

```text
ValueError: Unknown format code 'd' for object of type 'float'
2
2
```

Explanation: `d` accepts integers only, even when the float has no fractional part. Fix by using `f` with `.0` precision, or convert to `int` first.

**Exercise 6.**

```python
try:
    print("%s and %s" % ("tea",))
except TypeError as error:
    print("TypeError:", error)

print("%s and %s" % ("tea", "toast"))
print("%s" % ((1, 2),))
try:
    print("%s" % (1, 2))
except TypeError as error:
    print("TypeError:", error)
```

Output:

```text
TypeError: not enough arguments for format string
tea and toast
(1, 2)
TypeError: not all arguments converted during string formatting
```

Explanation: two codes need two values. A tuple on the right of `%` is read as the list of values, so `(1, 2)` supplies two values to one code and fails; `((1, 2),)` is a tuple holding one item, the tuple `(1, 2)`.

**Exercise 7.**

```python
print(f"{'Python':=^20}")
```

Output:

```text
=======Python=======
```

Explanation: fill `=`, align `^` (centre), width `20`. The six letters leave 14 padding characters, 7 on each side.

### Answers: Python f-Strings

**Exercise 1.**

```python
city = "Pune"
temperature = 28.456
print(f"{city}: {temperature:.1f} degrees")
```

Output:

```text
Pune: 28.5 degrees
```

Explanation: `.1f` rounds to one decimal place for display.

**Exercise 2.**

```python
a = 7
b = 3
print(f"{a * b = }")
print(f"{a * b=}")
label = "tea"
print(f"{label=}")
print(f"{label=!s}")
```

Output:

```text
a * b = 21
a * b=21
label='tea'
label=tea
```

Explanation: the text before `=` is copied exactly, including any spaces, so `{a * b = }` gives `a * b = 21`. The default conversion for `=` is `repr()`, which puts quotes around strings; `!s` switches to `str()`.

**Exercise 3.**

```python
value = 1234.5678
width = 14
precision = 2
print(f"[{value:>{width},.{precision}f}]")
```

Output:

```text
[      1,234.57]
```

Explanation: the spec is `>` (right), then the width from a nested field, then `,` for thousands, then `.` plus the nested precision, then `f`. The order inside the spec matters: width, then grouping, then precision.

**Exercise 4.**

```python
rows = [("Ana", 81.5), ("Bilal", 92.25), ("Chen", 77.0)]
for name, score in rows:
    print(f"{name:<8}{score:>7.2f}")
```

Output:

```text
Ana       81.50
Bilal     92.25
Chen      77.00
```

Explanation: `<8` and `>7.2f` set the column widths; the dictionary-free layout keeps the numbers aligned on the decimal point because every score has two decimals.

**Exercise 5.**

```python
count = 3
print(f"{{count}} = {count}")
```

Output:

```text
{count} = 3
```

Explanation: `{{count}}` is literal text; `{count}` is the value.

**Exercise 6.**

```python
totals = {"total": 120}
words = ["a", "b", "c"]
newline = "\n"

print(f"Total: {totals['total']}")
print(f"{newline.join(words)}")
```

Output:

```text
Total: 120
a
b
c
```

Explanation: single quotes inside double quotes avoid the pre-3.12 quote restriction, and the backslash is kept outside the braces by storing the newline in a variable first. This code runs unchanged on Python 3.11 and on 3.12 and later.

**Exercise 7.**

```python
ratio = 0.07312
print(f"{ratio:.2%}")
print(f"{ratio=}")
```

Output:

```text
7.31%
ratio=0.07312
```

Explanation: `.2%` multiplies by 100 and shows two decimals. `{ratio=}` shows the repr of the original value, which is the full `0.07312`.

---

## Chapter Summary and Key Takeaways

- Formatting inserts values into a sentence and controls their appearance. Python has three styles: `%`, `str.format()` and f-strings.
- f-strings (3.6 and later) are the usual choice: `f"{name} scored {score:.1f}"`. Use `str.format()` for templates that are stored and filled later, and expect `%` in older code and in `logging`.
- The format spec `[[fill]align][sign][#][0][width][grouping][.precision][type]` is shared by f-strings, `str.format()` and the built-in `format()`.
- Numbers align right and strings align left by default. `,` and `_` group digits, `.2f` fixes decimals, `%` shows a percentage, `b o x X` show other bases.
- The `=` specifier (3.8 and later) prints `expression=value` for quick debugging.
- Nested fields `{value:{width}.{precision}f}` make layout variable; double braces show literal braces.
- Python 3.12 relaxed the quoting rules; for code that must run on 3.11 and earlier, use different quote types and keep backslashes out of the braces.
- Formatting changes only the displayed text, never the number. Format at output time and calculate with full precision.

Next: [Chapter 10 — ord(), chr() and String Methods](10-ord-chr-and-string-methods.md) looks at characters as numbers and at the methods you use to clean and search text.
