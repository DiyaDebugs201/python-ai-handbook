# Chapter 06 — Strings: Basics, Indexing, Concatenation and Repetition

> Part 2 — Data Types and Strings · Video: 1:12:28–1:33:40 · Previous: [05 Numeric Types and Booleans](05-numeric-types-and-booleans.md) · Next: [07 String Slicing](07-string-slicing.md)

**In this chapter:** how to write text in Python (single, double and triple quotes), escape sequences and raw strings, why strings are immutable, how to find the length of a string with `len()`, how to read one character by position using positive and negative indexes and what `IndexError` means, how to join strings with `+`, repeat them with `*`, and test for a piece of text with `in`.

**Before you start:** you should know that a value has a type and that `type()` reports it ([Data Types and Integers](05-numeric-types-and-booleans.md#data-types-and-integers)), that `print()` is a built-in function that shows values, and that a `TypeError` means an operation does not fit the types involved. Recap: `int` is a whole number and `bool` is `True` or `False` ([The Boolean Data Type](05-numeric-types-and-booleans.md#the-boolean-data-type)). Everything in this chapter was run with Python 3.13.16; string behavior shown here is the same in every current Python 3 release. Traceback file paths in this chapter are shortened to `example.py`. Terms are defined in [../docs/GLOSSARY.md](../docs/GLOSSARY.md).

---

## String Basics

**Timestamp:** [1:12:28](https://www.youtube.com/watch?v=J9BI0jGOds8&t=4348s)

**Learning objectives:**

- Create strings with single, double and triple quotes and choose the quote style that avoids unnecessary escaping.
- Use escape sequences (`\n`, `\t`, `\\`, `\'`, `\"`) and raw strings (`r"..."`).
- Explain that strings are immutable and show what happens when you try to change one in place.
- Use `len()` to count the characters in a string.

**1. Intuition**

A string is a piece of text: a name, a sentence, an email address, the contents of a file. In Python it is a sequence of characters, one after the other, like beads on a thread or the letters on a printed ticket. Python's name for the type is `str`.

**2. Why does it exist?**

Programs constantly handle text: reading user input, printing messages, storing names, building file paths, and, in AI work, preparing prompts and processing documents. Numbers cannot represent words, so every language needs a text type. Python has no separate "character" type. A single character is simply a string of length 1.

**3. Technical explanation**

- A `str` is an immutable sequence of Unicode characters. Unicode is the international standard that gives a number (a code point) to characters from nearly every writing system, so Python 3 strings can hold English, Hindi, Chinese, accented letters and symbols alike. Code points are explored in [Chapter 10](10-ord-chr-and-string-methods.md).
- A string literal (text written directly in the program) is enclosed in matching quotes: `'...'`, `"..."`, `'''...'''` or `"""..."""`. Single and double quotes mean exactly the same thing; they exist so that you can include one kind of quote inside the other without escaping.
- Triple-quoted strings can span several lines, and the line breaks become part of the string.
- An escape sequence starts with a backslash `\` and stands for a character that is hard to type. The most common ones: `\n` (new line), `\t` (tab), `\\` (one backslash), `\'` (single quote), `\"` (double quote), and `\u00e9` (the Unicode character with hexadecimal code 00e9, which is "é").
- A raw string has the prefix `r` before the opening quote, for example `r"C:\new\table"`. Backslashes are kept as ordinary characters instead of starting an escape. A raw string cannot end with an odd number of backslashes, because the last backslash would escape the closing quote.
- Immutable means that once a string object is created, its contents cannot be changed. Operations that seem to modify a string, such as `upper()`, actually build and return a new string. The original stays as it was.
- `len(s)` is a built-in function that returns the number of characters in `s`. For the empty string `""` it is `0`.

**4. Syntax**

```text
variable = 'text'
variable = "text"
variable = '''text over
several lines'''
variable = r"raw text with \backslashes"
len(variable)
```

This is a pattern, not runnable code. The opening and closing quote must be the same kind. The prefix `r` goes immediately before the opening quote.

**5. Example 1 — Basic**

```python
greeting = "Hello, World"
name = 'Diya'
print(greeting)
print(name, type(name))
print("It's a sunny day")
print('She said "hello"')
print("Tab:\tcolumn two")
print("First line\nSecond line")
print("""Triple quotes
keep the line break""")
print(len(greeting), len(""), len(" "))
```

Output:

```text
Hello, World
Diya <class 'str'>
It's a sunny day
She said "hello"
Tab:	column two
First line
Second line
Triple quotes
keep the line break
12 0 1
```

The two apostrophe/quote lines show why both quote styles exist: `"It's a sunny day"` uses double quotes so the apostrophe needs no escape, and `'She said "hello"'` does the reverse. `\t` prints a tab and `\n` starts a new line. `len("Hello, World")` counts every character including the comma and the space: 12. `len("")` is 0, but `len(" ")` is 1, because a single space is a character.

**6. Example 2 — Practical**

File paths on Windows contain backslashes, which collide with escape sequences. A raw string avoids the problem.

```python
normal = "C:\\new\\table"
raw = r"C:\new\table"
print(normal)
print(raw)
print(normal == raw)

broken = "C:\new\table"
print(broken)
print(len(broken), len(raw))

message = "She said \"Hi\" and left"
print(message)
print("Back-slash: \\")
print("caf\u00e9")
```

Output:

```text
C:\new\table
C:\new\table
True
C:
ew	able
10 12
She said "Hi" and left
Back-slash: \
café
```

Line by line: `normal` escapes every backslash by doubling it, so each `\\` is one backslash character. `raw` writes the backslashes directly and produces the same string, so the comparison prints `True`. `broken` is a mistake: Python reads `\n` as a new line and `\t` as a tab, so the printed text is split and has fewer characters (12 against 12 for `raw`... see the output for the exact counts). `message` shows escaping a double quote inside a double-quoted string. The last line shows a Unicode escape producing the letter "é".

**7. Example 3 — Edge case or common mistake**

Immutability: you can read a character, but you cannot assign to a position.

```python
word = "Python"
word[0] = "J"
```

Traceback (last lines):

```text
Traceback (most recent call last):
  File "example.py", line 2, in <module>
    word[0] = "J"
    ~~~~^^^
TypeError: 'str' object does not support item assignment
```

The error says exactly what happened: a `str` object does not support item assignment. To get a changed string, build a new one and, if you want, give it the same name:

```python
word = "Python"
new_word = "J" + word[1:]
print(new_word)
print(word)

shout = word.upper()
print(shout)
print(word)

word = "Jython"
print(word)
```

Output:

```text
Jython
Python
PYTHON
Python
Jython
```

`word[1:]` is a slice meaning "everything from position 1 onward" ([Chapter 07](07-string-slicing.md)). `"J" + ...` creates a new string. The original `"Python"` was never modified; `upper()` also returns a new string. The last assignment `word = "Jython"` does not change the old string either: it makes the name `word` refer to a different string object. A name can be re-pointed; the string it used to refer to cannot be edited.

Two more errors you will see with quotes. This is not valid Python; it shows the error for a string that is never closed:

```text
print("Hello)
SyntaxError: unterminated string literal (detected at line 1)
```

And a raw string that ends with a single backslash is also not valid Python; it shows the error:

```text
path = r"C:\temp\"
SyntaxError: unterminated string literal (detected at line 1); perhaps you escaped the end quote?
```

The first has no closing quote. In the second, the final backslash escapes the closing quote even inside a raw string. Fix it by removing the trailing backslash or by concatenating: `r"C:\temp" + "\\"`.

**8. Common mistakes**

- Forgetting the closing quote, or using different opening and closing quotes (`"text'`).
- Including the same quote type inside a string without escaping it or switching quote style.
- Using single backslashes in Windows paths in a normal string (`"C:\new"`), which silently becomes a new line. Use a raw string, double the backslashes, or use forward slashes.
- Trying to change a character with `s[i] = ...`. Strings are immutable; build a new string.
- Expecting a string method such as `s.upper()` to change `s`. It returns a new string, so assign the result: `s = s.upper()`.
- Treating `len(" ")` as zero. Spaces and newlines count as characters.

**9. Real-world and AI applications**

- Every prompt sent to a language model is a string. Multi-line prompts are normally written with triple quotes.
- Reading text files, scraping web pages, cleaning datasets and building messages all depend on string handling.
- Raw strings are the standard way to write regular expressions (patterns for matching text) and Windows file paths.
- A model never sees a Python string as characters: text is first split into tokens ([Chapter 32](32-context-engineering-and-tokens.md)), so `len(text)` (characters) and the token count are different numbers.
- Immutability is one reason Python strings can be safely shared and used as dictionary keys ([Chapter 23](23-dictionaries.md)).

**10. Practice**

1. Create the string `It's 5 o'clock` using double quotes, then again using single quotes with escapes. Print both.
2. Print the text `Name<TAB>Age` on one line and `Asha<TAB>20` on the next, using `\t` and `\n` in a single `print()` call.
3. Create a three-line poem with a triple-quoted string and print it. Then print `len()` of it and explain why the number is larger than the number of visible letters.
4. Write a raw string for the path `D:\data\new_files\notes.txt` and print it. Then write the same path as a normal string with doubled backslashes and test that the two are equal.
5. Run `word = "cat"` followed by `word[0] = "b"`. Read the error, then produce `"bat"` without using assignment to an index.
6. Predict `len("a\nb")`, `len(r"a\nb")` and `len("""""")`... (hint for the last one: it is an empty triple-quoted string; check that you can write it).

**11. Interview questions**

- *Are strings mutable in Python?* No. They are immutable; operations that seem to change a string return a new one.
- *What is the difference between single and double quotes in Python?* None in meaning. Choose the one that avoids escaping quotes inside the text.
- *What is a raw string and when would you use one?* A string with an `r` prefix in which backslashes are literal characters. It is used for Windows paths and regular expressions.
- *Does Python have a character type?* No. A character is a string of length 1.
- *What does this do: `s = "abc"; s[0] = "x"`?* Raises `TypeError: 'str' object does not support item assignment`.

**12. Quick revision**

- `str` is an immutable sequence of Unicode characters; quotes `'` and `"` are equivalent, triple quotes allow several lines.
- Escapes: `\n`, `\t`, `\\`, `\'`, `\"`, `\uXXXX`. Prefix `r` makes backslashes literal.
- To change a string, build a new one; assigning to `s[i]` raises `TypeError`.
- `len()` counts characters including spaces and newlines.

---

## String Indexing

**Timestamp:** [1:19:04](https://www.youtube.com/watch?v=J9BI0jGOds8&t=4744s)

**Learning objectives:**

- Read a single character from a string with `s[i]`, starting from index 0.
- Compute the last valid index as `len(s) - 1`.
- Recognize and explain `IndexError: string index out of range` and the `TypeError` for non-integer indexes.

**1. Intuition**

Imagine a row of numbered lockers in a school corridor where the first locker is number 0, not 1. Each locker holds one character. To fetch a character you say which locker number you want. That number is the index (plural: indexes or indices).

**2. Why does it exist?**

Often you need one particular character: the first letter of a name, the last digit of a number, the character at a known position in a code. Indexing gives direct access to any position without looping through the whole string.

**3. Technical explanation**

- Indexing is zero-based: the first character is at index `0`, the second at `1`, and so on. For a string of length `n`, the valid non-negative indexes run from `0` to `n - 1`.
- The expression `s[i]` is evaluated with square brackets. It returns a new string of length 1 containing the character at that position. Because Python has no character type, the result is still a `str`.
- Python checks the index at run time. An integer outside the valid range raises `IndexError`. An index that is not an integer (such as a float) raises `TypeError`. A `bool` is accepted because it is an integer subclass, but this is poor style.
- The empty string has no valid index at all, so `""[0]` is an `IndexError`.
- Reading by index does not change the string.

Layout for `"Python"` (length 6):

| Character | P | y | t | h | o | n |
|-----------|---|---|---|---|---|---|
| Index | 0 | 1 | 2 | 3 | 4 | 5 |

**4. Syntax**

```text
string_value[index]
```

This is a pattern, not runnable code. `string_value` is a string or a variable holding one. `index` is an integer expression. The brackets directly follow the value with no space needed.

**5. Example 1 — Basic**

```python
word = "Python"
print(word[0])
print(word[1])
print(word[5])
print(type(word[0]))
print(len(word))
print(word[len(word) - 1])
```

Output:

```text
P
y
n
<class 'str'>
6
n
```

`word[0]` is the first character and `word[5]` the last, because the length is 6. The result type is `str`, not a separate character type. `word[len(word) - 1]` always gives the last character, because the last valid index is the length minus one.

**6. Example 2 — Practical**

A common use is extracting fixed-position information, such as the initial of a name or the last digit of a number written as text.

```python
full_name = "Meera Nair"
first_initial = full_name[0]
last_initial = full_name[6]
print(first_initial + last_initial)

order_code = "AB-2047"
print(order_code[0], order_code[1], order_code[2], order_code[3])
print(order_code[-1])
print(int(order_code[3]) + int(order_code[4]))

text = "level"
print(text[0] == text[4], text[1] == text[3])
```

Output:

```text
MN
A B - 2
7
2
True True
```

Line by line: in `"Meera Nair"` the space is at index 5, so `N` is at index 6. Joining two one-character strings with `+` gives `"MN"`. For `"AB-2047"` the characters are `A`, `B`, `-`, `2`; individual digit characters can be converted with `int()` for arithmetic (`2 + 0 = 2`). The `order_code[-1]` line uses a negative index, covered in [Negative Indexing](#negative-indexing). The last lines compare characters at mirror positions, the idea behind palindrome checks.

**7. Example 3 — Edge case or common mistake**

The most common error is going one step past the end.

```python
word = "Python"
print(word[6])
```

Traceback (last lines):

```text
Traceback (most recent call last):
  File "example.py", line 2, in <module>
    print(word[6])
          ~~~~^^^
IndexError: string index out of range
```

`"Python"` has 6 characters, so the valid indexes are 0 to 5. Index 6 does not exist. The fix is to remember "length minus one", or to use a negative index for the last character. Other index errors:

```python
word = "Python"

try:
    print(word[1.0])
except TypeError as error:
    print("TypeError:", error)

try:
    print(""[0])
except IndexError as error:
    print("IndexError:", error)

index = 3
print(word[index], word[index + 1])
print(word[int("2")])
```

Output:

```text
TypeError: string indices must be integers, not 'float'
IndexError: string index out of range
h o
t
```

A float index fails even when its value looks whole (`1.0`), because indexes must be integers. Indexing the empty string always fails. Using a variable or an expression as the index is fine as long as it evaluates to an integer within range. Remember that `input()` returns text, so convert it with `int()` before using it as an index.

**8. Common mistakes**

- Counting from 1 instead of 0, so `s[1]` is expected to be the first character.
- Using `s[len(s)]` expecting the last character; it is out of range. Use `s[len(s) - 1]` or `s[-1]`.
- Indexing an empty string without checking it first.
- Using a float index such as `s[n / 2]`; `/` returns a float. Use `s[n // 2]` for the middle index.
- Trying to assign to an index (`s[0] = "x"`); strings are immutable.

**9. Real-world and AI applications**

- Parsing fixed-format codes and IDs, checking the first character of a word (for example, whether a line starts with `#`), and reading individual digits.
- Character-level tasks in text processing: checking palindromes, counting letters, comparing the first and last characters.
- In AI and NLP, models work on tokens rather than raw characters, but character indexing is still used in preprocessing (for example, locating where an entity starts in a sentence). The same zero-based indexing applies to lists, tuples and arrays ([Chapter 18](18-lists-fundamentals.md)).

**10. Practice**

1. For `s = "Computer"`, print the first, third and last characters using non-negative indexes.
2. Given `s = "Hello, World"`, print the character at index `7` and explain which character is at index `5`.
3. Write code that prints the middle character of `"racecar"` using `len()` and `//`.
4. Predict the result of `"abc"[3]`, then run it and read the error. What is the largest valid index?
5. Given `digits = "90210"`, add the first and last digits as integers and print the sum.
6. Write a short piece of code that checks whether a 5-letter word is a palindrome by comparing characters at index 0 with 4 and 1 with 3.

**11. Interview questions**

- *What is the index of the first character of a string?* `0`.
- *What is the last valid index for a string of length `n`?* `n - 1`.
- *What type does `s[i]` return?* A `str` of length 1.
- *What exception is raised for `"abc"[5]`?* `IndexError: string index out of range`.
- *What exception for `"abc"[1.5]`?* `TypeError: string indices must be integers, not 'float'`.

**12. Quick revision**

- Zero-based: valid indexes are `0` to `len(s) - 1`.
- `s[i]` returns a one-character `str`; it does not modify `s`.
- Out-of-range integer: `IndexError`; non-integer index: `TypeError`.

---

## Negative Indexing

**Timestamp:** [1:23:35](https://www.youtube.com/watch?v=J9BI0jGOds8&t=5255s)

**Learning objectives:**

- Use negative indexes to count from the end of a string.
- Convert between a negative index and the equivalent non-negative index.
- State the valid range of negative indexes and what happens beyond it.

**1. Intuition**

Counting from the front uses 0, 1, 2 and so on. Sometimes you want "the last character" or "the second from last" without calculating the length. Negative indexes count backward from the end: `-1` is the last character, `-2` the one before it, and so on, like counting seats from the back of a train carriage.

**2. Why does it exist?**

Finding the last item with positive indexes needs `s[len(s) - 1]`, which is wordy and easy to get wrong. A negative index states the intent directly: `s[-1]`. This is useful for file extensions, last digits, trailing punctuation, and so on.

**3. Technical explanation**

- For a string of length `n`, a negative index `-k` refers to the same position as the non-negative index `n - k`. Python effectively adds `n` to a negative index before looking it up.
- Valid negative indexes run from `-1` (last character) to `-n` (first character). Anything below `-n` raises `IndexError`.
- Negative and non-negative indexes can be mixed freely; both point at the same characters.
- `-0` is just `0`, the first character, not the last.

Layout for `"Python"` (length 6):

| Character | P | y | t | h | o | n |
|-----------|---|---|---|---|---|---|
| Positive index | 0 | 1 | 2 | 3 | 4 | 5 |
| Negative index | -6 | -5 | -4 | -3 | -2 | -1 |

**4. Syntax**

```text
string_value[-k]        where 1 <= k <= len(string_value)
```

This is a pattern, not runnable code. `-1` is the last character and `-len(string_value)` is the first.

**5. Example 1 — Basic**

```python
word = "Python"
print(word[-1])
print(word[-2])
print(word[-6])
print(word[-1] == word[len(word) - 1])
print(word[-3] == word[3])
print(word[-0])
```

Output:

```text
n
o
P
True
True
P
```

`word[-1]` is `n`, the last character, and `word[-6]` is `P`, the first. The comparisons confirm that `-k` is the same as `len(word) - k`. `word[-0]` is `word[0]` because `-0` equals `0`, so it returns the first character, not the last.

**6. Example 2 — Practical**

```python
filename = "report_final.pdf"
print(filename[-1])
print(filename[-3] + filename[-2] + filename[-1])

sentence = "Is this working?"
print(sentence[-1] == "?")

number_text = "2024"
last_digit = int(number_text[-1])
print(last_digit % 2 == 0)

word = "Python"
print(word[0] + word[-1])
```

Output:

```text
f
pdf
True
True
Pn
```

Line by line: the last three characters of the file name spell the extension `pdf` (this only works for three-letter extensions; extensions of other lengths are better handled with slicing or `str.endswith()`, see [Chapter 07](07-string-slicing.md) and [Chapter 10](10-ord-chr-and-string-methods.md)). `sentence[-1] == "?"` tests whether the text ends with a question mark. The last digit of `"2024"` is converted to an integer, and `% 2 == 0` tests whether it is even (the `%` remainder operator is covered in [Chapter 11](11-arithmetic-operators.md)). The final line joins the first and last characters.

**7. Example 3 — Edge case or common mistake**

```python
word = "Python"

try:
    print(word[-7])
except IndexError as error:
    print("IndexError:", error)

try:
    print(word[6])
except IndexError as error:
    print("IndexError:", error)

print(word[-6], word[-len(word)])
print(word[-1], word[5])
print("" == "x"[:0])
```

Output:

```text
IndexError: string index out of range
IndexError: string index out of range
P P
n n
True
```

The valid negative range for a length-6 string is `-6` to `-1`. `-7` is out of range and raises `IndexError`, exactly like the positive index `6`. A frequent beginner error is assuming `-0` means the last character; it does not, the last character is `-1`. The final line, `"x"[:0]`, previews that a slice (unlike an index) returns an empty string instead of raising an error when it selects nothing ([Chapter 07](07-string-slicing.md)).

**8. Common mistakes**

- Using `s[-0]` for the last character (it is the first).
- Going past the start: `s[-len(s) - 1]` is out of range.
- Mixing up directions: `-1` is the last character and `-n` is the first.
- Using a negative index when the string might be empty: `""[-1]` is an `IndexError`.

**9. Real-world and AI applications**

- Checking the last character of a text (a closing punctuation mark, a trailing newline, a file extension).
- Taking the last element of any sequence such as a list of chat messages (`messages[-1]` is the most recent message) or a list of model outputs. The same rule works for lists and tuples.
- Negative positions appear in array libraries such as NumPy (for example, selecting the last feature column).

**10. Practice**

1. For `s = "Programming"` print the last character, the second-to-last character and the first character using only negative indexes.
2. Write the non-negative index equivalent of `s[-4]` for `s = "Programming"`, and confirm both give the same character.
3. Print whether the text `"hello.txt"` ends with the character `t` using a negative index.
4. Print the first and last characters of any non-empty string stored in a variable, without hard-coding the length.
5. Predict what `"abc"[-4]` does and what `"abc"[-3]` returns. Run both.
6. Write code that checks whether a 5-letter word is a palindrome using only negative indexes for the right-hand characters.

**11. Interview questions**

- *What does `s[-1]` return?* The last character of `s`.
- *How is `s[-k]` related to a non-negative index?* It equals `s[len(s) - k]`.
- *What is `s[-0]`?* The same as `s[0]`, the first character.
- *What happens with `"abc"[-4]`?* `IndexError: string index out of range`.
- *Do negative indexes work on lists?* Yes, with the same rules.

**12. Quick revision**

- `-1` is the last character and `-len(s)` is the first.
- `s[-k]` equals `s[len(s) - k]`; beyond `-len(s)` raises `IndexError`.
- `-0` is `0`.

---

## String Concatenation and Repetition

**Timestamp:** [1:27:35](https://www.youtube.com/watch?v=J9BI0jGOds8&t=5255s)

**Learning objectives:**

- Join strings with `+` and understand why both operands must be strings.
- Repeat a string with `*` and an integer.
- Test whether one string occurs inside another with `in` and `not in`.

**1. Intuition**

Concatenation (joining) is like gluing two strips of paper end to end. Repetition is like photocopying a strip several times and gluing the copies together. The `in` operator is like looking for a word inside a paragraph and answering yes or no.

**2. Why does it exist?**

Programs build text out of smaller parts: greeting plus name, line prefix plus message, a row of dashes for a divider. The operators `+` and `*` give a short, readable way to do this. The `in` operator answers "does this text contain that piece?" directly.

**3. Technical explanation**

- `a + b` with two strings returns a new string containing the characters of `a` followed by those of `b`. Neither `a` nor `b` changes (strings are immutable).
- `+` between a string and a non-string, such as an `int`, raises `TypeError`. Python does not convert automatically. Convert with `str()` first ([Chapter 08](08-type-conversion.md)), or use an f-string ([Chapter 09](09-string-formatting-and-f-strings.md)).
- `s * n` (or `n * s`) with an integer `n` returns `s` repeated `n` times. If `n` is `0` or negative, the result is the empty string. A float or string as the multiplier raises `TypeError`.
- Two string literals written side by side, such as `"ab" "cd"`, are joined by the parser into `"abcd"`. This applies only to literals, not to variables.
- `+=` on a string builds a new string and rebinds the name: `s += "x"` means `s = s + "x"`.
- The `*` operator has higher precedence than `+`, so `"a" + "b" * 3` is `"abbb"` ([Chapter 13](13-identity-operators-and-precedence.md)).
- `sub in s` returns `True` if `sub` occurs anywhere in `s` as a contiguous piece (a substring) and `False` otherwise. `sub not in s` is the opposite. The match is case-sensitive, and the empty string is considered to be in every string.
- `in` is an operator, not a function. For joining many strings from a list, the string method `str.join()` ([Chapter 10](10-ord-chr-and-string-methods.md)) is clearer and faster than many `+` operations.

**4. Syntax**

```text
string_a + string_b
string_a * integer
integer * string_a
substring in string_a
substring not in string_a
```

This is a pattern, not runnable code. Each line is an expression that produces a new `str` (for the first three) or a `bool` (for the last two).

**5. Example 1 — Basic**

```python
first = "Good"
second = "Morning"
print(first + second)
print(first + " " + second)
print("ab" * 3)
print(3 * "ab")
print("-" * 20)
print("ab" * 0 == "")
print("ab" "cd")
print("Python" in "I love Python")
print("python" in "I love Python")
print("Java" not in "I love Python")
```

Output:

```text
GoodMorning
Good Morning
ababab
ababab
--------------------
True
abcd
True
False
True
```

Joining `"Good"` and `"Morning"` gives `GoodMorning` with no space; add a `" "` string yourself. `"ab" * 3` repeats the text; the order of operands does not matter. A line of 20 dashes is a typical divider. Multiplying by `0` gives the empty string. Two adjacent literals are joined at compile time. `in` is case-sensitive: `"python"` is not found in `"I love Python"`.

**6. Example 2 — Practical**

```python
name = "Asha"
age = 21

greeting = "Hello, " + name + "!"
print(greeting)

print("Age: " + str(age))

title = "Report"
underline = "=" * len(title)
print(title)
print(underline)

line = "abc"
line += "def"
line += "!" * 2
print(line)

email = "asha@example.com"
if "@" in email and "." in email:
    print("Looks like an email address")
else:
    print("Not an email address")

print("a" + "b" * 3)
print(("a" + "b") * 3)
```

Output:

```text
Hello, Asha!
Age: 21
Report
======
abcdef!!
Looks like an email address
abbb
ababab
```

Line by line: `str(age)` converts the integer to text so `+` can join it. The `underline` is as long as the title because it repeats `"="` `len(title)` times. `line += "def"` creates a new string `"abcdef"` and points `line` at it; then `"!" * 2` is evaluated first and `"!!"` is appended. The email check uses `in` with the `and` operator ([Chapter 12](12-relational-logical-assignment-operators.md)); it is only a rough check, not real email validation. The last two lines show precedence: repetition happens before joining unless parentheses change the order.

**7. Example 3 — Edge case or common mistake**

```python
age = 25
print("Age: " + age)
```

Traceback (last lines):

```text
Traceback (most recent call last):
  File "example.py", line 2, in <module>
    print("Age: " + age)
                ~~~~^~~~~
TypeError: can only concatenate str (not "int") to str
```

Note that `print()` itself can accept several arguments of different types, separated by commas, so `print("Age:", age)` works and puts a space between them. Joining with `+` requires strings on both sides. More cases:

```python
age = 25
print("Age: " + str(age))
print("Age:", age)

try:
    print("ab" * 2.0)
except TypeError as error:
    print("TypeError:", error)

print("ab" * -1 == "")
print("a" + "b" == "ab")

original = "cat"
changed = original + "s"
print(original, changed)

print("" in "anything")
print("ab" in "xaby", "ba" in "ab")
```

Output:

```text
Age: 25
Age: 25
TypeError: can't multiply sequence by non-int of type 'float'
True
True
cat cats
True
True False
```

Convert the number with `str()` or pass it as a separate argument to `print()`. A float multiplier fails even when it looks like a whole number. A negative multiplier produces an empty string rather than an error. Concatenation never changes `original`; it returns a new string. The empty string is "in" every string. `in` looks for a contiguous piece in order: `"ab"` is in `"xaby"`, but `"ba"` is not in `"ab"`.

**8. Common mistakes**

- Writing `"Total: " + 5` (a `TypeError`). Use `str(5)`, an f-string, or separate `print()` arguments.
- Expecting a space to appear automatically between joined strings.
- Using a float or string as the repetition count; it must be an integer.
- Building a large string with `+` in a long loop. It works, but `str.join()` on a list is the standard efficient approach.
- Confusing `"5" + "5"` (`"55"`) with `5 + 5` (`10`), and `"5" * 3` (`"555"`) with `5 * 3` (`15`).
- Forgetting that `in` is case-sensitive and checks for a contiguous substring, not for individual characters in any order.
- Writing `"a" "b"` with a missing `+` between variables (`first second` is a `SyntaxError`); adjacent-literal joining works only with literals.

**9. Real-world and AI applications**

- Building prompts: instruction text plus the user's question plus context are joined into one prompt string. (Real code usually uses f-strings, covered in [Chapter 09](09-string-formatting-and-f-strings.md).)
- Formatting output with dividers such as `"-" * 40`.
- Checking whether a keyword occurs in text with `in` is the simplest form of text filtering (for example, flagging rows of a dataset that mention a certain word). Later chapters show more robust approaches.
- Repetition appears in padding and in building test data, such as `"word " * 1000` to create a long input for testing a text-processing function.

**10. Practice**

1. Join `"Python"`, a space and `"rocks"` and print the result.
2. Print a box top `+----------+` using `"+" + "-" * 10 + "+"`.
3. Given `name = "Ravi"` and `score = 88`, print `Ravi scored 88` using `+` and `str()`.
4. Predict what `"ab" * 3 + "c" * 2` prints, then run it.
5. Write code that prints `True` if the text `"error"` appears in the string `"File error: not found"` and also if the text `"Error"` does not appear in it. Explain why the second check is `True`.
6. Start with `s = ""` and use `+=` inside a `for` loop over `range(5)` to build `"01234"` (use `str(i)`). Then explain why `s` is a new string at each step.

**11. Interview questions**

- *What happens with `"abc" + 1`?* `TypeError: can only concatenate str (not "int") to str`.
- *What does `"ab" * 3` give? And `"ab" * 0`?* `"ababab"`, and `""`.
- *Does `+` change the original strings?* No. It returns a new string; strings are immutable.
- *What does the `in` operator check for strings?* Whether the left string occurs as a contiguous substring of the right string, case-sensitively.
- *Why is repeated `+=` on strings in a long loop not ideal?* Each step creates a new string; collecting parts in a list and calling `"".join(parts)` is the usual better approach.

**12. Quick revision**

- `+` joins two strings; both operands must be `str`. `*` repeats with an integer; `0` or negative gives `""`.
- `+=` rebinds the name to a new string.
- `in` / `not in` test for a case-sensitive substring; `"" in s` is always `True`.
- Convert numbers with `str()` before joining.

---

## Answers to Practice Exercises

### Answers: String Basics

ANSWERS_BASICS

### Answers: String Indexing

ANSWERS_INDEXING

### Answers: Negative Indexing

ANSWERS_NEG

### Answers: String Concatenation and Repetition

ANSWERS_CONCAT

---

## Chapter Summary and Key Takeaways

- A `str` is an immutable sequence of Unicode characters. Single and double quotes are equivalent; triple quotes span lines; escapes such as `\n`, `\t` and `\\` stand for special characters; a raw string `r"..."` keeps backslashes literally.
- Assigning to `s[i]` raises `TypeError`; build a new string instead. `len()` counts characters, including spaces.
- Indexing is zero-based: valid indexes are `0` to `len(s) - 1`. `s[i]` returns a one-character `str`. Out-of-range integer indexes raise `IndexError`; non-integer indexes raise `TypeError`.
- Negative indexes count from the end: `s[-k]` equals `s[len(s) - k]`; `-1` is the last character and `-0` is the first.
- `+` joins strings (both sides must be `str`), `*` repeats a string with an integer, and `in` tests for a case-sensitive substring.

Next: [Chapter 07 — String Slicing](07-string-slicing.md) shows how to take a whole range of characters at once with `[start:stop:step]`.
