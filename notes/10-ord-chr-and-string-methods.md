# Chapter 10 — ord(), chr() and String Methods

> Part 2 — Data Types and Strings · Video: 8:19:30–8:41:36 · Previous: [09 String Formatting and f-Strings](09-string-formatting-and-f-strings.md) · Next: [11 Operators Overview and Arithmetic Operators](11-arithmetic-operators.md)

**In this chapter:** how characters are stored as numbers (code points), how to convert between a character and its number with `ord()` and `chr()`, why strings sort the way they do, and a full tour of the most useful string methods: changing case, trimming, splitting and joining, searching, replacing, testing the content of a string, and padding.

**Why this chapter comes here:** in the video these two topics appear after dictionaries. In this handbook they are moved up so that all string material sits together in Part 2 (see the reorganization log in [SYLLABUS_MAPPING.md](../SYLLABUS_MAPPING.md#2-reorganization-log)).

**Before you start:** you need string basics, indexing and slicing ([String Basics](06-strings-basics-indexing-concatenation.md#string-basics), [String Slicing](07-string-slicing.md#string-slicing)) and f-strings ([Python f-Strings](09-string-formatting-and-f-strings.md#python-f-strings)). Recap: a string is an immutable sequence of characters, which means that no operation can change it in place; every operation that seems to change a string returns a new one. A few examples use a `for` loop, which repeats a block of code for each item; it is explained fully in [The for Loop](17-for-loop-range-and-nested-loops.md#the-for-loop), and here it simply means "for each character". Examples were run with Python 3.13; version-specific methods are marked.

---

## Strings Revisited: ord() and chr()

**Timestamp:** [8:19:30](https://www.youtube.com/watch?v=J9BI0jGOds8&t=29970s)

**Learning objectives:**

- Explain that every character has a number called a code point, defined by Unicode.
- Convert between characters and code points with `ord()` and `chr()`.
- Explain why `"Z" < "a"` is true and how strings are compared and sorted.
- Distinguish a character (code point) from the bytes used to store it.

**1. Intuition**

Computers only store numbers. To store text, everyone agrees on a numbered list of characters: character number 65 is `A`, number 66 is `B`, and so on. It works like seat numbers in a theatre: the seat has a number, and a number tells you which seat. `ord()` asks "which number is this character?" and `chr()` asks "which character has this number?".

**2. Why does it exist?**

Programs need to compare letters, sort words, shift letters in a cipher, check whether a character is a digit, and move text between systems. All of this depends on a shared mapping from characters to numbers. Unicode is that shared mapping, and it covers the letters of almost all writing systems, as well as digits, symbols and emoji.

**3. Technical explanation**

Unicode assigns each character a *code point*, an integer usually written in hexadecimal with the prefix `U+`, for example `U+0041` for `A`. Python strings are sequences of Unicode code points.

- `ord(character)` takes a string of exactly one character and returns its code point as an integer.
- `chr(number)` takes an integer from `0` to `1114111` (`0x10FFFF`) and returns the one-character string for that code point.
- They are inverse functions: `chr(ord(c)) == c`.

Useful facts about the first 128 code points (the ASCII range): the digits `0` to `9` are 48 to 57, the capital letters `A` to `Z` are 65 to 90, and the small letters `a` to `z` are 97 to 122. Each small letter is exactly 32 above its capital.

*Comparing strings.* Python compares two strings character by character using code points. The first position where they differ decides the result. Because all capital letters (65 to 90) come before all small letters (97 to 122), `"Zebra" < "apple"` is `True`. Sorting words with plain `sorted()` therefore puts capitalised words first. To ignore case when sorting, use a key such as `str.lower` (keys are explained in [Lambda Functions](28-first-class-functions-and-lambda.md#lambda-functions)). This is code-point order, not the dictionary order of any particular language.

*Characters versus bytes.* A code point is an abstract number. To store text in a file or send it over a network, it is converted to bytes by an *encoding*, most commonly UTF-8. In UTF-8 a character uses between 1 and 4 bytes: plain English letters use 1, `é` uses 2, `€` uses 3 and most emoji use 4. `len(text)` counts characters (code points), and `len(text.encode("utf-8"))` counts bytes. Python 3 strings are Unicode by default; bytes are a separate type written `b"..."`.

**4. Syntax**

```text
ord(character)        # character -> integer code point
chr(integer)          # integer   -> one-character string
text.encode("utf-8")  # string    -> bytes
```

This is a pattern, not runnable code. `ord` requires a string of length exactly 1. `chr` requires an integer in `range(0x110000)`. Both are built-in functions (see [Built-in Functions and print()](03-builtin-functions-print-and-modules.md#built-in-functions-and-print)).

**5. Example 1 — Basic**

```python
print(ord("A"), ord("a"), ord("0"), ord(" "))
print(chr(72), chr(105), chr(33))
print(ord("€"), ord("é"), ord("😀"))
print(chr(8364), chr(0x1F600))
print(chr(ord("A") + 2))
print(ord("a") - ord("A"))
print(chr(ord("m") - 32))
```

Output:

```text
65 97 48 32
H i !
8364 233 128512
€ 😀
C
32
M
```

Line by line:

- The first line shows the codes of a capital, a small letter, a digit character and a space. Note that the character `"0"` has code 48; it is not the number 0.
- `chr(72)`, `chr(105)` and `chr(33)` spell `Hi!`.
- Non-English characters and emoji have bigger code points. They are still single characters of a Python string.
- `chr(8364)` is the euro sign; `chr(0x1F600)` uses a hexadecimal literal (`0x`) and gives an emoji. Whether the emoji shows correctly depends on your terminal's font.
- `chr(ord("A") + 2)` moves two letters along the alphabet: `C`.
- `ord("a") - ord("A")` is 32, so subtracting 32 turns a small letter into a capital, as `chr(ord("m") - 32)` shows.

**6. Example 2 — Practical**

A Caesar cipher shifts each letter by a fixed number of places. It is a classic exercise, and not secure for real secrets. The code below also checks characters with comparisons and uses the remainder operator `%`, which is covered in [Arithmetic Operators](11-arithmetic-operators.md#arithmetic-operators): `x % 26` gives the remainder after dividing by 26, so that the shift wraps from `Z` back to `A`.

```python
def caesar(text, shift):
    result = ""
    for character in text:
        if "A" <= character <= "Z":
            position = ord(character) - ord("A")
            result += chr((position + shift) % 26 + ord("A"))
        elif "a" <= character <= "z":
            position = ord(character) - ord("a")
            result += chr((position + shift) % 26 + ord("a"))
        else:
            result += character
    return result


secret = caesar("Hello, World!", 3)
print(secret)
print(caesar(secret, -3))
print(caesar("xyz", 3))
```

Output:

```text
Khoor, Zruog!
Hello, World!
abc
```

Line by line:

- The function walks through the text one character at a time.
- For a capital letter, `ord(character) - ord("A")` converts it to a position from 0 to 25. Adding the shift and taking `% 26` wraps around the alphabet. Adding `ord("A")` converts back to a code point, and `chr()` turns it into a letter.
- Small letters are handled the same way with `"a"`.
- Anything else (space, comma, digits) is copied unchanged.
- Shifting by `-3` undoes a shift of `3`, so the second line returns the original. `xyz` wraps to `abc`.

Another practical use: comparing and sorting.

```python
print("apple" < "banana")
print("Zebra" < "apple")
print("a" < "B")
words = ["banana", "apple", "Cherry", "Apple"]
print(sorted(words))
print(sorted(words, key=str.lower))
print(sorted(words, key=str.casefold))
```

Output:

```text
True
True
False
['Apple', 'Cherry', 'apple', 'banana']
['apple', 'Apple', 'banana', 'Cherry']
['apple', 'Apple', 'banana', 'Cherry']
```

`sorted(words)` puts the capitalised words `Apple` and `Cherry` first, because capitals have smaller code points than small letters. Sorting with `key=str.lower` compares the lowercase versions, so the result is in dictionary order. `Apple` and `apple` compare as equal, so they keep their original relative order (sorting is stable). `casefold` is a stronger version of `lower` meant for comparing text in many languages.

**7. Example 3 — Edge case or common mistake**

`ord` needs exactly one character, `chr` needs a valid code point, and characters are not the same as bytes:

```python
print(ord("ab"))
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 1, in <module>
    print(ord("ab"))
          ~~~^^^^^^
TypeError: ord() expected a character, but string of length 2 found
```

```python
print(chr(-1))
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 1, in <module>
    print(chr(-1))
          ~~~^^^^
ValueError: chr() arg not in range(0x110000)
```

```python
print(chr(1114112))
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 1, in <module>
    print(chr(1114112))
          ~~~^^^^^^^^^
ValueError: chr() arg not in range(0x110000)
```

```python
text = "café"
print(len(text))
print(len(text.encode("utf-8")))
print(text.encode("utf-8"))
print("é", len("é"), len("é"))
print("é" == "é")
```

Output:

```text
4
5
b'caf\xc3\xa9'
é 2 1
False
```

What happened:

- `ord("ab")` fails because the argument has two characters. Use `ord` on one character at a time (or loop over the string).
- `chr(-1)` and `chr(1114112)` are outside the range of Unicode code points.
- `"café"` has 4 characters but 5 bytes in UTF-8, because `é` takes two bytes (`\xc3\xa9`).
- The last two lines show a subtle point: `"é"` is a plain `e` followed by a combining accent (two code points), while `"é"` is one code point. They look the same on screen, but `len` differs and they are not equal. Text from different sources is sometimes normalised with the standard-library function `unicodedata.normalize` before comparing.

**8. Common mistakes**

- Thinking that `ord("5")` is 5. It is 53, the code of the character `"5"`. To get the number, use `int("5")`.
- Passing a longer string to `ord`.
- Assuming sorting is alphabetical for every language. It follows code points unless you provide a different key.
- Confusing characters with bytes, and assuming `len(text)` is the storage size.
- Forgetting that `chr` and `ord` change only characters; for numbers in text, convert with `int()` and `str()`.
- Using a Caesar cipher (or any simple shift) for real security. It is trivially breakable.

**9. Real-world and AI applications**

Code points and encodings are behind every "weird character" bug: text that looks like `cafÃ©` is UTF-8 bytes read with the wrong encoding. Data cleaning for AI often involves normalising Unicode, removing control characters and handling emoji. Tokenizers for language models work on bytes or characters before merging them into tokens, so text with accents, emoji or non-English scripts can use more tokens than plain English of the same visible length (see [Context Engineering, Tokens and Token Costs](32-context-engineering-and-tokens.md#tokens-and-token-costs)). Checksums, hashing and simple encodings also start from `ord` and bytes.

**10. Practice**

1. Print the code points of the characters in `"Py3!"`, and print the characters with codes 80, 121, 51 and 33.
2. Write `is_upper_letter(c)` that uses `ord` to return `True` only for `"A"` to `"Z"`.
3. Write `next_letter(c)` that returns the next letter of the alphabet and wraps `"z"` to `"a"`.
4. Predict whether `"Python" < "python"`, `"10" < "9"` and `"abc" < "abd"` are true, then check.
5. Explain why `len("naïve")` and `len("naïve".encode("utf-8"))` differ, and print both.

**11. Interview questions**

- *What is Unicode?* A standard that gives every character a unique number (code point); Python strings are sequences of Unicode code points.
- *What is the difference between Unicode and UTF-8?* Unicode defines the code points; UTF-8 is one way of encoding those code points as bytes.
- *Why is `"B" < "a"` true?* Strings compare by code point, and `B` (66) is less than `a` (97).
- *What do `ord` and `chr` do?* `ord` converts a one-character string into its code point; `chr` converts a code point into a character.

**12. Quick revision**

- `ord("A")` is 65; `chr(65)` is `"A"`; they are inverses.
- Digits 48 to 57, capitals 65 to 90, small letters 97 to 122.
- Strings compare and sort by code point; capitals come before small letters unless you use a key such as `str.lower`.
- `len(text)` counts characters; `len(text.encode("utf-8"))` counts bytes.
- `ord` needs exactly one character; `chr` needs 0 to 1114111.

---

## String Methods

**Timestamp:** [8:26:41](https://www.youtube.com/watch?v=J9BI0jGOds8&t=30401s)

**Learning objectives:**

- Explain that a method is a function that belongs to an object, and that string methods return new strings.
- Use the common methods for case, trimming, splitting and joining, searching, replacing, testing and padding.
- Predict what each method returns when it does not find what it is looking for.
- Choose between `find` and `index`, and between `split` and `partition`.

**1. Intuition**

A string method is a built-in tool that a string carries around with it, like a pocket knife. You write the string, a dot, then the tool: `"hello".upper()`. The tool does not change the string you hold, because strings never change; it hands you a new, modified copy.

**2. Why does it exist?**

Text is everywhere: names, addresses, file lines, web pages, prompts. Real text is messy (extra spaces, mixed capitals, separators), and the same small cleaning jobs come up again and again. The standard library provides over forty methods so that these jobs do not need to be rewritten.

**3. Technical explanation**

A method call has the form `object.method(arguments)`. Python looks up `method` in the type of the object (`str` here) and calls it with the object as the first argument automatically. All `str` methods leave the original unchanged and return a new value, which is a string, a number, a boolean, or a list, depending on the method. If you do not store or use the returned value, the work is lost.

The main groups (all are available in every current Python 3 unless noted):

| Job | Methods |
|-----|---------|
| Change case | `upper()`, `lower()`, `title()`, `capitalize()`, `swapcase()`, `casefold()` |
| Trim | `strip()`, `lstrip()`, `rstrip()` (with no argument, remove whitespace at the ends; with an argument, remove any of those characters) |
| Split and join | `split()`, `rsplit()`, `splitlines()`, `partition()`, `rpartition()`, `join()` |
| Search | `find()`, `rfind()`, `index()`, `rindex()`, `count()`, `startswith()`, `endswith()`, and the `in` operator |
| Replace | `replace(old, new, count)`, `removeprefix()` and `removesuffix()` (3.9+) |
| Test the content | `isdigit()`, `isdecimal()`, `isnumeric()`, `isalpha()`, `isalnum()`, `isspace()`, `isupper()`, `islower()`, `istitle()` |
| Pad and align | `center()`, `ljust()`, `rjust()`, `zfill()` |
| Encode | `encode()` |

*Return values when nothing is found.* `find()` returns `-1` when the text is not found, while `index()` raises `ValueError` instead. `replace()` returns the string unchanged if there is nothing to replace. `split()` always returns a list. `startswith()` and the `is...` methods return `True` or `False`.

*`split()` with and without an argument.* `text.split()` with no argument splits on any run of whitespace and ignores empty pieces at the ends. `text.split(",")` splits at every comma and keeps empty pieces. `join()` is the opposite: `separator.join(list_of_strings)` glues the items together, with the separator between them. It is called on the separator, not on the list.

*`strip` removes a set of characters, not a word.* `"xxhixx".strip("x")` removes `x` characters from both ends; `"abcba".strip("ab")` removes any `a` or `b` at the ends and gives `"c"`.

**4. Syntax**

```text
text.method()
text.method(argument)
text.method(argument1, argument2)
separator.join(iterable_of_strings)
```

This is a pattern, not runnable code. Methods can be chained from left to right: `text.strip().lower().split()` applies `strip`, then `lower` to its result, then `split` to that result.

**5. Example 1 — Basic**

```python
text = "  Hello, Python World!  "

print(text.upper())
print(text.lower())
print(text.strip())
print(text.strip().title())
print(text.strip().swapcase())
print("python is fun".capitalize())
print(text.strip().replace("Python", "Java"))
print(text.strip().split(", "))
print("-".join(["2025", "03", "14"]))
print(text)
```

Output:

```text
  HELLO, PYTHON WORLD!  
  hello, python world!  
Hello, Python World!
Hello, Python World!
hELLO, pYTHON wORLD!
Python is fun
Hello, Java World!
['Hello', 'Python World!']
2025-03-14
  Hello, Python World!  
```

Line by line:

- `upper()` and `lower()` change every letter. `title()` capitalises the first letter of each word. `capitalize()` capitalises only the first character of the string and lowercases the rest.
- `strip()` removes the spaces at the start and end (not in the middle).
- `replace("Python", "Java")` returns a copy with every match replaced.
- `split(", ")` cuts the text at each comma and space, and returns a list of two strings.
- `"-".join([...])` glues the items with a hyphen between them. The items must all be strings.
- The last line shows the original `text` is untouched, spaces included.

**6. Example 2 — Practical**

Cleaning and analysing real-looking text: normalising a typed name, reading a record, building a web-address-friendly slug, counting words and checking a file name.

```python
raw_name = "   dIYA   sharma  "
clean_name = " ".join(raw_name.split()).title()
print(repr(clean_name))

record = "Asha,27,Mysuru"
name, age, city = record.split(",")
print(name, int(age) + 1, city)

title = "  Python: A Beginner's Guide  "
slug = title.strip().lower().replace(":", "").replace("'", "").replace(" ", "-")
print(slug)

sentence = "the quick brown fox jumps over the lazy dog the end"
words = sentence.split()
print(len(words), sentence.count("the"), sentence.find("fox"), sentence.rfind("the"))

file_name = "photo_2025.JPG"
print(file_name.lower().endswith((".jpg", ".png")))
print(file_name.removesuffix(".JPG"))
print("report.pdf".startswith("rep"))
```

Output:

```text
'Diya Sharma'
Asha 28 Mysuru
python-a-beginners-guide
11 3 16 44
True
photo_2025
True
```

Line by line:

- `raw_name.split()` splits on any whitespace and drops the empty pieces, so the extra spaces vanish. `" ".join(...)` puts one space between the words, and `title()` fixes the capitals.
- `record.split(",")` returns a list of three strings, which are unpacked into three variables. The age is converted with `int()` before arithmetic.
- The slug is built by chaining methods: trim, lowercase, remove punctuation, and replace spaces with hyphens.
- `count("the")` counts non-overlapping matches, including the one inside `"the end"`. `find("fox")` gives the first position, and `rfind("the")` gives the position of the last match, searching from the right.
- `endswith` accepts a tuple of endings and returns `True` if any matches. `removesuffix` was added in Python 3.9; on older versions use slicing.

Testing the content of a string, and padding for aligned output:

```python
print("12345".isdigit(), "12a".isdigit(), "".isdigit())
print("hello".isalpha(), "hello world".isalpha(), "abc123".isalnum())
print("   ".isspace(), "HELLO".isupper(), "Hello".istitle())

print("7".zfill(3))
print("-7".zfill(4))
print("hi".center(10, "*"))
print("hi".ljust(6, ".") + "|")
print("hi".rjust(6, ".") + "|")
```

Output:

```text
True False False
True False True
True True True
007
-007
****hi****
hi....|
....hi|
```

`isdigit()` is `True` only if the string is non-empty and has digits only: no minus sign, no decimal point and no spaces, so `"-5".isdigit()` and `"3.5".isdigit()` are `False`. `zfill(width)` pads with zeros on the left and keeps a leading sign in front. `center`, `ljust` and `rjust` pad with spaces, or with the character you pass as the second argument. For complex tables, f-string alignment is usually easier (see [String Formatting](09-string-formatting-and-f-strings.md#string-formatting)).

Splitting in other ways:

```python
path = "folder/sub/file.txt"
print(path.split("/"))
print(path.rsplit("/", 1))
print(path.partition("/"))
print(path.rpartition("."))
print("line one\nline two\r\nline three".splitlines())
print("a,b,,c".split(","))
print("a  b   c".split())
print("a  b   c".split(" "))
```

Output:

```text
['folder', 'sub', 'file.txt']
['folder/sub', 'file.txt']
('folder', '/', 'sub/file.txt')
('folder/sub/file', '.', 'txt')
['line one', 'line two', 'line three']
['a', 'b', '', 'c']
['a', 'b', 'c']
['a', '', 'b', '', '', 'c']
```

`split(sep, maxsplit)` and `rsplit(sep, maxsplit)` limit the number of cuts; `rsplit("/", 1)` splits once from the right, which is how you separate a file from its folder. `partition(sep)` always returns exactly three items: the part before the first separator, the separator itself, and the part after it (and if the separator is missing, the whole string plus two empty strings). `splitlines()` understands different line endings. The last two lines show why `split()` without an argument is better for human text: `split(" ")` creates empty strings for repeated spaces.

**7. Example 3 — Edge case or common mistake**

Forgetting that the method returns a new string:

```python
name = "diya"
name.upper()
print(name)

name = name.upper()
print(name)
```

Output:

```text
diya
DIYA
```

The first call produced `"DIYA"` and threw it away. Assigning the result back to the name keeps it.

`find` versus `index`, and a missing text:

```python
text = "banana"

print(text.find("nan"))
print(text.find("xyz"))
print(text.index("nan"))
print(text.index("xyz"))
```

Output:

```text
2
-1
2
Traceback (most recent call last):
  File "example.py", line 6, in <module>
    print(text.index("xyz"))
          ~~~~~~~~~~^^^^^^^
ValueError: substring not found
```

The first three lines work and the last one raises `ValueError`; the program stops there. Use `find` if "not found" is an expected case and you will check for `-1`. Use `index` if "not found" is a bug that should stop the program. A common mistake is to test `if text.find("a"):`, because `find` returns `0` when the match is at the start, and `0` counts as false; write `if text.find("a") != -1:` or, better, `if "a" in text:`.

Three more surprises:

```python
print("they're here".title())
print("abcba".strip("ab"))
print("a-b-c".replace("-", "+", 1))
print(", ".join(["a", 1, "b"]))
```

Output:

```text
They'Re Here
c
a+b-c
Traceback (most recent call last):
  File "example.py", line 4, in <module>
    print(", ".join(["a", 1, "b"]))
          ~~~~~~~~~^^^^^^^^^^^^^^^
TypeError: sequence item 1: expected str instance, int found
```

Run line by line, the first three behave unexpectedly but without an error: `title()` capitalises the letter after the apostrophe (`They'Re`), `strip("ab")` removes any combination of `a` and `b` from both ends (so only `c` is left), and `replace` with a third argument limits the number of replacements. The fourth line fails because `join` needs every item to be a string; convert first with `str(item)`.

The first three results, shown separately so that you can see them:

```python
print("they're here".title())
print("abcba".strip("ab"))
print("a-b-c".replace("-", "+", 1))
```

Output:

```text
They'Re Here
c
a+b-c
```

**8. Common mistakes**

- Calling a method and not using the result (`text.strip()` on its own line does nothing useful).
- Using `strip("abc")` as if it removed the word `abc`; it removes any of those letters. To remove a known prefix or suffix, use `removeprefix` / `removesuffix` (3.9+).
- Testing `if text.find(x):` instead of `!= -1` or `x in text`.
- Calling `join` on the list: it is `separator.join(items)`, not `items.join(separator)`.
- Joining numbers without converting them to strings.
- Using `split(" ")` on text with several spaces, then getting empty strings.
- Using `isdigit()` to check for numbers: it rejects negative numbers and decimals, and it accepts some characters (such as superscript digits) that `int()` cannot convert. For safe conversion, use `try`/`except ValueError` around `int()` or `float()`.
- Using `title()` for names with apostrophes or hyphens; the standard-library function `string.capwords` handles the apostrophe case better, though no automatic rule suits every name.

**9. Real-world and AI applications**

Almost every data pipeline starts with string methods: trimming whitespace, lowercasing, splitting a log line or a CSV row, replacing separators, checking prefixes of file names or URLs. In AI work, text is cleaned before it is used: removing extra whitespace, normalising case when appropriate, splitting a document into lines or sentences, and joining pieces into a single prompt with `"\n".join(parts)` (see [Context Engineering, Tokens and Token Costs](32-context-engineering-and-tokens.md#context-engineering)). Checking that a model's reply `startswith` a required marker, or splitting its answer on a delimiter you asked for, are routine checks. Be careful with case: lowering text can destroy information that a model could use, so clean only as much as the task needs.

**10. Practice**

1. Given `"  Learning Python  "`, produce `"learning python"`, `"LEARNING PYTHON"` and `"Learning Python"` (without the surrounding spaces) using methods.
2. Given `"apple,banana,cherry"`, produce a list of fruits, then join them with `" | "`.
3. Write `count_vowels(text)` that counts vowels in a string, ignoring case. Test it on `"Programming Language"`.
4. Given `url = "https://example.com/page"`, check whether it starts with `https`, and extract the domain with `partition`/`split` and slicing.
5. Write `is_valid_pin(text)` that returns `True` only if the text is exactly four digits. Test `"1234"`, `"12a4"`, `"123"` and `"-123"`.
6. Predict `"a,b,,c".split(",")`, `"a b  c".split()` and `" x ".strip().isalpha()`, then check.

**11. Interview questions**

- *Are strings mutable? What does `"abc".upper()` do to `"abc"`?* No. It returns a new string `"ABC"`; the original is unchanged.
- *What is the difference between `find()` and `index()`?* When the text is missing, `find` returns `-1` and `index` raises `ValueError`.
- *What does `" ".join(["a", "b"])` do, and why is `join` a string method?* It joins the strings of the list with a space between them. It is a method of the separator because it works for any iterable of strings, not only lists.
- *What is the difference between `split()` and `split(" ")`?* With no argument, runs of whitespace are one separator and empty pieces are dropped; with `" "`, every single space is a separator, so repeated spaces make empty strings.
- *Does `strip("abc")` remove the text "abc"?* No, it removes any of the characters `a`, `b` and `c` from both ends.

**12. Quick revision**

- String methods return new values; assign them if you need them.
- Case: `upper`, `lower`, `title`, `capitalize`, `swapcase`, `casefold`. Trim: `strip`, `lstrip`, `rstrip`.
- Split and join: `split`, `rsplit`, `splitlines`, `partition`, `separator.join(items)`.
- Search: `find` (returns `-1`), `index` (raises `ValueError`), `count`, `startswith`, `endswith`, `in`.
- Replace: `replace(old, new, count)`; `removeprefix` / `removesuffix` need Python 3.9+.
- Tests: `isdigit`, `isalpha`, `isalnum`, `isspace`, `isupper`, `islower` (empty strings give `False`).
- Pad: `zfill`, `center`, `ljust`, `rjust`.

---

## Answers to Practice Exercises

### Answers: Strings Revisited: ord() and chr()

1.

```python
for character in "Py3!":
    print(character, ord(character))

print("".join(chr(code) for code in [80, 121, 51, 33]))
```

Output:

```text
P 80
y 121
3 51
! 33
Py3!
```

The last line uses a *generator expression* (a compact loop inside the call, explained in [List Comprehension](20-list-comprehension.md#list-comprehension)). The same result without it: `chr(80) + chr(121) + chr(51) + chr(33)`.

2.

```python
def is_upper_letter(character):
    return ord("A") <= ord(character) <= ord("Z")


print(is_upper_letter("Q"), is_upper_letter("q"), is_upper_letter("5"))
```

Output:

```text
True False False
```

3.

```python
def next_letter(character):
    if character == "z":
        return "a"
    if character == "Z":
        return "A"
    return chr(ord(character) + 1)


print(next_letter("a"), next_letter("y"), next_letter("z"), next_letter("Z"))
```

Output:

```text
b z a A
```

4. `"Python" < "python"` is `True` (`P` is 80 and `p` is 112). `"10" < "9"` is `True`, because strings compare character by character and `"1"` (49) is less than `"9"` (57); this is why numbers stored as text sort wrongly. `"abc" < "abd"` is `True`.

```python
print("Python" < "python", "10" < "9", "abc" < "abd")
```

Output:

```text
True True True
```

5. `"ï"` is one character but takes two bytes in UTF-8.

```python
word = "naïve"
print(len(word))
print(len(word.encode("utf-8")))
```

Output:

```text
5
6
```

### Answers: String Methods

1.

```python
text = "  Learning Python  "

print(text.strip().lower())
print(text.strip().upper())
print(text.strip())
```

Output:

```text
learning python
LEARNING PYTHON
Learning Python
```

2.

```python
fruits = "apple,banana,cherry".split(",")
print(fruits)
print(" | ".join(fruits))
```

Output:

```text
['apple', 'banana', 'cherry']
apple | banana | cherry
```

3.

```python
def count_vowels(text):
    count = 0
    for character in text.lower():
        if character in "aeiou":
            count += 1
    return count


print(count_vowels("Programming Language"))
```

Output:

```text
7
```

`text.lower()` makes the check case-insensitive. `character in "aeiou"` is true if the character occurs in that string. `count += 1` adds one (see [Relational, Logical and Assignment Operators](12-relational-logical-assignment-operators.md#assignment-operators)).

4.

```python
url = "https://example.com/page"

print(url.startswith("https"))
scheme, separator, rest = url.partition("://")
domain = rest.split("/")[0]
print(scheme, domain)
```

Output:

```text
True
https example.com
```

`partition("://")` splits at the first `://` and returns three parts. `rest` is `example.com/page`; splitting at `/` and taking the first item gives the domain.

5.

```python
def is_valid_pin(text):
    return len(text) == 4 and text.isdigit()


for candidate in ["1234", "12a4", "123", "-123"]:
    print(candidate, is_valid_pin(candidate))
```

Output:

```text
1234 True
12a4 False
123 False
-123 False
```

`isdigit()` rejects `"12a4"` and `"-123"`; the length check rejects `"123"`. The `and` operator is explained in [Relational, Logical and Assignment Operators](12-relational-logical-assignment-operators.md#logical-operators).

6. `"a,b,,c".split(",")` is `['a', 'b', '', 'c']` (the empty piece between the two commas is kept). `"a b  c".split()` is `['a', 'b', 'c']`. `" x ".strip().isalpha()` is `True`.

```python
print("a,b,,c".split(","))
print("a b  c".split())
print(" x ".strip().isalpha())
```

Output:

```text
['a', 'b', '', 'c']
['a', 'b', 'c']
True
```

---

## Chapter Summary and Key Takeaways

- Every character has a Unicode code point. `ord()` gives the number for one character and `chr()` gives the character for a number.
- Strings compare and sort by code point, so capitals sort before small letters unless you use a key such as `str.lower`.
- `len(text)` counts characters; encoding to UTF-8 gives bytes, which can be more.
- String methods never change the original; they return new values, so assign the result.
- Core tools: `upper`, `lower`, `strip`, `split`, `join`, `replace`, `find`, `index`, `count`, `startswith`, `endswith`, the `is...` tests, and `zfill`/`center`/`ljust`/`rjust`.
- `find` returns `-1` when it fails, `index` raises `ValueError`; `strip` removes a set of characters, not a word; `join` is called on the separator.

This completes Part 2's string material. Next: [Chapter 11 — Operators Overview and Arithmetic Operators](11-arithmetic-operators.md) begins Part 3 with the operators that compute with numbers.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
